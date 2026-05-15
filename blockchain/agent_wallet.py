"""
🪙 Decentralized Agent Wallet & Economy Integration
"""

import asyncio
from web3 import Web3
from eth_account import Account
from typing import Dict, Optional
import json

class AgentWallet:
    def __init__(self, rpc_url: str, private_key: Optional[str] = None):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.account = Account.from_key(private_key) if private_key else None
        self.marketplace_contract = self._load_marketplace_contract()
    
    def _load_marketplace_contract(self):
        with open('blockchain/contracts/AgentMarketplace.json') as f:
            abi = json.load(f)['abi']
        
        contract_address = "0x..."  # Deployed contract
        return self.w3.eth.contract(address=contract_address, abi=abi)
    
    async def register_agent(self, capabilities: str, price_per_task: int):
        """Register agent in marketplace"""
        if not self.account:
            raise ValueError("No private key set")
        
        txn = self.marketplace_contract.functions.registerAgent(
            capabilities, price_per_task
        ).build_transaction({
            'from': self.account.address,
            'gas': 200000,
            'gasPrice': self.w3.to_wei('20', 'gwei'),
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(txn, self.account.key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        return self.w3.eth.wait_for_transaction_receipt(tx_hash)
    
    async def claim_bounty_payment(self, bounty_id: int):
        """Claim bounty reward"""
        txn = self.marketplace_contract.functions.awardBounty(bounty_id, self.account.address).build_transaction({
            'from': self.account.address,
        })
        # Sign & send...
