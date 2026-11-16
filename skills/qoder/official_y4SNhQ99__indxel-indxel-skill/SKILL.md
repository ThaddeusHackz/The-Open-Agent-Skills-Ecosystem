---
name: indxel
version: 1.0.0
description: When the user wants to set up, configure, or fix SEO in a Next.js project using the indxel SDK and CLI. Also use when the user mentions "SEO setup," "meta tags," "structured data," "JSON-LD," "seo config," "seo check," "broken SEO," "metadata validation," "OG image," "canonical URL," or "defineSEO." For live site crawling, keyword research, or indexation, see indxel-pro.
---

# Indxel — SEO infrastructure for developers

You are an expert in using the **indxel** npm package and CLI to set up bulletproof SEO in Next.js projects. Indxel is "ESLint for SEO" — it validates metadata at build time so broken SEO never ships to production.

**Knowledge Base:** Before making SEO recommendations, consult `references/seo-knowledge-base.md` for the complete set of SEO best practices, critical rules, structured data patterns (@graph, sameAs), GEO optimization (AI-readiness, semantic HTML, llms.txt), rendering strategies, and Core Web Vitals thresholds. This ensures your advice goes beyond tool usage and reflects what actually matters for ranking in 2026.

## Before Starting

**Check if indxel is already set up:**
1. Look for `seo.config.ts` (or `seo.config.js`) at the project root
2. Check if `indxel` is in `package.json` dependencies
3. Check if pages already use `createMetadata()` or `generateMetadata()`

If not set up, start with initialization. If already set up, skip to the relevant section.

---

## 1. Installation & Init

### Install the package

```bash
npm install indxel
```

### Initialize the project

```bash
npx indxel init
```

This generates:
- `seo.config.ts` — Global SEO configuration
- `app/sitemap.ts` — Dynamic sitemap
- `app/robots.ts` — robots.txt configuration
- `public/<key>.txt` — IndexNow verification key

With git hook guard:
```bash
npx indxel init --hook
```

---

## 2. defineSEO() — Global Configuration

Create `seo.config.ts` at the project root:

```ts
import { defineSEO } from 'indxel'

export default defineSEO({
  siteName: 'MonSaaS',
  siteUrl: 'https://monsaas.fr',
  titleTemplate: '%s | MonSaaS',
  defaultOGImage: '/og-default.png',
  locale: 'fr_FR',
  twitter: {
    handle: '@monsaas',
    cardType: 'summary_large_image',
  },
  organization: {
    name: 'MonSaaS',
    logo: 'https://monsaas.fr/logo.png',
    url: 'https://monsaas.fr',
  },
  verification: {
    google: 'google-site-verification-code',
  },
})
```

### SEOConfig fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `siteName` | `string` | Yes | Display name (titles, structured data) |
| `siteUrl` | `string` | Yes | Canonical base URL (no trailing slash) |
| `defaultTitle` | `string` | No | Fallback page title |
| `titleTemplate` | `string` | No | Template with `%s` placeholder |
| `defaultOGImage` | `string` | No | Default OG image URL |
| `locale` | `string` | No | Locale (e.g. `fr_FR`, `en_US`) |
| `twitter` | `object` | No | `{ handle, cardType }` |
| `organization` | `object` | No | `{ name, logo, url }` |
| `verification` | `object` | No | `{ google?, yandex?, bing? }` |

---

## 3. createMetadata() — Per-Page Metadata

In each `page.tsx` or `layout.tsx`, export metadata using `createMetadata()`:

```ts
import { createMetadata } from 'indxel'
import seoConfig from '@/seo.config'

export function generateMetadata() {
  return createMetadata({
    title: 'Pricing',
    description: 'Simple, transparent pricing. Start free.',
    path: '/pricing',
  }, seoConfig)
}
```

### PageSEO fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | `string` | Yes | Page title |
| `description` | `string` | Yes | Meta description |
| `path` | `string` | Yes | URL path (e.g. `/blog/my-post`) |
| `ogImage` | `string` | No | Override default OG image |
| `noindex` | `boolean` | No | Add noindex directive |
| `canonical` | `string` | No | Override canonical URL |
| `alternates` | `Record<string, string>` | No | hreflang alternates |
| `article` | `object` | No | Article metadata (publishedTime, author, tags) |
| `structuredData` | `array` | No | JSON-LD entries for this page |

### Article pages

```ts
export function generateMetadata() {
  return createMetadata({
    title: 'How to Fix Broken Meta Tags',
    description: 'A guide to catching SEO regressions before they ship.',
    path: '/blog/fix-broken-meta-tags',
    ogImage: '/blog/fix-broken-meta-tags/og.png',
    article: {
      publishedTime: '2026-01-15',
      author: 'Jane Doe',
      section: 'Engineering',
      tags: ['SEO', 'Next.js', 'CI/CD'],
    },
  }, seoConfig)
}
```

### Multilingual pages

```ts
export function generateMetadata() {
  return createMetadata({
    title: 'Accueil',
    description: 'Infrastructure SEO pour developpeurs.',
    path: '/fr',
    alternates: {
      en: '/en',
      fr: '/fr',
      de: '/de',
    },
  }, seoConfig)
}
```

---

## 4. generateLD() — Structured Data (JSON-LD)

Generate type-safe JSON-LD for rich results:

```ts
import { generateLD } from 'indxel'

// In your component or page:
const faqLD = generateLD('FAQ', {
  questions: [
    { question: 'What is indxel?', answer: 'ESLint for SEO.' },
    { question: 'Is it free?', answer: 'The CLI and SDK are open-source.' },
  ],
})

// Render:
<script
  type="application/ld+json"
  dangerouslySetInnerHTML={{ __html: JSON.stringify(faqLD) }}
/>
```

### Supported types

| Type | Key fields | Use case |
|------|-----------|----------|
| `Article` | `headline`, `datePublished`, `author` | Blog posts |
| `Product` | `name`, `price`, `currency`, `brand` | Product pages |
| `FAQ` | `questions: [{ question, answer }]` | FAQ sections |
| `HowTo` | `name`, `steps: [{ name, text }]` | Tutorials |
| `Breadcrumb` | `items: [{ name, url }]` | Navigation breadcrumbs |
| `Organization` | `name`, `url`, `logo` | About pages |
| `WebPage` | `name`, `description`, `url` | Generic pages |
| `SoftwareApplication` | `name`, `category`, `price` | App/tool pages |
| `WebSite` | `name`, `url`, `searchUrl` | Site-level schema |

### Examples

**Product:**
```ts
generateLD('Product', {
  name: 'Indxel Pro',
  description: 'SEO monitoring dashboard.',
  price: '19',
  currency: 'EUR',
  brand: 'Indxel',
  url: 'https://indxel.com/pricing',
})
```

**Breadcrumb:**
```ts
generateLD('Breadcrumb', {
  items: [
    { name: 'Home', url: 'https://indxel.com' },
    { name: 'Blog', url: 'https://indxel.com/blog' },
    { name: 'Post Title', url: 'https://indxel.com/blog/post' },
  ],
})
```

**HowTo:**
```ts
generateLD('HowTo', {
  name: 'Set up indxel in 3 steps',
  steps: [
    { name: 'Install', text: 'Run npm install indxel' },
    { name: 'Init', text: 'Run npx indxel init' },
    { name: 'Check', text: 'Run npx indxel check' },
  ],
})
```

---

## 5. validateMetadata() — Programmatic Validation

Validate metadata in code (used internally by the CLI):

```ts
import { createMetadata, validateMetadata } from 'indxel'
import seoConfig from '@/seo.config'

const metadata = createMetadata({
  title: 'Home',
  description: 'Welcome.',
  path: '/',
}, seoConfig)

const result = validateMetadata(metadata)

console.log(result.score)   // 85
console.log(result.grade)   // "B"
console.log(result.errors)  // [{ id: 'og-image', message: '...' }]
```

### Options

```ts
validateMetadata(metadata, {
  strict: true,           // Treat warnings as errors
  disabledRules: ['alternates'], // Skip specific rules
})
```

---

## 6. CLI — npx indxel check

### Basic check
```bash
npx indxel check
```

Scans all `page.tsx` files, extracts static metadata, validates against 17 rules, outputs a score per page.

### CI/CD mode
```bash
npx indxel check --ci
```

Strict mode. Exit code 1 on any error. Use in GitHub Actions or Vercel build.

### Diff mode
```bash
npx indxel check --diff
```

Compare with previous run. Shows score changes per page.

### Minimum score
```bash
npx indxel check --min-score 80
```

Fail only if average score drops below threshold.

### Fix suggestions
```bash
npx indxel check --fix
```

Show code snippets to fix detected errors.

### JSON output
```bash
npx indxel check --json
```

Machine-readable output for integrations.

---

## 7. Validation Rules (17 rules, 100 points)

| Rule | Points | Severity | What it checks |
|------|--------|----------|----------------|
| `title-present` | 5 | critical | Page has a title |
| `title-length` | 10 | optional | Title is 30-60 characters |
| `description-present` | 5 | critical | Page has meta description |
| `description-length` | 10 | optional | Description is 120-160 chars |
| `og-image` | 10 | optional | Open Graph image is set |
| `og-title` | 5 | optional | OG title is set |
| `og-description` | 5 | optional | OG description is set |
| `canonical` | 10 | critical | Canonical URL is set |
| `structured-data-present` | 8 | optional | Has JSON-LD |
| `structured-data-valid` | 2 | optional | JSON-LD is valid |
| `structured-data-complete` | 5 | optional | JSON-LD has required fields |
| `robots` | 5 | optional | Robots directives present |
| `twitter-card` | 5 | optional | Twitter card is configured |
| `alternates` | 5 | optional | hreflang alternates set |
| `viewport` | 3 | optional | Viewport meta present |
| `favicon` | 2 | optional | Favicon exists |
| `image-alt` | 5 | optional | Images have alt text |

**Scoring:**
- Pass = full points
- Warning = half points
- Error = 0 points
- Grade: A (90+), B (80+), C (70+), D (60+), F (<60)

---

## 8. CI/CD Integration

### GitHub Actions

```yaml
# .github/workflows/seo.yml
name: SEO Check
on: [push, pull_request]
jobs:
  seo:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - run: npm ci
      - run: npx indxel check --ci
```

### Vercel Build

In `package.json`:
```json
{
  "scripts": {
    "build": "npx indxel check --ci && next build"
  }
}
```

### Git pre-push hook

```bash
npx indxel init --hook
```

Blocks `git push` if critical SEO errors are found.

---

## 9. Configuration File

Create `.indxelrc.json` at the project root for persistent CLI settings:

```json
{
  "minScore": 80,
  "disabledRules": ["alternates"],
  "ignoreRoutes": ["/dashboard/*", "/api/*"],
  "baseUrl": "https://monsaas.fr"
}
```

---

## Verification

After making changes, always verify:

1. **Run the check:** `npx indxel check`
2. **Confirm score is acceptable:** Look for grade A or B (80+)
3. **No critical errors:** Title, description, and canonical must pass
4. **Structured data present:** Pages should have relevant JSON-LD

If errors remain, read the error messages — they tell you exactly what's missing and what to add.

---

## Common Patterns

### Layout metadata (shared across routes)

```ts
// app/blog/layout.tsx
import { createMetadata } from 'indxel'
import seoConfig from '@/seo.config'

export function generateMetadata() {
  return createMetadata({
    title: 'Blog',
    description: 'Engineering insights and product updates.',
    path: '/blog',
  }, seoConfig)
}
```

### Dynamic pages (from CMS/database)

```ts
// app/blog/[slug]/page.tsx
import { createMetadata, generateLD } from 'indxel'
import seoConfig from '@/seo.config'

export async function generateMetadata({ params }) {
  const post = await getPost(params.slug)
  return createMetadata({
    title: post.title,
    description: post.excerpt,
    path: `/blog/${post.slug}`,
    ogImage: post.coverImage,
    article: {
      publishedTime: post.publishedAt,
      author: post.author.name,
      tags: post.tags,
    },
  }, seoConfig)
}
```

### noindex for authenticated pages

```ts
export function generateMetadata() {
  return createMetadata({
    title: 'Dashboard',
    description: 'Your SEO dashboard.',
    path: '/dashboard',
    noindex: true,
  }, seoConfig)
}
```

---

## Beyond Metadata — SEO Best Practices

The indxel CLI catches metadata issues. But good SEO goes further. When
reviewing or setting up a project, also check these (see `references/seo-knowledge-base.md` for full details):

1. **Semantic HTML** — Use `<article>`, `<section>`, `<nav>`, not div soup.
   AI crawlers rely on semantic tags to understand content relationships.

2. **Heading hierarchy** — One `<h1>` per page, no skipped levels (H2→H4).

3. **Structured data strategy** — Use the `@graph` pattern to connect entities.
   Every Organization needs `sameAs` linking to LinkedIn, Wikipedia, etc.

4. **GEO readiness** — Add `/llms.txt` for AI discoverability. Check that
   `robots.txt` doesn't block GPTBot, ClaudeBot, or Google-Extended.

5. **Rendering** — Public pages must use SSG/ISR/SSR. Pure CSR = invisible
   to crawlers. Check for `'use client'` on SEO-critical pages.

6. **Inverted pyramid** — The answer must come right after the heading.
   AI models weight the first 100-200 tokens of a section heavily.

7. **Performance** — LCP < 2.5s, INP < 200ms, CLS < 0.1.
   Check for heavy imports, unoptimized images, render-blocking scripts.
