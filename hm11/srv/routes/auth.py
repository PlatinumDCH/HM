from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.repository import users as repository_users
from srv.schemas.user import UserSchema, TokenSchema, UserResponse
from srv.services.auth import auth_service

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, db:AsyncSession=Depends(get_db)):
    #проверка на то что такого пользователя нету в БД
    exists_user = await repository_users.get_user_by_email(body.email, db)
    if exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Account already exists')

    #создаем нового пользователя
    body.password = auth_service.get_pass_hash(body.password)
    new_user = await repository_users.create_user(body, db)
    return new_user

@router.post('/login', response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db) #usernmae->email
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid email')
    if not auth_service.verify_pass(body.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid pass')
    #создание токена
    access_token = await auth_service.create_access_token(data={'sub': user.email})
    refresh_token = await auth_service.create_refresh_token(data={'sub': user.email})
    await repository_users.update_token(user, refresh_token, db)
    return {'access_token': access_token, 'refresh_token':refresh_token, 'token_type':'bearer'}

@router.get('/refresh_token')
async def refresh_token(credentials:HTTPAuthorizationCredentials=Security(),db:AsyncSession=Depends(get_db)):
    pass
    return {}
