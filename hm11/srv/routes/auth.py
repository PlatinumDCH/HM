from fastapi import APIRouter, HTTPException, Depends, status, Path, Query, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.entity.models import UserToken
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
    new_access_token = await auth_service.create_access_token(data={'sub': user.email})
    new_refresh_token = await auth_service.create_refresh_token(data={'sub': user.email})
    await repository_users.update_token(user, new_refresh_token, db)
    return {'access_token': new_access_token, 'refresh_token':new_refresh_token, 'token_type':'bearer'}

@router.get('/refresh_token',response_model=TokenSchema)
async def refresh_token(credentials:HTTPAuthorizationCredentials=Security(get_refresh_token),
                        db:AsyncSession=Depends(get_db)):
    token = credentials.credentials #получаем refresh token из БД
    email = await auth_service.decode_refresh_token(token) #декодируем refresh token, получаем email
    user = await repository_users.get_user_by_email(email, db)
    user_token_query = await db.execute(
        select(UserToken).filter_by(user_id=user.id)
    )
    user_refresh_token = user_token_query.scalar_one_or_none()
    if not user_refresh_token or user_refresh_token != token:
        if user_refresh_token:
            await repository_users.update_token(user, token, db)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    # как новый логин, спрятано от пользователя
    new_access_token = await auth_service.create_access_token(data={'sub': user.email})
    new_refresh_token = await auth_service.create_refresh_token(data={'sub':user.email})
    await repository_users.update_token(user, new_refresh_token,db)
    return {'access_token': new_access_token,'refresh_token':new_refresh_token,'token_type':'bearer'}
