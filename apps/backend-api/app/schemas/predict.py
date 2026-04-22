from uuid import UUID

from pydantic import BaseModel


class PredictRequest(BaseModel):
    session_id: UUID
    actor_role: str
    pregnancies: int
    glucose: float
    blood_pressure: float
    skin_thickness: float
    insulin: float
    bmi: float
    diabetes_pedigree_function: float
    age: int
