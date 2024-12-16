from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_connection_db
from src.config import logger, configure_cors
from src.routes import contacts, autorisation, users
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from src.middleware import user_agent_ban_middleware
from src.middleware import banned_ips_middleware
from typing import Callable
import redis.asyncio as redis
from src.config import settings
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
async def lifespan(app:FastAPI):
    redis_client = await redis.Redis (
        host=settings.REDIS_DOMAIN,
        port=settings.REDIS_PORT,
        db=0,
        password=settings.REDIS_PASSWORD,
    )
    await FastAPILimiter.init(redis_client)
    yield 

app = FastAPI(lifespan=lifespan)

configure_cors(app)
@app.middleware('http')
async def add_user_agent_ban_middleware(request:Request, call_next: Callable):
    return await user_agent_ban_middleware(request, call_next)

@app.middleware('http')
async def add_banned_ip_middleware(request:Request, call_next: Callable):
    return await banned_ips_middleware(request, call_next)


app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(
    router = contacts.router, 
    prefix = "/api",
    dependencies=[Depends(RateLimiter(times=3,seconds=15))]
    )
app.include_router(
    router = autorisation.router, 
    prefix = "/api"
    )
app.include_router(
    router = users.router, 
    prefix = '/api'
    )

@app.get("/")
def index():
    return {"message": "Contact Application"}

@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_connection_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as err:    
        logger.critical('Database connection error, {err}')
        raise HTTPException(status_code=500, detail="Error connecting to the database")
    
