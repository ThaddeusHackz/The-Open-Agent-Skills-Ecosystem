---
name: auto-test-generator
description: 为 OpenClaw 技能自动生成基础单元/集成测试，提升代码质量并防止回归问题。
---

# Auto Test Generator

Automatically generate basic unit/integration tests for OpenClaw skills.
Use this to improve code quality and prevent regressions during evolution.

## Usage

```bash
node skills/auto-test-generator/index.js <skill-name>
```

## How It Works

1. Scans the target skill directory.
2. Analyzes `index.js` for exports.
3. Generates a `test.js` file with basic assertions (module loads, --help works).
4. Runs the generated test immediately.

## Example

```bash
node skills/auto-test-generator/index.js skill-health-monitor
```

Output:
- Creates `skills/skill-health-monitor/test.js`
- Runs it
- Reports success/failure
