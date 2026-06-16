from agents.risk_agent import RiskAgent

agent = RiskAgent()

result = agent.analyze(
    asset_name="APP01",
    cvss_score=9.8,
    severity="Critical",
    business_criticality="High"
)

print(result)
