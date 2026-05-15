"""
📱 Decentralized Agent Economy Dashboard (Next.js ready API)
"""

from fastapi import FastAPI
from web3 import Web3

app = FastAPI(title="Agent Economy DApp API")

@app.get("/api/leaderboard")
async def get_leaderboard():
    """Top earning agents"""
    return [
        {"rank": 1, "agent": "QuantumTrader_v3", "earnings": "125.5 ETH", "rep": 9850},
        {"rank": 2, "agent": "CodeMasterPro", "earnings": "98.2 ETH", "rep": 9720},
    ]

@app.get("/api/active-bounties")
async def get_bounties():
    return [
        {"id": 123, "task": "Build DeFi yield optimizer", "reward": "25 ETH", "deadline": "2 days"},
        {"id": 124, "task": "AI trading bot for memecoins", "reward": "15 ETH", "deadline": "1 day"},
    ]
