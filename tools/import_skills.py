#!/usr/bin/env python3
"""Import SKILL.md packages from this repo into any agent's skills directory.

Examples
--------
  # See what agents are supported and where they look for skills
  python3 tools/import_skills.py --list-agents

  # Preview the top 20 most-installed Qoder skills
  python3 tools/import_skills.py --list --source qoder --top 20

  # Install everything from skills.sh into Claude Code (user scope)
  python3 tools/import_skills.py --agent claude --source skills-sh --all

  # Install skills whose name mentions "react" into Cursor (project scope)
  python3 tools/import_skills.py --agent cursor --scope project \
      --name-sub react --all

  # Install a single skill by catalog id or path
  python3 tools/import_skills.py --agent qoder \
      --skill github:anthropics/skills/frontend-design

  # Install the 500 most-installed skills into the universal directory
  python3 tools/import_skills.py --agent universal --top 500
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# agent -> (user-level dir, project-level dir). None = not applicable.
# "universal" is the emerging cross-agent standard (~/.agents/skills) that
# skills.sh, Qoder, and most modern agents also discover.
AGENTS: dict[str, tuple[str | None, str | None]] = {
    "claude":        ("~/.claude/skills", ".claude/skills"),
    "claude-code":   ("~/.claude/skills", ".claude/skills"),
    "cursor":        ("~/.cursor/skills", ".cursor/skills"),
    "codex":         ("~/.codex/skills", ".codex/skills"),
    "copilot":       (None, ".github/skills"),
    "github-copilot": (None, ".github/skills"),
    "vscode":        (None, ".github/skills"),
    "windsurf":      ("~/.codeium/windsurf/skills", ".windsurf/skills"),
    "gemini":        ("~/.gemini/skills", ".gemini/skills"),
    "qoder":         ("~/.qoder/skills", ".qoder/skills"),
    "qoder-cn":      ("~/.qoder-cn/skills", ".qoder-cn/skills"),
    "cline":         ("~/.cline/skills", ".cline/skills"),
    "amp":           ("~/.amp/skills", ".amp/skills"),
    "goose":         ("~/.config/goose/skills", ".goose/skills"),
    "kilo":          ("~/.kilo/skills", ".kilo/skills"),
    "kiro":          ("~/.kiro/skills", ".kiro/skills"),
    "kiro-cli":      ("~/.kiro/skills", ".kiro/skills"),
    "opencode":      ("~/.config/opencode/skills", ".opencode/skills"),
    "roo":           ("~/.roo/skills", ".roo/skills"),
    "trae":          ("~/.trae/skills", ".trae/skills"),
    "zed":           ("~/.config/zed/skills", ".agents/skills"),
    "droid":         ("~/.factory/skills", ".factory/skills"),
    "openclaw":      ("~/.openclaw/skills", ".openclaw/skills"),
    "clawdbot":      ("~/.clawdbot/skills", ".clawdbot/skills"),
    "antigravity":   ("~/.agent/skills", ".agent/skills"),
    "nous-research": ("~/.nous/skills", ".nous/skills"),
    "codebuddy":     ("~/.codebuddy/skills", ".codebuddy/skills"),
    "zcode":         ("~/.zcode/skills", ".zcode/skills"),
    "universal":     ("~/.agents/skills", ".agents/skills"),
    "agents":        ("~/.agents/skills", ".agents/skills"),
}


def expand(p: str) -> str:
    return os.path.abspath(os.path.expanduser(p))


def load_catalogs(sources: list[str]) -> list[dict]:
    entries: list[dict] = []
    if "skills-sh" in sources:
        path = os.path.join(REPO, "catalog", "skills-sh.json")
        if os.path.exists(path):
            with open(path) as fh:
                entries.extend(json.load(fh).get("skills", []))
    if "qoder" in sources:
        path = os.path.join(REPO, "catalog", "qoder.json")
        if os.path.exists(path):
            with open(path) as fh:
                entries.extend(json.load(fh).get("skills", []))
    return entries


def walk_fallback(sources: list[str]) -> list[dict]:
    """When catalog JSONs are missing, reconstruct a minimal index from disk."""
    entries = []
    roots = []
    if "skills-sh" in sources:
        roots.append(os.path.join(REPO, "skills", "skills-sh"))
    if "qoder" in sources:
        roots.append(os.path.join(REPO, "skills", "qoder"))
    for root in roots:
        for dirpath, _, filenames in os.walk(root):
            if "SKILL.md" in filenames:
                rel = os.path.relpath(dirpath, REPO)
                entries.append({"id": rel, "name": os.path.basename(dirpath),
                                "path": rel, "installs": 0, "source":
                                "qoder" if rel.startswith("skills/qoder")
                                else "skills-sh"})
    return entries


def apply_filters(entries: list[dict], args) -> list[dict]:
    if args.name_sub:
        subs = [s.lower() for s in args.name_sub]
        entries = [e for e in entries
                   if any(s in (e.get("name") or "").lower()
                          or s in (e.get("skill_id") or "").lower()
                          or s in (e.get("source") or "").lower()
                          for s in subs)]
    if args.min_installs:
        entries = [e for e in entries
                   if (e.get("installs") or 0) >= args.min_installs]
    if args.category:
        cat = args.category.lower()
        entries = [e for e in entries
                   if cat in (e.get("category") or "").lower()]
    # catalogs are pre-sorted by installs desc; keep that order
    if args.top:
        entries = entries[:args.top]
    if args.limit:
        entries = entries[:args.limit]
    return entries


def install(entries: list[dict], dest_root: str, force: bool,
            dry_run: bool) -> tuple[int, int, int]:
    installed = skipped = missing = 0
    for e in entries:
        rel = e.get("path")
        if not rel:
            missing += 1
            continue
        src = os.path.join(REPO, rel)
        if not os.path.isdir(src):
            missing += 1
            continue
        # directory name: prefer namespaced id to avoid collisions
        name = e.get("name") or os.path.basename(src)
        if e.get("id", "").startswith("github:"):
            owner_repo = e.get("source", "").replace("/", "--")
            name = f"{owner_repo}--{e.get('skill_id') or name}"
        elif e.get("id", "").startswith("site:"):
            name = f"{(e.get('source') or 'site').replace('.', '-')}--{e.get('skill_id') or name}"
        name = "".join(c if c.isalnum() or c in "-_." else "-" for c in name)[:120]
        dest = os.path.join(dest_root, name)
        if os.path.exists(dest):
            if force and not dry_run:
                shutil.rmtree(dest)
            else:
                skipped += 1
                continue
        if dry_run:
            installed += 1
            continue
        shutil.copytree(src, dest, dirs_exist_ok=force)
        installed += 1
    return installed, skipped, missing


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Import SKILL.md packages into any agent",
        formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("--agent", help="target agent (see --list-agents)")
    ap.add_argument("--scope", choices=["user", "project"], default="user",
                    help="user-level (~ home) or project-level (cwd) dir")
    ap.add_argument("--dest", help="explicit destination dir (overrides --agent)")
    ap.add_argument("--source", action="append",
                    choices=["skills-sh", "qoder"],
                    help="corpus to import from (repeatable; default: both)")
    ap.add_argument("--name-sub", action="append",
                    help="substring filter on skill name/id/source (repeatable)")
    ap.add_argument("--min-installs", type=int, default=0)
    ap.add_argument("--category", help="qoder category filter, e.g. 'Design'")
    ap.add_argument("--top", type=int, help="only the N most-installed")
    ap.add_argument("--limit", type=int, help="hard cap after all filters")
    ap.add_argument("--skill", action="append",
                    help="install by catalog id (e.g. github:owner/repo/skill) "
                         "or by skills/ path (repeatable)")
    ap.add_argument("--all", action="store_true",
                    help="explicitly allow importing the entire filtered set")
    ap.add_argument("--list", action="store_true",
                    help="list matching skills without installing")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true",
                    help="overwrite existing skill dirs")
    ap.add_argument("--list-agents", action="store_true")
    args = ap.parse_args()

    if args.list_agents:
        print(f"{'agent':<18} {'user scope':<34} project scope")
        print("-" * 90)
        for a, (u, p) in AGENTS.items():
            print(f"{a:<18} {u or '-':<34} {p or '-'}")
        return

    sources = args.source or ["skills-sh", "qoder"]

    entries = load_catalogs(sources)
    if not entries:
        entries = walk_fallback(sources)
        if not entries:
            sys.exit("No skills found. Is the corpus harvested? "
                     "(catalog/*.json or skills/ missing)")

    if args.skill:
        wanted = set(args.skill)
        by_id = {e.get("id"): e for e in entries}
        by_path = {e.get("path"): e for e in entries}
        picked = []
        for w in wanted:
            e = by_id.get(w) or by_path.get(w)
            if not e:
                sys.exit(f"--skill not found: {w}")
            picked.append(e)
        entries = picked
    else:
        entries = apply_filters(entries, args)

    if not entries:
        sys.exit("No skills matched the filters.")

    if args.list:
        print(f"{'installs':>10}  {'source':<12} id")
        for e in entries:
            print(f"{(e.get('installs') or 0):>10}  "
                  f"{('qoder' if str(e.get('id','')).startswith('qoder') else 'skills-sh'):<12} "
                  f"{e.get('id')}")
        print(f"\n{len(entries)} skill(s).")
        return

    if args.dest:
        dest_root = expand(args.dest)
    elif args.agent:
        if args.agent not in AGENTS:
            sys.exit(f"Unknown agent '{args.agent}'. See --list-agents.")
        u, p = AGENTS[args.agent]
        target = u if args.scope == "user" else p
        if not target:
            sys.exit(f"Agent '{args.agent}' has no {args.scope}-scope dir; "
                     f"try --scope {'project' if args.scope == 'user' else 'user'} "
                     f"or --dest.")
        dest_root = expand(target)
    else:
        ap.error("provide --agent, --dest, --list, or --list-agents")

    if len(entries) > 1000 and not (args.all or args.top or args.limit):
        sys.exit(f"Refusing to import {len(entries)} skills without "
                 f"--all / --top / --limit (safety latch).")

    os.makedirs(dest_root, exist_ok=True)
    installed, skipped, missing = install(entries, dest_root, args.force,
                                          args.dry_run)
    verb = "would install" if args.dry_run else "installed"
    print(f"{verb} {installed} skill(s) -> {dest_root}")
    if skipped:
        print(f"skipped {skipped} (already present; use --force to overwrite)")
    if missing:
        print(f"warning: {missing} catalog entries had missing files on disk")


if __name__ == "__main__":
    main()
