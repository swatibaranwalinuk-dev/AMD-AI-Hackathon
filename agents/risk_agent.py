from models.qwen_loader import ask_llm

class RiskAgent:

    def analyze(
        self,
        asset_name,
        cvss_score,
        severity,
        business_criticality
    ):

        prompt = f"""
You are an enterprise vulnerability management expert.

Analyze the following vulnerability.

Asset: {asset_name}

CVSS Score: {cvss_score}

Severity: {severity}

Business Criticality: {business_criticality}

Provide:

1. Risk Level
2. Business Impact
3. Recommended Action
4. Maintenance Window
5. Rollback Requirement

Keep response concise.
"""

        result = ask_llm(
            prompt
        )

        return result
