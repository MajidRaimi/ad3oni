from typing import Any

import httpx

from src.shared.errors.exceptions import UpstreamError

_SUPERUSER_AUTH_PATH = "/api/collections/_superusers/auth-with-password"


class PocketBaseClient:
    def __init__(
        self, base_url: str, http: httpx.AsyncClient, email: str, password: str
    ) -> None:
        self._base_url = base_url.rstrip("/")
        self._http = http
        self._email = email
        self._password = password
        self._token: str | None = None

    @property
    def has_credentials(self) -> bool:
        return bool(self._email and self._password)

    async def authenticate(self) -> None:
        if not self.has_credentials:
            return
        response = await self._send(
            "POST",
            _SUPERUSER_AUTH_PATH,
            json={"identity": self._email, "password": self._password},
        )
        try:
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise UpstreamError(f"PocketBase authentication failed: {exc}") from exc
        self._token = response.json().get("token")

    async def list_records(
        self, collection: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        data = await self._request(
            "GET", f"/api/collections/{collection}/records", params=params
        )
        return data or {}

    async def get_first(
        self,
        collection: str,
        filter_: str,
        *,
        expand: str | None = None,
    ) -> dict[str, Any] | None:
        params: dict[str, Any] = {"filter": filter_, "perPage": 1, "skipTotal": True}
        if expand:
            params["expand"] = expand
        data = await self.list_records(collection, params)
        items: list[dict[str, Any]] = data.get("items", [])
        return items[0] if items else None

    async def create_record(
        self, collection: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        data = await self._request(
            "POST", f"/api/collections/{collection}/records", json=payload
        )
        return data or {}

    async def update_record(
        self, collection: str, record_id: str, payload: dict[str, Any]
    ) -> dict[str, Any]:
        data = await self._request(
            "PATCH",
            f"/api/collections/{collection}/records/{record_id}",
            json=payload,
        )
        return data or {}

    async def delete_record(self, collection: str, record_id: str) -> None:
        path = f"/api/collections/{collection}/records/{record_id}"
        response = await self._send("DELETE", path)
        if response.status_code == 401 and self.has_credentials:
            await self.authenticate()
            response = await self._send("DELETE", path)
        try:
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise UpstreamError(f"PocketBase request failed: {exc}") from exc

    async def _request(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> dict[str, Any] | None:
        response = await self._send(method, path, json=json, params=params)
        if response.status_code == 401 and self.has_credentials:
            await self.authenticate()
            response = await self._send(method, path, json=json, params=params)
        try:
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise UpstreamError(f"PocketBase request failed: {exc}") from exc
        data: dict[str, Any] = response.json()
        return data

    async def _send(
        self,
        method: str,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        headers = {"Authorization": self._token} if self._token else None
        try:
            return await self._http.request(
                method,
                f"{self._base_url}{path}",
                json=json,
                params=params,
                headers=headers,
            )
        except httpx.HTTPError as exc:
            raise UpstreamError(f"PocketBase request failed: {exc}") from exc
