from typing import Optional
from datetime import datetime, timedelta
import pytz
from jose import JWTError, jwt
from src.config import settings, logger
from src.schemas import UserSchema
from fastapi import Request
from src.services.rabbitmq_servise.produser import send_to_rabbit 


class EmailService:
    SECRET_KEY = settings.SECRET_KEY_JWT
    ALGORITHM = settings.ALGORITHM

    async def creare_email_token(self, data:dict, expires_delta:Optional[float]=None):
        to_encode = data.copy()
        unc_now = datetime.now(pytz.UTC)
        if expires_delta:
            expire = unc_now + timedelta(hours=expires_delta)
        else:
            expire = unc_now + timedelta(hours=12)
        to_encode.update({
            'exp':expire,
            'iat':datetime.now(pytz.UTC),
            'scope': 'email_token'
        })
        encoded_email_token = jwt.encode(
            to_encode, 
            self.SECRET_KEY, 
            algorithm=self.ALGORITHM
            )
        return encoded_email_token
    
    
    async def send_email(self, user:UserSchema, request:Request, email_token:Optional[str]=None):
        email_task = {
            'email': user.email,
            'username': user.username,
            'host': str(request.base_url),
            'queue_name':'confirm_email',
            'token':email_token
            }
        try:
            logger.info(f'Sending email task to RabbitMQ: {email_task} ')
            await send_to_rabbit(email_task)
        except Exception as err:
            logger.error(f'Failed to send email task to RabbitMQ: {err}')
            raise
        



email_service = EmailService()

        