# Quickstart Guide

Get production-ready AI agents running in under 60 seconds.

## Prerequisites (30 seconds)

1. **Docker & Docker Compose**
```bash
docker --version  # Docker 20+
docker-compose --version  # v2+
```

2. **OpenAI API Key**
```bash
export OPENAI_API_KEY="sk-your-key-here"
```

3. **Optional: Node.js (Web3 dashboard)**
```bash
node --version  # v18+
```

## Step 1: Clone & Launch (20 seconds)

```bash
git clone https://github.com/KOSASIH/4AI-Agent-Space
cd 4AI-Agent-Space
docker-compose up -d
```

**Wait for startup:**
```bash
docker-compose logs -f | grep "Dashboard ready"
```

## Step 2: Verify Services (5 seconds)

Open these URLs:

```
Dashboard:      http://localhost:8501
API Docs:       http://localhost:8000/docs  
Web3 UI:        http://localhost:3000
Metrics:        http://localhost:9090
```

## Step 3: Submit First Task (10 seconds)

**Via curl:**
```bash
curl -X POST http://localhost:8000/v1/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d '{
    "task": "Research the latest advancements in quantum computing hardware",
    "priority": "high"
  }'
```

**Expected response:**
```json
{
  "task_id": "task_1735689201478",
  "status": "queued", 
  "estimated_time": "45s"
}
```

## Step 4: Watch Live Progress (Real-time)

**Terminal:**
```bash
curl http://localhost:8000/v1/tasks/task_1735689201478
```

**Or WebSocket:**
```bash
wscat -c "ws://localhost:8000/ws/tasks/task_1735689201478"
```

**Expected completion:**
```json
{
  "status": "completed",
  "result": "Quantum computing advancements...",
  "team": ["researcher_v2.1", "analyst_pro"],
  "cost": 0.187,
  "confidence": 0.94
}
```

## Step 5: Python SDK (Optional - 10 seconds)

```bash
pip install 4ai-agent-client
```

```python
# test_client.py
from agent_space import Client
import asyncio

async def main():
    client = Client(api_key="sk-...")
    result = await client.create_task(
        "Build a FastAPI service with Redis cache"
    )
    print(result.content)

asyncio.run(main())
```

```bash
python test_client.py
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Port 8501 busy" | `docker-compose down && docker-compose up -d` |
| "API key invalid" | Check `OPENAI_API_KEY` export |
| "Chroma connection" | `docker-compose restart chroma` |
| "Agents not responding" | Check `docker-compose logs orchestrator` |

## Next Steps

1. **Customize agents** → [Configuration Guide](CONFIGURATION.md)
2. **Production deploy** → [Deployment Guide](DEPLOYMENT.md)
3. **Add plugins** → [Marketplace](MARKETPLACE.md)
4. **Scale up** → [Scaling](SCALING.md)

## Production Verification Checklist

- [ ] Dashboard loads (localhost:8501)
- [ ] API docs work (localhost:8000/docs)
- [ ] First task completes successfully
- [ ] WebSocket updates in real-time
- [ ] Metrics endpoint returns data
- [ ] Docker logs show no errors

**🎉 Congratulations! Your AI agent swarm is operational.**
