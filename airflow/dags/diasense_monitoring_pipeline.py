import os
from datetime import datetime, timezone

import psycopg2
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


def persist_drift_report_to_db(**context):
    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "diasense"),
        user=os.getenv("POSTGRES_USER", "diasense"),
        password=os.getenv("POSTGRES_PASSWORD", "diasense"),
    )
    now = datetime.now(timezone.utc)
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pipeline_runs
                    (pipeline_name, airflow_dag_id, airflow_run_id, status, started_at, ended_at, duration_seconds)
                VALUES (%s, %s, %s, %s::pipeline_status, %s, %s, %s)
                """,
                (
                    "diasense_monitoring_pipeline",
                    context["dag"].dag_id,
                    context["run_id"],
                    "success",
                    context["dag_run"].start_date or now,
                    context["dag_run"].end_date or now,
                    0,
                ),
            )
    conn.close()


with DAG(
    dag_id="diasense_monitoring_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule="@daily",
    catchup=False,
    tags=["diasense", "monitoring"],
) as dag:
    recompute_current_feature_stats_from_recent_data = BashOperator(
        task_id="recompute_current_feature_stats_from_recent_data",
        bash_command="cd /opt/airflow && python ml/src/drift_baseline.py",
    )

    compare_against_baseline = BashOperator(
        task_id="compare_against_baseline",
        bash_command="echo 'Comparing current feature stats against baseline artifacts'",
    )

    persist_drift_report = PythonOperator(
        task_id="persist_drift_report",
        python_callable=persist_drift_report_to_db,
    )

    emit_alert_metrics = BashOperator(
        task_id="emit_alert_metrics",
        bash_command="echo 'Emitting drift alert metrics to /metrics via backend-api integration'",
        trigger_rule=TriggerRule.ALL_DONE,
    )

    (
        recompute_current_feature_stats_from_recent_data
        >> compare_against_baseline
        >> persist_drift_report
        >> emit_alert_metrics
    )
