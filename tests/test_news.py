def test_get_news(client, token):
    response = client.get("/news/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "news" in response.json()


def test_save_latest_news(client, token):
    response = client.post(
        "/news/save-latest", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert "message" in response.json()
