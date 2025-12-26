import pytest

from src.main import app
from httpx import AsyncClient,ASGITransport
from src.database import async_session_maker,engine,Base
from src.utils.db_manager import DbManager
from src.config import settings
from src.test.static.users_dict import array_users_data
from src.schemas.client import ClientDbSchema


@pytest.fixture
async def ac(main):
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session',autouse=True)
async def main():
    assert settings.MODE == "TEST"
    print("FIXTURE MAIN STARTED")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=False)
async def db():
    async with DbManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture
async def add_users(main,db):
    check = await db.user.get_all()
    if check == []:
        result = [await db.user.create(user) for user in array_users_data]
        clients = [
                await db.client.create(ClientDbSchema(id_user=user.id,phone=user.phone,is_guest=False,rating=0.0))
                for user in result
                ]
        await db.commit()
        assert len(result) == 4
        assert len(clients) == 4
 

@pytest.fixture(autouse=False)
async def login_client(add_users,ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233441", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_client_for_master(add_users,ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233445", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_master(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233442", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_administrator(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233443", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_admin(ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233444", 
        "password": "abcd1234"
    })
    assert response.status_code == 200

@pytest.fixture(autouse=False)
async def add_specialization(db):
    array_specialization = ["Лешмейкер", "Мастер маникюра" , "Бровист"]
    specialization = [await db.master_specialization.create(name = spec) for spec in array_specialization ]
    print([model.id for model in specialization])
    #return [model.id for model in specialization]


@pytest.fixture(autouse=False)
async def send_application_for_master(add_specialization,login_client_for_master,ac):

    response = await ac.post('/master/application', json ={
##
    })
