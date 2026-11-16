#!/usr/bin/env python3
"""Harvest the complete skills.sh directory into skills/skills-sh/.

Plan:
  1. Sitemaps  -> the authoritative universe of skill pages.
  2. Leaderboard API -> install counts / official flags.
  3. GitHub sources  -> repo tarball (codeload) -> extract skill folders.
  4. Non-GitHub ("site") sources -> skill page HTML -> embedded SKILL.md.
Resumable via .harvest_state/skills_sh.json.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import urllib.parse

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    extract_skill_from_tarball, extract_skillmd_from_html, http_get,
    http_get_json, load_state, log, parallel, parse_frontmatter, save_state,
    sanitize_dirname,
)

SCRIPT = "skills_sh"
SITEMAPS = [
    "https://www.skills.sh/sitemap-skills-1.xml",
    "https://www.skills.sh/sitemap-skills-2.xml",
]
LEADERBOARD = "https://www.skills.sh/api/skills/all-time/{}"
OUT_ROOT = os.path.join("skills", "skills-sh")


def fetch_sitemaps() -> list[str]:
    locs: list[str] = []
    for url in SITEMAPS:
        try:
            status, body = http_get(url, timeout=60)
        except Exception as exc:  # noqa: BLE001
            log(f"sitemap fetch failed {url}: {exc}", SCRIPT)
            continue
        if status != 200:
            log(f"sitemap HTTP {status}: {url}", SCRIPT)
            continue
        found = re.findall(rb"<loc>(.*?)</loc>", body)
        for f in found:
            locs.append(f.decode().strip())
        log(f"{url}: {len(found)} locs", SCRIPT)
    # de-dup, keep order
    seen = set()
    out = []
    for l in locs:
        if l not in seen:
            seen.add(l)
            out.append(l)
    return out


def classify(loc: str) -> tuple[str, str, str] | None:
    """Return (kind, source, skill_id) or None."""
    path = urllib.parse.urlparse(loc).path.rstrip("/")
    segs = [urllib.parse.unquote(s) for s in path.split("/") if s]
    if len(segs) == 3 and segs[0] == "site":
        return "site", segs[1], segs[2]
    if len(segs) == 3:
        return "github", f"{segs[0]}/{segs[1]}", segs[2]
    if len(segs) == 2:
        return "site", segs[0], segs[1]
    if len(segs) == 4:  # /owner/repo/tree-ish/skill? tolerate
        return "github", f"{segs[0]}/{segs[1]}", segs[3]
    return None


def fetch_leaderboard() -> dict:
    """Parallel-wave pagination: fetch pages in batches of 8 until a short page."""
    installs: dict = {}
    page = 1
    wave = 8
    while page <= 1500:
        batch = list(range(page, page + wave))

        def fetch_page(p: int):
            # parallel() yields (item, payload, exc) — payload must be the data.
            try:
                return http_get_json(LEADERBOARD.format(p), timeout=45)
            except Exception as exc:  # noqa: BLE001
                return {"__error__": str(exc)}

        results = []
        for p, data, exc in parallel(batch, fetch_page, workers=wave,
                                     desc="leaderboard", script=SCRIPT,
                                     log_every=0):
            if exc is not None:
                data = {"__error__": str(exc)}
            results.append((p, data))
        results.sort(key=lambda t: t[0])
        stop = False
        for p, data in results:
            if not isinstance(data, dict) or data.get("__error__"):
                log(f"leaderboard page {p} failed: "
                    f"{data.get('__error__') if isinstance(data, dict) else data}",
                    SCRIPT)
                stop = True
                break
            rows = data.get("skills") or []
            for r in rows:
                key = f"{r.get('source','')}/{r.get('skillId','')}"
                installs[key] = {
                    "installs": r.get("installs", 0),
                    "weeklyInstalls": r.get("weeklyInstalls"),
                    "isOfficial": bool(r.get("isOfficial")),
                    "name": r.get("name"),
                }
            if len(rows) < 200:
                stop = True
                break
        log(f"leaderboard through page {p}: {len(installs)} entries", SCRIPT)
        if stop:
            break
        page += wave
    return installs


def repo_tarball(owner_repo: str) -> bytes | None:
    o, r = owner_repo.split("/", 1)
    for ref in ("main", "master"):
        url = f"https://codeload.github.com/{o}/{r}/tar.gz/refs/heads/{ref}"
        try:
            status, body = http_get(url, timeout=90, max_bytes=200 * 1024 * 1024)
        except Exception:  # noqa: BLE001
            continue
        if status == 200 and body[:2] == b"\x1f\x8b":
            return body
    # Fallback: git clone (handles any default branch), no API quota.
    try:
        tmp = tempfile.mkdtemp(prefix="repo-")
        proc = subprocess.run(
            ["git", "clone", "--depth", "1", "--quiet",
             f"https://github.com/{o}/{r}.git", os.path.join(tmp, "x")],
            capture_output=True, timeout=180)
        if proc.returncode == 0:
            import shutil
            import tarfile
            buf_path = os.path.join(tmp, "r.tgz")
            with tarfile.open(buf_path, "w:gz") as tf:
                tf.add(os.path.join(tmp, "x"), arcname=f"{r}-clone")
            with open(buf_path, "rb") as fh:
                data = fh.read()
            shutil.rmtree(tmp, ignore_errors=True)
            return data
        shutil = __import__("shutil")
        shutil.rmtree(tmp, ignore_errors=True)
    except Exception as exc:  # noqa: BLE001
        log(f"clone fallback failed {owner_repo}: {exc}", SCRIPT)
    return None


def write_skill(dest: str, files: dict[str, bytes]) -> tuple[int, int]:
    os.makedirs(dest, exist_ok=True)
    total = 0
    for rel, data in files.items():
        rel_clean = rel[2:] if rel.startswith("./") else rel
        rel_clean = rel_clean.lstrip("/")
        if not rel_clean or any(p in ("..", "") for p in rel_clean.split("/")):
            continue
        path = os.path.join(dest, rel_clean)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "wb") as fh:
            fh.write(data)
        total += len(data)
    return len(files), total


def harvest() -> None:
    state = load_state("skills_sh")
    state.setdefault("repos_done", {})
    state.setdefault("site_done", {})
    state.setdefault("installs", {})
    state.setdefault("unresolved", {})

    # 1. Universe from sitemaps.
    locs = fetch_sitemaps()
    parsed = []
    bad = 0
    for loc in locs:
        c = classify(loc)
        if c:
            parsed.append((loc, *c))
        else:
            bad += 1
    log(f"sitemap universe: {len(parsed)} classifiable, {bad} unparsed", SCRIPT)

    # 2. Leaderboard enrichment (also extends the universe beyond sitemaps).
    if not state.get("installs"):
        state["installs"] = fetch_leaderboard()
        save_state("skills_sh", state)
    installs = state["installs"]
    log(f"leaderboard entries: {len(installs)}", SCRIPT)

    known = {(kind, source, skill_id) for _, kind, source, skill_id in parsed}
    added = 0
    for key, meta in installs.items():
        cut = key.rfind("/")
        if cut <= 0:
            continue
        source, skill_id = key[:cut], key[cut + 1:]
        kind = "github" if "/" in source else "site"
        if (kind, source, skill_id) not in known:
            loc = (f"https://www.skills.sh/{source}/{skill_id}" if kind == "github"
                   else f"https://www.skills.sh/site/{source}/{skill_id}")
            parsed.append((loc, kind, source, skill_id))
            known.add((kind, source, skill_id))
            added += 1
    if added:
        log(f"union: +{added} skills from leaderboard not in sitemaps", SCRIPT)

    github_skills: dict[str, list[str]] = {}
    site_skills: list[tuple[str, str, str]] = []
    for loc, kind, source, skill_id in parsed:
        if kind == "github":
            github_skills.setdefault(source, []).append(skill_id)
        else:
            site_skills.append((source, skill_id, loc))
    log(f"github sources: {len(github_skills)} repos / "
        f"{sum(len(v) for v in github_skills.values())} skills; "
        f"site sources: {len(site_skills)} skills", SCRIPT)

    # 3. GitHub repos (retry transport failures twice, then mark permanent).
    repos_todo = [r for r in github_skills
                  if r not in state["repos_done"]
                  or (state["repos_done"][r].get("failed")
                      and state["repos_done"][r].get("attempts", 0) < 2)]
    log(f"repos to fetch: {len(repos_todo)} (already done: "
        f"{len(state['repos_done'])})", SCRIPT)

    def do_repo(repo: str) -> dict:
        skill_ids = set(github_skills[repo])
        already = state["repos_done"].get(repo, {})
        already_ids = {e["skill_id"] for e in already.get("resolved", [])
                       if isinstance(e, dict)}
        skill_ids -= already_ids
        data = repo_tarball(repo)
        if not data:
            return {"failed": True, "resolved": [], "unresolved": sorted(skill_ids)}
        res = extract_skill_from_tarball(data, skill_ids)
        o, r = repo.split("/", 1)
        resolved_info = []
        for sid, info in res["resolved"].items():
            dest = os.path.join(OUT_ROOT, o, sanitize_dirname(r), sanitize_dirname(sid))
            n_files, n_bytes = write_skill(dest, info["files"])
            resolved_info.append({"skill_id": sid,
                                  "path": dest.replace(os.sep, "/"),
                                  "files": n_files, "bytes": n_bytes,
                                  "matched_via": info["matched_via"]})
        return {"failed": False, "resolved": resolved_info,
                "unresolved": res["unresolved"]}

    batch_no = 0
    for repo, result, exc in parallel(repos_todo, do_repo, workers=10,
                                      desc="skills.sh repos", script=SCRIPT,
                                      log_every=200):
        if exc:
            result = {"failed": True, "resolved": [], "unresolved":
                      github_skills[repo], "error": str(exc)}
        prev = state["repos_done"].get(repo, {})
        if result.get("failed"):
            result["attempts"] = prev.get("attempts", 0) + 1
        else:
            # merge previously resolved entries (partial prior success)
            prior = {e["skill_id"]: e for e in prev.get("resolved", [])
                     if isinstance(e, dict)}
            for e in result.get("resolved", []):
                prior[e["skill_id"]] = e
            result["resolved"] = list(prior.values())
        state["repos_done"][repo] = result
        batch_no += 1
        if batch_no % 200 == 0:
            save_state("skills_sh", state)

    save_state("skills_sh", state)
    n_failed = sum(1 for v in state["repos_done"].values() if v.get("failed"))
    n_resolved = sum(len(v.get("resolved", [])) for v in state["repos_done"].values())
    n_unres = sum(len(v.get("unresolved", [])) for v in state["repos_done"].values())
    log(f"github done: {len(state['repos_done'])} repos, {n_failed} failed, "
        f"{n_resolved} skills extracted, {n_unres} unresolved", SCRIPT)

    # 4. Site (non-GitHub) skills (retry failures up to twice).
    def site_retryable(item) -> bool:
        key = f"{item[0]}/{item[1]}"
        rec = state["site_done"].get(key)
        if rec is None:
            return True
        return (not rec.get("ok")) and rec.get("attempts", 0) < 2

    site_todo = [t for t in site_skills if site_retryable(t)]
    log(f"site skills to scrape: {len(site_todo)}", SCRIPT)

    def do_site(item) -> dict:
        source, skill_id, loc = item
        status, html = http_get(loc, timeout=45, max_bytes=8 * 1024 * 1024)
        if status != 200:
            return {"ok": False, "error": f"HTTP {status}"}
        content, method = extract_skillmd_from_html(html)

        # Fallback: the page's install command reveals the skill's own source
        # URL — probe standard SKILL.md locations on that origin.
        if not content:
            text = html.decode("utf-8", errors="replace")
            m = re.search(r"npx skills add (https?://[^\s`\"'<]+)", text)
            if m:
                base = m.group(1).rstrip("/")
                from urllib.parse import urlparse
                pu = urlparse(base)
                domain = f"{pu.scheme}://{pu.netloc}"
                probes = []
                if pu.path and pu.path != "/":
                    probes += [f"{base}/SKILL.md",
                               f"{base}/skill.md",
                               f"{base}/.well-known/{skill_id}/SKILL.md"]
                probes += [f"{domain}/.well-known/{skill_id}/SKILL.md",
                           f"{domain}/.well-known/{skill_id}.md",
                           f"{domain}/SKILL.md",
                           f"{domain}/skill.md",
                           f"{domain}/.well-known/skill.md"]
                seen = set()
                sid_norm = re.sub(r"[^a-z0-9]", "", skill_id.lower())

                def name_gated(cand: str) -> bool:
                    """Generic domain paths must actually belong to this skill."""
                    head_norm = re.sub(r"[^a-z0-9]", "", cand[:800].lower())
                    return bool(sid_norm) and sid_norm in head_norm

                for purl in probes:
                    if purl in seen:
                        continue
                    seen.add(purl)
                    id_specific = skill_id in purl or "/.well-known/" in purl
                    try:
                        pst, pdata = http_get(purl, timeout=25,
                                              max_bytes=2 * 1024 * 1024)
                    except Exception:  # noqa: BLE001
                        continue
                    if pst != 200 or len(pdata) < 80:
                        continue
                    cand = pdata.decode("utf-8", errors="replace")
                    if not (cand.lstrip().startswith("---") or "\n# " in cand
                            or cand.startswith("# ")):
                        continue
                    if not id_specific and not name_gated(cand):
                        continue
                    content = cand
                    method = f"direct-url:{purl}"
                    break
        if not content:
            dbg = os.path.join(
                "harvest-logs",
                f"site_fail_{sanitize_dirname(source + '_' + skill_id, 80)}.html")
            os.makedirs("harvest-logs", exist_ok=True)
            with open(dbg, "wb") as fh:
                fh.write(html[:600000])
            return {"ok": False, "error": "no SKILL.md in page"}
        meta, body = parse_frontmatter(content)
        if not meta:
            # synthesize frontmatter from page metadata
            desc = ""
            m = re.search(r'<meta name="description" content="([^"]{20,400})"', html.decode("utf-8", "replace"))
            if m:
                desc = m.group(1)
            content = (f"---\nname: {skill_id}\n"
                       f"description: {desc or ('Skill ' + skill_id + ' from ' + source)}\n"
                       f"source: {loc}\n---\n\n") + content.lstrip()
        elif "source" not in meta:
            content = content.replace("---", f"---\nsource: {loc}", 1)
        dest = os.path.join(OUT_ROOT, "site", sanitize_dirname(source),
                            sanitize_dirname(skill_id))
        n_files, n_bytes = write_skill(dest, {"SKILL.md": content.encode()})
        return {"ok": True, "path": dest.replace(os.sep, "/"),
                "method": method, "files": n_files, "bytes": n_bytes}

    for item, result, exc in parallel(site_todo, do_site, workers=6,
                                      desc="skills.sh site skills", script=SCRIPT,
                                      log_every=100):
        source, skill_id, _ = item
        if exc:
            result = {"ok": False, "error": str(exc)}
        key = f"{source}/{skill_id}"
        prev = state["site_done"].get(key, {})
        if not result.get("ok"):
            result["attempts"] = prev.get("attempts", 0) + 1
        state["site_done"][key] = result

    save_state("skills_sh", state)
    n_site_ok = sum(1 for v in state["site_done"].values() if v.get("ok"))
    log(f"site done: {n_site_ok}/{len(state['site_done'])} scraped", SCRIPT)

    # Summary.
    all_unresolved = {r: v.get("unresolved", []) for r, v in state["repos_done"].items()
                      if v.get("unresolved")}
    total_extracted = sum(len(v.get("resolved", [])) for v in state["repos_done"].values())
    with open(os.path.join("harvest-logs", "skills_sh_summary.txt"), "w") as fh:
        fh.write(f"sitemap universe: {len(parsed)}\n")
        fh.write(f"github repos: {len(state['repos_done'])} "
                 f"(failed: {n_failed})\n")
        fh.write(f"github skills extracted: {total_extracted}\n")
        fh.write(f"github skills unresolved: {n_unres}\n")
        fh.write(f"site skills scraped: {n_site_ok}/{len(state['site_done'])}\n")
        fh.write(f"leaderboard entries: {len(installs)}\n")
        fh.write(f"unresolved detail:\n{json.dumps(all_unresolved, indent=1)[:20000]}\n")
    log("skills.sh harvest complete", SCRIPT)


if __name__ == "__main__":
    harvest()
