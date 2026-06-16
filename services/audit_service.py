import sqlite3

def write_audit(
    asset,
    action,
    status,
    agent
):

    conn=sqlite3.connect(
        "patchpilot.db"
    )

    cursor=conn.cursor()

    cursor.execute(
    """
    INSERT INTO audit_logs
    (
    asset_name,
    action,
    status,
    agent_name
    )
    VALUES
    (?, ?, ?, ?)
    """,
    (
        asset,
        action,
        status,
        agent
    )
    )

    conn.commit()

    conn.close()
