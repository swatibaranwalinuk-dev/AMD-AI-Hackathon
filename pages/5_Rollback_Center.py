import streamlit as st

from agents.rollback_agent import RollbackAgent

st.title("Rollback Center")

asset = st.selectbox(
    "Select Asset",
    [
        "APP01",
        "APP02",
        "DB01",
        "WEB01"
    ]
)

if st.button("Rollback"):

    rollback = RollbackAgent()

    result = rollback.rollback(
        asset
    )

    st.warning(result)
