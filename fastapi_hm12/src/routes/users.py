from fastapi import APIRouter, HTTPException,Request, Body
from fastapi import Response, Depends,status,UploadFile,File
from fastapi.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
import cloudinary.uploader
import cloudinary
import pickle

from src.schemas import ConfirmPassword, UserResponse
from src.repository import users as repository_users
from src.schemas import RequestEmail, ResetPassword
from src.database import get_connection_db
from src.config import settings, logger
from src.services import basic_service
from src.entity import UsersTable 


router = APIRouter(prefix='/users', tags=['users'])
templates = Jinja2Templates(directory='src/services/templates')


@router.get('/me',response_model=UserResponse, 
        dependencies=[Depends(RateLimiter(times=1, seconds=20 ))])
async def get_current_user(user:UsersTable=Depends(
    basic_service.auth_service.get_current_user)):
    try:
        logger.info('Reauest me andpoint')
        return user
    except Exception as err:
        logger.error(f'Error while getting current user: {err}')
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail='Too many reauests'
        )

@router.patch('/avatar', response_model=UserResponse,
        dependencies=[Depends(RateLimiter(times=1, seconds=20))])
async def get_current_user(
    file:UploadFile = File(),
    user:UsersTable = Depends(basic_service.auth_service.get_current_user),
    db:AsyncSession = Depends(get_connection_db)):
    public_id = f'uid43/{user.email}'
    resurs = cloudinary.uploader.upload(
        file.file,
        public_id=public_id,
        owerride=True
    )
    resurl_url = cloudinary.CloudinaryImage(public_id).build_url(
        width=250,
        height=250,
        crop='fill',
        version=resurs.get('version')
    )
    user = await repository_users.update_avatar_url(
        user.email,
        resurl_url,
        db
    )
    basic_service.auth_service.cashe.set(user.email, pickle.dumps(user))
    basic_service.auth_service.cashe.expire(user.email, 500)
    return user
    
@router.post('/request_email')
async def request_email(body: RequestEmail, request:Request,
                        db:AsyncSession = Depends(get_connection_db)):
    """ 
    body: email
    
    """
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    #create email token
    email_token = await basic_service.email_service.create_service_email_token(
        {'sub':user.email},
        settings.email_token
        )
    #create email data task
    email_task = {
                'email': user.email,
                'username': user.username,
                'host': str(request.base_url),
                'queue_name':'confirm_email',
                'token':email_token
                }
    #add email_token to UserTable 
    await repository_users.update_token(
        user, 
        email_token,
        settings.email_token, 
        db
        )
    # send task to rabbitmq service
    await basic_service.email_service.send_email(email_task, email_token)
    return {"message": "Check your email for confirmation."}

@router.get('/confirmed_email/{token}')
async def confirmed_email(
    token:str, 
    db:AsyncSession=Depends(get_connection_db)):
    
    email = await basic_service.jwt_service.decode_token(
        token, 
        settings.email_token
        )
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Verification error, user not found'
            )
    if user.confirmed:
        return {'message':'Your email already confirmed'}
    #change filed confirmed in UserTable
    await repository_users.confirmed_email(email, db)
    await repository_users.update_token(user, None, settings.email_token, db)
    return {'message': 'Email confirmed'}

@router.get('/{username}')
async def request_email(username: str, response: Response, db: AsyncSession = Depends(get_connection_db)):
    logger.info(f'{username} open verifivation email')
    return FileResponse("src/static/open_check.png", media_type="image/png", content_disposition_type="inline")

@router.post('/reset_password_request')
async def forgot_password(
    body: ResetPassword, 
    request:Request, 
    db:AsyncSession=Depends(get_connection_db)):
    """1.получить пользователя body.email -> get_user_by_emai
       2.проверка, есть ли он в БД
       3.создать токен сброса пароля
       4.создать data for email send service
       5.отправить email_task -> send_email
       """
    curent_user = await repository_users.get_user_by_email(body.email, db)
    if not curent_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    logger.info(f'Get curent user finifsh {curent_user.username}')
    re_pass_token = await basic_service.email_service.create_service_email_token(
        {'sub': curent_user.email},
        settings.reset_password_token)
    email_task = {
                'email': curent_user.email,
                'username': curent_user.username,
                'host': str(request.base_url),
                'queue_name':'reset_password',
                'token':re_pass_token
                }
    logger.info(f'toke = {re_pass_token}')
    await repository_users.update_token(
        curent_user, 
        re_pass_token,
        settings.reset_password_token, 
        db
        )
    await basic_service.email_service.send_email(email_task, re_pass_token)
    return {"message": "Check your email for resert password."}

"""
тело запроса token:str, password:str

из тела запроса извлекаем токен, из токена извлекаем email, заодно проверяем время жизни токена
извлекаем пользователя из bd
проверяем пароль (старый пароль == новый пароль)
если праль не совпадает,  захешировать, отправить в бд
удадение токена сброса пароля
                
"""

@router.post('/reset_password')
async def change_password(
    body: ConfirmPassword = Body(...),
    db:AsyncSession=Depends(get_connection_db)):
    logger.info('start change password')
    try:
        email = await basic_service.jwt_service.decode_token(
            body.token, 
            settings.reset_password_token
            )
    except HTTPException as err:
        raise err
    logger.info('get user')
    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Verification error, user not found'
            )
    logger.info('old_password == ? new_password ')
    identic_password = basic_service.password_service.verify_password(
        body.new_password, 
        user.password
        )
    if identic_password:
        logger.warning(f'new password == old password, {user.username}, {body.new_password}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='New password is the same as old password'
            )
    hashed_password = basic_service.password_service.get_password_hash(body.new_password)
    await repository_users.update_user_password(user, hashed_password, db)
    logger.info(f'{user.username} reset password')
    await repository_users.update_token(
        user, 
        None, 
        settings.reset_password_token, 
        db
        )
    logger.info(f'{user.username} del reset_password_token')
    return {'message': 'password successfully updated' }

@router.get('/reset_password_form/{token}')
async def reset_password_form(request: Request, token:str ):
    try:
        email = await basic_service.jwt_service.decode_token(
            token,
            settings.reset_password_token
        )
    except HTTPException as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Invalid or expired token'
        )
    
    return templates.TemplateResponse(
        'form_psw.html',
        {
            'request':request,
            'token':token,
        }
    )
