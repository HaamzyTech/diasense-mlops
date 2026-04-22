export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000";

export type PredictRequest = {
  session_id: string;
  actor_role: "patient" | "clinician";
  pregnancies: number;
  glucose: number;
  blood_pressure: number;
  skin_thickness: number;
  insulin: number;
  bmi: number;
  diabetes_pedigree_function: number;
  age: number;
};

export type PredictResponse = {
  request_id: string;
  model_version_id: string;
  predicted_label: boolean;
  risk_probability: number;
  risk_band: "low" | "moderate" | "high";
  interpretation: string;
  top_factors: Array<{ feature: string; importance: number }>;
  latency_ms: number;
  created_at: string;
};

export type OpsSummaryResponse = {
  services: Record<string, string>;
  active_model: Record<string, string>;
  latest_pipeline_status: string;
  latest_drift_status: string;
};

async function parseJson<T>(response: Response): Promise<T> {
  const body = await response.json().catch(() => null);
  if (!response.ok) {
    const detail = body && typeof body === "object" && "detail" in body ? String((body as { detail: unknown }).detail) : `HTTP ${response.status}`;
    throw new Error(detail);
  }
  return body as T;
}

export async function createPrediction(payload: PredictRequest): Promise<PredictResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/predict`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseJson<PredictResponse>(response);
}

export async function getPrediction(requestId: string): Promise<{ request: Record<string, unknown>; result: Record<string, unknown> }> {
  const response = await fetch(`${API_BASE_URL}/api/v1/predictions/${requestId}`, {
    cache: "no-store",
  });
  return parseJson(response);
}

export async function getOpsSummary(): Promise<OpsSummaryResponse> {
  const response = await fetch(`${API_BASE_URL}/api/v1/ops/summary`, {
    cache: "no-store",
  });
  return parseJson<OpsSummaryResponse>(response);
}
