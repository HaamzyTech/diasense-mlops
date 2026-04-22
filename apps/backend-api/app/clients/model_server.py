from typing import Any

import httpx


class ModelServerClient:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url

    async def invoke(self, dataframe_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        payload = {"dataframe_records": dataframe_records}
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(f"{self.base_url}/invocations", json=payload)
            response.raise_for_status()
            return response.json()
