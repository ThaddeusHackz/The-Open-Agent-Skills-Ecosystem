---
name: lark-mermaid-text-drawing
description: 该技能通过 lark-cli 创建、检查、替换、批量转换和审计飞书/Lark Docx 云文档中的 Mermaid“文本绘图”插件块。当用户提到飞书文本绘图、Mermaid 文本绘图、codeChart、把 Mermaid 代码块转换为插件块，或检查文档是否残留 Mermaid 代码块时使用。
version: 1.0.0
---

# 飞书 Mermaid 文本绘图

该技能操作飞书“文本绘图”插件块。用户明确要求文本绘图时，不得改用画板、图片或普通 Mermaid 代码块。

## 运行前提

1. 将本 `SKILL.md` 所在目录作为工作目录。所有脚本路径均相对于该目录，不依赖 Codex、仓库名称或用户主目录。
2. 环境必须提供 Python 3.9 或更高版本和 `lark-cli`。先执行以下只读自检：

   ```bash
   python3 scripts/lark_mermaid_text_drawing.py --help
   lark-cli auth status --json --verify
   ```

3. 如果命令不存在、登录过期或权限不足，停止操作并向用户说明缺失项，不得自动安装软件或绕过认证。
4. 只读操作需要 Docx 读取权限；写操作需要 Docx 写入权限，并使用当前已登录的用户身份。
5. 只有用户明确要求“创建、插入、转换、替换、更新”文档时，才执行带 `--yes` 的写命令。用户只说“查看、分析、检查、审计、测试”时，保持只读或先输出 dry-run 计划。

## 解析文档

- Docx token：直接作为脚本的 `--doc` 参数。
- `/docx/` URL：提取路径中的 Docx token。
- `/wiki/` URL：先用 `lark-cli wiki +node-get --as user --format json` 解析节点。仅当 `data.obj_type` 为 `docx` 时，才把 `data.obj_token` 作为 `--doc` 参数。
- Wiki 解析失败、无权限或节点不是 Docx 时停止；不得把 Wiki token 当成 Docx token。
- 不在答复、日志或提交内容中回显完整文档 token。脚本默认只输出不可逆的文档指纹。
- Docx token 是资源标识，不是登录凭证，但 `lark-cli` 会按官方命令格式把它放入 API 路径或 `--doc` 进程参数。不要在不可信的共享主机上运行；本技能无法消除操作系统进程审计对此类参数的记录。

## 标准工作流

### 批量转换

用户要求把文档内 Mermaid 代码块转换成文本绘图时：

1. 解析真实 Docx token。
2. 执行一次不带 `--yes` 的 `convert-code-blocks`，检查 dry-run 的候选数量、父块和位置。
3. 仅在用户已明确授权写入且候选数量符合预期时，对完全相同的参数追加一次 `--yes`。
4. 脚本按“读取全部层级 → 创建全部文本绘图 → 回读校验 → 删除原代码块 → 扫描残留”的顺序完成事务式转换。
5. 只有退出码为 `0`、输出包含 `result: success`，并且随后执行 `audit` 也返回退出码 `0` 时，才报告完成。

`converted: 0` 只表示没有识别到候选块，不能证明真实转换链路成功。

### 创建和替换

- `create`：必须使用本地 UTF-8 Mermaid 文件，通过 `--mermaid-file` 读取；先 dry-run，确认父块和插入位置后再追加 `--yes`。
- `replace`：先用 `list` 确认目标块，再传 `--block-id`；新块回读验证成功前，脚本不会删除旧块。
- Mermaid 内容通过标准输入传给 `lark-cli`，不会放入进程命令行参数。

### 检查和审计

- `list`：列出文本绘图块。默认只输出图类型、字符数和摘要，不输出 Mermaid 原文。
- `audit`：检查插件记录、主题、视图及 Mermaid 代码块残留；预期数量明确时使用 `--expected`。
- 只有用户明确要求查看 Mermaid 源码时，才对 `list` 或 `audit` 使用 `--include-source`，并避免把输出写入公共日志。

## 命令发现

通过帮助信息获得完整且可执行的参数说明，不在技能文件中保存真实 token 或伪造占位符：

```bash
python3 scripts/lark_mermaid_text_drawing.py convert-code-blocks --help
python3 scripts/lark_mermaid_text_drawing.py create --help
python3 scripts/lark_mermaid_text_drawing.py replace --help
python3 scripts/lark_mermaid_text_drawing.py list --help
python3 scripts/lark_mermaid_text_drawing.py audit --help
```

## 组件类型选择

按以下优先级确定文本绘图组件类型：

1. 用户或环境明确提供的 `--component-type-id`；
2. 当前文档中唯一的 Mermaid 文本绘图组件类型；
3. 已知兼容默认值 `blk_631fefbbae02400430b8f9f4`。

若自动发现多个类型，必须停止并请用户确定，不得猜测。默认值不是凭证，但可能随飞书租户或插件版本变化；创建后必须回读验证。

## Mermaid 兼容规则

- 流程图优先使用 `flowchart TD` 或 `flowchart LR`，时序图使用 `sequenceDiagram`。
- 节点 ID 只使用 ASCII 字母、数字和下划线；中文放在双引号标签中。
- 边文字使用双引号；标签含括号、冒号、斜杠或空格时加双引号。
- 一行只写一个节点或一条连线；避免 HTML、图标、Markdown 富文本、自定义 CSS、点击事件和实验性语法。
- 不确定插件支持的 Mermaid 版本时，把实验性图类型改写为流程图。
- 不把 Markdown 围栏写入插件记录；脚本会移除完整代码围栏、BOM 和多余首尾空白。

## 失败与恢复

- 新块回读验证成功前绝不删除原块；批量转换中所有新块验证成功前不删除任何原块。
- 删除结果不确定时，脚本回读实际状态。若部分原块已删除，则保留对应新块以避免内容丢失，并输出残留块 ID。
- 返回 `ok: false`、非零退出码或残留块 ID 时，报告准确错误和可恢复状态，不得盲目重试写命令。
- 不使用 `docs +whiteboard-update`；它操作飞书画板，不是文本绘图插件。
- 不修改 `lark-cli` 配置、不读取无关凭证、不将用户文档内容发送到飞书以外的服务。

## 发布前验证

发布新版本前必须提升 `version`，并完成以下检查：

```bash
python3 -m py_compile scripts/lark_mermaid_text_drawing.py
python3 scripts/lark_mermaid_text_drawing.py --help
```

还需确认目录可独立复制、`SKILL.md` 不包含待办项或真实凭证，并在受控文档中完成一次“dry-run → 转换 → audit”的前向验证。

## 版本历史

- `1.0.0`：首个可独立发布的 Qoder Skill；加入批量转换闭环、默认输出脱敏、stdin 传输 Mermaid 源码及失败恢复验证。
