import pytest
import json
import random
from app import create_app
from db import get_db


@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_get_water(client):
    request = client.get("/water")
    assert request.status_code == 200


def test_set_water(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'pH': 7, 'oxygen': 80, 'bacteria': 0,
               'temperature': 25}
    rv = client.post('/water', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Water successfully recorded"


def test_set_water_null(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'pH': 7, 'oxygen': 80, 'bacteria': 0,
               'temperature': ''}
    rv = client.post('/water', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Temperature value is required"


def test_update_water(client):

    with create_app().app_context():
        water = get_db().execute(
            'SELECT id'
            ' FROM water'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': water['id'], 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'pH': 5, 'oxygen': 70, 'bacteria': 1,
               'temperature': 28}
    rv = client.put('/water', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Water successfully updated"


def test_update_water_notfound(client):

    with create_app().app_context():
        water = get_db().execute(
            'SELECT id'
            ' FROM water'
            ' ORDER BY id DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': water['id'] + 1, 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'pH': 5, 'oxygen': 70,
               'bacteria': 1, 'temperature': 28}
    rv = client.put('/water', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Water does not exist."


def test_delete_water(client):

    with create_app().app_context():
        water = get_db().execute(
            'SELECT id'
            ' FROM water'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/water/' + str(water['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Water successfully deleted"