---
name: deity-agent-builder
description: |
  帮助使用 Deity TSX 框架构建 AI Agent。支持创建 Agent 组件、工作流编排、
  工具集成、LLM 适配器、测试验证等完整开发流程。
  触发词：deity, agent, workflow, 构建agent, 创建工作流, deity框架
---

# Deity Agent Builder — 构建指南

> 本技能帮助你使用 Deity TSX 框架快速、正确地构建 AI Agent 和工作流。

---

## 快速决策表

根据用户意图，跳转到对应步骤：

| 用户意图 | 起始步骤 | 关键模板 |
|---------|---------|---------|
| 从零开始建项目 | Step 1 → Step 2 | `project-setup.md` → `agent-*.md` |
| 创建简单 Agent | Step 2 | `agent-simple.md` |
| Agent 需要使用工具 | Step 2 → Step 4 | `agent-with-tools.md` |
| 创建完整 Agent（含验证、重试） | Step 2 | `agent-full.md` |
| 编排多 Agent 工作流 | Step 3 | `workflow-sequential.md` / `workflow-complex.md` |
| 自定义工具 | Step 4 | `tool-custom.md` |
| 接入 LLM（适配器） | Step 5 | `adapter-skeleton.md` |
| 测试 Agent | Step 6 | 内联指导 |
| 了解内置工具 | 参考 | `tools-reference.md` |
| 查 API 类型签名 | 参考 | `api-quick-ref.md` |
| 学习最佳实践 | 参考 | `patterns.md` |

---

## Step 1: 项目设置

**问用户：** 是新项目还是已有项目？

- **新项目** → 参考 [project-setup.md](./templates/project-setup.md) 创建完整项目结构
- **已有项目** → 确认已安装 `@limo-labs/deity` 和 `@limo-labs/deity-tools`

**关键检查：**
- `tsconfig.json` 中 `jsx: "react-jsx"` 和 `jsxImportSource: "@limo-labs/deity"`
- TypeScript `strict: true`
- `moduleResolution: "bundler"` 或 `"NodeNext"`

---

## Step 2: 定义 Agent

**根据复杂度选择模板：**

| 需求 | 模板 | 关键组件 |
|-----|------|---------|
| 最简单：提问 → 得到结构化回答 | [agent-simple.md](./templates/agent-simple.md) | `Prompt` + `Result` |
| 需要工具（文件、搜索等） | [agent-with-tools.md](./templates/agent-with-tools.md) | `Tools` + `Prompt` + `Result` |
| 完整：含观测、验证、重试 | [agent-full.md](./templates/agent-full.md) | 全部组件 |

**Agent 组件子节点顺序（必须遵循）：**
```
<Agent>
  <Tools>       ← 可选：工具定义
  <Prompt>      ← 必需：系统提示 + 用户提示
    <System>
    <User>
  <Observe>     ← 可选：LLM 执行后提取指标
  <Result>      ← 推荐：结构化输出提取
  <Validate>    ← 可选：语义验证规则
  <Retry>       ← 可选：重试策略
</Agent>
```

**核心原则：**
1. 每个 Agent 必须有 `id`、`input`（Zod schema）、`output`（Zod schema）
2. `<Result>` 的提取函数签名：`(ctx, llmResult, observed) => Output`
3. `<Validate>` 返回 `{ rules: [{ check: boolean, error: string }] }`
4. Agent 函数组件接受 props，返回 `AgentNode<I, O>`

---

## Step 3: 编排工作流

**根据需求选择模板：**

| 需求 | 模板 | 核心组件 |
|-----|------|---------|
| 多个 Agent 按顺序执行 | [workflow-sequential.md](./templates/workflow-sequential.md) | `Sequence` |
| 条件分支 / 并行 / 循环 | [workflow-complex.md](./templates/workflow-complex.md) | `Conditional` / `Parallel` / `Loop` / `ForEach` |

**数据流规则：**
- Agent A 的输出通过 `ctx.getOutput<TypeA>('agent-a-id')` 在后续 Agent 中访问
- `ForEach` 的 `items` 可以是函数 `(ctx) => ctx.getOutput('planner').tasks`
- `itemMode="property"` + `itemKey="task"` → 每个 item 注入为 `ctx.inputs.task`

**工作流组件层次：**
```
<Workflow>           ← 根容器：name, defaultModel, enhancements
  <Sequence>         ← 顺序执行
    <AgentA />
    <Parallel>       ← 并发执行
      <AgentB />
      <AgentC />
    </Parallel>
    <Conditional>    ← 条件分支
      <TrueBranch />
      <FalseBranch />
    </Conditional>
    <ForEach>        ← 动态迭代
      <AgentD />
    </ForEach>
    <Loop>           ← 固定次数循环
      <AgentE />
    </Loop>
  </Sequence>
</Workflow>
```

---

## Step 4: 添加工具

**决策：内置工具 vs 自定义工具？**

### 内置工具（来自 `@limo-labs/deity-tools`）

直接作为 JSX 组件使用。详细列表见 [tools-reference.md](./reference/tools-reference.md)。

```tsx
import { FileList, FileRead, MemoryStore, WebSearch } from '@limo-labs/deity-tools';
import type { ToolConfig } from '@limo-labs/deity-tools';

const config: ToolConfig = { workspaceRoot: '/path/to/project' };

<Tools>
  <FileList config={config} />    {/* 需要 ToolConfig */}
  <FileRead config={config} />
  <MemoryStore />                 {/* 无需配置 */}
  <WebSearch />
</Tools>
```

### 自定义工具

参考 [tool-custom.md](./templates/tool-custom.md)。两种方式：

1. **内联 `<Tool>` 组件** — 简单场景
2. **`ToolSpec` 对象 + `<ToolDef>`** — 可复用场景

---

## Step 5: LLM 适配器

**问用户：** 使用哪个 LLM 提供商？

参考 [adapter-skeleton.md](./templates/adapter-skeleton.md) 实现 `LLMAdapter` 接口。

**核心接口：**
```typescript
interface LLMAdapter {
  generate(
    messages: Message[],
    tools?: ToolSpec[],
    config?: GenerationConfig,
    ctx?: ExecutionContext
  ): Promise<LLMResponse>;
}
```

**关键点：**
- 必须处理 `tools` 参数（转为 provider SDK 格式或使用 prompt injection）
- 必须返回 `toolCalls` 数组（如果 LLM 返回了工具调用）
- `config.nativeToolCalling` 区分原生工具调用 vs prompt-based

---

## Step 6: 测试 Agent

**无需真实 LLM 即可测试的函数：**

```typescript
import {
  testFullAgent,        // 完整管线测试
  renderPromptPreview,  // 预览生成的 prompt
  dryRunValidate,       // 测试验证逻辑
  runObserve,           // 测试 Observe 逻辑
  testExtractOutput,    // 测试 Result 提取逻辑
  preflight             // 静态检查 Agent 定义
} from '@limo-labs/deity';
```

### 常用测试模式

```typescript
// 1. 预检查 — 静态验证 Agent 定义是否正确
const check = await preflight(myAgent);
console.log(check.passed, check.errors, check.warnings);

// 2. Prompt 预览 — 查看发送给 LLM 的消息
const preview = await renderPromptPreview(myAgent, {
  inputs: { query: 'test input' }
});
console.log(preview.snapshot);  // 格式化的 prompt 预览

// 3. 完整管线测试 — 模拟 LLM 返回，测试整条管线
const result = await testFullAgent(myAgent, {
  inputs: { query: 'test' },
  llmResult: {
    response: { content: '{"answer": "test result"}', toolCalls: [] },
    messages: [],
    rounds: 1,
    toolCallsExecuted: 0,
    errors: []
  }
});
console.log(result.output);      // 提取的输出
console.log(result.validation);  // 验证结果

// 4. 单独测试验证逻辑
const validation = await dryRunValidate(myAgent, {
  output: { answer: '' },  // 故意传入无效输出
  inputs: { query: 'test' }
});
console.log(validation.valid);  // false
```

---

## 必须遵守的规则

1. **所有导入来自两个包**：`@limo-labs/deity`（核心）和 `@limo-labs/deity-tools`（工具）
2. **Agent 函数返回类型必须断言**：`return (...) as AgentNode<I, O>`
3. **Zod schema 定义在 Agent 函数外部**（`const` 级别）
4. **`<Result>` 函数签名是 3 参数**：`(ctx, llmResult, observed) => Output`
5. **`<Validate>` 返回 `{ rules }` 对象**，不是 `ValidationResult`
6. **`<System>` 加载文件用 async 函数子节点或 `source="file:..."`**
7. **`<ForEach>` 的 `items` 用函数形式** 才能访问前序 Agent 输出
8. **`loopValidator` 在 LLM 循环内执行**，用于控制工具调用循环何时停止
9. **`extractLastToolResult` 的 `unwrap: true`** 自动解包 `{ success, data }` → 返回 `data`
10. **工具的 `execute` 返回 `ToolResult<T>`**：`{ success: true, data: ... }` 或 `{ success: false, error: '...' }`

---

## 常见问题排查

| 症状 | 原因 | 修复 |
|-----|------|-----|
| `Cannot find module '@limo-labs/deity'` | 未安装或 tsconfig 错误 | 检查 `npm ls @limo-labs/deity`，确认 `moduleResolution` |
| Agent 返回类型错误 | 缺少 `as AgentNode<I, O>` 断言 | 在 return 语句末尾加类型断言 |
| `<System>` 文件加载失败 | 路径错误或文件不存在 | 检查相对路径，使用 `required` prop 启用 fail-fast |
| `extractLastToolResult` 返回 `null` | 工具未被 LLM 调用 | 检查工具 `description` 是否清晰，或使用 `required: false` |
| `<Validate>` 不生效 | 返回格式错误 | 必须返回 `{ rules: [{ check, error }] }`，不是 `{ valid, errors }` |
| ForEach 中 `ctx.inputs.task` 是 `undefined` | `itemKey` 不匹配 | 确认 `itemKey` 值与访问的属性名一致 |
| LLM 不调用工具 | 工具 description 不够清晰 | 改善 description，在 System prompt 中明确要求使用工具 |
| 循环超时 | `loopConfig.timeout` 太短 | 增加 timeout，或设置合理的 `maxToolRounds` |

---

## 参考文件

- [API 快速参考](./reference/api-quick-ref.md) — 完整类型签名
- [模式与最佳实践](./reference/patterns.md) — 生产级模式 + 反模式
- [内置工具参考](./reference/tools-reference.md) — 所有内置工具详细说明
