import { getPrediction } from "@/lib/api";

interface PageProps {
  params: Promise<{ requestId: string }>;
}

function parseTopFactors(explanation: unknown): Array<{ feature: string; importance: number }> {
  if (!explanation) return [];
  try {
    const parsed = typeof explanation === "string" ? JSON.parse(explanation) : explanation;
    const factors = (parsed as { top_factors?: Array<{ feature: string; importance: number }> }).top_factors;
    return Array.isArray(factors) ? factors : [];
  } catch {
    return [];
  }
}

export default async function ResultPage({ params }: PageProps) {
  const { requestId } = await params;

  try {
    const data = await getPrediction(requestId);
    const result = data.result ?? {};
    const topFactors = parseTopFactors(result.explanation);

    return (
      <main className="container">
        <section className="card">
          <h1>Prediction Result</h1>
          <p>
            Risk Band: <span className={`badge ${String(result.risk_band ?? "")}`}>{String(result.risk_band ?? "unknown")}</span>
          </p>
          <p>Probability: {result.risk_probability !== null && result.risk_probability !== undefined ? `${(Number(result.risk_probability) * 100).toFixed(2)}%` : "n/a"}</p>
          <p>
            Interpretation: {result.risk_band === "low" ? "Low predicted diabetes risk." : result.risk_band === "moderate" ? "Moderate predicted diabetes risk." : result.risk_band === "high" ? "High predicted diabetes risk." : "Unavailable."}
          </p>
          <h3>Top Contributing Factors</h3>
          {topFactors.length === 0 ? (
            <p>No factors returned.</p>
          ) : (
            <ul>
              {topFactors.map((item) => (
                <li key={item.feature}>
                  {item.feature}: {item.importance}
                </li>
              ))}
            </ul>
          )}
          <p className="disclaimer">Disclaimer: This tool provides decision support and is not a medical diagnosis.</p>
        </section>
      </main>
    );
  } catch (error) {
    return (
      <main className="container">
        <section className="card">
          <h1>Prediction Result</h1>
          <p className="error">Unable to load prediction: {error instanceof Error ? error.message : "Unknown error"}</p>
          <p className="disclaimer">Disclaimer: This tool provides decision support and is not a medical diagnosis.</p>
        </section>
      </main>
    );
  }
}
