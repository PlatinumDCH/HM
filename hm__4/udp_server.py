import socket
import json
from pathlib import Path
from datetime import datetime
import config


def run_udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(config.ServerConfig.UDP_SERVER_ADDRESS.value)

    print("UDP server started on", config.ServerConfig.UDP_SERVER_ADDRESS.value)
    messages = {}

    storage_path = Path("storage")
    storage_path.mkdir(exist_ok=True)
    data_file = storage_path / "data.json"

    if data_file.exists() and data_file.stat().st_size > 0:
        try:
            with open(data_file, "r") as json_file:
                messages = json.load(json_file)
        except json.JSONDecodeError:
            print(
                "Error: Invalid JSON format in data.json. Initializing with empty messages."
            )
            messages = {}
    else:
        messages = {}

    while True:
        data, addr = sock.recvfrom(1024)
        try:
            data_dict = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError:
            print("Error decoding JSON.")
            continue

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        messages[timestamp] = data_dict

        with open(data_file, "w") as json_file:
            json.dump(messages, json_file, indent=2)
