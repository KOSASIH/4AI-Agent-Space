"""
📊 Enterprise Agent Monitoring & Analytics
"""

import time
import json
from collections import defaultdict
from typing import Dict, List
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class AgentMonitor:
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            "latency": [], "success_rate": [], "reflection_scores": [],
            "tool_usage": defaultdict(int), "iterations": []
        })
        self.session_logs = {}
    
    def log_agent_performance(self, agent_name: str, result: Dict):
        """Log comprehensive performance metrics"""
        start_time = time.time()
        metrics = self.metrics[agent_name]
        
        metrics["latency"].append(time.time() - start_time)
        metrics["success_rate"].append(1.0 if "success" in str(result) else 0.0)
        metrics["reflection_scores"].append(result.get("reflection_score", 0))
        metrics["iterations"].append(result.get("iterations", 1))
    
    def get_dashboard_data(self) -> Dict:
        """Generate dashboard-ready metrics"""
        summary = {}
        for agent, data in self.metrics.items():
            summary[agent] = {
                "avg_latency": sum(data["latency"][-100:]) / len(data["latency"][-100:]) if data["latency"] else 0,
                "success_rate": sum(data["success_rate"][-100:]) / len(data["success_rate"][-100:]),
                "avg_iterations": sum(data["iterations"][-100:]) / len(data["iterations"][-100:]),
                "top_tools": dict(sorted(data["tool_usage"].items(), key=lambda x: x[1], reverse=True)[:5])
            }
        return summary
    
    def generate_performance_chart(self) -> go.Figure:
        """Generate live performance dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=("Latency", "Success Rate", "Iterations", "Reflection Score")
        )
        
        for i, agent in enumerate(self.metrics.keys()):
            data = self.metrics[agent]
            fig.add_trace(
                go.Scatter(y=data["latency"][-50:], name=f"{agent}-latency", mode='lines'),
                row=1, col=1
            )
        
        return fig
