import contextlib
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from src.config.configurate import settings
from src.config.get_logger import logger


class DatabaseSessionManager:
    def __init__(self, url:str):
        self._engine: AsyncEngine | None = create_async_engine(url)
        self._session_maker: async_sessionmaker =  async_sessionmaker(
            autoflush=False,
            autocommit=False,
            bind=self._engine
        )

    @contextlib.asynccontextmanager
    async def session(self):
        if self._session_maker is None:
            raise Exception ('Session is not initialized')
        session = self._session_maker()
        try:
            yield session
        except Exception as err:
            logger.error(f"Session rollback, exception: {err}")
            await session.rollback()
            raise
        finally:
            await session.close()

sessionmanager = DatabaseSessionManager(settings.PG_URL)

async def get_connection_db():
    async with sessionmanager.session() as session:
        yield session