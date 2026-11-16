---
id: SKL-sdn-SDNNFVORCHESTRATION
name: Sdn Nfv Orchestration
description: SDN/NFV Orchestration enables dynamic network service provisioning and
  automation through Software-Defined Networking (SDN) and Network Functions Virtualization
  (NFV). This skill covers the design, im
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

# Sdn Nfv Orchestration

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
SDN/NFV Orchestration enables dynamic network service provisioning and automation through Software-Defined Networking (SDN) and Network Functions Virtualization (NFV). This skill covers the design, implementation, and operation of SDN controllers, NFV orchestrators, and VNF/CNF lifecycle management to enable network-as-a-service capabilities.

## Why This Matters
- **Agility**: Enables rapid service deployment and scaling without hardware changes
- **Cost Efficiency**: Optimizes resource utilization through network function virtualization
- **Automation**: Reduces manual configuration and operational overhead
- **Service Innovation**: Enables new network services to be deployed quickly
- **Multi-Tenancy**: Supports isolation and resource sharing for multiple tenants

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
* **Inputs**:
  - Network topology and infrastructure
  - Service requirements and SLAs
  - VNF/CNF catalog
  - Resource capacity and availability
  - Orchestration policies and constraints
* **Entry Conditions**:
  - SDN controller is deployed and accessible
  - NFV orchestrator (ONAP, OpenStack, etc.) is configured
  - Network infrastructure supports virtualization
  - Resource inventory is available
* **Outputs**:
  - Provisioned network services
  - VNF/CNF instances with configurations
  - Network slice configurations
  - Service health and status reports
* **Artifacts Required (Deliverables)**:
  - Service descriptors and templates
  - VNF/CNF deployment manifests
  - Network slice configurations
  - Orchestration logs and audit trails
* **Acceptance Evidence**:
  - Services are provisioned within SLA timeframes
  - Resource allocation matches service requirements
  - Network slices meet QoS specifications
  - VNFs/CNFs are healthy and operational
* **Success Criteria**:
  - Service provisioning time: <5min
  - Resource utilization: ≥80%
  - Service availability: ≥99.9%
  - Slice QoS compliance: 100%

## Skill Composition
* **Depends on**: [`kubernetes-deployment`](15-devops-infrastructure/kubernetes-deployment/SKILL.md), [`service-orchestration`](15-devops-infrastructure/service-orchestration/SKILL.md)
* **Compatible with**: [`docker-patterns`](15-devops-infrastructure/docker-patterns/SKILL.md), [`load-balancing`](15-devops-infrastructure/load-balancing/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [`multi-cloud-patterns`](15-devops-infrastructure/multi-cloud-patterns/SKILL.md), [`disaster-recovery`](40-system-resilience/disaster-recovery/SKILL.md)

---

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


## Assumptions / Constraints / Non-goals

* **Assumptions**:
  - Development environment is properly configured
  - Required dependencies are available
  - Team has basic understanding of domain
* **Constraints**:
  - Must follow existing codebase conventions
  - Time and resource limitations
  - Compatibility requirements
* **Non-goals**:
  - This skill does not cover edge cases outside scope
  - Not a replacement for formal training


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


## Agent Directives & Error Recovery
*(ข้อกำหนดสำหรับ AI Agent ในการคิดและแก้ปัญหาเมื่อเกิดข้อผิดพลาด)*

- **Thinking Process**: Analyze root cause before fixing. Do not brute-force.
- **Fallback Strategy**: Stop after 3 failed test attempts. Output root cause and ask for human intervention/clarification.
- **Self-Review**: Check against Guardrails & Anti-patterns before finalizing.
- **Output Constraints**: Output ONLY the modified code block. Do not explain unless asked.


## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns / Pitfalls

* ⛔ **Don't**: Log PII, catch-all exception, N+1 queries
* ⚠️ **Watch out for**: Common symptoms and quick fixes
* 💡 **Instead**: Use proper error handling, pagination, and logging


## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

