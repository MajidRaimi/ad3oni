import pytest
from fastapi.testclient import TestClient
from src.main import create_app
from src.shared.dependencies import get_pocketbase
from src.shared.ratelimit.limiter import limiter

from tests.conftest import FakePocketBase


@pytest.fixture
def limited_client() -> TestClient:
    app = create_app()
    app.dependency_overrides[get_pocketbase] = lambda: FakePocketBase()
    limiter.reset()
    limiter.enabled = True
    return TestClient(app)


def test_submit_is_rate_limited(limited_client: TestClient) -> None:
    payload = {"text": "اللهم ارزقني الصبر", "category": "anxiety"}
    statuses = [
        limited_client.post("/v1/prayers", json=payload).status_code for _ in range(6)
    ]
    limiter.reset()
    limiter.enabled = True

    assert statuses[:5] == [201, 201, 201, 201, 201]
    assert statuses[5] == 429
