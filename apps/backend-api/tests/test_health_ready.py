from fastapi.testclient import TestClient

from app.api.v1.endpoints import health
from app.main import app


class DummySession:
    def execute(self, *_args, **_kwargs):
        return None


def override_db():
    yield DummySession()


def test_health_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["service"] == "backend-api"
    assert body["version"] == "0.1.0"


def test_ready_endpoint(monkeypatch) -> None:
    app.dependency_overrides[health.get_db] = override_db

    class DummyResponse:
        status_code = 200

    class DummyClient:
        def __init__(self, *args, **kwargs):
            pass

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def get(self, _url):
            return DummyResponse()

    monkeypatch.setattr(health.httpx, "Client", DummyClient)

    client = TestClient(app)
    response = client.get("/api/v1/ready")
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ready"
    assert body["dependencies"]["postgres"] == "ok"
    assert body["dependencies"]["model_server"] == "ok"
    assert body["dependencies"]["mlflow_tracking"] == "ok"
    app.dependency_overrides.clear()
