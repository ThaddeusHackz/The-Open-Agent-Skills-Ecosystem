#!/usr/bin/env python3
"""Patch README.md and site/index.html placeholders with real corpus numbers
read from catalog/index.json and forensics/stats.json."""
from __future__ import annotations

import json
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fmt(n: int) -> str:
    return f"{n:,}"


def main() -> None:
    with open(os.path.join(REPO, "catalog", "index.json")) as fh:
        idx = json.load(fh)
    totals = idx["totals"]
    coverage = idx.get("coverage", {})

    findings_total = 0
    stats_path = os.path.join(REPO, "forensics", "stats.json")
    if os.path.exists(stats_path):
        with open(stats_path) as fh:
            findings_total = json.load(fh).get("findings_total", 0)

    replacements = {
        "{{SKILLS_SH_COUNT}}": fmt(totals["skills_sh"]),
        "{{QODER_COUNT}}": fmt(totals["qoder"]),
        "{{QODER_COUNT_REPORTED}}": fmt(coverage.get("qoder_indexed")
                                        or totals["qoder"]),
        "{{COMBINED_COUNT}}": fmt(totals["combined"]),
        "{{FORENSIC_FINDINGS}}": fmt(findings_total),
    }

    for rel in ("README.md", "site/index.html"):
        path = os.path.join(REPO, rel)
        if not os.path.exists(path):
            continue
        with open(path) as fh:
            text = fh.read()
        before = text
        for k, v in replacements.items():
            text = text.replace(k, v)
        if text != before:
            with open(path, "w") as fh:
                fh.write(text)
            print(f"updated {rel}")
        else:
            print(f"no placeholders in {rel}")

    print(json.dumps(replacements, indent=2))


if __name__ == "__main__":
    main()
