---
name: commit-in-batches
description: Automatically analyze staged/unstaged changes, group changes into atomic batches by concerns/types, and commit according to the standard emoji + type + module git commit convention. Triggered by `/commit`, "commit", "提交", or natural language.
---

# Git 自动化与原子化规范提交技能 (Git Commit Skill)

专门用于检查当前 Git 仓库工作区、暂存区及未跟踪变动，按关注点/模块拆解分批，并严格遵循自定义的 Rich Emoji + Type + Module 规范生成精准、专业的提交记录。

---

## 触发方式

- `/commit`
- `/commit [提示信息/模块说明]`
- 自然语言触发：“提交代码”、“commit”、“帮我提交当前修改”、“分批提交”

---

## 执行步骤与核心规则

严格按照以下流水线执行：

### 1. 检查当前工作区状态
并行执行以下命令分析当前上下文：
```bash
git status
git diff
git log -n 5 --oneline
```
- 如果工作区完全干净（无任何待提交或未跟踪文件），直接礼貌提示用户并结束。

### 2. 原子化分批规划 (Atomic / Batched Commits)
- 仔细审查所有修改和未跟踪文件。
- **严禁一股脑一次性提交**：如果工作区修改包含多个不同关注点、模块或方向的变动（例如：既有业务逻辑调整/新特性，又有构建配置/依赖修改，或是重构与修复混杂），**必须按逻辑变动的关注点及 Type 分类进行拆解分批**。
- 将相互关联的文件规划至同一批次，确保每个提交记录的 Type、Module 与目的高度统一。
- 若所有改动纯属同一逻辑范围，则作为单一批次提交。

### 3. 逐批生成提交信息并执行 Commit
对于规划好的每个批次：

#### 格式规范模板：
`<emoji><Type>:[<Module/Component>] <Description>`

#### Emoji 与 Type 分类推荐：
- **功能与特性 (Features & Capabilities)**：
  - ✨ `Feat`：新功能或核心特性开发
  - 🚀 `Update`：功能增强、迭代或发布
  - 🍱 `Sign` / `Asset`：签名、plist 配置、资源资产文件、哈希变更
  - 💄 `UI`：用户界面、视觉样式、布局调整
  - 🔌 `Plugin`：插件、驱动、外部硬件交互
- **修复与防护 (Fixes & Stability)**：
  - 🔧 `Fix`：一般 Bug 修复、缺陷修复或小补丁
  - 🐛 `Bug`：边界情况修复、缺陷排查
  - 🚑 `Hotfix`：关键紧急修复
  - 🛡️ `Guard`：防御性检查、pcall 保护、nil/空指针防护
- **维护与重构 (Maintenance & Housekeeping)**：
  - ⚙️ `Chore`：日常构建维护、辅助配置、琐碎微调
  - ♻️ `Refactor`：代码重构（不改变现有外部功能行为）
  - 🎨 `Format`：代码格式化、缩进、代码风格整理
  - 🔥 `Clean`：清理死代码、无用废弃注释
  - 🛑 `Disable`：临时禁用或跳过测试用例/功能
  - 📦 `Build`：依赖管理、构建脚本、打包打包流程
  - ⏪ `Revert`：撤销历史提交
- **测试、文档与诊断 (Testing, Docs & Diagnostics)**：
  - 🧪 `Test`：单元测试、集成测试、覆盖率测试
  - 📝 `Docs`：文档撰写、README 更新、说明更新
  - ⚡️ `Perf`：性能调优、速度加速、UPH 优化
  - 📡 `Network`：网络通信、TCP/UDP/WebSocket、RTSP/流媒体
  - 🔒 `Sec`：安全加固、鉴权认证、权限调整
  - 📈 `Telemetry`：数据埋点、监控上报、性能指标追踪

#### Description 撰写要求：
- 使用精准、简洁的地道英文描述本次提交的核心变动与目的。
- 首字母大写，末尾不加句号。
- 如果用户在命令参数中提供了特定的描述或上下文线索，充分融合到相关批次描述中。

#### 暂存与提交：
- 仅暂存归属于当前批次的文件：
  ```bash
  git add <file1> <file2>...
  git commit -m "<emoji><Type>:[<Module>] <Description>"
  ```

### 4. 验证与结果输出
- 循环直至所有规划批次完成，再次执行 `git status` 确保工作树干净。
- 清晰列出本次操作创建的所有提交哈希（commit hash）与提交说明（commit message）。
