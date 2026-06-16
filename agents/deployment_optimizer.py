"""
Deployment Optimizer Agent - Advanced Graph-Based Deployment Sequencing
Uses graph theory, topological sorting, and critical path analysis
to optimize deployment order and minimize risk and time.
"""

from typing import Dict, List, Set, Tuple, Optional
from collections import defaultdict, deque
import heapq


class DeploymentGraph:
    """Represents deployment as a directed acyclic graph (DAG)."""
    
    def __init__(self):
        self.graph = defaultdict(list)
        self.reverse_graph = defaultdict(list)
        self.asset_metadata = {}
    
    def add_asset(self, asset_name: str, metadata: Dict):
        """Add asset node to graph."""
        self.asset_metadata[asset_name] = metadata
    
    def add_dependency(self, from_asset: str, to_asset: str, weight: float = 1.0):
        """Add edge representing dependency."""
        self.graph[from_asset].append((to_asset, weight))
        self.reverse_graph[to_asset].append((from_asset, weight))


class DeploymentOptimizer:
    """
    Graph-based deployment optimizer using advanced algorithms:
    - Critical Path Method (CPM) for timeline optimization
    - Topological sorting for safe ordering
    - Minimum cut analysis for risk reduction
    - Parallel execution planning
    """
    
    def __init__(self):
        self.graph = DeploymentGraph()
    
    def optimize_deployment_sequence(
        self,
        assets: List[Dict],
        dependencies: Dict[str, List[str]],
        constraints: Dict = None
    ) -> Dict:
        """
        Generate optimal deployment sequence using graph algorithms.
        
        Args:
            assets: List of asset dicts with {name, cvss_score, severity, ...}
            dependencies: Dependency mapping {asset: [dependent_assets]}
            constraints: Optional deployment constraints
        
        Returns:
            Optimized deployment strategy with critical path and risk metrics
        """
        
        # Build graph
        for asset in assets:
            self.graph.add_asset(
                asset['name'],
                {
                    'cvss_score': asset.get('cvss_score', 5.0),
                    'success_rate': asset.get('success_rate', 0.9)
                }
            )
        
        for asset, deps in dependencies.items():
            for dep in deps:
                self.graph.add_dependency(asset, dep)
        
        # 1. Topological Sort
        topo_order = self._topological_sort()
        
        # 2. Critical Path Analysis
        critical_path = self._find_critical_path(assets)
        
        # 3. Risk Bottleneck Analysis
        bottlenecks = self._find_risk_bottlenecks()
        
        # 4. Parallel Execution Groups
        parallel_groups = self._identify_parallel_groups(topo_order)
        
        # 5. Minimum Cut for Risk Reduction
        min_cut = self._minimum_cut_analysis()
        
        return {
            "topological_order": topo_order,
            "critical_path": critical_path,
            "critical_path_length": len(critical_path),
            "bottlenecks": bottlenecks,
            "parallel_execution_groups": parallel_groups,
            "num_parallel_phases": len(parallel_groups),
            "risk_reduction_strategy": min_cut,
            "deployment_phases": self._generate_deployment_phases(
                parallel_groups,
                assets
            ),
            "optimization_metrics": {
                "time_efficiency": self._calculate_time_efficiency(
                    topo_order,
                    parallel_groups
                ),
                "risk_efficiency": self._calculate_risk_efficiency(
                    critical_path,
                    assets
                ),
                "parallelization_factor": len(parallel_groups) / len(topo_order)
            }
        }
    
    def _topological_sort(self) -> List[str]:
        """
        Topological sort using Kahn's algorithm.
        Returns assets in safe deployment order respecting dependencies.
        """
        
        in_degree = defaultdict(int)
        queue = deque()
        result = []
        
        # Calculate in-degrees
        all_assets = set(self.graph.asset_metadata.keys())
        for asset in all_assets:
            in_degree[asset] = len(self.graph.reverse_graph[asset])
        
        # Add nodes with no incoming edges
        for asset in all_assets:
            if in_degree[asset] == 0:
                queue.append(asset)
        
        # Process queue
        while queue:
            asset = queue.popleft()
            result.append(asset)
            
            # Remove edges to dependent nodes
            for dependent, _ in self.graph.graph[asset]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        if len(result) != len(all_assets):
            raise ValueError("Cyclic dependency detected!")
        
        return result
    
    def _find_critical_path(self, assets: List[Dict]) -> List[str]:
        """
        Find critical path using longest path algorithm.
        Critical path = path with highest risk or deployment time.
        """
        
        # Use dynamic programming to find longest path
        memo = {}
        
        def longest_path(node):
            if node in memo:
                return memo[node]
            
            max_path = [node]
            max_length = self._get_node_weight(node, assets)
            
            for next_node, edge_weight in self.graph.graph[node]:
                sub_path = longest_path(next_node)
                path_length = self._get_node_weight(node, assets) + edge_weight + sum(
                    self._get_node_weight(n, assets) for n in sub_path[1:]
                )
                
                if path_length > max_length:
                    max_length = path_length
                    max_path = [node] + sub_path
            
            memo[node] = max_path
            return max_path
        
        # Find longest path from all starting nodes
        all_paths = []
        for asset in self.graph.asset_metadata.keys():
            if len(self.graph.reverse_graph[asset]) == 0:  # Starting nodes
                path = longest_path(asset)
                all_paths.append(path)
        
        return max(all_paths, key=len) if all_paths else []
    
    def _get_node_weight(self, node: str, assets: List[Dict]) -> float:
        """Get weight of a node (based on CVSS/risk)."""
        for asset in assets:
            if asset['name'] == node:
                return asset.get('cvss_score', 5.0) / 10.0
        return 0.5
    
    def _find_risk_bottlenecks(self) -> List[Dict]:
        """Identify assets that are bottlenecks for many deployments."""
        
        bottlenecks = []
        
        for asset in self.graph.asset_metadata.keys():
            # Count how many assets depend on this one
            dependents = len(self.graph.graph[asset])
            
            if dependents > 1:
                bottlenecks.append({
                    "asset": asset,
                    "dependent_count": dependents,
                    "risk_level": "HIGH" if dependents > 3 else "MEDIUM"
                })
        
        return sorted(bottlenecks, key=lambda x: x['dependent_count'], reverse=True)
    
    def _identify_parallel_groups(self, topo_order: List[str]) -> List[List[str]]:
        """
        Identify assets that can be deployed in parallel (same group).
        Uses level-based grouping from topological order.
        """
        
        levels = {}
        
        for asset in topo_order:
            max_dep_level = -1
            
            for dep_asset, _ in self.graph.reverse_graph[asset]:
                if dep_asset in levels:
                    max_dep_level = max(max_dep_level, levels[dep_asset])
            
            levels[asset] = max_dep_level + 1
        
        # Group by level
        groups_by_level = defaultdict(list)
        for asset, level in levels.items():
            groups_by_level[level].append(asset)
        
        return [groups_by_level[i] for i in sorted(groups_by_level.keys())]
    
    def _minimum_cut_analysis(self) -> Dict:
        """
        Minimum cut analysis to identify critical chokepoints.
        Removing these assets would disconnect large portions of the deployment.
        """
        
        critical_assets = []
        
        for asset in self.graph.asset_metadata.keys():
            # Simple heuristic: count incoming and outgoing edges
            in_edges = len(self.graph.reverse_graph[asset])
            out_edges = len(self.graph.graph[asset])
            centrality = in_edges + out_edges
            
            if centrality > 2:
                critical_assets.append({
                    "asset": asset,
                    "centrality_score": centrality,
                    "recommendation": "Deploy first or with redundancy"
                })
        
        return {
            "critical_chokepoints": sorted(
                critical_assets,
                key=lambda x: x['centrality_score'],
                reverse=True
            )[:5],
            "strategy": "Prioritize critical assets in deployment sequence"
        }
    
    def _generate_deployment_phases(
        self,
        parallel_groups: List[List[str]],
        assets: List[Dict]
    ) -> List[Dict]:
        """Generate detailed deployment phases."""
        
        phases = []
        
        for phase_num, group in enumerate(parallel_groups, 1):
            phase_assets = [
                a for a in assets if a['name'] in group
            ]
            
            phases.append({
                "phase": phase_num,
                "parallel_assets": group,
                "asset_count": len(group),
                "total_cvss_score": sum(
                    a.get('cvss_score', 5.0) for a in phase_assets
                ),
                "risk_level": self._calculate_phase_risk(phase_assets)
            })
        
        return phases
    
    def _calculate_phase_risk(self, assets: List[Dict]) -> str:
        """Determine risk level for a deployment phase."""
        avg_cvss = sum(a.get('cvss_score', 5.0) for a in assets) / len(assets)
        
        if avg_cvss >= 8.0:
            return "CRITICAL"
        elif avg_cvss >= 6.0:
            return "HIGH"
        elif avg_cvss >= 4.0:
            return "MEDIUM"
        else:
            return "LOW"
    
    def _calculate_time_efficiency(
        self,
        topo_order: List[str],
        parallel_groups: List[List[str]]
    ) -> float:
        """
        Time efficiency = 1 - (critical_path_length / sequential_length)
        Higher is better (more parallelization).
        """
        sequential_length = len(topo_order)
        parallel_length = len(parallel_groups)
        
        if sequential_length == 0:
            return 0.0
        
        return 1.0 - (parallel_length / sequential_length)
    
    def _calculate_risk_efficiency(
        self,
        critical_path: List[str],
        assets: List[Dict]
    ) -> float:
        """
        Risk efficiency metric for critical path.
        Lower risk on critical path = higher efficiency.
        """
        if not critical_path:
            return 0.0
        
        path_risk = sum(
            next((a.get('cvss_score', 5.0) for a in assets if a['name'] == node), 0)
            for node in critical_path
        )
        
        max_possible_risk = sum(
            a.get('cvss_score', 5.0) for a in assets
        )
        
        return 1.0 - (path_risk / max_possible_risk) if max_possible_risk > 0 else 0.0
