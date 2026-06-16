class PlanningAgent:

    def create_plan(
        self,
        severity,
        business_criticality
    ):

        if severity == "Critical":

            return {
                "priority": "P1",
                "maintenance_window": "Immediate",
                "rollback_required": True
            }

        if severity == "High":

            return {
                "priority": "P2",
                "maintenance_window": "24 Hours",
                "rollback_required": True
            }

        return {
            "priority": "P3",
            "maintenance_window": "Next Scheduled Window",
            "rollback_required": False
        }
