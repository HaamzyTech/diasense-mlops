from typing import Any

import httpx

from app.core.config import get_settings
from app.core.exceptions import DependencyError


class ModelServerClient:
    def __init__(self, base_url: str | None = None) -> None:
        settings = get_settings()
        self.base_url = base_url or settings.model_server_url
        self.timeout = settings.request_timeout_seconds

    def invoke(self, dataframe_records: list[dict[str, Any]]) -> list[dict[str, Any]]:
        payload = {"dataframe_records": dataframe_records}
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.post(f"{self.base_url}/invocations", json=payload)
                response.raise_for_status()
                body = response.json()
                if not isinstance(body, list):
                    raise DependencyError("Invalid model-server response format")
                return body
        except (httpx.HTTPError, ValueError) as exc:
            raise DependencyError(f"Failed to call model-server: {exc}") from exc
