"use client";

import { useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import { createPrediction, type PredictRequest } from "@/lib/api";

const initialForm: PredictRequest = {
  session_id: crypto.randomUUID(),
  actor_role: "patient",
  pregnancies: 0,
  glucose: 120,
  blood_pressure: 70,
  skin_thickness: 20,
  insulin: 80,
  bmi: 25,
  diabetes_pedigree_function: 0.5,
  age: 30,
};

function validate(form: PredictRequest): string[] {
  const errors: string[] = [];
  if (!form.session_id) errors.push("Session ID is required.");
  if (!["patient", "clinician"].includes(form.actor_role)) errors.push("Role must be patient or clinician.");
  if (form.age < 1 || form.age > 120) errors.push("Age must be between 1 and 120.");
  if (form.glucose < 0 || form.glucose > 300) errors.push("Glucose must be between 0 and 300.");
  if (form.bmi < 0 || form.bmi > 100) errors.push("BMI must be between 0 and 100.");
  return errors;
}

export default function PredictPage() {
  const [form, setForm] = useState<PredictRequest>(initialForm);
  const [errors, setErrors] = useState<string[]>([]);
  const [serverError, setServerError] = useState<string>("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const hasErrors = useMemo(() => validate(form).length > 0, [form]);

  const updateNumber = (key: keyof PredictRequest) => (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = Number(event.target.value);
    setForm((prev) => ({ ...prev, [key]: Number.isFinite(value) ? value : 0 }));
  };

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const validationErrors = validate(form);
    setErrors(validationErrors);
    setServerError("");
    if (validationErrors.length > 0) return;

    try {
      setLoading(true);
      const response = await createPrediction(form);
      router.push(`/result/${response.request_id}`);
    } catch (error) {
      setServerError(error instanceof Error ? error.message : "Unable to submit prediction.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="container">
      <section className="card">
        <h1>Risk Prediction</h1>
        <form onSubmit={onSubmit}>
          <div className="grid">
            <label>
              Role
              <select value={form.actor_role} onChange={(e) => setForm((p) => ({ ...p, actor_role: e.target.value as "patient" | "clinician" }))}>
                <option value="patient">patient</option>
                <option value="clinician">clinician</option>
              </select>
            </label>
            <label>
              Age
              <input type="number" value={form.age} onChange={updateNumber("age")} />
            </label>
            <label>
              Pregnancies
              <input type="number" value={form.pregnancies} onChange={updateNumber("pregnancies")} />
            </label>
            <label>
              Glucose
              <input type="number" value={form.glucose} onChange={updateNumber("glucose")} />
            </label>
            <label>
              Blood Pressure
              <input type="number" value={form.blood_pressure} onChange={updateNumber("blood_pressure")} />
            </label>
            <label>
              Skin Thickness
              <input type="number" value={form.skin_thickness} onChange={updateNumber("skin_thickness")} />
            </label>
            <label>
              Insulin
              <input type="number" value={form.insulin} onChange={updateNumber("insulin")} />
            </label>
            <label>
              BMI
              <input type="number" step="0.1" value={form.bmi} onChange={updateNumber("bmi")} />
            </label>
            <label>
              Diabetes Pedigree Function
              <input type="number" step="0.0001" value={form.diabetes_pedigree_function} onChange={updateNumber("diabetes_pedigree_function")} />
            </label>
          </div>
          {errors.length > 0 && (
            <ul className="error">
              {errors.map((error) => (
                <li key={error}>{error}</li>
              ))}
            </ul>
          )}
          {serverError && <p className="error">{serverError}</p>}
          <button disabled={loading || hasErrors} type="submit">
            {loading ? "Submitting..." : "Predict Risk"}
          </button>
        </form>
        <p className="disclaimer">Disclaimer: This tool provides decision support and is not a medical diagnosis.</p>
      </section>
    </main>
  );
}
