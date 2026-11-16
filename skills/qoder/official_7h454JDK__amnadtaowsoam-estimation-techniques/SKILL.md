---
id: SKL-estimation-ESTIMATIONTECHNIQUES
name: Estimation Techniques
description: Software estimation is the process of predicting the effort, time, and
  resources required to complete a project. This skill covers multiple estimation
  approaches including story points, T-shirt sizing
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

# Estimation Techniques

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Software estimation is the process of predicting the effort, time, and resources required to complete a project. This skill covers multiple estimation approaches including story points, T-shirt sizing, planning poker, three-point estimation (PERT), bottom-up vs top-down methods, velocity calculation, cone of uncertainty, buffer management, and bias mitigation strategies for accurate project planning.

## Why This Matters
- **Better Planning**: Accurate estimates enable realistic timelines and resource allocation
- **Stakeholder Trust**: Transparent estimation builds credibility with stakeholders
- **Team Buy-in**: Collaborative estimation creates team commitment to delivery
- **Risk Management**: Proper buffers and uncertainty ranges account for risks
- **Continuous Improvement**: Tracking estimates vs actuals improves accuracy over time

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
  - User stories or requirements
  - Historical velocity data
  - Similar past project data
  - Team availability and capacity
* **Entry Conditions**:
  - Requirements are understood (at least at high level)
  - Team is available for estimation session
  - Estimation tool is configured (Jira, PlanningPoker, etc.)
  - Historical data is accessible (for velocity-based estimation)
* **Outputs**:
  - Story point estimates for each user story
  - Total project estimate with confidence ranges
  - Velocity calculation and planning capacity
  - Buffer allocation for risk management
* **Artifacts Required (Deliverables)**:
  - Estimated backlog with story points
  - Velocity tracking spreadsheet
  - Estimation meeting notes
  - Risk assessment and buffer allocation
* **Acceptance Evidence**:
  - Team consensus on estimates documented
  - Velocity chart showing stable trend
  - Historical comparison completed
  - Stakeholder sign-off on estimates
* **Success Criteria**:
  - Estimation accuracy within ±20% of actual
  - Team velocity stable (±10% over 3 sprints)
  - Stakeholder satisfaction with communication
  - Estimation process completed within timebox

## Skill Composition
* **Depends on**: [agile-scrum](../18-project-management/agile-scrum/SKILL.md), [user-stories](../18-project-management/user-stories/SKILL.md)
* **Compatible with**: [project-planning](../18-project-management/project-planning/SKILL.md), [risk-management](../18-project-management/risk-management/SKILL.md)
* **Conflicts with**: Fixed-price contracts without buffer, rigid deadlines
* **Related Skills**: [requirement-analysis](../18-project-management/requirement-analysis/SKILL.md), [technical-specifications](../18-project-management/technical-specifications/SKILL.md)

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

