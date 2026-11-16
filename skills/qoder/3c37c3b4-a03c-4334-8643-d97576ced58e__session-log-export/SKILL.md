---
name: session-log-export
description: 把 Qoder 本地缓存的 Quest 会话日志(JSONL)导出为 conversation-log.md，落到对应需求 spec 目录的 session/ 子目录，作为可追溯、可分析的必须产出物。当用户要求"记录 session log"、"归档会话到 spec"、"导出会话日志"或需求收尾需要补齐 session/ 产出物时使用。
version: 1.0.0
---

# Session Log Export — Quest 会话日志归档

把 Qoder 本地缓存的 Quest 会话（JSONL）转换为 `conversation-log.md`，落到**对应需求 spec 文件夹的 `session/` 子目录**，对齐《端到端交付2.0》的 spec 产出物规范：

```
specs/{编号}-{需求名}/
├── spec.md
├── plan.md
├── tasks.md
├── check_reports/
└── session/                 (必须) Agent会话记录
    └── conversation-log.md
```

session log 三重职责：
1. **黑匣子回溯** — 交付物出问题时定位是物料缺陷 / 需求模糊 / 模型幻觉
2. **Loop 分析数据源** — 元数据表记录用户轮次 / 助手消息数，供后续统计分析
3. **产出物完整性** — session/ 与 check_reports/ 同级，是需求收尾的必须项

## 触发方式

- `/session-log-export <specDir>` — 导出当前 Quest 到指定 spec 目录
- `/session-log-export <taskId> <specDir>` — 导出指定历史 Quest
- `/session-log-export`（无参）— 列出候选 spec 目录 + 最近 10 个 Quest，让用户配对选择
- 自然语言："记录 session log"、"归档会话到 spec"、"导出会话日志"

可选标志：
- `--no-commit` — 只落盘不 commit
- `--force` — 同一 taskId 已归档时覆盖该 Session 区块
- `--all` — 存量补录模式，交互式把历史 Quest 逐个配对到既有 spec 目录

## 边界声明

- **只读** Qoder 缓存目录（`~/.qoder/cache/projects/`），绝不修改/删除缓存
- **只写** 目标 spec 目录下的 `session/` 子目录
- 自动脱敏后落盘（AK/SK、token、JWT、password、私钥等）
- commit 但**不 push**；main/master 分支上拒绝 commit

## 执行步骤

### Step 1: 定位 Qoder 缓存目录

```bash
ls -dt ~/.qoder/cache/projects/{当前workspace目录名}-*/conversation-history 2>/dev/null | head -1
```

- workspace 目录名取当前项目根目录的 basename（如 `busyming-mcp-service`）
- 多个 hash 目录时取 mtime 最新的一个
- 找不到时告知用户："未找到本项目的 Qoder 会话缓存"，终止

### Step 2: 确定要导出的 taskId

- 用户指定了 taskId → 直接使用，校验 `{cache}/conversation-history/{taskId}/{taskId}.jsonl` 存在
- 用户未指定 → 默认当前 Quest；若无法确定当前 taskId，列出最近 10 个供选择：

```bash
ls -t {cache}/conversation-history/*/*.jsonl | head -10
```

每个候选展示：taskId + mtime + 首条用户消息前 30 字（用下面命令提取）：

```bash
python3 -c "
import json,re,sys
for line in open(sys.argv[1]):
    obj=json.loads(line)
    if obj.get('role')!='user': continue
    for c in obj.get('message',{}).get('content',[]):
        m=re.search(r'<user_query>\s*(.*?)\s*</user_query>', c.get('text',''), re.S)
        if m: print(m.group(1)[:30].replace(chr(10),' ')); sys.exit()
" {jsonl路径}
```

### Step 3: 确定目标 spec 目录

- 用户指定了 specDir → 校验目录存在（应包含 spec.md 或至少是 specs/ 下的需求目录）
- 用户未指定 → 用 Glob `**/specs/*/spec.md` 发现项目内所有 spec 目录（覆盖 backend-project/specs/、fe-project/*/specs/、product-project/*/specs/），列出让用户选择
- 不允许自行猜测配对关系，配对必须由用户确认

### Step 4: 执行转换（含脱敏）

```bash
python3 .qoder/skills/session-log-export/assets/convert.py \
  --jsonl {jsonl路径} \
  --spec-dir {specDir} \
  --patterns .qoder/skills/session-log-export/assets/redact-patterns.txt
```

- exit 0：成功，脚本会输出轮次/消息数/脱敏项统计，转述给用户
- exit 2：该 taskId 已归档过 → 询问用户是否覆盖，确认后加 `--force` 重跑
- exit 1：报错（JSONL 不存在 / 无对话内容 / spec 目录不存在），把错误转述给用户

转换规则（脚本内置，无需干预）：
- 用户消息只保留 `<user_query>` 标签内的原始输入，系统注入内容全部过滤
- Qoder JSONL 只落盘文本块（无 tool_use/tool_result），因此日志为纯对话文本
- 同一 spec 多次 Quest 归档为同一 conversation-log.md 中的多个 `## Session: {taskId}` 区块，元数据表逐行累计

### Step 5: git 提交

1. `git branch --show-current` — 若为 main/master，**拒绝 commit**，提示用户切 feature 分支后重试（落盘结果保留）
2. 用户带了 `--no-commit` → 跳过本步
3. 否则：

```bash
git add {specDir}/session/
git commit -m "docs(session): 归档 Quest {taskId} 会话日志到 {spec目录名}"
```

4. **不执行 push** — 推送与 MR 流程由用户或 git-ops 技能完成

### Step 6: 结果汇报

向用户汇报：
- 落盘路径：`{specDir}/session/conversation-log.md`
- 统计：用户轮次 / 助手消息数 / 脱敏项数
- commit 状态（已提交的 commit id / 已跳过 / 因 main 分支被拒绝）

## 存量补录（--all 模式）

1. 列出缓存中全部 task JSONL（按 mtime 倒序）+ 各自首条用户消息摘要
2. 列出项目内全部 spec 目录
3. 逐个询问用户"这个 Quest 归到哪个 spec？"（可回答"跳过"）
4. 每确认一对就执行一次 Step 4，全部完成后统一执行一次 Step 5（单次 commit）

## 流程约定

每个 spec 需求收尾时执行一次 `/session-log-export <specDir>`，使 `session/` 成为与 `check_reports/` 同级的必须产出物。多次迭代的需求（多个 Quest）在每轮收尾时都追加归档一次。

## 注意事项

- Qoder 缓存属临时目录，重装/清缓存会丢失，重要会话应及时归档
- 项目路径变更会导致缓存 hash 目录变化，旧缓存不会自动迁移
- 脱敏为固定 regex 清单，无法保证 100% 覆盖；commit 前建议快速浏览一遍生成的 markdown
- 生成文件中的 Session 区块不要手工编辑，否则可能破坏追加/覆盖逻辑
