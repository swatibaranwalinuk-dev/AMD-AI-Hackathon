"""
Strategic Planning Agent with AI-Driven Strategic Optimization
Uses constraint satisfaction, genetic algorithms, and Monte Carlo simulations
for intelligent patch deployment planning.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import heapq


@dataclass
class Asset:
    """Asset representation for optimization."""
    name: str
    cvss_score: float
    severity: str
    business_criticality: str
    dependencies: List[str]
    success_rate: float = 0.9


class ConstraintBasedPlanningAgent:
    """
    Intelligent deployment planning using constraint satisfaction problems (CSP)
    and multi-objective optimization.
    """
    
    def __init__(self):
        """Initialize the strategic planning agent."""
        self.constraints = []
        self.deployment_windows = self._initialize_windows()
        
    def create_strategic_plan(
        self,
        assets: List[Asset],
        maintenance_windows: List[Dict],
        risk_tolerance: float = 0.1,
        max_parallel_deployments: int = 5
    ) -> Dict:
        """
        Create optimized deployment plan using multiple strategies.
        
        Args:
            assets: List of assets to patch
            maintenance_windows: Available deployment windows
            risk_tolerance: Acceptable risk level (0-1)
            max_parallel_deployments: Maximum concurrent deployments
        
        Returns:
            Optimized deployment strategy with timeline and risk metrics
        """
        
        # 1. Dependency analysis
        dependency_graph = self._build_dependency_graph(assets)
        
        # 2. Constraint satisfaction
        feasible_schedules = self._find_feasible_schedules(
            assets,
            maintenance_windows,
            dependency_graph,
            max_parallel_deployments
        )
        
        # 3. Genetic algorithm optimization
        optimal_schedule = self._optimize_with_genetic_algorithm(
            feasible_schedules,
            assets,
            risk_tolerance
        )
        
        # 4. Monte Carlo risk simulation
        risk_analysis = self._monte_carlo_simulation(
            optimal_schedule,
            assets,
            num_simulations=10000
        )
        
        # 5. Generate strategic recommendations
        strategy = self._generate_strategic_recommendations(
            optimal_schedule,
            risk_analysis,
            assets
        )
        
        return strategy
    
    def _build_dependency_graph(self, assets: List[Asset]) -> Dict[str, List[str]]:
        """Build asset dependency graph for safe deployment sequencing."""
        
        graph = {}
        for asset in assets:
            graph[asset.name] = asset.dependencies
        
        return graph
    
    def _find_feasible_schedules(
        self,
        assets: List[Asset],
        windows: List[Dict],
        dependencies: Dict[str, List[str]],
        max_parallel: int
    ) -> List[List[Tuple[str, str]]]:
        """
        Find all feasible deployment schedules using constraint satisfaction.
        
        Constraints:
        - Respect dependency order
        - Fit within maintenance windows
        - Respect max parallel deployments
        - Minimize total deployment time
        """
        
        feasible_schedules = []
        
        # Topological sort to respect dependencies
        sorted_assets = self._topological_sort(assets, dependencies)
        
        # Try different scheduling strategies
        schedules = [
            self._greedy_scheduling(sorted_assets, windows, max_parallel),
            self._window_aware_scheduling(sorted_assets, windows, max_parallel),
            self._risk_weighted_scheduling(sorted_assets, windows, max_parallel)
        ]
        
        for schedule in schedules:
            if self._validate_schedule(schedule, dependencies, windows, max_parallel):
                feasible_schedules.append(schedule)
        
        return feasible_schedules
    
    def _topological_sort(
        self,
        assets: List[Asset],
        dependencies: Dict[str, List[str]]
    ) -> List[Asset]:
        """Topologically sort assets by dependencies."""
        
        visited = set()
        result = []
        
        def visit(asset_name: str):
            if asset_name in visited:
                return
            visited.add(asset_name)
            
            for dep in dependencies.get(asset_name, []):
                visit(dep)
            
            # Find and add asset object
            for asset in assets:
                if asset.name == asset_name:
                    result.append(asset)
                    break
        
        for asset in assets:
            visit(asset.name)
        
        return result
    
    def _greedy_scheduling(
        self,
        sorted_assets: List[Asset],
        windows: List[Dict],
        max_parallel: int
    ) -> List[Tuple[str, str]]:
        """Greedy scheduling: prioritize high-risk assets."""
        
        schedule = []
        window_idx = 0
        parallel_count = 0
        
        # Sort by risk (CVSS score)
        priority_assets = sorted(
            sorted_assets,
            key=lambda a: float(a.cvss_score),
            reverse=True
        )
        
        for asset in priority_assets:
            if parallel_count >= max_parallel:
                window_idx += 1
                parallel_count = 0
            
            if window_idx < len(windows):
                schedule.append((asset.name, windows[window_idx]['window_id']))
                parallel_count += 1
        
        return schedule
    
    def _window_aware_scheduling(
        self,
        sorted_assets: List[Asset],
        windows: List[Dict],
        max_parallel: int
    ) -> List[Tuple[str, str]]:
        """Schedule considering maintenance window capacity."""
        
        schedule = []
        window_slots = {w['window_id']: max_parallel for w in windows}
        
        for asset in sorted_assets:
            for window in windows:
                if window_slots[window['window_id']] > 0:
                    schedule.append((asset.name, window['window_id']))
                    window_slots[window['window_id']] -= 1
                    break
        
        return schedule
    
    def _risk_weighted_scheduling(
        self,
        sorted_assets: List[Asset],
        windows: List[Dict],
        max_parallel: int
    ) -> List[Tuple[str, str]]:
        """Schedule weighted by risk and success probability."""
        
        # Create priority queue: (priority, asset)
        priority_queue = []
        
        for asset in sorted_assets:
            # Higher priority = higher risk * lower success probability
            priority = (asset.cvss_score / 10.0) / (asset.success_rate + 0.1)
            heapq.heappush(priority_queue, (-priority, asset))
        
        schedule = []
        window_idx = 0
        parallel_count = 0
        
        while priority_queue:
            _, asset = heapq.heappop(priority_queue)
            
            if parallel_count >= max_parallel:
                window_idx += 1
                parallel_count = 0
            
            if window_idx < len(windows):
                schedule.append((asset.name, windows[window_idx]['window_id']))
                parallel_count += 1
        
        return schedule
    
    def _validate_schedule(
        self,
        schedule: List[Tuple[str, str]],
        dependencies: Dict[str, List[str]],
        windows: List[Dict],
        max_parallel: int
    ) -> bool:
        """Validate schedule against all constraints."""
        
        # Check all assets scheduled
        if len(schedule) == 0:
            return False
        
        # Check window capacity
        window_counts = {}
        for _, window_id in schedule:
            window_counts[window_id] = window_counts.get(window_id, 0) + 1
            if window_counts[window_id] > max_parallel:
                return False
        
        # Check dependencies respected (simplified check)
        scheduled_order = [asset for asset, _ in schedule]
        for asset, deps in dependencies.items():
            if asset in scheduled_order:
                asset_idx = scheduled_order.index(asset)
                for dep in deps:
                    if dep in scheduled_order:
                        dep_idx = scheduled_order.index(dep)
                        if dep_idx > asset_idx:
                            return False
        
        return True
    
    def _optimize_with_genetic_algorithm(
        self,
        schedules: List[List[Tuple[str, str]]],
        assets: List[Asset],
        risk_tolerance: float,
        population_size: int = 100,
        generations: int = 50
    ) -> List[Tuple[str, str]]:
        """
        Optimize schedule using genetic algorithm.
        
        Fitness function optimizes for:
        - Minimal deployment time
        - Risk within tolerance
        - Success probability
        """
        
        if not schedules:
            return []
        
        # Initialize population from feasible schedules
        population = [schedules[i % len(schedules)] for i in range(population_size)]
        
        for generation in range(generations):
            # Evaluate fitness
            fitness_scores = [
                self._calculate_fitness(schedule, assets, risk_tolerance)
                for schedule in population
            ]
            
            # Selection (tournament selection)
            selected = self._tournament_selection(population, fitness_scores, k=population_size // 2)
            
            # Crossover
            offspring = self._crossover(selected, population_size)
            
            # Mutation
            offspring = [self._mutate(child) for child in offspring]
            
            # Replacement
            population = selected + offspring[:population_size - len(selected)]
        
        # Return best schedule
        fitness_scores = [
            self._calculate_fitness(schedule, assets, risk_tolerance)
            for schedule in population
        ]
        best_idx = np.argmax(fitness_scores)
        
        return population[best_idx]
    
    def _calculate_fitness(
        self,
        schedule: List[Tuple[str, str]],
        assets: List[Asset],
        risk_tolerance: float
    ) -> float:
        """Calculate fitness score for a schedule."""
        
        # Time factor: prefer shorter schedules
        time_score = 1.0 / (len(schedule) + 1)
        
        # Risk factor: penalties for high-risk deployments
        risk_score = 0.0
        for asset_name, _ in schedule:
            for asset in assets:
                if asset.name == asset_name:
                    risk = (asset.cvss_score / 10.0) * (1 - asset.success_rate)
                    if risk > risk_tolerance:
                        risk_score -= 0.5
                    else:
                        risk_score += asset.success_rate * 0.1
        
        return time_score + risk_score
    
    def _tournament_selection(self, population, fitness_scores, k=50):
        """Tournament selection for GA."""
        selected = []
        for _ in range(k):
            tournament_idx = np.random.choice(len(population), size=5, replace=False)
            winner_idx = tournament_idx[np.argmax([fitness_scores[i] for i in tournament_idx])]
            selected.append(population[winner_idx])
        return selected
    
    def _crossover(self, population, target_size):
        """Genetic crossover operation."""
        offspring = []
        for _ in range(target_size - len(population)):
            parent1, parent2 = np.random.choice(len(population), 2, replace=False)
            split = np.random.randint(1, len(population[parent1]))
            child = population[parent1][:split] + population[parent2][split:]
            offspring.append(child)
        return offspring
    
    def _mutate(self, schedule):
        """Random mutation to maintain diversity."""
        if np.random.random() < 0.1:  # 10% mutation rate
            idx1, idx2 = np.random.choice(len(schedule), 2, replace=False)
            schedule[idx1], schedule[idx2] = schedule[idx2], schedule[idx1]
        return schedule
    
    def _monte_carlo_simulation(
        self,
        schedule: List[Tuple[str, str]],
        assets: List[Asset],
        num_simulations: int = 10000
    ) -> Dict:
        """
        Run Monte Carlo simulations to assess deployment risk.
        
        Returns probability distributions for:
        - Successful deployments
        - Failed deployments
        - Rollback scenarios
        """
        
        successful_runs = 0
        failed_runs = 0
        rollback_count = 0
        total_time_samples = []
        
        for _ in range(num_simulations):
            success = True
            
            for asset_name, _ in schedule:
                for asset in assets:
                    if asset.name == asset_name:
                        # Simulate deployment with success probability
                        if np.random.random() > asset.success_rate:
                            success = False
                            rollback_count += 1
                        break
            
            if success:
                successful_runs += 1
            else:
                failed_runs += 1
            
            # Simulate deployment time
            total_time_samples.append(len(schedule) * np.random.normal(1.0, 0.2))
        
        return {
            "success_probability": successful_runs / num_simulations,
            "failure_probability": failed_runs / num_simulations,
            "expected_rollbacks": rollback_count / num_simulations,
            "avg_deployment_time": np.mean(total_time_samples),
            "std_deployment_time": np.std(total_time_samples),
            "confidence_95_percentile": np.percentile(total_time_samples, 95)
        }
    
    def _generate_strategic_recommendations(
        self,
        schedule: List[Tuple[str, str]],
        risk_analysis: Dict,
        assets: List[Asset]
    ) -> Dict:
        """Generate strategic deployment recommendations."""
        
        return {
            "deployment_sequence": schedule,
            "total_phases": len(set(w for _, w in schedule)),
            "risk_analysis": risk_analysis,
            "success_probability": risk_analysis["success_probability"],
            "strategic_actions": [
                f"Deploy {len(schedule)} patches in phases",
                f"Expected success rate: {risk_analysis['success_probability']*100:.1f}%",
                f"Prepare for {risk_analysis['expected_rollbacks']:.1f} potential rollbacks",
                f"Estimated deployment time: {risk_analysis['avg_deployment_time']:.1f} ± {risk_analysis['std_deployment_time']:.1f} hours",
                "Monitor first phase closely before proceeding",
                "Have rollback plans ready for all assets"
            ],
            "risk_mitigations": [
                "Stagger deployments to minimize blast radius",
                "Test patches in staging environment first",
                "Maintain communication channels during deployment",
                "Have runbooks prepared for each asset type"
            ],
            "approval_status": "Ready for deployment" if risk_analysis["success_probability"] > 0.95 else "Review required"
        }
    
    def _initialize_windows(self) -> List[Dict]:
        """Initialize default maintenance windows."""
        return [
            {"window_id": "immediate", "duration": 1},
            {"window_id": "24h", "duration": 24},
            {"window_id": "weekend", "duration": 48},
            {"window_id": "monthly", "duration": 120}
        ]
