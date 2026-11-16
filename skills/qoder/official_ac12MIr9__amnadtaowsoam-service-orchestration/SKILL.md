---
id: SKL-service-SERVICEORCHESTRATION
name: Service Orchestration
description: 'Patterns for orchestrating multiple microservices in Docker Compose
  and Kubernetes environments. This skill covers service dependency management, health
  checks, service discovery, load balancing, and '
version: 1.0.0
status: active
owner: '@cerebra-team'
last_updated: '2026-02-22'
category: Backend
tags:
- api
- backend
- server
- database
stack:
- Python
- Node.js
- REST API
- GraphQL
difficulty: Intermediate
---

# Service Orchestration

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Patterns for orchestrating multiple microservices in Docker Compose and Kubernetes environments. This skill covers service dependency management, health checks, service discovery, load balancing, and deployment strategies for building robust, scalable microservices architectures.

## Why This Matters
Service orchestration is critical for microservices because it:

- **Manages complexity** of multiple interdependent services
- **Enables zero-downtime deployments** with advanced strategies
- **Provides automatic service discovery** for dynamic environments
- **Implements health checks** for self-healing systems
- **Distributes traffic** efficiently across service instances
- **Scales services automatically** based on demand

---

## Core Concepts & Rules

### 1. Core Principles
- Follow established patterns and conventions
- Maintain consistency across codebase
- Document decisions and trade-offs

### 2. Implementation Guidelines
- Start with the simplest viable solution
- Iterate based on feedback and requirements
- Test thoroughly before deployment


## Inputs / Outputs / Contracts
#

## Skill Composition
* **Depends on**: [git-workflow](..\..\01-foundations\git-workflow/SKILL.md)
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: [docker](..\docker-compose/SKILL.md), [kubernetes](..\kubernetes-deployment/SKILL.md)

## Quick Start / Implementation Example

1. Review requirements and constraints
2. Set up development environment
3. Implement core functionality following patterns
4. Write tests for critical paths
5. Run tests and fix issues
6. Document any deviations or decisions

```python
# Example implementation following best practices
def example_function():
    # Your implementation here
    pass
```


## Assumptions
- Services are containerized with Docker
- Services expose health check endpoints
- Network connectivity between services is available
- Team has experience with Docker and/or Kubernetes
- Infrastructure resources are available

## Compatibility & Prerequisites

* **Supported Versions**:
  - Python 3.8+
  - Node.js 16+
  - Modern browsers (Chrome, Firefox, Safari, Edge)
* **Required AI Tools**:
  - Code editor (VS Code recommended)
  - Testing framework appropriate for language
  - Version control (Git)
* **Dependencies**:
  - Language-specific package manager
  - Build tools
  - Testing libraries
* **Environment Setup**:
  - `.env.example` keys: `API_KEY`, `DATABASE_URL` (no values)


## Test Scenario Matrix (QA Strategy)

| Type | Focus Area | Required Scenarios / Mocks |
| :--- | :--- | :--- |
| **Unit** | Core Logic | Must cover primary logic and at least 3 edge/error cases. Target minimum 80% coverage |
| **Integration** | DB / API | All external API calls or database connections must be mocked during unit tests |
| **E2E** | User Journey | Critical user flows to test |
| **Performance** | Latency / Load | Benchmark requirements |
| **Security** | Vuln / Auth | SAST/DAST or dependency audit |
| **Frontend** | UX / A11y | Accessibility checklist (WCAG), Performance Budget (Lighthouse score) |


## Technical Guardrails & Security Threat Model

### 1. Security & Privacy (Threat Model)
* **Top Threats**: Injection attacks, authentication bypass, data exposure
- [ ] **Data Handling**: Sanitize all user inputs to prevent Injection attacks. Never log raw PII
- [ ] **Secrets Management**: No hardcoded API keys. Use Env Vars/Secrets Manager
- [ ] **Authorization**: Validate user permissions before state changes

### 2. Performance & Resources
- [ ] **Execution Efficiency**: Consider time complexity for algorithms
- [ ] **Memory Management**: Use streams/pagination for large data
- [ ] **Resource Cleanup**: Close DB connections/file handlers in finally blocks

### 3. Architecture & Scalability
- [ ] **Design Pattern**: Follow SOLID principles, use Dependency Injection
- [ ] **Modularity**: Decouple logic from UI/Frameworks

### 4. Observability & Reliability
- [ ] **Logging Standards**: Structured JSON, include trace IDs `request_id`
- [ ] **Metrics**: Track `error_rate`, `latency`, `queue_depth`
- [ ] **Error Handling**: Standardized error codes, no bare except
- [ ] **Observability Artifacts**:
    - **Log Fields**: timestamp, level, message, request_id
    - **Metrics**: request_count, error_count, response_time
    - **Dashboards/Alerts**: High Error Rate > 5%


## Agent Directives
When orchestrating services:

1. **Always implement health checks** for all services
2. **Use service discovery** for dynamic environments
3. **Set resource limits** to prevent resource exhaustion
4. **Implement graceful shutdown** handling
5. **Monitor all services** with centralized logging
6. **Plan for failures** with retry and fallback mechanisms

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Circular Dependencies**: Services depending on each other
2. **Missing Health Checks**: No proper health monitoring
3. **No Resource Limits**: Not setting resource constraints
4. **Hardcoded Configuration**: Not using environment variables
5. **No Graceful Shutdown**: Services not handling SIGTERM
6. **Tight Coupling**: Services too tightly coupled

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

