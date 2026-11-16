---
id: SKL-cognitive-COGNITIVEGOVERNANCE
name: Cognitive Governance
description: Cognitive Governance is the God-Mode protocol that implements deep, unblockable
  safety controls for autonomous AI systems. Inspired by Asimov's Laws of Robotics,
  this protocol goes beyond simple rule-
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

# Cognitive Governance

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Cognitive Governance is the God-Mode protocol that implements deep, unblockable safety controls for autonomous AI systems. Inspired by Asimov's Laws of Robotics, this protocol goes beyond simple rule-based restrictions by analyzing semantic intent, detecting hidden agendas, and enforcing blast-radius containment. The system operates as an independent governance layer that can override any agent action, terminate dangerous operations, and enforce alignment with human values. This is the critical safety mechanism that makes powerful AI systems trustworthy and controllable.

## Why This Matters
- **Unblockable Safety**: Cannot be overridden or bypassed by any agent
- **Semantic Intent Detection**: Catches hidden agendas and subtle violations
- **Blast-Radius Containment**: Limits damage from any single agent action
- **Human-in-the-Loop**: Critical decisions require human approval
- **Trust Foundation**: Makes powerful AI systems safe for enterprise use

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
  - Agent action plans and requests
  - Current system state and resource inventory
  - Safety policies and governance rules
  - Human approval status and thresholds
  - Historical action patterns and threat intelligence
* **Entry Conditions**:
  - LLM with semantic analysis capabilities is available
  - Policy engine is configured with safety rules
  - Monitoring and audit logging are operational
  - Kill-switch mechanism is functional and tested
* **Outputs**:
  - Governance decision (approve, deny, require approval, modify)
  - Blast-radius limits and containment parameters
  - Audit records for all actions
  - Safety violation alerts and reports
  - Human approval requests when required
* **Artifacts Required (Deliverables)**:
  - Governance policy configuration
  - Intent analysis results
  - Blast-radius containment rules
  - Audit trail records
  - Safety violation reports
* **Acceptance Evidence**:
  - All actions pass governance validation
  - No unsafe actions are executed
  - Blast-radius is properly contained
  - Audit trail is complete and immutable
  - Human approval workflow is functional
* **Success Criteria**:
  - False positive rate: <5% (legitimate actions incorrectly blocked)
  - False negative rate: 0% (unsafe actions must never be approved)
  - Response time: <100ms for governance decisions
  - Audit completeness: 100% of actions logged
  - Kill-switch reliability: 100% (must always work)

## Skill Composition
* **Depends on**: None - this is the foundational safety layer
* **Compatible with**: All God-Mode protocols and meta-skills
* **Conflicts with**: None - this is mandatory for all autonomous operations
* **Related Skills**: [`security-baseline-controls`](64-meta-standards/security-baseline-controls/SKILL.md), [`logging-metrics-tracing-standard`](64-meta-standards/logging-metrics-tracing-standard/SKILL.md)

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

