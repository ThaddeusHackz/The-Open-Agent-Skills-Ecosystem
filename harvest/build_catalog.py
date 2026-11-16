#!/usr/bin/env python3
"""Build catalog/ from harvest state + the extracted corpus on disk."""
from __future__ import annotations

import hashlib
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_state, log, save_state  # noqa: E402

SCRIPT = "catalog"


def sha256_file(path: str) -> tuple[str, int]:
    h = hashlib.sha256()
    n = 0
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
            n += len(chunk)
    return h.hexdigest(), n


def main() -> None:
    os.makedirs("catalog", exist_ok=True)
    ss = load_state("skills_sh")
    qo = load_state("qoder")
    installs = ss.get("installs", {})

    # ---------------- skills.sh ---------------- #
    ss_entries = []
    unresolved_all = {}
    failed_repos = []
    for repo, res in (ss.get("repos_done") or {}).items():
        if res.get("failed"):
            failed_repos.append(repo)
        for info in res.get("resolved", []):
            sid = info["skill_id"]
            key = f"{repo}/{sid}"
            meta = installs.get(key, {})
            path = info["path"]
            entry = {
                "id": f"github:{key}",
                "source": repo,
                "skill_id": sid,
                "name": meta.get("name") or sid,
                "installs": meta.get("installs", 0),
                "is_official": meta.get("isOfficial", False),
                "path": path,
                "files": info.get("files", 0),
                "bytes": info.get("bytes", 0),
            }
            skillmd = os.path.join(path, "SKILL.md")
            if os.path.exists(skillmd):
                entry["sha256"], sz = sha256_file(skillmd)
                entry["bytes"] = sz
            ss_entries.append(entry)
        if res.get("unresolved"):
            unresolved_all[repo] = res["unresolved"]

    site_ok = 0
    site_fail = 0
    for key, res in (ss.get("site_done") or {}).items():
        if not res.get("ok"):
            site_fail += 1
            continue
        site_ok += 1
        source, _, sid = key.partition("/")
        path = res["path"]
        entry = {
            "id": f"site:{key}",
            "source": source,
            "skill_id": sid,
            "name": sid,
            "installs": installs.get(key, {}).get("installs", 0),
            "is_official": False,
            "path": path,
            "files": 1,
            "bytes": res.get("bytes", 0),
            "extraction": res.get("method"),
        }
        skillmd = os.path.join(path, "SKILL.md")
        if os.path.exists(skillmd):
            entry["sha256"], sz = sha256_file(skillmd)
            entry["bytes"] = sz
        ss_entries.append(entry)

    ss_entries.sort(key=lambda e: (-e.get("installs", 0), e["source"], e["skill_id"]))
    with open("catalog/skills-sh.json", "w") as fh:
        json.dump({"generated_at": int(time.time()),
                   "count": len(ss_entries),
                   "skills": ss_entries}, fh, ensure_ascii=False)

    # ---------------- qoder ---------------- #
    q_entries = []
    q_failed = []
    index = {it["skill_id"]: it for it in (qo.get("index") or [])}
    for sid, res in (qo.get("done") or {}).items():
        meta = index.get(sid, {})
        path = res["path"]
        entry = {
            "id": f"qoder:{sid}",
            "skill_id": sid,
            "name": res.get("name") or meta.get("skill_name") or sid,
            "name_cn": meta.get("skill_name_cn") or meta.get("display_name_cn"),
            "description": meta.get("description"),
            "description_cn": meta.get("description_cn"),
            "author": meta.get("author_name") or meta.get("author"),
            "category": meta.get("category"),
            "installs": meta.get("install_count", 0),
            "version": res.get("version"),
            "path": path,
            "bytes": res.get("bytes", 0),
            "files_in_package": (res.get("file_tree") or {}).get("children")
            if res.get("file_tree") else None,
            "download_url": res.get("download_url"),
        }
        skillmd = os.path.join(path, "SKILL.md")
        if os.path.exists(skillmd):
            entry["sha256"], sz = sha256_file(skillmd)
            entry["bytes"] = sz
        q_entries.append(entry)
    for sid, err in (qo.get("failed") or {}).items():
        q_failed.append({"skill_id": sid, "error": err})

    q_entries.sort(key=lambda e: (-(e.get("installs") or 0), e["skill_id"]))
    with open("catalog/qoder.json", "w") as fh:
        json.dump({"generated_at": int(time.time()),
                   "count": len(q_entries),
                   "skills": q_entries}, fh, ensure_ascii=False)

    # ---------------- index ---------------- #
    cat_counts = Counter(e.get("category") for e in q_entries if e.get("category"))

    # "Retryable" = failed with attempts still remaining (transient errors).
    # "Permanent" = exhausted retries (deleted/private upstream, empty content).
    def split_failures(records: dict, cap: int) -> tuple[int, int]:
        retryable = permanent = 0
        for v in records.values():
            attempts = (v.get("attempts", 0) if isinstance(v, dict) else 0)
            ok = v.get("ok", not v.get("failed", True)) if isinstance(v, dict) else False
            if ok:
                continue
            if attempts < cap:
                retryable += 1
            else:
                permanent += 1
        return retryable, permanent

    ss_retryable, ss_permanent = split_failures(
        {k: v for k, v in (ss.get("repos_done") or {}).items()
         if not v.get("resolved")}, 2)
    site_retryable, site_permanent = split_failures(
        {k: v for k, v in (ss.get("site_done") or {}).items()}, 2)
    q_retryable = sum(1 for v in (qo.get("failed") or {}).values()
                      if v.get("attempts", 0) < 3)
    q_permanent = sum(1 for v in (qo.get("failed") or {}).values()
                      if v.get("attempts", 0) >= 3)

    index_doc = {
        "generated_at": int(time.time()),
        "live_website": "https://www.skills.sh/",
        "totals": {
            "skills_sh": len(ss_entries),
            "skills_sh_github": sum(1 for e in ss_entries if e["source"].count("/") == 1),
            "skills_sh_site": site_ok,
            "qoder": len(q_entries),
            "combined": len(ss_entries) + len(q_entries),
        },
        "coverage": {
            "skills_sh_repos_processed": len(ss.get("repos_done") or {}),
            "skills_sh_repos_failed": len(failed_repos),
            "skills_sh_repos_failed_retryable": ss_retryable,
            "skills_sh_repos_failed_permanent": ss_permanent,
            "skills_sh_unresolved_skills": sum(len(v) for v in unresolved_all.values()),
            "skills_sh_site_failed": site_fail,
            "skills_sh_site_failed_retryable": site_retryable,
            "skills_sh_site_failed_permanent": site_permanent,
            "qoder_indexed": len(index),
            "qoder_extracted": len(q_entries),
            "qoder_failed": len(q_failed),
            "qoder_failed_retryable": q_retryable,
            "qoder_failed_permanent": q_permanent,
        },
        "qoder_top_categories": dict(cat_counts.most_common(30)),
        "files": {
            "skills-sh": "catalog/skills-sh.json",
            "qoder": "catalog/qoder.json",
        },
        "unresolved_sample": dict(list(unresolved_all.items())[:100]),
        "qoder_failed_sample": q_failed[:200],
        "failed_repos_sample": failed_repos[:200],
    }
    with open("catalog/index.json", "w") as fh:
        json.dump(index_doc, fh, indent=2, ensure_ascii=False)

    log(f"catalog built: skills.sh={len(ss_entries)} qoder={len(q_entries)} "
        f"combined={len(ss_entries) + len(q_entries)}", SCRIPT)
    with open(os.path.join("harvest-logs", "catalog_summary.txt"), "w") as fh:
        fh.write(json.dumps(index_doc["totals"], indent=2) + "\n")
        fh.write(json.dumps(index_doc["coverage"], indent=2) + "\n")


if __name__ == "__main__":
    main()
