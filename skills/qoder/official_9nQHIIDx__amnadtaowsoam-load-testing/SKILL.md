---
id: SKL-load-LOADTESTING
name: Load Testing
description: Load testing evaluates system performance under expected and peak load
  conditions. This skill covers load testing concepts, tools (k6, Artillery, Locust,
  JMeter), test scenarios, metrics, ramp-up stra
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

# Load Testing

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Load testing evaluates system performance under expected and peak load conditions. This skill covers load testing concepts, tools (k6, Artillery, Locust, JMeter), test scenarios, metrics, ramp-up strategies, bottleneck identification, CI/CD integration, production testing, and best practices.

## Why This Matters
Load testing ensures:
- **System Reliability**: Prevents production failures under load
- **Performance SLAs**: Validates response time and throughput requirements
- **Capacity Planning**: Determines infrastructure needs for growth
- **Cost Optimization**: Identifies over-provisioned resources
- **User Experience**: Ensures acceptable performance during peak traffic

## Core Concepts
1. **Virtual Users (VUs)**: Simulated concurrent users
2. **Requests Per Second (RPS)**: Request rate measurement
3. **Throughput**: Successful requests per time unit
4. **Response Time**: Time to receive complete response
5. **Latency**: Network delay component of response time
6. **Error Rate**: Percentage of failed requests
7. **Percentiles**: p95, p99 response time measurements

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
- Test environment mirrors production configuration
- Sufficient test data is available
- Network connectivity between test runner and target
- Monitoring tools are configured on target system

## Compatibility
- **k6**: Cross-platform (Linux, macOS, Windows)
- **Artillery**: Node.js based, cross-platform
- **Locust**: Python based, cross-platform
- **JMeter**: Java based, cross-platform

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


## Agent Directives
1. Always start with smoke tests
2. Gradually increase load in stages
3. Monitor system resources during tests
4. Stop tests immediately if production is affected
5. Document all findings and recommendations

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Testing in Production Without Safeguards**
   ```javascript
   // Bad: Direct production testing
   export default function () {
     http.get('https://production.example.com/api');
   }

   // Good: Use canary deployment
   export default function () {
     http.get('https://canary.example.com/api');
   }
   ```

2. **Unrealistic Test Scenarios**
   ```javascript
   // Bad: Unrelated requests
   export default function () {
     http.get('/users');
     http.get('/products');
     http.get('/orders');
   }

   // Good: Realistic user flow
   export default function () {
     group('User Flow', () => {
       const res = http.get('/users');
       const userId = res.json()[0].id;
       http.get(`/users/${userId}`);
     });
   }
   ```

3. **No Thresholds Defined**
   ```javascript
   // Bad: No thresholds
   export const options = {
     stages: [{ duration: '5m', target: 100 }],
   };

   // Good: Clear thresholds
   export const options = {
     stages: [{ duration: '5m', target: 100 }],
     thresholds: {
       http_req_duration: ['p(95)<500'],
       http_req_failed: ['rate<0.01'],
     },
   };
   ```

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

