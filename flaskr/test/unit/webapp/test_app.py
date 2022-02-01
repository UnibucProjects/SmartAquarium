import pytest
import json
from app import create_app


@pytest.fixture
def client():
    local_app = create_app()
    client = local_app.test_client()

    yield client


def test_root_endpoint(client):
    landing = client.get("/")
    html = landing.data.decode()

    assert 'Hello, World!' in html
    assert landing.status_code == 200