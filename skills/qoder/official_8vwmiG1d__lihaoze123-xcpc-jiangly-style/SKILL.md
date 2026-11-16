---
name: xcpc-jiangly-style
description: Use when writing C++ competitive programming solutions for Codeforces, ICPC, or similar contests. Apply when creating XCPC solutions to ensure code follows jiangly's proven style patterns.
license: MIT
metadata:
  author: chumeng
  version: "2.4.0"
  source: jiangly Codeforces submissions
---

# XCPC: jiangly C++ Style

## Overview

Proven C++ coding style from jiangly's Codeforces submissions. Focuses on safety, maintainability, and modern C++ features for competitive programming.

**Core principle:** Zero global pollution, zero global arrays, explicit types, modern C++.

## When to Use

- Writing C++ solutions for Codeforces, ICPC, AtCoder, etc.
- Creating competitive programming templates
- Reviewing contest solutions
- Teaching competitive programming best practices

**Don't use for:**
- Production C++ code (different requirements)
- Non-competitive programming projects

---

<IMPORTANT>

## MANDATORY WORKFLOW - READ BEFORE WRITING CODE

**This skill enforces strict adherence to jiangly's coding style. You MUST follow this workflow:**

### Step 1: Consult Rules Before Writing

**Before writing ANY code, you MUST:**

1. **Read the relevant rule files** in `rules/` directory based on your task
2. **Check Red Flags table** below to avoid common mistakes
3. **Reference examples** from rule files - they are the source of truth

### Step 2: Match Rule Requirements

For each code decision, verify against rules:

| Task | Rule File | Key Points |
|------|-----------|------------|
| Variable naming | `rules/naming.md` | `snake_case`, uppercase for temp count arrays (`S, T`) |
| String operations | `rules/in-place-operations.md` | `reserve()`, `swap()` for reuse |
| Temporary arrays | `rules/scope-control.md` | Block scopes `{}`, timely release |
| Logical operators | `rules/formatting.md` | Use `and`, `or`, `not` keywords |
| Loop comparisons | `rules/minimal-code.md` | Symmetric patterns: `s[i] <= t[j]` |
| Memory usage | `rules/in-place-operations.md` | `vis` arrays, no duplicate containers |
| Function design | `rules/struct-patterns.md` | Constructors, const correctness |

### Step 3: Verify Against Red Flags

**Before finalizing code, check EVERY row in the Red Flags table below.**

If any pattern matches, you MUST fix it before output.

### Step 4: Self-Correction Checklist

After writing code, verify:

- [ ] No using namespace std;
- [ ] No global arrays (all in solve())
- [ ] Used using i64 = long long;
- [ ] Used and/or/not instead of &&/||/!
- [ ] Used std:: prefix everywhere
- [ ] 4-space indentation, K&R braces
- [ ] No line compression (one statement per line)
- [ ] Used "\n" not std::endl
- [ ] Large temporary arrays in block scopes {}
- [ ] Strings preallocated with reserve() when size known
- [ ] Used swap() for O(1) variable reuse
- [ ] Used push_back() for single characters, not +=
- [ ] Symmetric comparison patterns (a[i] <= b[j])
- [ ] Uppercase names for temporary count arrays (S, T)
- [ ] Use iota + lambda for index-value sorting, not structs
- [ ] Loop variables initialized in for header when possible
- [ ] Output uses " \n"[i == n - 1] for space-separated values

### Rule Files are PRIMARY Reference

The Quick Reference table below is a summary. **Rule files contain the complete, authoritative examples.** When in doubt, read the rule file.

</IMPORTANT>

---

| Category | Rule | File |
|----------|------|------|
| Namespace | Never `using namespace std;` | [no-global-namespace](rules/no-global-namespace.md) |
| Arrays | Zero global arrays | [zero-global-arrays](rules/zero-global-arrays.md) |
| Types | Use `using i64 = long long;` | [explicit-types](rules/explicit-types.md) |
| Indexing | Follow problem's natural indexing | [keep-indexing-consistent](rules/keep-indexing-consistent.md) |
| I/O | Disable sync, use `\n` | [fast-io](rules/fast-io.md) |
| Naming | `snake_case` for vars, `PascalCase` for structs | [naming](rules/naming.md) |
| Minimal | Avoid unnecessary variables, merge conditions | [minimal-code](rules/minimal-code.md) |
| Formatting | 4-space indent, K&R braces, no line compression | [formatting](rules/formatting.md) |
| Simplicity | Prefer simple data structures | [simplicity-first](rules/simplicity-first.md) |
| Memory | Use in-place operations | [in-place-operations](rules/in-place-operations.md) |
| Scope | Use block scopes for temporaries | [scope-control](rules/scope-control.md) |
| DFS | Use depth array, avoid parent parameter | [dfs-techniques](rules/dfs-techniques.md) |
| Recursion | Lambda + self pattern | [recursion](rules/recursion.md) |
| Structs | Constructor patterns, const correctness | [struct-patterns](rules/struct-patterns.md) |
| Operators | Overload patterns for custom types | [operator-overloading](rules/operator-overloading.md) |
| Helpers | chmax, ceilDiv, gcd, power, etc. | [helper-functions](rules/helper-functions.md) |
| DP | Use `vector`, never `memset` | [dp-patterns](rules/dp-patterns.md) |
| Modern C++ | CTAD, structured binding, C++20 features | [modern-cpp-features](rules/modern-cpp-features.md) |

## Code Template

```cpp
#include <bits/stdc++.h>

using i64 = long long;

void solve() {
    int n;
    std::cin >> n;

    std::vector<int> a(n);
    for (int i = 0; i < n; i++) {
        std::cin >> a[i];
    }

    std::cout << ans << "\n";
}

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    int t;
    std::cin >> t;

    while (t--) {
        solve();
    }

    return 0;
}
```

## Red Flags - STOP

| Anti-pattern | Correct approach |
|--------------|------------------|
| `using namespace std;` | Use `std::` prefix |
| `int a[100005];` global | `std::vector<int> a(n);` in solve() |
| `#define int long long` | `using i64 = long long;` |
| `for (int i = 1; i <= n; i++)` | `for (int i = 0; i < n; i++)` **OR** keep problem's indexing |
| `void dfs(int u, int p)` global | Lambda with self capture |
| `std::endl` | Use `"\n"` |
| `if (x) do_something();` | Always use braces |
| `a && b` logical operators | Use `and`, `or`, `not` keywords |
| **Over-engineered** HLD + segment tree | Use binary lifting for simple path queries |
| **Creating** `e1, e2` containers | Use `vis` boolean array |
| **Converting** 1-indexed to 0-indexed | Keep original indexing |
| **Expanding** boolean logic into verbose if-else | Merge conditions |
| **Introducing** unnecessary intermediate variables | Use direct formulas |
| **Over-semantic** local variable names | Use `x, y, l, r` for short-lived vars |
| **Passing** parent in DFS | Use depth array to check visited |
| **Explicit** template parameters | Use CTAD where possible |
| **Large** arrays at function scope | Use block scopes `{}` for temporaries |
| **String** without `reserve()` | Preallocate for known size |
| **Variable** assignment instead of `swap()` | Use O(1) swap |
| **Creating** struct for simple index-value sort | Use `std::iota` + lambda |
| **Loop** variable initialized outside for | Initialize in for header: `for (int i = 0, j = 0; ...)` |
| **Output** with trailing space handling | Use `" \n"[i == n - 1]` trick |

## Full Documentation

For complete details on all rules: [AGENTS.md](AGENTS.md)

---

<CRITICAL>

## FINAL CHECKPOINT - BEFORE OUTPUTTING CODE

**You MUST verify ALL items below before showing code to user:**

```
□ Read relevant rule files (naming.md, formatting.md, etc.)
□ Checked against Red Flags table
□ No `using namespace std;`
□ No global arrays
□ Used `i64` for long long
□ Used `and`/`or`/`not` keywords
□ Used `std::` prefix throughout
□ 4-space indent, K&R braces
□ No compressed lines
□ Used `"\n"` not `std::endl`
□ Temporary arrays in block scopes
□ String operations use `reserve()` and `swap()`
□ Symmetric comparison patterns
□ Uppercase temp array names (S, T)
□ Use iota + lambda for sorting with indices
□ Loop vars in for header when scope permits
□ Output uses " \n"[i == n - 1] trick
```

**If ANY item fails, fix before output. This is non-negotiable.**

</CRITICAL>
