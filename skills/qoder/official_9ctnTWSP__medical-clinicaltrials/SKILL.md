---
name: medical-clinicaltrials
description: 访问 ClinicalTrials.gov，支持按疾病、干预措施、阶段和状态筛选，通过 NCT ID 检索详情，获取试验元数据及研究信息，用于查找正在进行中的试验、识别药物再利用机会及跟踪招募情况。
---

# Clinical Trials Search

Access ClinicalTrials.gov to search clinical trials with advanced filtering options.

## What it does

- Search clinical trials by condition, intervention, phase, and status
- Retrieve detailed trial information by NCT ID
- Filter by disease/condition or treatment type
- Access trial metadata and study information

## Use cases

- Find ongoing clinical trials for specific diseases (myasthenia gravis, multiple sclerosis)
- Identify trials for drug repurposing opportunities
- Track trial status and recruitment
- Discover treatment innovations

## Tools available

- `ctg_search_studies` - Search trials with various filters
- `ctg_get_study` - Get single study by NCT ID
- `ctg_search_by_condition` - Search trials by disease
- `ctg_search_by_intervention` - Search trials by treatment
- `ctg_get_study_metadata` - Get available fields metadata

## Requirements

No API key required. Public ClinicalTrials.gov API access.

## Author

Pascal Brockmeyer & medical-mcps contributors
