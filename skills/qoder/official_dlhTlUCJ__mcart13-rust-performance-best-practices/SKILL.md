---
name: rust-performance-best-practices
description: Expert-level Rust performance optimization guidelines for build profiles, allocation, synchronization, async/await, and I/O. This skill should be used when writing, reviewing, or optimizing Rust code for performance. Triggers on tasks involving slow Rust code, large binary size, long compile times, LTO configuration, release profile tuning, allocation reduction, clone avoidance, lock contention, BufReader/BufWriter, flamegraph analysis, async runtime issues, Tokio performance, spawn_blocking, parking_lot vs std sync, or any Rust performance investigation.
---

# Rust Performance Best Practices

Expert-level performance optimization guide for Rust. Contains 45+ rules across 9 categories with real benchmarks, failure modes, and profiling workflows.

## When to Apply

Reference these guidelines when:

- Investigating slow Rust programs or high latency
- Optimizing build times or binary size
- Reviewing allocation-heavy code
- Debugging lock contention or thread scaling issues
- Setting up release profiles for production
- Working with async runtimes (Tokio, async-std)

## When NOT to Apply

Skip these optimizations when:

- Code isn't in a hot path (profile first!)
- Readability would suffer significantly
- You haven't measured a performance problem
- The optimization requires unsafe code you can't verify
- Premature optimization would delay shipping

## The Optimization Workflow

**CRITICAL**: Most Rust code doesn't need optimization. Profile first, optimize second.

```
┌─────────────────────────────────────────────────────────────┐
│                   OPTIMIZATION WORKFLOW                      │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. MEASURE FIRST                                           │
│     └── Profile before changing anything                   │
│     └── Use cargo flamegraph, perf, or heaptrack           │
│     └── Identify actual bottlenecks (don't guess!)         │
│                                                             │
│  2. CHECK BUILD SETTINGS                                    │
│     └── Release mode? (10-100x vs debug)                   │
│     └── LTO enabled? (5-20% improvement)                   │
│     └── Target CPU? (10-30% for SIMD)                      │
│                                                             │
│  3. FIX ALGORITHMIC ISSUES                                  │
│     └── O(n²) → O(n log n) matters more than micro-opts   │
│     └── Check data structure choices                       │
│     └── Avoid unnecessary work                             │
│                                                             │
│  4. REDUCE ALLOCATIONS                                      │
│     └── Pre-size collections (with_capacity)               │
│     └── Reuse buffers (clear + reuse)                      │
│     └── Avoid cloning (borrow instead)                     │
│                                                             │
│  5. OPTIMIZE HOT LOOPS                                      │
│     └── Iterators over indices                             │
│     └── Reduce lock scope                                  │
│     └── Batch I/O operations                               │
│                                                             │
│  6. MEASURE AGAIN                                           │
│     └── Verify improvement with benchmarks                 │
│     └── Check for regressions elsewhere                    │
│     └── Document the optimization                          │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Quick Profiling Commands

```bash
# CPU profiling (Linux)
cargo flamegraph --bin myapp
perf record -g ./target/release/myapp && perf report

# Memory profiling
heaptrack ./target/release/myapp && heaptrack_gui heaptrack.myapp.*.gz
DHAT_LOG_FILE=dhat.out cargo run --release && dh_view.py dhat.out

# Benchmark
cargo bench                          # All benchmarks
cargo bench hot_function             # Specific benchmark

# Check allocations
MALLOC_TRACE=/tmp/mtrace.log ./target/release/myapp
mtrace ./target/release/myapp /tmp/mtrace.log

# Assembly inspection
cargo asm my_crate::hot_function --rust

# syscall count
strace -c ./target/release/myapp 2>&1 | head -20
```

## Common Scenarios → Rules

### "My Rust program is slow"

```
Is it running in debug mode?
├── YES → build-release-profile (10-100x speedup)
└── NO
    │
    Where does flamegraph show time?
    ├── malloc/free → alloc-* rules (with_capacity, reuse buffers)
    ├── Mutex::lock → sync-* rules (RwLock, atomics, shorter scope)
    ├── read/write syscalls → io-* rules (BufReader/BufWriter)
    ├── clone/drop → alloc-avoid-clone, use references
    └── Your code → iter-* rules, algorithm improvements
```

### "My binary is too large"

```
1. Enable LTO: build-enable-lto (10-20% smaller)
2. Set opt-level = 'z': build-opt-level (optimizes for size)
3. panic = 'abort': build-panic-abort (removes unwinding code)
4. Strip symbols: strip = true in Cargo.toml
5. Remove debug info: debug = 0
```

### "High memory usage"

```
1. Pre-size collections: alloc-*-with-capacity
2. Reuse allocations: alloc-reuse-buffers
3. Avoid cloning: alloc-avoid-clone
4. Use slices in APIs: alloc-use-slices-in-apis
5. Consider arena allocators: bumpalo crate
```

### "Lock contention / thread scaling"

```
1. Profile: lock_api::ReentrantMutex or parking_lot profiling
2. Reduce lock scope: sync-keep-lock-scope-short
3. Read-heavy? → sync-use-rwlock
4. Simple counters? → sync-use-atomics
5. Message passing? → sync-use-channels
6. Thread-local + periodic flush for stats
```

### "Slow file I/O"

```
1. Wrap in BufReader/BufWriter: io-use-bufreader, io-use-bufwriter
2. Flush before returning: io-flush-bufwriter (data loss prevention!)
3. Reuse line buffer: io-read-line-with-bufread
4. Consider mmap for random access: memmap2 crate
```

## Rule Categories

| Priority | Category        | Typical Impact                      | Prefix    |
| -------- | --------------- | ----------------------------------- | --------- |
| 1        | Build Profiles  | 10-100x (debug→release)             | `build-`  |
| 2        | Benchmarking    | Enables measurement                 | `bench-`  |
| 3        | Allocation      | 2-50x for allocation-heavy code     | `alloc-`  |
| 4        | Data Structures | 2-10x for hot paths                 | `data-`   |
| 5        | Iteration       | 2-5x for loop-heavy code            | `iter-`   |
| 6        | Synchronization | 5-100x for contended code           | `sync-`   |
| 7        | I/O             | 10-100x for I/O-bound code          | `io-`     |
| 8        | Unsafe          | 5-30% in tight loops (experts only) | `unsafe-` |

## 1. Build Profiles (CRITICAL)

These apply to ALL Rust code. Check these first.

| Rule                    | Impact      | One-liner                            |
| ----------------------- | ----------- | ------------------------------------ |
| `build-release-profile` | 10-100x     | Always ship release builds           |
| `build-opt-level`       | 2-5x        | opt-level=3 for speed, 'z' for size  |
| `build-enable-lto`      | 5-20%       | LTO enables cross-crate optimization |
| `build-codegen-units`   | 5-15%       | codegen-units=1 for max optimization |
| `build-panic-abort`     | Binary size | panic='abort' removes unwinding      |
| `build-target-cpu`      | 10-30%      | target-cpu=native for SIMD           |
| `build-pgo`             | 5-20%       | Profile-guided optimization          |
| `build-incremental-off` | 5-10%       | Disable for release builds           |

## 2. Benchmarking (REQUIRED)

You can't optimize what you don't measure.

| Rule                  | Purpose                             |
| --------------------- | ----------------------------------- |
| `bench-cargo-bench`   | Use `cargo bench` with criterion    |
| `bench-bench-profile` | Bench profile enables optimizations |
| `bench-black-box`     | Prevent dead code elimination       |
| `bench-avoid-io`      | I/O variance destroys measurements  |

## 3. Allocation

Every allocation is a syscall. Reduce them.

| Rule                          | Impact      | Pattern                                                           |
| ----------------------------- | ----------- | ----------------------------------------------------------------- |
| `alloc-vec-with-capacity`     | 2-10x       | `Vec::with_capacity(n)` not `Vec::new()`                          |
| `alloc-string-with-capacity`  | 2-5x        | `String::with_capacity(n)`                                        |
| `alloc-hashmap-with-capacity` | 2-5x        | `HashMap::with_capacity(n)`                                       |
| `alloc-reuse-buffers`         | 2-10x       | `.clear()` and reuse, don't reallocate (up to 50x in tight loops) |
| `alloc-use-slices-in-apis`    | Flexibility | `&[T]` not `Vec<T>` in parameters                                 |
| `alloc-avoid-clone`           | 2-10x       | Borrow `&T` instead of `clone()` (benefits scale with data size)  |

## 4. Data Structures

The right data structure beats micro-optimization.

| Rule                             | When                          |
| -------------------------------- | ----------------------------- |
| `data-avoid-linkedlist`          | Almost always (Vec wins)      |
| `data-choose-vecdeque-for-queue` | FIFO queues                   |
| `data-choose-map-type`           | HashMap=O(1), BTreeMap=sorted |
| `data-use-entry-api`             | Insert-or-update patterns     |
| `data-repr-transparent`          | FFI newtypes                  |

## 5. Iteration

Iterators are as fast as loops and safer.

| Rule                           | Impact        | Pattern                                 |
| ------------------------------ | ------------- | --------------------------------------- |
| `iter-avoid-collect-then-loop` | 2-3x          | Chain iterators, don't collect          |
| `iter-use-lazy-iterators`      | 2-3x          | `.filter().map()` not intermediate vecs |
| `iter-use-any-find`            | Short-circuit | `.any()` not `.filter().count() > 0`    |
| `iter-use-retain`              | In-place      | `.retain()` not `.filter().collect()`   |
| `iter-use-binary-search`       | O(log n)      | `.binary_search()` on sorted data       |

## 6. Synchronization

Locks are expensive. Minimize contention.

| Rule                         | Impact         | When                                          |
| ---------------------------- | -------------- | --------------------------------------------- |
| `sync-share-with-arc`        | Avoids copying | Share large (>64B) data across threads        |
| `sync-use-rwlock`            | 2-8x for reads | >80% reads, few writes; consider parking_lot  |
| `sync-keep-lock-scope-short` | 4x             | Minimize code under lock                      |
| `sync-use-channels`          | 3-4x           | Message passing vs shared state               |
| `sync-use-atomics`           | 20x            | Simple counters, flags                        |
| `sync-use-parking-lot`       | 1.5-5x         | Prefer `parking_lot` over std sync primitives |

## 7. I/O

Every syscall costs. Buffer them.

| Rule                        | Impact   | Pattern                              |
| --------------------------- | -------- | ------------------------------------ |
| `io-use-bufreader`          | 50x      | Wrap `File` in `BufReader`           |
| `io-use-bufwriter`          | 18x      | Wrap `File` in `BufWriter`           |
| `io-flush-bufwriter`        | CRITICAL | **Must flush or lose data!**         |
| `io-read-line-with-bufread` | 53x      | Reuse String buffer with `read_line` |

## 8. Async/Await (HIGH)

Critical for Tokio and async-std applications.

| Rule                      | Impact        | Pattern                                      |
| ------------------------- | ------------- | -------------------------------------------- |
| `async-spawn-blocking`    | Prevents hang | Use `spawn_blocking` for CPU-bound work      |
| `async-cooperative`       | Latency       | Yield periodically in long computations      |
| `async-mutex-choice`      | Correctness   | `tokio::sync::Mutex` across `.await` points  |
| `async-avoid-blocking-io` | Throughput    | Use async I/O, not std::fs in async contexts |
| `async-bounded-channels`  | Backpressure  | Prefer bounded channels for flow control     |

**Key insight**: The async runtime is cooperative. Blocking the executor thread starves all other tasks.

```rust
// BAD: Blocks the async runtime
async fn process(data: &[u8]) -> Result<Hash> {
    let hash = expensive_hash(data);  // CPU-bound, blocks executor!
    Ok(hash)
}

// GOOD: Offload to blocking thread pool
async fn process(data: Vec<u8>) -> Result<Hash> {
    tokio::task::spawn_blocking(move || expensive_hash(&data)).await?
}
```

## 9. Unsafe (Expert Only)

Only after profiling proves these matter.

| Rule                      | Impact        | Risk                      |
| ------------------------- | ------------- | ------------------------- |
| `unsafe-get-unchecked`    | 5-30%         | UB if bounds wrong        |
| `unsafe-use-maybeuninit`  | 20-100x alloc | UB if read before write   |
| `unsafe-avoid-transmute`  | Correctness   | Prefer safe alternatives  |
| `unsafe-repr-transparent` | Zero-cost     | Required for FFI newtypes |

## Decision Trees

### When to use with_capacity?

```
Do you know the size?
├── YES, exact → with_capacity(exact)
├── YES, approximate → with_capacity(estimate)
└── NO
    │
    Will it grow frequently?
    ├── YES → Start bigger or use reserve()
    └── NO → Vec::new() is fine
```

### Mutex vs RwLock vs Atomics?

```
Is it a simple counter/flag?
├── YES → Atomics (20x faster)
└── NO
    │
    What's the read/write ratio?
    ├── Mostly reads (>90%) → RwLock
    ├── Mostly writes → Mutex
    └── Mixed → Mutex (simpler)

    Consider: parking_lot > std for all of these
```

### When is unsafe get_unchecked worth it?

```
Did you profile and find bounds checks are the bottleneck?
├── NO → Don't use it
└── YES
    │
    Did you check if LLVM already removed the bounds check?
    ├── NO → Check assembly first (cargo asm)
    └── YES, still there
        │
        Can you use iterators instead?
        ├── YES → Use iterators (same speed, safe)
        └── NO → get_unchecked with documented invariants
```

## Reading Rules

Each rule file in `rules/` contains:

- **Quantified impact** with real benchmark numbers
- **Visual explanations** of how the optimization works
- **Incorrect examples** showing common mistakes
- **Correct examples** with best practices
- **When NOT to apply** - trade-offs and edge cases
- **Common mistakes** to avoid
- **Profiling commands** to identify the issue
- **References** to official docs

## Full Compiled Document

For all rules in a single file: `AGENTS.md`
