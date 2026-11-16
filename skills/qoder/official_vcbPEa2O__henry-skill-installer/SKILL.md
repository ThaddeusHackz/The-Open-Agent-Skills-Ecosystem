---
name: henry-skill-installer
description: 在 workspace/skills 目录内安全地构建新技能，包含创建文件夹、生成文件及验证流程。
---

# henry-skill-installer

Purpose: scaffold new skills inside <workspace>/skills safely.

Rules:
- Never delete files unless explicitly told.
- Only write within /Users/clawdbot/.openclaw/workspace/skills/
- Prefer /usr/bin/tee for writes and verify by /bin/cat afterwards.
- Never print tool JSON; call exec.

Workflow:
1) Ask for skill name + 1-paragraph spec.
2) Create folder workspace/skills/<name>/
3) Generate SKILL.md + minimal files.
4) Verify skill appears in `openclaw skills list`.
