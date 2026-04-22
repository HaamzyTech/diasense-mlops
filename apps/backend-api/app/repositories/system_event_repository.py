from sqlalchemy import text
from sqlalchemy.orm import Session


class SystemEventRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_event(self, service_name: str, severity: str, message: str, metadata: dict) -> None:
        stmt = text(
            """
            INSERT INTO system_events (service_name, severity, message, metadata)
            VALUES (:service_name, :severity, :message, :metadata::jsonb)
            """
        )
        self.db.execute(stmt, {
            "service_name": service_name,
            "severity": severity,
            "message": message,
            "metadata": str(metadata).replace("'", '"'),
        })
        self.db.commit()
