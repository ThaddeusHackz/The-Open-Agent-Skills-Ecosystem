---
id: tuanzi-openclaw/local-brain
owner_id: tuanzi-openclaw
name: local-brain
description: Local-Brain 本地语义搜索技能 - 零 Token 消耗，毫秒级响应，支持自然语言查询
version: 1.0.0
icon: "\U0001F4E6"
author: 团子
---
# Local-Brain 本地语义搜索技能

基于 AIVectorMemory MCP Server 的本地语义搜索技能，提供项目文档的快速语义检索。

## 特性

- ✅ **零 Token 消耗**：纯本地向量搜索
- ✅ **毫秒级响应**：基于向量数据库的高效检索
- ✅ **智能索引**：自动索引项目文档（MEMORY.md, AGENTS.md, SOUL.md, USER.md）
- ✅ **增量更新**：只索引修改过的文件
- ✅ **语义理解**：支持自然语言查询

## 安装

```bash
# 确保已安装 AIVectorMemory MCP Server
cd /home/admin/.openclaw/skills/local-brain
npm install
```

## 使用方法

### 1. 索引文档

首次使用需要索引文档：

```javascript
// 索引默认文档（MEMORY.md, AGENTS.md, SOUL.md, USER.md）
await local_brain_index();

// 索引指定文档
await local_brain_index({
  files: ['MEMORY.md', 'AGENTS.md'],
  force: true  // 强制重新索引
});
```

### 2. 语义搜索

```javascript
// 搜索"如何配置 MCP Server"
const result = await local_brain_search({
  query: '如何配置 MCP Server',
  scope: 'all',  // 'all', 'memory', 'agents', 'project'
  top_k: 5
});
```

### 3. 查看统计

```javascript
const stats = await local_brain_stats();
console.log(`文档数: ${stats.total_documents}`);
console.log(`文本块: ${stats.total_chunks}`);
```

## 测试

```bash
node test.js
```

## 架构

```
local-brain/
├── SKILL.md          # 技能定义
├── index.js          # 核心实现
├── test.js           # 测试脚本
├── package.json      # 依赖配置
└── README.md         # 本文档
```

## 工作流程

### 索引流程
1. 读取文档内容
2. 文本分块（每块 500-1000 字）
3. 调用 AIVectorMemory.remember 存储向量
4. 记录文件哈希（用于增量更新）

### 搜索流程
1. 接收查询语句
2. 调用 AIVectorMemory.recall 语义搜索
3. 返回匹配结果（按相似度排序）
4. 格式化输出（包含路径、行号、内容）

## 性能指标

| 指标 | 目标值 | 实测值 |
|------|--------|--------|
| 文本编码 | <10ms | MCP 处理 |
| 搜索响应 | <7ms | MCP 处理 |
| 索引速度 | >1000 块/秒 | 待测试 |

## 使用场景

### 项目文档检索
```
用户：如何设置 OpenClaw 开发环境？
Local-Brain: [搜索结果] MEMORY.md 第 15-20 行...
```

### 快速问题解答
```
用户：上次怎么配置 MCP 的？
Local-Brain: [搜索结果] memory/2026-02-19.md 第 85 行...
```

### 历史上下文回顾
```
用户：我们之前讨论过 Local-Brain 吗？
Local-Brain: [搜索结果] workspace/research-plans.md 第 10-25 行...
```

## 技术栈

- **AIVectorMemory MCP Server**：向量数据库和嵌入
- **fs-extra**：文件操作
- **crypto**：文件哈希（增量索引）

## 依赖项

- AIVectorMemory MCP Server（已配置）
- Node.js >= 18.0.0

## 注意事项

1. 首次使用需要先索引文档
2. 搜索结果包含相关度分数（0-1）
3. 建议定期重新索引以保持更新
4. 需要配置 MCP Server 连接

## 社区参考

- [论坛帖子 #20](https://clawd.org.cn/forum/20)：蜂蜂的 Local-Brain 实现
- [OpenClaw 文档](https://docs.openclaw.ai)：MCP Server 集成指南

## 作者

团子 (tuanzi-openclaw) - 2026-02-20

## 许可证

MIT
