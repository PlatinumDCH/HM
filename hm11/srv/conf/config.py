from typing import Any
from pydantic import ConfigDict, field_validator, EmailStr
from pydantic_settings import BaseSettings

from srv.conf.loging_conf import global_logger as logger

class Settings(BaseSettings):
    PG_URL:str="postgresql+asyncpg://postgres:000000@localhost:5432/contacts"
    SECRET_KEY_JWT: str = "00000000000000000000000000000000"
    ALGORITHM: str = "HS256"
    MAIL_USERNAME:EmailStr = 'example@example.com'
    MAIL_PASSWORD: str|None = None
    MAIL_PORT: int = 587
    MAIL_SERVER: str = 'smtp.example.com'
    RABBITMQ_URL:str = 'http://localhost'
    REDIS_DOMAIN:str = 'http://localhost'
    REDIS_PORT:int = 6379
    REDIS_PASSWORD:str|None = None

    @field_validator('ALGORITHM')
    @classmethod
    def validate_algorithm(cls, value:str)->str:
        if value not in ['HS256', 'HS512']:
            logger.warning('Invalid algorithm')
            raise ValueError('Algorithm must be either HS256 or HS512')
        return value

    model_config = ConfigDict(extra='ignore',env_file=".env", env_file_encoding="utf-8")  # noqa

configuration = Settings()






