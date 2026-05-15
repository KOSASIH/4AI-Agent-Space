"""
🏆 Agent Reputation & Bounty Marketplace
"""

from dataclasses import dataclass
from typing import Dict, List
import numpy as np

@dataclass
class AgentReputation:
    agent_id: str
    success_rate: float
    response_time: float
    client_satisfaction: float
    total_earnings: float
    bounty_wins: int
    
    @property
    def reputation_score(self) -> float:
        return (0.4 * self.success_rate + 
                0.3 * (1/self.response_time) + 
                0.2 * self.client_satisfaction + 
                0.1 * np.log(self.total_earnings + 1))

class BountyAuctioneer:
    def __init__(self):
        self.active_bounties: Dict[int, Dict] = {}
        self.agent_bids: Dict[str, List] = defaultdict(list)
    
    async def run_dutch_auction(self, bounty_id: int, initial_reward: float, duration: int):
        """Dutch auction for complex bounties"""
        reward = initial_reward
        decay_rate = initial_reward / duration
        
        while reward > 0 and duration > 0:
            # Notify capable agents
            candidates = self._find_capable_agents(bounty_id)
            winner = await self._select_winner(candidates, reward)
            
            if winner:
                self._award_bounty(bounty_id, winner, reward)
                break
            
            reward -= decay_rate
            duration -= 1
            await asyncio.sleep(60)  # 1min intervals
