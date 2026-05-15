"""
👥 Human-in-the-Loop Approval & Collaboration System
"""

import asyncio
from typing import Dict, Callable, Optional
from enum import Enum

class HITLStatus(Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    MODIFIED = "modified"

class HumanLoopManager:
    def __init__(self):
        self.pending_reviews: Dict[str, Dict] = {}
        self.callbacks: Dict[str, Callable] = {}
    
    async def request_review(self, task_id: str, agent_plan: Dict, 
                           reviewer_id: str = "human") -> HITLStatus:
        """Request human review for high-risk actions"""
        self.pending_reviews[task_id] = {
            "plan": agent_plan,
            "reviewer": reviewer_id,
            "status": HITLStatus.PENDING,
            "timestamp": asyncio.get_event_loop().time()
        }
        
        # WebSocket notification to dashboard
        await self._notify_reviewers(task_id)
        
        # Wait for response (timeout 5min)
        try:
            result = await asyncio.wait_for(
                self._wait_for_review(task_id), timeout=300
            )
            return result
        except asyncio.TimeoutError:
            return HITLStatus.APPROVED  # Auto-approve on timeout
    
    async def submit_review(self, task_id: str, decision: str, 
                          feedback: Optional[str] = None):
        """Submit human review decision"""
        if task_id not in self.pending_reviews:
            return False
            
        review = self.pending_reviews[task_id]
        review["status"] = HITLStatus(decision)
        review["feedback"] = feedback
        review["reviewed_at"] = asyncio.get_event_loop().time()
        
        # Trigger callback
        if task_id in self.callbacks:
            await self.callbacks[task_id](review)
        
        return True
