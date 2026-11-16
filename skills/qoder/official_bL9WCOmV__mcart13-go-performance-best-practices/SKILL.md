---
name: go-performance-best-practices
description: Go performance optimization guidelines for profiling, allocation, GC tuning, concurrency, PGO, and I/O. This skill should be used when writing, reviewing, or optimizing Go code for performance. Triggers on tasks involving slow services, high latency, high memory usage, memory leaks, goroutine leaks, GC pressure, CPU profiling, pprof analysis, allocation reduction, sync.Pool, mutex contention, HTTP client tuning, Profile-Guided Optimization, GOMEMLIMIT tuning, Go 1.24 features, Swiss Tables, or any Go performance investigation.
---

# Go Performance Best Practices

Comprehensive performance optimization guide for Go codebases. Contains 41 rules across 8 categories with real-world benchmarks, BOMvault-specific examples, and proven optimization patterns from 10+ years of production experience.

## When to Apply

Reference these guidelines when:

- Writing or refactoring Go code
- Tuning latency, throughput, allocation rate, or GC behavior
- Investigating performance regressions
- Reviewing code for performance issues
- Debugging memory leaks or goroutine leaks
- Optimizing containerized services (ECS, Kubernetes)

## The Performance Optimization Workflow

### Phase 1: Measure First (Don't Guess)

**Never optimize without data.** The #1 mistake is optimizing based on intuition.

```bash
# Step 1: Establish baseline with benchmarks
go test -bench=. -benchmem -count=5 ./... | tee baseline.txt

# Step 2: Generate CPU profile for hot paths
go test -bench=BenchmarkCriticalPath -cpuprofile=cpu.prof
go tool pprof -http=:8080 cpu.prof

# Step 3: Generate heap profile for allocations
go test -bench=BenchmarkCriticalPath -memprofile=heap.prof
go tool pprof -http=:8080 heap.prof

# Step 4: Check allocation counts (correlates with latency)
go tool pprof -alloc_objects heap.prof
```

**Key pprof views:**
| View | Use For |
|------|---------|
| `top` | Quick ranking of hot functions |
| `list funcname` | Line-by-line attribution |
| `web` | Visual call graph |
| `flame` | Flame graph for deep call stacks |
| `peek funcname` | Callers and callees |

### Phase 2: Identify the Bottleneck

**Use the right profile for the right problem:**

| Symptom                            | Profile Type | pprof Flag                          |
| ---------------------------------- | ------------ | ----------------------------------- |
| High CPU usage                     | CPU          | `-cpuprofile`                       |
| High memory usage                  | Heap (inuse) | `-memprofile` + `-inuse_space`      |
| High allocation rate / GC pressure | Heap (alloc) | `-memprofile` + `-alloc_objects`    |
| Goroutine leaks                    | Goroutine    | `runtime/pprof.Lookup("goroutine")` |
| Lock contention                    | Mutex        | `-mutexprofile`                     |
| Blocking operations                | Block        | `-blockprofile`                     |

**Quick diagnosis commands:**

```bash
# CPU: What's using the most cycles?
go tool pprof -top cpu.prof

# Memory: What's consuming the most heap?
go tool pprof -top -inuse_space heap.prof

# Allocations: What's creating the most objects?
go tool pprof -top -alloc_objects heap.prof

# Compare before/after
go tool pprof -base baseline.prof optimized.prof
```

### Phase 3: Apply Targeted Optimization

**Match the symptom to the optimization category:**

| Symptom             | Category       | Key Rules                                              |
| ------------------- | -------------- | ------------------------------------------------------ |
| CPU-bound           | Work Avoidance | `work-cache-*`, `work-short-circuit-*`                 |
| Memory-bound        | Allocation     | `alloc-preallocate-*`, `alloc-copy-to-avoid-retention` |
| GC pauses           | GC Tuning      | `gc-set-gomemlimit`, `gc-use-sync-pool`                |
| I/O latency         | I/O            | `io-buffered-io`, `io-reuse-http-client`               |
| Lock contention     | Concurrency    | `conc-reduce-lock-contention`, `conc-use-atomics`      |
| Goroutine explosion | Concurrency    | `conc-limit-goroutines`, `conc-bounded-channels`       |

### Phase 4: Verify Improvement

```bash
# Run benchmark again
go test -bench=. -benchmem -count=5 ./... | tee optimized.txt

# Compare results
benchstat baseline.txt optimized.txt

# Verify no regressions in other benchmarks
```

**Success criteria:**

- Measurable improvement (not just "feels faster")
- No regressions in other areas
- Code remains readable and maintainable
- Changes are justified by data

---

## Common Optimization Scenarios

### Scenario 1: High Latency / Slow Response Times

**Symptoms:** P99 latency spikes, slow API responses, timeouts

**Diagnosis:**

```bash
# CPU profile during slow requests
curl http://localhost:8080/debug/pprof/profile?seconds=30 > cpu.prof
go tool pprof -http=:8080 cpu.prof
```

**Common causes and fixes:**

| Cause                | Indicator                    | Fix                                                  |
| -------------------- | ---------------------------- | ---------------------------------------------------- |
| JSON encoding        | `encoding/json` in top       | Use `json.NewEncoder` streaming, consider `jsoniter` |
| Regex compilation    | `regexp.Compile` in hot path | Cache compiled regex at init                         |
| Slice/map scanning   | Loops in profile             | Convert to map lookup                                |
| String concatenation | `+` operator in loops        | Use `strings.Builder`                                |
| Excessive logging    | Logger in top                | Reduce log level in hot path                         |

### Scenario 2: High Memory Usage / OOM Kills

**Symptoms:** Container OOM killed, memory growing over time, swap thrashing

**Diagnosis:**

```bash
# Heap profile
curl http://localhost:8080/debug/pprof/heap > heap.prof
go tool pprof -inuse_space -top heap.prof

# Check for memory leaks (growing allocations)
go tool pprof -alloc_space -top heap.prof
```

**Common causes and fixes:**

| Cause                     | Indicator                     | Fix                        |
| ------------------------- | ----------------------------- | -------------------------- |
| Large slice retention     | `append` with small subslices | `copy()` to new slice      |
| Unbounded caches          | Map growing without eviction  | Add LRU/TTL eviction       |
| io.ReadAll on large files | Large `[]byte` allocations    | Stream with `io.Copy`      |
| String/[]byte conversions | `runtime.stringtoslicebyte`   | Stay in one domain         |
| Goroutine leaks           | Goroutine count growing       | Check context cancellation |

### Scenario 3: High GC Pressure / CPU Spent in GC

**Symptoms:** `gc_pause_seconds` high, `runtime.mallocgc` in CPU profile

**Diagnosis:**

```bash
# Check GC stats
GODEBUG=gctrace=1 ./myservice 2>&1 | head -20

# Allocation profile
go tool pprof -alloc_objects -top heap.prof
```

**Common causes and fixes:**

| Cause                    | Indicator                    | Fix                                   |
| ------------------------ | ---------------------------- | ------------------------------------- |
| Many small allocations   | High `alloc_objects`         | Use sync.Pool                         |
| Creating slices in loops | `make([]T, ...)` in hot path | Preallocate or pool                   |
| fmt.Sprintf in hot path  | `fmt.*` allocations          | Use strconv                           |
| Interface boxing         | `interface{}` conversions    | Use generics or concrete types        |
| Not setting GOMEMLIMIT   | Frequent GC cycles           | Set GOMEMLIMIT to 80-90% of container |

### Scenario 4: Goroutine Leaks / Count Growing

**Symptoms:** Goroutine count increases over time, eventual resource exhaustion

**Diagnosis:**

```bash
# Goroutine profile
curl http://localhost:8080/debug/pprof/goroutine?debug=2 > goroutine.txt
cat goroutine.txt | head -100

# Count by state
curl http://localhost:8080/debug/pprof/goroutine?debug=1 | head -50
```

**Common causes and fixes:**

| Cause                   | Indicator                          | Fix                                   |
| ----------------------- | ---------------------------------- | ------------------------------------- |
| Blocked channel receive | `chan receive` in stack            | Add timeout or close channel          |
| HTTP client no timeout  | `net/http.(*persistConn).readLoop` | Set client timeout                    |
| Ticker not stopped      | `time.Tick` in stack               | Use `time.NewTicker` + `defer Stop()` |
| Context not cancelled   | `context.Background()` everywhere  | Pass and check context                |
| Worker pool leak        | Workers waiting on closed channel  | Proper shutdown signaling             |

### Scenario 5: Lock Contention / Serialized Execution

**Symptoms:** CPU not fully utilized, goroutines blocked on mutex

**Diagnosis:**

```bash
# Mutex profile (must be enabled)
curl http://localhost:8080/debug/pprof/mutex > mutex.prof
go tool pprof -top mutex.prof

# Block profile
curl http://localhost:8080/debug/pprof/block > block.prof
go tool pprof -top block.prof
```

**Common causes and fixes:**

| Cause                       | Indicator                      | Fix                     |
| --------------------------- | ------------------------------ | ----------------------- |
| Global mutex                | Single lock in mutex profile   | Shard by key            |
| Write lock for reads        | `sync.Mutex` on read-heavy map | Use `sync.RWMutex`      |
| Lock held during I/O        | I/O calls while holding lock   | Release lock before I/O |
| Atomic operations on struct | `atomic.Value` for config      | Use `atomic.Pointer[T]` |

---

## BOMvault Service Optimization Guide

### License Enricher

**Profile:** CPU-bound, high allocation rate from parsing

**Key optimizations:**

- Cache compiled SPDX license regex patterns at init
- Pool `bytes.Buffer` for license text processing
- Preallocate slice for `AffectedPackages` based on typical size
- Stream large license files instead of `io.ReadAll`

```go
// BOMvault license-enricher pattern
var (
    spdxRegex = regexp.MustCompile(`^[A-Za-z0-9][A-Za-z0-9.-]*$`)
    bufPool   = sync.Pool{New: func() any { return new(bytes.Buffer) }}
)

func (e *Enricher) ProcessLicense(data []byte) (*License, error) {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    defer bufPool.Put(buf)
    // ... use buf for processing
}
```

### Vulnerability Enricher

**Profile:** I/O-bound (NVD API), memory spikes from CVE data

**Key optimizations:**

- Reuse `http.Client` with connection pooling
- Stream JSON responses for large CVE feeds
- Set `GOMEMLIMIT` to 80% of container memory
- Use map for CVE ID lookups instead of slice scanning
- Batch database inserts (100-500 per batch)

```go
// BOMvault vulnerability-enricher pattern
var nvdClient = &http.Client{
    Timeout: 30 * time.Second,
    Transport: &http.Transport{
        MaxIdleConns:        100,
        MaxIdleConnsPerHost: 10,
        IdleConnTimeout:     90 * time.Second,
    },
}

type CVEIndex struct {
    byID map[string]*CVE  // O(1) lookup
}
```

### Graph Ingest

**Profile:** Memory-bound, large SBOM processing

**Key optimizations:**

- Stream SBOM JSON parsing with `json.Decoder`
- Copy component slices to avoid retaining entire SBOM
- Use `GOMEMLIMIT` with soft memory limit
- Bounded worker pool for parallel component processing
- Context timeouts for database operations

```go
// BOMvault graph-ingest pattern
func (g *GraphIngest) ProcessSBOM(ctx context.Context, r io.Reader) error {
    dec := json.NewDecoder(r)  // Stream, don't ReadAll

    // Bounded parallelism
    sem := make(chan struct{}, 10)

    for dec.More() {
        var component Component
        if err := dec.Decode(&component); err != nil {
            return err
        }

        sem <- struct{}{}
        go func(c Component) {
            defer func() { <-sem }()
            g.processComponent(ctx, c)
        }(component)
    }
    return nil
}
```

### Alert Writer

**Profile:** I/O-bound (SARIF generation), batch processing

**Key optimizations:**

- Precompute report templates at startup
- Batch writes to reduce syscalls
- Pool buffers for SARIF report generation
- Use `strings.Builder` for alert message construction

```go
// BOMvault alert-writer pattern
var (
    reportTemplates = template.Must(template.ParseGlob("templates/*.html"))
    bufPool         = sync.Pool{New: func() any { return new(bytes.Buffer) }}
)

func (w *AlertWriter) GenerateSARIF(findings []*Finding) ([]byte, error) {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    buf.Grow(len(findings) * 500)  // Estimate size
    defer bufPool.Put(buf)

    // Batch write to buffer, then single Write to output
}
```

---

## Rule Categories by Priority

| Priority | Category                      | Impact   | Prefix   |
| -------- | ----------------------------- | -------- | -------- |
| 1        | Measurement & Profiling       | CRITICAL | `prof-`  |
| 2        | Allocation & Data Structures  | HIGH     | `alloc-` |
| 3        | Strings, Bytes & Encoding     | HIGH     | `bytes-` |
| 4        | Concurrency & Synchronization | HIGH     | `conc-`  |
| 5        | GC & Memory Limits            | HIGH     | `gc-`    |
| 6        | I/O & Networking              | HIGH     | `io-`    |
| 7        | Runtime & Scheduling          | MEDIUM   | `rt-`    |
| 8        | Work Avoidance & Caching      | MEDIUM   | `work-`  |

## Quick Reference

### 1. Measurement & Profiling (CRITICAL)

| Rule                          | Impact     | When to Apply                      |
| ----------------------------- | ---------- | ---------------------------------- |
| `prof-use-testing-benchmarks` | Foundation | Always benchmark before optimizing |
| `prof-report-allocs`          | Foundation | When allocation rate matters       |
| `prof-benchmark-timers`       | Foundation | When setup skews results           |
| `prof-cpu-profile`            | Foundation | CPU-bound workloads                |
| `prof-heap-profile`           | Foundation | Memory issues, GC pressure         |

### 2. Allocation & Data Structures (HIGH)

| Rule                            | Impact      | When to Apply             |
| ------------------------------- | ----------- | ------------------------- |
| `alloc-preallocate-slices`      | 2-10x       | Known size, append loops  |
| `alloc-preallocate-maps`        | 2-5x        | Known cardinality         |
| `alloc-copy-to-avoid-retention` | Memory leak | Subslices of large arrays |
| `alloc-use-copy-builtin`        | 2-3x        | Slice-to-slice moves      |
| `alloc-avoid-string-byte-conv`  | 2x          | Frequent conversions      |
| `alloc-use-zero-value-buffers`  | Minor       | Buffer initialization     |

### 3. Strings, Bytes & Encoding (HIGH)

| Rule                          | Impact    | When to Apply                              |
| ----------------------------- | --------- | ------------------------------------------ |
| `bytes-use-strings-builder`   | 100-1000x | String concatenation loops (vs + operator) |
| `bytes-use-bytes-buffer`      | 10-100x   | Byte accumulation                          |
| `bytes-grow-when-known`       | 2-5x      | Known final size                           |
| `bytes-avoid-fmt-in-hot-path` | 5-10x     | Number formatting                          |
| `bytes-precompile-regexp`     | 10-100x   | Regex in hot path                          |

### 4. Concurrency & Synchronization (HIGH)

| Rule                          | Impact          | When to Apply           |
| ----------------------------- | --------------- | ----------------------- |
| `conc-limit-goroutines`       | Stability       | Unbounded parallelism   |
| `conc-bounded-channels`       | 2-5x            | Burst absorption        |
| `conc-use-context-cancel`     | Resource safety | Long-running operations |
| `conc-reduce-lock-contention` | 2-10x           | Mutex in profile        |
| `conc-use-atomics`            | 5-10x           | Simple counters         |
| `conc-pass-context`           | Resource safety | All API boundaries      |

### 5. GC & Memory Limits (HIGH)

| Rule                     | Impact              | When to Apply            |
| ------------------------ | ------------------- | ------------------------ |
| `gc-set-gomemlimit`      | OOM prevention      | Containerized apps       |
| `gc-tune-gogc`           | CPU/memory tradeoff | GC overhead visible      |
| `gc-use-sync-pool`       | 10-50x              | Short-lived buffers      |
| `gc-reset-before-put`    | Memory leak         | Pooled objects with refs |
| `gc-avoid-pooling-large` | Memory              | Large objects (>32KB)    |

### 6. I/O & Networking (HIGH)

| Rule                     | Impact      | When to Apply            |
| ------------------------ | ----------- | ------------------------ |
| `io-buffered-io`         | 10x         | Unbuffered file I/O      |
| `io-stream-large-bodies` | O(1) memory | Large HTTP bodies        |
| `io-reuse-http-client`   | 7-10x       | Multiple HTTP requests   |
| `io-tune-transport`      | 2-5x        | High concurrency HTTP    |
| `io-set-timeouts`        | Stability   | All HTTP servers/clients |

### 7. Runtime & Scheduling (MEDIUM)

| Rule                      | Impact        | When to Apply        |
| ------------------------- | ------------- | -------------------- |
| `rt-avoid-busy-loop`      | 100x CPU      | Polling loops        |
| `rt-stop-tickers`         | Resource leak | time.NewTicker usage |
| `rt-set-gomaxprocs`       | Container CPU | Docker/ECS/K8s       |
| `rt-use-timeout-contexts` | Stability     | External calls       |

### 8. Work Avoidance & Caching (MEDIUM)

| Rule                        | Impact       | When to Apply               |
| --------------------------- | ------------ | --------------------------- |
| `work-cache-compiled-regex` | 10-100x      | Regex in request path       |
| `work-cache-lookups`        | O(1) vs O(n) | Repeated containment checks |
| `work-batch-small-writes`   | 3-10x        | Many small writes           |
| `work-precompute-templates` | 10-100x      | Template in request path    |
| `work-short-circuit-common` | 2-10x        | Common trivial inputs       |

---

## Decision Trees

### "My service is slow"

```
Is it CPU-bound? (CPU near 100%)
├── Yes → Profile CPU
│   ├── Hot function is I/O → Check io-* rules
│   ├── Hot function is encoding → Check bytes-* rules
│   ├── Hot function is your code → Check work-* rules
│   └── Hot function is GC → Check gc-* rules
└── No → Profile for blocking
    ├── Mutex contention → Check conc-reduce-lock-contention
    ├── Channel blocking → Check conc-bounded-channels
    ├── Network I/O → Check io-* rules
    └── Disk I/O → Check io-buffered-io
```

### "My service uses too much memory"

```
Is memory growing over time?
├── Yes (leak) →
│   ├── Goroutine count growing → Check context cancellation
│   ├── Map growing → Add eviction/TTL
│   ├── Slice retention → Use copy() for subslices
│   └── Pooled object refs → Reset before Put
└── No (steady but high) →
    ├── Large allocations → Stream instead of ReadAll
    ├── Many small allocations → Use sync.Pool
    ├── High peak usage → Set GOMEMLIMIT
    └── Buffer reallocation → Preallocate with known size
```

### "My service has GC problems"

```
Is GC taking too much CPU?
├── Yes →
│   ├── Many objects → Pool short-lived objects
│   ├── Large heap → Set GOMEMLIMIT higher
│   └── Frequent cycles → Increase GOGC (200-400)
└── No, but pauses are long →
    ├── Large heap → Reduce allocation rate
    └── Pointer-heavy structures → Consider flat arrays
```

---

## Profiling Cheat Sheet

### Enable pprof in Production

```go
import _ "net/http/pprof"

func main() {
    go func() {
        log.Println(http.ListenAndServe("localhost:6060", nil))
    }()
    // ... rest of app
}
```

### Common pprof Commands

```bash
# Interactive mode
go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
go tool pprof http://localhost:6060/debug/pprof/heap

# Web UI (recommended)
go tool pprof -http=:8080 cpu.prof

# Command-line analysis
go tool pprof -top cpu.prof
go tool pprof -list=FunctionName cpu.prof
go tool pprof -png -output=profile.png cpu.prof

# Compare profiles
go tool pprof -base before.prof after.prof

# Allocation analysis
go tool pprof -alloc_objects heap.prof  # Count of allocations
go tool pprof -alloc_space heap.prof    # Bytes allocated
go tool pprof -inuse_objects heap.prof  # Current live objects
go tool pprof -inuse_space heap.prof    # Current memory usage
```

### Benchmark Commands

```bash
# Run all benchmarks
go test -bench=. -benchmem ./...

# Run specific benchmark
go test -bench=BenchmarkProcess -benchmem

# Multiple runs for statistical significance
go test -bench=. -benchmem -count=10 | tee results.txt

# Compare results
go install golang.org/x/perf/cmd/benchstat@latest
benchstat before.txt after.txt

# Generate profiles from benchmarks
go test -bench=BenchmarkProcess -cpuprofile=cpu.prof -memprofile=mem.prof
```

---

## Profile-Guided Optimization (PGO)

Go 1.21+ supports PGO for 2-7% performance improvement in production workloads.

### PGO Workflow

```bash
# Step 1: Collect production CPU profile (30+ seconds recommended)
curl http://localhost:6060/debug/pprof/profile?seconds=60 > default.pgo

# Step 2: Place profile in package directory
cp default.pgo ./cmd/myservice/default.pgo

# Step 3: Build with PGO (auto-detects default.pgo)
go build ./cmd/myservice

# Step 4: Verify PGO was applied
go build -gcflags="-d=pgo" ./cmd/myservice 2>&1 | grep "PGO"
```

**Best practices:**

- Collect profiles under realistic production load
- Re-collect profiles periodically (weekly/monthly)
- PGO improves inlining and devirtualization decisions
- Works best for CPU-bound workloads

### PGO Impact by Workload Type

| Workload Type     | Expected Improvement | Notes                                   |
| ----------------- | -------------------- | --------------------------------------- |
| HTTP services     | 2-4%                 | Helps with routing, JSON, template code |
| GRPC services     | 3-5%                 | Protocol buffer encoding benefits       |
| CLI tools         | 2-3%                 | Shorter startup time                    |
| Computation-heavy | 5-7%                 | Best for math, parsing, encoding        |

## Go 1.24 Features (January 2025+)

Go 1.24 introduces significant runtime improvements:

### Swiss Tables for Maps

Maps now use Swiss Tables internally for ~10% faster operations on average:

```go
// No code changes required - automatic in Go 1.24+
m := make(map[string]int)  // Uses Swiss Tables internally
```

**Impact:** Lookup and iteration 10-30% faster depending on workload.

### `testing.B.Loop` for Benchmarks

New idiomatic benchmark pattern (Go 1.24+):

```go
// Go 1.23 and earlier
func BenchmarkProcess(b *testing.B) {
    for i := 0; i < b.N; i++ {
        process()
    }
}

// Go 1.24+ (preferred)
func BenchmarkProcess(b *testing.B) {
    for b.Loop() {
        process()
    }
}
```

**Benefits:** Avoids common mistakes with benchmark timers, cleaner syntax.

### Version Compatibility Table

| Feature                 | Minimum Go Version | Impact             |
| ----------------------- | ------------------ | ------------------ |
| Generics                | 1.18               | Type-safe pools    |
| `GOMEMLIMIT`            | 1.19               | OOM prevention     |
| PGO                     | 1.21               | 2-7%               |
| `maps` stdlib package   | 1.21               | Clone, Keys        |
| `slices` stdlib package | 1.21               | Sort, Clone        |
| `sync.OnceFunc`         | 1.21               | Lazy init          |
| `cmp` package           | 1.21               | Generic compare    |
| `log/slog`              | 1.21               | Structured logs    |
| Swiss Tables (maps)     | 1.24               | 10% faster maps    |
| `testing.B.Loop`        | 1.24               | Cleaner benchmarks |

## References

- [Effective Go](https://go.dev/doc/effective_go)
- [Go Performance Wiki](https://github.com/golang/go/wiki/Performance)
- [pprof Documentation](https://pkg.go.dev/runtime/pprof)
- [A Guide to the Go Garbage Collector](https://tip.golang.org/doc/gc-guide)
- [High Performance Go Workshop](https://dave.cheney.net/high-performance-go-workshop/dotgo-paris.html)
- [Go Memory Model](https://go.dev/ref/mem)
- [Profile-Guided Optimization](https://go.dev/doc/pgo)
- [Go 1.24 Release Notes](https://go.dev/doc/go1.24)

## Full Compiled Document

For the complete guide with all rules expanded: `AGENTS.md`
