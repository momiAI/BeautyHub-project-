import pytest

@pytest.mark.parametrize('name_specialization', [
    ('Лешмейкер'),
    ('Мастер маникюра'),
    ('Бровист')

])
async def test_add_specialization(login_admin,ac,name_specialization):
    response = await ac.post("/admin/specialization/add", json = {
        "name" : name_specialization
    })
    assert response.status_code == 200




@pytest.mark.parametrize('specialization_id,name_service,category,status_code', [
    (1,'Наращивание ресниц','lash',200),
    (2,'Наращивание ногтей', 'nails',200),
    (3,'Татуаж бровей','brows',200),
    (3,'Провека Enum','browss',422),
    (4,'Проверка дб на поиск','brows',200)
])
async def test_add_service(login_admin,ac,specialization_id,name_service,category,status_code):
    response = await ac.post(f'/admin/service-add/{specialization_id}', 
        params={"specialization_id" : specialization_id}, 
        json={        
        "name": name_service,
        "category": category
        })
    
    result = response.json()

    assert response.status_code == status_code
    assert "data" in result
    