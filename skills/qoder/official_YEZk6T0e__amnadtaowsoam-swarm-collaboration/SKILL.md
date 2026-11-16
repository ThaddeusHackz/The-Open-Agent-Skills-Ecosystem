---
id: SKL-swarm-SWARMCOLLABORATION
name: Swarm Collaboration
description: Swarm Collaboration enables multiple AI agents with different personas
  to work together on complex tasks. Each agent has specialized expertise (Architect,
  Coder, Reviewer/Security) and they collaborat
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

# Swarm Collaboration

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Swarm Collaboration enables multiple AI agents with different personas to work together on complex tasks. Each agent has specialized expertise (Architect, Coder, Reviewer/Security) and they collaborate through a shared context and message queue. The swarm system enables parallel execution, cross-agent communication, and coordinated problem-solving that exceeds the capabilities of any single agent.

## Why This Matters
- **Specialized Expertise**: Each agent focuses on their domain, leading to better quality
- **Parallel Processing**: Multiple agents can work simultaneously, reducing total execution time
- **Cross-Validation**: Agents review each other's work, catching errors early
- **Scalability**: Swarm can scale to handle larger, more complex tasks
- **Resilience**: If one agent fails, others can continue or retry

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
  - User task or problem description
  - Task complexity and requirements
  - Available agent personas
  - Shared context workspace
  - Message queue for agent communication
* **Entry Conditions**:
  - All agent personas are defined and available
  - Shared context workspace is initialized
  - Message queue is running
  - Task decomposition rules are defined
* **Outputs**:
  - Decomposed task plan with agent assignments
  - Individual agent outputs
  - Aggregated final result
  - Execution logs and agent communications
* **Artifacts Required (Deliverables)**:
  - Task decomposition plan
  - Agent execution logs
  - Final aggregated result
  - Cross-agent review comments
* **Acceptance Evidence**:
  - Task is decomposed appropriately for multiple agents
  - Each agent completes their assigned subtask
  - Results are aggregated correctly
  - Cross-agent communication is logged
* **Success Criteria**:
  - Task decomposition accuracy: ≥90%
  - Agent success rate: ≥95%
  - Cross-agent communication: 100%
  - Total execution time: <3x single-agent baseline

## Skill Composition
* **Depends on**: [`skill-router`](00-meta-skills/skill-router/SKILL.md), [`intelligence-router`](00-meta-skills/intelligence-router/SKILL.md)
* **Compatible with**: [`self-validation-cicd`](00-meta-skills/self-validation-cicd/SKILL.md), [`skill-generator`](00-meta-skills/skill-generator/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [`system-thinking`](00-meta-skills/system-thinking/SKILL.md), [`architectural-reviews`](00-meta-skills/architectural-reviews/SKILL.md), [`code-review`](01-foundations/code-review/SKILL.md)

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

