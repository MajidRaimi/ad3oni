from fastapi.testclient import TestClient
from src.main import create_app

client = TestClient(create_app())


def test_ping_returns_pong() -> None:
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.text == "pong"


def test_health_reports_ok() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["environment"] == "dev"
