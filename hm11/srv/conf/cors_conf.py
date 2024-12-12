from enum import Enum
from ipaddress import ip_address

class CorsBaned(Enum):
    IPS = [
        ip_address('192.168.1.1'),
        ip_address('192.168.1.2'),
        ip_address('127.0.0.1')
              ]
    USER_AGENTS = [r'Googlebot', r'Python-urllib']


#бан по ip
# @app.middleware("http")
# async def ban_ips(request: Request, call_next: Callable):
#     ip = ip_address(request.client.host)
#     if ip in banned_ips:
#         return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "You are banned"})
#     response = await call_next(request)
#     return response
