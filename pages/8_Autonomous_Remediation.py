import streamlit as st

from agents.discovery_agent import DiscoveryAgent
from agents.risk_agent import RiskAgent
from agents.planning_agent import PlanningAgent
from agents.deployment_agent import DeploymentAgent
from agents.validation_agent import ValidationAgent

st.title("🚀 Autonomous Remediation")

if st.button(
    "Start Autonomous Remediation"
):

    discovery = DiscoveryAgent()
    risk = RiskAgent()
    planning = PlanningAgent()
    deployment = DeploymentAgent()
    validation = ValidationAgent()

    assets = discovery.discover()

    progress = st.progress(0)

    status = st.empty()

    total = len(assets)

    for idx,row in assets.iterrows():

        asset = row["asset_name"]

        status.write(
            f"Processing {asset}"
        )

        risk.analyze(
            asset,
            row["cvss_score"],
            row["severity"],
            row["business_criticality"]
        )

        planning.create_plan(
            row["severity"],
            row["business_criticality"]
        )

        deployment.deploy_patch(
            asset
        )

        validation.validate(
            asset
        )

        progress.progress(
            (idx+1)/total
        )

    st.success(
        "Autonomous Remediation Completed"
    )
