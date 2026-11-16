---
name: create-custom-homework-review-skill
description: Use when creating a custom homework grading skill for Qoder/Codex from assignment requirements, reference answers, standard examples, rubrics, and student submission formats. This skill designs the grading basis, chooses exactly one score type among dimension, gradient, and item, creates evaluation items using only currently supported formats, and scaffolds a reusable project-local homework review skill.
---

# 自定义作业批阅 Skill 创建器

## 批阅创建对象

创建一个新的作业批阅 skill，而不是直接批阅学生作业。输入通常包括作业要求、参考答案或标准样例、学生提交样例、文件类型说明、教师特殊扣分规则和平台输出要求。输出是一个可继续完善或直接验证的批阅 skill 初稿。

本技能自带资源：

- `scripts/scaffold_review_skill.py`：生成目标批阅 skill 的目录、`SKILL.md` 初稿和 `agents/openai.yaml`。
- `references/review_skill_template.md`：批阅 skill 的完整结构模板、评分方式选择规则和评价项格式约束。

## 创建流程

1. 读取用户给出的作业材料。
   - 明确作业类型、学生提交形态、是否有标准参考、是否需要逐题/逐项/整体评分。
   - 若材料里已经给出评分规则，优先保留教师规则；若未给出，按作业目标自行设计评分项和评价标准。
2. 选择目标 skill 名称。
   - 使用小写英文、数字和连字符，建议以 `grade-` 开头。
   - 名称必须短、稳定、能表达批阅对象，例如 `grade-lab-report-rubric`。
3. 运行脚手架生成初稿。
   - 在当前项目内默认输出到 `/Users/zhangyichi/工作/能力训练/homework_review/.qoder/skills`。
   - 示例：
     ```bash
     python3 scripts/scaffold_review_skill.py \
       --skill-name grade-example-homework \
       --display-name 示例作业批阅 \
       --assignment-type "学生提交的示例作业，依据教师提供的作业要求和参考答案评分" \
       --output-dir /Users/zhangyichi/工作/能力训练/homework_review/.qoder/skills
     ```
4. 编辑目标 skill。
   - 读取 `references/review_skill_template.md`。
   - 将目标 `SKILL.md` 中的 TODO 全部替换为具体批阅规则。
   - 在 `score_type` 中只保留一种：`dimension`、`gradient` 或 `item`。
   - 自行设计评分表：维度、梯度或固定评分项的分值必须合计等于 `full_score`。
   - 评价项默认保留「综合评语」和「改进建议」，再按作业类型补充必要项目。
5. 遵守当前平台限制。
   - 评价项 `format` 只能使用：`文本式`、`清单式`、`对比式`、`标签式`。
   - 不要生成时间线类评价项。
   - 不要生成图文、图片数组、媒体嵌入或 `items[].images` 字段。
   - 客观复核信息如果需要展示，放入 `evaluations` 中的 `标签式` 或 `清单式` 项。
6. 验证目标 skill。
   - 运行：
     ```bash
     python3 /Users/zhangyichi/.codex/skills/.system/skill-creator/scripts/quick_validate.py <目标skill目录>
     ```
   - 若目标 skill 自带脚本，至少运行 `python3 -m py_compile` 或一个最小烟测。

## 评分方式选择

- 使用 `item`：题目数量固定、每题分值明确、参考答案逐题给分，例如试卷、实验数据表、固定问答题。
- 使用 `dimension`：同一份提交需要从多个质量维度累计评分，例如报告、论文、设计方案、视频展示。
- 使用 `gradient`：教师更关心整体档位，或平台只需要等级/区间，例如表现性任务、开放创作、整体能力评价。

如果材料同时适合多种方式，优先选择最贴近教师复审习惯的方式；不要在同一个目标 skill 中混用多种 `score_type`。

## 输出约束

目标 skill 的最终批阅结果必须由其自身定义清楚。创建器生成初稿时要保证：

- `SKILL.md` frontmatter 只有 `name` 和 `description`。
- `description` 写清批阅对象、基准、评分和评价方式。
- 评分项只有一种 `score_type`。
- `evaluations` 的每个评价项都有合法 `format` 和字段映射。
- 不创建 README、安装说明、变更日志等额外文档。
