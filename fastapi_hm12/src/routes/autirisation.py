from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_connection_db
from src.schemas import UserSchema



router = APIRouter(prefix='/auth', tags=['auth'])

@router.post('/signup')
async def signup(body: UserSchema, db:AsyncSession=Depends(get_connection_db)):
    pass
    return  {}

@router.post('/login')
async def login(body: OAuth2PasswordRequestForm=Depends(), 
                db:AsyncSession=Depends(get_connection_db)):
    pass
    return {}

@router.get('/refresh_token')
async def refresh_token(credentials:HTTPAuthorizationCredentials=Security(),db:AsyncSession=Depends(get_connection_db)):
    pass
    return {}