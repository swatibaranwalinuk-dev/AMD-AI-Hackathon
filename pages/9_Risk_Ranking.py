import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///patchpilot.db"
)

st.title("Risk Ranking")

df = pd.read_sql(
    "SELECT * FROM assets",
    engine
)

weights = {
    "High":3,
    "Medium":2,
    "Low":1
}

df["risk_score"] = (
    df["cvss_score"]
    *
    df["business_criticality"].map(weights)
)

df = df.sort_values(
    "risk_score",
    ascending=False
)

st.dataframe(
    df,
    use_container_width=True
)

st.bar_chart(
    df.set_index(
        "asset_name"
    )["risk_score"]
)
