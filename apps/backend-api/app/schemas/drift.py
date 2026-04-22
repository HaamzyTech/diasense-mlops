from pydantic import BaseModel


class DriftFeature(BaseModel):
    feature_name: str
    baseline_mean: float
    current_mean: float
    baseline_variance: float
    current_variance: float
    psi: float | None = None
    ks_stat: float | None = None
    status: str


class DriftResponse(BaseModel):
    report_date: str
    overall_status: str
    features: list[DriftFeature]
