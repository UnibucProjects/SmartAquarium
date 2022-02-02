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


def test_get_feeding_schedule(client):
    request = client.get("/feeding_schedule")
    assert request.status_code == 200


def test_set_feeding_schedule(client):
    with create_app().app_context():
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'food_type_id': food_ids[food_id]['id'],
               'schedule': '12:45;20:00', 'available_type_quantity': 50}
    rv = client.post('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully recorded."


def test_set_feeding_schedule_null(client):
    with create_app().app_context():
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'food_type_id': food_ids[food_id]['id'],
               'schedule': '', 'available_type_quantity': 50}
    rv = client.post('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Schedule is required."


def test_update_feeding_schedule(client):

    with create_app().app_context():
        feeding_schedule = get_db().execute(
            'SELECT id'
            ' FROM feeding_schedule'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)

    payload = {'id': feeding_schedule['id'], 'aquarium_id': aquarium_ids[aquarium_id]['id'],
               'food_type_id': food_ids[food_id]['id'], 'schedule': '16:15', 'available_type_quantity': 100}
    rv = client.put('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully updated."


def test_update_feeding_schedule_notfound(client):

    with create_app().app_context():
        feeding_schedule = get_db().execute(
            'SELECT id'
            ' FROM feeding_schedule'
            ' ORDER BY id DESC'
        ).fetchone()
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)

    payload = {'id': feeding_schedule['id'] + 1, 'aquarium_id': aquarium_ids[aquarium_id]['id'],
               'food_type_id': food_ids[food_id]['id'], 'schedule': '16:15', 'available_type_quantity': 100}
    rv = client.put('/feeding_schedule', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Feeding schedule does not exist."


def test_delete_feeding_schedule(client):

    with create_app().app_context():
        feeding_schedule = get_db().execute(
            'SELECT id'
            ' FROM feeding_schedule'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/feeding_schedule/' + str(feeding_schedule['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Feeding schedule successfully deleted."