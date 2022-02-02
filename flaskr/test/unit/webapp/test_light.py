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


def test_get_light(client):
    request = client.get("/light")
    assert request.status_code == 200


def test_set_light(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'intensity': 60, 'color': 'yellow',
               'schedule': '12:15-20:30'}
    rv = client.post('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Light settings successfully recorded"


def test_set_light_null(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'intensity': 60, 'color': '',
               'schedule': '12:15-20:30'}
    rv = client.post('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Color is required."


def test_update_light(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': light['id'], 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'intensity': 60,
               'color': 'purple', 'schedule': '10:45-22:30'}
    rv = client.put('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Light settings successfully updated"


def test_update_light_notfound(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY id DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': light['id'] + 1, 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'intensity': 60,
               'color': 'purple', 'schedule': '10:45-22:30'}
    rv = client.put('/light', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Light does not exist."


def test_delete_light(client):

    with create_app().app_context():
        light = get_db().execute(
            'SELECT id'
            ' FROM light'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/light/' + str(light['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Light successfully deleted."