from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.entity.models import User


async def get_user_by_email(email:str, db:AsyncSession=Depends(get_db)):
    user_query = select(User).filter_by(email=email)
    user = await db.execute(user_query)
    user = user.scalar_one_or_none()
    return user