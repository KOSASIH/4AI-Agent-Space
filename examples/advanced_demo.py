"""
🚀 Advanced Demo - Multi-Agent Quantum System
"""

import asyncio
from src.agents.quantum_agent import QuantumAgent
from src.memory.vector_memory import VectorMemory
from src.tools.web_search import advanced_web_search, scrape_website

async def main():
    # Initialize memory
    memory = VectorMemory()
    
    # Create specialist agents
    researcher = QuantumAgent("Researcher", tools=[advanced_web_search, scrape_website])
    analyst = QuantumAgent("Analyst")
    writer = QuantumAgent("Writer")
    
    # Complex research task
    task = """
    Research the latest advancements in quantum computing hardware as of 2024.
    Identify top 3 companies, their breakthroughs, and future implications.
    Provide sources and technical details.
    """
    
    # Orchestrated execution
    results = []
    for agent in [researcher, analyst, writer]:
        result = await agent.execute(task)
        results.append(result)
        print(f"✅ {agent.name}: {result['result'].content[:200]}...")
    
    print("🎉 Multi-Agent Mission Complete!")

if __name__ == "__main__":
    asyncio.run(main())
