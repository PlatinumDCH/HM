from fastapi import APIRouter, HTTPException,Request, Response, Depends,status
from fastapi.responses import FileResponse
from src.schemas import RequestEmail
from src.database import get_connection_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository import users as repository_users

from src.services import basic_service
from src.config import settings

router = APIRouter(prefix='/users', tags=['users'])


@router.post('/request_email')
async def request_email(body: RequestEmail, request:Request,
                        db:AsyncSession = Depends(get_connection_db)):
    
    user = await repository_users.get_user_by_email(body.email, db)
    if user.confirmed:
        return {"message": "Your email is already confirmed"}
    
    email_token = await basic_service.email_service.create_email_token({'sub':user.email})

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
    #получить email пользователя по токену который пришел
    email = await basic_service.jwt_service.decode_token(
        token, 
        settings.email_token
        )
    # вытянет пользователя по emeail
    user = await repository_users.get_user_by_email(email, db)

    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Verification error, user not found')
    
    if user.confirmed:
        return {'message':'Your email already confirmed'}
    
    await repository_users.confirmed_email(email, db)
    await repository_users.update_token(user, None, settings.email_token, db)
    return {'message': 'Email confirmed'}

@router.get('/{username}')
async def request_email(username: str, response: Response, db: AsyncSession = Depends(get_connection_db)):
    #logic save info < user open mail >
    return FileResponse("src/static/open_check.png", media_type="image/png", content_disposition_type="inline")



@router.post('/reset_password')
async def reset_password(request:Request, response: Response):
    # отправка писька на смену пароля 
    pass
