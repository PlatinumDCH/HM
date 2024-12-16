from enum import Enum
from ipaddress import ip_address
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class CorsIpBanned(Enum):
    IPS = [
        ip_address('192.168.1.1'),
        ip_address('192.168.1.2'),
        ip_address('127.0.0.1')
    ]
    USER_AGENTS = [r'Googlebot',r'Python-urllib']

def configure_cors(app:FastAPI)->None:
    origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=['*']
    )
