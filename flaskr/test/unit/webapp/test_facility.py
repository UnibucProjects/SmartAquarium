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


def test_get_facility(client):
    request = client.get("/facility")
    assert request.status_code == 200


def test_set_facility(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'electricity': 1, 'movement_sensor': 1,
               'temperature_sensor': 1, 'filter_sensor': 1, 'weight_sensor': 1}
    rv = client.post('/facility', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "New facility list successfully recorded"


def test_set_facility_null(client):
    with create_app().app_context():
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'electricity': 1, 'movement_sensor': '',
               'temperature_sensor': 1, 'filter_sensor': 1, 'weight_sensor': 1}
    rv = client.post('/facility', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Movement sensor status is required."


def test_update_facility(client):

    with create_app().app_context():
        facility = get_db().execute(
            'SELECT id'
            ' FROM facility'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': facility['id'], 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'electricity': 1,
               'movement_sensor': 1, 'temperature_sensor': 0, 'filter_sensor': 1, 'weight_sensor': 0}
    rv = client.put('/facility', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Facility list successfully updated"


def test_update_facility_notfound(client):

    with create_app().app_context():
        facility = get_db().execute(
            'SELECT id'
            ' FROM facility'
            ' ORDER BY id DESC'
        ).fetchone()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'id': facility['id'] + 1, 'aquarium_id': aquarium_ids[aquarium_id]['id'], 'electricity': 1,
               'movement_sensor': 1, 'temperature_sensor': 0, 'filter_sensor': 1, 'weight_sensor': 0}
    rv = client.put('/facility', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Facility list does not exist."


def test_delete_facility(client):

    with create_app().app_context():
        facility = get_db().execute(
            'SELECT id'
            ' FROM facility'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/facility/' + str(facility['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Facility list successfully deleted"