---
id: SKL-mec-MECNETWORKSLICING
name: Mec Network Slicing
description: This skill covers the architecture, implementation, and operation of
  5G/6G core network functions with focus on Multi-access Edge Computing (MEC) and
  Network Slicing. It enables building ultra-low lat
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

# Mec Network Slicing

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
This skill covers the architecture, implementation, and operation of 5G/6G core network functions with focus on Multi-access Edge Computing (MEC) and Network Slicing. It enables building ultra-low latency applications (sub-1ms) that require deterministic network performance, such as autonomous vehicles, industrial automation, and real-time AR/VR.

## Why This Matters
- **Ultra-Low Latency**: Enables critical applications like autonomous driving and remote surgery
- **Network Slicing**: Allows multiple logical networks on shared infrastructure with guaranteed SLAs
- **Edge Computing**: Reduces round-trip time by processing data at the network edge

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
  - Network topology configuration (YAML/TOML)
  - Slice templates with QoS parameters (latency, bandwidth, reliability)
  - UE (User Equipment) subscription profiles
  - MEC application container images
* **Entry Conditions**:
  - Kubernetes cluster with CNI plugin (Calico/Cilium) deployed
  - Container registry accessible from edge nodes
  - Network time synchronization (PTP/IEEE 1588) configured
  - Sufficient hardware resources (CPU with DPDK support, FPGA for acceleration)
* **Outputs**:
  - Deployed 5G core NFs as Kubernetes pods/services
  - Network slice configurations with associated QoS policies
  - MEC application manifests and deployment artifacts
  - Monitoring dashboards for slice performance metrics
* **Artifacts Required (Deliverables)**:
  - Helm charts for 5G core deployment
  - Network slice configuration files
  - MEC application manifests (Kubernetes CRDs)
  - API documentation for slice management
* **Acceptance Evidence**:
  - Successful UE registration and PDU session establishment
  - Slice isolation verification (traffic segregation, resource allocation)
  - End-to-end latency measurements meeting slice SLA
  - MEC application functional tests
* **Success Criteria**:
  - End-to-end latency < 1ms for URLLC slices
  - Slice provisioning time < 30 seconds
  - 99.999% availability for critical slices
  - Network slice throughput meets defined bandwidth guarantees

## Skill Composition
* **Depends on**: [kubernetes-platform](../../62-scale-operations/kubernetes-platform/SKILL.md), [observability-packaging](../../69-platform-engineering-lite/observability-packaging/SKILL.md)
* **Compatible with**: [edge-cloud-sync](../../75-edge-computing/edge-cloud-sync/SKILL.md), [lightweight-kubernetes](../../75-edge-computing/lightweight-kubernetes/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [sdn-nfv-orchestration](../../92-software-defined-networking-sdn-nfv/sdn-nfv-orchestration/SKILL.md)

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

