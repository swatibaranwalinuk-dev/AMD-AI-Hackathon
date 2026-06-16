CREATE TABLE IF NOT EXISTS assets (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_name TEXT NOT NULL,

    operating_system TEXT NOT NULL,

    business_criticality TEXT NOT NULL,

    cvss_score REAL,

    severity TEXT,

    vulnerability TEXT,

    status TEXT,

    last_scan TEXT

);

CREATE TABLE IF NOT EXISTS deployments (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_name TEXT,

    action TEXT,

    deployment_status TEXT,

    deployment_time TEXT

);

CREATE TABLE IF NOT EXISTS validations (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_name TEXT,

    validation_status TEXT,

    validation_time TEXT

);

CREATE TABLE IF NOT EXISTS rollbacks (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    asset_name TEXT,

    rollback_reason TEXT,

    rollback_time TEXT

);
