from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar
from typing import Optional

from srv.database.db import get_db
from srv.entity.models import User, UserToken
from srv.schemas.user import UserSchema
from srv.conf.loging_conf import global_logger as logger

async def get_user_by_email(email:str, db:AsyncSession=Depends(get_db))->Optional[User]:
    user_query = select(User).filter_by(email=email)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    return user


async def create_user(body:UserSchema, db:AsyncSession=Depends(get_db))->User:
    avatar:Optional[str] = None
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


async def update_token(user:User, token:str|None, db:AsyncSession):
    try:
        # проверка, существует ли токен дли данного пользователя
        user_query = select(UserToken).filter_by(user_id = user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()
        if user_token:
            user_query = (
                update(UserToken)
                .where(UserToken.user_id == user.id)
                .values(refresh_token=token)
            )
            await db.execute(user_query)
        else:
            # создать новую запись токена
            new_token = UserToken(user_id=user.id, refresh_token=token)
            db.add(new_token)
        await db.commit()
    except Exception as err:
        await db.rollback()
        logger.error(f"Failed to update user's token: {err}")
        raise err
    
async def update_reset_pasw_token(user:User, token:str|None, db:AsyncSession):
    try:
        user_query = select(UserToken).filter_by(user_id = user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()
        if user_token:
            user_query = (
                update(UserToken)
                .where(UserToken.user_id == user.id)
                .values(reset_password_token=token))
            await db.execute(user_query)
        else:
            new_token = UserToken(user_id=user.id, reset_password_token=token)
            db.add(new_token)
        await db.commit()
    except Exception as err:
        await db.rollback()
        logger.error(f'Failed to update reset password token: {err}')
        raise err

async def update_email_token(user:User, token:str|None, db:AsyncSession):
    try:
        user_query = select(UserToken).filter_by(user_id = user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()
        if user_token:
            user_query = (
                update(UserToken)
                .where(UserToken.user_id == user.id)
                .values(email_token=token))
            await db.execute(user_query)
        else:
            new_token = UserToken(user_id=user.id, email_token=token)
            db.add(new_token)
        await db.commit()
    except Exception as err:
        await db.rollback()
        logger.error(f'Failed to update reset password token: {err}')
        raise err

async def confirmed_email(email:str, db:AsyncSession)->None:
    user = await get_user_by_email(email, db) #получение почты пользователя
    user.confirmed = True # изменение поля confirmed
    await db.commit() # сохранить изменения

async def update_avatar_url(email: str, url: str | None, db: AsyncSession) -> User:
    user = await get_user_by_email(email, db)
    user.avatar = url
    await db.commit()
    await db.refresh(user)
    return user