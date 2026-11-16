---
id: SKL-test-TESTDATAFACTORY
name: Test Data Factory
description: Test data factories provide a clean, reusable way to create test data.
  This skill covers factory patterns, libraries (Factory Boy for Python, Fishery for
  TypeScript), fixture factories, Faker integrat
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

# Test Data Factory

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Test data factories provide a clean, reusable way to create test data. This skill covers factory patterns, libraries (Factory Boy for Python, Fishery for TypeScript), fixture factories, Faker integration, database seeding, realistic test data, data relationships, performance considerations, and reusability.

## Why This Matters
Test data factories provide:
- **Consistency**: Reproducible test data across test runs
- **Maintainability**: Centralized test data management
- **Realism**: Faker generates realistic test data
- **Flexibility**: Easy to override defaults for specific tests
- **Performance**: Efficient batch creation of test data
- **Clean Tests**: Reduced duplication in test code

## Core Concepts
1. **Factory Pattern**: Create objects with default values and overrides
2. **Sequence**: Auto-incrementing values for uniqueness
3. **SubFactory**: Handle related objects automatically
4. **LazyAttribute**: Compute values based on other attributes
5. **Fixture Integration**: Use factories with test frameworks
6. **Faker Integration**: Generate realistic test data
7. **Database Seeding**: Efficiently populate test databases

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
- Test models are defined and accessible
- Database connection is available for persistence
- Faker is installed for realistic data generation

## Compatibility
- **Python**: 3.8+
- **TypeScript**: 4.5+
- **Factory Boy**: 3.2+
- **Fishery**: 2.0+
- **Faker**: 15.0+ (Python), 7.0+ (TypeScript)

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
1. Always use factories for test data
2. Use Faker for realistic data
3. Clean up test data after tests
4. Use batch operations for performance
5. Handle data relationships properly
6. Keep factories simple and focused

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Hardcoded Test Data**
   ```python
   # Bad
   def test_create_user():
       user = {
           'id': 1,
           'name': 'Test User',
           'email': 'test@example.com',
       }
       assert user['id'] is not None

   # Good
   def test_create_user():
       user = UserFactory.create()
       assert user['id'] is not None
   ```

2. **No Cleanup**
   ```python
   # Bad
   @pytest.fixture
   def user():
       return UserFactory.create()

   # Good
   @pytest.fixture
   def user():
       user = UserFactory.create()
       yield user
       UserFactory.delete(user['id'])
   ```

3. **Complex Factories**
   ```python
   # Bad: Complex factory with logic
   class UserFactory(BaseFactory):
       @classmethod
       def create(cls, **kwargs):
           if 'email' not in kwargs:
               kwargs['email'] = f'user{cls._counter}@example.com'
           # More complex logic
           return {**defaults, **kwargs}

   # Good: Simple factory
   class UserFactory(BaseFactory):
       @classmethod
       def create(cls, **kwargs):
           defaults = {'email': 'test@example.com'}
           defaults.update(kwargs)
           return defaults
   ```

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

