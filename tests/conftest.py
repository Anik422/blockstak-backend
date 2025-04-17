import pytest
from fastapi.testclient import TestClient
from main import app
from app import config


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture(scope="session")
def token(client):
    response = client.post(
        "/token",
        data={"username": config.CLIENT_ID, "password": config.CLIENT_SECRET},
    )
    assert response.status_code == 200
    return response.json()["access_token"]
