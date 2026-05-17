# Production Deployment Guide

Complete instructions for all deployment targets.

## Environment Requirements

```
Kubernetes: 1.25+
Helm: 3.12+
Docker: 20+
Terraform: 1.5+
Node.js: 18+ (optional dashboard)
```

## 1. Docker Compose (Development - 60s)

```bash
# Clone and start
git clone https://github.com/KOSASIH/4AI-Agent-Space
cd 4AI-Agent-Space
export OPENAI_API_KEY="sk-..."
docker-compose up -d

# Verify
docker-compose ps  # All services UP
docker-compose logs orchestrator  # No errors
```

**Ports exposed:**
```
8501: Streamlit Dashboard
8000: FastAPI API
3000: Web3 Dashboard  
9090: Prometheus
```

**Stop:**
```bash
docker-compose down -v  # -v removes volumes
```

## 2. Kubernetes (Helm - Production - 5min)

### Add Helm Repository
```bash
helm repo add 4ai https://charts.4ai.space/
helm repo update
```

### Basic Install
```bash
helm install ai-platform 4ai/agent-space \
  --namespace ai-agent --create-namespace \
  --set openai.apiKey=$OPENAI_API_KEY
```

### Production Install (Full Config)
```bash
helm install ai-platform 4ai/agent-space \
  --namespace production --create-namespace \
  --values production-values.yaml \
  --set autoscaler.enabled=true \
  --set monitoring.prometheus.enabled=true
```

### Verify Deployment
```bash
# Check pods
kubectl get pods -n production

# Port-forward dashboard
kubectl port-forward svc/ai-platform 8501:80 -n production

# Check HPA
kubectl get hpa -n production
```

**production-values.yaml:**
```yaml
orchestrator:
  replicas: 5
memory:
  chroma:
    replicas: 3
    persistence:
      size: 100Gi
autoscaler:
  minReplicas: 3
  maxReplicas: 100
ingress:
  enabled: true
  hostname: agents.yourdomain.com
```

## 3. Terraform (Cloud Providers - 10min)

### AWS EKS
```bash
cd terraform/aws
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars (cluster name, region)
terraform init
terraform plan
terraform apply
```

**Outputs:**
```
cluster_endpoint = "https://..."
dashboard_url = "https://agents.yourdomain.com"
```

### Google GKE
```bash
cd terraform/gcp
terraform init
terraform apply -var="project_id=your-gcp-project"
```

### Azure AKS
```bash
cd terraform/azure
az login
terraform init
terraform apply
```

## 4. Custom Configuration

### Override via Helm Values
```yaml
# High-throughput config
agents:
  replicas: 20
  resources:
    requests:
      cpu: 500m
      memory: 2Gi
    limits:
      cpu: 2000m
      memory: 8Gi

# Large memory config  
chromadb:
  persistence:
    size: 500Gi
```

### Environment Variables
```bash
# Per-pod env vars
openai:
  apiKey: $OPENAI_API_KEY
  model: "gpt-4o-mini"  # Cost-optimized
redis:
  password: "supersecret"
```

## 5. Monitoring & Observability

### Prometheus + Grafana (Auto-installed)
```
Dashboard: http://localhost:3001/grafana
Default login: admin/prom-operator
Pre-built dashboards:
- Agent throughput
- Latency histograms  
- Error rates
- Queue depth
```

### Custom Alerts
```yaml
# values.yaml
prometheus:
  alerts:
    - alert: HighErrorRate
      expr: rate(agent_errors_total[5m]) > 0.01
      for: 2m
      labels:
        severity: critical
```

## 6. Upgrade Process

```bash
# Check current version
helm list -n production

# Upgrade (zero-downtime)
helm upgrade ai-platform 4ai/agent-space \
  --namespace production --reuse-values

# Rollback if needed
helm rollback ai-platform 1 -n production
```

## 7. Backup & Disaster Recovery

### Velero (Kubernetes Backup)
```bash
helm install velero vmware-tanzu/velero \
  --set configuration.provider=aws \
  --set credentials.secretContents.cloud=s3-credentials
```

### ChromaDB Backup
```bash
# PersistentVolume daily snapshots
kubectl get pv  # Check storage
```

## 8. Cost Optimization

```
Development:           Free (local)
Small Team (10 users): $99/month
Production (1k users): $450/month  
Enterprise (100k):    $2,100/month
```
