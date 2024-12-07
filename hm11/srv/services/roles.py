from fastapi import Request, Depends, HTTPException, status

from srv.entity.models import Role, User
from srv.services.auth import auth_service
from srv.conf.loging_conf import setup_logger

logger = setup_logger(__name__)

class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles

    async def __call__(self, request: Request, user: User = Depends(auth_service.get_current_user)):
        logger.info(user.role, self.allowed_roles)
        if user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="FORBIDDEN"
            )