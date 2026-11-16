---
id: SKL-jest-JESTPATTERNS
name: Jest Patterns
description: Jest is a JavaScript testing framework that focuses on simplicity. This
  skill covers Jest setup, test structure, mocking, async testing, snapshot testing,
  coverage, React component testing, API testin
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

# Jest Patterns

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Jest is a JavaScript testing framework that focuses on simplicity. This skill covers Jest setup, test structure, mocking, async testing, snapshot testing, coverage, React component testing, API testing, and best practices.

## Why This Matters
Jest is the most popular testing framework for JavaScript/TypeScript projects, providing:
- Zero configuration setup for most use cases
- Built-in mocking, assertions, and coverage
- Fast parallel test execution
- Snapshot testing for UI components
- Excellent React integration through React Testing Library

## Core Concepts
1. **Test Structure**: Organized using `describe`, `it`, and `test` blocks
2. **Matchers**: Built-in assertion methods for various data types
3. **Mocking**: Isolate code under test from external dependencies
4. **Async Testing**: Handle promises, async/await, and callbacks
5. **Snapshot Testing**: Capture and compare component output
6. **Setup/Teardown**: `beforeEach`, `afterEach`, `beforeAll`, `afterAll`
7. **Coverage**: Measure test coverage with configurable thresholds

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
- Project uses npm or yarn for package management
- TypeScript is configured for type checking
- React Testing Library is used for React component testing

## Compatibility
- Node.js 16+ (LTS recommended)
- Works with JavaScript and TypeScript
- Compatible with React, Vue, Angular, and vanilla JS

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
1. Always run tests before committing
2. Update snapshots intentionally (use `jest -u` sparingly)
3. Keep test files organized alongside source files
4. Use appropriate matchers for each assertion

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Testing Implementation Details**
   ```typescript
   // Bad
   it('should set internal state', () => {
     component.setState({ count: 1 });
     expect(component.state.count).toBe(1);
   });

   // Good
   it('should increment counter', () => {
     render(<Counter />);
     fireEvent.click(screen.getByRole('button'));
     expect(screen.getByText('Count: 1')).toBeInTheDocument();
   });
   ```

2. **Testing Multiple Things in One Test**
   ```typescript
   // Bad
   it('should handle user operations', () => {
     const user = userService.create({ name: 'John' });
     expect(user.id).toBeDefined();
     const updated = userService.update(user.id, { name: 'Jane' });
     expect(updated.name).toBe('Jane');
   });

   // Good
   it('should create user', () => {
     const user = userService.create({ name: 'John' });
     expect(user.id).toBeDefined();
   });

   it('should update user', () => {
     const user = userService.create({ name: 'John' });
     const updated = userService.update(user.id, { name: 'Jane' });
     expect(updated.name).toBe('Jane');
   });
   ```

3. **Over-mocking**
   ```typescript
   // Bad - mocking everything
   jest.mock('./utils');
   jest.mock('./constants');
   jest.mock('./helpers');

   // Good - mock only external dependencies
   jest.mock('./api');
   ```

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

