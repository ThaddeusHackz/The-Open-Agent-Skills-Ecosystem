"""Shared utilities for the corpus harvest."""
from __future__ import annotations

import json
import os
import re
import tarfile
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO

UA = "open-agent-skills-ecosystem-harvest/1.0"
STATE_DIR = ".harvest_state"
LOG_DIR = "harvest-logs"

MAX_FILE_BYTES = 200_000       # per support file kept from GitHub tarballs
MAX_SKILL_BYTES = 1_000_000    # per extracted skill folder
MAX_HTTP_BYTES = 32 * 1024 * 1024

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", ".idea",
             ".vscode", ".next", "dist", "build", ".pytest_cache", ".mypy_cache"}
SKIP_FILES = {".DS_Store", "Thumbs.db"}

TEXT_EXTS = {".md", ".markdown", ".txt", ".py", ".js", ".mjs", ".cjs", ".ts",
             ".tsx", ".jsx", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg",
             ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd", ".rb",
             ".go", ".rs", ".java", ".kt", ".swift", ".c", ".h", ".cpp",
             ".hpp", ".cs", ".php", ".pl", ".r", ".sql", ".graphql", ".gql",
             ".env.example", ".csv", ".tsv", ".xml", ".html", ".htm", ".css",
             ".scss", ".svg", ".dockerfile", ".gitignore", ".editorconfig",
             ".license", ".rst", ".adoc", ".tex", ".bib", ".lua", ".ex", ".exs",
             ".clj", ".hs", ".ml", ".erl", ".zig", ".dart", ".vue", ".svelte"}


def log(msg: str, script: str = "harvest") -> None:
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    os.makedirs(LOG_DIR, exist_ok=True)
    with open(os.path.join(LOG_DIR, f"{script}.log"), "a") as fh:
        fh.write(line + "\n")


def http_get(url: str, *, timeout: int = 30, retries: int = 4,
             max_bytes: int = MAX_HTTP_BYTES,
             headers: dict | None = None) -> tuple[int, bytes]:
    hdrs = {"User-Agent": UA, "Accept": "*/*"}
    if headers:
        hdrs.update(headers)
    last: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read(max_bytes + 1)
                if len(data) > max_bytes:
                    raise ValueError(f"response exceeds {max_bytes} bytes: {url}")
                return resp.status, data
        except urllib.error.HTTPError as exc:
            if exc.code in (404, 410):
                return exc.code, b""
            if exc.code in (429, 500, 502, 503, 504):
                last = exc
            else:
                return exc.code, b""
        except Exception as exc:  # noqa: BLE001
            last = exc
        time.sleep(min(2 ** attempt * 0.5, 8) + 0.25 * attempt)
    raise RuntimeError(f"GET failed after {retries} tries: {url} :: {last}")


def http_get_json(url: str, **kw) -> dict:
    status, body = http_get(url, **kw)
    if status != 200 or not body:
        raise RuntimeError(f"HTTP {status} for {url}")
    return json.loads(body)


def parallel(iterable, fn, *, workers: int = 8, desc: str = "",
             script: str = "harvest", log_every: int = 500):
    """Run fn(item) over iterable with a thread pool; yields (item, result_or_exc)."""
    done = 0
    total = len(iterable) if hasattr(iterable, "__len__") else None
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futures = {pool.submit(fn, it): it for it in iterable}
        for fut in as_completed(futures):
            item = futures[fut]
            try:
                yield item, fut.result(), None
            except Exception as exc:  # noqa: BLE001
                yield item, None, exc
            done += 1
            if log_every and done % log_every == 0:
                t = f"{done}/{total}" if total else str(done)
                log(f"{desc}: {t} done", script)


def load_state(name: str) -> dict:
    path = os.path.join(STATE_DIR, f"{name}.json")
    if os.path.exists(path):
        with open(path) as fh:
            return json.load(fh)
    return {}


def save_state(name: str, obj: dict) -> None:
    os.makedirs(STATE_DIR, exist_ok=True)
    path = os.path.join(STATE_DIR, f"{name}.json")
    tmp = path + ".tmp"
    with open(tmp, "w") as fh:
        json.dump(obj, fh, ensure_ascii=False)
    os.replace(tmp, path)


def sanitize_dirname(name: str, max_len: int = 80) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", name).strip("-._")
    name = re.sub(r"-{2,}", "-", name)
    return (name or "unnamed")[:max_len]


def normalize_name(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def parse_frontmatter(text: str) -> tuple[dict, str]:
    """Minimal YAML frontmatter parser (flat key: value, plus folded lists)."""
    if not text.startswith("---"):
        return {}, text
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not m:
        return {}, text
    meta: dict = {}
    for line in m.group(1).splitlines():
        if not line or line[0] in " \t" or line.lstrip().startswith("#"):
            continue
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip("\"'")
    return meta, text[m.end():]


def is_text_path(path: str) -> bool:
    base = os.path.basename(path)
    if base in SKIP_FILES:
        return False
    if base.startswith(".env") or base in {"LICENSE", "Makefile", "Dockerfile",
                                           "CODEOWNERS", "NOTICE"}:
        return True
    ext = os.path.splitext(base)[1].lower()
    return ext in TEXT_EXTS or ext == ""


def extract_skill_from_tarball(data: bytes, skill_ids: set[str]) -> dict:
    """Extract skill folders from a repo tarball.

    Returns {skill_id: {files: {relpath: bytes}, matched_via: str}} for
    skills that could be located, plus 'unresolved' list.
    """
    out: dict = {"resolved": {}, "unresolved": [], "all_skillmd": []}
    tf = tarfile.open(fileobj=BytesIO(data), mode="r:gz")
    members = [m for m in tf.getmembers() if m.isfile()]

    # Index every SKILL.md in the archive.
    skillmds: list[tuple[str, str]] = []  # (dir_relpath, member_name)
    for m in members:
        parts = m.name.split("/")
        if any(p in SKIP_DIRS for p in parts):
            continue
        if os.path.basename(m.name).lower() in ("skill.md", "skill.mdx"):
            dir_rel = "/".join(parts[1:-1])  # strip codeload root dir
            skillmds.append((dir_rel, m.name))
    out["all_skillmd"] = [d for d, _ in skillmds]

    # Build lookup maps.
    by_dir: dict[str, list[str]] = {}
    by_fm: dict[str, list[str]] = {}
    for dir_rel, member in skillmds:
        by_dir.setdefault(normalize_name(os.path.basename(dir_rel) or "root"), []).append(member)
        try:
            fh = tf.extractfile(member)
            head = fh.read(4096).decode("utf-8", errors="replace") if fh else ""
        except Exception:  # noqa: BLE001
            head = ""
        meta, _ = parse_frontmatter(head)
        fm_name = meta.get("name")
        if fm_name:
            by_fm.setdefault(normalize_name(fm_name), []).append(member)

    def locate(skill_id: str) -> str | None:
        nid = normalize_name(skill_id)
        for table in (by_dir, by_fm):
            hits = table.get(nid, [])
            if hits:
                return sorted(hits, key=lambda p: (p.count("/"), len(p)))[0]
        # loose: frontmatter/dir containing the id
        for table in (by_dir, by_fm):
            for k, hits in table.items():
                if nid and (nid in k or k in nid) and len(k) >= 4:
                    return sorted(hits, key=lambda p: (p.count("/"), len(p)))[0]
        return None

    for skill_id in skill_ids:
        member = locate(skill_id)
        if not member:
            out["unresolved"].append(skill_id)
            continue
        root_dir = member.rsplit("/", 1)[0]
        files: dict[str, bytes] = {}
        total = 0

        def under_root(name: str) -> bool:
            if root_dir:
                return name.startswith(root_dir + "/")
            return True

        # Pass 1: SKILL.md itself (must never be dropped by the size budget).
        for m in members:
            if not under_root(m.name):
                continue
            if os.path.basename(m.name).lower() not in ("skill.md", "skill.mdx"):
                continue
            fh = tf.extractfile(m)
            if fh is None:
                continue
            rel = m.name[len(root_dir) + 1:] if root_dir else os.path.basename(m.name)
            data = fh.read()
            files[rel] = data
            total += len(data)

        # Pass 2: supporting files until the budget runs out.
        for m in members:
            if not under_root(m.name):
                continue
            if os.path.basename(m.name).lower() in ("skill.md", "skill.mdx"):
                continue
            rel = m.name[len(root_dir) + 1:] if root_dir else os.path.basename(m.name)
            if any(p in SKIP_DIRS for p in rel.split("/")):
                continue
            if not is_text_path(rel):
                continue
            if m.size > MAX_FILE_BYTES:
                continue
            if total + m.size > MAX_SKILL_BYTES:
                continue
            fh = tf.extractfile(m)
            if fh is None:
                continue
            files[rel] = fh.read()
            total += m.size
        if "SKILL.md" not in files and "skill.md" not in {f.lower(): f for f in files}:
            # ensure some SKILL.md landed
            if not any(os.path.basename(f).lower() == "skill.md" for f in files):
                out["unresolved"].append(skill_id)
                continue
        out["resolved"][skill_id] = {"files": files, "matched_via": member}
    tf.close()
    return out


SKILLMD_RSC_RE = re.compile(r'self\.__next_f\.push\(\[1,\s*"((?:[^"\\]|\\.)*)"\]\)')


def extract_skillmd_from_html(html: bytes) -> tuple[str | str | None, str]:
    """Pull the full SKILL.md text out of a skills.sh Next.js page.

    Returns (content_or_None, method).
    """
    text = html.decode("utf-8", errors="replace")

    # Strategy A: concatenate Next.js flight-data segments and slice the
    # region between the "SKILL.md" section marker and the "Show more" control.
    segs = SKILLMD_RSC_RE.findall(text)
    if segs:
        stream_parts = []
        for s in segs:
            try:
                stream_parts.append(json.loads('"' + s + '"'))
            except Exception:  # noqa: BLE001
                stream_parts.append(s.replace('\\"', '"').replace("\\n", "\n"))
        stream = "".join(stream_parts)
        idx = stream.find("Show more")
        if idx == -1:
            idx = stream.find("Related skills")
        if idx != -1:
            region = stream[:idx]
            # last section marker named SKILL.md before the content end
            markers = [m.start() for m in re.finditer(r"SKILL\.md", region)]
            for start in reversed(markers):
                chunk = region[start + len("SKILL.md"):]
                # content starts at first newline after marker
                nl = chunk.find("\n")
                if nl == -1:
                    continue
                body = chunk[nl + 1:]
                if body.lstrip().startswith("---"):
                    end = body.find("\n---", 3)
                    if end != -1:
                        candidate = body[:end + 4].lstrip("\n") + body[end + 4:]
                    else:
                        candidate = body
                else:
                    candidate = body
                candidate = candidate.strip("\x00")
                if len(candidate) >= 200 and ("\n# " in candidate or candidate.startswith("#")):
                    return candidate, "rsc-stream"
        # Fallback inside stream: grab from first H1 after last 'SKILL.md'
        m = re.search(r"SKILL\.md.{0,400}?(---\nname:.*?|#\s+\S.*)", stream, re.DOTALL)
        if m and len(m.group(1)) >= 200:
            return m.group(1), "rsc-regex"

    # Strategy B: raw HTML body region.
    m = re.search(r"SKILL\.md.*?<pre[^>]*>(.*?)</pre>", text, re.DOTALL)
    if m:
        import html as htmllib
        body = htmllib.unescape(m.group(1))
        if len(body) >= 200:
            return body, "pre-block"

    return None, "none"
