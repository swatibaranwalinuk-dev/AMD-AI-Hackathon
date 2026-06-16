from agents.discovery_agent import DiscoveryAgent
from agents.risk_agent import RiskAgent
from agents.planning_agent import PlanningAgent
from agents.deployment_agent import DeploymentAgent
from agents.validation_agent import ValidationAgent
from agents.reporting_agent import ReportingAgent

discovery = DiscoveryAgent()
risk = RiskAgent()
planning = PlanningAgent()
deployment = DeploymentAgent()
validation = ValidationAgent()
reporting = ReportingAgent()

assets = discovery.discover()

for _, row in assets.iterrows():

    print("\n")
    print("=" * 60)

    asset_name = row["asset_name"]

    print("ASSET:", asset_name)

    analysis = risk.analyze(
        asset_name,
        row["cvss_score"],
        row["severity"],
        row["business_criticality"]
    )

    print("\nRISK ANALYSIS")
    print(analysis)

    plan = planning.create_plan(
        row["severity"],
        row["business_criticality"]
    )

    print("\nPLAN")
    print(plan)

    deployment_result = deployment.deploy_patch(
        asset_name
    )

    print("\nDEPLOYMENT")
    print(deployment_result)

    reporting.log_deployment(
        asset_name,
        "Patch OpenSSL",
        deployment_result["status"]
    )

    validation_result = validation.validate(
        asset_name
    )

    print("\nVALIDATION")
    print(validation_result)

    reporting.log_validation(
        asset_name,
        validation_result["validation"]
    )

print("\n")
print("PatchPilot Run Completed")
