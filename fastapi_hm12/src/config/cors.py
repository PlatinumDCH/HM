from enum import Enum

class CorsIpBanned(Enum):
    IPS = [
        # ip_address('192.168.1.1'),
        # ip_address('192.168.1.2'),
        # ip_address('127.0.0.1')
    ]
    USER_AGENTS = [r'Googlebot',r'Python-urllib']

