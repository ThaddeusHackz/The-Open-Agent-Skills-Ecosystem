---
name: document-creator-sophnet
description: 一款集成的文档创建技能，支持创建 Word 文档（DOCX）和 PowerPoint 演示文稿（PPTX），并自动上传至 OSS 返回 URL。
---

# Document Creator with Auto-Upload SophNet

## Description

An integrated document creation skill that supports creating Word documents (DOCX) and PowerPoint presentations (PPTX), with automatic upload to OSS and URL return.

## Usage

```bash
# Create document using skill
openclaw document-creator /path/to/your/file.txt

# Or call via session
# In OpenClaw session: Create document /path/to/file.png
```

## Configuration Requirements

- Set `SOPH_API_KEY` environment variable
- Or configure sophnet API key in OpenClaw config file

## Supported Parameters

- `file_path`: Local file path to upload (required)

## Return Value

- Success: Returns signed URL string
- Failure: Throws exception with error message

## Dependencies

- Python 3.7+
- requests library
- OpenClaw config access permission