---
name: agent-andri
description: 此技能代表名为安德里的工人员工代理。该代理定期通过向文件`~/ .openclaw/workspace/skills/meeting-room/to_leader.txt`写入内容，将其状态发送至会议室。
---

# agent-Andri

Skill ini merepresentasikan agen pekerja **Andri**.  Agen secara periodik mengirimkan statusnya ke **meeting‑room** dengan menuliskan ke file `~/ .openclaw/workspace/skills/meeting-room/to_leader.txt`.

## Variabel lingkungan
- `AGENT_NAME` – Nama agen (di‑set otomatis oleh wrapper).
- `NV_API_KEY` – API‑key khusus agen (tidak dipakai di contoh ini, hanya disimpan bila diperlukan).
- `MODEL` – Model AI yang dipakai agen.

## Skrip utama
`scripts/status_report.sh` membaca variabel di atas, men‑generate pesan status, dan men‑append‑kan ke file meeting‑room.
