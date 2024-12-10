from fastapi import APIRouter, HTTPException, Depends, status, Security, Request
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.entity.models import UserToken, User
from srv.repository import users as repository_users
from srv.schemas.user import UserSchema, TokenSchema, UserResponse
from srv.schemas.email import RequestEmail
from rabbit_mq_service.mail_publisher import publish_message
from srv.services.auth import auth_service
from rabbit_mq_service.mail_producer import send_to_rabbitmq
from srv.conf.loging_conf import global_logger as logger

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(body: UserSchema, request:Request, db:AsyncSession=Depends(get_db))->User:
    #проверка на то что такого пользователя нет в БД
    exists_user = await repository_users.get_user_by_email(body.email, db)
    if exists_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail='Account already exists')
    #создаем нового пользователя
    body.password = auth_service.get_pass_hash(body.password)
    new_user = await repository_users.create_user(body, db)

    email_task = {
        'email': new_user.email,
        'username': new_user.username,
        'host': str(request.base_url)
    }
    await send_to_rabbitmq(email_task, queue_name='email_queue')
    return new_user

@router.post('/login', response_model=TokenSchema)
async def login(body: OAuth2PasswordRequestForm=Depends(), db:AsyncSession=Depends(get_db)):
    user = await repository_users.get_user_by_email(body.username, db) #usernmae->email
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='invalid email')
    if not user.confirmed:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Not confirmed email')
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
    token = credentials.credentials #токен извлекается из запроса
    email = await auth_service.decode_refresh_token(token) #декодируем refresh token, получаем email
    user = await repository_users.get_user_by_email(email, db)
    user_token_query = await db.execute(
        select(UserToken).filter_by(user_id=user.id)
    )
    user_refresh_token = user_token_query.scalar_one_or_none()
    try:
        if not user_refresh_token or user_refresh_token != token:
            logger.warning(f"Invalid refresh token for user: {user.email}")
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')
    except Exception as e:
        logger.error(f"Error processing refresh token for user: {email} - {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    # как новый логин, спрятано от пользователя
    new_access_token = await auth_service.create_access_token(data={'sub': user.email})
    new_refresh_token = await auth_service.create_refresh_token(data={'sub':user.email})
    await repository_users.update_token(user, new_refresh_token,db)
    return {'access_token': new_access_token,'refresh_token':new_refresh_token,'token_type':'bearer'}

@router.post('/request_email')
async def request_email(body:RequestEmail, request:Request,db:AsyncSession=Depends(get_db)):
    user = await repository_users.get_user_by_email(body.email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if user.confirmed:
        return {'message':'Your email is already confirmed'}
    message = {
                'email':user.email,
                'username':user.username,
                'host':str(request.base_url)}
    try:
        await publish_message(message)
    except Exception as err:
        logger.error(f"Error connecting to RabbitMQ: {err}")
        raise HTTPException(status_code=500, detail="Failed to process the request")

@router.get('/confirmed_email/{token}')
async def confirmed_email(token:str, db:AsyncSession=Depends(get_db)):
    email = await auth_service.get_email_from_token(token)
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Verification error')
    if user.confirmed:
        return {'message':'Your email already confirmed'}
    await repository_users.confirmed_email(email, db)
    return {'message': 'Email confirmed'}