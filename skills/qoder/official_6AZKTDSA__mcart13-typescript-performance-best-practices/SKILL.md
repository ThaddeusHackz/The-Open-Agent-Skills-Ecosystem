---
name: typescript-performance-best-practices
description: TypeScript performance optimization guidelines for build times, type-checking, declaration emit, and editor responsiveness. This skill should be used when writing, reviewing, or optimizing TypeScript code and tsconfig settings. Triggers on tasks involving slow builds, slow type-checking, CI timeouts, editor lag, tsserver memory issues, monorepo configuration, project references, incremental builds, declaration emit, isolatedDeclarations, --noCheck flag, TypeScript 5.6+ features, TypeScript 7 migration, or any TypeScript performance investigation.
---

# TypeScript Performance Best Practices

Comprehensive performance optimization guide for TypeScript codebases. Contains 43 rules across 8 categories, prioritized by impact to guide automated refactoring and code generation.

## When to Apply

Reference these guidelines when:

- Writing or refactoring TypeScript code
- Tuning build times, type-checking performance, declaration emit, or editor responsiveness
- Investigating performance regressions
- Reviewing code for performance issues
- Configuring tsconfig.json for new projects or monorepos

## Quick Diagnostic Workflow

When TypeScript feels slow, follow this diagnostic sequence:

```bash
# Step 1: Get baseline metrics
tsc --extendedDiagnostics --noEmit

# Key metrics to check:
# - Files: Should match expected source count
# - Check time: Usually the bottleneck (>10s is high)
# - Instantiations: High count indicates complex generics

# Step 2: If file count is high
tsc --listFiles | wc -l
tsc --explainFiles 2>&1 | grep -v "@types" | head -50

# Step 3: If Check time is high
tsc --generateTrace ./trace --noEmit
# Open chrome://tracing and load trace/trace.json

# Step 4: If module resolution is slow
tsc --traceResolution 2>&1 | head -200
```

## Rule Categories by Priority

| Priority | Category                      | Impact      | Quick Win                         |
| -------- | ----------------------------- | ----------- | --------------------------------- |
| 1        | Build Graph & Incremental     | CRITICAL    | Enable `incremental: true`        |
| 2        | Program Scope & Inputs        | HIGH        | Narrow `include` patterns         |
| 3        | Module Resolution & Imports   | HIGH        | Use `moduleResolution: "bundler"` |
| 4        | Type Acquisition & Lib Checks | MEDIUM-HIGH | Enable `skipLibCheck: true`       |
| 5        | Type System Complexity        | CRITICAL    | Annotate function return types    |
| 6        | Declaration Emit & Public API | MEDIUM-HIGH | Enable `isolatedDeclarations`     |
| 7        | Editor/tsserver Performance   | MEDIUM-HIGH | Use project references            |
| 8        | Diagnostics & Profiling       | DIAGNOSTIC  | Run `tsc --extendedDiagnostics`   |

## Common Scenarios

### Scenario: Slow CI Builds (>60s)

**Symptoms:** CI takes minutes, incremental doesn't help

**Diagnostic:**

```bash
tsc --extendedDiagnostics --noEmit
# Check: Files count, Check time, Memory used
```

**Likely fixes:**

1. Enable `incremental: true` with cached `.tsbuildinfo`
2. Enable `skipLibCheck: true` (10-50% improvement)
3. Split into project references (60-70% memory reduction)
4. Narrow `include` patterns

---

### Scenario: Slow Editor/IntelliSense

**Symptoms:** Autocomplete lags, hover takes seconds, high memory

**Diagnostic:**

```bash
# Check tsserver memory
ps aux | grep tsserver | awk '{print $6/1024 " MB"}'
```

**Likely fixes:**

1. Enable `disableReferencedProjectLoad: true`
2. Enable `disableSolutionSearching: true`
3. Enable `disableSourceOfProjectReferenceRedirect: true`
4. Split into project references

---

### Scenario: Type Checking Takes >10s

**Symptoms:** `Check time` dominates in diagnostics

**Diagnostic:**

```bash
tsc --generateTrace ./trace --noEmit
# Open chrome://tracing, find slow checkSourceFile operations
```

**Likely fixes:**

1. Add explicit return type annotations to exported functions
2. Simplify large unions (50+ members)
3. Replace deep intersections with interface extension
4. Name complex types with type aliases

---

### Scenario: Unexpected Files in Build

**Symptoms:** More files than expected, node_modules source compiled

**Diagnostic:**

```bash
tsc --explainFiles 2>&1 | grep -v "@types" | grep "node_modules"
```

**Likely fixes:**

1. Add `"exclude": ["node_modules", "dist"]`
2. Narrow `include` to `["src"]`
3. Remove broad `**/*` patterns

## Quick Reference

### 1. Build Graph & Incremental (CRITICAL)

**Impact:** 50-80% faster rebuilds; essential for monorepos

| Rule                       | Impact   | Description                                   |
| -------------------------- | -------- | --------------------------------------------- |
| `build-project-references` | CRITICAL | Split large repos into referenced projects    |
| `build-composite`          | CRITICAL | Enable composite for project reference builds |
| `build-incremental`        | CRITICAL | Reuse prior type-checking work                |
| `build-tsbuildinfo`        | HIGH     | Cache incremental state in stable location    |
| `build-tsc-build`          | HIGH     | Use `tsc --build` for reference graphs        |
| `build-assume-direct-deps` | MEDIUM   | Speed up watch in very large repos            |

### 2. Program Scope & Inputs (HIGH)

**Impact:** Reduces files parsed; every extra file costs time

| Rule                         | Impact      | Description                            |
| ---------------------------- | ----------- | -------------------------------------- |
| `scope-tight-include`        | HIGH        | Restrict include to source directories |
| `scope-exclude-build-output` | HIGH        | Exclude dist/build/node_modules        |
| `scope-avoid-broad-globs`    | MEDIUM-HIGH | Avoid `**/*` in large repos            |
| `scope-use-files-array`      | MEDIUM      | Explicit file lists for small packages |
| `scope-separate-tests`       | MEDIUM      | Keep tests in separate tsconfig        |

### 3. Module Resolution & Imports (HIGH)

**Impact:** Reduces resolution overhead; wrong mode = excessive lookups

| Rule                              | Impact      | Description                       |
| --------------------------------- | ----------- | --------------------------------- |
| `resolve-moduleResolution-modern` | HIGH        | Use node16/nodenext/bundler       |
| `resolve-bundler-mode`            | HIGH        | Use bundler mode for bundled apps |
| `resolve-keep-paths-tight`        | MEDIUM-HIGH | Avoid catch-all paths patterns    |
| `resolve-use-packagejson-exports` | MEDIUM      | Use package.json exports/imports  |
| `resolve-baseurl-minimize`        | MEDIUM      | Use baseUrl only when needed      |

### 4. Type Acquisition & Lib Checks (MEDIUM-HIGH)

**Impact:** 10-50% faster type-checking; skips redundant work

| Rule                                       | Impact      | Description                           |
| ------------------------------------------ | ----------- | ------------------------------------- |
| `types-limit-types`                        | MEDIUM-HIGH | Include only needed @types            |
| `types-restrict-typeRoots`                 | MEDIUM      | Limit global type search paths        |
| `types-skip-lib-check`                     | HIGH        | Skip .d.ts validation (major win)     |
| `types-typeacquisition-control`            | MEDIUM      | Control automatic type acquisition    |
| `types-disable-filename-based-acquisition` | LOW         | Prevent filename-based type downloads |

### 5. Type System Complexity (CRITICAL)

**Impact:** Complex types cause O(n^2) checking; simplification = big wins

| Rule                            | Impact      | Description                                 |
| ------------------------------- | ----------- | ------------------------------------------- |
| `type-annotate-exports`         | CRITICAL    | Named exported types reduce emit cost       |
| `type-annotate-returns`         | CRITICAL    | Return annotations reduce inference         |
| `type-name-complex-types`       | HIGH        | Named types reduce expansions               |
| `type-avoid-deep-intersections` | HIGH        | Interfaces cached; intersections recomputed |
| `type-avoid-large-unions`       | HIGH        | Large unions cause O(n\*m) checking         |
| `type-export-named-types`       | MEDIUM-HIGH | Named exports reduce .d.ts size             |

### 6. Declaration Emit & Public API (MEDIUM-HIGH)

**Impact:** Up to 3x faster with isolatedDeclarations (requires `--noCheck` or alternative emitters like swc/oxc to benefit); parallel emit

| Rule                        | Impact      | Description                          |
| --------------------------- | ----------- | ------------------------------------ |
| `dts-emit-declaration-only` | MEDIUM-HIGH | Skip JS emit when bundler handles it |
| `dts-declarationDir`        | MEDIUM      | Organize .d.ts output separately     |
| `dts-strip-internal`        | MEDIUM      | Remove @internal from .d.ts          |
| `dts-isolated-declarations` | CRITICAL    | Enable parallel .d.ts emit           |
| `dts-noCheck-fast-emit`     | HIGH        | Skip type-check for .d.ts emit       |

### 7. Editor/tsserver Performance (MEDIUM-HIGH)

**Impact:** ~3GB to <1GB memory; faster startup, navigation

| Rule                                       | Impact      | Description                       |
| ------------------------------------------ | ----------- | --------------------------------- |
| `tsserver-disable-referenced-project-load` | MEDIUM-HIGH | Load projects on demand           |
| `tsserver-disable-solution-searching`      | MEDIUM-HIGH | Stop upward config search         |
| `tsserver-disable-source-redirect`         | MEDIUM-HIGH | Use .d.ts across boundaries       |
| `tsserver-use-project-references`          | HIGH        | Split projects for memory savings |
| `tsserver-solution-config`                 | MEDIUM-HIGH | Root tsconfig with files:[]       |

### 8. Diagnostics & Profiling (DIAGNOSTIC)

**Purpose:** Tools for finding performance issues, not optimizations themselves

| Rule                        | Purpose                   | When to Use                 |
| --------------------------- | ------------------------- | --------------------------- |
| `diag-extended-diagnostics` | Detailed timing breakdown | First diagnostic to run     |
| `diag-diagnostics`          | Quick timing overview     | CI summaries                |
| `diag-explain-files`        | Why files are included    | Unexpected file count       |
| `diag-trace-resolution`     | Module resolution steps   | "Cannot find module" errors |
| `diag-generate-trace`       | Chrome DevTools trace     | Deep type-checking analysis |
| `diag-list-files`           | All files in compilation  | Scope audits                |

## Recommended Base Configuration

For most TypeScript projects:

```json
{
  "compilerOptions": {
    // Performance essentials
    "incremental": true,
    "skipLibCheck": true,
    "moduleResolution": "bundler",

    // For libraries
    "declaration": true,
    "declarationMap": true,
    "isolatedDeclarations": true,

    // Standard strictness
    "strict": true,
    "noUncheckedIndexedAccess": true,

    // Output
    "target": "ES2022",
    "module": "ESNext"
  },
  "include": ["src"],
  "exclude": ["node_modules", "dist"]
}
```

For monorepos, add to each package:

```json
{
  "compilerOptions": {
    "composite": true,
    "disableReferencedProjectLoad": true,
    "disableSolutionSearching": true,
    "disableSourceOfProjectReferenceRedirect": true
  }
}
```

## TypeScript 5.6+ Performance Features

Recent TypeScript versions (5.6-5.8) introduced significant performance improvements:

### `--noCheck` Flag (TS 5.6+)

Skip type-checking when you only need transpilation or declaration emit:

```bash
# Fast declaration emit without type-checking
tsc --declaration --emitDeclarationOnly --noCheck

# Combine with isolatedDeclarations for maximum speed
tsc --declaration --emitDeclarationOnly --noCheck --isolatedDeclarations
```

**When to use:** CI pipelines where type-checking runs separately, or when using swc/esbuild for transpilation.

### `--libReplacement` Flag (TS 5.8+)

Control whether lib.d.ts can be replaced by node_modules types:

```json
{
  "compilerOptions": {
    "libReplacement": false
  }
}
```

**Impact:** Prevents unexpected type resolution slowdowns from packages that ship their own lib replacements.

### Version Compatibility Table

| Feature                | Minimum TS Version | Impact       |
| ---------------------- | ------------------ | ------------ |
| `isolatedDeclarations` | 5.5                | Up to 3x     |
| `--noCheck`            | 5.6                | 2-10x emit   |
| `--libReplacement`     | 5.8                | Varies       |
| Swiss Table internals  | 5.8                | 5-20% faster |

## TypeScript 7 Preview (Experimental)

TypeScript 7, currently in development, is being rewritten in Go for significantly faster compilation. Early benchmarks suggest:

- **10x faster** type-checking in large codebases
- **5x faster** editor responsiveness
- Full backward compatibility with TS 5.x configs

**Status (as of January 2026):** Preview builds available. Not production-ready. Monitor [TypeScript 7 roadmap](https://github.com/microsoft/TypeScript/issues/59905) for updates.

## How to Use

Read individual rule files for detailed explanations and code examples:

```
rules/build-project-references.md
rules/type-annotate-returns.md
rules/diag-generate-trace.md
```

Each rule file contains:

- **Impact rating** with quantified description
- **Why it matters** with numbered benefits
- **Incorrect/Correct** code examples
- **When NOT to apply** (important for avoiding over-optimization)
- **Common mistakes** to avoid
- **Diagnostic commands** for verification
- **References** to official documentation

## References

- [TypeScript Performance Wiki](https://github.com/microsoft/TypeScript/wiki/Performance)
- [TypeScript tsconfig Reference](https://www.typescriptlang.org/tsconfig)
- [TypeScript Project References](https://www.typescriptlang.org/docs/handbook/project-references.html)
- [TypeScript 5.5 isolatedDeclarations](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-5.html)
- [TypeScript 5.6 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-6.html)
- [TypeScript 5.8 Release Notes](https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-8.html)
- [TypeScript 7 Roadmap (Go Rewrite)](https://github.com/microsoft/TypeScript/issues/59905)
