"""Swarm Intelligence Engine - Predict Anything
Based on MiroFish architecture - Universal Swarm Intelligence"""

import asyncio
import logging
import random
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
import math

logger = logging.getLogger(__name__)


class SwarmAgent:
    """
    Individual agent in the swarm
    """
    
    def __init__(self, agent_id: int, position: List[float], capability: float = 1.0):
        self.agent_id = agent_id
        self.position = position  # [x, y, ...]
        self.velocity = [0.0] * len(position)
        self.capability = capability  # 0-1 capability score
        self.best_position = position.copy()
        self.best_fitness = float('-inf')
        self.fitness_history = []
    
    def update(self, learning_rate: float = 0.1):
        """Update position based on velocity"""
        for i in range(len(self.position)):
            self.position[i] += self.velocity[i] * learning_rate
    
    def fitness(self, target: List[float]) -> float:
        """Calculate fitness - distance to target (higher is better)"""
        distance = sum((self.position[i] - target[i]) ** 2 for i in range(len(self.position)))
        return -distance  # Negative distance = higher fitness when closer


class SwarmIntelligence:
    """
    Swarm Intelligence Engine - Particle Swarm Optimization
    Used for prediction, optimization, and finding solutions
    """
    
    def __init__(self, num_agents: int = 50, dimensions: int = 2):
        self.num_agents = num_agents
        self.dimensions = dimensions
        self.agents = []
        self.global_best = None
        self.global_best_fitness = float('-inf')
        
        # PSO parameters
        self.w = 0.729  # Inertia weight
        self.c1 = 1.49  # Cognitive coefficient
        self.c2 = 1.49  # Social coefficient
        
        # Initialize agents
        self._init_agents()
    
    def _init_agents(self):
        """Initialize swarm agents"""
        for i in range(self.num_agents):
            position = [random.uniform(-10, 10) for _ in range(self.dimensions)]
            agent = SwarmAgent(i, position, capability=random.uniform(0.5, 1.0))
            self.agents.append(agent)
    
    async def optimize(self, objective_fn: Callable, target: List[float] = None, 
                       iterations: int = 100) -> Dict:
        """
        Optimize using particle swarm optimization
        
        Args:
            objective_fn: Function to maximize/minimize
            target: Target position (if predicting location)
            iterations: Number of iterations
            
        Returns:
            Best solution found
        """
        logger.info(f"🔮 Starting swarm optimization with {self.num_agents} agents")
        
        for iteration in range(iterations):
            # Evaluate each agent
            for agent in self.agents:
                if target:
                    fitness = agent.fitness(target)
                else:
                    fitness = objective_fn(agent.position)
                
                agent.fitness_history.append(fitness)
                
                # Update personal best
                if fitness > agent.best_fitness:
                    agent.best_fitness = fitness
                    agent.best_position = agent.position.copy()
                
                # Update global best
                if fitness > self.global_best_fitness:
                    self.global_best_fitness = fitness
                    self.global_best = agent.position.copy()
            
            # Update velocities and positions
            for agent in self.agents:
                r1, r2 = random.random(), random.random()
                
                for i in range(self.dimensions):
                    # PSO velocity update
                    cognitive = self.c1 * r1 * (agent.best_position[i] - agent.position[i])
                    social = self.c2 * r2 * (self.global_best[i] - agent.position[i] if self.global_best else 0)
                    
                    agent.velocity[i] = self.w * agent.velocity[i] + cognitive + social
                    
                    # Limit velocity
                    agent.velocity[i] = max(-1, min(1, agent.velocity[i]))
                
                agent.update()
            
            if iteration % 20 == 0:
                logger.info(f"  Iteration {iteration}: Best fitness = {self.global_best_fitness:.4f}")
        
        return {
            "best_position": self.global_best,
            "best_fitness": self.global_best_fitness,
            "convergence": self._calculate_convergence()
        }
    
    def _calculate_convergence(self) -> float:
        """Calculate how converged the swarm is (0-1, higher = more converged)"""
        if not self.agents:
            return 0.0
        
        # Calculate variance of positions
        variances = []
        for dim in range(self.dimensions):
            positions = [agent.position[dim] for agent in self.agents]
            mean = sum(positions) / len(positions)
            variance = sum((p - mean) ** 2 for p in positions) / len(positions)
            variances.append(variance)
        
        avg_variance = sum(variances) / len(variances)
        # Lower variance = higher convergence
        convergence = 1 / (1 + avg_variance)
        return convergence
    
    async def predict(self, known_points: List[List[float]], target_point: List[float],
                      prediction_type: str = "interpolate") -> float:
        """
        Predict a value using swarm intelligence
        
        Args:
            known_points: Known data points [[x1,y1], [x2,y2], ...]
            target_point: Point to predict
            prediction_type: "interpolate", "extrapolate", "classify"
        """
        if not known_points:
            return 0.0
        
        if prediction_type == "interpolate":
            # Find weighted average of nearby points
            distances = []
            for point in known_points:
                dist = sum((point[i] - target_point[i]) ** 2 for i in range(len(point))) ** 0.5
                distances.append((dist, point))
            
            distances.sort(key=lambda x: x[0])
            
            # Weighted average of closest points
            weight_sum = 0
            value_sum = 0
            for dist, point in distances[:5]:
                if dist == 0:
                    return point[-1]  # Exact match
                weight = 1 / (dist ** 2 + 0.001)
                weight_sum += weight
                value_sum += weight * point[-1]
            
            return value_sum / weight_sum if weight_sum > 0 else 0
        
        return 0.0


class ForecastingTool:
    """
    Forecasting using swarm intelligence
    """
    
    def __init__(self):
        self.swarm = SwarmIntelligence(num_agents=30, dimensions=1)
    
    async def forecast(self, data: List[float], steps_ahead: int = 5) -> List[float]:
        """
        Forecast future values based on historical data
        
        Args:
            data: Historical data points
            steps_ahead: Number of steps to forecast
            
        Returns:
            Forecasted values
        """
        if len(data) < 3:
            return data * steps_ahead
        
        # Simple linear trend + swarm optimization for pattern
        n = len(data)
        x_mean = sum(range(n)) / n
        y_mean = sum(data) / n
        
        # Calculate slope
        numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        slope = numerator / denominator if denominator != 0 else 0
        intercept = y_mean - slope * x_mean
        
        # Forecast
        forecasts = []
        for i in range(steps_ahead):
            forecast = slope * (n + i) + intercept
            forecasts.append(forecast)
        
        return forecasts
    
    async def detect_anomalies(self, data: List[float], threshold: float = 2.0) -> List[int]:
        """
        Detect anomalies in data using standard deviation
        
        Args:
            data: Data to analyze
            threshold: Standard deviations to consider anomaly
            
        Returns:
            Indices of anomalous data points
        """
        if len(data) < 3:
            return []
        
        mean = sum(data) / len(data)
        std = (sum((x - mean) ** 2 for x in data) / len(data)) ** 0.5
        
        anomalies = []
        for i, value in enumerate(data):
            z_score = abs(value - mean) / std if std > 0 else 0
            if z_score > threshold:
                anomalies.append(i)
        
        return anomalies


class OptimizationTool:
    """
    General optimization using swarm intelligence
    """
    
    def __init__(self):
        self.swarm = None
    
    async def find_optimal(self, objective_fn: Callable, bounds: List[tuple], 
                          iterations: int = 100) -> Dict:
        """
        Find optimal solution using swarm
        
        Args:
            objective_fn: Function to optimize
            bounds: [(min, max), ...] for each dimension
            iterations: Number of iterations
            
        Returns:
            Optimal solution and value
        """
        dimensions = len(bounds)
        swarm = SwarmIntelligence(num_agents=50, dimensions=dimensions)
        
        # Wrap objective with bounds
        def bounded_objective(position):
            # Apply bounds
            for i in range(dimensions):
                position[i] = max(bounds[i][0], min(bounds[i][1], position[i]))
            return objective_fn(position)
        
        result = await swarm.optimize(bounded_objective, iterations=iterations)
        
        return result


class PredictionEngine:
    """
    Unified prediction engine using swarm intelligence
    """
    
    def __init__(self):
        self.swarm_intelligence = SwarmIntelligence()
        self.forecasting = ForecastingTool()
        self.optimizer = OptimizationTool()
    
    async def predict(self, data: Any, prediction_type: str = "forecast", **kwargs) -> Any:
        """
        Unified predict method
        
        Args:
            data: Input data
            prediction_type: "forecast", "classify", "optimize", "recommend"
            **kwargs: Additional parameters
        """
        if prediction_type == "forecast":
            return await self.forecasting.forecast(data, kwargs.get("steps_ahead", 5))
        
        elif prediction_type == "anomaly":
            return await self.forecasting.detect_anomalies(data, kwargs.get("threshold", 2.0))
        
        elif prediction_type == "optimize":
            return await self.optimizer.find_optimal(
                data,  # objective function
                kwargs.get("bounds", [(-10, 10)]),
                kwargs.get("iterations", 100)
            )
        
        return None