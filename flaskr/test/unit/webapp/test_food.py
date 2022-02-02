import pytest
import json
from app import create_app
from db import get_db


@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_get_food(client):
    request = client.get("/food")
    assert request.status_code == 200


def test_set_food(client):
    payload = {'food': 'Sticks', 'quant': 200}
    rv = client.post('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food type successfully recorded"


def test_set_food_null(client):
    payload = {'food': "", 'quant': 200}
    rv = client.post('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 403
    assert res["status"] == 'Food type is required.'


def test_update_food(client):

    with create_app().app_context():
        food = get_db().execute(
            'SELECT id'
            ' FROM food'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    payload = {'id': food['id'], 'food': 'Tablets', 'quant': 100}
    rv = client.put('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food type successfully updated"


def test_update_food_notfound(client):

    with create_app().app_context():
        food = get_db().execute(
            'SELECT id'
            ' FROM food'
            ' ORDER BY id DESC'
        ).fetchone()
    payload = {'id': food['id'] + 1, 'food': 'Tablets', 'quant': 100}
    rv = client.put('/food', data=payload, follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 404
    assert res["status"] == "Food does not exist."


def test_delete_food(client):

    with create_app().app_context():
        food = get_db().execute(
            'SELECT id'
            ' FROM food'
            ' ORDER BY timestamp DESC'
        ).fetchone()
    rv = client.delete('/food/' + str(food['id']), follow_redirects=True)
    res = json.loads(rv.data.decode())
    assert rv.status_code == 200
    assert res["status"] == "Food type successfully deleted"