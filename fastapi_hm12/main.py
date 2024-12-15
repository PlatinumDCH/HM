from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_connection_db
from src.config import logger
from src.routes import contacts, autorisation, users
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware




BASE_DIR = Path('.')

app = FastAPI()

#без єтой штуку брузер не сможет виполнять запроси
allow_origins=['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=['*'],
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory='src/static'), name='static')

app.include_router(contacts.router, prefix="/api")
app.include_router(autorisation.router, prefix="/api")
app.include_router(users.router, prefix='/api')

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
    
