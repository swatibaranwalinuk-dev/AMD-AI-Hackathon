import sqlite3
from datetime import datetime

from services.audit_service import write_audit


class DeploymentAgent:

    def deploy_patch(self, asset):

        conn = sqlite3.connect(
            "patchpilot.db"
        )

        cursor = conn.cursor()

        cursor.execute(
        """
        UPDATE assets
        SET status='Patched'
        WHERE asset_name=?
        """,
        (asset,)
        )

        cursor.execute(
        """
        INSERT INTO deployments
        (
            asset_name,
            action,
            deployment_status,
            deployment_time
        )
        VALUES
        (?, ?, ?, ?)
        """,
        (
            asset,
            "Patch Deployment",
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
            "Patch Deployment",
            "SUCCESS",
            "DeploymentAgent"
        )

        return f"Patch deployed on {asset}"