---
id: SKL-file-FILECOMPRESSION
name: File Compression
description: File compression reduces file size by encoding data more efficiently.
  This skill covers various compression algorithms, implementation patterns, and best
  practices for both Node.js and Python.
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

# File Compression

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
File compression reduces file size by encoding data more efficiently. This skill covers various compression algorithms, implementation patterns, and best practices for both Node.js and Python.

## Why This Matters
File compression is essential for reducing storage costs, improving transfer speeds, and optimizing bandwidth usage. By choosing the right compression algorithm and implementation strategy, you can achieve significant savings (60-80% for text-based content) while maintaining acceptable performance. This skill provides comprehensive patterns for both Node.js and Python, covering synchronous, asynchronous, and streaming approaches.

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
- Compression libraries are available in the runtime environment
- Sufficient memory is available for compression operations
- Client supports decompression for the chosen algorithm
- File system access is available for file-based operations

## Compatibility
- Gzip: Universal compatibility
- Brotli: Modern browsers (Chrome, Firefox, Edge, Safari)
- Zlib (DEFLATE): Universal compatibility

---

## Test Scenario Matrix
| Scenario | Test Case | Expected Result |
|----------|-----------|----------------|
| Text Compression | Compress HTML file | 60-80% size reduction |
| Binary Compression | Compress JPG file | Minimal/no reduction |
| Streaming | Compress 1GB file | Low memory usage |
| Decompression | Decompress gzip file | Original content restored |
| Auto-detect | Detect compression type | Correct algorithm identified |
| Archive | Create ZIP archive | All files included |

---

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
- Always check if file should be compressed before compressing
- Use streaming compression for files larger than 100MB
- Pre-compress static assets when possible
- Monitor compression ratios and adjust levels accordingly

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Compressing already compressed files**: Don't compress ZIP, MP3, MP4, PNG, JPG
2. **Using high compression for real-time**: Use level 1-3 for real-time responses
3. **Loading entire file into memory**: Use streaming for large files
4. **Ignoring client capabilities**: Check Accept-Encoding header
5. **Not monitoring compression ratios**: Track effectiveness

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

