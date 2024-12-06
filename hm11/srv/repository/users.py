from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar

from srv.database.db import get_db
from srv.entity.models import User
from srv.schemas.user import UserSchema
from srv.conf.loging_conf import setup_logger

logger = setup_logger(__name__)

async def get_user_by_email(email:str, db:AsyncSession=Depends(get_db)):
    user_query = select(User).filter_by(email=email)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    return user


async def create_user(body:UserSchema, db:AsyncSession=Depends(get_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        logger.error(err)
    new_user = User(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
