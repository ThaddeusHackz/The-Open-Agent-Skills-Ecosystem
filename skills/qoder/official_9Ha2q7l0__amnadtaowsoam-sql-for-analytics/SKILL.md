---
id: SKL-sql-SQLFORANALYTICS
name: Sql For Analytics
description: Analytics SQL focuses on aggregations, analysis, and insights rather
  than transactional operations. Effective analytics SQL uses window functions, CTEs,
  complex joins, and optimization techniques to q
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

# Sql For Analytics

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Analytics SQL focuses on aggregations, analysis, and insights rather than transactional operations. Effective analytics SQL uses window functions, CTEs, complex joins, and optimization techniques to query large datasets efficiently. This skill covers core analytics patterns, performance optimization, and database-specific features for PostgreSQL, MySQL, BigQuery, and Snowflake.

## Why This Matters
- **Data Insights**: SQL is the primary language for extracting business insights from data
- **Performance**: Well-optimized queries can reduce execution time from hours to seconds
- **Scalability**: Efficient queries scale better as data volumes grow
- **Reproducibility**: SQL queries provide a documented, reproducible way to analyze data
- **Foundation**: SQL skills are foundational for data engineering, analytics, and BI roles

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
  - Database schema (tables, columns, relationships)
  - Business requirements (KPIs, metrics, reports)
  - Data sources (events, orders, users, products)
  - Time periods (date ranges for analysis)
* **Entry Conditions**:
  - Database accessible with appropriate permissions
  - Schema documented and understood
  - Business requirements clearly defined
  - Sample data available for testing
* **Outputs**:
  - SQL queries for analytics
  - Query results (aggregated data)
  - Query execution plans
  - Performance metrics
* **Artifacts Required (Deliverables)**:
  - SQL query files with comments
  - Query documentation (purpose, logic, expected results)
  - Performance analysis (EXPLAIN output)
  - Test results with sample data
* **Acceptance Evidence**:
  - Queries return expected results
  - Query performance meets requirements (e.g., < 30s for 1M rows)
  - Queries are readable and maintainable
  - Queries handle edge cases (NULLs, empty results)
* **Success Criteria**:
  - Queries execute successfully
  - Results are accurate and validated
  - Performance is optimized (indexes, EXPLAIN analysis)
  - Queries are documented and version controlled

## Skill Composition
* **Depends on**: [kpi-metrics](file://23-business-analytics/kpi-metrics/), [retention-analytics](file://23-business-analytics/retention-analytics/), [data-visualization](file://23-business-analytics/data-visualization/)
* **Compatible with**: [cohort-analysis](file://23-business-analytics/cohort-analysis/), [funnel-analysis](file://23-business-analytics/funnel-analysis/), [business-intelligence](file://23-business-analytics/business-intelligence/)
* **Conflicts with**: None
* **Related Skills**: [database-optimization](file://04-database/database-optimization/), [dashboard-design](file://23-business-analytics/dashboard-design/)

---

## Quick Start
#

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


## Anti-patterns
#

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

