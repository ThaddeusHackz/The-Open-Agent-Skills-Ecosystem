---
id: SKL-intelligence-INTELLIGENCEROUTER
name: Intelligence Router
description: The Intelligence Router implements the "Twin-Engine" Intelligence Architecture
  that governs how skills are routed, composed, and validated within the CerebraSkills
  ecosystem. Layer A provides determin
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

# Intelligence Router

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
The Intelligence Router implements the "Twin-Engine" Intelligence Architecture that governs how skills are routed, composed, and validated within the CerebraSkills ecosystem. Layer A provides deterministic, predictable routing through metadata validation and rule-based matching, while Layer B enhances with AI-assisted semantic search, intent mapping, and quality improvement suggestions. This dual approach ensures reliability while enabling intelligent, context-aware skill discovery.

## Why This Matters
- **Predictability**: Layer A ensures deterministic routing for high-impact operations, preventing hallucinations and ensuring consistent behavior
- **Flexibility**: Layer B provides AI-assisted semantic understanding for fuzzy requests, natural language queries, and multilingual support
- **Scalability**: Skill Packs enable efficient composition of multiple skills for common workflows
- **Quality**: Built-in validation and telemetry ensure the skill ecosystem remains healthy and conflict-free

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
  - User request (natural language or structured)
  - Current skill catalog with metadata
  - Relationship graph from all SKILL.md files
  - Synonym map for semantic expansion
  - Embedding index for semantic search
* **Entry Conditions**:
  - Skill catalog is indexed and searchable
  - Relationship graph is built and validated
  - Embedding index is populated (for Layer B)
  - Metadata vocabulary is defined
* **Outputs**:
  - Selected skill(s) with execution order
  - Dependency resolution results
  - Conflict warnings and resolutions
  - Routing decision rationale
* **Artifacts Required (Deliverables)**:
  - Routing table (deterministic rules)
  - Skill pack definitions
  - Telemetry data (usage statistics)
  - Validation reports
* **Acceptance Evidence**:
  - Routing decisions are deterministic for Layer A
  - Semantic search returns relevant skills for Layer B
  - Conflicts are detected and resolved
  - Telemetry shows skill usage patterns
* **Success Criteria**:
  - Deterministic routing accuracy: ≥95%
  - Semantic search relevance: ≥80% (user satisfaction)
  - Conflict detection: 100%
  - Routing latency: <500ms for deterministic, <2s for semantic

## Skill Composition
* **Depends on**: [`skill-generator`](00-meta-skills/skill-generator/SKILL.md)
* **Compatible with**: All skills (this routes them)
* **Conflicts with**: None
* **Related Skills**: [`skill-router`](00-meta-skills/skill-router/SKILL.md), [`swarm-collaboration`](00-meta-skills/swarm-collaboration/SKILL.md)

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

