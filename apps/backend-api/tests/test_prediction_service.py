from app.services.prediction_service import interpretation_for_band, map_risk_band


class DummyPredictionRepo:
    def create_request(self, _payload):
        return {"id": "22222222-2222-2222-2222-222222222222"}

    def create_result(self, _payload):
        return {"id": "1", "created_at": "2026-04-21T12:00:00Z"}


class DummyModelRepo:
    def get_active(self):
        return {"id": "33333333-3333-3333-3333-333333333333"}


class DummyClient:
    def invoke(self, _records):
        return [{"predicted_label": True, "risk_probability": 0.9, "top_factors": []}]


def test_risk_band_mapping() -> None:
    assert map_risk_band(0.1) == "low"
    assert map_risk_band(0.33) == "moderate"
    assert map_risk_band(0.65) == "moderate"
    assert map_risk_band(0.66) == "high"


def test_interpretation_mapping() -> None:
    assert interpretation_for_band("low").startswith("Low predicted")
    assert interpretation_for_band("moderate").startswith("Moderate predicted")
    assert interpretation_for_band("high").startswith("High predicted")
