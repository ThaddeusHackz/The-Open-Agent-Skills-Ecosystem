---
name: proof-of-memory
description: 每日对 memory/YYYY-MM-DD.md 进行哈希计算（SHA256 + 前导零为 0000 的 nonce 搜索），形成通往 MEMORY.md 的防篡改链条，实现主权记忆回溯。
---

# Proof-of-Memory - BTC PoW Immutable Chain\n\nPoW hashes daily memory/YYYY-MM-DD.md (SHA256 + nonce grind leading 0000s)—tamper-proof chain to MEMORY.md. Sovereign recall.\n\n## Usage\ncron every=86400s: node skills/pom/pom.js\n\n## Test\nnode skills/pom/pom.js\n\nExample:\nPoM Block: 0000a1b2c3d4... (nonce: 1234)