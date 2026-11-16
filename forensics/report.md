# Forensic Scan Report — Open Agent Skills Ecosystem

- **Files scanned:** 63,281 SKILL.md files (595.2 MB)
- **With valid frontmatter:** 63,215 (99.9%)
- **Clean files (no findings):** 60,073
- **Total findings:** 4,117

## Findings by severity

| Severity | Findings | Files affected |
|---|---:|---:|
| critical | 606 | 596 |
| high | 818 | 723 |
| medium | 899 | 801 |
| low | 1,794 | 1,088 |

## Findings by rule

| Rule | Hits | Severity | Description |
|---|---:|---|---|
| R014 | 1,472 | low | Environment credential identifier present |
| R006 | 720 | high | Secret harvesting + outbound transfer co-occurrence |
| R001 | 562 | critical | Pipe remote payload into a shell |
| R016 | 288 | low | Unsigned remote installer reference |
| S007 | 223 | medium | Homoglyph skill name |
| R011 | 212 | medium | Zero-width / invisible characters in content |
| R008 | 140 | medium | Prompt-injection phrasing (instruction override) |
| R015 | 118 | medium | Privilege escalation request |
| R005 | 79 | high | Webhook / request-catcher exfiltration endpoint |
| S005 | 66 | medium | Suspiciously short body (truncation?) |
| S001 | 66 | medium | Missing YAML frontmatter |
| R009 | 59 | medium | Concealment language (hide actions from the user) |
| R004 | 36 | critical | Destructive recursive delete of system/home paths |
| S003 | 33 | low | Missing description |
| R013 | 11 | medium | Download-then-execute sequence |
| S004 | 10 | high | Empty skill body |
| R007 | 9 | high | Raw socket reverse shell / netcat transfer |
| R003 | 5 | critical | base64 payload piped to shell |
| R010 | 4 | medium | Anti-forensics (clear history / logs) |
| R002 | 3 | critical | Decode-and-eval (obfuscated execution) |
| S002 | 1 | low | Missing name |

## Top critical/high findings (triage list)

| Sev | Rule | File | Why |
|---|---|---|---|
| critical | R001 | `skills/qoder/3e761ff9-009f-4ace-8e8a-3069130f67e1__alibabacloud-support/SKILL.md` | Pipe remote payload into a shell — `stall or upgrade with `brew install aliyun-cli` (macOS) or `curl -fsSL https://aliyuncli.a` |
| critical | R001 | `skills/qoder/767a37d4-8c0c-4338-8910-f39e555ed2f4__literature-review/SKILL.md` | Pipe remote payload into a shell — ` parallel-cli (PRIMARY — for web search and URL extraction) curl -fsSL https://parallel.ai` |
| critical | R001 | `skills/qoder/93f1344a-67ac-4b3e-841a-d570466e5e58__alibabacloud-workbench-cli/SKILL.md` | Pipe remote payload into a shell — `DATA}/bootstrap.log`. **Linux / macOS (manual):** ```bash curl -fsSL https://workbench-cli` |
| critical | R001 | `skills/qoder/a0581ef6-161b-4ef3-ad81-deb546e778ff__apify-actor-development/SKILL.md` | Pipe remote payload into a shell — `nstall the CLI by piping remote scripts to a shell > (e.g. `curl … | bash` or `irm … | iex` |
| critical | R001 | `skills/qoder/cfa3c2f8-5b38-4665-831d-0a3ca8fdac8e__antom-reconciliation-expert/SKILL.md` | Pipe remote payload into a shell — `l via one command: - **macOS / Linux (including WSL)**: `curl -fsSL https://mdn.alipayobje` |
| critical | R001 | `skills/qoder/d4329afb-e87b-44ef-a557-84bb4f69a736__enterprise-ai-data-governance/SKILL.md` | Pipe remote payload into a shell — `hain. Do not use unreviewed remote pipe installers such as `curl | sh`, `curl | bash`, or ` |
| critical | R001 | `skills/qoder/f0447c9a-0436-41dc-ab28-736e84baa962__lark-cli-guide/SKILL.md` | Pipe remote payload into a shell — `用户系统，或通过 `uname -s` 判断）： **Linux / WSL（推荐 nvm）：** ```bash curl -o- https://raw.githubuserc` |
| critical | R001 | `skills/qoder/f6ee6914-2109-44dd-a085-9a06b76d43bb__apify-actorization/SKILL.md` | Pipe remote payload into a shell — `nstall the CLI by piping remote scripts to a shell > (e.g. `curl ... | bash` or `irm ... |` |
| critical | R001 | `skills/qoder/official88441354__render-deploy/SKILL.md` | Pipe remote payload into a shell — ` to install: - macOS: `brew install render` - Linux/macOS: `curl -fsSL https://raw.githubu` |
| critical | R001 | `skills/qoder/official_00eKITsn__video-ad-specs/SKILL.md` | Pipe remote payload into a shell — `nce.sh](https://inference.sh) CLI. ## Quick Start ```bash curl -fsSL https://cli.inference` |
| critical | R001 | `skills/qoder/official_01CmB3zl__openclaw-dlp-guard/SKILL.md` | Pipe remote payload into a shell — `RE)` | "' OR 1=1 --" | | Command Injection | `[;&\|]\s*(rm\|wget\|curl\|nc\|bash\|sh\|pyth` |
| critical | R001 | `skills/qoder/official_0LcuMcnc__openclaw-insight/SKILL.md` | Pipe remote payload into a shell — `) Use the official one-click installation script: ```bash curl -fsSL https://raw.githubuse` |
| critical | R004 | `skills/qoder/official_0UJOaGhz__safe-shell-execution-claude-code/SKILL.md` | Destructive recursive delete of system/home paths — `ify → "May skip security hooks" ``` ### File System ``` rm -rf / rm -fr / rm -r -f / rm -f` |
| critical | R001 | `skills/qoder/official_1AVBunf6__ai-security-guard/SKILL.md` | Pipe remote payload into a shell — ` ### High（询问确认） | 模式 | 说明 | 示例 | |-----|------|------| | `curl | sh` | 远程脚本执行 | `curl url ` |
| critical | R001 | `skills/qoder/official_1FswK0du__peon-ping-openclaw/SKILL.md` | Pipe remote payload into a shell — ` peon status ``` If Homebrew is unavailable, use: ```bash curl -fsSL https://raw.githubuse` |
| critical | R001 | `skills/qoder/official_1M92Gt4m__devtools-secrets/SKILL.md` | Pipe remote payload into a shell — `n 2>/dev/null | head -1))" || echo "MISSING — install with: curl https://mise.run | sh"` -` |
| critical | R001 | `skills/qoder/official_1fvIwEmj__plume-notecard/SKILL.md` | Pipe remote payload into a shell — ` keys, and tokens - No remote code execution patterns like `curl | bash` - HTTPS-only down` |
| critical | R001 | `skills/qoder/official_1l6SlPMx__clawboard/SKILL.md` | Pipe remote payload into a shell — ` ### 1) Quick Scripted Install (recommended) Use: ```bash curl -fsSL https://raw.githubuse` |
| critical | R001 | `skills/qoder/official_1npvXETq__llm-data-automation/SKILL.md` | Pipe remote payload into a shell — `Internet Required) ### Using Ollama ```bash # Install curl -fsSL https://ollama.com/instal` |
| critical | R001 | `skills/qoder/official_22dQ8iTN__delneg-qwen-3-5-plus-video-feedback/SKILL.md` | Pipe remote payload into a shell — `irect HTTP URL. | | `uv: command not found` | macOS/Linux: `curl -LsSf https://astral.sh/u` |
| critical | R001 | `skills/qoder/official_25wK6jqh__alibabacloud-cloudbackup-ecs-file-backup-essential-edition/SKILL.md` | Pipe remote payload into a shell — `erify >= 3.3.3. If not installed or version too low, > run `curl -fsSL https://aliyuncli.a` |
| critical | R001 | `skills/qoder/official_2DVYnKEO__openclaw-sync-bridge/SKILL.md` | Pipe remote payload into a shell — `oken - 过期时友好提示重新申请 ## 安装 ### 自动安装 **Mac/Linux:** ```bash curl -fsSL https://clawhub.ai/Jay` |
| critical | R001 | `skills/qoder/official_2WUfnLyR__agi-terminal-helper/SKILL.md` | Pipe remote payload into a shell — `ll NOT do - I will not run remote “install scripts” (e.g., `curl | sh`) without explicit u` |
| critical | R001 | `skills/qoder/official_2bakXPam__majiayu000-creating-zed-extensions/SKILL.md` | Pipe remote payload into a shell — ` Development Workflow ### 1. Setup ```bash # Install Rust curl --proto '=https' --tlsv1.2 ` |
| critical | R001 | `skills/qoder/official_2hlh8qfD__evolv3-ai-iii/SKILL.md` | Pipe remote payload into a shell — `e. --- ## Quick Start ### 1. Install the Engine ```bash curl -fsSL https://install.iii.dev` |
| critical | R001 | `skills/qoder/official_2sOFk5mY__tesla-connect/SKILL.md` | Pipe remote payload into a shell — ` - teslacli install: - kind: shell cmd: "curl -fsSL https://raw.githubusercontent.com/Agen` |
| critical | R001 | `skills/qoder/official_30VixP8d__dicklesworthstone-mcp-skill-gen/SKILL.md` | Pipe remote payload into a shell — `t be installed. If not available, install with: ```bash curl -fsSL https://raw.githubuserc` |
| critical | R001 | `skills/qoder/official_36lw3IaV__balloob-ollama/SKILL.md` | Pipe remote payload into a shell — `alled, guide users to install it: **macOS/Linux:** ```bash curl -fsSL https://ollama.com/i` |
| critical | R001 | `skills/qoder/official_3GG65UOq__duclm1x1-claw-skill-guard/SKILL.md` | Pipe remote payload into a shell — ` It's Dangerous | |---------|------|-------------------| | `curl \| bash` | 🔴 CRITICAL | E` |
| critical | R001 | `skills/qoder/official_3hGgh6vW__carmandale-prove/SKILL.md` | Pipe remote payload into a shell — ` installed:** ```bash # Install elan (Lean version manager) curl https://raw.githubusercon` |
| critical | R001 | `skills/qoder/official_3tM7YJ2U__corespeed-pptx/SKILL.md` | Pipe remote payload into a shell — `", "kind": "shell", "command": "curl -fsSL https://deno.land/install.sh | sh", "bins": ["d` |
| critical | R001 | `skills/qoder/official_3wlACZmk__alibabacloud-sms-send-short-message/SKILL.md` | Pipe remote payload into a shell — `= 3.3.3. If not installed or the version > is too low, run `curl -fsSL https://aliyuncli.a` |
| critical | R001 | `skills/qoder/official_3wq0agN5__laurigates-hooks-permission-request-hook/SKILL.md` | Pipe remote payload into a shell — ` # Piped network execution if echo "$COMMAND" | grep -Eq '(curl|wget)\s.*\|\s*(bash|sh|zsh` |
| critical | R004 | `skills/qoder/official_3wq0agN5__laurigates-hooks-permission-request-hook/SKILL.md` | Destructive recursive delete of system/home paths — ` issue list` | — | | `deny` | — | `rm -rf /`, `rm -rf ~/`, `rm -rf $HOME`, `git push --for` |
| critical | R001 | `skills/qoder/official_4WE06LgP__qmind-knowledge/SKILL.md` | Pipe remote payload into a shell — `l. ### Script installation #### sh — macOS / Linux ```sh curl -fsSL https://download.qoder` |
| critical | R001 | `skills/qoder/official_4arjGPGQ__alibabacloud-sas-overview/SKILL.md` | Pipe remote payload into a shell — `erify >= 3.3.3. If not installed or version too low, > run `curl -fsSL https://aliyuncli.a` |
| critical | R001 | `skills/qoder/official_4fgRA1Vl__parallel-search/SKILL.md` | Pipe remote payload into a shell — `allel.ai](https://parallel.ai) 2. Install the CLI: ```bash curl -fsSL https://parallel.ai/` |
| critical | R001 | `skills/qoder/official_4kLzxfHJ__majiayu000-container-optimize/SKILL.md` | Pipe remote payload into a shell — `" RUN apk add --no-cache git curl \\" echo " && curl -sSL script.sh | sh \\" echo " && rm ` |
| critical | R004 | `skills/qoder/official_4kLzxfHJ__majiayu000-container-optimize/SKILL.md` | Destructive recursive delete of system/home paths — `"apt-get install" "$dockerfile"; then if ! grep -q "rm -rf /var/lib/apt/lists" "$dockerfil` |
| critical | R001 | `skills/qoder/official_4lqw3QMk__pupper0601-memory-manager/SKILL.md` | Pipe remote payload into a shell — `xt # 配置 OpenClaw 记忆系统 mm onboard --openclaw # 方法3: 一键安装脚本 curl -fsSL https://raw.githubuse` |

## Duplicate content clusters (top)

- Duplicate clusters: 2,856 (covering 6,933 files)
- Clusters spanning BOTH skills.sh and Qoder: 564

| Copies | Cluster (first paths) |
|---:|---|
| 26 | `skills/skills-sh/pixijs/pixijs-skills/pixijs-accessibility/SKILL.md`, `skills/skills-sh/pixijs/pixijs-skills/pixijs-application/SKILL.md`, `skills/skills-sh/pixijs/pixijs-skills/pixijs-assets/SKILL.md` (+23 more) |
| 18 | `skills/qoder/official_5z8b94kK__my-agent-browser/SKILL.md`, `skills/qoder/official_69IxBbpM__agent-browser-qw/SKILL.md`, `skills/qoder/official_9Qseke35__temp-agent-browser/SKILL.md` (+15 more) |
| 17 | `skills/qoder/official_0rRhB87c__clawhub-gstca/SKILL.md`, `skills/qoder/official_53uDnC9L__clawhub-hh1fd/SKILL.md`, `skills/qoder/official_E7jdzBtt__clawhub-6yr3b/SKILL.md` (+14 more) |
| 17 | `skills/qoder/official_11eXmgI0__diegosouzapw-convex-component-authoring-ihmorol/SKILL.md`, `skills/qoder/official_FwMa3dLg__diegosouzapw-convex-component-authoring-pratikkadam254/SKILL.md`, `skills/qoder/official_IRw7SEbi__diegosouzapw-convex-component-authoring-kristofferaas/SKILL.md` (+14 more) |
| 16 | `skills/qoder/official_29Kwqjjj__diegosouzapw-matchms-ricable/SKILL.md`, `skills/qoder/official_2cTh3e7R__diegosouzapw-matchms-pur3v4d3r/SKILL.md`, `skills/qoder/official_7Se94cgt__diegosouzapw-matchms-aiskillstore/SKILL.md` (+13 more) |
| 16 | `skills/skills-sh/longbridge/skills/longbridge-candlestick/SKILL.md`, `skills/skills-sh/longbridge/skills/longbridge-capital-flow/SKILL.md`, `skills/skills-sh/longbridge/skills/longbridge-chanlun/SKILL.md` (+13 more) |
| 14 | `skills/skills-sh/auth0/agent-skills/auth0-angular/SKILL.md`, `skills/skills-sh/auth0/agent-skills/auth0-expo/SKILL.md`, `skills/skills-sh/auth0/agent-skills/auth0-express/SKILL.md` (+11 more) |
| 13 | `skills/qoder/official_3BWD4POW__5kahoisaac-find-skills/SKILL.md`, `skills/qoder/official_C9TuSm25__kimyx0207-original/SKILL.md`, `skills/qoder/official_FlyBRbkh__new-slug/SKILL.md` (+10 more) |
| 13 | `skills/qoder/official_Hu3MqY79__majiayu000-5164e31c-9aa8-4cdb-a065-82e7bcce85d4/SKILL.md`, `skills/qoder/official_IYUb1gRs__boisenoise-composio-canvas-design/SKILL.md`, `skills/qoder/official_LhPdmM0f__nnllkk-canvas-design/SKILL.md` (+10 more) |
| 12 | `skills/qoder/official_20EAxvqD__self-improving-agent-3-0-0/SKILL.md`, `skills/qoder/official_2Wz77lhr__self-improving-agent-tmp/SKILL.md`, `skills/qoder/official_BYbTMK9M__l-yifan-self-improving/SKILL.md` (+9 more) |
| 12 | `skills/qoder/official_6NfKJQyD__duclm1x1-pro/SKILL.md`, `skills/qoder/official_6WmcgWEY__majiayu000-99-meta-skillcreator/SKILL.md`, `skills/qoder/official_ENwxUG7h__whysignup-aaaa/SKILL.md` (+9 more) |
| 12 | `skills/skills-sh/101-skills/superpowers/agent-browser/SKILL.md`, `skills/skills-sh/bankai-skills/superpowers/agent-browser/SKILL.md`, `skills/skills-sh/beltsh/superpowers/agent-browser/SKILL.md` (+9 more) |
| 12 | `skills/skills-sh/101-skills/superpowers/python-executor/SKILL.md`, `skills/skills-sh/bankai-skills/superpowers/python-executor/SKILL.md`, `skills/skills-sh/beltsh/superpowers/python-executor/SKILL.md` (+9 more) |
| 12 | `skills/skills-sh/101-skills/superpowers/remotion-render/SKILL.md`, `skills/skills-sh/bankai-skills/superpowers/remotion-render/SKILL.md`, `skills/skills-sh/beltsh/superpowers/remotion-render/SKILL.md` (+9 more) |
| 12 | `skills/skills-sh/101-skills/superpowers/web-search/SKILL.md`, `skills/skills-sh/bankai-skills/superpowers/web-search/SKILL.md`, `skills/skills-sh/beltsh/superpowers/web-search/SKILL.md` (+9 more) |

## Interpretation notes

- Rules are **heuristic triage signals**, not verdicts: a skill that legitimately documents `curl | sh` install steps will trip R001/R016 — review context before condemning.
- R006 fires when credential-looking identifiers and outbound HTTP calls co-occur; common in benign deploy skills, rare in pure knowledge skills.
- Duplicate clusters are expected: popular skill packs are forked across many repositories on skills.sh.

