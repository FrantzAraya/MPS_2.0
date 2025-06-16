"""Cliente HTTP para comunicarse con la API."""

import httpx

from server.database import settings


class APIClient:
    def __init__(self) -> None:
        self.base_url = f"http://127.0.0.1:{settings.api_port}"
        self.client = httpx.AsyncClient(base_url=self.base_url)

    async def get(self, ruta: str):
        resp = await self.client.get(ruta)
        resp.raise_for_status()
        return resp.json()

    async def post(self, ruta: str, data: dict):
        resp = await self.client.post(ruta, json=data)
        resp.raise_for_status()
        return resp.json()
