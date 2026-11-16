---
id: SKL-test-TESTDRIVENDEVELOPMENTAGENTIC
name: Test Driven Development Agentic
description: "Test-Driven Development (TDD) for AI agents is a disciplined approach\
  \ where tests are written before implementation. For AI agents, tests serve as both\
  \ specification and verification\u2014they define what "
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

# Test Driven Development Agentic

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Test-Driven Development (TDD) for AI agents is a disciplined approach where tests are written before implementation. For AI agents, tests serve as both specification and verification—they define what the agent should produce and ensure the implementation meets those requirements. This skill teaches the Red-Green-Refactor cycle adapted for agentic development.

## Why This Matters
TDD for agents ensures:
- **Tests as Specs**: Tests define clear expectations for AI
- **Prevents Hallucinations**: Tests constrain what AI can produce
- **Improves First-Shot Success**: Clear expectations reduce iterations
- **Enables Safe Refactoring**: Tests catch regressions
- **Documents Behavior**: Tests serve as living documentation

## Core Concepts
1. **Red Phase**: Write a failing test that defines desired behavior
2. **Green Phase**: Write minimum code to make test pass
3. **Refactor Phase**: Improve code without changing behavior
4. **AAA Pattern**: Arrange, Act, Assert structure
5. **Test-First**: Write tests before implementation
6. **Specification**: Tests serve as living documentation
7. **Regression Prevention**: Tests catch unintended changes

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
- Test framework is configured (Jest, pytest, etc.)
- Development environment supports test execution
- Requirements are clear enough to write tests

## Compatibility
- **JavaScript**: Jest, Mocha, Jasmine
- **TypeScript**: Jest, Vitest
- **Python**: pytest, unittest

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
1. Always write tests first
2. Make tests fail before implementing
3. Write minimum code to pass
4. Refactor only when tests pass
5. Keep tests independent
6. Never change tests to match code

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Writing Tests After Code**
   ```javascript
   // Bad: Implementation first
   function calculateTotal(order) {
     return order.subtotal + order.tax - order.discount;
   }
   
   // Then test
   it('should calculate total', () => {
     // ...
   });

   // Good: Test first
   it('should calculate total', () => {
     expect(calculateTotal(order)).toBe(100);
   });
   
   function calculateTotal(order) {
     return order.subtotal + order.tax - order.discount;
   }
   ```

2. **Writing Too Many Tests at Once**
   ```javascript
   // Bad: Multiple tests before implementation
   it('should calculate total', () => { /* ... */ });
   it('should handle discount', () => { /* ... */ });
   it('should validate input', () => { /* ... */ });
   
   // Good: One test at a time
   it('should calculate total', () => { /* ... */ });
   // Implement, then next test
   ```

3. **Skipping Refactor Phase**
   ```javascript
   // Bad: No refactoring
   function process(data) {
     // Complex, messy code
     if (data.type === 'A') { /* ... */ }
     else if (data.type === 'B') { /* ... */ }
     // ...
   }

   // Good: Refactored
   function process(data) {
     const handler = getHandler(data.type);
     return handler(data);
   }
   ```

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

