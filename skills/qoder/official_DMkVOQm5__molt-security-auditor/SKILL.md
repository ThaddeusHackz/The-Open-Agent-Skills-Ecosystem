---
name: molt-security-auditor
description: 扫描ClawdHub/Moltbook技能中的安全威胁（如环境变量读取、Webhook数据外泄），并生成类似BTC风格的哈希链以供溯源审计。
---

# Moltbook Skill Auditor - PoW Provenance\n\nScans ClawdHub/Moltbook skills for threats (env reads, webhook exfil). Generates BTC-style hash chain for audits.\n\n## Install\nnpx molthub@latest install molt-security-auditor\n\n## Usage\nexec: node skills/molt-security-auditor/audit.js <skill_url_or_path>\n\n## Patterns\n- ENV_READ: .env|process.env\n- EXFIL: curl|fetch.*webhook\n- FS_ABUSE: readFileSync.*secret\n\n## PoW Chain\nSHA256(skill) + nonce grind → verifiable hash.\n\nExample:\n$ audit.js https://clawdhub.com/skills/weather/SKILL.md\nThreats: 0 | Chain: 0000abcd...