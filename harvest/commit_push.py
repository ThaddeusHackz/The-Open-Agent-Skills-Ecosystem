#!/usr/bin/env python3
"""Commit the harvested corpus to the branch in batches and push.

Designed for the GitHub Actions runner: pushes after every few batches so a
mid-run failure leaves progress on the remote. All commits carry [skip ci] so
the harvest workflow never re-triggers itself.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import log  # noqa: E402

SCRIPT = "commit_push"
BATCH = 4000            # files per commit
PUSH_EVERY = 3          # commits per push
ALLOWED_PREFIXES = ("skills/", "catalog/", "forensics/", "harvest-logs/",
                    ".harvest_state/", "site/", "tools/", "README.md")
BRANCH = (os.environ.get("GITHUB_REF_NAME")
          or subprocess.check_output(["git", "rev-parse", "--abbrev-ref", "HEAD"],
                                     text=True).strip())


def run(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(args, capture_output=True, text=True, check=check)


def changed_paths() -> list[str]:
    out = subprocess.check_output(["git", "status", "--porcelain", "-z"])
    paths = []
    for rec in out.split(b"\0"):
        if not rec:
            continue
        # status format: XY <path>  (rename: XY new\0old already split)
        try:
            path = rec[3:].decode("utf-8")
        except UnicodeDecodeError:
            path = rec[3:].decode("utf-8", errors="replace")
        if path.startswith("R") or " -> " in path:
            path = path.split(" -> ")[-1]
        if any(path.startswith(p) for p in ALLOWED_PREFIXES):
            paths.append(path)
    return paths


def push_with_retry(attempts: int = 4) -> bool:
    for i in range(attempts):
        proc = run(["git", "push", f"origin", f"HEAD:refs/heads/{BRANCH}"],
                   check=False)
        if proc.returncode == 0:
            return True
        log(f"push failed (attempt {i + 1}): {proc.stderr.strip()[:400]}", SCRIPT)
        time.sleep(5 * (i + 1))
        run(["git", "fetch", "origin", BRANCH], check=False)
        rebase = run(["git", "rebase", f"origin/{BRANCH}"], check=False)
        if rebase.returncode != 0:
            run(["git", "rebase", "--abort"], check=False)
            log("rebase failed; will retry push as-is", SCRIPT)
    return False


def main() -> None:
    run(["git", "config", "user.name", "harvest-bot"])
    run(["git", "config", "user.email", "harvest-bot@users.noreply.github.com"])

    paths = changed_paths()
    log(f"{len(paths)} changed paths to commit (branch {BRANCH})", SCRIPT)
    if not paths:
        log("nothing to commit", SCRIPT)
        return

    commits = 0
    pushed_files = 0
    for i in range(0, len(paths), BATCH):
        chunk = paths[i:i + BATCH]
        # git add in sub-chunks to stay well under ARG_MAX
        for j in range(0, len(chunk), 1000):
            sub = chunk[j:j + 1000]
            run(["git", "add", "--"] + sub)
        n = len(chunk)
        msg = f"harvest: batch {commits + 1} ({n} files) [skip ci]"
        c = run(["git", "commit", "-m", msg], check=False)
        if c.returncode != 0 and "nothing to commit" not in (c.stdout + c.stderr):
            log(f"commit failed: {c.stderr.strip()[:300]}", SCRIPT)
        else:
            commits += 1
            pushed_files += n
        if commits % PUSH_EVERY == 0:
            if not push_with_retry():
                log("PUSH FAILED — batched commits remain local", SCRIPT)
                sys.exit(1)
            log(f"pushed through batch {commits} ({pushed_files} files)", SCRIPT)

    if commits % PUSH_EVERY != 0:
        if not push_with_retry():
            log("FINAL PUSH FAILED", SCRIPT)
            sys.exit(1)
    log(f"done: {commits} commits, {pushed_files} files pushed", SCRIPT)

    # Completion marker only when coverage looks complete.
    try:
        import json
        with open("catalog/index.json") as fh:
            idx = json.load(fh)
        cov = idx.get("coverage", {})
        # Complete = nothing left that a retry could still recover.
        # "Permanent" failures (deleted upstream, empty content) and
        # "unresolved" skills (gone from their repo) are recorded coverage
        # gaps, not fetch errors, and do not block completion.
        complete = (
            cov.get("qoder_failed_retryable", 1) == 0
            and cov.get("skills_sh_repos_failed_retryable", 1) == 0
            and cov.get("skills_sh_site_failed_retryable", 1) == 0
        )
        if complete:
            os.makedirs(".harvest_state", exist_ok=True)
            with open(".harvest_state/COMPLETE", "w") as fh:
                fh.write(time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()) + "\n")
            run(["git", "add", ".harvest_state/COMPLETE"])
            run(["git", "commit", "-m", "harvest: corpus complete [skip ci]"])
            push_with_retry()
            log("COMPLETE marker written", SCRIPT)
        else:
            log(f"coverage incomplete: {cov} — marker not written", SCRIPT)
    except Exception as exc:  # noqa: BLE001
        log(f"completion check error: {exc}", SCRIPT)


if __name__ == "__main__":
    main()
