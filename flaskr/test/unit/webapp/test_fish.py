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


def test_get_fish(client):
    request = client.get("/fish")
    assert request.status_code == 200


def test_set_fish(client):
    with create_app().app_context():
        fish_type_ids = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    fish_type_id = random.randint(0, len(fish_type_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'type_id': fish_type_ids[fish_type_id]['id'],
               'name': 'Bob', 'health': 100, 'birthday': '12/01/2022'}
    rv = client.post('/fish', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish successfully recorded."


def test_set_fish_null(client):
    with create_app().app_context():
        fish_type_ids = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    fish_type_id = random.randint(0, len(fish_type_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)
    payload = {'aquarium_id': aquarium_ids[aquarium_id]['id'], 'type_id': fish_type_ids[fish_type_id]['id'],
               'name': '', 'health': 100, 'birthday': '12/01/2022'}
    rv = client.post('/fish', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == "Fish name is required."


def test_update_fish(client):

    with create_app().app_context():
        fish = get_db().execute(
            'SELECT id'
            ' FROM fish'
            ' ORDER BY timestamp DESC'
        ).fetchone()
        fish_type_ids = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    fish_type_id = random.randint(0, len(fish_type_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)

    payload = {'id': fish['id'], 'aquarium_id': aquarium_ids[aquarium_id]['id'],
               'type_id': fish_type_ids[fish_type_id]['id'], 'name': 'Bill', 'health': 75, 'birthday': '10/10/2021'}
    rv = client.put('/fish', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish successfully updated"


def test_update_fish_notfound(client):

    with create_app().app_context():
        fish = get_db().execute(
            'SELECT id'
            ' FROM fish'
            ' ORDER BY id DESC'
        ).fetchone()
        fish_type_ids = get_db().execute(
            'SELECT id'
            ' FROM fish_type'
        ).fetchall()
        aquarium_ids = get_db().execute(
            'SELECT id'
            ' FROM aquarium'
        ).fetchall()

    fish_type_id = random.randint(0, len(fish_type_ids)-1)
    aquarium_id = random.randint(0, len(aquarium_ids)-1)

    payload = {'id': fish['id'] + 1, 'aquarium_id': aquarium_ids[aquarium_id]['id'],
               'type_id': fish_type_ids[fish_type_id]['id'], 'name': 'Bill', 'health': 75, 'birthday': '10/10/2021'}
    rv = client.put('/fish', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Fish does not exist."


def test_delete_fish(client):

    with create_app().app_context():
        fish = get_db().execute(
            'SELECT id'
            ' FROM fish'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': fish['id']}
    rv = client.delete('/fish', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Fish successfully deleted."