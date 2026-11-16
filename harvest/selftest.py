#!/usr/bin/env python3
"""Endpoint self-test, run from the GitHub Actions runner (unrestricted egress).

Proves every data source the harvest depends on before we spend hours on it.
"""
import json
import sys
import urllib.request

FAILURES = []


def get(url, timeout=30, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent": "harvest-selftest/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, resp.read()


LOG_LINES = []


def check(name, fn):
    try:
        detail = fn()
        line = f"PASS  {name} :: {detail}"
    except Exception as exc:  # noqa: BLE001
        import traceback
        FAILURES.append(name)
        line = f"FAIL  {name} :: {exc}\n{traceback.format_exc()}"
    print(line)
    LOG_LINES.append(line)


def t_skills_leaderboard():
    status, body = get("https://www.skills.sh/api/skills/all-time/1")
    data = json.loads(body)
    n = len(data.get("skills", []))
    assert status == 200 and n > 0, f"status={status} n={n}"
    return f"{n} rows on page 1"


def t_skills_sitemap():
    status, body = get("https://www.skills.sh/sitemap-skills-1.xml")
    assert status == 200 and b"<url>" in body, f"status={status}"
    return f"{body.count(b'<loc>')} urls in sitemap-skills-1"


def t_skills_detail_api():
    # Public (undocumented) detail endpoint candidates.
    candidates = [
        "https://www.skills.sh/api/skills/vercel-labs/skills/find-skills",
        "https://www.skills.sh/api/skill/vercel-labs/skills/find-skills",
    ]
    errs = []
    for url in candidates:
        try:
            status, body = get(url)
            if status == 200 and b"SKILL" in body.upper():
                return f"{url} -> {len(body)} bytes"
            errs.append(f"{url} status={status}")
        except Exception as exc:  # noqa: BLE001
            errs.append(f"{url} {exc}")
    raise RuntimeError("; ".join(errs))


def t_skills_page_html():
    status, body = get("https://www.skills.sh/vercel-labs/skills/find-skills")
    assert status == 200 and b"SKILL" in body, f"status={status}"
    return f"{len(body)} bytes html"


def t_qoder_index():
    url = ("https://qoder.com/apphub/api/v1/marketplace/catalog/extensions"
           "?extension_types=skill&pagination.current_page=1&pagination.page_size=50")
    status, body = get(url)
    data = json.loads(body)
    pages = data["skills"]["pages"]
    assert status == 200 and pages["total_size"] > 0
    return f"total_size={pages['total_size']} last_page={pages['last_page']} items={len(data['skills']['items'])}"


def t_qoder_detail():
    url = "https://qoder.com/apphub/api/v1/marketplace/skills/official03866510/detail"
    status, body = get(url)
    data = json.loads(body)
    assert status == 200 and data.get("readme_content"), f"status={status}"
    return f"readme={len(data['readme_content'])}B download_url={'yes' if data.get('download_url') else 'no'}"


def t_codeload():
    status, body = get("https://codeload.github.com/vercel-labs/skills/tar.gz/refs/heads/main", timeout=60)
    assert status == 200 and body[:2] == b"\x1f\x8b", f"status={status} magic={body[:2]!r}"
    return f"{len(body)} bytes tarball"


def main():
    check("skills.sh leaderboard API", t_skills_leaderboard)
    check("skills.sh sitemap", t_skills_sitemap)
    check("skills.sh detail API", t_skills_detail_api)
    check("skills.sh skill page html", t_skills_page_html)
    check("qoder catalog index", t_qoder_index)
    check("qoder skill detail", t_qoder_detail)
    check("codeload.github.com tarballs", t_codeload)

    import os
    os.makedirs("harvest-logs", exist_ok=True)
    with open("harvest-logs/selftest.txt", "w") as fh:
        fh.write("\n".join(LOG_LINES) + "\n")

    if FAILURES:
        print(f"\n{len(FAILURES)} endpoint(s) failed: {', '.join(FAILURES)}")
        sys.exit(1)
    print("\nAll endpoints OK.")


if __name__ == "__main__":
    main()
