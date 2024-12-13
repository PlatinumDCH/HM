from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from src.database import get_connection_db
from src.config import logger
from src.routes import contacts
from src.routes import autirisation

app = FastAPI()
app.include_router(contacts.router, prefix="/api")
app.include_router(autirisation.router, prefix="/api")

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