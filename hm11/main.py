from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from srv.database.db import get_db
from srv.routes import contacts
from srv.conf.loging_conf import global_logger as logger
from srv.routes import auth

app = FastAPI()

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

app.include_router(router=auth.router, prefix='/api')
app.include_router(router=contacts.router, prefix="/api")

@app.get("/")
def index()->dict:
    return {"message": "Contact Application"}


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