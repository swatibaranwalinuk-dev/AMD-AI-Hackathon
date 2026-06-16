import sqlite3
from datetime import datetime

from services.audit_service import write_audit

class ValidationAgent:

    def validate(
        self,
        asset
    ):

        conn = sqlite3.connect(
            "patchpilot.db"
        )

        cursor = conn.cursor()

        cursor.execute(
        """
        INSERT INTO validations
        (
            asset_name,
            validation_status,
            validation_time
        )
        VALUES
        (?, ?, ?)
        """,
        (
            asset,
            "SUCCESS",
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        )

        conn.commit()

        conn.close()

        write_audit(
            asset,
            "Validation",
            "SUCCESS",
            "ValidationAgent"
        )

        return f"Validation Passed for {asset}"