---
id: SKL-ml-MLMODELTESTING
name: Ml Model Testing
description: ML model testing ensures machine learning models perform correctly and
  reliably. This skill covers model testing types (unit, integration, validation),
  training pipeline testing, inference testing, da
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

# Ml Model Testing

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
ML model testing ensures machine learning models perform correctly and reliably. This skill covers model testing types (unit, integration, validation), training pipeline testing, inference testing, data validation, performance tests, regression tests, A/B testing, shadow testing, and production monitoring.

## Why This Matters
ML model testing ensures:
- **Model Reliability**: Models perform as expected in production
- **Data Quality**: Input data meets expected quality standards
- **Performance Standards**: Models meet accuracy and latency requirements
- **Reproducibility**: Training pipelines produce consistent results
- **Fairness**: Models don't exhibit bias across groups
- **Drift Detection**: Early warning of performance degradation

## Core Concepts
1. **Unit Tests**: Test individual model components and functions
2. **Integration Tests**: Test complete training and inference pipelines
3. **Model Validation**: Evaluate model performance on test data
4. **Data Validation**: Ensure input data quality and consistency
5. **Performance Tests**: Measure accuracy, precision, recall, F1, AUC
6. **Regression Tests**: Detect performance degradation over time
7. **A/B Testing**: Compare model variants in production
8. **Shadow Testing**: Test new models alongside production without impact
9. **Monitoring**: Track model performance and data drift in production

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
- Test data is representative of production data
- Model artifacts can be loaded and used for inference
- Ground truth labels are available for test data
- Monitoring infrastructure is in place

## Compatibility
- **Python**: 3.8+
- **PyTorch**: 1.10+
- **TensorFlow**: 2.8+
- **scikit-learn**: 1.0+

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
1. Always validate data before training
2. Test on held-out test data only
3. Monitor for data and model drift
4. Test model robustness to edge cases
5. Evaluate fairness across protected groups
6. Use statistical significance for A/B tests

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Testing on Training Data**
   ```python
   # Bad: Testing on training data
   def test_model_accuracy():
       model = MyModel()
       model.load('model.h5')
       
       X_train, y_train = load_train_data()
       y_pred = model.predict(X_train)
       
       accuracy = calculate_accuracy(y_train, y_pred)
       assert accuracy >= 0.95  # Overfitted!

   # Good: Testing on test data
   def test_model_accuracy():
       model = MyModel()
       model.load('model.h5')
       
       X_test, y_test = load_test_data()
       y_pred = model.predict(X_test)
       
       accuracy = calculate_accuracy(y_test, y_pred)
       assert accuracy >= 0.85  # Realistic threshold
   ```

2. **Ignoring Data Quality**
   ```python
   # Bad: No data quality checks
   def test_model_predictions():
       model = MyModel()
       model.load('model.h5')
       
       X_test = load_test_data()[0]
       predictions = model.predict(X_test)
       
       assert predictions is not None

   # Good: Validate data quality
   def test_model_predictions():
       model = MyModel()
       model.load('model.h5')
       
       X_test, y_test = load_test_data()
       
       # Check data quality
       assert not np.any(np.isnan(X_test))
       assert not np.any(np.isinf(X_test))
       
       predictions = model.predict(X_test)
       
       assert predictions is not None
       assert not np.any(np.isnan(predictions))
   ```

3. **No Fairness Testing**
   ```python
   # Bad: No fairness testing
   def test_model_accuracy():
       model = MyModel()
       model.load('model.h5')
       
       X_test, y_test = load_test_data()
       y_pred = model.predict(X_test)
       
       accuracy = calculate_accuracy(y_test, y_pred)
       assert accuracy >= 0.8

   # Good: Test fairness across groups
   def test_model_fairness():
       model = MyModel()
       model.load('model.h5')
       
       X_test, y_test = load_test_data()
       
       # Group by protected attribute
       group_a = X_test[X_test['protected_attribute'] == 0]
       group_b = X_test[X_test['protected_attribute'] == 1]
       
       accuracy_a = calculate_accuracy(y_test[group_a.index], model.predict(group_a))
       accuracy_b = calculate_accuracy(y_test[group_b.index], model.predict(group_b))
       
       fairness_threshold = 0.05  # 5% difference allowed
       assert abs(accuracy_a - accuracy_b) < fairness_threshold
   ```

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

