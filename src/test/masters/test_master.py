import pytest
from datetime import datetime,timedelta

async def test_me(ac,login_master):
    response = await ac.get('/master/me')

    assert response.status_code == 200
    assert response.cookies.get('user_id')



@pytest.mark.parametrize('ids_specialization,status_code', [
    ([1,2],200),
    ([67,88],404)
])
async def test_send_application(ac,login_client_for_master_1,add_specialization,ids_specialization,status_code):
    response = await ac.post('/master/application', json= {
                "bio_short": "Профессионал своего дела",
                "specializations": [
                    1,
                    2
                ],
                "portfolio": ["Возможная ссылка", "Другая ссылка"],
    })
    assert response.status_code == status_code

@pytest.mark.parametrize('day,status_code', [
    (datetime.now(),200),
    (datetime.now() - timedelta(days=1),422)
])
async def test_add_day_off(ac,login_master,day,status_code):
    response = await ac.post('/master/day-off/add/', json={
        "day" : day.strftime("%Y-%m-%d"),
        "reason" : "заболела"
    })

    assert response.status_code == status_code