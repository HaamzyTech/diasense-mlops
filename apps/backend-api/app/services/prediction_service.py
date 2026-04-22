from app.clients.model_server import ModelServerClient


class PredictionService:
    def __init__(self, model_server_client: ModelServerClient) -> None:
        self.model_server_client = model_server_client

    async def predict(self, payload: dict) -> list[dict]:
        # TODO: Validate and transform payload before model-server invocation.
        return await self.model_server_client.invoke([payload])
