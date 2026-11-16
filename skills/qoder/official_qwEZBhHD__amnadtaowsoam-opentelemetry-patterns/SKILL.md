---
id: SKL-opentelemetry-OPENTELEMETRYPATTERNS
name: Opentelemetry Patterns
description: 'OpenTelemetry (OTel) is a vendor-neutral observability framework for
  collecting and exporting telemetry data (traces, metrics, and logs). It''s a CNCF
  project that has become the industry standard for '
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

# Opentelemetry Patterns

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
OpenTelemetry (OTel) is a vendor-neutral observability framework for collecting and exporting telemetry data (traces, metrics, and logs). It's a CNCF project that has become the industry standard for distributed tracing and observability. This skill covers SDK setup, manual instrumentation, custom metrics, context propagation, baggage, and production patterns.

## Why This Matters
- **Vendor Neutral**: Switch backends (Jaeger, Zipkin, Datadog, Tempo) without code changes
- **Unified Standard**: Single SDK for traces, metrics, and logs reduces complexity
- **Auto-instrumentation**: Automatic tracing for popular frameworks (Express, Fastify, NestJS) with minimal code
- **Context Propagation**: Trace requests across service boundaries automatically with distributed context

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
  - OpenTelemetry SDK packages
  - Application code for instrumentation
  - Collector endpoint URL
  - Service name and version for resource attributes
  - Environment variables for configuration

* **Entry Conditions**:
  - Application codebase structured for instrumentation
  - Collector deployed and accessible
  - Backend (Jaeger, Tempo, Prometheus) configured
  - Network connectivity between services and collector

* **Outputs**:
  - Instrumented application with telemetry collection
  - Spans with attributes and events
  - Metrics with appropriate labels
  - Context propagation across service boundaries
  - Collector configuration for processing and export

* **Artifacts Required (Deliverables)**:
  - OpenTelemetry SDK initialization code
  - Manual instrumentation code for custom spans and metrics
  - Collector configuration file
  - Environment variable documentation
  - Dashboard configurations for metrics visualization

* **Acceptance Evidence**:
  - Screenshot of trace in Jaeger/Tempo showing distributed transaction
  - Screenshot of metrics in Prometheus/Grafana
  - Screenshot of collector metrics showing successful export
  - Test showing context propagation across services

* **Success Criteria**:
  - Traces appear in backend within 5 seconds of completion
  - Metrics are scraped and available in Prometheus
  - Context propagates correctly across service boundaries
  - Sampling rate is appropriate for production load

## Skill Composition
* **Depends on**: [distributed-tracing](./distributed-tracing/SKILL.md), [prometheus-metrics](./prometheus-metrics/SKILL.md), [performance-monitoring](./performance-monitoring/SKILL.md)
* **Compatible with**: [error-tracking](./error-tracking/SKILL.md), [elk-stack](./elk-stack/SKILL.md), [grafana-dashboards](./grafana-dashboards/SKILL.md)
* **Conflicts with**: Vendor-specific SDKs (Datadog SDK, New Relic SDK) - use OpenTelemetry instead
* **Related Skills**: [logging-standards](../../64-meta-standards/logging-metrics-tracing-standard/SKILL.md), [api-design-contracts](../../71-infrastructure-patterns/api-design-contracts/SKILL.md)

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

