
async def test_me(login_client,ac):
    response = await ac.get('/users/me')
    assert response.status_code == 200
    assert "data" in response.json()


async def test_refresh_coockies(login_client,ac):
    response = await ac.post('/users/refresh')
    assert response.status_code == 200
    assert "message" in response.json()


async def test_logout(login_client,ac):
    response = await ac.post('/users/logout')
    assert response.status_code == 200
    assert "message" in response.json()


async def test_login_user(ac):
    response = await ac.post('/users/login',json= {
        "phone": "+76362233441", 
        "password": "abcd1234"
    })
    result = response.json()
    assert response.status_code == 200
    assert 'message' in result
    assert len(response.cookies) ==2
    

async def test_delete(login_client,ac,db):
    response = await ac.delete('/users/delete')
    users = await db.user.get_all()
    assert response.status_code == 200
    assert "data" in response.json()



async def test_create(ac,db):
    response = await ac.post('/users/create', json={
        "phone" : "+76362233441",
        "name" : "Client",
        "password" : "abcd1234"
    })
    users = await db.user.get_all()
    client = await db.client.get_object(phone = "76362233441")
    result_response = response.json()
    

    assert "data" in result_response
    assert result_response["data"]["id"] == client.id_user