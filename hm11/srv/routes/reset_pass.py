from fastapi import APIRouter, Depends, HTTPException,status, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from rabbit_mq_service.mail_publisher import publish_message
from srv.database.db import get_db
from srv.schemas.reset_pass import ResetPassword, ConfirmPassword
from srv.repository  import users as repository_users
from srv.services.auth import auth_service
from srv.conf.loging_conf import global_logger as logger

router = APIRouter()

@router.post('/password/reset',tags=["users"])
async def request_password_reset(data:ResetPassword,
                                 request:Request,
                                 db: AsyncSession = Depends(get_db)):
    user = await repository_users.get_user_by_email(data.email, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    task_data = {
        'email': user.email,
        'username': user.username,
        'host':str(request.base_url),
        'type': 'reset_password',
    }
    try:
         await publish_message(task_data, 'reset_password')
    except Exception as e:
        logger.error('Error connection to RabbitMQ')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error connection to RabbitMQ")
    return {"message": "Password reset link sent to your email"}

