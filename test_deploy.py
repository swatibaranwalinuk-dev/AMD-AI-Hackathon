from agents.deployment_agent import DeploymentAgent

agent = DeploymentAgent()

print(
    agent.deploy_patch(
        "APP01"
    )
)
