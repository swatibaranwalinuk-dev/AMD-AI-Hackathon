from pydantic import BaseModel

class Vulnerability(BaseModel):

    asset_name: str

    operating_system: str

    business_criticality: str

    cvss_score: float

    severity: str

    vulnerability: str

    status: str


class PatchPlan(BaseModel):

    priority: str

    maintenance_window: str

    rollback_required: bool


class DeploymentResult(BaseModel):

    asset_name: str

    deployment_status: str


class ValidationResult(BaseModel):

    asset_name: str

    validation_status: str
