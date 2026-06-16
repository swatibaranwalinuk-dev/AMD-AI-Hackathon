import streamlit as st

from models.qwen_loader import ask_llm

st.title("Executive Summary")

if st.button("Generate Executive Report"):

    prompt = """
Generate executive cyber security summary.

Include:

1. Risks
2. Assets impacted
3. Remediation progress
4. Recommendations

Limit to 200 words.
"""

    with st.spinner():

        result = ask_llm(
            prompt
        )

    st.write(result)
