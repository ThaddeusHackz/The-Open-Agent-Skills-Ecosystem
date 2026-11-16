---
name: ai-pc-screen-doctor
description: "Diagnose AI PC screen errors from screenshots, OCR text, and user context. Use when the task is to turn terminal errors, blue screens, installer failures, IDE build failures, or inference error screenshots into structured diagnosis results with probable causes, repair steps, commands, and verification checklists."
---

# AI PC Screen Doctor

Use this skill when the user needs a structured diagnosis for a screen error rather than a generic chat response.

## Inputs

- `image_path`: optional local screenshot path
- `ocr_text`: optional copied error text or OCR text
- `context`: optional environment, system version, recent actions, and reproduction notes

## Output

Return a JSON diagnosis with these fields:

```json
{
  "engine": "openclaw-local-rules",
  "id": "python_missing_module",
  "title": "Python 依赖缺失或解释器环境不一致",
  "category": "Python dependency",
  "severity": "medium",
  "confidence": 0.88,
  "summary": "结构化诊断摘要",
  "signals": [],
  "probable_causes": [],
  "immediate_actions": [],
  "commands": [],
  "verification": [],
  "escalation": []
}
```

## Workflow

1. Read `ocr_text` and `context`.
2. If `image_path` exists, treat it as supporting context; do not require image understanding to proceed.
3. Match the input against known fault patterns.
4. Produce a low-risk, executable diagnosis.
5. Prefer concrete commands and verification steps over generic advice.

## Covered cases

- Python dependency or interpreter mismatch
- Node install or permission failures
- GPU / NPU memory exhaustion
- Display driver failures, black screen, blue screen
- Generic screen failures with missing context

## Local execution

```powershell
cd ai_pc_screen_doctor_skill\skill
python skill.py --text "ModuleNotFoundError: No module named openvino_genai" --context "Windows 11, venv changed"
```

With an image path:

```powershell
python skill.py --image ".\sample.png" --text "VIDEO_TDR_FAILURE" --context "外接显示器后偶发黑屏蓝屏"
```

## Runtime notes

- Python `>= 3.9`
- No external API is required for the minimal skill
- Optional environment variables for the full project:
  - `DASHSCOPE_API_KEY`
  - `DEEPSEEK_API_KEY`

## Files

- `manifest.json`: skill metadata
- `skill.py`: CLI entry and local rules engine
