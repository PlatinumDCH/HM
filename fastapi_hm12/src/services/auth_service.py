from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import users as repository_users
from src.services.jwt_service import JWTService
from src.database import get_connection_db

class AuthService:
    auth2_scheme = OAuth2PasswordBearer(tokenUrl='api/auth/login')

    async def get_current_user(self, token: str = Depends(auth2_scheme), db: AsyncSession = Depends(get_connection_db)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Could not validate credentials',
            headers={'WWW-Authenticate': 'Bearer'}
        )
        try:
            payload = JWTService().decode_refresh_token(token)
            if payload['scope'] == 'access_token':
                email = payload['sub']  # Субъект (email)
                if email is None:
                    raise credentials_exception
            else:
                raise credentials_exception
        except JWTError as err:
            raise credentials_exception
        user = await repository_users.get_user_by_email(email, db)
        if user is None:
            raise credentials_exception
        return user