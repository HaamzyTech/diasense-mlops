import { getOpsSummary } from "@/lib/api";

export default async function OpsPage() {
  try {
    const summary = await getOpsSummary();

    return (
      <main className="container">
        <section className="card">
          <h1>Operations Summary</h1>

          <h3>Service Health</h3>
          <ul>
            {Object.entries(summary.services).map(([service, status]) => (
              <li key={service}>
                {service}: {status}
              </li>
            ))}
          </ul>

          <h3>Active Model</h3>
          <p>{summary.active_model.model_name} v{summary.active_model.model_version} ({summary.active_model.stage})</p>

          <h3>Latest Pipeline Run</h3>
          <p>{summary.latest_pipeline_status}</p>

          <h3>Latest Drift Summary</h3>
          <p>{summary.latest_drift_status}</p>

          <h3>Operational Tools</h3>
          <ul>
            <li><a href="http://localhost:8080" target="_blank">Airflow UI</a></li>
            <li><a href="http://localhost:5000" target="_blank">MLflow UI</a></li>
            <li><a href="http://localhost:9090" target="_blank">Prometheus UI</a></li>
            <li><a href="http://localhost:3001" target="_blank">Grafana UI</a></li>
          </ul>
        </section>
      </main>
    );
  } catch (error) {
    return (
      <main className="container">
        <section className="card">
          <h1>Operations Summary</h1>
          <p className="error">Unable to load ops summary: {error instanceof Error ? error.message : "Unknown error"}</p>
        </section>
      </main>
    );
  }
}
