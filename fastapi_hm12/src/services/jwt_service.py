from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from src.config import settings
import pytz

class JWTService:
    SECRET_KEY = settings.SECRET_KEY_JWT
    ALGORITHM = settings.ALGORITHM

    async def create_access_token(
            self, 
            data: dict, 
            expires_delta:Optional[float]=None)->str:
        to_encode = data.copy()
        unc_now = datetime.now(pytz.UTC)
        if expires_delta:
            expire = unc_now + timedelta(minutes=expires_delta)
        else:
            expire = unc_now + timedelta(minutes=20)
        to_encode.update(
            {'iat': datetime.now(pytz.UTC),  # time created token
             'exp': expire,  # finishing time token
             'scope': 'access_token'}  # token type
        )
        encoded_assess_token = jwt.encode(
            to_encode, 
            self.SECRET_KEY, 
            algorithm=self.ALGORITHM
            )
        return encoded_assess_token
        
    async def create_refresh_token(
            self, data: dict,
            expires_delta: Optional[float] = None) -> str:
        to_encode = data.copy()
        utc_now = datetime.now(pytz.UTC)
        if expires_delta:
            expire = utc_now + timedelta(seconds=expires_delta)
        else:
            expire = utc_now + timedelta(days=7)
        to_encode.update({
            'iat': datetime.now(pytz.UTC),  # time creates token
            'exp': expire,  # finisfing time token
            'scope': 'refresh_token'  # type token
        })
        encoded_refresh_token = jwt.encode(
            to_encode, 
            self.SECRET_KEY, 
            algorithm=self.ALGORITHM)
        return encoded_refresh_token
    
    async def decode_refresh_token(self, refresh_token: str) -> str:
        """return email from refresh token"""
        try:
            payload = jwt.decode(
            refresh_token, 
            self.SECRET_KEY, 
            algorithms=[self.ALGORITHM]
            )
            if payload['scope'] == 'refresh_token':
                email = payload['sub']
                return email
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Invalid scope for token'
                )
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail='Could not validate credentials'
                )