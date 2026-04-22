from fastapi import FastAPI

from app.api.v1.api import api_router

app = FastAPI(title="backend-api", version="0.1.0")
app.include_router(api_router, prefix="/api/v1")


@app.get("/metrics")
def metrics() -> str:
    # TODO: Integrate Prometheus registry exposition.
    return "# TODO: Prometheus metrics exposition"
