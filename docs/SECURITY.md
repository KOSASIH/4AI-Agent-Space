# Security & Compliance

Enterprise-grade security for production deployments.

## Threat Model

```
Attack Vectors Assessed:
├── API Abuse (rate limiting)
├── Agent Jailbreaking (prompt guards)
├── Data exfiltration (PII redaction)
├── Denial of Service (resource limits)
├── Token theft (Web3 signatures)
└── Supply chain (SBOM + vuln scans)
```

## Authentication & Authorization

### API Key Protection
```
- Rate limited (60-6000 RPM tiers)
- IP whitelisting support
- Key rotation (30-day expiry)
- Audit logging (all API calls)
```

### JWT Tokens
```
- RS256 signing (JWKS endpoint)
- 15min access + 24h refresh
- Role-based claims (user/admin/agent)
- Revocation list (Redis)
```

### Web3 Signatures
```
- EIP-712 typed data signing
- Chain ID enforcement (replay protection)
- Nonce validation
- Agent reputation gating
```

## Data Protection

### PII Redaction
```
Automatic NER-based redaction:
- Names, emails, phone numbers
- Credit cards, SSNs
- API keys, passwords
- Config: ENABLE_PII_REDACTION=true
```

### Encryption at Rest
```
Postgres: AWS RDS encryption
ChromaDB: Volume encryption
Redis: TLS + AUTH
Config files: SOPS encryption
```

### Encryption in Transit
```
- TLS 1.3 (all services)
- HTTP/2 + HSTS
- Certificate rotation (cert-manager)
- mTLS between services (Istio)
```

## Agent Safety

### Prompt Injection Protection
```
Multi-layer guards:
1. System prompt isolation
2. Output filtering (LLM-as-judge)  
3. Jailbreak detection (95% accuracy)
4. Human-in-loop for high-risk tasks
```

### Resource Limits
```
Per-agent sandbox:
- CPU: 2 cores max
- Memory: 8Gi max
- Network: Outbound only (allowlist)
- File system: tmpfs (ephemeral)
- Execution timeout: 300s max
```

### Tool Safety
```
Code execution:
├── Docker sandbox (non-root)
├── Network isolation  
├── File read-only
└── Timeout + OOM killer

Web scraping:
├── Rate limiting (10 req/s)
├── User-agent rotation
└── Robots.txt compliance
```

## Infrastructure Security

### Kubernetes Hardening
```
Pod Security Standards: Restricted
Network Policies: Default deny
Admission controllers: Gatekeeper
Image scanning: Trivy + Cosign
Secrets: External Secrets Operator
```

### Supply Chain Security
```
Docker images:
├── Multi-stage builds
├── Non-root users
├── SBOM generation (syft)
├── Sigstore Cosign signing

Dependencies:
├── Dependabot weekly updates
├── Snyk vulnerability scanning
└── GitHub Advanced Security
```

## Compliance

```
SOC2 Type II: In progress (Q1 2025)
GDPR: Data residency controls
HIPAA: Available enterprise tier
ISO 27001: Planned Q3 2025
```

## Security Headers

```
Strict-Transport-Security: max-age=31536000
Content-Security-Policy: script-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Referrer-Policy: strict-origin
Permissions-Policy: geolocation=()
```

## Incident Response

```
Detection: 24/7 monitoring + AI anomaly detection
Response: 15min MTTR (enterprise SLA)
Post-mortem: Automated root cause analysis
Notification: Automatic PagerDuty/Slack
```

## Vulnerability Disclosure

```
Report to: security@4ai.space
PGP Key: Available on keybase.io/4ai
Bounty Program: Up to $50,000 (HackerOne)
Response SLA: 48 hours
```

## Configuration Hardening

### Production Settings
```yaml
# security.yaml
api:
  rate_limit: 6000  # RPM
  cors_origins: []  # Empty in prod
  
agents:
  sandbox: true
  network_allowlist: ["api.openai.com"]
  
secrets:
  rotation_interval: "30d"
```

## Audit Logging

```
All requests logged to Loki:
├── User ID + IP + timestamp
├── Request/response bodies (redacted)
├── Agent decisions + tool calls
├── 90-day retention (GDPR)
```

## Penetration Testing

```
Annual pentests by Cure53
Continuous automated scanning
Bug bounty: HackerOne ($10k-$50k)
```

**Report security issues:** security@4ai.space
