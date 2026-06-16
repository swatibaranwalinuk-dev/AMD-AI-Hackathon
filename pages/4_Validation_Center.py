import streamlit as st

from agents.validation_agent import ValidationAgent

st.title("Validation Center")

asset = st.selectbox(
    "Select Asset",
    [
        "APP01",
        "APP02",
        "DB01",
        "WEB01"
    ]
)

if st.button("Validate"):

    validator = ValidationAgent()

    result = validator.validate(
        asset
    )

    st.success(result)
