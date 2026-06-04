from fastapi.testclient import TestClient


def test_list_prayers_returns_paginated_envelope(client: TestClient) -> None:
    response = client.get("/v1/prayers")
    assert response.status_code == 200
    body = response.json()
    assert body["totalItems"] == 1
    assert body["perPage"] == 20
    prayer = body["items"][0]
    assert prayer["status"] == "confirmed"
    assert prayer["category"]["group"]["slug"] == "emotion"
    assert prayer["type"]["slug"] == "prophetic"


def test_list_prayers_rejects_invalid_sort(client: TestClient) -> None:
    response = client.get("/v1/prayers", params={"sort": "drop"})
    assert response.status_code == 422


def test_list_prayers_caps_per_page(client: TestClient) -> None:
    response = client.get("/v1/prayers", params={"perPage": 500})
    assert response.status_code == 422


def test_random_prayer(client: TestClient) -> None:
    response = client.get("/v1/prayers/random")
    assert response.status_code == 200
    assert response.json()["id"] == "p1"


def test_get_prayer_by_id(client: TestClient) -> None:
    response = client.get("/v1/prayers/p1")
    assert response.status_code == 200
    assert response.json()["text"] == "اللهم اغفر لي وارحمني"


def test_submit_prayer_creates_pending(client: TestClient) -> None:
    response = client.post(
        "/v1/prayers",
        json={"text": "اللهم ارزقني الصبر", "category": "anxiety"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "pending"
    submitted = client.fake.created[0]  # type: ignore[attr-defined]
    assert submitted["status"] == "pending"
    assert submitted["category"] == "c1"
    assert submitted["text_original"] == "اللهم ارزقني الصبر"
    jobs = client.queue.jobs  # type: ignore[attr-defined]
    assert jobs == [("process_prayer", ("new1",))]


def test_submit_prayer_without_category(client: TestClient) -> None:
    response = client.post(
        "/v1/prayers",
        json={"text": "اللهم اشرح لي صدري"},
    )
    assert response.status_code == 201
    submitted = client.fake.created[0]  # type: ignore[attr-defined]
    assert "category" not in submitted
    assert submitted["status"] == "pending"


def test_submit_prayer_rejects_short_text(client: TestClient) -> None:
    response = client.post(
        "/v1/prayers",
        json={"text": "x", "category": "anxiety"},
    )
    assert response.status_code == 422
