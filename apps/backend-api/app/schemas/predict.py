from uuid import UUID

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    session_id: UUID
    actor_role: str
    pregnancies: int = Field(ge=0, le=30)
    glucose: float = Field(ge=0, le=300)
    blood_pressure: float = Field(ge=0, le=200)
    skin_thickness: float = Field(ge=0, le=100)
    insulin: float = Field(ge=0, le=1000)
    bmi: float = Field(ge=0, le=100)
    diabetes_pedigree_function: float = Field(ge=0, le=10)
    age: int = Field(ge=1, le=120)


class TopFactor(BaseModel):
    feature: str
    importance: float


class PredictResponse(BaseModel):
    request_id: UUID
    model_version_id: UUID
    predicted_label: bool
    risk_probability: float
    risk_band: str
    interpretation: str
    top_factors: list[TopFactor]
    latency_ms: int
    created_at: str
