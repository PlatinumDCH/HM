from fastapi import APIRouter, HTTPException,Request, Response, Depends,status
from fastapi import Form
from fastapi.responses import FileResponse
from src.schemas import RequestEmail
from src.database import get_connection_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import users as repository_users
from src.schemas import ResetPassword
from src.schemas.validate_password import ConfirmPassword
from src.services import basic_service
from src.config import settings, logger
from pydantic import ValidationError
router = APIRouter(prefix='/users', tags=['users'])


@router.post('/request_email')
async def request_email(body: RequestEmail, request:Request,
                        db:AsyncSession = Depends(get_connection_db)):
    
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    email_token = await basic_service.email_service.create_service_email_token(
        {'sub':user.email},
        settings.email_token
        )

    email_task = {
                'email': user.email,
                'username': user.username,
                'host': str(request.base_url),
                'queue_name':'confirm_email',
                'token':email_token
                }
    await repository_users.update_token(
        user, 
        email_token,
        settings.email_token, 
        db
        )
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
    
    await repository_users.confirmed_email(email, db)
    await repository_users.update_token(user, None, settings.email_token, db)
    return {'message': 'Email confirmed'}

@router.get('/{username}')
async def request_email(username: str, response: Response, db: AsyncSession = Depends(get_connection_db)):
    logger.info(f'{username} open verifivation email')
    return FileResponse("src/static/open_check.png", media_type="image/png", content_disposition_type="inline")



@router.post('/reset_password')
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
    token: str = Form(...),
    new_psw:str = Form(...), 
    db:AsyncSession=Depends(get_connection_db)):
    try:
        email = await basic_service.jwt_service.decode_token(
            token, 
            settings.reset_password_token
            )
    except HTTPException as err:
        raise err

    user = await repository_users.get_user_by_email(email, db)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='Verification error, user not found'
            )
    
    try:
        validate_password = ConfirmPassword(new_psw=new_psw)
    except ValueError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err.errors()
        )



    identic_password = basic_service.password_service.verify_password(
        new_psw, 
        user.password
        )
    if identic_password:
        logger.warning(f'new password == old password, {user.username}, {new_psw}')
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail='New password is the same as old password'
            )
    hashed_password = basic_service.password_service.get_password_hash(new_psw)
    await repository_users.update_user_password(user, hashed_password, db)
    logger.info(f'{user.username} reset password')
    await repository_users.update_token(user, None, settings.reset_password_token, db)
    logger.info(f'{user.username} del reset_password_token')

    return {'message': 'password successfully updated' }

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory='src/services/templates')

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
