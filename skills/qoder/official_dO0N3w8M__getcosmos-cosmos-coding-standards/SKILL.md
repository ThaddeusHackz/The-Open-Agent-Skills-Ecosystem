---
name: cosmos-coding-standards
description: Coding standards for readable, maintainable, testable code including SOLID principles, clean code practices, DDD, and TDD. Use when implementing new features, refactoring code, performing code reviews, ensuring code quality, or when frontend changes are made that require UI testing.
---

# Coding Standards & Best Practices

Implementing effective coding standards, architecture, and practices is crucial for developing software that is readable, maintainable, and testable. High-quality code is designed for change, with a focus on low coupling, high cohesion, and clear, intent-revealing structures.

## Coding Standards & Best Practices (Readability)

**Consistency**: Use automated formatting tools (e.g., Biome, typecheck) to enforce consistent indentation, line length, and styling. Code is not complete if linting errors exist.

**Naming Conventions**: Use descriptive, noun-based names for variables and classes, and camelCase for methods. Avoid abbreviations. Use prefixes like `is` for booleans.

**Self-Documenting Code**: Code should communicate its intent without excessive comments. If comments are necessary, they should explain "why" rather than "what".

**Small Functions**: Break large functions into smaller, single-purpose chunks (e.g., `buildSchedule()` instead of a large `process()` method).

**No Magic Numbers**: Replace raw, hard-coded numbers or strings with named constants.

## Architectural Principles (Maintainability)

**SOLID Principles**: Adhere to Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, and Dependency Inversion.

**Separation of Concerns**: Separate business logic from I/O operations (database, UI, network).

**Low Coupling & High Cohesion**: Components should depend on abstractions (interfaces) rather than concrete implementations to reduce interdependencies.

**Domain-Driven Design (DDD)**: Model software based on the domain, keeping domain logic independent of external frameworks.

**Avoid Anti-Patterns (KISS)**: Steer clear of "God Objects" (classes with too many responsibilities) and widespread "Copy & Paste" programming.

## Testable Code Design (Testability)

**Dependency Injection (DI)**: Pass dependencies into functions/classes rather than creating them internally, enabling the use of mocks or stubs.

**Unit Test Isolation**: Ensure units of code can be tested in isolation without needing to connect to databases or live systems.

**Predictable Input/Output**: Write pure functions where possible—same input always yields the same output.

**Independence**: Tests should be independent of one another, with clear setup and teardown strategies. Review how they are done in the project and continue best practices.

## UI Testing

When frontend changes are made, perform UI testing using browser tools to verify visual and functional correctness.

## Summary Table of Key Principles

| Principle | Goal | Actionable Advice |
|-----------|------|-------------------|
| SOLID | Scalability | Build loosely coupled components. |
| Clean Code | Readability | Use meaningful names; keep functions small. |
| DDD | Maintainability | Separate domain logic from infrastructure. |
| TDD/DI | Testability | Inject dependencies; minimize side effects. |
| Automation | Consistency | Use linting/formatting tools in CI/CD. |
| UI Testing | Quality Assurance | aLL frontend changes require manual browser testing. |
