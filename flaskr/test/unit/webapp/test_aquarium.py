import pytest
import json
from app import create_app
from db import get_db


@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_get_aquarium(client):
    request = client.get("/aquarium")
    assert request.status_code == 200


def test_set_aquarium(client):
    payload = {'name': 'Aquarium', 'mode': 'pet', 'total_quant': 0}
    rv = client.post('/aquarium', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Aquarium successfully recorded"


def test_set_aquarium_null(client):
    payload = {'name': 'Aquarium', 'mode': 'pet', 'total_quant': ''}
    rv = client.post('/aquarium', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Total quantity is required.'


def test_update_aquarium(client):

    with create_app().app_context():
        aquarium = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': aquarium['id'], 'name': 'Aquarium', 'mode': 'petshop', 'total_quant': 50}
    rv = client.put('/aquarium', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Aquarium successfully updated"


def test_update_aquarium_notfound(client):

    with create_app().app_context():
        aquarium = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': aquarium['id'] + 1, 'name': 'Aquarium', 'mode': 'petshop', 'total_quant': 50}
    rv = client.put('/aquarium', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Aquarium does not exist."


def test_delete_aquarium(client):

    with create_app().app_context():
        aquarium = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/aquarium/' + str(aquarium['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Aquarium successfully deleted"