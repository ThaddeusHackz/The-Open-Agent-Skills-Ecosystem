---
name: sync-fe-spec
description: 当产品发布新版本时，自动对比变更并增量更新前端Spec文件（spec.md、tasks.md）。在产品Changelog更新后使用，解决前端Spec与产品需求脱节的问题。
---

# 前端 Spec 增量同步

读取产品最新 Changelog 和 Demo，对比已有前端 Spec，生成增量更新，确保前端实现规格与产品需求保持同步。

## 触发场景

- 产品发布新版本（新的 Changelog.md 出现）
- 产品 Demo 有视觉/交互变更
- 后端 API 契约有变更
- 用户主动要求同步前端 spec

## 前置条件

- 产品已更新 `product-project/v{version}/Changelog.md`
- 前端已有 `fe-project/mcp-market-fe-project/specs/{feature}/` 目录（如果没有，先用本流程创建初始版本）

## 执行流程

### Step 1: 识别变更源

1. 查找最新的产品版本目录：
   ```
   product-project/v{最新日期}-{版本号}/
   ```
2. 读取 `Changelog.md`，提取变更项列表
3. 如果有产品 spec：读取 `specs/{feature}/spec.md`
4. 如果有后端 spec：读取 `backend-project/specs/{feature}/api-doc.md`

### Step 2: 对比现有前端 Spec

1. 读取当前前端 spec：
   ```
   fe-project/mcp-market-fe-project/specs/{feature}/spec.md
   fe-project/mcp-market-fe-project/specs/{feature}/tasks.md
   ```
2. 逐条对比 Changelog 中的变更项与现有 spec 的覆盖情况
3. 分类为：
   - **新增**：Changelog 中提到但前端 spec 未覆盖的功能
   - **修改**：已有功能但参数/交互/视觉发生变更
   - **删除**：Changelog 明确标注删除的功能

### Step 3: 生成增量更新

#### 更新 spec.md

- 新增的 User Story 追加到对应章节
- 修改的 User Story 更新内容并标注 `[CHANGED: {日期}]`
- 删除的功能标注 `[DEPRECATED: {日期}]` 但保留记录

#### 更新 tasks.md

- 新增任务格式：`- [ ] [NEW] T{序号} {描述}`
- 修改任务格式：`- [ ] [CHANGED] T{序号} {描述}（原: {旧描述}）`
- 删除任务格式：`- [x] [DELETED] T{序号} {描述}`
- 已完成任务保持 `[x]` 不变

#### 更新 api-contracts.md（如果后端有变更）

- 新增接口追加
- 修改接口更新参数/响应格式
- 标注变更日期

### Step 4: 更新 component-map.md（如果有新页面/组件）

- 新增页面/区块映射追加到表格
- 标注 `[NEW]`

### Step 5: 触发视觉更新（可选）

如果 Changelog 包含视觉相关变更（关键词：样式、颜色、布局、字号、间距、渐变、动画），提示用户运行 `/extract-demo-visual` 更新视觉参考。

### Step 6: 输出变更摘要

在控制台输出本次同步的变更摘要：

```
## Spec 同步完成

### 变更统计
- 新增: {n} 个 User Story, {m} 个任务
- 修改: {n} 个 User Story, {m} 个任务
- 删除: {n} 个功能

### 更新文件
- [x] spec.md — {新增/修改/无变化}
- [x] tasks.md — {新增 N 个任务}
- [ ] api-contracts.md — {无变化/需更新}
- [ ] component-map.md — {无变化/新增 N 个映射}
- [ ] visual-reference.md — {建议运行 /extract-demo-visual}
```

## 首次使用（无已有 spec）

如果 `fe-project/mcp-market-fe-project/specs/` 目录不存在，执行初始化流程：

1. 创建目录结构
2. 从产品 spec 派生前端 spec.md（聚焦技术实现细节）
3. 从产品 tasks.md 派生前端 tasks.md（仅保留前端相关任务）
4. 创建空的 component-map.md 和 api-contracts.md 模板
5. 提示用户运行 `/extract-demo-visual`

## 输出物

- 更新后的 `spec.md`
- 更新后的 `tasks.md`
- 更新后的 `api-contracts.md`（如适用）
- 更新后的 `component-map.md`（如适用）
- 变更摘要（控制台输出）

## 注意事项

- 永远不全量覆盖已有文件，仅增量修改
- 已完成的任务（[x]）不应被意外清除
- 保留文件中的注释和自定义内容
- 如果产品变更与后端API有关，检查后端 api-doc.md 是否有对应更新
- 版本号追踪：spec.md 顶部应标注"最后同步版本"

