import sqlite3
from datetime import datetime

from services.audit_service import write_audit


class RollbackAgent:

    def rollback(
        self,
        asset,
        reason="Validation Failed"
    ):

        conn = sqlite3.connect(
            "patchpilot.db"
        )

        cursor = conn.cursor()

        cursor.execute(
        """
        UPDATE assets
        SET status='Rollback'
        WHERE asset_name=?
        """,
        (asset,)
        )

        cursor.execute(
        """
        INSERT INTO rollbacks
        (
            asset_name,
            rollback_reason,
            rollback_time
        )
        VALUES
        (?, ?, ?)
        """,
        (
            asset,
            reason,
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )
        )

        conn.commit()
        conn.close()

        write_audit(
            asset,
            "Rollback",
            "SUCCESS",
            "RollbackAgent"
        )

        return f"Rollback completed for {asset}"