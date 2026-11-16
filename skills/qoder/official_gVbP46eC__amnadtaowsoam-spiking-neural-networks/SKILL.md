---
id: SKL-spiking-SPIKINGNEURALNETWORKS
name: Spiking Neural Networks
description: This skill covers the implementation of neuromorphic computing systems
  using Spiking Neural Networks (SNNs) that mimic the brain's event-driven processing.
  It enables building ultra-low power AI syste
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

# Spiking Neural Networks

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
This skill covers the implementation of neuromorphic computing systems using Spiking Neural Networks (SNNs) that mimic the brain's event-driven processing. It enables building ultra-low power AI systems for edge devices, real-time sensor processing, and applications requiring minimal energy consumption.

## Why This Matters
- **Ultra-Low Power**: Orders of magnitude lower power consumption than traditional neural networks
- **Event-Driven Processing**: Only processes when events occur, ideal for sparse data
- **Real-Time Performance**: Sub-millisecond latency for time-critical applications

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
  - Event-based sensor data (spike trains, DVS events)
  - Traditional data converted to spike trains
  - Network architecture and neuron parameters
  - Learning rules and hyperparameters
* **Entry Conditions**:
  - Neuromorphic SDK installed (Loihi SDK, SpiNNaker, Nengo)
  - Neuromorphic hardware available (or simulation environment)
  - Event-based sensor data or conversion pipeline
  - Python 3.9+ with required libraries
* **Outputs**:
  - Trained SNN model
  - Spike train visualizations and analysis
  - Power consumption metrics
  - Inference results with timing information
* **Artifacts Required (Deliverables)**:
  - SNN architecture definition
  - Training scripts and conversion utilities
  - Deployment configuration for neuromorphic hardware
  - Performance and power analysis reports
* **Acceptance Evidence**:
  - Model achieves target accuracy on test data
  - Power consumption meets requirements (<10mW for edge)
  - Inference latency < 1ms for time-critical tasks
  - Successful deployment on neuromorphic hardware
* **Success Criteria**:
  - Accuracy within 10% of equivalent ANN baseline
  - Power consumption < 10% of equivalent ANN
  - Inference latency < 1ms for real-time applications
  - Energy efficiency > 1000 TOPS/W

## Skill Composition
* **Depends on**: [high-performance-inference](../../78-inference-model-serving/high-performance-inference/SKILL.md), [model-registry-versioning](../../77-mlops-data-engineering/model-registry-versioning/SKILL.md)
* **Compatible with**: [edge-cloud-sync](../../75-edge-computing/edge-cloud-sync/SKILL.md), [lightweight-kubernetes](../../75-edge-computing/lightweight-kubernetes/SKILL.md)
* **Conflicts with**: None
* **Related Skills**: [robotics-ros](../../95-embodied-ai-robotics/robotics-ros/SKILL.md)

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

