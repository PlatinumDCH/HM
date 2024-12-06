#autentification and create token

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt
import pytz

from srv.database.db import get_db
from srv.repository import users as repository_users
from srv.conf.config import SECRET_KEY as KEY
from srv.conf.config import ALGORITHM as ALGO

class Auth:
    pwd_context = CryptContext(schemes = 'bcrypt',deprecated = 'auto',bcrypt__rounds = 6)
    SECRET_KEY = KEY
    ALGORITHM = ALGO

    def verify_pass(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def get_pass_hash(self, password:str):
        return self.pwd_context.hash(password)

    auth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/login')

    async def create_access_token(self, data:dict, expires_delta:Optional[float]=None):
        to_encode = data.copy()
        utc_now = datetime.now(pytz.UTC)
        if expires_delta:
            expire = utc_now + timedelta(seconds=expires_delta)
        else:
            expire = utc_now + timedelta(minutes=15)
        to_encode.update(
            {'iat': datetime.now(pytz.UTC),  # кода мы создали токен
             'exp': expire,  # сколько он будет жить
             'scope': 'access_token'}  # указание именно access_token
        )
        encoded_assess_token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_assess_token

    async def create_refresh_token(self):
        pass
    async def decode_refresh_token(self):
        pass
    async def get_current_user(self):
        pass


auth_service = Auth()