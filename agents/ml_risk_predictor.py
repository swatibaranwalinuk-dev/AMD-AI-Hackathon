"""
ML-Based Risk Predictor Agent
Uses transformer models for intelligent vulnerability risk assessment
leveraging zero-shot classification for context-aware decisions.
"""

from transformers import pipeline
import numpy as np
from typing import Dict, List, Tuple


class MLRiskPredictor:
    """
    Advanced risk prediction using machine learning and NLP
    to analyze vulnerabilities with contextual understanding.
    """
    
    def __init__(self):
        """Initialize the ML-based risk prediction model."""
        # Use zero-shot classification for flexible risk categories
        self.classifier = pipeline(
            "zero-shot-classification",
            model="facebook/bart-large-mnli"
        )
        
        # Risk categories for classification
        self.risk_categories = [
            "Critical - Immediate deployment required",
            "High - Deploy within 24 hours",
            "Medium - Schedule deployment within week",
            "Low - Include in routine maintenance"
        ]
        
        # Historical patterns (would be loaded from database)
        self.deployment_history = {}
        
    def predict_deployment_risk(
        self,
        asset_name: str,
        cvss_score: float,
        severity: str,
        business_criticality: str,
        historical_failures: int = 0,
        total_deployments: int = 0
    ) -> Dict:
        """
        Predict deployment risk using ML model with multiple factors.
        
        Args:
            asset_name: Name of the asset
            cvss_score: CVSS vulnerability score (0-10)
            severity: Severity level (Critical, High, Medium, Low)
            business_criticality: Business criticality (Critical, High, Medium, Low)
            historical_failures: Number of past deployment failures
            total_deployments: Total deployment history count
        
        Returns:
            Dict with risk prediction, confidence, and recommendations
        """
        
        # Build contextual description for classification
        context = self._build_risk_context(
            asset_name,
            cvss_score,
            severity,
            business_criticality,
            historical_failures,
            total_deployments
        )
        
        # Use zero-shot classification
        classification_result = self.classifier(
            context,
            self.risk_categories,
            multi_class=False
        )
        
        # Parse results
        predicted_category = classification_result['labels'][0]
        confidence_score = classification_result['scores'][0]
        
        # Calculate composite risk score
        risk_score = self._calculate_risk_score(
            cvss_score,
            severity,
            historical_failures,
            total_deployments
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            predicted_category,
            risk_score,
            asset_name
        )
        
        return {
            "asset": asset_name,
            "predicted_risk_level": predicted_category,
            "confidence": float(confidence_score),
            "composite_risk_score": float(risk_score),
            "recommendations": recommendations,
            "deployment_readiness": confidence_score > 0.85,
            "success_probability": self._estimate_success_rate(
                historical_failures,
                total_deployments
            )
        }
    
    def _build_risk_context(
        self,
        asset_name: str,
        cvss_score: float,
        severity: str,
        business_criticality: str,
        failures: int,
        total: int
    ) -> str:
        """Build textual context for the ML model."""
        
        failure_rate = (failures / total * 100) if total > 0 else 0
        
        context = f"""
        Asset being patched: {asset_name}
        
        Vulnerability Metrics:
        - CVSS Score: {cvss_score}/10
        - Severity Level: {severity}
        - Business Criticality: {business_criticality}
        
        Historical Performance:
        - Past deployment attempts: {total}
        - Failed deployments: {failures}
        - Failure rate: {failure_rate:.1f}%
        
        System Risk Profile:
        - High CVSS score indicates critical vulnerability requiring urgent patching
        - Business criticality affects deployment window flexibility
        - Historical failure rate suggests deployment risk level
        
        Assessment Context:
        This vulnerability assessment considers both technical severity and 
        operational risk factors to determine optimal deployment strategy.
        """
        
        return context.strip()
    
    def _calculate_risk_score(
        self,
        cvss_score: float,
        severity: str,
        failures: int,
        total: int
    ) -> float:
        """Calculate composite risk score (0-1 scale)."""
        
        # CVSS component (40% weight)
        cvss_component = (cvss_score / 10.0) * 0.4
        
        # Severity mapping (30% weight)
        severity_map = {
            "Critical": 1.0,
            "High": 0.75,
            "Medium": 0.5,
            "Low": 0.25
        }
        severity_component = severity_map.get(severity, 0.5) * 0.3
        
        # Historical reliability (30% weight)
        failure_rate = (failures / total) if total > 0 else 0
        reliability_component = failure_rate * 0.3
        
        # Composite score
        risk_score = cvss_component + severity_component + reliability_component
        
        return min(1.0, max(0.0, risk_score))
    
    def _generate_recommendations(
        self,
        risk_category: str,
        risk_score: float,
        asset_name: str
    ) -> Dict:
        """Generate actionable recommendations based on risk assessment."""
        
        recommendations = {
            "deployment_window": "",
            "testing_level": "",
            "rollback_required": False,
            "approval_required": False,
            "actions": []
        }
        
        if "Immediate" in risk_category or risk_score > 0.8:
            recommendations.update({
                "deployment_window": "ASAP",
                "testing_level": "CRITICAL",
                "rollback_required": True,
                "approval_required": True,
                "actions": [
                    "Prepare rollback plan immediately",
                    "Alert operations team",
                    "Monitor deployment closely",
                    "Have backup systems ready"
                ]
            })
        
        elif "24 hours" in risk_category or risk_score > 0.5:
            recommendations.update({
                "deployment_window": "Next 24 hours",
                "testing_level": "HIGH",
                "rollback_required": True,
                "approval_required": False,
                "actions": [
                    "Schedule deployment window",
                    "Prepare rollback procedures",
                    "Run comprehensive tests",
                    "Document dependencies"
                ]
            })
        
        elif "week" in risk_category or risk_score > 0.25:
            recommendations.update({
                "deployment_window": "Within 7 days",
                "testing_level": "STANDARD",
                "rollback_required": False,
                "approval_required": False,
                "actions": [
                    "Include in planned maintenance",
                    "Coordinate with team",
                    "Standard testing procedure"
                ]
            })
        
        else:
            recommendations.update({
                "deployment_window": "Regular maintenance cycle",
                "testing_level": "BASIC",
                "rollback_required": False,
                "approval_required": False,
                "actions": [
                    "Include in routine updates",
                    "Standard deployment procedure"
                ]
            })
        
        return recommendations
    
    def _estimate_success_rate(self, failures: int, total: int) -> float:
        """Estimate probability of successful deployment."""
        
        if total == 0:
            return 0.85  # Default confidence for new assets
        
        success_rate = 1.0 - (failures / total)
        return float(success_rate)


class AdaptiveRiskLearner:
    """
    Learns from deployment outcomes to continuously improve risk predictions.
    """
    
    def __init__(self):
        """Initialize the adaptive learning system."""
        self.deployment_patterns = {}
        self.asset_profiles = {}
        
    def record_deployment_outcome(
        self,
        asset: str,
        prediction: Dict,
        actual_outcome: Dict
    ) -> None:
        """
        Record deployment outcome to improve future predictions.
        
        Args:
            asset: Asset name
            prediction: Original prediction from ML model
            actual_outcome: Actual deployment result
        """
        
        if asset not in self.deployment_patterns:
            self.deployment_patterns[asset] = []
        
        self.deployment_patterns[asset].append({
            "prediction": prediction,
            "outcome": actual_outcome,
            "accuracy": self._calculate_accuracy(prediction, actual_outcome)
        })
        
        # Update asset profile
        self._update_asset_profile(asset)
    
    def _calculate_accuracy(self, prediction: Dict, outcome: Dict) -> float:
        """Calculate prediction accuracy."""
        
        predicted_success = prediction.get("deployment_readiness", False)
        actual_success = outcome.get("success", False)
        
        return 1.0 if predicted_success == actual_success else 0.0
    
    def _update_asset_profile(self, asset: str) -> None:
        """Update asset's historical profile."""
        
        patterns = self.deployment_patterns.get(asset, [])
        
        if patterns:
            successes = sum(
                1 for p in patterns if p["outcome"].get("success", False)
            )
            self.asset_profiles[asset] = {
                "total_deployments": len(patterns),
                "successful_deployments": successes,
                "success_rate": successes / len(patterns),
                "avg_prediction_accuracy": np.mean(
                    [p["accuracy"] for p in patterns]
                )
            }
