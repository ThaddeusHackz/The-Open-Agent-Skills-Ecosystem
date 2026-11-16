---
name: inkos
description: |
  AI 自主写小说系统。通过对话窗口直接驱动小说创作全流程：创建书籍、写章、审阅、修订、导出。

  当用户提到以下意图时触发：
  - 写小说、创作小说、开始写书、创建小说项目
  - 写下一章、继续写、续写、写新章节
  - 审阅章节、审核、通过草稿
  - 导出小说、导出 EPUB、导出 TXT
  - 查看写作状态、查看进度
  - 修改小说设定、改名、番外、同人
  - InkOS、inkos 相关操作
---

# InkOS — 对话式小说创作

通过 `inkos interact --json` 与 InkOS 交互，这是首选入口。

## 环境状态

- 已全局配置：provider=custom, model=modelroute, max-tokens=8192, lang=zh
- API 端点：`http://127.0.0.1:19000/proxy/llm`（QClaw 本地代理）
- 工作目录：`C:\Users\willc\.qclaw\workspace`（所有 inkos 项目在此创建）

## Windows 执行注意

InkOS 命令必须通过 `cmd /c` 调用（PowerShell 执行策略限制）：

```
cmd /c "inkos <command> [args]"
```

## 核心交互：inkos interact

**首选入口**，自然语言驱动一切操作：

```bash
cmd /c "inkos interact --json --message ""<自然语言指令>"""
```

支持的意图（15+种）：
- 写作：继续写、写下一章、换种风格写
- 修订：修改某章、把XX改掉、收紧节奏
- 审阅：审阅草稿、通过、驳回
- 管理：改名、创建新书、切换书籍
- 导出：导出 TXT / EPUB
- 查询：状态、进度、章节列表

返回 JSON 包含：request 解析、assistant 回复、execution state、pending decision、recent events。

**pending decision 不为空时**，必须将决策选项展示给用户，等待用户选择后再继续。

## 原子命令（备选，必要时使用）

### 项目管理

```bash
cmd /c "inkos init <项目名>"          # 初始化项目（cd 到 workspace 目录后执行）
cmd /c "inkos status"                # 查看状态
cmd /c "inkos doctor"                # 环境检查
```

### 书籍管理

```bash
cmd /c "inkos book create --title ""<书名>"" --genre <类型>"
# 类型：xuanhuan(玄幻) xianxia(仙侠) dushi(都市) kehuan(科幻) lishi(历史) junshi(军事) youxi(游戏) qita(其他)
cmd /c "inkos book list"             # 列出所有书
cmd /c "inkos book info <书ID>"      # 查看书详情
```

### 写作

```bash
cmd /c "inkos write next <书名>"      # 完整管线：草稿→审计→修订
cmd /c "inkos draft <书名>"          # 仅写草稿（不审计不修订）
cmd /c "inkos audit <书名> <章节>"   # 审计单章
cmd /c "inkos revise <书名> <章节>"  # 修订单章
```

### 审阅

```bash
cmd /c "inkos review list <书名>"         # 查看待审阅章节
cmd /c "inkos review approve <书名> <章节>"  # 通过单章
cmd /c "inkos review approve-all <书名>"    # 批量通过
cmd /c "inkos review reject <书名> <章节>"   # 驳回
```

### 导出

```bash
cmd /c "inkos export <书名>"              # 导出 TXT
cmd /c "inkos export <书名> --format epub"  # 导出 EPUB
```

### 其他

```bash
cmd /c "inkos detect <书名>"           # AI 痕迹检测
cmd /c "inkos style analyze <书名>"    # 文风分析
cmd /c "inkos fanfic <书名>"           # 同人创作工具
cmd /c "inkos analytics <书名>"        # 数据分析
```

## 工作流程

1. **首次使用**：用户说"开始写小说" → 用 interact 创建书 + 设定 → 写第一章
2. **日常写作**：用户说"写下一章" → `inkos interact --json --message "写下一章"`
3. **审阅流程**：写完后检查 pending decision → 展示给用户选择
4. **导出**：用户说"导出" → `inkos export <书名> --format epub`

## 关键规则

- 涉及书名、消息等中文内容时，用双引号包裹，内部双引号转义为 `""`
- 优先使用 `inkos interact`，只在需要精确控制时用原子命令
- interact 返回的 pending decision 必须告知用户，不可自动决定
- 执行时间较长的命令（write next、export）设置较长 timeout（300s+）
