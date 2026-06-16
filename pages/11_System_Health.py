import streamlit as st
import pandas as pd
import sqlite3

st.title("System Health")

conn=sqlite3.connect(
    "patchpilot.db"
)

assets=pd.read_sql(
    "select * from assets",
    conn
)

audit=pd.read_sql(
    "select * from audit_logs",
    conn
)

conn.close()

st.subheader(
    "Assets"
)

st.dataframe(
    assets,
    use_container_width=True
)

st.subheader(
    "Audit Trail"
)

st.dataframe(
    audit,
    use_container_width=True
)
