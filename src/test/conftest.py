import pytest

from src.main import app
from httpx import AsyncClient,ASGITransport
from src.database import async_session_maker,engine,Base
from src.utils.db_manager import DbManager
from src.config import settings
from src.test.static.users_dict import array_users_data
from src.schemas.client import ClientDbSchema
from src.schemas.masters import MasterSpecializationCreateSchema,MasterDBSchema


@pytest.fixture
async def ac(main):
    async with AsyncClient(transport=ASGITransport(app=app),base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope='session',autouse=True)
async def main():
    assert settings.MODE == "TEST"

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

@pytest.fixture(autouse=False)
async def add_master(add_users,db):
    check = await db.master.get_all()
    if check == []:
        user = await db.user.get_object(phone = '76362233442')
        result = await db.master.create(MasterDBSchema(id_user=user.id,bio='Master test'))
        await db.commit()
        return result


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
async def login_client_for_master_1(add_users,ac):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233446", 
        "password": "abcd1234"
    })
    assert response.status_code == 200

@pytest.fixture(autouse=False)
async def login_master(add_master,ac):
    
    response = await ac.post('/users/login', json = {
        "phone": "+76362233442", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_administrator(ac,add_users):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233443", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def login_admin(ac,add_users):
    response = await ac.post('/users/login', json = {
        "phone": "+76362233444", 
        "password": "abcd1234"
    })
    assert response.status_code == 200


@pytest.fixture(autouse=False)
async def add_specialization(db):
    check = await db.master_specialization.get_all()
    if check == []:
        array_specialization = ["Лешмейкер", "Мастер маникюра" , "Бровист"]
        specialization = [await db.master_specialization.create(MasterSpecializationCreateSchema(name = spec)) for spec in array_specialization ]
        await db.commit()


@pytest.fixture(autouse=False)
async def send_application_for_master(ac,add_specialization,login_client_for_master,db):
    check = await db.master_request.get_all()
    if check == []:    
        response = await ac.post('/master/application',json= { 
                "bio_short": "Профессионал своего дела",
                "specializations": [
                    1,2
                    ],
                "portfolio": ["Возможная ссылка", "Другая ссылка"],
        })

        assert response.status_code == 200
    