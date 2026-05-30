from fastapi.testclient import TestClient


def test_list_groups(client: TestClient) -> None:
    response = client.get("/v1/groups")
    assert response.status_code == 200
    body = response.json()
    assert body[0]["slug"] == "emotion"


def test_get_group(client: TestClient) -> None:
    response = client.get("/v1/groups/emotion")
    assert response.status_code == 200
    assert response.json()["name"] == "المشاعر"


def test_get_missing_group_returns_404(client: TestClient) -> None:
    response = client.get("/v1/groups/missing")
    assert response.status_code == 404
    assert response.json()["error"]["code"] == "not_found"


def test_list_categories_expands_group(client: TestClient) -> None:
    response = client.get("/v1/categories")
    assert response.status_code == 200
    category = response.json()[0]
    assert category["slug"] == "anxiety"
    assert category["group"]["slug"] == "emotion"


def test_list_types(client: TestClient) -> None:
    response = client.get("/v1/types")
    assert response.status_code == 200
    assert response.json()[0]["slug"] == "prophetic"
