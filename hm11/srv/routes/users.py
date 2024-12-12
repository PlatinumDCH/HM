import pickle
import cloudinary
import cloudinary.uploader

from fastapi import (
    APIRouter,
    File,
    HTTPException,
    Depends,
    status,
    Path,
    Query,
    UploadFile,
)
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession


from srv.entity.models import User
from srv.schemas.user import UserResponse
from srv.services.auth import auth_service
from srv.conf.loging_conf import global_logger as logger
from srv.database.db import get_db
from srv.conf.config import configuration
from srv.repository import users as repository_users

router = APIRouter(prefix="/users", tags=["users"])
cloudinary.config(
    cloud_name=configuration.CLD_NAME,
    api_key=configuration.CLD_API_KEY,
    api_secret=configuration.CLD_API_SECRET,
    secure=True,
)


@router.get(
    "/me",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(user: User = Depends(auth_service.get_current_user)):
    try:
        logger.info("Request to /me endpoint")
        return user
    except Exception as e:
        logger.error(f"Error while getting current user: {e}")
        raise HTTPException(status_code=429, detail="Too many requests")


@router.patch(
    "/avatar",
    response_model=UserResponse,
    dependencies=[Depends(RateLimiter(times=1, seconds=20))],
)
async def get_current_user(
    file: UploadFile = File(),
    user: User = Depends(auth_service.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    public_id = f'uid43/{user.email}'
    resurs = cloudinary.uploader.upload(
        file.file, 
        public_id=public_id,
        owerride=True)
    resurs_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250,
        height=250,
        crop="fill",
        version=resurs.get('version')
    )
    user = await repository_users.update_avatar_url(user.email, resurs_url, db)
    auth_service.cache.set(user.email, pickle.dumps(user))
    auth_service.cache.expire(user.email, 500)
    return user
