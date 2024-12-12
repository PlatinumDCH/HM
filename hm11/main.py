import re
from pathlib import Path
from typing import Callable
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from fastapi.staticfiles import StaticFiles

from srv.database.db import get_db
from srv.routes import contacts, auth, check_open, users
from srv.conf.loging_conf import global_logger as logger
from srv.conf.config import configuration
from srv.conf.cors_conf import CorsBaned

async def lifespan(app: FastAPI):
    r = await redis.Redis(
        host=configuration.REDIS_DOMAIN,
        port=configuration.REDIS_PORT,
        db=0,
        password=configuration.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(r)
    yield

app = FastAPI(lifespan=lifespan)

#функция для создания CORS
def configure_cors(app:FastAPI)->None:
    origins = ['*']
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

configure_cors(app)

@app.middleware('http')
async def user_agent_ban_niddleware(request:Request, call_next: Callable):
    user_agent = request.headers.get('user-agent')
    for ban_pattern in CorsBaned.USER_AGENTS.value:
        if re.search(ban_pattern, user_agent):
            return JSONResponse(
                status_code=status.HTTP_403_FORBIDDEN, 
                content={"detail": "You are baned"})
    response = await call_next(request)
    return response

BASE_DIR = Path('.')

app.mount('/static', StaticFiles(directory=BASE_DIR/'srv/static'), name ='static')

app.include_router(router=check_open.router, prefix='/api', dependencies=[Depends(RateLimiter(times=2,seconds=60))])
app.include_router(router=auth.router, prefix='/api')
app.include_router(router=contacts.router, prefix="/api",dependencies=[Depends(RateLimiter(times=3, seconds=20))])
app.include_router(users.router, prefix="/api")



templates = Jinja2Templates(directory=BASE_DIR/'srv/templates')

@app.get("/", response_class=HTMLResponse)
def index(request: Request)->dict:
    return templates.TemplateResponse('index.html', context={'request':request,
                                                             'our':'Build with FastAPI'})


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db))->dict:
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        logger.error(f'Database connection error: {e}')
        raise HTTPException(status_code=500, detail="Error connecting to the database")