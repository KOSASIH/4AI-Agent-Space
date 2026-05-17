---
name: 'Production PR Template'
about: 'Submit a production-ready pull request'
title: ''
labels: ''
assignees: ''

---

## 🎯 What This PR Does

**Brief description (1 sentence):**

Closes #123

## 📋 Type of Change

- [ ] 🎉 **New Feature**
- [ ] 🐛 **Bug Fix** 
- [ ] ✨ **Enhancement**
- [ ] 📚 **Documentation**
- [ ] 🚀 **Performance**
- [ ] 🔒 **Security**
- [ ] ♻️ **Refactor**
- [ ] ✅ **Tests**
- [ ] 🤖 **Agent Plugin**
- [ ] 🌐 **Infrastructure**

## 📈 Changes Made

### Code Changes
```
src/agents/quantum_agent.py  | +45 -12
src/marketplace/plugins/...  | New agent plugin
tests/integration/test_api.py| +23 -0
docs/API.md                 | +15 -3
```

### New Dependencies
```
None added / Added: numpy==1.24.3
```

## ✅ Pre-Merge Checklist **(REQUIRED)**

### Code Quality
- [ ] `make format` ✅ Black + Prettier
- [ ] `make lint` ✅ ESLint + flake8
- [ ] `make typecheck` ✅ mypy strict
- [ ] `make security` ✅ Snyk + Trivy clean

### Testing
- [ ] `make test` ✅ 90%+ coverage
- [ ] `make test-e2e` ✅ End-to-end passes
- [ ] Load tested ✅ 10k req/min stable

### Verification Steps
```
1. docker-compose up -d
2. make test-agent NAME=new_plugin  
3. curl /v1/tasks/... → Success
4. Dashboard shows new agent ✓
```

## 📊 Performance Impact

```
Benchmark Results:
├── Latency p95: 2.1s → 1.9s (-10%)
├── Throughput: 12k → 14k tasks/min (+17%)
└── Memory usage: unchanged
```

## 🔒 Security Review

- [ ] No secrets in code
- [ ] Input validation added
- [ ] PII redaction verified
- [ ] Prompt injection tested

## 📝 Changelog

```
## [Unreleased]

### Added
- New trading agent plugin (#123)

### Fixed
- Memory leak in orchestrator pool (#124)
```

## 🧪 Manual Testing

### Browser Test
1. Load dashboard → New agent visible
2. Submit task → Team includes new agent
3. Results accurate → Sources verified

### API Test
```bash
curl -X POST /v1/tasks \
  -d '{"task": "test new agent"}' \
  → Returns expected result
```

## 📱 Screenshots

**Before:**
```
[Dashboard without new agent]
```

**After:**
```
[Dashboard with new agent visible]
```

## 🌐 External Impact

- [ ] API backwards compatible
- [ ] Config changes documented
- [ ] Migration scripts included (if needed)

## 👥 Reviewers Needed

```
Core reviewers: @agent-core-team
Infra: @infra-team  
Security: @security-team
```

## 🚀 Deployment Notes

```
Helm upgrade: No breaking changes
Docker image: Tagged v2.1.3
Terraform: No state changes
```

---

## **Reviewer Verification** *(Fill after review)*

**Code Review:** @username  
**Tests Verified:** @username  
**Security Approved:** @username  
**Performance OK:** @username  
**Docs Accurate:** @username  

```
Merge Method: Squash & Merge
Release: v2.1.3 (patch)
```

**Ready for merge when all boxes checked! 🚀**
```
