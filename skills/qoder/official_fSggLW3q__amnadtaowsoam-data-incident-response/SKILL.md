---
id: SKL-data-DATAINCIDENTRESPONSE
name: Data Incident Response
description: Data Incident Response is the process of detecting, triaging, and resolving
  issues related to data quality, availability, or integrity. Unlike application incidents,
  data incidents can have long-lasti
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

# Data Incident Response

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Data Incident Response is the process of detecting, triaging, and resolving issues related to data quality, availability, or integrity. Unlike application incidents, data incidents can have long-lasting impacts on analytics, ML models, and business decisions.

**Core Principle**: "Bad data is worse than no data. Detect fast, respond faster, prevent recurrence."

This skill provides comprehensive procedures and playbooks for handling data incidents including data loss, corruption, breaches, pipeline failures, schema breaking changes, quality degradation, and freshness violations.

## Why This Matters
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>
- **<Benefit>**: <short explanation>

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
  - <e.g., env vars, request payload, file paths, schema>
* **Entry Conditions**:
  - <Pre-requisites: e.g., Repo initialized, DB running, specific branch checked out>
* **Outputs**:
  - <e.g., artifacts (PR diff, docs, tests, dashboard JSON)>
* **Artifacts Required (Deliverables)**:
  - <e.g., Code Diff, Unit Tests, Migration Script, API Docs>
* **Acceptance Evidence**:
  - <e.g., Test Report (screenshot/log), Benchmark Result, Security Scan Report>
* **Success Criteria**:
  - <e.g., p95 < 300ms, coverage ≥ 80%>

## Skill Composition
* **Depends on**: None
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: None

## Quick Start
#

## Assumptions
- Automated monitoring is in place for critical data pipelines
- Backups are available and tested regularly
- Team has 24/7 on-call coverage for P0/P1 incidents
- Communication channels are established for incident response
- Access controls allow quick permission revocation

## Compatibility
- Works with any SQL database (PostgreSQL, MySQL, Snowflake, BigQuery)
- Compatible with all major data pipeline tools (Airflow, dbt, Prefect)
- Language-agnostic monitoring approach
- Adaptable to different team structures and sizes

## Test Scenario Matrix
| Scenario | Test Case | Expected Outcome |
|----------|-----------|------------------|
| Data Loss | DELETE without WHERE clause | Detect immediately, restore from backup |
| Data Corruption | ETL bug multiplies values | Identify affected rows, fix and reprocess |
| Pipeline Failure | DAG fails mid-execution | Alert triggered, downstream paused |
| Schema Drift | Column renamed upstream | Detect schema change, update pipeline |
| Quality Degradation | Increasing null rate | Alert when threshold exceeded |
| Freshness Violation | Data not updated in SLA | Alert when data is stale |

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


## Agent Directives
1. **Always prioritize stopping the bleeding** over investigation
2. **Communicate early** - don't wait for complete information
3. **Preserve evidence** - logs, corrupted data, timestamps
4. **Document everything** - timeline, decisions, actions
5. **Learn from every incident** - update prevention measures

## Definition of Done
A data incident is considered resolved when:

- [ ] Root cause identified and documented
- [ ] Data restored to correct state
- [ ] Downstream pipelines resumed and healthy
- [ ] Data quality checks passing
- [ ] Stakeholders notified of resolution
- [ ] Postmortem completed (if required by severity)
- [ ] Prevention measures implemented
- [ ] Playbooks updated with lessons learned
- [ ] Monitoring/alerting updated if needed
- [ ] Team debrief conducted

## Anti-patterns
1. **Silent failures**: Don't suppress errors without logging
2. **Quick fixes without root cause**: Always investigate and fix root cause
3. **Overwriting corrupted data**: Preserve corrupted data for analysis
4. **Ignoring prevention**: Every incident should improve defenses
5. **Blame culture**: Focus on process, not people

## Reference Links
#

## Versioning
This skill follows semantic versioning (MAJOR.MINOR.PATCH):
- **MAJOR**: Breaking changes to procedures or playbooks
- **MINOR**: New procedures or significant enhancements
- **PATCH**: Bug fixes or documentation updates
