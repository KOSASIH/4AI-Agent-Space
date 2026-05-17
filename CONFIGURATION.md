# Configuration Reference

Complete settings for development, staging, and production.

## File Locations

```
Primary: config/agent_config.yaml
Kubernetes: ConfigMap (auto-generated)
Docker: docker-compose.override.yaml
Env vars: Override all settings
```

## Core Configuration (`config/agent_config.yaml`)

### Agent Engine
```yaml
agents:
  # LLM Model
  default_model: "gpt-4o-mini"        # gpt-4o, gpt-4o-mini, llama3
  temperature: 0.1                    # 0.0-1.0 (deterministic-creative)
  max_iterations: 15                  # Reasoning steps per agent
  max_context_tokens: 128000          # Context window
  
  # Team coordination
  max_team_size: 5                    # Agents per task
  team_selection: "ml"                # "ml", "greedy", "round_robin"
  
  # Safety
  sandbox_tools: true                 # Docker sandbox for code exec
  timeout_seconds: 300                # Per-task timeout
```

### Memory Systems
```yaml
memory:
  # Vector database
  chroma:
    persist_directory: "./chroma_db"
    embedding_model: "sentence-transformers/all-MiniLM-L6-v2"
    collection_name: "agent_memory"
    replicas: 3                       # K8s only
  
  # Session memory  
  redis:
    host: "localhost"
    port: 6379
    db: 0
    password: null
    max_memory_mb: 4096
  
  # Conversation history
  history_limit: 10                   # Messages per conversation
  reflection_enabled: true            # Agent self-reflection
```

### Orchestrator
```yaml
orchestrator:
  max_parallel_tasks: 100             # Concurrent orchestration
  retry_attempts: 3
  retry_backoff: "exponential"        # linear, exponential, jitter
  failure_threshold: 0.1              # Fail task if >10% agent failure
  
  # Team building
  team_build_timeout: 30              # Seconds to assemble team
  min_team_quality: 0.8               # Reject low-quality teams
```

### API Server
```yaml
api:
  host: "0.0.0.0"
  port: 8000
  rate_limit_rpm: 6000                # Requests per minute
  cors_origins: 
    - "http://localhost:3000"
    - "https://dashboard.yourdomain.com"
  jwt_secret: "change-in-production!"
```

### Autoscaling (Kubernetes)
```yaml
autoscaler:
  enabled: true
  min_replicas: 3
  max_replicas: 100
  cpu_threshold: 70                   # % CPU utilization
  memory_threshold: 80                # % Memory utilization
  queue_threshold: 100                # Redis queue length
```

## Environment Variable Overrides

All YAML settings can be overridden:

```
# Agent settings
AGENTS__DEFAULT_MODEL=gpt-4o
AGENTS__TEMPERATURE=0.2
AGENTS__MAX_ITERATIONS=20

# Redis
MEMORY__REDIS__HOST=redis-cluster
MEMORY__REDIS__PASSWORD=supersecret

# API
API__RATE_LIMIT_RPM=10000
```

## Plugin-Specific Config

`src/marketplace/plugins/*/plugin.yaml`:

```yaml
name: "QuantumTrader"
version: "3.1.0"
author: "AI Research Lab"
description: "Advanced crypto trading agent"

capabilities:
  - "trading" 
  - "prediction"
  - "finance"

pricing:
  price_per_task: 0.05      # AET per task
  max_concurrent: 10        # Parallel executions

resources:
  cpu_request: "500m"
  memory_request: "2Gi"
  gpu: false

tools:
  - "market_data"
  - "technical_analysis"
  - "risk_management"

settings:
  trading_pairs: ["BTC-USD", "ETH-USD"]
  risk_limit: 0.02           # 2% max loss
```

## Resource Profiles

### Development (Local)
```yaml
agents:
  replicas: 1
  cpu: "100m"
  memory: "512Mi"
chroma:
  replicas: 1
```

### Production Small (100 users)
```yaml
agents:
  replicas: 5
  cpu: "500m" 
  memory: "2Gi"
chroma:
  replicas: 3
  storage: "50Gi"
```

### Production Large (10k+ users)
```yaml
agents:
  replicas: 50
  cpu: "2000m"
  memory: "8Gi"
chroma:
  replicas: 5
  storage: "500Gi"
```

## Logging Configuration

```yaml
logging:
  level: "INFO"                    # DEBUG|INFO|WARN|ERROR
  format: "json"                   # json|text|logfmt
  max_file_size: "100MB"
  retention_days: 30
  
  # Structured fields
  fields:
    task_id: true
    agent_id: true  
    user_id: true
    cost: true
```

## Security Configuration

```yaml
security:
  # Data protection
  pii_redaction: true              # Auto PII removal
  prompt_guards: true              # Jailbreak protection
  
  # Network
  network_allowlist:
    - "api.openai.com"
    - "duckduckgo.com"
    - "redis-cluster"
  
  # Sandboxing
  code_sandbox: "docker"           # docker|firecracker|none
  max_exec_time: 60                # Code execution timeout
```

## Performance Profiles

### Speed-First (Low latency)
```yaml
agents:
  model: "gpt-4o-mini"
  max_iterations: 8
  max_team_size: 3
api:
  rate_limit_rpm: 10000
```

### Quality-First (Best results)
```yaml
agents:
  model: "gpt-4o"
  max_iterations: 25
  temperature: 0.3
  max_team_size: 7
```

## Database Schema (Postgres)

Auto-migrated by Alembic:

```sql
-- tasks table
CREATE TABLE tasks (
  id UUID PRIMARY KEY,
  status VARCHAR(20),
  result JSONB,
  cost DECIMAL,
  created_at TIMESTAMP
);

-- agents table  
CREATE TABLE agents (
  id UUID PRIMARY KEY,
  name VARCHAR(100),
  reputation DECIMAL,
  earnings DECIMAL
);
```

## Health Check Endpoints

```
/health          → Overall system health
/ready           → Ready for traffic
/metrics         → Prometheus metrics
/debug/pprof     → Go pprof (orchestrator)
```
