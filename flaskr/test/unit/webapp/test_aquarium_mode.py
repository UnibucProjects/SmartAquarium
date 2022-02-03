
from flask import request
import pytest
import json
from app import create_app, create_rest_api
from db import get_db

@pytest.fixture
def client():
    local_app = create_app()
    create_rest_api(local_app)
    client = local_app.test_client()

    yield client


def test_get_aquarium_invalid_id(client):

    with create_app().app_context():
        light_data = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY id DESC'
        ).fetchone()
    invalid_id = light_data['id'] + 1
    request = client.get('/aquariumMode/' + str(invalid_id))

    assert request.status_code == 403


def test_set_aquarium_with_invalid_id(client):
    with create_app().app_context():
        light_data = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
        ' ORDER BY id DESC'
        ).fetchone()
    invalid_id = light_data['id'] + 1
    valid_type = 'crescatorie';
    request = client.put('/aquariumMode/' + str(invalid_id) + '?type=' + valid_type)

    assert request.status_code == 403


def test_set_aquarium_with_invalid_type(client):
    with create_app().app_context():
        light_data = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
        ' ORDER BY id DESC'
        ).fetchone()
    valid_id = light_data['id']
    invalid_type = 'notCrescatorie'
    request = client.put('/aquariumMode/' + str(valid_id) + '?type=' + invalid_type)

    assert request.status_code == 403


def test_set_aquarium_with_valid_type(client):
    local_app = create_app()
    with local_app.app_context():
        light_data = get_db().execute(
        'SELECT id'
        ' FROM aquarium'
        ' ORDER BY id DESC'
        ).fetchone()

    valid_id = light_data['id']
    valid_type = 'crescatorie'
    request = client.put('/aquariumMode/' + str(1) + '?type=' + valid_type)

    res = json.loads(request.data.decode())
    assert request.status_code == 200
