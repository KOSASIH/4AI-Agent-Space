"""
🤖 Multi-Agent Orchestrator with Hierarchical Decision Making
Supports: Dynamic team assembly, task delegation, consensus
"""

import asyncio
import networkx as nx
from typing import Dict, List, Any, Optional
from enum import Enum
import json
from datetime import datetime

from src.agents.quantum_agent import QuantumAgent
from src.monitoring.agent_monitor import AgentMonitor

class CollaborationMode(Enum):
    HIERARCHICAL = "hierarchical"
    PEER_TO_PEER = "p2p"
    CONSENSUS = "consensus"

class MultiAgentOrchestrator:
    def __init__(self, agents: Dict[str, QuantumAgent]):
        self.agents = agents
        self.agent_graph = nx.DiGraph()
        self.monitor = AgentMonitor()
        self.active_tasks = {}
        self.mode = CollaborationMode.HIERARCHICAL
        
    async def assemble_team(self, task: str, complexity: str = "medium") -> List[str]:
        """AI-powered dynamic team assembly"""
        team_prompt = f"""
        Task: {task}
        Complexity: {complexity}
        Available agents: {list(self.agents.keys())}
        
        Select optimal team (1-5 agents) and their roles. JSON output:
        {{"team": [agent_names], "roles": {{agent: role}}, "coordinator": "lead_agent"}}
        """
        
        # Use smartest agent for team selection
        selector = self.agents["analyst"]
        response = await selector.model.ainvoke([{"role": "user", "content": team_prompt}])
        
        team_config = json.loads(response.content)
        return team_config["team"]
    
    async def execute_collaborative_task(self, task: str, max_iterations: int = 20) -> Dict:
        """Execute complex tasks with agent collaboration"""
        task_id = f"task_{datetime.now().timestamp()}"
        self.active_tasks[task_id] = {"status": "planning", "team": []}
        
        # 1. Assemble team
        team = await self.assemble_team(task)
        self.active_tasks[task_id]["team"] = team
        
        # 2. Build collaboration graph
        self._build_collaboration_graph(team)
        
        # 3. Hierarchical execution
        results = {}
        coordinator = "analyst"  # Default
        
        for agent_name in nx.topological_sort(self.agent_graph):
            agent = self.agents[agent_name]
            context = self._gather_context(task_id, agent_name)
            
            result = await agent.execute(task, context)
            results[agent_name] = result
            
            self.monitor.log_agent_performance(agent_name, result)
        
        # 4. Consensus & final synthesis
        final_result = await self._synthesize_results(results, task)
        
        self.active_tasks[task_id]["status"] = "completed"
        return {
            "task_id": task_id,
            "team": team,
            "individual_results": results,
            "final_result": final_result,
            "metrics": self.monitor.get_session_metrics(task_id)
        }
    
    def _build_collaboration_graph(self, team: List[str]):
        """Build dependency graph based on roles"""
        self.agent_graph.clear()
        self.agent_graph.add_nodes_from(team)
        
        # Simple hierarchical structure
        hierarchy = ["researcher", "analyst", "writer", "reviewer"]
        for i in range(len(team)-1):
            if team[i] in hierarchy and team[i+1] in hierarchy:
                self.agent_graph.add_edge(team[i], team[i+1])
    
    async def _synthesize_results(self, results: Dict, original_task: str) -> str:
        """Consensus-based final result synthesis"""
        synthesis_agent = self.agents["writer"]
        context = {
            "original_task": original_task,
            "agent_contributions": {k: v["result"].content for k, v in results.items()}
        }
        
        final_prompt = """
        Synthesize all contributions into coherent final answer.
        Resolve conflicts, fill gaps, ensure completeness.
        """
        
        result = await synthesis_agent.execute(final_prompt, context)
        return result["result"].content
    
    def _gather_context(self, task_id: str, agent_name: str) -> Dict:
        """Gather relevant context for agent"""
        task_data = self.active_tasks[task_id]
        prev_results = {
            agent: results["result"].content 
            for agent, results in self.monitor.get_previous_results(task_id).items()
            if self.agent_graph.has_edge(agent, agent_name)
        }
        return {"previous_work": prev_results, "task_progress": task_data}
