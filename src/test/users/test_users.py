
async def me(login_client,ac):
    response = await ac.get('/users/me')
    print(response.json())
    assert response.status_code == 200