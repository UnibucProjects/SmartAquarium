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


def test_get_fish_type(client):
    request = client.get("/fish_type")
    assert request.status_code == 200


def test_set_fish_type(client):
    with create_app().app_context():
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    payload = {'name': 'Goldfish', 'min_temperature': 25, 'max_temperature': 28, 'min_light_intensity': 67,
               'max_light_intensity': 75, 'food_id': food_ids[food_id]['id']}
    rv = client.post('/fish_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish type successfully recorded"


def test_set_fish_type_null(client):
    with create_app().app_context():
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    payload = {'name': 'Goldfish', 'min_temperature': '', 'max_temperature': 28, 'min_light_intensity': 67,
               'max_light_intensity': 75, 'food_id': food_ids[food_id]['id']}
    rv = client.post('/fish_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Fish type min temperature is required."


def test_update_fish_type(client):

    with create_app().app_context():
        fish_types = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    payload = {'id': fish_types['id'], 'name': 'Koi', 'min_temperature': 23, 'max_temperature': 27,
               'min_light_intensity': 70, 'max_light_intensity': 74, 'food_id': food_ids[food_id]['id']}
    rv = client.put('/fish_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish type successfully updated"


def test_update_fish_type_notfound(client):

    with create_app().app_context():
        fish_types = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
            ' ORDER BY id DESC'
        ).fetchone()
        food_ids = get_db().execute(
            'SELECT id'
            ' FROM food'
        ).fetchall()

    food_id = random.randint(0, len(food_ids)-1)
    payload = {'id': fish_types['id'] + 1, 'name': 'Koi', 'min_temperature': 23, 'max_temperature': 27,
               'min_light_intensity': 70, 'max_light_intensity': 74, 'food_id': food_ids[food_id]['id']}
    rv = client.put('/fish_type', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Fish type does not exist."


def test_delete_fish_type(client):

    with create_app().app_context():
        fish_types = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/fish_type/' + str(fish_types['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish type successfully deleted"