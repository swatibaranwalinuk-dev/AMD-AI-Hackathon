from datetime import datetime
from sqlalchemy import text
from database.db import engine

class ReportingAgent:

    def log_deployment(
        self,
        asset_name,
        action,
        deployment_status
    ):

        query = text("""
        INSERT INTO deployments
        (
            asset_name,
            action,
            deployment_status,
            deployment_time
        )
        VALUES
        (
            :asset_name,
            :action,
            :deployment_status,
            :deployment_time
        )
        """)

        with engine.begin() as connection:

            connection.execute(
                query,
                {
                    "asset_name": asset_name,
                    "action": action,
                    "deployment_status": deployment_status,
                    "deployment_time": str(datetime.now())
                }
            )

    def log_validation(
        self,
        asset_name,
        validation_status
    ):

        query = text("""
        INSERT INTO validations
        (
            asset_name,
            validation_status,
            validation_time
        )
        VALUES
        (
            :asset_name,
            :validation_status,
            :validation_time
        )
        """)

        with engine.begin() as connection:

            connection.execute(
                query,
                {
                    "asset_name": asset_name,
                    "validation_status": validation_status,
                    "validation_time": str(datetime.now())
                }
            )
