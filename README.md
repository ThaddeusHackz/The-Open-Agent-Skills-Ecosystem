# The Open Agent Skills Ecosystem

> ## 🌐 Live website: **[skills.sh](https://www.skills.sh/)**
> The canonical, always-updated directory for this ecosystem lives at
> **[https://www.skills.sh/](https://www.skills.sh/)** — browse, rank, and
> install from the live leaderboard there. This repository is the complete,
> offline, importable mirror of it (plus the entire Qoder skills marketplace).

[![harvest](https://img.shields.io/badge/last%20harvest-see%20Actions%20log-blue)](../../actions)
[![skills.sh](https://img.shields.io/badge/live%20directory-skills.sh-success)](https://www.skills.sh/)

## What's inside

| Corpus | Skills | What it is |
|---|---:|---|
| `skills/skills-sh/` | **{{SKILLS_SH_COUNT}}** | Every skill indexed by [skills.sh](https://www.skills.sh/) — the open agent skills directory — as full `SKILL.md` packages, grouped `owner/repo/skill` |
| `skills/qoder/` | **{{QODER_COUNT}}** | The entire [Qoder](https://qoder.com) skills marketplace ({{QODER_COUNT_REPORTED}}+ skills at harvest time), each as a `SKILL.md` package |
| **Combined** | **{{COMBINED_COUNT}}** | Importable into any agent with one command |

Every skill is a standard agent-skill folder: a `SKILL.md` with YAML
frontmatter (`name`, `description`) plus any small supporting files that came
with it — the exact format Claude Code, Cursor, Codex, Qoder, Copilot, Gemini,
Windsurf, and 15+ other agents load natively.

## Import all skills into any agent

```bash
# See every supported agent and where it reads skills from
python3 tools/import_skills.py --list-agents

# Preview what would be installed
python3 tools/import_skills.py --list --source qoder --top 20

# Install the 500 most-installed skills.sh skills into Claude Code
python3 tools/import_skills.py --agent claude --source skills-sh --top 500

# Install EVERYTHING into the universal cross-agent directory (~/.agents/skills)
python3 tools/import_skills.py --agent universal --all

# One-liner with no tooling: plain copy works too
mkdir -p ~/.agents/skills && cp -r skills/qoder/* skills/skills-sh/* ~/.agents/skills/
```

Supported targets include `claude`, `cursor`, `codex`, `copilot`, `vscode`,
`windsurf`, `gemini`, `qoder`, `cline`, `amp`, `goose`, `kilo`, `kiro`,
`opencode`, `roo`, `trae`, `zed`, `droid`, `openclaw`, `antigravity`, and the
universal `~/.agents/skills` standard — each with `--scope user|project`.

Filter with `--name-sub`, `--min-installs`, `--category`, `--top`, `--limit`,
or target one skill with `--skill <id>`.

## Repository layout

```
skills/
  skills-sh/<owner>/<repo>/<skill>/SKILL.md   # skills.sh directory mirror
  skills-sh/site/<domain>/<skill>/SKILL.md    # non-GitHub skills.sh sources
  qoder/<skill-id>__<name>/SKILL.md           # Qoder marketplace mirror
catalog/
  index.json        # coverage, totals, provenance summary
  skills-sh.json    # every skills.sh skill: id, installs, path, sha256
  qoder.json        # every Qoder skill: id, author, category, installs, path
forensics/
  report.md         # forensic scan of the whole corpus
  findings.jsonl    # one line per finding (severity, rule, file, excerpt)
  stats.json        # machine-readable totals
tools/
  import_skills.py  # import into any agent
harvest/            # the pipeline that builds all of the above
site/               # static landing page → points at skills.sh
```

## Forensic scan

`harvest/forensics.py` runs a full forensic pass over **every** `SKILL.md`:

- **Structural validation** — frontmatter present, name/description set,
  non-empty body, valid UTF-8, truncation detection
- **20+ abuse rules** — remote-payload-into-shell, decode-and-eval, webhook
  exfiltration, secret-harvesting + outbound transfer, reverse shells,
  prompt-injection phrasing, concealment language, anti-forensics,
  zero-width characters, opaque base64 blobs, homoglyph names
- **Duplicate clustering** — SHA-256 clusters across both corpora, including
  cross-source duplicates

Read **[forensics/report.md](forensics/report.md)** for the full report.
Rules are triage signals, not verdicts — review context before condemning.

## Live website

The project's live website is **[https://www.skills.sh/](https://www.skills.sh/)**:

- Leaderboard: [skills.sh](https://www.skills.sh/) · [Trending](https://www.skills.sh/trending) · [Hot](https://www.skills.sh/hot)
- Install from anywhere: `npx skills add <owner/repo>`
- API docs: [skills.sh/docs/api](https://www.skills.sh/docs/api)

The static page in [`site/`](site/) is an optional mirror front-door that links
straight to the live directory.

## Provenance & attribution

- Skills are authored by their original authors and organizations. This repo
  **mirrors** them for offline use, auditing, and bulk import — it does not
  claim ownership of any skill.
- `catalog/*.json` records the source (repository or marketplace id), author,
  install counts, and content SHA-256 for every skill.
- Individual skills may carry their own licenses in accompanying files; check
  the skill folder and its upstream source before redistribution.

## Re-running the harvest

The corpus is built by the [`harvest`](.github/workflows/harvest.yml) GitHub
Actions workflow (endpoint self-test → skills.sh sitemap + leaderboard →
GitHub tarball extraction → Qoder marketplace sweep → forensic scan → catalog →
batched commits). It is idempotent and resumable via `.harvest_state/`; push a
change touching `harvest/**` to trigger it, or wait for the scheduled/manual
dispatch.
