import sqlite3

conn = sqlite3.connect("patchpilot.db")

cursor = conn.cursor()

cursor.execute("DELETE FROM assets")

assets = [
    (
        "APP01",
        "Linux",
        "High",
        9.8,
        "Critical",
        "CVE-2025-0001",
        "Pending"
    ),
    (
        "APP02",
        "Linux",
        "Medium",
        7.4,
        "High",
        "CVE-2025-0002",
        "Pending"
    ),
    (
        "DB01",
        "Linux",
        "High",
        8.8,
        "Critical",
        "CVE-2025-0003",
        "Pending"
    ),
    (
        "WEB01",
        "Linux",
        "Low",
        5.1,
        "Medium",
        "CVE-2025-0004",
        "Pending"
    )
]

for asset in assets:

    cursor.execute(
        """
        INSERT INTO assets
        (
            asset_name,
            operating_system,
            business_criticality,
            cvss_score,
            severity,
            vulnerability,
            status
        )
        VALUES
        (?, ?, ?, ?, ?, ?, ?)
        """,
        asset
    )

conn.commit()

conn.close()

print("Assets Loaded Successfully")
