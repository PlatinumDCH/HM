from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.schemas.user import UserSchema

router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/signup')
async def signup(body: UserSchema, db:AsyncSession=Depends(get_db)):
    pass
    return  {}

@router.post('/login')
async def login(body: OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    pass
    return {}

@router.get('/refresh_token')
async def refresh_token(credentials:HTTPAuthorizationCredentials=Security(),db:AsyncSession=Depends(get_db)):
    pass
    return {}
