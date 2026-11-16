---
name: astro-paper-reviewer
description: 基于BibTeX文献库和arXiv资源，对天文学论文LaTeX草稿进行逐小节审查-修改循环，提升论文质量。当用户提到论文修改、文献引用检查、LaTeX审查、arXiv文献检索时必须使用此技能。
dependency:
  system:
    - pip3 install arxiv pybtex requests
---

# 天文学论文智能审查与修改

## 任务目标
- 本 Skill 用于：基于 BibTeX 文献库和 arXiv 资源，对天文学论文 LaTeX 草稿进行逐小节审查-修改循环
- 能力：
  - 解析 BibTeX 文件提取文献元数据（标题、关键词、摘要、arXiv ID）
  - 通过 arXiv API 获取论文全文（PDF/HTML）
  - 逐小节审查 LaTeX 论文内容
  - 检查文献引用准确性和相关性
  - 提出修改建议并迭代优化
- 触发：当用户需要审查天文学论文、检查文献引用、修改 LaTeX 草稿时

## 前置准备
- 依赖说明：
  - `arxiv`：Python arXiv 官方库，用于获取论文元数据和PDF
  - `pybtex`：专业的 BibTeX 解析库
  - `requests`：HTTP 请求库
- 输入文件要求：
  - `bibtexabs.bib`：包含文献信息的 BibTeX 文件
  - `.tex` 文件：待审查的 LaTeX 论文草稿

## 操作步骤

### 1. 解析 BibTeX 文献库
- 调用 `scripts/parse_bibtex.py` 解析 `bibtexabs.bib`
- 提取每篇文献的：标题、关键词、摘要、arXiv ID (eprint)
- 构建文献知识库，用于后续引用检查

### 2. 理解论文内容
- 读取用户提供的 LaTeX 论文草稿
- 识别论文结构（摘要、引言、方法、结果、讨论、结论等小节）
- 提取当前小节的关键论点和引用需求

### 3. 文献深度检索（按需）
- 当 BibTeX 中的信息不足以支持审查时：
  - 调用 `scripts/fetch_arxiv.py` 通过 arXiv ID 获取论文信息
  - PDF 链接：`https://arxiv.org/pdf/{eprint}`
  - HTML 链接（2020年后）：`https://arxiv.org/html/{eprint}`
  - 或使用 arXiv API 搜索相关论文

### 4. 逐小节审查-修改循环
对每个小节执行以下循环，直至无问题：
1. **审查阶段**：
   - 检查论点是否清晰、逻辑是否连贯
   - 验证文献引用是否准确、相关
   - 检查术语使用是否规范
   - 识别需要补充引用的位置
2. **修改阶段**：
   - 提出具体的修改建议
   - 补充缺失的文献引用
   - 优化表述和逻辑结构
3. **验证阶段**：
   - 确认修改是否解决了问题
   - 检查是否引入新问题
   - 决定是否进入下一轮审查

### 5. 输出审查报告
- 生成完整的审查报告，包含：
  - 各小节修改摘要
  - 新增/修改的文献引用列表
  - 修改后的 LaTeX 代码

## 资源索引

### 脚本工具
- **[scripts/parse_bibtex.py](scripts/parse_bibtex.py)**
  - 用途：使用 pybtex 解析 BibTeX 文件，提取文献元数据
  - 触发时机：在审查开始前，**必须调用此脚本**解析文献库
  - 输入：`bibtexabs.bib` 文件路径
  - 输出：JSON 格式的文献数据

- **[scripts/fetch_arxiv.py](scripts/fetch_arxiv.py)**
  - 用途：使用 arxiv 库通过 ID 或关键词获取论文信息，支持下载 PDF
  - 触发时机：当需要深度了解某篇文献时，**立即调用此脚本**
  - 支持：通过 eprint 获取元数据、下载 PDF、搜索相关论文

- **[scripts/latex_parser.py](scripts/latex_parser.py)**
  - 用途：解析 LaTeX 论文结构，提取各小节内容和引用
  - 触发时机：在审查开始前，**必须调用此脚本**解析论文结构
  - 输出：JSON 格式的论文结构和引用信息

- **[scripts/paper_reviewer.py](scripts/paper_reviewer.py)**
  - 用途：执行逐小节审查-修改循环的核心脚本
  - 触发时机：当需要对论文进行审查时，**调用此脚本**
  - 功能：小节审查、引用检查、修改建议生成

### 参考文档
- **[references/bibtex-format.md](references/bibtex-format.md)**
  - 内容：BibTeX 文件格式规范和常见字段说明
  - 使用时机：在解析 BibTeX 前，**必须先读取此文档**了解格式规范
  - 关键作用：确保正确提取文献元数据

- **[references/arxiv-api-guide.md](references/arxiv-api-guide.md)**
  - 内容：arXiv API 使用指南和查询示例
  - 使用时机：在调用 arXiv API 前，**必须先读取此文档**
  - 关键作用：了解 API 调用方式和返回格式

## 注意事项
- **附件读取规则**：当任务涉及 BibTeX 解析或 arXiv API 调用时，**必须优先读取** references/ 中的相关文档
- **脚本调用规则**：遇到 BibTeX 解析、arXiv 数据获取等技术性操作时，**立即调用** scripts/ 中的对应脚本
- **审查策略**：采用"审查-修改-验证"循环，确保每个小节质量达标后再进入下一节
- **文献引用原则**：优先使用 BibTeX 中已有的文献，必要时通过 arXiv API 补充