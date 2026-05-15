"""
🧠 Advanced Hybrid Vector Memory with Temporal Awareness
"""

import chromadb
from chromadb.config import Settings
from datetime import datetime, timedelta
from typing import List, Dict, Any
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings

class VectorMemory:
    def __init__(self, persist_directory: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2"
        )
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        return self.client.get_or_create_collection(
            name="agent_memory",
            metadata={"hnsw:space": "cosine"}
        )
    
    def store_episode(self, agent_id: str, messages: List[Dict], score: float):
        """Store complete interaction episode with temporal metadata"""
        timestamp = datetime.now().isoformat()
        
        for i, msg in enumerate(messages):
            content = msg.get('content', '')
            embedding = self.embeddings.embed_query(content)
            
            self.collection.add(
                embeddings=[embedding],
                documents=[content],
                metadatas=[{
                    "agent_id": agent_id,
                    "timestamp": timestamp,
                    "message_type": msg.get('type', 'unknown'),
                    "position": i,
                    "episode_score": score,
                    "recency_weight": self._calculate_recency_weight(timestamp)
                }],
                ids=[f"{agent_id}_{timestamp}_{i}"]
            )
    
    def hybrid_search(self, query: str, agent_id: str = None, k: int = 10) -> List[Dict]:
        """Semantic + temporal + agent-specific hybrid search"""
        query_embedding = self.embeddings.embed_query(query)
        
        # Base semantic search
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=k*2,
            where={"agent_id": agent_id} if agent_id else {}
        )
        
        # Re-rank by hybrid score: semantic + recency + relevance
        scored_results = []
        for i, (doc, meta, dist) in enumerate(zip(results['documents'][0], results['metadatas'][0], results['distances'][0])):
            recency_weight = meta['recency_weight']
            semantic_score = 1 - dist
            hybrid_score = 0.6 * semantic_score + 0.3 * recency_weight + 0.1 * meta['episode_score']
            
            scored_results.append({
                'content': doc,
                'metadata': meta,
                'score': hybrid_score
            })
        
        return sorted(scored_results, key=lambda x: x['score'], reverse=True)[:k]
    
    def _calculate_recency_weight(self, timestamp: str) -> float:
        """Exponential decay based on recency"""
        dt = datetime.fromisoformat(timestamp)
        hours_ago = (datetime.now() - dt).total_seconds() / 3600
        return np.exp(-hours_ago / 24)  # 24h half-life
