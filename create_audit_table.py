import sqlite3

conn=sqlite3.connect("patchpilot.db")

cursor=conn.cursor()

cursor.execute(
"""
CREATE TABLE IF NOT EXISTS audit_logs(

id INTEGER PRIMARY KEY AUTOINCREMENT,

asset_name TEXT,

action TEXT,

status TEXT,

agent_name TEXT,

created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
"""
)

conn.commit()

conn.close()

print("Audit table created")
