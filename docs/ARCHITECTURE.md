# System Architecture

Production-grade design for 1M+ tasks/day at 99.99% uptime.

## High-Level Overview

```
                    ┌─────────────────┐
                    │   End Users     │
                    │ REST/WS/Web     │
                    └──────────┬──────┘
                               │
                    ┌──────────▼──────────┐
                    │    API Gateway      │
                    │     FastAPI         │
                    │ Rate limiting       │
                    │ Auth/JWT            │
                    └──────────┬──────────┘
                               │ gRPC
                    ┌──────────▼──────────┐
                    │   Orchestrator      │
                    │ ┌────────────────┐ │
                    │ │ Team Assembly  │ │
                    │ │ Task Router    │ │
                    │ │ Load Balancer  │ │
                    │ └────────────────┘ │
                    └──────────┬──────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
        ┌───────▼──────┐ ┌────▼──────┐ ┌────▼──────┐
        │   Agent Pods  │ │ ChromaDB  │ │  Redis    │
        │ (10-500)      │ │ Memory    │ │ Queue     │
        │ QuantumAgent  │ │ 3 replicas│ │ Cluster   │
        └───────────────┘ └────────────┘ └──────────┘
                │              │              │
         ┌──────▼──────┐ ┌────▼──────┐ ┌────▼──────┐
         │   Postgres   │ │   Grafana  │ │  Loki     │
         │ Agent State  │ │ Dashboard  │ │   Logs    │
         └──────────────┘ └────────────┘ └──────────┘
```

## Component Breakdown

### 1. API Gateway (FastAPI)
```
Responsibilities:
- Authentication (JWT + API keys)
- Rate limiting (Redis)
- Request validation
- WebSocket broadcasting
- Metrics collection
Scaling: Stateless, 10+ replicas
```

### 2. Orchestrator (Core Brain)
```
Core logic:
- Dynamic team assembly (ML-based)
- Task decomposition + routing
- Load balancing across agent pools
- Failure recovery + retry logic
Scaling: Stateful, 3-10 replicas
```

### 3. Quantum Agent Pool
```
Agent lifecycle:
- Probabilistic decision making
- Tool calling (web/code/files)
- RAG memory lookup
- Self-reflection + improvement
Scaling: Stateless, 10-500+ replicas
Memory: 2Gi RAM / 2 CPU per pod
```

### 4. Persistent Storage
```
ChromaDB (Vector Memory): 3 replicas, 100Gi PV
Redis (Task Queue): Cluster, 99.99% SLA
Postgres (State): Managed RDS, 5min backups
```

## Data Flow (Task Lifecycle)

```
1. User submits task → API Gateway
2. Auth/validate → Orchestrator  
3. Team assembly (5 agents) → Redis queue
4. Agents execute → Chroma memory lookup
5. Partial results → Orchestrator coordination
6. Final synthesis → Postgres storage
7. WebSocket push → User notification
8. Metrics → Prometheus
```

## Scaling Architecture

### Horizontal Pod Autoscaler (HPA)
```
Triggers:
- CPU: 70% average
- Memory: 80% average  
- Queue length: Redis llen > 100
- Custom: ML prediction model

Min: 3 replicas | Max: 500 replicas
```

### Vertical Scaling
```
Small:    m5.large (2CPU/8Gi) → 1k tasks/min
Medium:   m5.4xlarge → 10k tasks/min
Large:    m5.24xlarge → 75k tasks/min
GPU:      g5.12xlarge → Code/vision agents
```

## Fault Tolerance

```
99.99% Uptime SLA:
├── 3x ChromaDB replicas (etcd consensus)
├── Redis Sentinel (3 masters)
├── Postgres Read Replicas  
├── Agent HPA (auto-recovery)
├── Circuit breakers (per-agent)
└── Graceful degradation
```

## Security Model

```
Authentication:
├── API Keys (OpenAI-style)
├── JWT tokens (stateless)
└── Web3 wallet signatures

Data Protection:
├── Input sanitization
├── PII redaction (NER models)
├── Audit logging (Loki)
└── SOC2/GDPR compliant
```

## Observability Stack

```
Metrics: Prometheus + Grafana (50+ dashboards)
Logs: Loki + Grafana (structured JSON)
Traces: Jaeger (distributed tracing)
Alerts: Alertmanager (PagerDuty/Slack)
```

## Deployment Targets

```
✅ AWS EKS (terraform/aws/)
✅ Google GKE (terraform/gcp/)  
✅ Azure AKS (terraform/azure/)
✅ On-prem K8s (helm charts)
✅ Docker Compose (dev)
```

## Performance Characteristics

```
p50 Latency: 1.2s
p95 Latency: 2.8s  
p99 Latency: 7.1s
Error Rate: 0.13%
Throughput: 300k tasks/hour (75 replicas)
```
