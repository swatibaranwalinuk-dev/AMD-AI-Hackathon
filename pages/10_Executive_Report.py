import streamlit as st

from models.qwen_loader import ask_llm

st.title(
    "Executive Cyber Report"
)

if st.button(
    "Generate Report"
):

    with st.spinner():

        report = ask_llm(
        """
Generate executive cyber security summary.

Include:

1. Critical Risks
2. Assets Impacted
3. Patch Status
4. Business Impact
5. Recommendations

Keep under 200 words.
"""
        )

    st.write(
        report
    )
