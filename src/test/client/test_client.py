import pytest
from datetime import datetime,timedelta

@pytest.mark.parametrize('date,status_code', [
    (datetime.now() - timedelta(days=1),422),
    (datetime.now() + timedelta(days=1), 200),
    (datetime.now() + timedelta(1), 409)
])
async def test_subscribe_to_master(ac,login_client,db,date,status_code):
    master = await db.master.get_all()
    service = await db.service.get_all()
    response = await ac.post('/client/subscribe/', json= {
        "id_master": master[0].id,
        "id_service": service[0].id,
        "date_time": date.strftime("%Y-%m-%dT%H:%M")
    })

    assert response.status_code == status_code

@pytest.mark.parametrize('id_form,status_code,noop', [
    (1,200,None),
    (1,200,'No-op'),
    (2,404,None),

])
async def test_cancel_recording(ac,login_client,id_form,status_code,noop,db):
    response = await ac.patch(f'/client/cancel/{id_form}')
    result = response.json()

    if noop is not None:
        assert result['data'] == 'No-op'
    
    assert response.status_code == status_code