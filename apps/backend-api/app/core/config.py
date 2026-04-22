from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "backend-api"
    app_version: str = "0.1.0"
    postgres_host: str = "postgres"
    postgres_port: int = 5432
    postgres_db: str = "diasense"
    postgres_user: str = "diasense"
    postgres_password: str = "diasense"
    model_server_url: str = "http://model-server:5001"
    mlflow_tracking_uri: str = "http://mlflow-tracking:5000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
