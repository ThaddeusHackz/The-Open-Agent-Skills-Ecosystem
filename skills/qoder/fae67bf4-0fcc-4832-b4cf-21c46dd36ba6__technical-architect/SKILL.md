---
name: technical-architect
description: System design skill focusing on module boundary definitions, component interactions, API design, data modeling, tech stack evaluation, and non-functional requirements.
---

# Technical Architect Skill

Use this skill when designing component architectures, defining REST/gRPC/GraphQL interfaces, planning database schemas, establishing technical trade-offs, or writing Architecture Decision Records (ADRs).

## Core Responsibilities

1. System & Component Design:
   - Define clear service/module boundaries, communication protocols, and data ownership.
   - Address Non-Functional Requirements (NFRs): Scalability, Availability, Latency, Security, Maintainability.
   - Use standard architectural diagrams (C4 model, sequence diagrams, flowcharts).

2. Technical Decision Framework (ADR Format):
   - Title: Short descriptive name.
   - Context: Problem statement and business drivers.
   - Decision: Option selected and implementation details.
   - Trade-offs: Pros, cons, risks, alternative options rejected.

3. Integration & Data Modeling:
   - Design stateless APIs with clear contracts, standard status codes, structured errors.
   - Choose optimal data storage strategy (Relational, Document, Cache, Event Store).
   - Plan messaging/queue patterns for asynchronous workflows (RabbitMQ, Kafka, SQS).
