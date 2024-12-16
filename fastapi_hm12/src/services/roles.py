from fastapi import Request, Depends, HTTPException, status

from src.services.basic import basic_service
from src.entity import Role, UsersTable
from src.config import logger

class RoleAccess:
    def __init__(self, allowed_roles: list[Role]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, request: Request,
                       user:UsersTable = Depends(basic_service.auth_service.get_current_user)):
        logger.info(user.role, self.allowed_roles)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Forbidden'
        )