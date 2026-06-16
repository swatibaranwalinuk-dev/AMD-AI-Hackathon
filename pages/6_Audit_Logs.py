import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "sqlite:///patchpilot.db"
)

st.title("Audit Logs")

deployments = pd.read_sql(
    "select * from deployments",
    engine
)

validations = pd.read_sql(
    "select * from validations",
    engine
)

st.subheader("Deployments")

st.dataframe(
    deployments,
    use_container_width=True
)

st.subheader("Validations")

st.dataframe(
    validations,
    use_container_width=True
)
