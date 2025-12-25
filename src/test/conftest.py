import pytest

from src.main import app
from httpx import AsyncClient,ASGITransport
from src.database import async_session_maker,engine,Base
from src.utils.db_manager import DbManager
from src.config import settings
from src.test.static.users_dict import array_users_data


@pytest.fixture(scope='session',autouse=True)
async def ac():
    async with AsyncClient(transport=ASGITransport(app=app, base_url="http://test")) as ac:
        yield ac

@pytest.fixture(scope='session',autouse=True)
async def main():
    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope='function', autouse=True)
async def db():
    async with DbManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture(scope="session",autouse=True)
async def add_users(db):
    result = [await db.user.create(user) for user in array_users_data]

    print(result,len(result))


async def login_client(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233441", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


async def login_master(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233442", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


async def login_administrator(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233443", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


async def login_admin(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233444", 
        "password": "abcd1234"
    })
    assert response.status_code == 200

