from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from fastapi_mail.errors import ConnectionErrors
from pydantic import EmailStr
from pathlib import Path

from srv.services.auth import auth_service
from srv.conf.loging_conf import setup_logger
from srv.conf.config import mail,password,port,mail_server

logger = setup_logger(__name__)

conf = ConnectionConfig(
    MAIL_USERNAME=mail,
    MAIL_PASSWORD=password,
    MAIL_FROM=mail,
    MAIL_PORT=port,
    MAIL_SERVER=mail_server,
    MAIL_FROM_NAME='Contact server',
    MAIL_STARTTLS=False,
    MAIL_SSL_TLS=True,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    TEMPLATE_FOLDER=Path(__file__).parent/'templates'
)

async def send_email(email:EmailStr, username:str, host:str):
    try:
        token_verification = auth_service.create_email_token({'sub':email})
        message = MessageSchema(
            subject='Confirm your email',
            recipients=[email],
            template_body={'host':host, 'username':username, 'token':token_verification},
            subtype=MessageType.html
        )
        fm=FastMail(conf)
        await fm.send_message(message, template_name='veriy_email.html')
    except ConnectionErrors as err:
        logger.error(err)