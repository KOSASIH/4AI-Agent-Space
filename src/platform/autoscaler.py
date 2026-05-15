"""
⚙️ Intelligent Auto-Scaling for Agent Workloads
Predictive scaling based on queue length, complexity, revenue
"""

import asyncio
import redis
from typing import Dict, List
import numpy as np
from sklearn.linear_model import LinearRegression

class PredictiveAutoscaler:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)
        self.model = LinearRegression()
        self.training_data = []
        self.min_replicas = 3
        self.max_replicas = 100
        
    async def scale_decision(self, metrics: Dict) -> int:
        """Predict optimal replica count"""
        queue_length = self.redis.llen("agent:task_queue")
        cpu_usage = metrics.get("cpu_usage", 0)
        pending_revenue = metrics.get("pending_revenue", 0)
        
        # ML prediction
        features = np.array([[queue_length, cpu_usage, pending_revenue]])
        predicted_replicas = int(self.model.predict(features)[0])
        
        # Heuristic bounds
        return max(self.min_replicas, 
                  min(self.max_replicas, predicted_replicas))
    
    async def monitor_and_scale(self):
        """Continuous scaling loop"""
        while True:
            metrics = await self._collect_metrics()
            target_replicas = await self.scale_decision(metrics)
            
            current_replicas = self.redis.get("current_replicas") or 3
            if abs(target_replicas - int(current_replicas)) > 1:
                await self._adjust_replicas(target_replicas)
            
            await asyncio.sleep(30)  # Check every 30s
    
    async def _collect_metrics(self) -> Dict:
        """Collect platform metrics"""
        return {
            "queue_length": self.redis.llen("agent:task_queue"),
            "cpu_usage": float(self.redis.get("system:cpu") or 0),
            "memory_usage": float(self.redis.get("system:memory") or 0),
            "pending_revenue": float(self.redis.get("billing:pending") or 0)
        }
