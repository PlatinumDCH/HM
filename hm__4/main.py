from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
import mimetypes
from urllib.parse import urlparse
import socket
import json
import threading
from udp_server import run_udp_server
from config import ServerConfig

HTTP_ADDRESS = ServerConfig.HTTP_SERVER_ADDRESS.value
UDP_ADDRESS = ServerConfig.UDP_SERVER_ADDRESS.value


class MyServ(BaseHTTPRequestHandler):

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        post_data = self.rfile.read(content_length)

        self.send_to_udp_server(post_data)

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Data received and sent to UDP server!")

    def do_GET(self):

        parsed_path = urlparse(self.path)
        path = parsed_path.path

        if path == "/":
            file_path = Path("front-init") / "index.html"
            self.send_file(file_path)

        elif path == "/message.html":
            file_path = Path("front-init") / "message.html"
            self.send_file(file_path)

        elif path.startswith("/static/"):
            # path to static files
            file_path = Path() / self.path.lstrip("/")
            self.send_file(file_path)

        else:
            file_path = Path("front-init") / "error.html"
            self.send_file(file_path, status_code=404)

    def send_file(self, file_path, status_code=200):
        try:
            with open(file_path, "rb") as fh:
                content = fh.read()

                mime_type, *_ = mimetypes.guess_type(file_path)
                self.send_response(status_code)
                self.send_header(
                    "Content-Type", mime_type if mime_type else "text/plain"
                )
                self.send_header("Content-Length", len(content))
                self.end_headers()

                # send file content to clien
                self.wfile.write(content)

        except FileNotFoundError:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"404 Not Found: error.html does not exist.")

    def send_to_udp_server(self, data):

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:

            data_dict = {}
            for item in data.decode("utf-8").split("&"):
                key, value = item.split("=")
                data_dict[key] = value

            sock.sendto(json.dumps(data_dict).encode("utf-8"), UDP_ADDRESS)


if __name__ == "__main__":

    httpd = HTTPServer(HTTP_ADDRESS, MyServ)

    # run http-server
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    print("HTTP-server run in port 3000...")

    # run upd_server
    run_udp_server()
