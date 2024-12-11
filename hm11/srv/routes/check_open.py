from fastapi import APIRouter, Depends, Response
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession

from srv.database.db import get_db
from srv.conf.loging_conf import global_logger as logger

router = APIRouter(prefix='/check', tags=['open_check'])

@router.get('/{username}')
async def request_email(username:str, response:Response, db: AsyncSession = Depends(get_db)):
    logger.info(f'{username} open link')
    return FileResponse('srv/static/open_check.png', media_type='image/png', content_disposition_type='inline')
