---
name: arxiv-paper-rater
description: >
  Search, score, and track ArXiv research papers based on user-defined preferences
  and multi-dimensional scoring criteria. This skill should be used when the user
  wants to find and evaluate academic papers, track research trends, or maintain
  a curated reading list with quality filtering. Triggers include: searching papers,
  rating papers, finding top papers, tracking research, paper recommendations, or
  any mention of ArXiv with quality filtering intent.
agent_created: true
---

# ArXiv Paper Rater

Search, evaluate, and curate ArXiv research papers with personalized scoring and deduplication.

## Overview

This skill extends basic ArXiv search with a structured evaluation pipeline: user preferences
define scoring criteria, each paper is scored across multiple dimensions, and only papers
meeting the threshold are recorded — with deduplication to avoid revisiting previously
rated papers.

## Core Capabilities

### 1. Preference Management

Read `references/preferences.md` at the start of each session. This file contains:

- Research interest areas (or instructions to use per-query topics)
- Scoring dimensions (Innovation, Relevance, Practicality, Rigor)
- Dimension weights and passing threshold
- Customization rules

When the user requests changes to preferences (e.g., "add a dimension", "change the
threshold", "adjust weights"), update `references/preferences.md` immediately and confirm.

### 2. Paper Search

Use `scripts/search_arxiv.sh` to query the ArXiv API:

```bash
# Flag-based interface (recommended)
scripts/search_arxiv.sh -q "<query>" [-n max_results] [-c category] [-s start] [--date-from YYYY-MM-DD] [--date-to YYYY-MM-DD]

# Legacy positional interface (still supported)
scripts/search_arxiv.sh "<query>" [max_results] [category]
```

**Flag arguments:**

| Flag | Short | Default | Description |
|------|-------|---------|-------------|
| `--query` | `-q` | (required) | Search keywords |
| `--max-results` | `-n` | 10 | Number of results to return |
| `--category` | `-c` | none | ArXiv category filter, e.g. cs.AI, cs.CL |
| `--start` | `-s` | 0 | Pagination offset for fetching results beyond the first page |
| `--date-from` | — | none | Start date filter (YYYY-MM-DD) |
| `--date-to` | — | none | End date filter (YYYY-MM-DD); defaults to today if only `--date-from` is set |

**Examples:**
```bash
# Basic search
scripts/search_arxiv.sh -q "LLM reasoning" -n 5

# With category filter
scripts/search_arxiv.sh -q "transformer" -n 10 -c cs.AI

# Pagination: fetch results 11-20
scripts/search_arxiv.sh -q "text-to-SQL" -n 10 -s 10

# Date range: only papers from April 2026
scripts/search_arxiv.sh -q "LLM agent" --date-from 2026-04-01 --date-to 2026-04-30

# Recent papers: last 7 days to today
scripts/search_arxiv.sh -q "RAG" --date-from 2026-04-25

# Legacy positional style (still works)
scripts/search_arxiv.sh "LLM reasoning" 5 cs.AI
```

Parse the returned XML. Each `<entry>` contains `<title>`, `<summary>`, `<author>`,
`<published>`, and `<link title="pdf">`. The `<opensearch:totalResults>` field
indicates the total number of matching papers — use this with the `--start` flag
to paginate through large result sets.

### 3. Paper Scoring

For each paper found, perform the following evaluation:

1. **Read the abstract** (`<summary>` field) carefully
2. **Check deduplication**: Search `references/rated_papers.md` for the paper's
   ArXiv ID. If found, skip and note as duplicate.
3. **Score each dimension** (1-10) per the rubric in `references/preferences.md`:
   - Innovation (创新性)
   - Relevance (相关性)
   - Practicality (实用性)
   - Rigor (严谨性)
4. **Calculate weighted score** using the weights from preferences
5. **Determine status**:
   - **Pass**: Weighted Score >= threshold (default 6.5)
   - **Borderline**: Within 1.0 point below threshold
   - **Fail**: Below borderline range

### 4. Record Keeping

For papers that **pass** the scoring threshold, append an entry to
`references/rated_papers.md` using this format:

```markdown
### [SCORE] ArXiv_ID - PAPER_TITLE
- **中文标题**: Chinese translation of the paper title
- **Authors**: First Author et al.
- **Published**: YYYY-MM-DD
- **Rated**: YYYY-MM-DD
- **Link**: https://arxiv.org/abs/XXXX.XXXXX
- **Scores**: Innovation=N Relevance=N Practicality=N Rigor=N
- **Weighted**: N.NN
- **Keywords**: topic1, topic2
- **Summary**: One-sentence summary.
```

**Deduplication**: Before scoring any paper, check `references/rated_papers.md`
for an existing entry with the same ArXiv ID. If found, skip the paper and inform
the user it was previously rated.

## Workflow

### Standard Search & Rate Workflow

1. Read `references/preferences.md` to load current preferences and scoring criteria
2. Read `references/rated_papers.md` to load previously rated paper IDs
3. Accept user's search topic/keywords (or use default interests from preferences)
4. Run `scripts/search_arxiv.sh "<query>" <count> [category]`
5. Parse XML results, extract paper entries
6. For each paper:
   a. Extract ArXiv ID from the entry URL
   b. Check deduplication against `references/rated_papers.md`
   c. If duplicate, skip and note
   d. If new, score across all dimensions
   e. Calculate weighted score
   f. Determine pass/borderline/fail status
7. Present results to the user in a structured table:
   - Paper title, authors, weighted score, dimension scores, status
   - Highlight passed papers, flag borderline ones
8. For passed papers, append entries to `references/rated_papers.md`
9. Optionally provide a brief analysis of the batch results

### Preference Update Workflow

When the user requests preference changes:

1. Read current `references/preferences.md`
2. Apply the requested changes
3. Write updated `references/preferences.md`
4. Confirm the changes to the user

### History Review Workflow

When the user wants to review previously rated papers:

1. Read `references/rated_papers.md`
2. Present the entries, optionally filtered by keyword, date range, or score range

## Output Format

Present search results in a clear table:

| # | Title | 中文标题 | Authors | Score | I | R | P | Rg | Status |
|---|-------|---------|---------|-------|---|---|---|----|--------|
| 1 | Paper Title | 论文标题 | Author et al. | 7.8 | 8 | 8 | 7 | 8 | PASS |
| 2 | Another Paper | 另一篇论文 | Author et al. | 6.2 | 7 | 6 | 6 | 5 | BORDERLINE |

Legend: I=Innovation, R=Relevance, P=Practicality, Rg=Rigor

For each passed paper, also provide a 2-3 sentence summary explaining why it passed
and what makes it noteworthy.

## Examples

- "帮我搜一下最近关于 LLM reasoning 的论文，按我的标准评分"
- "Search ArXiv for multimodal models, score and filter the results"
- "查看我之前评过的论文"
- "把评分阈值调到 7.0"
- "给实用性维度加大权重到 0.35"
- "今天 ArXiv 有什么值得看的 AI Agent 论文吗？"

## Resources

- `scripts/search_arxiv.sh`: ArXiv API search script with category support
- `references/preferences.md`: User preferences, scoring dimensions, weights, and threshold
- `references/rated_papers.md`: Record of previously rated papers for deduplication
