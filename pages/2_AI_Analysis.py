import streamlit as st

from agents.risk_agent import RiskAgent

st.title("🤖 AI Risk Analysis")

asset = st.selectbox(
    "Asset",
    [
        "APP01",
        "APP02",
        "DB01",
        "WEB01"
    ]
)

cvss = st.number_input(
    "CVSS Score",
    value=9.8
)

severity = st.selectbox(
    "Severity",
    [
        "Critical",
        "High",
        "Medium",
        "Low"
    ]
)

business = st.selectbox(
    "Business Criticality",
    [
        "High",
        "Medium",
        "Low"
    ]
)

if st.button(
    "Analyze Risk"
):

    with st.spinner(
        "Running Qwen 3-8B on AMD MI300X..."
    ):

        agent = RiskAgent()

        result = agent.analyze(
            asset,
            cvss,
            severity,
            business
        )

        st.success(
            "Analysis Completed"
        )

        st.markdown(result)