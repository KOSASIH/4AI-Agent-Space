"""
📱 Real-time Agent Dashboard (Streamlit)
"""

import streamlit as st
import asyncio
import plotly.graph_objects as go
from src.orchestrator.multi_agent_orchestrator import MultiAgentOrchestrator
from src.monitoring.agent_monitor import AgentMonitor

async def main():
    st.set_page_config(page_title="4AI Agent Space", layout="wide")
    
    # Sidebar
    st.sidebar.title("🤖 Agent Control")
    task = st.sidebar.text_area("Enter complex task:", height=100)
    
    if st.sidebar.button("🚀 Launch Multi-Agent Mission"):
        with st.spinner("Assembling quantum team..."):
            orchestrator = MultiAgentOrchestrator({
                "researcher": "research_agent",
                "analyst": "analyst_agent", 
                "writer": "writer_agent"
            })
            
            result = await orchestrator.execute_collaborative_task(task)
            st.session_state.result = result
    
    # Main dashboard
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Missions Completed", len(st.session_state.get("results", [])))
    
    with col2:
        monitor = AgentMonitor()
        metrics = monitor.get_dashboard_data()
        st.metric("Avg Success Rate", f"{metrics.get('avg_success', 0):.1%}")
    
    with col3:
        st.metric("Active Agents", 12)
    
    # Results
    if "result" in st.session_state:
        st.subheader("🎯 Mission Results")
        result = st.session_state.result
        
        for agent, data in result["individual_results"].items():
            with st.expander(f"📋 {agent}"):
                st.write(data["result"].content)
        
        st.success("✅ Final Synthesized Result")
        st.write(result["final_result"])

if __name__ == "__main__":
    asyncio.run(main())
