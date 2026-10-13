from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_list_images_returns_success():
    response = client.get("/images")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_missing_image_returns_404():
    response = client.get("/images/999999")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Image not found"
    }


def test_get_missing_image_calls_returns_404():
    response = client.get("/images/999999/calls")

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Image not found"
    }