---
name: ui-mockup-builder
description: >
  Build interactive UI mockups to communicate product ideas, test hypotheses, and replace PRDs
  as the primary thinking artifact. Use this skill whenever the user wants to visualize a product
  change, prototype an onboarding flow, mock up a dashboard, illustrate a feature concept, or
  communicate a product direction to stakeholders. Also trigger when the user says "show me what
  this would look like", "mock up", "prototype", "wireframe", "sketch this out", "visualize this
  feature", or "how would this flow work". Prefer mockups over written specs — a clickable prototype
  communicates more than 10 pages of PRD. This skill covers everything from quick lo-fi wireframes
  to polished interactive prototypes.
---

# UI Mockup Builder

## When to Use

- Communicating a product change to the team
- Testing whether a UI concept makes sense before engineering investment
- Exploring multiple approaches to the same problem (A vs B vs C)
- Illustrating data findings ("here's what the new dashboard page would look like")
- Onboarding flow redesigns
- Stakeholder presentations (show, don't tell)

## Before You Start

**Read these references:**
1. `shared-references/metric-definitions.md` — Use real baselines in dashboards and metric displays
2. `shared-references/design-principles.md` — Especially principle #3 (generalist amplification) and #10 (knowledge preservation)
3. The frontend design skill for aesthetic guidance: `/mnt/skills/public/frontend-design/SKILL.md`
4. `shared-references/dashboard-standard.md` — When mocking up analytics dashboards, match the canonical visual language: design tokens, layout architecture, chart theming, and component APIs

Mockups serve a different purpose than production frontends. Adjust:
- **Speed over polish** — A mockup that takes 10 minutes beats a pixel-perfect one that takes 2 hours
- **Clarity over creativity** — The goal is to communicate the idea, not win design awards
- **Interactivity over beauty** — Clickable states > static screenshots

## Philosophy: Why Mockups Replace PRDs

A PRD describes a product change. A mockup **is** the product change, rendered at low fidelity.

| PRD says... | Mockup shows... |
|------------|----------------|
| "Add a progress indicator to onboarding" | The actual progress bar, in context, with states |
| "The copilot should suggest next steps" | The suggestion UI, with real copy, positioned correctly |
| "Improve the builder empty state" | The new empty state with actual content and CTAs |

**For engineers:** A mockup eliminates ambiguity. They see what to build.
**For stakeholders:** A mockup is a conversation starter. They react to what they see.
**For you (the PM):** Building the mockup forces you to resolve design decisions you'd otherwise hand-wave in a PRD.

## Fidelity Decision Tree

```
What's the purpose?
│
├─ "Quick exploration / thinking tool"
│   → Lo-fi wireframe (grayscale, system fonts, boxes)
│   → Output: Single HTML file, <100 lines
│   → Time: 5 minutes
│
├─ "Team discussion / design review"
│   → Mid-fi mockup (real layout, placeholder content, basic styling)
│   → Output: HTML/React with Tailwind, interactive states
│   → Time: 15-30 minutes
│
├─ "Stakeholder presentation / eng handoff"
│   → Hi-fi prototype (real content, brand colors, animations)
│   → Output: React component with Landbot styling, multiple states
│   → Time: 30-60 minutes
│
└─ "Data-driven dashboard / analytics view"
    → Functional prototype (real data structure, charts, filters)
    → Output: React + Recharts/D3, with sample data
    → Time: 30-60 minutes
```

## Landbot Design Context

Landbot's product has specific UI patterns. Mockups should feel like they belong in the product.

### Brand Basics
- **Primary colors:** Landbot uses a blue-heavy palette with green accents
- **Typography:** Clean sans-serif (the product uses system fonts + custom heading fonts)
- **Layout:** Left sidebar navigation, main content area, right panel for properties/settings
- **Builder:** Visual flow-based builder with blocks connected by arrows. Think Figma + Zapier hybrid.
- **Chat widget:** Bottom-right floating widget that expands into a conversation panel

### Common UI Patterns to Mock Up

**1. Onboarding flows**
- Step indicator (numbered or progress bar)
- Single question per screen
- Large, clear CTAs
- Skip/back navigation

**2. Builder improvements**
- Block palette (left sidebar)
- Canvas (center, with draggable blocks)
- Properties panel (right sidebar)
- The "copilot" appears as a floating assistant element

**3. Dashboard/analytics views**
- Metric cards at top (KPIs)
- Charts below (line, bar, or area)
- Filter bar (date range, segment selectors)
- Table at bottom for drill-down

**4. Chat widget / conversation UI**
- Message bubbles (user = right-aligned, agent = left-aligned)
- Typing indicators
- Quick reply buttons
- Rich media (images, cards, carousels)

## Building Methodology

### Step 1: Clarify the Concept

Before touching code, answer:
1. **What screen/flow?** (onboarding step 3, builder empty state, analytics page)
2. **What's the ONE thing this mockup needs to communicate?** (the copilot suggests actions, the progress bar motivates completion, the new metric card shows AHA reach)
3. **Who's the audience?** (just me thinking, team design review, stakeholder presentation)
4. **What interactions matter?** (click to expand, hover for tooltip, toggle between views)

### Step 2: Choose Output Format

| Format | Best For | Tooling |
|--------|---------|---------|
| **Single HTML file** | Quick wireframes, simple layouts | Raw HTML + inline CSS |
| **React (.jsx)** | Interactive prototypes with state | React + Tailwind + shadcn/ui |
| **HTML + embedded charts** | Dashboard mockups with data | HTML + Chart.js or inline SVG |
| **SVG** | Flow diagrams, architecture sketches | SVG markup |

**Default choice:** React (.jsx) — most versatile, supports interactivity, renders in Claude.ai artifacts.

### Step 3: Build Iteratively

**Round 1: Structure** — Get the layout right. Gray boxes, placeholder text. No styling.
**Round 2: Content** — Replace placeholders with real copy, real metric values, real labels.
**Round 3: Polish** — Add colors, spacing, hover states, transitions (only if fidelity warrants it).

### Step 4: Add Data Context

This is where the mockup skill connects to the analytical skills. When building mockups for:

- **Onboarding changes:** Pull real AHA reach numbers, activation rates, builder event frequencies from funnel analysis
- **Dashboard designs:** Use actual metric values and ranges from `metric-definitions.md`
- **Experiment presentations:** Show the A/B test results IN the mockup (before/after comparison)

**Example:** Don't mock up a dashboard with "XX%" — pull the real activation rate from `shared-references/metric-definitions.md`. Real numbers make the mockup credible and the discussion concrete.

## Templates and Patterns

### Template: Metric Card (for dashboards)

```jsx
const MetricCard = ({ label, value, trend, trendLabel }) => (
  <div className="bg-white rounded-lg border border-gray-200 p-5 shadow-sm">
    <div className="text-sm text-gray-500 font-medium">{label}</div>
    <div className="text-3xl font-bold text-gray-900 mt-1">{value}</div>
    <div className={`text-sm mt-2 ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
      {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% {trendLabel}
    </div>
  </div>
);

// Usage with real Landbot data — get current values from shared-references/metric-definitions.md:
<MetricCard label="7-Day Activation Rate" value="[from metric-definitions.md]" trend={2.3} trendLabel="vs last week" />
<MetricCard label="Builder AHA Reach" value="[from metric-definitions.md]" trend={-0.4} trendLabel="vs last week" />
<MetricCard label="Signup→Paid (30d)" value="[from metric-definitions.md]" trend={5.1} trendLabel="vs last month" />
```

### Template: Onboarding Step

```jsx
const OnboardingStep = ({ step, totalSteps, question, options, onSelect }) => (
  <div className="max-w-lg mx-auto p-8">
    {/* Progress */}
    <div className="flex gap-1 mb-8">
      {Array.from({length: totalSteps}, (_, i) => (
        <div key={i} className={`h-1 flex-1 rounded-full ${
          i < step ? 'bg-blue-500' : i === step ? 'bg-blue-300' : 'bg-gray-200'
        }`} />
      ))}
    </div>
    
    {/* Question */}
    <h2 className="text-2xl font-bold text-gray-900 mb-6">{question}</h2>
    
    {/* Options */}
    <div className="space-y-3">
      {options.map((opt, i) => (
        <button key={i} onClick={() => onSelect(opt)}
          className="w-full text-left p-4 rounded-lg border border-gray-200 
                     hover:border-blue-400 hover:bg-blue-50 transition-all">
          <div className="font-medium text-gray-900">{opt.label}</div>
          {opt.description && (
            <div className="text-sm text-gray-500 mt-1">{opt.description}</div>
          )}
        </button>
      ))}
    </div>
  </div>
);
```

### Template: A/B Test Results Presentation

```jsx
const ExperimentResult = ({ name, control, treatment, pValue, significant }) => (
  <div className="bg-white rounded-xl border p-6 max-w-2xl">
    <h3 className="text-lg font-bold mb-4">{name}</h3>
    
    {/* Visual comparison */}
    <div className="flex gap-8 mb-6">
      <div className="flex-1 text-center p-4 bg-gray-50 rounded-lg">
        <div className="text-sm text-gray-500 mb-1">Control</div>
        <div className="text-3xl font-bold">{control}%</div>
      </div>
      <div className={`flex-1 text-center p-4 rounded-lg ${
        significant ? 'bg-green-50 ring-2 ring-green-200' : 'bg-gray-50'
      }`}>
        <div className="text-sm text-gray-500 mb-1">Treatment</div>
        <div className="text-3xl font-bold">{treatment}%</div>
      </div>
    </div>
    
    {/* Stats */}
    <div className="flex justify-between text-sm text-gray-600">
      <span>Relative lift: {((treatment - control) / control * 100).toFixed(1)}%</span>
      <span>p-value: {pValue}</span>
      <span className={significant ? 'text-green-600 font-medium' : 'text-gray-400'}>
        {significant ? '✓ Significant' : '○ Not significant'}
      </span>
    </div>
  </div>
);
```

### Template: Chat Widget Mockup

```jsx
const ChatMessage = ({ sender, text, time, quickReplies }) => (
  <div className={`flex ${sender === 'user' ? 'justify-end' : 'justify-start'} mb-3`}>
    <div className={`max-w-xs px-4 py-2 rounded-2xl ${
      sender === 'user' 
        ? 'bg-blue-500 text-white rounded-br-md' 
        : 'bg-gray-100 text-gray-900 rounded-bl-md'
    }`}>
      <div className="text-sm">{text}</div>
      <div className={`text-xs mt-1 ${
        sender === 'user' ? 'text-blue-200' : 'text-gray-400'
      }`}>{time}</div>
    </div>
  </div>
);
```

## Multi-Variant Mockups

When exploring alternatives, build 2-3 variants in the same file with a toggle:

```jsx
const [variant, setVariant] = useState('A');

// Variant selector at top
<div className="flex gap-2 mb-6 p-2 bg-gray-100 rounded-lg w-fit">
  {['A', 'B', 'C'].map(v => (
    <button key={v} onClick={() => setVariant(v)}
      className={`px-4 py-1.5 rounded-md text-sm font-medium transition ${
        variant === v ? 'bg-white shadow text-gray-900' : 'text-gray-500'
      }`}>
      Variant {v}
    </button>
  ))}
</div>

// Then conditionally render based on variant
{variant === 'A' && <VariantA />}
{variant === 'B' && <VariantB />}
{variant === 'C' && <VariantC />}
```

This is far more effective for team discussions than separate files — people can switch back and forth in the same view.

## Lessons Check

### Before Execution

Before starting any task with this skill:

1. Read `LESSONS.md` in this skill's directory — check local rules for known pitfalls
2. Check `shared-references/lessons.md` for cross-skill rules tagged `mockup`
3. If a rule's **trigger condition** matches what you're about to do — follow the rule

### After Any Correction

When the user corrects an error or points out a mistake:

1. **Log the incident** in this skill's `LESSONS.md` using the incident template (I-XXX)
2. **Extract the rule**: What's the generalizable pattern? Write it as an imperative ("Always X when Y")
3. **Decide scope**:
   - Is this specific to this skill's methodology? → Add as a **local rule** (L-XXX) in this skill's `LESSONS.md`
   - Does it apply to 2+ skills, or is the root cause environmental? → **Promote** to `shared-references/lessons.md` (R-XXX) and leave a reference in the local file
4. **Confirm with the user**: "I've logged this as [L-XXX/R-XXX]: [rule summary]. Does that capture it correctly?"

### Promotion Criteria

Promote a local lesson to `shared-references/lessons.md` when ANY of:
- It would prevent mistakes in other skills (cross-domain relevance)
- The root cause is environmental (BigQuery, Landbot data, LLM behavior, tooling)
- The same lesson was independently discovered by another skill

## Cross-Skill Connections

- **When you need real numbers for the mockup →** Pull from funnel analysis findings (→ `landbot-funnel-analyzer` skill)
- **When the mockup represents a testable change →** Design the experiment to validate it (→ `ab-test-designer` skill)
- **When mocking up conversation UI →** Ground it in quality dimensions from eval framework (→ `conversational-agent-evaluator` skill)
- **When the mockup needs to actually work →** Graduate to a functional MVP (→ `mvp-builder` skill)
- **When mocking up an OKR dashboard or progress visualization →** Use OKR tracking methodology for correct status detection (→ `okr-expert` skill)
- **When research findings suggest a product change →** Mock it up for stakeholder feedback (→ `user-research-synthesizer` skill)
- **When mocking up a competitive response feature →** Ground in competitive analysis first (→ `competitive-intelligence` skill)
- **When mocking up a retention intervention →** Validate the churn pattern first (→ `churn-analyzer` skill)
- **When the mockup needs to look on-brand for stakeholders →** Apply Landbot brand guidelines (→ `landbot-brand-styling` plugin skill)

## Common Mistakes

1. **Over-polishing too early** — A gray-box wireframe shown in 10 minutes is worth more than a polished mockup shown next week
2. **Forgetting states** — Always mock: empty state, loading state, populated state, error state
3. **Using fake numbers** — Use real baselines from metric-definitions.md. Fake numbers invite fake discussions
4. **Building one variant when the decision needs three** — If you're deciding between approaches, mock all of them
5. **Treating the mockup as the spec** — The mockup starts the conversation; the team refines it together
