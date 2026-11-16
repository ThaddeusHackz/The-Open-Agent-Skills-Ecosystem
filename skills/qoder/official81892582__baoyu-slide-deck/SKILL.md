---
name: baoyu-slide-deck
version: 1.0.0
description: Generates professional slide deck images from content. Creates outlines with style instructions, then generates individual slide images. Use when user asks to "create slides", "make a presentation", "generate deck", "slide deck", or "PPT".
description_zh: 从内容生成专业幻灯片图片。创建带有样式指令的大纲，然后生成单独的幻灯片图片。适用于"创建幻灯片"、"制作演示文稿"、"PPT"等场景。
category: content-creation
---

# Slide Deck Generator

Transform content into professional slide deck images.

## Usage

```bash
/baoyu-slide-deck path/to/content.md
/baoyu-slide-deck path/to/content.md --style sketch-notes
/baoyu-slide-deck path/to/content.md --audience executives
/baoyu-slide-deck path/to/content.md --lang zh
/baoyu-slide-deck path/to/content.md --slides 10
/baoyu-slide-deck path/to/content.md --outline-only
/baoyu-slide-deck  # Then paste content
```

## Script Directory

**Agent Execution Instructions**:
1. Determine this SKILL.md file's directory path as `SKILL_DIR`
2. Script path = `${SKILL_DIR}/scripts/<script-name>.ts`

| Script | Purpose |
|--------|---------|
| `scripts/merge-to-pptx.ts` | Merge slides into PowerPoint |
| `scripts/merge-to-pdf.ts` | Merge slides into PDF |

## Options

| Option | Description |
|--------|-------------|
| `--style <name>` | Visual style: preset name, `custom`, or custom style name |
| `--audience <type>` | Target: beginners, intermediate, experts, executives, general |
| `--lang <code>` | Output language (en, zh, ja, etc.) |
| `--slides <number>` | Target slide count (8-25 recommended, max 30) |
| `--outline-only` | Generate outline only, skip image generation |
| `--prompts-only` | Generate outline + prompts, skip images |
| `--images-only` | Generate images from existing prompts directory |
| `--regenerate <N>` | Regenerate specific slide(s): `--regenerate 3` or `--regenerate 2,5,8` |

**Slide Count by Content Length**:
| Content | Slides |
|---------|--------|
| < 1000 words | 5-10 |
| 1000-3000 words | 10-18 |
| 3000-5000 words | 15-25 |
| > 5000 words | 20-30 (consider splitting) |

## Style System

### Presets

| Preset | Dimensions | Best For |
|--------|------------|----------|
| `blueprint` (Default) | grid + cool + technical + balanced | Architecture, system design |
| `chalkboard` | organic + warm + handwritten + balanced | Education, tutorials |
| `corporate` | clean + professional + geometric + balanced | Investor decks, proposals |
| `minimal` | clean + neutral + geometric + minimal | Executive briefings |
| `sketch-notes` | organic + warm + handwritten + balanced | Educational, tutorials |
| `watercolor` | organic + warm + humanist + minimal | Lifestyle, wellness |
| `dark-atmospheric` | clean + dark + editorial + balanced | Entertainment, gaming |
| `notion` | clean + neutral + geometric + dense | Product demos, SaaS |
| `bold-editorial` | clean + vibrant + editorial + balanced | Product launches, keynotes |
| `editorial-infographic` | clean + cool + editorial + dense | Tech explainers, research |
| `fantasy-animation` | organic + vibrant + handwritten + minimal | Educational storytelling |
| `intuition-machine` | clean + cool + technical + dense | Technical docs, academic |
| `pixel-art` | pixel + vibrant + technical + balanced | Gaming, developer talks |
| `scientific` | clean + cool + technical + dense | Biology, chemistry, medical |
| `vector-illustration` | clean + vibrant + humanist + balanced | Creative, children's content |
| `vintage` | paper + warm + editorial + balanced | Historical, heritage |

### Style Dimensions

| Dimension | Options | Description |
|-----------|---------|-------------|
| **Texture** | clean, grid, organic, pixel, paper | Visual texture and background treatment |
| **Mood** | professional, warm, cool, vibrant, dark, neutral | Color temperature and palette style |
| **Typography** | geometric, humanist, handwritten, editorial, technical | Headline and body text styling |
| **Density** | minimal, balanced, dense | Information density per slide |

Full specs: `references/dimensions/*.md`

### Auto Style Selection

| Content Signals | Preset |
|-----------------|--------|
| tutorial, learn, education, guide, beginner | `sketch-notes` |
| classroom, teaching, school, chalkboard | `chalkboard` |
| architecture, system, data, analysis, technical | `blueprint` |
| creative, children, kids, cute | `vector-illustration` |
| briefing, academic, research, bilingual | `intuition-machine` |
| executive, minimal, clean, simple | `minimal` |
| saas, product, dashboard, metrics | `notion` |
| investor, quarterly, business, corporate | `corporate` |
| launch, marketing, keynote, magazine | `bold-editorial` |
| entertainment, music, gaming, atmospheric | `dark-atmospheric` |
| explainer, journalism, science communication | `editorial-infographic` |
| story, fantasy, animation, magical | `fantasy-animation` |
| gaming, retro, pixel, developer | `pixel-art` |
| biology, chemistry, medical, scientific | `scientific` |
| history, heritage, vintage, expedition | `vintage` |
| lifestyle, wellness, travel, artistic | `watercolor` |
| Default | `blueprint` |

## Design Philosophy

Decks designed for **reading and sharing**, not live presentation:
- Each slide self-explanatory without verbal commentary
- Logical flow when scrolling
- All necessary context within each slide
- Optimized for social media sharing

See `references/design-guidelines.md` for:
- Audience-specific principles
- Visual hierarchy
- Content density guidelines
- Color and typography selection
- Font recommendations

See `references/layouts.md` for layout options.

## File Management

### Output Directory

```
slide-deck/{topic-slug}/
├── source-{slug}.{ext}
├── outline.md
├── prompts/
│   └── 01-slide-cover.md, 02-slide-{slug}.md, ...
├── 01-slide-cover.png, 02-slide-{slug}.png, ...
├── {topic-slug}.pptx
└── {topic-slug}.pdf
```

**Slug**: Extract topic (2-4 words, kebab-case). Example: "Introduction to Machine Learning" → `intro-machine-learning`

**Conflict Handling**: See Step 1.3 for existing content detection and user options.

## Language Handling

**Detection Priority**:
1. `--lang` flag (explicit)
2. EXTEND.md `language` setting
3. User's conversation language (input language)
4. Source content language

**Rule**: ALL responses use user's preferred language:
- Questions and confirmations
- Progress reports
- Error messages
- Completion summaries

Technical terms (style names, file paths, code) remain in English.

## Workflow

Copy this checklist and check off items as you complete them:

```
Slide Deck Progress:
- [ ] Step 1: Setup & Analyze
  - [ ] 1.1 Load preferences
  - [ ] 1.2 Analyze content
  - [ ] 1.3 Check existing ⚠️ REQUIRED
- [ ] Step 2: Confirmation ⚠️ REQUIRED (Round 1, optional Round 2)
- [ ] Step 3: Generate outline
- [ ] Step 4: Review outline (conditional)
- [ ] Step 5: Generate prompts
- [ ] Step 6: Review prompts (conditional)
- [ ] Step 7: Generate images
- [ ] Step 8: Merge to PPTX/PDF
- [ ] Step 9: Output summary
```

### Flow

```
Input → Preferences → Analyze → [Check Existing?] → Confirm (1-2 rounds) → Outline → [Review Outline?] → Prompts → [Review Prompts?] → Images → Merge → Complete
```

### Step 1: Setup & Analyze

**1.1 Load Preferences (EXTEND.md)**

Use Bash to check EXTEND.md existence (priority order):

```bash
# Check project-level first
test -f .baoyu-skills/baoyu-slide-deck/EXTEND.md && echo "project"

# Then user-level (cross-platform: $HOME works on macOS/Linux/WSL)
test -f "$HOME/.baoyu-skills/baoyu-slide-deck/EXTEND.md" && echo "user"
```

┌──────────────────────────────────────────────────┬───────────────────┐
│                       Path                       │     Location      │
├──────────────────────────────────────────────────┼───────────────────┤
│ .baoyu-skills/baoyu-slide-deck/EXTEND.md         │ Project directory │
├──────────────────────────────────────────────────┼───────────────────┤
│ $HOME/.baoyu-skills/baoyu-slide-deck/EXTEND.md   │ User home         │
└──────────────────────────────────────────────────┴───────────────────┘

**When EXTEND.md Found** → Read, parse, **output summary to user**:

```
📋 Loaded preferences from [full path]
├─ Style: [preset/custom name]
├─ Audience: [audience or "auto-detect"]
├─ Language: [language or "auto-detect"]
└─ Review: [enabled/disabled]
```

**When EXTEND.md Not Found** → First-time setup using AskUserQuestion or proceed with defaults.

**EXTEND.md Supports**: Preferred style | Custom dimensions | Default audience | Language preference | Review preference

Schema: `references/config/preferences-schema.md`

**1.2 Analyze Content**

1. Save source content (if pasted, save as `source.md`)
   - **Backup rule**: If `source.md` exists, rename to `source-backup-YYYYMMDD-HHMMSS.md`
2. Follow `references/analysis-framework.md` for content analysis
3. Analyze content signals for style recommendations
4. Detect source language
5. Determine recommended slide count
6. Generate topic slug from content

**1.3 Check Existing Content** ⚠️ REQUIRED

**MUST execute before proceeding to Step 2.**

Use Bash to check if output directory exists:

```bash
test -d "slide-deck/{topic-slug}" && echo "exists"
```

**If directory exists**, use AskUserQuestion:

```
header: "Existing"
question: "Existing content found. How to proceed?"
options:
  - label: "Regenerate outline"
    description: "Keep images, regenerate outline only"
  - label: "Regenerate images"
    description: "Keep outline, regenerate images only"
  - label: "Backup and regenerate"
    description: "Backup to {slug}-backup-{timestamp}, then regenerate all"
  - label: "Exit"
    description: "Cancel, keep existing content unchanged"
```

**Save to `analysis.md`** with:
- Topic, audience, content signals
- Recommended style (based on Auto Style Selection)
- Recommended slide count
- Language detection

### Step 2: Confirmation ⚠️ REQUIRED

**Two-round confirmation**: Round 1 always, Round 2 only if "Custom dimensions" selected.

**Language**: Use user's input language or saved language preference.

**Display summary**:
- Content type + topic identified
- Language: [from EXTEND.md or detected]
- **Recommended style**: [preset] (based on content signals)
- **Recommended slides**: [N] (based on content length)

#### Round 1 (Always)

**Use AskUserQuestion** for all 5 questions:

**Question 1: Style**
```
header: "Style"
question: "Which visual style for this deck?"
options:
  - label: "{recommended_preset} (Recommended)"
    description: "Best match based on content analysis"
  - label: "{alternative_preset}"
    description: "[alternative style description]"
  - label: "Custom dimensions"
    description: "Choose texture, mood, typography, density separately"
```

**Question 2: Audience**
```
header: "Audience"
question: "Who is the primary reader?"
options:
  - label: "General readers (Recommended)"
    description: "Broad appeal, accessible content"
  - label: "Beginners/learners"
    description: "Educational focus, clear explanations"
  - label: "Experts/professionals"
    description: "Technical depth, domain knowledge"
  - label: "Executives"
    description: "High-level insights, minimal detail"
```

**Question 3: Slide Count**
```
header: "Slides"
question: "How many slides?"
options:
  - label: "{N} slides (Recommended)"
    description: "Based on content length"
  - label: "Fewer ({N-3} slides)"
    description: "More condensed, less detail"
  - label: "More ({N+3} slides)"
    description: "More detailed breakdown"
```

**Question 4: Review Outline**
```
header: "Outline"
question: "Review outline before generating prompts?"
options:
  - label: "Yes, review outline (Recommended)"
    description: "Review slide titles and structure"
  - label: "No, skip outline review"
    description: "Proceed directly to prompt generation"
```

**Question 5: Review Prompts**
```
header: "Prompts"
question: "Review prompts before generating images?"
options:
  - label: "Yes, review prompts (Recommended)"
    description: "Review image generation prompts"
  - label: "No, skip prompt review"
    description: "Proceed directly to image generation"
```

#### Round 2 (Only if "Custom dimensions" selected)

**Use AskUserQuestion** for all 4 dimensions:

**Question 1: Texture**
```
header: "Texture"
question: "Which visual texture?"
options:
  - label: "clean"
    description: "Pure solid color, no texture"
  - label: "grid"
    description: "Subtle grid overlay, technical"
  - label: "organic"
    description: "Soft textures, hand-drawn feel"
  - label: "pixel"
    description: "Chunky pixels, 8-bit aesthetic"
```
(Note: "paper" available via Other)

**Question 2: Mood**
```
header: "Mood"
question: "Which color mood?"
options:
  - label: "professional"
    description: "Cool-neutral, navy/gold"
  - label: "warm"
    description: "Earth tones, friendly"
  - label: "cool"
    description: "Blues, grays, analytical"
  - label: "vibrant"
    description: "High saturation, bold"
```
(Note: "dark", "neutral" available via Other)

**Question 3: Typography**
```
header: "Typography"
question: "Which typography style?"
options:
  - label: "geometric"
    description: "Modern sans-serif, clean"
  - label: "humanist"
    description: "Friendly, readable"
  - label: "handwritten"
    description: "Marker/brush, organic"
  - label: "editorial"
    description: "Magazine style, dramatic"
```
(Note: "technical" available via Other)

**Question 4: Density**
```
header: "Density"
question: "Information density?"
options:
  - label: "balanced (Recommended)"
    description: "2-3 key points per slide"
  - label: "minimal"
    description: "One focus point, maximum whitespace"
  - label: "dense"
    description: "Multiple data points, compact"
```

**After Round 2**: Store custom dimensions as the style configuration.

**After Confirmation**:
1. Update `analysis.md` with confirmed preferences
2. Store `skip_outline_review` flag from Question 4
3. Store `skip_prompt_review` flag from Question 5
4. → Step 3

### Step 3: Generate Outline

Create outline using the confirmed style from Step 2.

**Style Resolution**:
- If preset selected → Read `references/styles/{preset}.md`
- If custom dimensions → Read dimension files from `references/dimensions/` and combine

**Generate**:
1. Follow `references/outline-template.md` for structure
2. Build STYLE_INSTRUCTIONS from style or dimensions
3. Apply confirmed audience, language, slide count
4. Save as `outline.md`

**After generation**:
- If `--outline-only`, stop here
- If `skip_outline_review` is true → Skip Step 4, go to Step 5
- If `skip_outline_review` is false → Continue to Step 4

### Step 4: Review Outline (Conditional)

**Skip this step** if user selected "No, skip outline review" in Step 2.

**Purpose**: Review outline structure before prompt generation.

**Language**: Use user's input language or saved language preference.

**Display**:
- Total slides: N
- Style: [preset name or "custom: texture+mood+typography+density"]
- Slide-by-slide summary table:

```
| # | Title | Type | Layout |
|---|-------|------|--------|
| 1 | [title] | Cover | title-hero |
| 2 | [title] | Content | [layout] |
| 3 | [title] | Content | [layout] |
| ... | ... | ... | ... |
```

**Use AskUserQuestion**:
```
header: "Confirm"
question: "Ready to generate prompts?"
options:
  - label: "Yes, proceed (Recommended)"
    description: "Generate image prompts"
  - label: "Edit outline first"
    description: "I'll modify outline.md before continuing"
  - label: "Regenerate outline"
    description: "Create new outline with different approach"
```

**After response**:
1. If "Edit outline first" → Inform user to edit `outline.md`, ask again when ready
2. If "Regenerate outline" → Back to Step 3
3. If "Yes, proceed" → Continue to Step 5

### Step 5: Generate Prompts

1. Read `references/base-prompt.md`
2. For each slide in outline:
   - Extract STYLE_INSTRUCTIONS from outline (not from style file again)
   - Add slide-specific content
   - If `Layout:` specified, include layout guidance from `references/layouts.md`
3. Save to `prompts/` directory
   - **Backup rule**: If prompt file exists, rename to `prompts/NN-slide-{slug}-backup-YYYYMMDD-HHMMSS.md`

**After generation**:
- If `--prompts-only`, stop here and output prompt summary
- If `skip_prompt_review` is true → Skip Step 6, go to Step 7
- If `skip_prompt_review` is f