---
id: SKL-algorithmic-ALGORITHMICSELFDISCOVERY
name: Algorithmic Self Discovery
description: Algorithmic Self-Discovery is the God-Mode protocol that enables AI agents
  to autonomously invent, create, and deploy their own MCP (Model Context Protocol)
  tools when existing tools are insufficient.
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

# Algorithmic Self Discovery

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Algorithmic Self-Discovery is the God-Mode protocol that enables AI agents to autonomously invent, create, and deploy their own MCP (Model Context Protocol) tools when existing tools are insufficient. This protocol eliminates the "tool ceiling" by allowing the agent to analyze problems, discover missing capabilities, write new tools from scratch, package them as MCP servers, and integrate them into the CerebraSkills knowledge base permanently. The agent becomes a true tool inventor rather than just a tool user.

## Why This Matters
- **Unbounded Capability**: AI never encounters a dead-end - if no tool exists, it creates one
- **Knowledge Accumulation**: Each invented tool becomes permanent capability for future tasks
- **Autonomous Evolution**: System grows its own capabilities without human intervention
- **Domain Adaptation**: Can create specialized tools for any domain it encounters
- **Meta-Learning**: Learns how to learn by discovering patterns in tool creation

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
  - Task description requiring tool invention
  - Existing MCP tool inventory
  - External API documentation or target system specifications
  - Security constraints and approval requirements
  - Performance requirements and resource limits
* **Entry Conditions**:
  - LLM with code generation capabilities is available
  - MCP server framework is configured
  - Code review and security scanning tools are deployed
  - CerebraSkills knowledge base is accessible for tool registration
* **Outputs**:
  - Complete MCP tool implementation
  - Tool documentation and usage examples
  - Test suite with coverage reports
  - Security scan results
  - Registration confirmation in CerebraSkills
* **Artifacts Required (Deliverables)**:
  - MCP tool source code
  - Tool specification (OpenAPI/MCP schema)
  - Unit and integration tests
  - Documentation (README, API docs)
  - Security audit report
* **Acceptance Evidence**:
  - Tool executes successfully in sandbox environment
  - All tests pass with ≥80% coverage
  - Security scan shows no critical vulnerabilities
  - Tool is discoverable via skill router
  - Documentation is complete and accurate
* **Success Criteria**:
  - Tool invention success rate: ≥90%
  - Tool execution reliability: ≥99%
  - Security approval rate: 100% (no unsafe tools deployed)
  - Tool reuse rate: ≥50% (invented tools used in future tasks)

## Skill Composition
* **Depends on**: [`cognitive-governance`](000-GOD-MODE-PROTOCOL/cognitive-governance/SKILL.md), [`liquid-architecture`](000-GOD-MODE-PROTOCOL/liquid-architecture/SKILL.md)
* **Compatible with**: [`skill-generator`](00-meta-skills/skill-generator/SKILL.md), [`self-validation-cicd`](00-meta-skills/self-validation-cicd/SKILL.md)
* **Conflicts with**: None - this is a foundational capability
* **Related Skills**: [`code-generation`](01-foundations/code-generation/SKILL.md), [`api-integration`](03-backend-api/api-integration/SKILL.md)

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

