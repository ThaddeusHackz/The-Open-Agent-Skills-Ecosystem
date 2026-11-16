---
name: prototype-to-code
description: >
  Use this skill when a user wants to turn a visual wireframe, mockup, or Claude Design
  prototype into working production code. Triggers include: "implement this wireframe",
  "build this mockup", "turn this prototype into code", "code up this design", "implement
  this UI from the screenshot/image", "PM handed me a wireframe to build", "translate this
  Claude Design prototype to React/Next.js/Vue/HTML", or any task where the user provides
  a visual design artifact (image, URL, description of screens) and wants functional code.
  Also trigger when a user says "hand this off to engineering" and a prototype is present.
  This skill covers the full prototype-to-production pipeline. Always use it before writing
  UI code from a design artifact.
---

# Prototype to Code Skill

This skill covers translating any visual design artifact — Claude Design prototype, wireframe
image, mockup screenshot, or Figma export — into clean, production-ready code.

## Inputs This Skill Handles

| Input type | How to process |
|---|---|
| Claude Design handoff bundle | → Use `claude-design-handoff` skill (that skill is specialized for bundles) |
| Claude Design prototype URL | Fetch the URL; read the interactive prototype; extract component structure |
| Wireframe image (PNG/JPG) | Analyze the image visually; extract layout, hierarchy, and components |
| Figma export (JSON/SVG) | Parse the Figma structure; extract frames as screens |
| Sketch or Adobe XD screenshot | Treat as wireframe image |
| Written description of screens | Ask for clarification on layout before proceeding |

---

## Phase 1: Design Analysis

Before writing a single line of code, fully analyze the design artifact.

### 1.1 Identify Screens and States
List all the screens or views present:
- Main view (what the user sees first)
- Secondary views (detail pages, modals, sidebars)
- State variants (empty, loading, error, success)
- Responsive variants (mobile/tablet/desktop if shown)

### 1.2 Extract the Layout Structure
Identify the layout pattern:
- **Full-page layout**: fixed nav + scrollable content + optional footer
- **Dashboard**: sidebar + main content area + optional right panel
- **Card grid**: responsive masonry or fixed-column grid
- **Split view**: two equal panels (e.g. list + detail)
- **Wizard/stepper**: sequential form with progress indicator
- **Landing page**: stacked sections with varied backgrounds

Map each section to a semantic HTML element: `<header>`, `<nav>`, `<main>`, `<section>`, `<aside>`, `<footer>`.

### 1.3 Identify All Components
For each distinct UI element, name it and classify it:

```
Page-level:   Navbar, Sidebar, PageHeader, Footer
Content:      HeroSection, FeatureCard, PricingTier, TestimonialRow
Forms:        SearchBar, FilterPanel, LoginForm, SignupForm
Data display: DataTable, StatCard, ChartContainer, Timeline
Feedback:     Toast, AlertBanner, EmptyState, LoadingSpinner, SkeletonCard
Navigation:   TabGroup, Breadcrumb, Pagination, StepIndicator
```

### 1.4 Establish Component Hierarchy
Build a tree before coding:

```
<Page>
  <Navbar logo actions=[SearchBar, UserMenu] />
  <main>
    <Sidebar links=[...] />
    <Content>
      <PageHeader title actions=[CreateButton] />
      <DataTable rows columns filters />
      <Pagination />
    </Content>
  </main>
</Page>
```

---

## Phase 2: Technology Decisions

If not already specified, confirm or infer the stack:

| Signal | Inferred stack |
|---|---|
| Claude Design handoff with Next.js repo | Next.js App Router + Tailwind + shadcn/ui |
| Tailwind classes visible in design | Tailwind CSS |
| MUI-style components | Material UI / Joy UI |
| Bootstrap grid visible | Bootstrap 5 |
| No framework specified | Ask: React, Vue, or plain HTML? |

**Default recommendation** (if user has no preference):
- React + Tailwind CSS + shadcn/ui components
- File structure: one file per component in `src/components/`

---

## Phase 3: Implementation Order

Always build in this order to avoid rework:

### Step 1: Tokens and Global Styles
```css
/* globals.css */
:root {
  --color-primary: /* from design */;
  --font-body: /* from design */;
  --spacing-base: 4px;
}
```

### Step 2: Layout Shell
Build the page wrapper with the correct grid/flex structure.
Do NOT fill in content yet — just establish the skeleton.

```jsx
// layout.tsx
export default function Layout({ children }) {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="flex flex-1">
        <Sidebar />
        <main className="flex-1 p-6">{children}</main>
      </div>
      <Footer />
    </div>
  )
}
```

### Step 3: Primitive / Leaf Components
Build the smallest, most reusable pieces first:
- Buttons (all variants)
- Badge, Tag, Chip
- Input, Select, Checkbox
- Avatar, Icon wrapper

### Step 4: Composite Components
Assemble primitives into larger components:
- Card (using Button, Badge, Avatar)
- DataTable row (using Checkbox, Badge, ActionMenu)
- FilterPanel (using Input, Select, Button)

### Step 5: Page Sections
Compose components into full page sections:
- HeroSection, FeatureGrid, PricingSection, etc.

### Step 6: Full Pages
Wire together layout + sections into complete pages.

### Step 7: Edge States
For every data-driven component, implement:
```jsx
// Always handle these four states
if (isLoading) return <SkeletonCard />
if (error) return <ErrorBanner message={error.message} />
if (!data || data.length === 0) return <EmptyState cta="Create your first item" />
return <DataList items={data} />
```

### Step 8: Responsive Behavior
Apply breakpoint classes for mobile/tablet. Default approach:
- Mobile first: base styles = mobile
- `md:` prefix = tablet (768px)
- `lg:` prefix = desktop (1024px)

---

## Phase 4: Quality Checklist

Before declaring implementation complete:

- [ ] All colors reference token variables (no hardcoded hex)
- [ ] All font sizes use the design scale
- [ ] Spacing uses consistent multiples of base unit
- [ ] All four data states implemented (loading/error/empty/populated)
- [ ] Interactive elements have hover + focus styles
- [ ] Keyboard navigation works (tab order, focus rings)
- [ ] Color contrast meets WCAG AA (4.5:1 for text)
- [ ] Layout doesn't break at 375px (iPhone SE) or 1920px (wide desktop)
- [ ] No `console.log` statements left in code
- [ ] Component file names match the design spec names

---

## Communicating With the User During Implementation

At the start: confirm the stack and the scope (all screens or just one?).

During implementation: if the design is ambiguous on something important (e.g. what happens when the user clicks X, or what data drives a table), ask **one focused question** rather than blocking on every uncertainty.

At the end, provide:
1. **File list** — every file created or modified
2. **Usage example** — how to render the top-level component
3. **Open questions** — anything not addressed (e.g. "API endpoints not yet connected")
4. **Suggested next steps** — e.g. "add authentication", "connect to API", "add animation"

---

## Framework-Specific Notes

### React + Tailwind
- Use `cn()` utility (clsx + tailwind-merge) for conditional classes
- Prefer named exports for components, default export for pages
- Use `data-*` attributes for state variants instead of inline styles

### Next.js App Router
- Server components by default; add `'use client'` only when needed (interactivity, hooks)
- Place page components in `app/[route]/page.tsx`
- Use `loading.tsx` and `error.tsx` for automatic edge state handling

### Vue 3
- Use Composition API (`<script setup>`)
- Scoped styles per component
- Use `defineProps` with TypeScript types

### Plain HTML/CSS
- Use CSS custom properties for all tokens
- Flexbox/Grid for layout; avoid floats
- One `<section>` per major page region with a unique `id`
