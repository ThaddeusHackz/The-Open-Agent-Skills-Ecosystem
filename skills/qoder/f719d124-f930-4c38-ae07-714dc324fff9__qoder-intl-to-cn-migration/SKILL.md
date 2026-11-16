---
name: qoder-intl-to-cn-migration
description: '在同一台 Windows 电脑上把 Qoder Desktop 国际版（~/.qoder + %APPDATA%\com.qoder.app.stable）的本地数据迁移到 Qoder 国内版/Qoder CN（~/.qoder-cn + %APPDATA%\com.qodercn.app.stable）：工作区列表、历史会话与消息、记忆 memories、技能/Agent、插件开关、本地自动化、技能进化建议；并为云端绑定项（QMind 知识库、云端自动化、MCP OAuth）给出重建清单。用于"国际版迁移国内版""Qoder 换国内版数据怎么搬""国内版工作区/会话是空的""迁移后还缺什么"等请求。'
---

# Qoder 国际版 → 国内版 数据迁移

## 关键事实（先读）

- 两版**账号与云端完全隔离**，本地数据分两处：`~/.qoder[-cn]/`（会话文件、记忆、技能、设置）和 `%APPDATA%\com.qoder[cn].app.stable\main.sqlite`（**侧边栏工作区列表、会话索引、消息的唯一来源**）。只拷目录时国内版侧边栏仍为空，必须导入 main.sqlite；**不需要退出重登**。
- 国内版进程名是 `Qoder CN.exe`（有空格），按 `Qoder.exe`/`QoderCN.exe` 过滤会漏检。写 main.sqlite 前必须**完全退出国内版（含托盘）**，否则运行中的客户端会覆盖写入。
- 本 Skill 通常运行在**国际版**里（才能用 qmind MCP 读国际版云端知识库）；国际版不用关。
- 绝不迁移登录态与机器标识：`.auth`、`auth*.dat`、`.config.json`、`mcp-router.json`、`state.json`、`installation_id`、`umid-cache.json`、`qoder-data.v1*.json`、collaboration 凭据、MCP OAuth 凭据。完整取舍见 [references/data-map.md](references/data-map.md)。

## 流程

脚本：`scripts/qoder_migrate.py`（Python 3 标准库）。`files`/`db` 默认演练，加 `--apply` 才写入；演练的 db 在国内版库**副本**上执行。

1. **前置**：确认国内版已安装、已登录并启动过一次（否则无 `~/.qoder-cn`、无 main.sqlite）。
2. **审计**：`python scripts/qoder_migrate.py audit`
   向用户汇报：账号 id、目录缺口、缺失插件、各表缺口行数、云端项数量。
3. **文件同步**：先 `files` 演练，检查"覆盖"清单（国际版较新才覆盖；若用户已在国内版改过 MEMORY.md 等需提醒），确认后 `files --apply`。
   - memories 会同时写入 `memories/<国际版id前8位>` 与 `memories/<国内版id前8位>`，兼容国内版按任一前缀查找。
   - settings.json 只补 `enabledPlugins` 中国内版缺的键（国内版已有值优先），自动备份。
4. **数据库导入**：先 `db` 演练并汇报每表 +N 与孤儿会话检查；然后请用户**完全退出国内版**（用提问工具等待用户确认"已关闭"），再 `db --apply`。脚本检测到国内版进程仍在会中止（退出码 3）。
5. 请用户**启动国内版**，核对侧边栏工作区数量、任意老会话可打开、本地自动化在列。
6. **云端项**（无法本地迁移，交给用户在国内版重建）：
   - 云端自动化：`python scripts/qoder_migrate.py cloud` 导出到桌面 `Qoder国内版-云端自动化重建参数.md`（名称/cron/时区/完整提示词）。缓存为空时让用户在国际版打开一次「自动化」页再导。
   - QMind 知识库：用 qmind MCP（`list_notebooks` → `list_sources`）列出国际版各知识库的源文件名；在本机磁盘（桌面、文档、下载、企业微信/钉钉缓存目录、其它盘符）按文件名查找原件，复制到桌面 `<知识库名>-知识库源文件/`，并核对数量。让用户在国内版新建同名知识库并上传；找不到原件的逐一列出。
   - MCP OAuth（如 Postman）：在国内版重新授权，不要拷凭据（加密载荷与版本/账号绑定，拷过去不会被复用）。
   - 已安装插件：`audit` 列出的国内版缺失插件，到国内版插件市场安装；不要拷 `plugins/cache`。
7. **收尾汇报**：用表格列出 已迁移 / 刻意未迁移（原因）/ 需用户手动重建 三类，以及回滚点：`main.sqlite.bak-<时间戳>`、`settings.json.bak-<时间戳>`。

## 注意

- 可重复执行（`insert or ignore` + 只补缺失文件），用于增量同步迁移后国际版新产生的会话；但会复活用户在国内版里**硬删除**的会话，重跑前告知用户。
- 同根路径的工作区不会重复创建：国际版工作区与国内版已有工作区根路径相同时，会话改挂到国内版那条（保留国内版的命名）。
- 两版表结构列顺序可能不同，脚本按列名交集导入；某版独有列会在输出中标出。
- `chat_session_history_revisions`、`chat_session_search_segments` 显示 +0 是正常的：插入会话/消息时触发器已自动生成。
- 正在进行中的国际版会话可能少最后 1~2 条消息；迁移完成后在国内版继续工作即可。
- 回滚：退出国内版，把 `main.sqlite.bak-<时间戳>` 复制回 `main.sqlite`，并删除同目录下的 `main.sqlite-wal`、`main.sqlite-shm`。
- 非默认安装路径用 `--intl-home --cn-home --intl-roaming --cn-roaming` 指定。仅验证过 Windows。
