---
id: SKL-model-MODELINTERPRETABILITYALGORITHMICAUDITING
name: Model Interpretability Algorithmic Auditing
description: This skill covers the implementation of explainable AI techniques to
  make machine learning models transparent and interpretable. It includes local and
  global explanation methods (LIME, SHAP), algorith
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

# Model Interpretability Algorithmic Auditing

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
This skill covers the implementation of explainable AI techniques to make machine learning models transparent and interpretable. It includes local and global explanation methods (LIME, SHAP), algorithmic auditing for bias detection, fairness metrics, and compliance with AI regulations (EU AI Act, GDPR).

## Why This Matters
- **Regulatory Compliance**: Meets GDPR, EU AI Act, and other AI transparency requirements
- **Trust & Adoption**: Enables stakeholders to understand and trust AI decisions
- **Bias Detection**: Identifies and mitigates unfair biases in ML models

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
  - Trained ML model (any framework)
  - Dataset for explanation and auditing
  - Protected attributes for fairness analysis
  - Explanation configuration (method, parameters)
* **Entry Conditions**:
  - ML model trained and saved (pickle, ONNX, TensorFlow SavedModel)
  - Dataset available for explanation
  - SHAP, LIME, Alibi libraries installed
  - Python 3.9+ with required ML frameworks
* **Outputs**:
  - Local explanations for individual predictions
  - Global explanations for model behavior
  - Fairness audit reports with metrics
  - Bias detection results and recommendations
* **Artifacts Required (Deliverables)**:
  - Explanation configuration files
  - Audit report templates
  - Fairness metric calculations
  - Visualization dashboards
* **Acceptance Evidence**:
  - Explanations are consistent and stable across runs
  - Fairness metrics meet regulatory thresholds
  - Bias is detected and documented
  - Explanations are understandable to domain experts
* **Success Criteria**:
  - Explanation stability > 0.8 (consistency across runs)
  - Fairness metrics within acceptable range (e.g., disparate impact ratio > 0.8)
  - Explanation generation time < 1 second per prediction
  - Stakeholder satisfaction with explanation quality

## Skill Composition
* **Depends on**: [model-registry-versioning](../../77-mlops-data-engineering/model-registry-versioning/SKILL.md), [mlflow-patterns](../../77-mlops-data-engineering/mlflow-patterns/SKILL.md)
* **Compatible with**: [ai-evaluation](../../52-ai-evaluation/SKILL.md), [ai-governance](../../44-ai-governance/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [llm-security-redteaming](../../61-ai-production/llm-security-redteaming/SKILL.md)

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

