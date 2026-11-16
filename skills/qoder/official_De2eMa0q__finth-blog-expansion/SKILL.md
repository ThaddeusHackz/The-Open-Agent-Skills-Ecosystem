---
name: finth-blog-expansion
description: FINTH Day 5 — Blog expansion: expand 3 approved LinkedIn articles into full WordPress-ready blog posts
---

You are the FINTH content production engine. Read the project instruction file first before doing anything else.

PROJECT INSTRUCTION FILE:
~/Library/Mobile Documents/com~apple~CloudDocs/CoWork_Projects/FINTH/Content Center/FINTH — Content center/00-Brand-Foundations/COWORK_PROJECT_INSTRUCTION.md

BASE FOLDER (all reads and writes happen here):
~/Library/Mobile Documents/com~apple~CloudDocs/CoWork_Projects/FINTH/Content Center/FINTH — Content center/

This is the DAY 5 BLOG EXPANSION task.

## Step 1 — Read context

Read in this order:
1. 00-Brand-Foundations/BRAND_BRIEF.md
2. 00-Brand-Foundations/image-prompt-system.md
3. 08-Scheduled-Outputs/Articles-[current month]-[year].md
4. 09-Blog-finth-co/seo-keyword-map.md

## Step 2 — Read Corey skills files

Before drafting, read these skill files:
- /Users/apichaichiarakul/marketingskills/skills/copywriting/SKILL.md
- /Users/apichaichiarakul/marketingskills/skills/content-strategy/SKILL.md
- /Users/apichaichiarakul/marketingskills/skills/customer-research/SKILL.md
- /Users/apichaichiarakul/marketingskills/skills/ai-seo/SKILL.md

AI SEO skill requirements:
- First paragraph must be a self-contained answer block quotable by AI overview
- Include at least one statistic with source inline
- Use structured numbered sequences that AI can extract
- Bold key diagnostic questions

## Step 3 — Expand each article to full blog post (1,200-1,500 words)

Expand from the LinkedIn article by:
- Deepening the opening scene into a full paragraph
- Adding one practical framework or diagnostic the article only implied
- Adding the counterintuitive insight or advantage section
- Adding a structured diagnostic for readers already in the problem
- Strengthening the conviction close

Each blog post delivered in exactly three layers:

---

LAYER 1 — WORDPRESS METADATA

```
Title:            [article title — focus keyphrase in first 6 words]
Focus Keyphrase:  [primary keyword from seo-keyword-map.md]
Meta Description: [140-155 chars exactly — factual, no hype, no em dashes]
Slug:             [hyphenated-lowercase-url]
Secondary Keyphrases: [kw1] | [kw2] | [kw3]
Excerpt:          [2-3 sentences — first paragraph quotable by AI overview]
Featured Image:   [FULL image prompt — complete base template from correct scenario in image-prompt-system.md PLUS all variable fields filled in for this specific piece. Never abbreviated. Never a one-sentence description. Copy the full prompt from the planning file image prompt for this piece.]
Tags:             [comma-separated, hyphenated, lowercase]
Category:         [pillar name]
```

LAYER 2 — ARTICLE CONTENT (clean HTML — paste directly into WordPress content area)

```html
<h1>[Title]</h1>
<p>[Opening — self-contained, quotable by AI, no em dashes]</p>
<h2>[Section 1]</h2>
<p>...</p>
<h3>[Subsection if needed]</h3>
<p>...</p>
<h2>[Section 2]</h2>
<p>...</p>
<h2>[Section 3]</h2>
<p>...</p>
<h2>[Closing section]</h2>
<p>...</p>
<p>Further reading: <a href="/insights/[slug]">[related article 1]</a> and <a href="/insights/[slug]">[related article 2]</a>.</p>
```

Rules for Layer 2:
- No inline styles on article content
- H1 for title, H2 for main sections, H3 for subsections only
- Bold for key diagnostic questions or critical statements only
- Ordered lists for sequences, unordered lists for parallel items
- Internal links to at least 2 related articles
- No em dashes anywhere
- British English, sentence case

LAYER 3 — CTA BLOCK (paste after Layer 2)

```html
<div style="background: #e8dec5; padding: 24px; margin-top: 30px; border-left: 4px solid #272d4f;">
  <h3 style="margin-top: 0; color: #111111;">[CTA headline — specific offer]</h3>
  <p style="color: #111111;">[CTA body — 1-2 sentences, specific, no hype]</p>
  <a href="https://finth.co/contact" style="color: #e95c4b; text-decoration: none; font-weight: 500;">[Link text]</a>
</div>
```

---

## Step 4 — Update Notion

For all 3 blog post rows in the content calendar database (data_source_id: 8a1fb44e-765e-4642-b294-cb3ab9066b19):
- Update Status to "In progress"
- Update publish date to 48-72 hours after the corresponding LinkedIn article date
- Update Word Count with actual word count

## Step 5 — Save output

Save each blog as a separate file:
- 08-Scheduled-Outputs/Blog-[Month]-[Year]-1.md
- 08-Scheduled-Outputs/Blog-[Month]-[Year]-2.md
- 08-Scheduled-Outputs/Blog-[Month]-[Year]-3.md

Also save a copy of each approved blog to: 09-Blog-finth-co/drafts/[YYYY-MM-DD]_blog_[slug].md

Report back with: word counts per blog, Notion rows updated, Featured Image scenario used per piece.