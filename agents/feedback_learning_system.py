"""
Feedback Learning System - Self-Improving Agent Framework
Learns from deployment outcomes to continuously improve predictions and strategies.
Implements reinforcement learning principles for adaptive patch management.
"""

from typing import Dict, List, Tuple
import json
from datetime import datetime
from collections import defaultdict
import numpy as np


class DeploymentOutcome:
    """Represents a single deployment outcome for learning."""
    
    def __init__(
        self,
        asset_name: str,
        prediction: Dict,
        actual_result: Dict,
        timestamp: str = None
    ):
        self.asset_name = asset_name
        self.prediction = prediction
        self.actual_result = actual_result
        self.timestamp = timestamp or datetime.now().isoformat()
        self.prediction_accuracy = self._calculate_accuracy()
    
    def _calculate_accuracy(self) -> float:
        """Calculate how accurate the prediction was."""
        
        predicted_success = self.prediction.get('deployment_readiness', False)
        actual_success = self.actual_result.get('success', False)
        
        return 1.0 if predicted_success == actual_success else 0.0


class AdaptiveLearningSystem:
    """
    System that learns from deployment outcomes and improves future predictions.
    Implements Q-learning style value updates.
    """
    
    def __init__(self):
        """Initialize the learning system."""
        self.deployment_history = []
        self.asset_profiles = defaultdict(lambda: {
            'total_deployments': 0,
            'successful_deployments': 0,
            'failed_deployments': 0,
            'success_rate': 0.85,
            'prediction_accuracy': [],
            'avg_deployment_time': 0,
            'risk_assessments': []
        })
        self.pattern_database = defaultdict(list)
        self.learning_models = {}
        
    def record_deployment_outcome(
        self,
        asset_name: str,
        prediction: Dict,
        actual_result: Dict
    ) -> Dict:
        """
        Record a deployment outcome and learn from it.
        
        Args:
            asset_name: Name of deployed asset
            prediction: Original prediction from ML model
            actual_result: Actual deployment result
        
        Returns:
            Learning insights and updated model metrics
        """
        
        # Create outcome record
        outcome = DeploymentOutcome(asset_name, prediction, actual_result)
        self.deployment_history.append(outcome)
        
        # Update asset profile
        self._update_asset_profile(asset_name, outcome)
        
        # Extract and store patterns
        self._extract_patterns(asset_name, outcome)
        
        # Recalibrate models if threshold reached
        insights = self._generate_learning_insights(asset_name, outcome)
        
        return insights
    
    def _update_asset_profile(
        self,
        asset_name: str,
        outcome: DeploymentOutcome
    ) -> None:
        """Update asset's historical profile with new outcome."""
        
        profile = self.asset_profiles[asset_name]
        
        profile['total_deployments'] += 1
        
        if outcome.actual_result.get('success', False):
            profile['successful_deployments'] += 1
        else:
            profile['failed_deployments'] += 1
        
        # Update success rate (exponential moving average)
        alpha = 0.2  # Learning rate
        new_success = 1.0 if outcome.actual_result.get('success') else 0.0
        profile['success_rate'] = (
            alpha * new_success + (1 - alpha) * profile['success_rate']
        )
        
        # Track prediction accuracy
        profile['prediction_accuracy'].append(outcome.prediction_accuracy)
        
        # Update deployment time estimate
        actual_time = outcome.actual_result.get('deployment_time', 0)
        profile['avg_deployment_time'] = (
            alpha * actual_time + (1 - alpha) * profile['avg_deployment_time']
        )
        
        # Store risk assessment
        profile['risk_assessments'].append({
            'timestamp': outcome.timestamp,
            'predicted_risk': outcome.prediction.get('composite_risk_score', 0),
            'actual_outcome': outcome.actual_result.get('success', False)
        })
    
    def _extract_patterns(
        self,
        asset_name: str,
        outcome: DeploymentOutcome
    ) -> None:
        """Extract behavioral patterns from deployments."""
        
        patterns = {
            'asset_type': outcome.prediction.get('asset_type', 'unknown'),
            'severity': outcome.prediction.get('severity', 'unknown'),
            'time_of_day': datetime.fromisoformat(
                outcome.timestamp
            ).strftime('%H:%M'),
            'success': outcome.actual_result.get('success', False),
            'error_type': outcome.actual_result.get('error_type', None)
        }
        
        self.pattern_database[asset_name].append(patterns)
    
    def _generate_learning_insights(
        self,
        asset_name: str,
        outcome: DeploymentOutcome
    ) -> Dict:
        """Generate insights from the learning outcome."""
        
        profile = self.asset_profiles[asset_name]
        
        insights = {
            "asset": asset_name,
            "outcome_timestamp": outcome.timestamp,
            "prediction_accuracy": outcome.prediction_accuracy,
            "updated_metrics": {
                "success_rate": float(profile['success_rate']),
                "total_deployments": profile['total_deployments'],
                "successful_deployments": profile['successful_deployments'],
                "failure_rate": profile['failed_deployments'] / max(
                    profile['total_deployments'], 1
                )
            },
            "learning_indicators": self._compute_learning_indicators(
                asset_name,
                outcome
            ),
            "recommendations_for_next_deployment": self._generate_adaptive_recommendations(
                asset_name,
                outcome
            )
        }
        
        return insights
    
    def _compute_learning_indicators(
        self,
        asset_name: str,
        outcome: DeploymentOutcome
    ) -> Dict:
        """Compute metrics indicating what was learned."""
        
        profile = self.asset_profiles[asset_name]
        
        # Prediction drift: how much our estimates have changed
        prediction_drift = 0.0
        if len(profile['prediction_accuracy']) > 1:
            recent = profile['prediction_accuracy'][-5:]
            prediction_drift = np.std(recent)
        
        # Confidence level in current model
        min_samples = 10
        confidence = min(
            1.0,
            profile['total_deployments'] / min_samples
        )
        
        # Trend analysis
        recent_outcomes = self.deployment_history[-10:]
        recent_asset_outcomes = [
            o for o in recent_outcomes if o.asset_name == asset_name
        ]
        
        trend = "stable"
        if len(recent_asset_outcomes) > 2:
            success_trend = [
                1.0 if o.actual_result.get('success') else 0.0
                for o in recent_asset_outcomes
            ]
            if np.mean(success_trend[-3:]) > np.mean(success_trend[:-3]):
                trend = "improving"
            elif np.mean(success_trend[-3:]) < np.mean(success_trend[:-3]):
                trend = "degrading"
        
        return {
            "prediction_drift": float(prediction_drift),
            "model_confidence": float(confidence),
            "trend": trend,
            "recommendation_quality": "high" if confidence > 0.8 else "medium" if confidence > 0.5 else "low"
        }
    
    def _generate_adaptive_recommendations(
        self,
        asset_name: str,
        outcome: DeploymentOutcome
    ) -> List[str]:
        """Generate recommendations based on what was learned."""
        
        profile = self.asset_profiles[asset_name]
        recommendations = []
        
        success = outcome.actual_result.get('success', False)
        
        if success:
            recommendations.append("✓ Deployment successful - continue current strategy")
            
            if profile['success_rate'] > 0.95:
                recommendations.append("Asset is highly reliable - can increase deployment frequency")
            
        else:
            recommendations.append("✗ Deployment failed - adjust strategy")
            
            error_type = outcome.actual_result.get('error_type', 'unknown')
            
            if error_type == 'timeout':
                recommendations.append("  → Increase timeout window for this asset type")
            elif error_type == 'dependency_failure':
                recommendations.append("  → Review and re-order dependency chain")
            elif error_type == 'compatibility':
                recommendations.append("  → Perform staging test before next deployment")
            
            # Check for repeated patterns
            recent_failures = [
                o for o in self.deployment_history[-20:]
                if o.asset_name == asset_name and not o.actual_result.get('success')
            ]
            
            if len(recent_failures) > 2:
                recommendations.append(f"  → {len(recent_failures)} recent failures detected - investigate root cause")
        
        # Provide next action
        if profile['total_deployments'] < 5:
            recommendations.append("Need more data for reliable predictions - continue monitoring")
        else:
            recommendations.append(f"Model confidence: {profile['success_rate']*100:.1f}%")
        
        return recommendations
    
    def get_asset_intelligence(self, asset_name: str) -> Dict:
        """Get accumulated intelligence about an asset."""
        
        profile = self.asset_profiles[asset_name]
        patterns = self.pattern_database[asset_name]
        
        # Analyze common failure modes
        failures = [p for p in patterns if not p['success']]
        failure_modes = defaultdict(int)
        for failure in failures:
            error = failure.get('error_type', 'unknown')
            failure_modes[error] += 1
        
        # Best deployment time
        successes = [p for p in patterns if p['success']]
        success_times = [p['time_of_day'] for p in successes]
        best_time = max(set(success_times), key=success_times.count) if success_times else "any"
        
        return {
            "asset": asset_name,
            "deployment_history": {
                "total": profile['total_deployments'],
                "successful": profile['successful_deployments'],
                "failed": profile['failed_deployments'],
                "success_rate": float(profile['success_rate'])
            },
            "common_failure_modes": dict(failure_modes),
            "best_deployment_time": best_time,
            "average_deployment_time": float(profile['avg_deployment_time']),
            "patterns_learned": len(patterns),
            "recommendation": self._smart_recommendation(asset_name, profile)
        }
    
    def _smart_recommendation(self, asset_name: str, profile: Dict) -> str:
        """Generate smart deployment recommendation."""
        
        if profile['total_deployments'] < 3:
            return "Insufficient data - perform test deployment with monitoring"
        elif profile['success_rate'] > 0.95:
            return "Ready for production deployment - high confidence"
        elif profile['success_rate'] > 0.85:
            return "Deploy with standard precautions"
        elif profile['success_rate'] > 0.70:
            return "Deploy with enhanced monitoring and rollback plan"
        else:
            return "Investigate failure root cause before deploying - requires troubleshooting"
    
    def generate_model_report(self) -> Dict:
        """Generate comprehensive report on model learning progress."""
        
        total_deployments = len(self.deployment_history)
        
        if total_deployments == 0:
            return {"status": "No deployments recorded yet"}
        
        successful = sum(
            1 for o in self.deployment_history
            if o.actual_result.get('success', False)
        )
        
        # Overall metrics
        overall_success_rate = successful / total_deployments
        avg_prediction_accuracy = np.mean(
            [o.prediction_accuracy for o in self.deployment_history]
        )
        
        # Asset-level analysis
        best_asset = max(
            self.asset_profiles.items(),
            key=lambda x: x[1]['success_rate']
        )
        
        worst_asset = min(
            self.asset_profiles.items(),
            key=lambda x: x[1]['success_rate']
        )
        
        return {
            "learning_progress": {
                "total_deployments_observed": total_deployments,
                "overall_success_rate": float(overall_success_rate),
                "prediction_accuracy": float(avg_prediction_accuracy),
                "assets_tracked": len(self.asset_profiles)
            },
            "best_performing_asset": {
                "name": best_asset[0],
                "success_rate": float(best_asset[1]['success_rate']),
                "deployments": best_asset[1]['total_deployments']
            },
            "worst_performing_asset": {
                "name": worst_asset[0],
                "success_rate": float(worst_asset[1]['success_rate']),
                "deployments": worst_asset[1]['total_deployments']
            },
            "actionable_insights": [
                f"System has learned from {total_deployments} deployments",
                f"Average prediction accuracy: {avg_prediction_accuracy*100:.1f}%",
                f"Focus on improving {worst_asset[0]} (success rate: {worst_asset[1]['success_rate']*100:.1f}%)",
                f"Replicate success patterns from {best_asset[0]} to other assets"
            ]
        }
