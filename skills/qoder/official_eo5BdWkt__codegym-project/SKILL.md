---
name: codegym-project
description: Live project tracking document for CodeGym. Architecture decisions, implementation progress, technical retrospective. This is the "how" document — updated as we build. Consult this skill when implementing features, making tech decisions, or reviewing what's been built.
---

# CodeGym — Project Tracker

> **Status**: Scaffold complete — building features
> **Last updated**: 2026-03-21 (post-scaffold)

## Architecture

### Tech Stack

| Layer | Choice | Rationale |
|-------|--------|-----------|
| Runtime | Bun 1.3.10 | Faster installs, faster cold starts, native Vercel support via `buildCommand` in vercel.json |
| Framework | Next.js 16.2.1 (App Router) | Vercel-native, RSC for fast loads, API routes for backend |
| AI | Gemini 2.5 Flash/Pro via Vercel AI SDK v6.0.134 | Hackathon requirement, structured output with Zod |
| AI Provider | @ai-sdk/google v3.0.52 | Official Gemini adapter for AI SDK |
| Schema | Zod v4.3.6 | Structured AI output validation (NOT Zod v3) |
| Database | Supabase (PostgreSQL) | Free credits, real-time subscriptions, stores problems/submissions/profiles |
| Auth | BetterAuth | Hackathon sponsor, free, all auth flows, Agent Auth protocol for problem generator |
| Code Editor | Monaco Editor (@monaco-editor/react) | VS Code engine, syntax highlighting, IntelliSense |
| Execution | In-browser (JS/TS) + Vercel Sandbox v1.9.0 (stretch) | No Docker available on Vercel serverless |
| Styling | Tailwind CSS v4 | Fast to build, dark mode by default |
| Voice | ElevenLabs v1.59.0 (convertAsStream) | Problem narration, accessibility |
| Monitoring | Sentry @sentry/nextjs v10.45.0 | Error tracking, AI agent monitoring |
| Deployment | Vercel | Hackathon requirement |

### Sponsor Integration Map

| Sponsor | Integration | Priority |
|---------|------------|----------|
| Google/DeepMind | Gemini 2.5 Flash/Pro — core AI engine for all generation | Required |
| Vercel | AI SDK + Sandbox + Deployment | Required |
| Supabase | PostgreSQL data layer + realtime | High |
| BetterAuth | User auth + Agent Auth protocol | High |
| ElevenLabs | Voice narration of problems | Medium |
| Sentry | Error monitoring in production | Medium |
| Augment Code | Dev tool during hackathon | Low |

### System Diagram

```
┌─────────────────────────────────────────────────┐
│              Next.js App (Vercel)                │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │ Problem   │  │ MCQ      │  │ Skill        │  │
│  │ Generator │  │ Marathon  │  │ Dashboard    │  │
│  │ Page      │  │ Page     │  │ Page         │  │
│  └─────┬────┘  └─────┬────┘  └──────┬───────┘  │
│        │              │              │           │
│  ┌─────▼──────────────▼──────────────▼───────┐  │
│  │           API Routes (Route Handlers)      │  │
│  │  /api/generate  /api/mcq  /api/profile     │  │
│  └─────┬──────────────┬──────────────┬───────┘  │
│        │              │              │           │
│  ┌─────▼────┐  ┌──────▼─────┐  ┌────▼───────┐  │
│  │ Gemini   │  │ Supabase   │  │ Execution  │  │
│  │ AI SDK   │  │ Client     │  │ Engine     │  │
│  └──────────┘  └────────────┘  └────────────┘  │
└─────────────────────────────────────────────────┘
```

### Key API Routes (Implemented)

| Route | Method | Purpose | Status |
|-------|--------|---------|--------|
| `/api/generate-problem` | POST | Generate coding problem via Gemini `generateObject` + `ProblemSchema` | ✅ Built |
| `/api/generate-mcq` | POST | Generate adaptive MCQ batch via `MCQBatchSchema`. Accepts `customPrompt` + `onboardingNotes` for personalized generation | ✅ Built |
| `/api/generate-onboarding` | POST | Generate 3-8 skill-assessment questions based on user's prompt. Uses `OnboardingBatchSchema` | ✅ Built |
| `/api/save-onboarding` | POST | Save onboarding Q&A answers as notes in `user_memories.notes` | ✅ Built |
| `/api/mcq-results` | POST | Record MCQ session results and update memory via `updateMemory()` | ✅ Built |
| `/api/history` | GET | Fetch merged practice history: generated problems + marathon sessions | ✅ Built |
| `/api/review-code` | POST | AI code review via `CodeReviewSchema` | ✅ Built |
| `/api/tts` | POST | ElevenLabs TTS streaming (uses `convertAsStream`) | ✅ Built |
| `/api/auth/[...all]` | GET/POST | BetterAuth catch-all (lazy-init, force-dynamic) | ✅ Built |
| `/api/execute` | POST | Run user code in Vercel Sandbox | ❌ Not started |
| `/api/profile` | GET | Fetch user's skill profile from Supabase | ❌ Not started |

### Data Model (Supabase)

```sql
-- Core tables
users (id, email, name, created_at)
problems (id, title, statement_md, language, difficulty, tags,
          skeleton, test_harness, solution_code, prompt_used,
          created_at, user_id)
submissions (id, user_id, problem_id, code, passed, total,
             stdout, stderr, created_at)
mcq_sessions (id, user_id, topic, difficulty_level, score,
              questions_json, answers_json, created_at)
skill_profiles (user_id, summary_text, strengths, weaknesses,
                domain_scores_json, updated_at)
```

### Gemini Prompt Structures

**Problem Generation prompt key fields:**
- User's natural language request
- Target language
- Desired difficulty
- Output: structured JSON with title, statement, testCases, skeleton, solution

**Onboarding Generation prompt key fields (`/api/generate-onboarding`):**
- User's free-text prompt (what they want to practice)
- Existing memory profile + notes (if returning user)
- Output: 3-8 `OnboardingQuestion` objects with question, options[], key

**MCQ Generation prompt key fields (`/api/generate-mcq`):**
- `customPrompt` — user's free-text topic request
- `onboardingNotes` — self-assessment Q&A from onboarding phase
- Memory context: skill summary, notes, weak/strong skills
- Output: array of 5-10 MCQ objects calibrated to assessed level

**Skill Profile Update prompt key fields:**
- Current skill profile (summary + notes)
- New submission/MCQ results
- Output: updated natural language summary + domain scores

---

## Implementation Log

> Entries added as features are built. Each entry: what was built, decisions made, problems hit.

### Phase 0: Project Setup
- **Status**: ✅ Complete
- Next.js 16 scaffolded with Bun, all deps installed, build passes
- Sentry client/server/edge configs + instrumentation.ts
- BetterAuth lazy-init server + catch-all route
- Supabase server/client libraries configured
- ElevenLabs TTS route with `convertAsStream` (not `.stream()`)
- Monaco code editor with dynamic import (SSR-safe)
- Dark mode, Geist fonts, vercel.json, .env.example

### Phase 1: Problem Generator
- **Status**: ✅ API built, UI built
- `generateObject()` + `ProblemSchema` Zod schema (11 fields)
- Practice page: split panel — problem description left, Monaco editor right
- Domain/difficulty selectors, progressive hints, TTS narration button
- Code review submission flow with `CodeReviewSchema`

### Phase 2: Code Workspace
- **Status**: 🔄 Partial
- Monaco editor integrated with dynamic import
- Test case display in problem panel
- Missing: Vercel Sandbox execution, test runner

### Phase 3: MCQ Marathon
- **Status**: ✅ UI built, API built, onboarding flow complete
- **New flow**: idle (prompt input) → onboarding (3-8 skill-assessment questions) → active (MCQ quiz) → results
- **"I'm Feeling Lucky"** button skips onboarding, goes straight to MCQ generation (uses existing memory only)
- User enters free-text prompt instead of selecting from topic dropdown
- Onboarding questions generated by Gemini via `OnboardingBatchSchema` — assess skill level for the specific topic
- Onboarding answers saved as `notes` in `user_memories` table via `saveOnboardingNotes()`
- Notes + prompt + memory context all passed to `/api/generate-mcq` for personalized question difficulty
- `MCQBatchSchema` for batch generation, adaptive skill tracking (weak/strong skills)
- Full quiz UI: answer selection, confirm, explanation reveal, scoring, help flashcard
- Memory has two fields: `skill_summary` (AI-generated narrative) and `notes` (onboarding Q&A history)

### Phase 4: Skill Profile / Dashboard
- **Status**: ✅ Complete
- Live dashboard fetches `/api/memory?userId=demo-user` on mount
- Domain proficiency bars, strength/weakness tag pills, stat cards
- AI-generated skill summary with "time ago" timestamp
- Empty state with CTAs to /marathon, /generate, /chat
- Full memory system: `user_memories` + `interaction_log` tables in Supabase
- `src/lib/memory/service.ts` — `getOrCreateMemory`, `updateMemory`, `logInteraction`

### Phase 5: Polish & Demo Prep
- **Status**: 🔄 In Progress

#### Completed
- ✅ Generate → saves to Supabase (generated_problems table) + /problems list page
- ✅ Marathon → calls /api/mcq-results when completed (memory persists)
- ✅ Code review → passes userId so memory updates
- ✅ Chat multi-turn fixed for AI SDK v6 + memory tool calls
- ✅ Code editor now has a LeetCode-style Test Cases / Output panel
- ✅ Generate problem routes now use the user's typed prompt for topic targeting
- ✅ Generate page now has a marathon-style onboarding questionnaire, with an I'm Feeling Lucky fast path
- ✅ /problems now shows marathon history with continue links back to /marathon
- ✅ Sidebar renamed from Dashboard → Memory
- ✅ Coding-problem solve summaries now write to memory with valid interaction types and real problem tags

#### TODO (Priority Order)
1. **[MEDIUM] Real code execution polish**
  - `/api/execute` still needs production-hardening around Vercel Sandbox
  - Improve per-test actual output visibility for debugging

#### Database Status
- ✅ `user_memories` table — exists
- ✅ `interaction_log` table — exists  
- ✅ `generated_problems` table — SQL written in schema.sql, needs to be run in Supabase
- ❌ `mcq_sessions` table — not created yet (interaction_log stores MCQ data instead)

---

## Technical Decisions Log

> Record every significant decision with context so future-us understands why.

| # | Decision | Alternatives Considered | Rationale | Date |
|---|----------|------------------------|-----------|------|
| 1 | Bun runtime | Node.js, Deno | Faster installs + cold starts, native Vercel support, better streaming perf | 2026-03-21 |
| 2 | BetterAuth over Supabase Auth | Supabase Auth | More sponsor integration points, Agent Auth protocol is a differentiator | 2026-03-21 |
| 3 | TypeScript throughout | JavaScript | Type safety, better DX, Gemini structured output typing | 2026-03-21 |
| 4 | Lazy-init for all SDK clients | Module-scope init | ElevenLabs and BetterAuth both crash at build time if env vars missing. Next.js evaluates module scope during `bun run build` "Collecting page data" phase. Must use getter functions. | 2026-03-21 |
| 5 | `convertAsStream` not `stream` | `.stream()` | ElevenLabs SDK v1.59.0 does NOT have `.stream()` on TextToSpeech. Actual methods: `convert()`, `convertAsStream()`, `convertWithTimestamps()`, `streamWithTimestamps()`. Confirmed via node_modules type defs. | 2026-03-21 |
| 6 | `any` type for BetterAuth cache | Explicit `ReturnType<typeof betterAuth>` | Generic type variance issue — concrete config has narrower types than `BetterAuthOptions`. `any` is the pragmatic fix for lazy init pattern. | 2026-03-21 |
| 7 | Dark mode only (no light) | Light/dark toggle | Hackathon — faster to build one theme well. Removed `prefers-color-scheme` media query. | 2026-03-21 |
| 8 | `force-dynamic` on SDK routes | Static optimization | Routes using ElevenLabs, BetterAuth need runtime env vars. Without `force-dynamic`, Next.js tries to pre-render them. | 2026-03-21 |
| 9 | MCQ onboarding flow with notes | Direct topic dropdown | Free-text prompt + AI-generated skill-assessment questions personalize MCQ difficulty far better than a static dropdown. Notes persist in `user_memories.notes` alongside the AI-generated `skill_summary`, giving the memory system both structured (summary) and raw (notes) data. "I'm Feeling Lucky" preserves the quick-start path for returning users. | 2026-03-21 |

---

## Memory System (Phase 4.5 — AI Skill Tracking)

### What It Does
Every user interaction (code review, MCQ session, problem generation, chat) is recorded and fed to Gemini, which updates a live "skill document" per user. This is like Claude's memory feature — a continuously-updated profile of what the user knows.

### Architecture
```
User Action → API route → updateMemory() → Gemini (MemoryUpdateSchema) → Supabase upsert
                                         ↑
                                    getRecentInteractions()
```

### Key Files
- `src/lib/memory/service.ts` — 5 exported functions (`getOrCreateMemory`, `updateMemory`, `logInteraction`, `getRecentInteractions`, `saveOnboardingNotes`)
- `src/app/api/memory/route.ts` — GET (read) / POST (record interaction)
- `src/app/api/mcq-results/route.ts` — records MCQ session outcomes
- `src/app/api/generate-onboarding/route.ts` — generates skill-assessment questions from prompt
- `src/app/api/save-onboarding/route.ts` — saves onboarding Q&A as notes in memory
- `src/app/dashboard/page.tsx` — live dashboard showing real skill data

### Core Functions

```typescript
// Read or initialize memory for a user
const memory = await getOrCreateMemory(userId);

// Update memory after any interaction
await updateMemory(userId, {
  type: 'code_review' | 'mcq_session' | 'problem_attempt' | 'chat_message',
  domain: 'api-design',        // optional
  difficulty: 'intermediate',   // optional
  score: 80,                    // optional (0-100)
  metadata: {},                 // any extra context
  skillsInvolved: ['express-middleware', 'error-handling'],
});
```

### Supabase Schema
```sql
-- One row per user — continuously updated
CREATE TABLE user_memories (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL UNIQUE,
  skill_summary TEXT NOT NULL DEFAULT '',  -- AI-generated narrative (the "summary")
  notes TEXT NOT NULL DEFAULT '',          -- Onboarding Q&A history (the "notes")
  domain_scores JSONB NOT NULL DEFAULT '{}',
  strong_skills TEXT[] NOT NULL DEFAULT '{}',
  weak_skills TEXT[] NOT NULL DEFAULT '{}',
  problems_attempted INT NOT NULL DEFAULT 0,
  mcqs_answered INT NOT NULL DEFAULT 0,
  avg_score NUMERIC(5,2) NOT NULL DEFAULT 0,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
  updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- One row per interaction — used as context for Gemini memory updates
CREATE TABLE interaction_log (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  user_id TEXT NOT NULL,
  type TEXT NOT NULL,
  domain TEXT,
  difficulty TEXT,
  score INT,
  metadata JSONB NOT NULL DEFAULT '{}',
  skills_involved TEXT[] NOT NULL DEFAULT '{}',
  summary TEXT,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### MemoryUpdateSchema (Zod v4)
```typescript
export const MemoryUpdateSchema = z.object({
  skillSummary: z.string(),
  domainScores: z.object({
    'api-design': z.number().min(0).max(100),
    'state-management': z.number().min(0).max(100),
    // ... 10 domains total
  }),
  strongSkills: z.array(z.string()),
  weakSkills: z.array(z.string()),
  interactionSummary: z.string(),
});
```

### 10 Tracked Domains
`api-design`, `state-management`, `data-transformation`, `auth-security`, `database-queries`, `testing`, `performance`, `devops`, `frontend-ui`, `system-design`

### Demo Mode
All routes accept optional `userId` param:
- Default to `userId = 'demo-user'` when not provided
- Supabase stores all data under `user_id = 'demo-user'`
- No auth required for hackathon demo

### Non-Blocking Memory Updates
All API routes update memory without blocking the main response:
```typescript
// Fire and forget — don't await, don't fail the request
updateMemory(userId, interactionData).catch(err =>
  console.error('[memory-update] failed:', err)
);
```

### Dashboard Integration
The dashboard (`/dashboard`) fetches `GET /api/memory?userId=demo-user` on mount and displays:
- Domain proficiency bars (color-coded: ≥70 green, ≥40 amber, else red)
- Strong/weak skill tags (pill UI)
- AI-generated skill summary with "X ago" timestamp
- Stat cards: problems attempted, MCQs answered, avg score

### AI SDK React v3 — Using `DefaultChatTransport` for Extra Body Fields
The AI SDK `useChat` hook in v3 doesn't accept `body` directly on the root options object. Use `DefaultChatTransport` instead:
```typescript
import { DefaultChatTransport } from 'ai';
import { useChat } from '@ai-sdk/react';

const { messages, sendMessage, status } = useChat({
  transport: new DefaultChatTransport({
    api: '/api/chat',
    body: { userId: 'demo-user' },  // extra fields sent with every request
  }),
});
```
In the API route, these extra fields are accessible via `req.json()` alongside `messages`.

### Chat Memory Integration
Chat route loads memory before generating a response, and updates it after:
```typescript
const memory = await getOrCreateMemory('demo-user');

const result = streamText({
  model: geminiFlash,
  system: `You are a coding tutor. The user's skill profile: ${memory.skill_summary}
           Strong skills: ${memory.strong_skills.join(', ')}
           Weak skills: ${memory.weak_skills.join(', ')}`,
  messages,
  onFinish: async ({ text }) => {
    await updateMemory('demo-user', {
      type: 'chat_message',
      metadata: { excerpt: text.slice(0, 200) },
      skillsInvolved: [],
    });
  },
});
```

---

## Retrospective

> Updated continuously. What went right, what went wrong, lessons learned.

### What Went Right
- Pre-researching all sponsor SDKs before coding saved massive time
- Creating reference skills means future Claude instances don't repeat mistakes
- `generateObject()` with Zod schemas is clean — define shape once, get typed output
- Monaco dynamic import was straightforward with `next/dynamic`
- Memory system E2E test passed first try — Supabase reads/writes and Gemini updates all worked
- Non-blocking memory updates pattern prevents memory failures from degrading main UX
- Dashboard reads real Supabase data and renders domain bars/skill tags cleanly
- `DefaultChatTransport` in AI SDK v3 is the correct way to pass extra request fields

### What Went Wrong
- ElevenLabs SDK docs/research said `.stream()` — actual SDK has `.convertAsStream()`. Lost time on build error.
- BetterAuth lazy init was non-obvious — `betterAuth()` accesses env vars at call time, which crashed build
- BetterAuth type variance issue — `ReturnType<typeof betterAuth>` doesn't work as a cache variable type
- `create-next-app` rejected directory name with capital letters (npm naming restriction)
- `body` on `useChat({body: ...})` doesn't work in AI SDK v3 — must use `DefaultChatTransport`
- VS Code `get_errors` tool can show stale TypeScript errors after file changes — always verify with `bun run build`
- Vercel deploy env var with `!` character fails in bash — use `set +H` first to disable history expansion

### Key Learnings
- **Always check `node_modules/.../Client.d.ts`** when SDK methods don't match docs
- **Next.js builds evaluate module-scope code** — any SDK that requires env vars MUST be lazy-initialized
- **`export const dynamic = "force-dynamic"`** is the escape hatch for routes that need runtime env vars
- **Bun v1.3.10 works perfectly** with Next.js 16 — no compatibility issues found
- **Zod v4** ships with AI SDK v6 — don't install Zod v3 separately
- **AI SDK v3 `useChat`**: use `DefaultChatTransport({body: {...}})` inside `transport:` not root `body`
- **AI SDK v3 `useChat`** destructures `{messages, sendMessage, status}` — NOT `input/handleSubmit/isLoading`
- **Memory updates should be non-blocking** — fire-and-forget with `.catch(console.error)` pattern
- **`set +H` in bash** before commands with `!` characters in values (common with DSNs/secrets)

### If We Did It Again
- Build a quick "does it compile?" check for each SDK integration before moving to the next
- Use `any` for SDK lazy-init caching from the start — fighting TS generics wastes time
- Start with `.env.local` populated with dummy values to catch build-time crashes early
