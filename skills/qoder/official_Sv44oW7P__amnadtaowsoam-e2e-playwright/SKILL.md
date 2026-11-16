---
id: SKL-e2e-E2EPLAYWRIGHT
name: E2E Playwright
description: Playwright is a Node.js library to automate Chromium, Firefox, and WebKit
  with a single API. This skill covers Playwright setup, locators, actions, assertions,
  page object model, fixtures, parallel ex
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

# E2E Playwright

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Playwright is a Node.js library to automate Chromium, Firefox, and WebKit with a single API. This skill covers Playwright setup, locators, actions, assertions, page object model, fixtures, parallel execution, visual regression, and CI/CD integration for building robust end-to-end tests.

## Why This Matters
E2E testing with Playwright is critical because it:

- **Validates complete user journeys** from start to finish
- **Catches integration issues** that unit tests miss
- **Supports multiple browsers** for cross-browser testing
- **Provides fast, reliable** test execution
- **Enables parallel execution** for faster test runs
- **Supports visual regression** testing for UI consistency
- **Integrates with CI/CD** for automated testing

---

## Core Concepts
| Concept | Description |
|---------|-------------|
| **Page Object Model** | Reusable page classes for UI elements |
| **Locators** | Strategies for finding elements on page |
| **Actions** | User interactions (click, type, etc.) |
| **Assertions** | Verifying expected outcomes |
| **Fixtures** | Reusable test setup and teardown |
| **Parallel Execution** | Running tests concurrently |
| **Visual Regression** | Comparing screenshots for UI changes |

## Inputs / Outputs / Contracts
#

## Skill Composition
* **Depends on**: None
* **Compatible with**: None
* **Conflicts with**: None
* **Related Skills**: None

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


## Assumptions
- Application is web-based and accessible via browser
- Application has stable, predictable UI elements
- Test environment is accessible and configured
- Team has basic JavaScript/TypeScript knowledge
- CI/CD pipeline is available for automated testing

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


## Agent Directives
When writing E2E tests:

1. **Use Page Object Model** for maintainable tests
2. **Use descriptive test names** that explain what's being tested
3. **Use explicit waits** to avoid flaky tests
4. **Use fixtures** for reusable test setup
5. **Test across browsers** for cross-browser compatibility
6. **Use parallel execution** for faster test runs
7. **Add assertions** to verify expected outcomes

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Inline Locators**: Not using page object model
2. **Hardcoded Waits**: Using fixed timeouts instead of explicit waits
3. **Brittle Locators**: Using CSS selectors that break easily
4. **No Test Isolation**: Tests depending on each other
5. **Ignoring Flaky Tests**: Not investigating and fixing flaky tests
6. **Testing Production**: Running tests against production environment

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

