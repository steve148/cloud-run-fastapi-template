from fastapi.testclient import TestClient

from template_app.main import app

client = TestClient(app)


def test_get_main() -> None:
    response = client.get("/v1")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}
