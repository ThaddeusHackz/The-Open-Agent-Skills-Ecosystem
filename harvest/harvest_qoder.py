#!/usr/bin/env python3
"""Harvest the full Qoder skills marketplace into skills/qoder/.

Endpoints (public, no auth):
  GET https://qoder.com/apphub/api/v1/marketplace/catalog/extensions
      ?extension_types=skill&pagination.current_page=N&pagination.page_size=50
  GET https://qoder.com/apphub/api/v1/marketplace/skills/{id}/detail
      -> readme_content (full SKILL.md), download_url, file_tree, metadata
  GET https://qoder.com/api/v1/marketplace/skills/{id}/files?path=/SKILL.md
      -> fallback content channel

Resumable via .harvest_state/qoder.json.
"""
from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import (  # noqa: E402
    http_get, http_get_json, load_state, log, parallel, parse_frontmatter,
    save_state, sanitize_dirname,
)

SCRIPT = "qoder"
INDEX_URL = ("https://qoder.com/apphub/api/v1/marketplace/catalog/extensions"
             "?extension_types=skill&pagination.current_page={page}"
             "&pagination.page_size=50")
DETAIL_URL = "https://qoder.com/apphub/api/v1/marketplace/skills/{sid}/detail"
FILE_URL = "https://qoder.com/api/v1/marketplace/skills/{sid}/files?path=%2FSKILL.md"
OUT_ROOT = os.path.join("skills", "qoder")


def write_skill(dest: str, rel: str, data: bytes) -> None:
    path = os.path.join(dest, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "wb") as fh:
        fh.write(data)


def fetch_index() -> list[dict]:
    """Page through the whole catalog, dedup by skill_id."""
    items: dict[str, dict] = {}
    page = 1
    last_page = None
    total_size = None
    while True:
        try:
            data = http_get_json(INDEX_URL.format(page=page), timeout=45)
        except Exception as exc:  # noqa: BLE001
            log(f"index page {page} failed: {exc}", SCRIPT)
            if page > 1:
                break
            raise
        skills = data.get("skills") or {}
        rows = skills.get("items") or []
        pages = skills.get("pages") or {}
        last_page = pages.get("last_page") or last_page
        total_size = pages.get("total_size") or total_size
        for r in rows:
            sid = r.get("skill_id")
            if sid:
                items[sid] = r
        if page % 50 == 0:
            log(f"index page {page}/{last_page}: {len(items)}/{total_size} unique",
                SCRIPT)
        if not rows:
            break
        if last_page and page >= last_page:
            break
        if page > 2000:
            break
        page += 1
    log(f"index complete: {len(items)} unique skills "
        f"(reported total {total_size})", SCRIPT)
    if total_size and len(items) < total_size * 0.995:
        # Second pass with a different sort to fill gaps from unstable ordering.
        log("shortfall detected — filling with sort_by=latest sweep", SCRIPT)
        page = 1
        while True:
            url = INDEX_URL.format(page=page) + "&sort_by=latest"
            try:
                data = http_get_json(url, timeout=45)
            except Exception:  # noqa: BLE001
                break
            rows = (data.get("skills") or {}).get("items") or []
            new = 0
            for r in rows:
                sid = r.get("skill_id")
                if sid and sid not in items:
                    items[sid] = r
                    new += 1
            if not rows or (page > 1 and new == 0 and page > 10):
                pass
            pages = (data.get("skills") or {}).get("pages") or {}
            lp = pages.get("last_page") or 0
            if page % 50 == 0:
                log(f"fill pass page {page}/{lp}: {len(items)} unique", SCRIPT)
            if not rows or page >= lp:
                break
            page += 1
        log(f"after fill pass: {len(items)} unique", SCRIPT)
    return list(items.values())


def harvest() -> None:
    state = load_state("qoder")
    state.setdefault("done", {})
    state.setdefault("failed", {})
    state.setdefault("index", [])

    if not state["index"]:
        items = fetch_index()
        state["index"] = items
        save_state("qoder", state)
    items = state["index"]
    log(f"index loaded: {len(items)} skills; done so far: {len(state['done'])}",
        SCRIPT)

    def retryable(item: dict) -> bool:
        sid = item.get("skill_id")
        if sid in state["done"]:
            return False
        return state["failed"].get(sid, {}).get("attempts", 0) < 3

    todo = [it for it in items if retryable(it)]
    log(f"details to fetch: {len(todo)}", SCRIPT)

    def do_skill(item: dict) -> dict:
        sid = item["skill_id"]
        name = item.get("skill_name") or sid
        # 1) detail endpoint (readme_content = full SKILL.md)
        content = None
        detail_meta = {}
        try:
            d = http_get_json(DETAIL_URL.format(sid=sid), timeout=40)
            detail_meta = {
                "version": d.get("version"),
                "download_url": d.get("download_url"),
                "file_tree": summarize_tree(d.get("file_tree")),
                "category_detail": d.get("category"),
                "tags": d.get("tags"),
                "updated_at": d.get("updated_at"),
            }
            rc = d.get("readme_content")
            if isinstance(rc, str) and rc.strip():
                content = rc
        except Exception as exc:  # noqa: BLE001
            detail_meta["detail_error"] = str(exc)
        # 2) fallback: per-file endpoint
        if content is None:
            try:
                f = http_get_json(FILE_URL.format(sid=sid), timeout=40)
                if isinstance(f.get("content"), str) and f["content"].strip():
                    content = f["content"]
            except Exception as exc:  # noqa: BLE001
                detail_meta["file_error"] = str(exc)
        if content is None:
            return {"result": None, "meta": detail_meta}

        meta, _ = parse_frontmatter(content)
        if not meta.get("name") or not meta.get("description"):
            inject = []
            if not meta.get("name"):
                inject.append(f"name: {name}")
            if not meta.get("description"):
                desc = (item.get("description") or "").replace("\n", " ").strip()
                inject.append(f"description: {desc or name}")
            if inject:
                if content.startswith("---"):
                    end = content.find("\n---", 3)
                    if end != -1:
                        content = (content[:end] + "\n" + "\n".join(inject)
                                   + content[end:])
                else:
                    content = "---\n" + "\n".join(inject) + "\n---\n\n" + content

        dest = os.path.join(OUT_ROOT,
                            f"{sanitize_dirname(sid, 40)}__{sanitize_dirname(name, 60)}")
        write_skill(dest, "SKILL.md", content.encode("utf-8"))
        return {"result": {"path": dest.replace(os.sep, "/"),
                           "bytes": len(content.encode("utf-8")),
                           "name": name, **detail_meta},
                "meta": detail_meta}

    n = 0
    for item, payload, exc in parallel(todo, do_skill, workers=24,
                                       desc="qoder skills", script=SCRIPT,
                                       log_every=1000):
        sid = item["skill_id"]
        if exc is not None:
            payload = {"result": None, "meta": {"error": str(exc)}}
        result = payload.get("result")
        meta = payload.get("meta")
        if result is None:
            prev = state["failed"].get(sid, {})
            entry = dict(meta or {})
            entry["attempts"] = prev.get("attempts", 0) + 1
            state["failed"][sid] = entry
            state["done"].pop(sid, None)
        else:
            state["done"][sid] = result
            state["failed"].pop(sid, None)
        n += 1
        if n % 2000 == 0:
            save_state("qoder", state)

    save_state("qoder", state)
    log(f"qoder harvest: {len(state['done'])} ok, {len(state['failed'])} failed "
        f"of {len(items)} indexed", SCRIPT)

    with open(os.path.join("harvest-logs", "qoder_summary.txt"), "w") as fh:
        fh.write(f"indexed: {len(items)}\n")
        fh.write(f"extracted: {len(state['done'])}\n")
        fh.write(f"failed: {len(state['failed'])}\n")
        fh.write(f"failed ids sample: {list(state['failed'])[:200]}\n")


def summarize_tree(node, depth: int = 0) -> dict | None:
    if not node or not isinstance(node, dict):
        return None
    return {
        "name": node.get("name"),
        "path": node.get("path"),
        "type": node.get("type"),
        "size": node.get("size"),
        "children": (len(node.get("files") or [])
                     if node.get("type") == "directory" else 0),
    }


if __name__ == "__main__":
    harvest()
