---
id: SKL-bulkhead-BULKHEADPATTERNS
name: Bulkhead Patterns
description: 'The Bulkhead pattern is a resilience design pattern that isolates resources
  to prevent failures in one part of a system from cascading to other parts. Named
  after the watertight compartments in ships '
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

# Bulkhead Patterns

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
The Bulkhead pattern is a resilience design pattern that isolates resources to prevent failures in one part of a system from cascading to other parts. Named after the watertight compartments in ships that prevent the entire vessel from sinking if one compartment is breached.

**Core Principle**: "Isolate critical resources so that failure in one area doesn't sink the entire system."

## Why This Matters
- **Failure Containment**: Prevents cascading failures by limiting blast radius
- **Resource Guarantees**: Each component gets dedicated resources, ensuring predictable performance
- **Graceful Degradation**: System continues operating with reduced capacity when one component fails
- **Improved Observability**: Isolated pools make it easier to monitor and debug specific workloads

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
  - Service/workload definitions and priority levels
  - Resource requirements (threads, connections, memory)
  - Traffic patterns and expected load
* **Entry Conditions**:
  - Service architecture defined with clear component boundaries
  - Resource pools configured based on workload analysis
* **Outputs**:
  - Isolated resource pools with monitoring
  - Bulkhead configuration documentation
* **Artifacts Required (Deliverables)**:
  - Bulkhead implementation code
  - Pool sizing calculations and rationale
  - Monitoring dashboards for pool utilization
* **Acceptance Evidence**:
  - Load test results showing isolation effectiveness
  - Monitoring screenshots showing pool behavior
  - Failure injection test results
* **Success Criteria**:
  - Failure in one pool does not affect other pools
  - Pool utilization within 70-90% target range
  - P95 latency for critical workloads meets SLA under normal conditions

## Skill Composition
* **Depends on**: Failure Modes Analysis (40-system-resilience/failure-modes)
* **Compatible with**: Circuit Breaker, Graceful Degradation, Retry Strategies
* **Conflicts with**: Shared resource pool architectures (without isolation)
* **Related Skills**: 
  - [40-system-resilience/failure-modes](40-system-resilience/failure-modes/SKILL.md)
  - [40-system-resilience/graceful-degradation](40-system-resilience/graceful-degradation/SKILL.md)
  - [40-system-resilience/retry-timeout-strategies](40-system-resilience/retry-timeout-strategies/SKILL.md)

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

