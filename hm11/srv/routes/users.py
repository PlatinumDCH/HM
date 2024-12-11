from fastapi import APIRouter,HTTPException,Depends,status,Path,Query
from fastapi_limiter.depends import RateLimiter

from srv.entity.models import User, Role
from srv.schemas.user import UserResponse
from srv.services.auth import auth_service
from srv.conf.loging_conf import global_logger as logger


router = APIRouter(prefix='/users', tags=['users'])
@router.get('/me',
            response_model=UserResponse,
            dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(user:User=Depends(auth_service.get_current_user)):
    try:
        logger.info('Request to /me endpoint')
        return user
    except Exception as e:
        logger.error(f'Error while getting current user: {e}')
        raise HTTPException(status_code=429, detail="Too many requests")