import asyncio
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession


from main import app
from src.database.conection_postgres import get_connection_db
from src.entity.base_model import BaseModel as Base
from src.entity import UsersTable
from src.services import basic_service


SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

TestingSessionLocal = async_sessionmaker(
    autocommit=False, 
    autoflush=False,
    expire_on_commit=False,  # не закрывать пока мы сами не скажем
    bind=engine)

test_user={
    "username": "deadpool", 
    "email": "deadpool@example.com", 
    "password": "123456789"
    }


"""
scope="module" инициализаци соединения для кажого модуля-файлика
function - для кадой функции теста
class - иниц для каждого класса
session - один раз для всего тестирования
"""

@pytest.fixture(scope="module")
async def init_models_wrape():
    """создали фикстуру для модуля, которая будет перед каждым тестом
    дропать базу и там создавать тестового пользователя"""
    async def init_models():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        async with TestingSessionLocal() as session:
            hash_password = basic_service.password_service.get_password_hash
            current_user = UsersTable(
                **test_user,
                hashed_password = hash_password,
                confirmed = True,
                role='admin'
            )
            session.add(current_user)
            await session.commit()
    asyncio.run(init_models())

@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="module")
def client():
    # Dependency override

    async def override_get_db():
        session = TestingSessionLocal()

        try:
            yield session
        except Exception as err:
            print(err)
            await session.rollback()
        finally:
            await session.close()

    app.dependency_overrides[get_connection_db] = override_get_db

    yield TestClient(app)


@pytest.fixture(scope="module")
def user():
    return {"username": "deadpool", "email": "deadpool@example.com", "password": "123456789"}
