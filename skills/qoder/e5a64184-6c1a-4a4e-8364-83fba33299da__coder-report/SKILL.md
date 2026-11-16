---
name: coder-report
description: 根据Git提交历史自动生成工作日报并支持提交Moka加班。当用户需要写日报、汇总当天工作、生成提交报告或提交加班时使用。
title: 研发日报
category: 效率
---

# 研发日报生成器

根据Git提交历史自动汇总生成简洁的工作日报，并支持直接提交加班申请。

## 使用场景

- 用户说"生成今天的日报"
- 用户说"汇总3月18日的工作"
- 用户说"根据git提交写日报"

## 技能工作流

获取用户 → 获取提交 → 分类分析 → 生成日报 → 输出确认 → (可选)提交加班

## 前置条件

- Git 已配置用户信息
- 时间范围：统计当天 6:00 到次日 6:00 的提交记录（适配加班场景）

## 执行步骤

### 1. 自动发现工程并收集提交

使用脚本自动扫描代码工作区下的所有 Git 工程,并行收集提交记录:

```bash
# 收集今天的提交(使用配置中的工作区)
python3 scripts/collect-commits.py

# 收集指定日期的提交(使用配置中的工作区)
python3 scripts/collect-commits.py 2026-03-27

# 指定工作区并收集提交(同时会更新配置)
python3 scripts/collect-commits.py /path/to/project_workspace 2026-03-27
```

**错误处理:**

如果脚本报错 `配置不存在` 或 `workspace 未配置`:
1. 使用 `ask_user_question` 询问用户:「未找到代码工作区配置,请指定扫描范围」
   - 选项 A:扫描当前工作区父目录(推荐)
   - 选项 B:指定自定义路径
2. 获取用户选择后,使用 `config_helper.py` 保存配置:
   ```bash
   python3 scripts/config_helper.py set workspace /path/to/workspace
   ```
3. 重新执行收集脚本

脚本输出 JSON 格式：
```json
{
  "date": "2026-03-27",
  "author": "用户名",
  "repos_scanned": ["project-a", "project-b"],
  "commits": [
    {
      "hash": "abc1234",
      "message": "feat: xxx",
      "date": "2026-03-27",
      "datetime": "2026-03-27 18:30:00 +0800",
      "repo": "project-a"
    }
  ],
  "total": 5
}
```

提交按 `datetime` 降序排列，第一个即为最晚提交。

**异常处理**：
- 无提交记录 → 输出「当日无你的提交记录，请确认日期是否正确」
- 未配置 Git 用户名 → 提示「请配置 git config user.name」
- 未找到 Git 工程 → 提示「未找到 Git 工程，请确认目录结构」

### 2. 分析并分类提交

解析脚本输出的 JSON，将提交按模块/功能域分组：

| 分类 | 匹配关键词 |
|------|-----------|
| 后端基础设施 | common, config, entity, mapper, pom, docker |
| 认证/安全 | auth, login, jwt, permission, rbac |
| 网关/API | gateway, route, filter |
| 业务模块 | erp, wms, tms, platform, order, inventory |
| 前端页面 | feat(page), component, route, layout |
| 测试 | test, spec, e2e |
| 文档 | docs, readme, wiki |
| CI/CD | ci, cd, jenkins, deploy |

**多工程展示**：
- 或按工程分组展示提交

### 3. 生成日报

按以下模板输出：

```markdown
## {日期}工作日报

**主要完成工作：**

1. **{分类1}**：{简要描述具体内容}。

2. **{分类2}**：{简要描述具体内容}。

...（按重要性排序，保留3-5条核心内容）

**总结**：{一句话整体工作概括}。

> 最后提交时间：yyyy-MM-dd HH:mm:ss【{工程名}】
```

**最后提交时间需要精确到时分秒**

### 4. 输出确认

展示生成的日报，询问用户是否需要调整或补充其他内容。

**可选操作**：
- 指定特定工程重新生成
- 调整日期范围
- 手动补充未提交的工作内容

### 5. 提交加班(可选)

日报输出确认后,询问用户是否需要提交加班申请。

**提交流程:**

1. 使用 `ask_user_question` 工具询问用户：「是否需要根据本次日报提交加班申请？」
   - 选项 A：是，自动提交加班
   - 选项 B：否，跳过

2. 若用户选择「是」，执行加班提交：
   - **日期**：日报对应的日期（格式 YYYY-MM-DD）
   - **加班原因**：提取日报中的「主要完成工作」与「总结」内容，拼接为加班原因文本
   - **附件**：自动生成代码片段附件（rendered to JPG）
   - **提交模式**：自动提交，无需用户再次确认

3. 加班原因拼接格式参考：
   ```
   {主要完成工作各条目，逗号分隔}。{总结内容}
   ```

4. 执行提交命令:
   ```bash
   python3 scripts/mokahr_overtime_cli.py submit-date \
     --date 2026-05-15 \
     --reason "加班原因" \
     --auto-generate-attachment \
     --code-snippet "# 代码片段内容"
   ```

**错误处理:**

如果脚本报错 `配置不存在` 或 `email/password 未配置`:
1. 使用 `ask_user_question` 询问用户:「未找到 Mokahr 账号配置,请输入登录信息」
   - 提示用户输入邮箱
   - 提示用户输入密码
2. 获取用户信息后,使用 `config_helper.py` 保存配置:
   ```bash
   python3 scripts/config_helper.py set email user@example.com
   python3 scripts/config_helper.py set password "your-password"
   ```
3. 重新执行提交命令

5. 可选参数：
   - `--start`: 加班开始时间（如 18:30）
   - `--end`: 加班结束时间（如 23:00）
   - `--attachment <path>`: 使用提供的图片附件
   - `--code-snippet-file <path>`: 从文件读取代码片段

6. 提交完成后，将结果反馈给用户（包括审批流程信息）。

**一键自动提交流程（当用户只提供日期时）：**

当用户只提供一个日期（如"3月30日"或"2026-03-30"），自动执行：
1. 收集 Git 提交记录
2. 生成工作日报
3. 生成代码片段附件
4. 自动提交加班申请，无需用户确认

## 输出规范

1. **精简性**：每条工作描述控制在20-30字
2. **结构化**：使用编号列表，加粗分类标题
3. **完整性**：覆盖当天所有有意义的提交
4. **总结性**：最后用一句话概括整体进展

## 示例

**输入**：脚本收集到 ai-coding-kit、fengqun-scm 等工程的提交记录

**输出**：
```markdown
## 3月27日工作日报

**主要完成工作：**

1. **文档与技能优化**：重构 diagram、modeling 等技能文档，优化构建流程。

2. **WMS仓库管理**：修复前后端字段不匹配，优化库存快照及安全库存功能。

3. **数据库设计**：补充 wms_warehouse_region 表缺失字段。

4. **部署优化**：增加Nacos服务JVM内存配置。

5. **版本发布**：完成 v1.0 MVP 里程碑版本。


**总结**：完成WMS模块功能优化、多个技能文档重构及v1.0 MVP版本发布。

> 最后提交时间：2026-03-27 18:30:00【fengqun-scm】
```

## 加班提交辅助功能

### 日报转代码片段规范

将日报内容转换为模拟业务代码风格的 Python 代码（用于附件生成）：

```python
# {repo} - {commit_message}
# commit: {hash} - {date}

def process_daily_work():
    """{日期}工作任务处理"""
    tasks = [
        {"category": "{分类}", "content": "{描述}"},
        ...
    ]
    
    for task in tasks:
        execute(task)
    
    return summarize(tasks)
```

**代码片段规范：**
- 直接与加班内容相关，不涉及 Mokahr 提交逻辑
- 使用真实的业务代码片段或函数体，避免说明性文字
- 避免使用占位符如 `TODO`, `example`, `demo` 或通用模板名称
- 保持语义自然，即使不完全可运行

### Mokahr 加班命令参考

**扫描日期（检查是否可提交）：**
```bash
python3 scripts/mokahr_overtime_cli.py scan-date --date 2026-05-15
```

**扫描整月（找出可提交日期）：**
```bash
python3 scripts/mokahr_overtime_cli.py scan-month --month 2026-05
```

**预测审批路径：**
```bash
python3 scripts/mokahr_overtime_cli.py predict-path --date 2026-05-15
```

**提交加班：**
```bash
python3 scripts/mokahr_overtime_cli.py submit-date \
  --date 2026-05-15 \
  --reason "系统升级" \
  --auto-generate-attachment \
  --code-snippet "# 代码片段"
```

**加班规则：**
- 工作日：要求打卡时间在 21:30 之后，强制提交开始时间为 18:30
- 周末或节假日：要求加班时长大于 0 小时
- 最小加班时长：2小时

### 批量提交本月加班

当用户要求"提交本月加班"时：
1. 扫描本月所有日期，找出有 Git 提交的日期
2. 对每个有提交的日期：
   - 检查是否符合加班条件（工作日18:30后，周末全天）
   - 生成工作日报
   - 自动生成代码片段附件
   - 提交加班申请
3. 汇总提交结果，反馈给用户
