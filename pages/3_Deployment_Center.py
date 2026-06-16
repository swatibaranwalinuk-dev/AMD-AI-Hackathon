import streamlit as st

from agents.deployment_agent import DeploymentAgent

st.title("Patch Deployment Center")

asset = st.selectbox(
    "Select Asset",
    [
        "APP01",
        "APP02",
        "DB01",
        "WEB01"
    ]
)

if st.button("Deploy Patch"):

    deployment = DeploymentAgent()

    result = deployment.deploy_patch(
        asset
    )

    st.success(result)
