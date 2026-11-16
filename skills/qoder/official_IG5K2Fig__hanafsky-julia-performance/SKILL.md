---
name: julia-performance
description: |
  Julia code performance optimization skill. Covers type stability, memory reduction,
  profiling, SIMD, and parallelization.
  Use this skill when the user mentions: Julia performance, type stability, @benchmark,
  @btime, @code_warntype, BenchmarkTools, ProfileView, JET.jl, @report_opt, @report_call,
  runtime dispatch, memory allocation, StaticArrays, LoopVectorization, @turbo, Threads,
  slow Julia code, Julia optimization, or any request to profile/speed up Julia code.
---

# Julia Performance Optimization

Apply optimizations in this order — measure first, then fix.

## Step 1: Measure before optimizing

```julia
using BenchmarkTools

@btime my_function(args...)        # quick measurement
@benchmark my_function(args...)    # full stats with distribution
```

Key fields in `@benchmark` output:
- `median time` — use median, not mean (robust to outliers)
- `allocs` — high alloc count suggests type instability
- `memory estimate` — unexpectedly large → unnecessary array copies

## Step 2: Fix type instability

Julia's JIT compiler can only optimize when types are known at compile time.

```julia
# Quick check (red ::Any = type-unstable)
@code_warntype my_function(args...)

# Deeper: inspect the full call graph
@code_llvm my_function(args...)
```

### JET.jl — automated type analysis

JET traverses the entire call graph and detects runtime dispatch automatically.
More powerful than `@code_warntype` for complex code.

```julia
using JET

@report_opt my_function(args...)   # find runtime dispatch
@report_call my_function(args...)  # find type errors

# Whole-file analysis
report_file("scripts/explore.jl"; analyzer=JET.OptAnalyzer)
```

**Recommended workflow:** `@report_opt` first (fix dispatch) → `@report_call` (fix errors)

> ⚠️ JET v0.11 requires Julia 1.12. `] add JET` picks the right version automatically.

### Common type instability patterns

```julia
# ❌ Non-const global variable
x = 1.0
f() = x * 2

# ✅ Use const or pass as argument
const x = 1.0
f(x) = x * 2

# ❌ Return type changes in branches
g(flag) = flag ? 1 : 1.0   # Int vs Float64

# ✅ Unify return types
g(flag) = flag ? 1.0 : 1.0
```

## Step 3: Reduce memory allocations

```julia
# ❌ Allocate inside loop
for i in 1:1000
    tmp = zeros(100)
end

# ✅ Pre-allocate and reuse
tmp = zeros(100)
for i in 1:1000
    fill!(tmp, 0)
end

# ✅ Use in-place operations (! functions)
mul!(C, A, B)           # C = A*B without allocation
broadcast!(f, dst, src)

# ✅ Avoid slice copies with @views
f(@view A[1:100, :])
```

## Step 4: Array access and loop patterns

```julia
# ✅ Julia is column-major — loop columns in outer loop
for j in 1:m, i in 1:n
    A[i, j] = ...
end

# ✅ Small fixed-size arrays → StaticArrays
using StaticArrays
v = SVector{3, Float64}(1.0, 2.0, 3.0)

# ✅ Skip bounds checks (only after verifying correctness)
@inbounds for x in A
    s += x
end

# ✅ Explicit SIMD with LoopVectorization
using LoopVectorization
@turbo for i in eachindex(A)
    A[i] = sqrt(A[i])
end
```

## Step 5: Profile to find hotspots

```julia
using Profile, ProfileView

@profile my_heavy_function()
ProfileView.view()    # flamegraph (requires ] add ProfileView)
Profile.print()       # text output
```

## Step 6: Parallelism (only when steps 1–5 are exhausted)

```julia
# Multi-threading (launch with julia -t 4)
Threads.@threads for i in 1:n
    result[i] = heavy_compute(i)
end
```

## Checklist

| Check | Tool |
|-------|------|
| Find bottleneck | `@benchmark` |
| Type instability (quick) | `@code_warntype` |
| Type instability (full graph) | `JET.@report_opt` |
| Type errors | `JET.@report_call` |
| Excess allocations | `@benchmark` allocs field |
| Column-major access | code review |
| Global variables | code review → `const` |
| Slice copies | `@views` |

## Package policy

Never run `Pkg.add` or any Pkg operation. If a required package is missing, stop and ask the human:

```
⚠️ Package not installed. Please run in Julia REPL:
] add BenchmarkTools
Resume when done.
```

See the project README for the list of recommended packages to pre-install.

## References

| Book | Author | Notes |
|------|--------|-------|
| *Julia High Performance* 2nd ed. (2019) | Avik Sengupta (Packt) | The standard reference for Julia optimization |
| *Hands-on Design Patterns with Julia* (2020) | Tom Kwong (Packt) | Performance-aware design patterns |
| *Practical Julia* (2023) | Lee Phillips (No Starch) | Scientific computing focus |

- [Julia Performance Tips (official docs)](https://docs.julialang.org/en/v1/manual/performance-tips/) ← read this first
