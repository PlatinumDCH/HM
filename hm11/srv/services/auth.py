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



auth_service = Auth()