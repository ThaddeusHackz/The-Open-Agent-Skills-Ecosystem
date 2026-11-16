---
name: "create-doc-skill"
description: "Creates reusable documentation scraping skills from any documentation website URL. Analyzes site structure via web crawling, generates main-skill and sub-skill SKILL.md files with doc-mapping tables, and sets up cache_docs.py for on-demand HTML-to-Markdown caching. Use when the user wants to turn any documentation site into a JeeSite-style doc skill: 'create a doc skill for this site', 'make a doc scraper for ...', 'turn these docs into a skill'."
---

# 文档技能创建器

将任意文档站点转换为 JeeSite 风格的文档爬取 Skill。自动分析站点结构，生成主索引、子 Skill、缓存脚本。

## 前置条件

- 目标文档站点可公开访问（无需登录）
- 文档页面具有一致的 URL 结构（如 `/docs/xxx/`）
- 安装 Python 依赖：`pip install requests html2text`

## 创建流程

### 阶段 1：信息收集

向用户确认以下信息：

1. **项目名称**（英文小写+连字符）：如 `jeesite`、`my-framework`
2. **文档站点基础 URL**：如 `https://example.com/docs/`
3. **Skill 存放位置**：个人 (`~/.qoder/skills/`) 或项目 (`.qoder/skills/`)
4. **文档分区方式**：按功能模块 / 按导航菜单 / 按目录结构

如果用户未明确分区，使用 Firecrawl 或直接爬取分析站点：

```
用 firecrawl-map 或直接抓取首页，提取侧边栏/导航链接，
按一级导航项划分为不同的子 Skill。
```

### 阶段 2：站点结构分析

1. **获取页面列表**：爬取文档首页，提取侧边栏或导航中的所有文档链接
2. **划分 Skill 分区**：将链接按一级分类归组，每组创建一个子 Skill
3. **确定内容选择器**：打开一个具体文档页面，找到包裹正文内容的 HTML 容器（如 `<div class="theme-vdoing-content">`、`<article class="markdown">`、`<main>`）
4. **记录 permalink 模式**：确认 URL 如何映射到 permalink（如 `/docs/overview/` → `/overview/`）

### 阶段 3：生成文件

按以下步骤生成完整的 Skill 目录：

#### 3.1 创建目录结构

```
<skill-name>/
├── SKILL.md                          # 主索引文件
├── scripts/
│   ├── cache_docs.py                 # 按需缓存脚本
│   └── batch_cache.py                # 批量缓存脚本
├── references/
│   ├── <sub-skill-1>/
│   │   └── SKILL.md                  # 子 Skill 映射文件
│   ├── <sub-skill-2>/
│   │   └── SKILL.md
│   └── .cache/                       # 缓存目录（自动生成）
└── assets/                           # 可选：logo 等资源
```

#### 3.2 生成 cache_docs.py

复制 [templates/cache_docs.py](templates/cache_docs.py) 到 `scripts/cache_docs.py`，修改：

1. **DOCS_BASE_URL**（第 29 行附近）：设置为你的文档站点基础 URL
2. **CONTENT_SELECTORS**（第 36 行附近）：保留匹配目标站点的选择器，删除不匹配的
3. **CONTENT_CLEAN_PATTERNS**（第 50 行附近）：添加站点特有的需要清理的元素

验证脚本可用：
```bash
python3 scripts/cache_docs.py --skill <sub-skill> --permalink /test-permalink/
```

#### 3.3 生成 batch_cache.py

创建 `scripts/batch_cache.py`：
```python
#!/usr/bin/env python3
"""批量缓存所有文档"""
import sys, os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
from cache_docs import cache_page, discover_skills

def main():
    skills = discover_skills()
    total = success = fail = 0
    failed_docs = []
    for skill in skills:
        skill_name = skill["name"]
        docs = skill.get("documents", [])
        if not docs:
            continue
        print(f"\n{'='*60}\n  Skill: {skill_name} ({len(docs)} 篇)\n{'='*60}")
        for doc in docs:
            total += 1
            print(f"\n[{total}] {doc['title']}")
            result = cache_page(skill_name, doc["permalink"], force=False)
            if result:
                success += 1
            else:
                fail += 1
                failed_docs.append(f"{skill_name}:{doc['permalink']} ({doc['title']})")
    print(f"\n{'='*60}\n  缓存完成: 总计 {total} 篇, 成功 {success} 篇, 失败 {fail} 篇")
    if failed_docs:
        print("  失败列表:")
        for f in failed_docs:
            print(f"    - {f}")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
```

#### 3.4 生成主 SKILL.md

使用 [templates/main-skill.md](templates/main-skill.md) 模板，替换以下占位符：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{SKILL_NAME}}` | 主 Skill 名称 | `jeesite` |
| `{{SKILL_DESCRIPTION}}` | 一句话描述（含触发词） | `JeeSite快速开发平台文档总索引。Invoke when user asks about JeeSite documentation...` |
| `{{PROJECT_NAME}}` | 项目显示名 | `JeeSite` |
| `{{SKILLS_TABLE}}` | Markdown 表格，列出所有子 Skill | 见下方 |
| `{{ROUTING_TABLE}}` | 用户问题→Skill 的路由表 | 见下方 |
| `{{CROSS_SKILL_TABLE}}` | 跨 Skill 场景关联表 | 见下方 |

**SKILLS_TABLE 格式**：
```markdown
| Skill name     | 名称    | 说明   |
|----------------|---------|---------|
| <project-name> | <项目名> | <项目名> 平台文档总索引  |
| quick-start    | 快速了解    | 平台简介、架构特点等基础知识 |
| backend-dev    | 后端开发手册  | 安装部署、API、数据库等 |
| frontend       | 前端开发手册  | 组件、样式、路由等 |
```

**ROUTING_TABLE 格式**：
```markdown
| 用户问题方向 | 推荐Skill |
|-------------|-----------|
| 平台介绍、架构、技术选型 | quick-start |
| 安装部署、API、数据库 | backend-dev |
| 组件、样式、路由 | frontend |
```

**CROSS_SKILL_TABLE 格式**：
```markdown
| 场景 | 需要加载的 Skills |
|------|-------------------|
| 前后端权限控制 | backend-dev + frontend |
| 数据库 + API | backend-dev + quick-start |
```

#### 3.5 生成子 SKILL.md

为每个分区创建 `references/<sub-skill-name>/SKILL.md`，使用 [templates/sub-skill.md](templates/sub-skill.md) 模板，替换以下占位符：

| 占位符 | 说明 | 示例 |
|--------|------|------|
| `{{SKILL_NAME}}` | 子 Skill 名称 | `backend-dev` |
| `{{SKILL_DESCRIPTION}}` | 描述+触发词 | `检索后端开发文档（API、数据库、部署等）。Invoke when user asks about backend...` |
| `{{SKILL_TITLE}}` | 中文标题 | `后端开发手册` |
| `{{SKILL_OVERVIEW}}` | 概述段落 | `后端开发指南，包括安装部署、API、数据库等。` |
| `{{KEYWORDS}}` | 逗号分隔的关键词 | `安装、部署、API、数据库、Shiro、权限、工具类` |
| `{{TRIGGER_SCENARIOS}}` | 触发场景列表 | `- 如何安装\n- API怎么写\n- 数据库配置` |
| `{{DOC_MAPPING_TABLE}}` | 文档映射表行 | 见下方 |
| `{{FAQ_TABLE}}` | 常见问题映射表行 | 见下方 |

**DOC_MAPPING_TABLE 格式**（每行一篇文档）：
```markdown
| 平台简介 | 平台简介 | /overview/ | 平台介绍、核心优势。关键章节：平台介绍 | /feature/ |
| 安装部署 | 安装部署 | /install-deploy/ | 环境搭建、初始化数据库。关键章节：开发环境 | /faq/ |
| 代码生成 | 代码生成 | /code-gen/ | 代码生成器使用指南。关键章节：生成步骤 | /dao/ |
```

**FAQ_TABLE 格式**：
```markdown
| 如何安装？ | 安装部署 | https://example.com/docs/install-deploy/ |
| API 怎么写？ | API 文档 | https://example.com/docs/api/ |
```

### 阶段 4：验证

1. **脚本验证**：运行 `python3 scripts/cache_docs.py --skill <sub-skill> --permalink /test/` 测试一篇文档
2. **读取缓存**：读取生成的 `__00.md` 文件，确认 Markdown 格式正确、章节导航完整
3. **Skill 发现**：确保 Agent 可发现所有子 Skill
4. **端到端测试**：模拟用户提问，验证路由→缓存→回答流程

## 调试技巧

### 内容提取失败

如果 `cache_docs.py` 提取内容为空或不完整：

1. 查看 stderr 输出中的 `DEBUG: 内容提取成功，选择器: xxx` 确认用了哪个选择器
2. 手动查看目标页面的 HTML 源码，找到包裹正文的容器
3. 在 `CONTENT_SELECTORS` 中添加对应的正则表达式

```python
# 添加自定义选择器
CONTENT_SELECTORS = [
    # 你的自定义选择器放在最前面
    (r'<div[^>]*class="[^"]*your-content-class[^"]*"[^>]*>(.*?)</div>', "自定义"),
    # ... 保留其他选择器作为回退
]
```

### URL 模式不匹配

如果 permalink 到 URL 的转换不正确，修改 `permalink_to_url()` 函数中的拼接逻辑。

### 图片无法下载

部分站点有防盗链，可在请求头中添加 `Referer`：
```python
img_resp = requests.get(img_url, timeout=REQUEST_TIMEOUT, headers={
    "User-Agent": "Doc-Skills-Cache/2.0",
    "Referer": doc_url,  # 添加 Referer
})
```

## 模板参考

| 文件 | 用途 |
|------|------|
| [templates/main-skill.md](templates/main-skill.md) | 主索引 SKILL.md 模板 |
| [templates/sub-skill.md](templates/sub-skill.md) | 子 Skill SKILL.md 模板 |
| [templates/cache_docs.py](templates/cache_docs.py) | 通用缓存脚本（Python） |
