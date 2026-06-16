# 🛡️ PatchPilot AI - Autonomous Patch & Vulnerability Management Platform

**An AI-powered, autonomous platform for intelligent patch discovery, risk analysis, and secure deployment at scale.**

## 📋 Overview

PatchPilot AI is an enterprise-grade vulnerability management solution that leverages multi-agent AI orchestration to automate the entire patch lifecycle. Designed for the AMD AI Hackathon, it demonstrates how AI agents can work collaboratively to solve complex security operations challenges.

### Key Features

- 🤖 **Multi-Agent Architecture**: Six specialized AI agents working in concert
- 🔍 **Automated Discovery**: Identifies vulnerable assets across your infrastructure
- 📊 **Intelligent Risk Analysis**: CVSS-based severity assessment with business impact consideration
- 🚀 **Autonomous Deployment**: Automated patch application with safety guardrails
- ✅ **Validation & Verification**: Post-deployment health checks and compliance validation
- 📈 **Real-Time Dashboard**: Streamlit-based monitoring with key metrics and visualizations
- 🔄 **Rollback Capabilities**: Safe recovery mechanisms for failed deployments
- 📝 **Comprehensive Audit Trail**: Full logging and compliance reporting

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     PatchPilot AI Platform                      │
└─────────────────────────────────────────────────────────────────┘

                        ┌──────────────────┐
                        │  Streamlit UI    │
                        │   Dashboard      │
                        └────────┬─────────┘
                                 │
                    ┌────────────┴────────────┐
                    │                         │
        ┌───────────▼──────────┐   ┌────────▼──────────┐
        │   Asset Metrics      │   │  Deployment      │
        │   Severity Charts    │   │  Status Tracking │
        │   Audit Logs         │   │  Validation Info │
        └──────────────────────┘   └──────────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 │
                    ┌────────────▼─────────────┐
                    │   SQLite Database       │
                    │   (patchpilot.db)       │
                    │  - Assets Table         │
                    │  - Audit Logs           │
                    │  - Deployment History   │
                    └────────────┬─────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
        │          AGENT ORCHESTRATION LAYER             │
        │                        │                        │
        └────────────────────────┼────────────────────────┘
        │                                                  │
        
        ┌─────────────────┐  ┌──────────────────┐
        │ 1. Discovery    │  │ 2. Risk Analysis │
        │ Agent           │  │ Agent            │
        │                 │  │                  │
        │ • Scans assets  │  │ • CVSS scoring   │
        │ • Identifies    │  │ • Severity eval  │
        │   vulnerabilities   │ • Business      │
        │ • Inventories   │  │   impact assess  │
        │   managed nodes │  │ • Risk scoring   │
        └────────┬────────┘  └────────┬─────────┘
                 │                     │
                 └──────────┬──────────┘
                            │
        ┌─────────────────┐  ┌──────────────────┐
        │ 3. Planning     │  │ 4. Deployment    │
        │ Agent           │  │ Agent            │
        │                 │  │                  │
        │ • Prioritizes   │  │ • Executes patch │
        │   deployments   │  │ • Applies fixes  │
        │ • Creates       │  │ • Monitors       │
        │   strategy      │  │   process        │
        │ • Schedules     │  │ • Error handling │
        │   updates       │  │ • Rollback prep  │
        └────────┬────────┘  └────────┬─────────┘
                 │                     │
                 └──────────┬──────────┘
                            │
        ┌─────────────────┐  ┌──────────────────┐
        │ 5. Validation   │  │ 6. Reporting     │
        │ Agent           │  │ Agent            │
        │                 │  │                  │
        │ • Health checks │  │ • Logs events    │
        │ • Compliance    │  │ • Audit trail    │
        │   validation    │  │ • Generates      │
        │ • Verify patch  │  │   reports        │
        │   application   │  │ • Executive      │
        │ • Performance   │  │   summaries      │
        │   monitoring    │  │ • Compliance doc │
        └─────────────────┘  └──────────────────┘
```

### Agent Flow Diagram

```
START
  │
  ▼
┌─────────────────┐
│ Discovery Agent │  ◄─ Scans infrastructure
│   discover()    │     Returns: List of vulnerable assets
└────────┬────────┘
         │
         ▼
    ┌────────────────────────────────┐
    │ For Each Asset                 │
    └────────┬───────────────────────┘
             │
             ▼
       ┌──────────────────┐
       │ Risk Agent       │  ◄─ Analyzes: CVSS, severity,
       │  analyze()       │       business criticality
       └────────┬─────────┘       Returns: Risk score + details
                │
                ▼
         ┌─────────────────┐
         │ Planning Agent  │  ◄─ Creates deployment strategy
         │ create_plan()   │     based on risk level
         └────────┬────────┘     Returns: Deployment plan
                  │
                  ▼
         ┌──────────────────┐
         │ Deployment Agent │  ◄─ Executes patch application
         │ deploy_patch()   │     Returns: Deployment status
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Validation Agent │  ◄─ Verifies successful patching
         │  validate()      │     Returns: Validation results
         └────────┬─────────┘
                  │
                  ▼
         ┌──────────────────┐
         │ Reporting Agent  │  ◄─ Logs all activities
         │ log_deployment() │     Updates audit trail
         └────────┬─────────┘
                  │
       Next Asset │  Or END if all processed
                  │
                  ▼
              ┌────────┐
              │ END    │
              └────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- AMD ROCm (for GPU acceleration) - Optional but recommended
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/swatibaranwalinuk-dev/AMD-AI-Hackathon.git
   cd AMD-AI-Hackathon
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   python setup_database.py
   ```

### Running the Platform

#### Option 1: Run the AI Pipeline
```bash
python run_patchpilot.py
```
This executes the full autonomous patch management pipeline and logs results to the database.

#### Option 2: View the Dashboard
```bash
python -m streamlit run dashboard.py \
  --server.address 0.0.0.0 \
  --server.port 8501 \
  --server.enableCORS false \
  --server.enableXsrfProtection false
```

Access the dashboard at: `http://localhost:8501`

---

## 📁 Project Structure

```
AMD-AI-Hackathon/
├── README.md                          # Project documentation
├── requirements.txt                   # Python dependencies
├── patchpilot.db                      # SQLite database
├── CMD.txt                            # Command reference
│
├── agents/                            # Multi-agent orchestration
│   ├── discovery_agent.py             # Asset discovery & scanning
│   ├── risk_agent.py                  # Risk analysis & scoring
│   ├── planning_agent.py              # Deployment strategy planning
│   ├── deployment_agent.py            # Patch deployment execution
│   ├── validation_agent.py            # Post-deployment validation
│   └── reporting_agent.py             # Audit logging & reporting
│
├── dashboard.py                       # Streamlit UI dashboard
├── run_patchpilot.py                  # Main orchestration script
│
├── database/                          # Database layer
│   └── [database initialization files]
│
├── services/                          # Service integrations
│   └── [external service integrations]
│
├── models/                            # AI/ML models
│   └── [trained models & model configs]
│
├── data/                              # Data storage
│   └── [asset data, results]
│
├── managed_assets/                    # Asset tracking
│   └── [asset inventory]
│
├── pages/                             # Dashboard pages
│   ├── analysis.py                    # AI Analysis page
│   ├── deployment.py                  # Deployment tracking
│   ├── validation.py                  # Validation results
│   └── rollback.py                    # Rollback operations
│
├── health_check.sh                    # System health verification
├── create_audit_table.py              # Audit log setup
├── generate_executive_summary.py      # Report generation
├── load_assets.py                     # Asset data loader
│
└── tests/                             # Test suite
    ├── test_cve.py                    # CVE handling tests
    ├── test_deploy.py                 # Deployment tests
    ├── test_risk_agent.py             # Risk analysis tests
    └── test_rollback.py               # Rollback mechanism tests
```

---

## 🔄 Workflow Process

### Step 1: Asset Discovery
- Scans your infrastructure
- Identifies systems and their versions
- Detects known vulnerabilities (CVE database lookup)
- Returns comprehensive asset inventory

### Step 2: Risk Analysis
- Evaluates CVSS scores for each vulnerability
- Assesses business criticality
- Prioritizes patches by risk level
- Creates risk matrix for decision making

### Step 3: Deployment Planning
- Creates intelligent deployment strategy
- Determines safe deployment windows
- Plans rollback procedures
- Optimizes patch sequencing

### Step 4: Autonomous Deployment
- Executes patches automatically
- Monitors deployment progress
- Handles errors gracefully
- Maintains deployment logs

### Step 5: Validation & Verification
- Confirms successful patch application
- Runs health checks
- Verifies system stability
- Completes compliance checks

### Step 6: Audit & Reporting
- Logs all actions and decisions
- Generates compliance reports
- Creates executive summaries
- Maintains audit trail for governance

---

## 📊 Dashboard Features

The Streamlit dashboard provides real-time visibility:

### Main Dashboard
- **Asset Metrics**: Total count of managed assets
- **Critical Severity Count**: High-risk vulnerabilities requiring immediate action
- **High Severity Count**: Medium-high risk vulnerabilities
- **Pending Patches**: Assets awaiting deployment
- **Severity Distribution Chart**: Visual breakdown of vulnerability severity

### Additional Pages
- **AI Analysis**: Detailed risk analysis and recommendations
- **Deployment Tracking**: Real-time deployment status and progress
- **Validation Results**: Post-deployment health and compliance status
- **Rollback Operations**: Emergency rollback capabilities with logs

---

## 🧠 AI Technology Stack

- **Pydantic AI**: Multi-agent orchestration and coordination
- **Hugging Face Transformers**: NLP and ML capabilities for risk assessment
- **Accelerate**: Distributed training and inference acceleration
- **SQLAlchemy**: Database ORM for asset and audit management
- **Streamlit**: Interactive web dashboard framework
- **AMD ROCm**: GPU acceleration for AI model inference

---

## 💾 Database Schema

### Assets Table
```sql
CREATE TABLE assets (
    id INTEGER PRIMARY KEY,
    asset_name TEXT UNIQUE,
    asset_type TEXT,
    cvss_score FLOAT,
    severity TEXT,              -- Critical, High, Medium, Low
    business_criticality TEXT,  -- Critical, High, Medium, Low
    status TEXT,                -- Pending, Deployed, Validated, Failed
    deployment_date TIMESTAMP,
    validation_date TIMESTAMP,
    last_updated TIMESTAMP
);
```

### Audit Logs Table
```sql
CREATE TABLE audit_logs (
    id INTEGER PRIMARY KEY,
    asset_name TEXT,
    action TEXT,              -- Discovery, Analysis, Deployment, Validation
    action_details TEXT,
    status TEXT,              -- Success, Failed, Warning
    timestamp TIMESTAMP,
    agent_name TEXT
);
```

---

## 🔒 Security & Compliance

- ✅ **Audit Trail**: Complete logging of all actions
- ✅ **Rollback Capability**: Safe recovery from failed deployments
- ✅ **Validation Checks**: Post-deployment verification
- ✅ **Risk-Based Prioritization**: Smart scheduling of patches
- ✅ **Compliance Reporting**: Executive summaries and audit logs

---

## 📈 Performance & Scalability

- Processes multiple assets concurrently
- GPU-accelerated inference for rapid risk assessment
- Efficient database queries for asset discovery
- Streamlined agent communication
- Scalable to enterprise-scale deployments

---

## 🛠️ Troubleshooting

### Dashboard not accessible
```bash
# Check if Streamlit is running
ps -ef | grep streamlit

# Kill existing process if needed
pkill -f streamlit

# Verify required packages
python -m pip show streamlit
```

### Database issues
```bash
# Recreate database
python create_audit_table.py
python setup_database.py
```

### GPU acceleration issues
```bash
# Check ROCm installation
rocm-smi

# Verify GPU availability
python -c "import torch; print(torch.cuda.is_available())"
```

---

## 📝 Testing

Run the test suite to verify components:

```bash
# Test CVE handling
python test_cve.py

# Test deployment pipeline
python test_deploy.py

# Test risk analysis
python test_risk_agent.py

# Test rollback mechanism
python test_rollback.py
```

---

## 🎯 Use Cases

1. **Enterprise IT Operations**: Automate patch management across hundreds of servers
2. **Cloud Infrastructure**: Manage vulnerabilities in dynamic cloud environments
3. **Compliance & Governance**: Maintain audit trails and compliance reports
4. **Critical Infrastructure**: Secure sensitive systems with intelligent patching
5. **DevOps Pipelines**: Integrate automated patching into CI/CD workflows

---

## 🚀 Future Enhancements

- [ ] Integration with real CVE feeds (NVD, MITRE)
- [ ] Machine learning-based deployment risk prediction
- [ ] Multi-cloud support (AWS, Azure, GCP)
- [ ] Real-time threat intelligence feeds
- [ ] Advanced analytics and predictive maintenance
- [ ] Kubernetes/container patch orchestration
- [ ] API endpoint for third-party integrations
- [ ] Advanced scheduling with ML-based optimization

---

## 📄 License

This project is developed for the AMD AI Hackathon 2024.

---

## 👥 Author

**Swati Baranwal**  
AMD AI Hackathon Team

---

## 📞 Support

For issues, questions, or contributions, please open an issue in the GitHub repository.

---

## 🏆 Hackathon Submission

**Project**: PatchPilot AI - Autonomous Patch & Vulnerability Management Platform  
**Category**: Enterprise AI Solution  
**Tech Stack**: Python, AI Agents, Streamlit, SQLite, AMD ROCm  
**Innovation**: Multi-agent orchestration for autonomous security operations

---

*Last Updated: June 2024*
