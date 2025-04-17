from app import config


def test_token_valid_credentials(client):
    response = client.post(
        "/token",
        data={"username": config.CLIENT_ID, "password": config.CLIENT_SECRET}, 
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_token_invalid_credentials(client):
    response = client.post(
        "/token",
        data={"username": "invalid", "password": "wrong"},
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid client credentials"
