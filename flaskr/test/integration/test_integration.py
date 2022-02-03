import pytest
import json
import random
from app import create_app, create_mqtt_app
from db import get_db
import status
import time
from paho.mqtt.client import MQTT_ERR_SUCCESS


@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()
    with local_app.app_context():
        yield client


@pytest.fixture
def mqtt_client():
    local_app = create_app()
    mqtt = create_mqtt_app()
    with local_app.test_client():
        with local_app.app_context():
            yield mqtt


def test_mqtt_publishing(mqtt_client):
    message = json.dumps(status.get_status(), default=str)
    print(message)
    res = mqtt_client.publish('test message', message)
    assert res[0] == MQTT_ERR_SUCCESS


def test_utility_status_update(client):
    """
    Changes in resource availability should reflect in outputted status
    """
    # add new facility entry with everything functional
    payload = {'aquarium_id': 1, 'electricity': 1, 'movement_sensor': 1,
               'temperature_sensor': 1, 'filter_sensor': 1, 'weight_sensor': 1}
    rv = client.post('/facility', data=payload, follow_redirects=True)
    time.sleep(7)   # wait for update
    message = json.dumps(status.get_utility_status(), default=str)
    res = json.loads(rv.data.decode())

    expected_status = f"All utilities in aquarium 1 are working fine!"
    assert expected_status in message

    # break electricity
    with create_app().app_context():
        get_db().execute(
            'UPDATE facility'
            ' SET electricity=0'
            ' WHERE id=?',
            (res['data']['id'],)
        )
        get_db().commit()

    time.sleep(7)   # wait for update
    message = json.dumps(status.get_utility_status(), default=str)
    print(message)
    new_status = f"-Electricity in aquarium 1 seems to be broken. Please fix!-"
    assert new_status in message


