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

class Auth:
    pwd_context = CryptContext(schemes = 'bcrypt',deprecated = 'auto',bcrypt__rounds = 6)




auth_service = Auth()