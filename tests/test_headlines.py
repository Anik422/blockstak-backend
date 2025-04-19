from unittest.mock import patch


def test_get_top_headlines_by_country(client, token):
    response = client.get(
        "/news/headlines/country/us", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert isinstance(json_data["news"], list)
    assert isinstance(json_data["totalResults"], int)


def test_get_top_headlines_by_source(client, token):
    response = client.get(
        "/news/headlines/source/bbc-news", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert isinstance(json_data["news"], list)
    assert isinstance(json_data["totalResults"], int)


def test_filter_headlines_success(client, token):
    response = client.get(
        "/news/headlines/filter?country=us",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["status"] == "success"
    assert isinstance(json_data["news"], list)
    assert isinstance(json_data["totalResults"], int)


def test_filter_headlines_failed(client, token):
    with patch("requests.get") as mock_get:
        mock_get.return_value.status_code = 500
        mock_get.return_value.json.return_value = {"message": "Error fetching news"}

        response = client.get(
            "/news/headlines/filter?country=us&source=bbc-news",
            headers={"Authorization": f"Bearer {token}"},
        )
        assert response.status_code == 500
        assert response.json()["detail"] == "Error fetching news"
