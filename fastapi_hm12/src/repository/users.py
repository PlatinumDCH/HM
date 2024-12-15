from fastapi import Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from libgravatar import Gravatar
from sqlalchemy.orm import joinedload
from src.database import get_connection_db
from src.entity import UsersTable, UserTokensTable
from src.schemas import UserSchema
from src.config  import logger

async def get_user_by_email(email:str, db:AsyncSession=Depends(get_connection_db))->UsersTable|None:
    """возвращает объект вользователя из БД"""
    user_query = select(UsersTable).filter_by(email=email)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    return user

async def create_user(body:UserSchema, db:AsyncSession=Depends(get_connection_db)):
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as err:
        logger.error(err)
    new_user = UsersTable(**body.model_dump(), avatar=avatar)
    db.add(new_user)
    await db.commit()
    # await db.refresh(new_user)
    await db.refresh(new_user)
    return new_user

async def update_token(user, token:str,
                       token_type:str, db:AsyncSession):
    try:
        # проверка, существует ли токен для данного пользователя
        user_query = select(UserTokensTable).filter_by(user_id = user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()

        if user_token:
            update_query = (
                update(UserTokensTable)
                .where(UserTokensTable.user_id == user.id)
                .values(**{token_type: token})
            )
            await db.execute(update_query)
            new_token = user_token
            
        else:
            new_token = UserTokensTable(user_id=user.id, **{token_type: token})
            db.add(new_token)
            

        await db.commit()
        await db.refresh(new_token)

    except Exception as err:
        await db.rollback()
        logger.error(f"Failed to update user's token: {err}/{token_type}")
        raise err
    
async def get_token(user:UsersTable, token_type:str, db:AsyncSession)->str|None:
    """_Извлекает указанные тип токена пользователя из БД_

    Args:
        user (UsersTable): _обьект пользователя из БД_
        token_type (str): _тип нужного токена_
        db (AsyncSession): _ассинхронная сессия с БД_

    Returns:
        str|None: _encoded token:str  or  None_
    """
    try:
        user_query = select(UserTokensTable).filter_by(user_id=user.id)
        result = await db.execute(user_query)
        user_token = result.scalar_one_or_none()

        if user_token:
            return getattr(user_token, token_type, None)
        else:
            return None
    except Exception as err:
        logger.error(f'Failed to get user token: {err}/{token_type}')
        raise err

async def confirmed_email(email:str, db:AsyncSession)->None:
    user = await get_user_by_email(email, db) 
    user.confirmed = True 
    await db.commit()
    await db.refresh(user)