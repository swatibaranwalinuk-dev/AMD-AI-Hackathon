import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///patchpilot.db"
)

st.set_page_config(
    page_title="PatchPilot AI",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ PatchPilot AI")
st.caption("Autonomous Patch & Vulnerability Management Platform")

df = pd.read_sql(
    "SELECT * FROM assets",
    engine
)

total_assets = len(df)

critical = len(
    df[df["severity"] == "Critical"]
)

high = len(
    df[df["severity"] == "High"]
)

pending = len(
    df[df["status"] == "Pending"]
)

col1,col2,col3,col4 = st.columns(4)

with col1:
    st.metric(
        "Assets",
        total_assets
    )

with col2:
    st.metric(
        "Critical",
        critical
    )

with col3:
    st.metric(
        "High",
        high
    )

with col4:
    st.metric(
        "Pending",
        pending
    )

st.divider()

st.subheader("Severity Distribution")

severity_counts = (
    df["severity"]
    .value_counts()
)

st.bar_chart(
    severity_counts
)

st.divider()

st.subheader("Current Assets")

st.dataframe(
    df,
    use_container_width=True
)

st.info(
    "Use the pages menu on the left to access AI Analysis, Deployment, Validation and Rollback."
)
