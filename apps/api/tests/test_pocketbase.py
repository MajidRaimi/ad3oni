import asyncio
from typing import Any, cast

import httpx
import pytest
from src.shared.errors.exceptions import UpstreamError
from src.shared.pocketbase.client import PocketBaseClient

_AUTH_PATH = "/api/collections/_superusers/auth-with-password"
_RECORDS_PATH = "/api/collections/prayers/records"


class FakeTransport:
    def __init__(self, *, stale_statuses: list[int] | None = None) -> None:
        self.valid_token: str | None = None
        self.auth_calls = 0
        self.write_calls = 0
        self.stale_statuses = stale_statuses or []
        self.auth_delay = 0.0

    def _response(self, status_code: int, payload: dict[str, Any]) -> httpx.Response:
        return httpx.Response(
            status_code,
            json=payload,
            request=httpx.Request("POST", "http://pb.test"),
        )

    async def request(
        self,
        method: str,
        url: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> httpx.Response:
        if url.endswith(_AUTH_PATH):
            self.auth_calls += 1
            if self.auth_delay:
                await asyncio.sleep(self.auth_delay)
            self.valid_token = f"token-{self.auth_calls}"
            return self._response(200, {"token": self.valid_token})

        self.write_calls += 1
        if self.stale_statuses:
            status = self.stale_statuses.pop(0)
            return self._response(
                status, {"message": "Only superusers can perform this action."}
            )
        token = (headers or {}).get("Authorization")
        if token != self.valid_token:
            return self._response(
                403, {"message": "Only superusers can perform this action."}
            )
        return self._response(200, {"id": "p1", "status": "pending"})


def _client(transport: FakeTransport, *, credentials: bool = True) -> PocketBaseClient:
    return PocketBaseClient(
        "http://pb.test",
        cast(httpx.AsyncClient, transport),
        "admin@ad3oni.com" if credentials else "",
        "secret" if credentials else "",
    )


@pytest.mark.asyncio
async def test_expired_token_403_triggers_reauth_and_retry() -> None:
    transport = FakeTransport(stale_statuses=[403])
    client = _client(transport)
    await client.authenticate()

    record = await client.create_record("prayers", {"text": "اللهم ارزقني الصبر"})

    assert record["id"] == "p1"
    assert transport.auth_calls == 2
    assert transport.write_calls == 2


@pytest.mark.asyncio
async def test_expired_token_401_still_triggers_reauth() -> None:
    transport = FakeTransport(stale_statuses=[401])
    client = _client(transport)
    await client.authenticate()

    record = await client.create_record("prayers", {"text": "اللهم اشرح لي صدري"})

    assert record["id"] == "p1"
    assert transport.auth_calls == 2


@pytest.mark.asyncio
async def test_delete_record_also_recovers_from_403() -> None:
    transport = FakeTransport(stale_statuses=[403])
    client = _client(transport)
    await client.authenticate()

    await client.delete_record("prayers", "p1")

    assert transport.auth_calls == 2
    assert transport.write_calls == 2


@pytest.mark.asyncio
async def test_persistent_403_is_not_retried_forever() -> None:
    transport = FakeTransport(stale_statuses=[403, 403])
    client = _client(transport)
    await client.authenticate()

    with pytest.raises(UpstreamError):
        await client.create_record("prayers", {"text": "اللهم اغفر لي"})

    assert transport.write_calls == 2


@pytest.mark.asyncio
async def test_missing_credentials_does_not_retry() -> None:
    transport = FakeTransport(stale_statuses=[403])
    client = _client(transport, credentials=False)
    await client.authenticate()

    with pytest.raises(UpstreamError):
        await client.create_record("prayers", {"text": "اللهم ارحمني"})

    assert transport.auth_calls == 0
    assert transport.write_calls == 1


@pytest.mark.asyncio
async def test_concurrent_stale_writes_reauthenticate_once() -> None:
    transport = FakeTransport(stale_statuses=[403] * 5)
    transport.auth_delay = 0.01
    client = _client(transport)
    await client.authenticate()

    results = await asyncio.gather(
        *(client.create_record("prayers", {"text": f"دعاء {index}"}) for index in range(5))
    )

    assert all(record["id"] == "p1" for record in results)
    assert transport.auth_calls == 2
