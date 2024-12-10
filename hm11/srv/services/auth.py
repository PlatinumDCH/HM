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

    async def create_access_token(self, data:dict, expires_delta:Optional[float]=None)->str:
        to_encode:dict = data.copy()
        utc_now:datetime = datetime.now(pytz.UTC)
        if expires_delta:
            expire:datetime = utc_now + timedelta(seconds=expires_delta)
        else:
            expire:datetime = utc_now + timedelta(minutes=15)
        to_encode.update(
            {'iat': datetime.now(pytz.UTC),
             'exp': expire,
             'scope': 'access_token'})
        encoded_assess_token:str = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_assess_token

    async def create_refresh_token(self, data:dict, expires_delta:Optional[float]=None)->str:
        to_encode:dict = data.copy()
        utc_now:datetime = datetime.now(pytz.UTC)
        if expires_delta:
            expire:datetime = utc_now + timedelta(seconds=expires_delta)
        else:
            expire:datetime = utc_now + timedelta(days=7)
        to_encode.update(
            {'iat': datetime.now(pytz.UTC),  # кода мы создали токен
             'exp': expire,  # сколько он будет жить
             'scope': 'refresh_token'})  # указание на refresh_token
        encoded_refresh_token:str = jwt.encode(to_encode, self.SECRET_KEY, self.ALGORITHM)
        return encoded_refresh_token

    async def decode_refresh_token(self, refresh_token:str):
        try:
            payload = jwt.decode(refresh_token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid scope for token')
        except JWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

    async def get_current_user(self, token:str=Depends(auth2_scheme),db:AsyncSession=Depends(get_db)):
        """Вытащить из БД пользователя чей токен получила функция
        процесс:
            --приходит токен jwt на сервер
            --эта функция разбирает jwt token
            --возвращаем пользователя с бд"""
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'})
        try:
            # Decode JWT
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            if payload['scope'] == 'access_token':
                email = payload['sub']  # subject
                if email is None:
                    raise credentials_exception
            else:
                return credentials_exception
        except JWTError as e:
            raise credentials_exception

        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user

    def create_email_token(self, data:dict):
        to_encode = data.copy()
        expire = datetime.now(pytz.UTC) + timedelta(days=7)
        to_encode.update(
            {'iat':datetime.now(pytz.UTC),
             'exp':expire}
        )
        token = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token


auth_service = Auth()