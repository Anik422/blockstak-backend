def test_redirect_to_docs(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the API. Visit /docs for documentation."}
    assert response.headers["Content-Type"] == "application/json"