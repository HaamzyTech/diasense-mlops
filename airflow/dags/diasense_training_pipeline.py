import os
from datetime import datetime, timezone

import psycopg2
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule


def record_pipeline_run(**context):
    status = "success" if context["dag_run"].get_state() == "success" else "failed"
    started_at = context["dag_run"].start_date or datetime.now(timezone.utc)
    ended_at = context["dag_run"].end_date or datetime.now(timezone.utc)
    duration_seconds = int((ended_at - started_at).total_seconds())

    conn = psycopg2.connect(
        host=os.getenv("POSTGRES_HOST", "postgres"),
        port=os.getenv("POSTGRES_PORT", "5432"),
        dbname=os.getenv("POSTGRES_DB", "diasense"),
        user=os.getenv("POSTGRES_USER", "diasense"),
        password=os.getenv("POSTGRES_PASSWORD", "diasense"),
    )
    with conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO pipeline_runs
                    (pipeline_name, airflow_dag_id, airflow_run_id, status, started_at, ended_at, duration_seconds)
                VALUES (%s, %s, %s, %s::pipeline_status, %s, %s, %s)
                """,
                (
                    "diasense_training_pipeline",
                    context["dag"].dag_id,
                    context["run_id"],
                    status,
                    started_at,
                    ended_at,
                    duration_seconds,
                ),
            )
    conn.close()


with DAG(
    dag_id="diasense_training_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["diasense", "training"],
) as dag:
    ingest = BashOperator(task_id="ingest", bash_command="cd /opt/airflow && dvc repro ingest")
    validate = BashOperator(task_id="validate", bash_command="cd /opt/airflow && dvc repro validate")
    preprocess = BashOperator(task_id="preprocess", bash_command="cd /opt/airflow && dvc repro preprocess")
    train = BashOperator(task_id="train", bash_command="cd /opt/airflow && dvc repro train")
    evaluate = BashOperator(task_id="evaluate", bash_command="cd /opt/airflow && dvc repro evaluate")
    register = BashOperator(task_id="register", bash_command="cd /opt/airflow && dvc repro register")

    record_pipeline_run_success_or_failure = PythonOperator(
        task_id="record_pipeline_run_success_or_failure",
        python_callable=record_pipeline_run,
        trigger_rule=TriggerRule.ALL_DONE,
    )

    ingest >> validate >> preprocess >> train >> evaluate >> register >> record_pipeline_run_success_or_failure
