---
id: SKL-cdn-CDNINTEGRATION
name: Cdn Integration
description: Content Delivery Networks (CDNs) distribute content across multiple geographical
  locations to reduce latency, improve load times, and reduce bandwidth costs. This
  skill covers CloudFront and Cloudflar
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

# Cdn Integration

## Skill Profile
*(Select at least one profile to enable specific modules)*
- [ ] **DevOps**
- [x] **Backend**
- [ ] **Frontend**
- [ ] **AI-RAG**
- [ ] **Security Critical**

## Overview
Content Delivery Networks (CDNs) distribute content across multiple geographical locations to reduce latency, improve load times, and reduce bandwidth costs. This skill covers CloudFront and Cloudflare CDN integration patterns.

## Why This Matters
CDNs are essential for modern web applications to provide fast, reliable content delivery to users worldwide. By caching content at edge locations closer to users, CDNs significantly reduce latency, improve user experience, and reduce load on origin servers. This skill provides comprehensive patterns for integrating with major CDN providers (CloudFront and Cloudflare) including setup, caching strategies, invalidation, security, and optimization.

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
- Origin servers are accessible from CDN edge locations
- SSL certificates are properly configured for custom domains
- S3 buckets are properly configured with appropriate policies
- DNS records are properly configured to point to CDN

## Compatibility
- CloudFront: Compatible with S3, custom origins, ALB/ELB
- Cloudflare: Compatible with any HTTP/HTTPS origin
- Terraform: AWS provider 4.x+, Cloudflare provider 3.x+

---

## Test Scenario Matrix
| Scenario | Test Case | Expected Result |
|----------|-----------|----------------|
| Static Asset Caching | Request cached asset | Served from edge, fast response |
| Cache Miss | Request uncached asset | Fetched from origin, cached for next request |
| Invalidation | Invalidate cached file | File removed from edge cache |
| Signed URL | Access with expired signed URL | 403 Forbidden |
| Custom Domain | Access via custom domain | Serves content with SSL |
| Cache Control | Different TTL per content type | Appropriate caching behavior |

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
- Always validate CDN configuration before deployment
- Use appropriate cache headers for different content types
- Implement cache warming for critical assets
- Monitor CDN performance metrics

## Definition of Done (DoD) Checklist

- [ ] Tests passed + coverage met
- [ ] Lint/Typecheck passed
- [ ] Logging/Metrics/Trace implemented
- [ ] Security checks passed
- [ ] Documentation/Changelog updated
- [ ] Accessibility/Performance requirements met (if frontend)


## Anti-patterns
1. **Wildcard invalidation**: Avoid using `/*` for invalidation - it's slow and expensive
2. **Long TTL for dynamic content**: Don't cache dynamic content with long TTL
3. **No cache headers**: Always set cache headers to control caching behavior
4. **Ignoring cache hit rates**: Monitor and optimize cache hit rates
5. **Direct origin access**: Prevent direct access to origin when using CDN

## Reference Links & Examples

* Internal documentation and examples
* Official documentation and best practices
* Community resources and discussions


## Versioning & Changelog

* **Version**: 1.0.0
* **Changelog**:
  - 2026-02-22: Initial version with complete template structure

