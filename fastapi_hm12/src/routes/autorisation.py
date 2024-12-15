from fastapi import APIRouter, Depends, Security
from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials
from fastapi import status, HTTPException, Request, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import HTTPAuthorizationCredentials
from fastapi.security import HTTPBearer
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_connection_db
from src.repository import users as repository_users
from src.schemas import UserSchema,UserResponse
from src.schemas import UserSchema, TokenSchema
from src.services import basic_service
from src.config import settings
from src.config import logger
from src.entity import UsersTable
from sqlalchemy.orm import selectinload

router = APIRouter(prefix='/auth', tags=['auth'])
get_refresh_token = HTTPBearer()

@router.post('/signup', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    body: UserSchema, 
    request:Request,
    db:AsyncSession=Depends(get_connection_db)
    ):
    """body: форма заполнения
       db: сессия базы данных """
    exists_user = await repository_users.get_user_by_email(body.email, db)
    if exists_user:
        logger.warning('user already exists')
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Account already exists'
            )
    
    body.password = basic_service.password_service.get_password_hash(body.password)

    new_user = await repository_users.create_user(body, db)
    email_token = await basic_service.email_service.create_service_email_token(
        {'sub':new_user.email},
        settings.email_token)

    email_task = {
                'email': new_user.email,
                'username': new_user.username,
                'host': str(request.base_url),
                'queue_name':'confirm_email',
                'token':email_token
                }
    await repository_users.update_token(
        new_user, 
        email_token,
        settings.email_token, 
        db
        )
    await basic_service.email_service.send_email(email_task, email_token)
    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email
    }
    
@router.post('/login')
async def login(body: OAuth2PasswordRequestForm=Depends(), 
                db:AsyncSession=Depends(get_connection_db))->dict:
    """_Aутентификация пользователя и выдача токенов доступа и обновления_

    Args:uyu
        OAuth2PasswordRequestForm = form_data, !NOT json
        nead feal:
            username:str [usefull email users]
            password:str XxX
            Optional:    scope: список областей доступа
            Optional:    grand_type: [usefull <password>] Для парольной аунт.
            Optional:    cliend id:xXx
            Optional:    client_secret: xXx
        (автоматически проверяет есть ли необходимые поля
        автоматически  извлекает данные из тела запроса
        автоматически так как Depends->вызывает функцию или класс)
        db (AsyncSession, optional): _асинхронная сессия базы данных_.

    Raises:
        HTTPException: _Invalid email_
        HTTPException: _Invalid password_

    Returns:
        dict: _dict{access_token:X, refresh_token:X, token_type:X}_
    """
    user = await repository_users.get_user_by_email(body.username, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='invalid email'
            )
    if not user.confirmed:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Account not confirmed, check email'
            )
    if not basic_service.password_service.verify_password(
        body.password, 
        user.password
        ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail='Invalid pass'
            )
    
    encoded_access_token = await basic_service.jwt_service.create_access_token(data={'sub': user.email})
    encoded_refresh_token = await basic_service.jwt_service.create_refresh_token(data={'sub': user.email})

    await repository_users.update_token(
        user, 
        encoded_refresh_token, 
        settings.refresh_token,
        db)
    return {
        'access_token': encoded_access_token, 
        'refresh_token':encoded_refresh_token, 
        'token_type':'bearer'
        }


@router.get('/refresh_token', response_model=TokenSchema)
async def refresh_token(
    credentials:HTTPAuthorizationCredentials=Security(get_refresh_token),
    db:AsyncSession=Depends(get_connection_db)):
    coming_refresh_token = credentials.credentials
    decode_email = await basic_service.jwt_service.decode_token(coming_refresh_token, settings.refresh_token)
    user = await repository_users.get_user_by_email(decode_email, db)
    old_refresh_token = await repository_users.get_token(user,settings.refresh_token, db)
    try:
        if not old_refresh_token or old_refresh_token != coming_refresh_token:
            logger.error('input RefreshToken != RefreshToken in db, or token not yiet in DB')
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Interval server error '
            )
    except Exception as err:
        logger.error(f'Error pocessing refresh token for user: {user.email}-{str(err)}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='Interval server error '
        )
    
    # псевдо-регистрация на сревере,выдача токенов
    new_access_token = await basic_service.jwt_service.create_access_token(
        data={'sub':user.email}
        )
    new_refresh_token = await basic_service.jwt_service.create_refresh_token(
        data={'sub':user.email}
        )
    await repository_users.update_token(user, new_refresh_token, settings.refresh_token, db)

    return {
        'access_token':new_access_token, 
        'refresh_token':new_refresh_token, 
        'token_type':'bearer'
        }
