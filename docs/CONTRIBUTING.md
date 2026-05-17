# Contributing Guide

Thank you for your interest in contributing! We welcome all contributions.

## Development Workflow

### 1. Setup Development Environment

```bash
git clone https://github.com/KOSASIH/4AI-Agent-Space
cd 4AI-Agent-Space
make dev-setup
```

### 2. Local Development Stack

```bash
# Start dev environment
make dev-up

# Available services:
# Dashboard: http://localhost:8501
# API: http://localhost:8000/docs
# Dev database: localhost:5432
```

### 3. Code Style

```
Python: Black + isort + mypy
JS: Prettier + ESLint
YAML: yamllint
Docker: hadolint
```

**Auto-format on commit:**
```bash
pip install pre-commit
pre-commit install
```

### 4. Testing

```
Unit tests: pytest tests/unit/
Integration: pytest tests/integration/
E2E: playwright test/
Load test: locust -f locustfile.py
```

**Run tests:**
```bash
make test          # All tests
make test-unit     # Unit only
make test-e2e      # End-to-end
make test-load     # Load testing
```

### 5. Creating Agents (Plugin System)

1. **Create new agent:**
```bash
make new-agent NAME=my_trader VERSION=1.0.0
```

2. **Agent structure:**
```
src/marketplace/plugins/my_trader/
├── __init__.py
├── agent.py          # QuantumAgent subclass
├── tools.py          # Custom tools
└── plugin.yaml       # Metadata
```

3. **Test locally:**
```bash
make test-agent NAME=my_trader
```

4. **Publish to marketplace:**
```bash
make publish-agent NAME=my_trader
```

### 6. Pull Request Workflow

1. **Fork repository**
2. **Create feature branch:**
```bash
git checkout -b feature/my-agent
```

3. **Development workflow:**
```bash
# Make changes
git add .
git commit -m "feat: add my trading agent (#123)"

# Run tests
make test

# Push
git push origin feature/my-agent
```

4. **PR Requirements:**
```
✅ Tests pass (90%+ coverage)
✅ Black formatting
✅ No linting errors  
✅ Docs updated
✅ CHANGELOG entry
✅ Version bump if breaking
```

### 7. Commit Message Format

```
feat: add new quantum agent
fix: resolve memory leak in orchestrator
docs: update API reference
refactor: improve agent pooling
test: add integration tests for marketplace
chore: update dependencies
```

## Agent Development Guidelines

### Capabilities Declaration
```python
PLUGIN_INFO = {
    "name": "MyTrader",
    "version": "1.0.0",
    "capabilities": ["trading", "prediction", "finance"],
    "price_per_task": 0.05
}
```

### Tool Integration
```python
@tool  
async def fetch_market_data(symbol: str) -> str:
    """Fetch real-time market data"""
    # Implementation
    pass
```

## Release Process

### Version Bumping
```bash
# Prepare release
npm version patch  # or minor/major
git push --follow-tags

# Build & publish
make release
```

### Changelog Automation
```
Automated CHANGELOG generation on release
Format: Keep a Changelog standard
```

## Code Owners

```
src/agents/          @agent-core-team
src/marketplace/     @plugin-maintainers  
src/orchestrator/    @orchestration-team
docs/                @docs-team
terraform/           @infra-team
```

## Support for Contributors

```
Questions: #contributors Discord channel
Agent review: @agent-reviewers
Infra review: @infra-reviewers
Security issues: security@4ai.space
```

## Security Policy

Report vulnerabilities to security@4ai.space
No public disclosure until fixed.

## Translation & Localization

See `TRANSLATIONS.md` for i18n guidelines.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---
Thank you for building the future of AI agents with us!
```
