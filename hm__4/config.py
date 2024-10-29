from enum import Enum


class ServerConfig(Enum):
    HTTP_SERVER_ADDRESS = ("", 3000)
    UDP_SERVER_ADDRESS = ("", 5000)
