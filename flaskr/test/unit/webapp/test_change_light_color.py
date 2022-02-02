from flask import request
import pytest
import json
from app import create_app, create_rest_api
from db import get_db
from change_light import is_aquarium_id_valid


@pytest.fixture
def client():
    local_app = create_app()
    create_rest_api(local_app)
    client = local_app.test_client()

    yield client

def get_max_aquarium_id():
    light_data = get_db().execute(
        'SELECT id, timestamp, default_mode, total_food_quantity'
        ' FROM aquarium'
        ' ORDER BY timestamp DESC'
        ).fetchone()
    return light_data['id']


def test_get_aquarium_light_color_invalid_id(client):
    with create_app().app_context():
        invalid_id = get_max_aquarium_id() + 1
    request = client.get('/lightColor/' + str(invalid_id))

    assert request.status_code == 403


def test_get_aquarium_light_color_valid_id(client):
    with create_app().app_context():
        valid_id = get_max_aquarium_id()
    request = client.get('/lightColor/' + str(valid_id))

    assert request.status_code == 200


def test_change_light_color_valid_aquarium_id(client):
    color = 'test_color'
    with create_app().app_context():
        valid_id = get_max_aquarium_id()

    request = client.put('/lightColor/' + str(valid_id) + '?color=' + color)

    assert request.status_code == 200


def test_change_light_color_invalid_aquarium_id(client):
    color = 'test_color'
    with create_app().app_context():
        invalid_id = get_max_aquarium_id() + 1

    request = client.put('/lightColor/' + str(invalid_id) + '?color=' + color)

    assert request.status_code == 403