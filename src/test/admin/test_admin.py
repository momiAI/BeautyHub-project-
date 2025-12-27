import pytest


@pytest.mark.parametrize('specialization_id,name_service,category,status_code,data', [
    (1,'Наращивание ресниц','lash',200,'data'),
    (2,'Наращивание ногтей', 'nails',200,'data'),
    (3,'Татуаж бровей','brows',200,'data'),
    (3,'Провека Enum','browss',422,'detail'),
    (4,'Проверка дб на поиск','brows',404,'detail')
])
async def test_add_service(add_specialization,login_admin,ac,specialization_id,name_service,category,status_code,data):
    response = await ac.post(f'/admin/service-add/{specialization_id}', 
        params={"specialization_id" : specialization_id}, 
        json={        
        "name": name_service,
        "category": category
        })
    
    result = response.json()

    assert response.status_code == status_code
    assert data in result

@pytest.mark.parametrize('id_application,status_code', [
    (1,200),
    (2,404),
    (1,409)
])
async def test_confirm_application(ac,send_application_for_master,login_admin,id_application,status_code):
    response = await ac.post(f'/admin/master/confirm/{id_application}')
    
    assert response.status_code == status_code
    