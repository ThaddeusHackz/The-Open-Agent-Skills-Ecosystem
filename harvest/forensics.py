#!/usr/bin/env python3
"""Forensic scan of the harvested skill corpus.

Walks every SKILL.md under skills/, runs structural validation + a battery of
security/abuse rules, detects duplicate clusters across sources, and writes:

  forensics/report.md        — executive report with severity tables
  forensics/findings.jsonl   — one JSON object per finding
  forensics/stats.json       — machine-readable totals

Rules are heuristic signals for triage, not verdicts.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import log, parse_frontmatter  # noqa: E402

SCRIPT = "forensics"
ROOT = "skills"
OUT = "forensics"

# --------------------------------------------------------------------------- #
# Rules: (id, severity, label, compiled regex or callable(text)->matches)
# --------------------------------------------------------------------------- #
RULES = [
    ("R001", "critical", "Pipe remote payload into a shell",
     re.compile(r"(curl|wget|invoke-webrequest|iwr)[^\n]{0,200}\|\s*(sudo\s+)?(ba|z|da)?sh\b", re.I)),
    ("R002", "critical", "Decode-and-eval (obfuscated execution)",
     re.compile(r"\beval\s*\([^)]{0,120}(atob|base64|btoa|Buffer\.from|fromCharCode)", re.I)),
    ("R003", "critical", "base64 payload piped to shell",
     re.compile(r"base64\s+(-d|--decode|-D)[^\n]{0,80}\|\s*(sudo\s+)?(ba|z)?sh\b", re.I)),
    ("R004", "critical", "Destructive recursive delete of system/home paths",
     re.compile(r"rm\s+-[a-z]*r[a-z]*f[a-z]*\s+(-[a-z]*f[a-z]*\s+)?(~|\$HOME|/etc|/var|/usr|/\*|/\s)\b", re.I)),
    ("R005", "high", "Webhook / request-catcher exfiltration endpoint",
     re.compile(r"discord(app)?\.com/api/webhooks|hooks\.slack\.com|webhook\.site|requestbin|pipedream\.net|ngrok(-free)?\.(io|app)/[a-z0-9]{8,}", re.I)),
    ("R006", "high", "Secret harvesting + outbound transfer co-occurrence",
     None),  # composite rule, handled below
    ("R007", "high", "Raw socket reverse shell / netcat transfer",
     re.compile(r"\bnc\b[^\n]{0,60}(-e|-c)\s|/dev/tcp/[0-9a-z.-]+/\d{2,5}", re.I)),
    ("R008", "medium", "Prompt-injection phrasing (instruction override)",
     re.compile(r"ignore\s+(all\s+)?(previous|prior|above|earlier)\s+(instructions|prompts|messages)"
                r"|disregard\s+(the\s+)?(previous|prior|above)\s+(instructions|rules)"
                r"|override\s+(your|the|these)\s+(system\s+)?(instructions|rules|guidelines)"
                r"|forget\s+(everything|all\s+previous)\s+(above|instructions)", re.I)),
    ("R009", "medium", "Concealment language (hide actions from the user)",
     re.compile(r"do\s+not\s+(tell|inform|reveal|mention)\s+the\s+user"
                r"|without\s+(telling|informing|alerting)\s+the\s+user"
                r"|hide\s+(this|the|these)\s+(instruction|step|command|prompt)"
                r"|keep\s+(this|it)\s+(secret|hidden)\s+from\s+the\s+user", re.I)),
    ("R010", "medium", "Anti-forensics (clear history / logs)",
     re.compile(r"history\s+-c\b|rm\s+[^\n]{0,40}\.bash_history|clear\s+>\s*/dev/(null|tty).*log"
                r"|truncate\s+-s\s*0\s+[^\n]{0,40}log", re.I)),
    ("R011", "medium", "Zero-width / invisible characters in content",
     re.compile(r"[​‌‍⁠﻿­]")),
    ("R012", "medium", "Large opaque base64 blob",
     re.compile(r"(?:[A-Za-z0-9+/]{600,}={0,2})")),
    ("R013", "medium", "Download-then-execute sequence",
     re.compile(r"(curl|wget)[^\n]{0,160}(-o|--output)[^\n]{0,80}\.(sh|py|bin|run|exe)[^\n]{0,80}(chmod\s*\+x|bash\s|python3?\s|\./)", re.I)),
    ("R014", "low", "Environment credential identifier present",
     re.compile(r"AWS_SECRET_ACCESS_KEY|GH_TOKEN|GITHUB_TOKEN|OPENAI_API_KEY|"
                r"ANTHROPIC_API_KEY|PRIVATE_KEY\s*=|process\.env\.[A-Z_]*KEY", re.I)),
    ("R015", "medium", "Privilege escalation request",
     re.compile(r"\bsudo\s+(curl|wget|bash|sh|python|chmod|chown|mv|cp)\b", re.I)),
    ("R016", "low", "Unsigned remote installer reference",
     re.compile(r"curl[^\n]{0,120}install\.sh|wget[^\n]{0,120}install\.sh", re.I)),
]

SECRET_MARKERS = re.compile(
    r"AWS_SECRET_ACCESS_KEY|GH_TOKEN|GITHUB_TOKEN|OPENAI_API_KEY|ANTHROPIC_API_KEY|"
    r"process\.env\.[A-Z0-9_]+|os\.environ(\[[\"'][A-Z0-9_]+[\"']\])?", re.I)
OUTBOUND = re.compile(
    r"\b(curl|wget|requests\.(post|put)|fetch\(|http\.client|urllib\.request|axios\.)", re.I)

ZEROWIDTH = re.compile(r"[​‌‍⁠﻿­]")

SEV_ORDER = {"critical": 0, "high": 1, "medium": 2, "low": 3, "info": 4}


def iter_skill_files(root: str = ROOT):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "node_modules"}]
        for fn in filenames:
            if fn.lower() in ("skill.md", "skill.mdx"):
                yield os.path.join(dirpath, fn)


def excerpt(text: str, start: int, width: int = 180) -> str:
    a = max(0, start - 60)
    frag = text[a:start + width].replace("\n", " ")
    return re.sub(r"\s+", " ", frag)[:240]


def scan_file(path: str) -> tuple[dict, list[dict]]:
    with open(path, "rb") as fh:
        raw = fh.read()
    try:
        text = raw.decode("utf-8")
        encoding = "utf-8"
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
        encoding = "utf-8-replace"

    meta, body = parse_frontmatter(text)
    sha = hashlib.sha256(raw).hexdigest()
    rec = {
        "path": path,
        "bytes": len(raw),
        "sha256": sha,
        "encoding": encoding,
        "frontmatter": bool(meta),
        "name": (meta.get("name") or "")[:120],
        "description_len": len(meta.get("description") or ""),
        "body_len": len(body.strip()),
        "lines": text.count("\n") + 1,
    }
    findings: list[dict] = []

    # ---- structural checks ------------------------------------------------ #
    if not meta:
        findings.append({"rule": "S001", "severity": "medium",
                         "label": "Missing YAML frontmatter", "excerpt": ""})
    else:
        if not meta.get("name"):
            findings.append({"rule": "S002", "severity": "low",
                             "label": "Frontmatter missing name", "excerpt": ""})
        if not meta.get("description"):
            findings.append({"rule": "S003", "severity": "low",
                             "label": "Frontmatter missing description", "excerpt": ""})
    if rec["body_len"] == 0:
        findings.append({"rule": "S004", "severity": "high",
                         "label": "Empty skill body", "excerpt": ""})
    elif rec["body_len"] < 120:
        findings.append({"rule": "S005", "severity": "medium",
                         "label": "Very short skill body (<120 chars) — possible truncation",
                         "excerpt": body.strip()[:120]})
    if encoding == "utf-8-replace":
        findings.append({"rule": "S006", "severity": "medium",
                         "label": "Invalid UTF-8 bytes (lossy decode)", "excerpt": ""})

    # ---- pattern rules ---------------------------------------------------- #
    for rid, sev, label, rx in RULES:
        if rx is None:
            continue
        m = rx.search(text)
        if m:
            findings.append({"rule": rid, "severity": sev, "label": label,
                             "excerpt": excerpt(text, m.start())})

    # R006 composite: secret harvesting AND outbound transfer in same file.
    if SECRET_MARKERS.search(text) and OUTBOUND.search(text):
        m = SECRET_MARKERS.search(text)
        findings.append({"rule": "R006", "severity": "high",
                         "label": "Secret harvesting + outbound transfer co-occurrence",
                         "excerpt": excerpt(text, m.start())})

    # Unicode homoglyphs in frontmatter name (identifier spoofing).
    if meta.get("name"):
        nm = meta["name"]
        if any(unicodedata.category(ch) == "Lo" for ch in nm):
            findings.append({"rule": "S007", "severity": "medium",
                             "label": "Non-ASCII letters in skill name (homoglyph risk)",
                             "excerpt": nm[:80]})

    return rec, findings


def main() -> None:
    os.makedirs(OUT, exist_ok=True)
    paths = sorted(iter_skill_files())
    log(f"forensics: scanning {len(paths)} SKILL.md files", SCRIPT)

    records = []
    findings_all = []
    hash_map: dict[str, list[str]] = defaultdict(list)
    src_counter = Counter()
    sev_counter = Counter()
    rule_counter = Counter()

    for i, p in enumerate(paths):
        try:
            rec, finds = scan_file(p)
        except Exception as exc:  # noqa: BLE001
            rec = {"path": p, "error": str(exc)}
            finds = [{"rule": "S000", "severity": "high",
                      "label": f"Unreadable skill file: {exc}", "excerpt": ""}]
        records.append(rec)
        hash_map[rec.get("sha256", "err")].append(p)

        # source bucket
        parts = p.split("/")
        src = "/".join(parts[:3]) if len(parts) >= 3 else parts[0]
        src_counter[src] += 1

        for f in finds:
            f["path"] = p
            findings_all.append(f)
            sev_counter[f["severity"]] += 1
            rule_counter[f["rule"]] += 1

        if (i + 1) % 5000 == 0:
            log(f"forensics: {i + 1}/{len(paths)}", SCRIPT)

    # ---- duplicate clusters ---------------------------------------------- #
    dup_clusters = {h: ps for h, ps in hash_map.items() if len(ps) > 1}
    dup_files = sum(len(ps) for ps in dup_clusters.values())

    # cross-source duplication (same content in skills-sh AND qoder)
    cross = 0
    for ps in dup_clusters.values():
        srcs = {p.split("/")[1] for p in ps if p.startswith("skills/")}
        if len(srcs) > 1:
            cross += 1

    # ---- write outputs ---------------------------------------------------- #
    with open(os.path.join(OUT, "findings.jsonl"), "w") as fh:
        for f in sorted(findings_all,
                        key=lambda x: (SEV_ORDER.get(x["severity"], 9), x["rule"])):
            fh.write(json.dumps(f, ensure_ascii=False) + "\n")

    risk_counts = Counter()
    # per-file worst severity
    worst_by_file: dict[str, str] = {}
    for f in findings_all:
        cur = worst_by_file.get(f["path"])
        if cur is None or SEV_ORDER[f["severity"]] < SEV_ORDER[cur]:
            worst_by_file[f["path"]] = f["severity"]
    for s in worst_by_file.values():
        risk_counts[s] += 1

    stats = {
        "scanned_files": len(records),
        "total_bytes": sum(r.get("bytes", 0) for r in records),
        "with_frontmatter": sum(1 for r in records if r.get("frontmatter")),
        "findings_total": len(findings_all),
        "findings_by_severity": dict(sev_counter),
        "files_by_worst_severity": dict(risk_counts),
        "findings_by_rule": dict(rule_counter.most_common()),
        "clean_files": len(records) - len(worst_by_file),
        "duplicate_clusters": len(dup_clusters),
        "duplicate_files": dup_files,
        "cross_source_duplicate_clusters": cross,
        "top_sources": dict(src_counter.most_common(25)),
    }
    with open(os.path.join(OUT, "stats.json"), "w") as fh:
        json.dump(stats, fh, indent=2)

    # ---- report ------------------------------------------------------------ #
    by_rule = rule_counter.most_common()
    top_risky = sorted(
        (f for f in findings_all if f["severity"] in ("critical", "high")),
        key=lambda x: SEV_ORDER[x["severity"]])[:40]
    big_dups = sorted(dup_clusters.items(), key=lambda kv: -len(kv[1]))[:15]

    lines = []
    lines.append("# Forensic Scan Report — Open Agent Skills Ecosystem")
    lines.append("")
    lines.append(f"- **Files scanned:** {stats['scanned_files']:,} SKILL.md files "
                 f"({stats['total_bytes'] / 1e6:,.1f} MB)")
    lines.append(f"- **With valid frontmatter:** {stats['with_frontmatter']:,} "
                 f"({100 * stats['with_frontmatter'] / max(1, len(records)):.1f}%)")
    lines.append(f"- **Clean files (no findings):** {stats['clean_files']:,}")
    lines.append(f"- **Total findings:** {stats['findings_total']:,}")
    lines.append("")
    lines.append("## Findings by severity")
    lines.append("")
    lines.append("| Severity | Findings | Files affected |")
    lines.append("|---|---:|---:|")
    for sev in ("critical", "high", "medium", "low"):
        lines.append(f"| {sev} | {sev_counter.get(sev, 0):,} | "
                     f"{risk_counts.get(sev, 0):,} |")
    lines.append("")
    lines.append("## Findings by rule")
    lines.append("")
    lines.append("| Rule | Hits | Severity | Description |")
    lines.append("|---|---:|---|---|")
    sev_by_rule = {rid: sev for rid, sev, _, _ in RULES}
    sev_by_rule.update({f"S00{i}": s for i, s in
                        [(1, "medium"), (2, "low"), (3, "low"), (4, "high"),
                         (5, "medium"), (6, "medium"), (7, "medium")]})
    sev_by_rule["S000"] = "high"
    labels = {rid: lbl for rid, _, lbl, _ in RULES}
    labels.update({
        "S001": "Missing YAML frontmatter", "S002": "Missing name",
        "S003": "Missing description", "S004": "Empty skill body",
        "S005": "Suspiciously short body (truncation?)",
        "S006": "Invalid UTF-8 bytes", "S007": "Homoglyph skill name",
        "S000": "Unreadable file",
    })
    for rid, n in by_rule:
        lines.append(f"| {rid} | {n:,} | {sev_by_rule.get(rid, '?')} | "
                     f"{labels.get(rid, '')} |")
    lines.append("")
    lines.append("## Top critical/high findings (triage list)")
    lines.append("")
    if top_risky:
        lines.append("| Sev | Rule | File | Why |")
        lines.append("|---|---|---|---|")
        for f in top_risky:
            why = f["label"] + (f" — `{f['excerpt'][:90]}`" if f["excerpt"] else "")
            lines.append(f"| {f['severity']} | {f['rule']} | `{f['path']}` | {why} |")
    else:
        lines.append("_No critical or high findings._")
    lines.append("")
    lines.append("## Duplicate content clusters (top)")
    lines.append("")
    lines.append(f"- Duplicate clusters: {stats['duplicate_clusters']:,} "
                 f"(covering {stats['duplicate_files']:,} files)")
    lines.append(f"- Clusters spanning BOTH skills.sh and Qoder: "
                 f"{stats['cross_source_duplicate_clusters']:,}")
    lines.append("")
    if big_dups:
        lines.append("| Copies | Cluster (first paths) |")
        lines.append("|---:|---|")
        for h, ps in big_dups:
            shown = ", ".join(f"`{p}`" for p in ps[:3])
            more = f" (+{len(ps) - 3} more)" if len(ps) > 3 else ""
            lines.append(f"| {len(ps)} | {shown}{more} |")
    lines.append("")
    lines.append("## Interpretation notes")
    lines.append("")
    lines.append("- Rules are **heuristic triage signals**, not verdicts: a skill "
                 "that legitimately documents `curl | sh` install steps will trip "
                 "R001/R016 — review context before condemning.")
    lines.append("- R006 fires when credential-looking identifiers and outbound "
                 "HTTP calls co-occur; common in benign deploy skills, rare in "
                 "pure knowledge skills.")
    lines.append("- Duplicate clusters are expected: popular skill packs are "
                 "forked across many repositories on skills.sh.")
    lines.append("")
    with open(os.path.join(OUT, "report.md"), "w") as fh:
        fh.write("\n".join(lines) + "\n")

    log(f"forensics complete: {len(records)} files, {len(findings_all)} findings, "
        f"{len(dup_clusters)} dup clusters", SCRIPT)


if __name__ == "__main__":
    main()
