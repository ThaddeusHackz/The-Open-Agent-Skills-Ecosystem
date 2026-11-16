---
name: Agile Project Management at Scale
description: Sprint planning, story pointing, standup formats, retrospectives, burndown charts, RAID logs, velocity tracking, Scrum vs Kanban
---

# Agile Project Management at Scale: Enterprise Playbook

## Agile Fundamentals

Agile is not a checklist of ceremonies. It's a feedback system. Over 30 years managing teams from 3 to 500 people, I've seen Agile transform from a developer fad to the standard way knowledge workers operate. The core insight: work in short, repeatable cycles; measure progress; adjust quickly. Everything else is commentary.

## Sprint Planning (The Foundation)

### Sprint Cadence Selection

Sprint length matters. Shorter sprints = faster feedback. Longer sprints = deeper work.

```
SPRINT LENGTH DECISION TREE

1-week sprint:
  Use when: Product volatility is high, stakeholder urgency is constant
  Pros: Fast feedback, easy course correction, high engagement
  Cons: Ceremony overhead (planning eats more sprint %), shallow work possible
  Best for: Startups, teams in crisis mode, rapidly changing requirements

2-week sprint:
  Use when: Most teams. It's the default for good reason.
  Pros: Enough time for meaningful work, feedback loop is tight
  Cons: Less time for complex features
  Best for: 90% of software teams

3-week sprint:
  Use when: Teams with highly interdependent work, shipping complexity
  Pros: Time for complex features, fewer planning ceremonies
  Cons: Slower feedback, harder to plan accurately
  Best for: Infrastructure, platform teams, large refactors

4-week sprint:
  Use when: Enterprise, highly regulated, limited stakeholder availability
  Pros: Deep focus, reduced ceremony overhead
  Cons: Delayed feedback, harder to adjust course
  Best for: Rare. Usually a sign of poor planning discipline.
```

### Sprint Planning Ceremony (2 Hours for 2-Week Sprint)

**Part 1: Understanding the Goal (15 Minutes)**
```
1. Product Lead presents sprint goal
   - One sentence: "Ship customer groups feature for Acme cohort"
   - Explicitly call out what's NOT in this sprint
   - Show data: customer requests, churn impact, strategy alignment

2. Team asks clarifying questions
   - "Are we handling nested groups?"
   - "Do we need API v2 changes?"
   - "Is this blocking anything downstream?"

3. Agree on goal (team consensus, not unanimous agreement)
```

**Part 2: Backlog Refinement & Estimation (75 Minutes)**

```
STORY POINTING FRAMEWORK

Point scale (Fibonacci): 1, 2, 3, 5, 8, 13, 21
Why Fibonacci? It reflects uncertainty. Distance between 3 and 5 is small.
Distance between 8 and 13 is larger (reflecting higher uncertainty).

Baseline: Define a "3-point story"
Example: "Add user avatar to profile page"
- Time: 1-2 days work
- Complexity: Medium (API call, UI component, database field)
- Uncertainty: Known approach, no major blockers

Using that as baseline:
- 1-point: Simple, well-understood (CSS change, typo fix)
- 2-point: Straightforward (add new field, simple API call)
- 3-point: Medium (implement feature with some unknowns)
- 5-point: Complex (requires API changes, data migration, testing)
- 8-point: Very complex (cross-team dependency, new tech, high risk)
- 13-point: Too big, split it up

Stories > 13 points should be split into smaller stories.

Pointing Exercise (Planning Poker):
1. Product lead reads story
2. Each engineer estimates independently (no discussion)
3. All estimates revealed simultaneously
4. Outliers explain reasoning
5. Re-estimate if new info emerged, otherwise average or take high estimate

Example:
Story: "Implement Stripe webhook for subscription cancellation"
Engineer A: 5 points (straightforward, done this before)
Engineer B: 8 points (we haven't tested webhook resilience)
Engineer C: 5 points
Engineer D: 8 points (unfamiliar with Stripe API)

Discussion: Engineer B and D explain concerns about webhook testing and error handling.
Consensus: 8 points. Adds validation and retry logic.
```

### Sprint Planning Output

```
SPRINT BACKLOG (Sample, 2-Week Sprint)

Sprint Goal: Ship customer groups feature for Acme cohort

Epics / Initiatives:
- User-facing groups UI (13 points)
- Backend groups API (8 points)
- Groups permissions system (8 points)
- Stripe webhook integration (8 points)
Total: 37 points

Team capacity: 5 engineers × 2 weeks = 100 point-hours max
Typical: 60-70 points (leave 30-40% buffer for interruptions, bugs, meetings)

Committed: 37 points (well under capacity)

Individual Assignments:
- Frontend lead: Groups UI (13 pts)
- Backend lead: Groups API (8 pts)
- Permission specialist: Permissions system (8 pts)
- Payment engineer: Stripe webhooks (8 pts)
- Float engineer: Buffer for support, bugs, interruptions

Dependencies:
- Groups API must be complete before UI development starts (linked)
- Permissions system can start in parallel (independent)
- Stripe webhook testing requires staging environment (pre-requisite)

Blockers/Risks:
- Stripe API rate limits may affect testing (monitor)
- Unfamiliarity with permissions model (plan for pair programming)
```

## Story Pointing Best Practices

### Story Estimation Mistakes

```
Mistake 1: Conflating effort and risk
"This is uncertain, so let's call it 13 points"
Reality: Uncertainty and effort are different. A 5-point story that's uncertain
is still 5 points of work—just with higher variance.
Fix: Separate risk (acceptance criteria, spike) from effort (points).

Mistake 2: Gaming the system
Engineer inflates points to protect capacity or avoid overcommitment.
Reality: Velocity data becomes useless, planning becomes fiction.
Fix: Create psychological safety. Overcommitment should never happen
(that's the PM's job to prevent).

Mistake 3: Scope creep in stories
Estimate 3 points, then add 2 more acceptance criteria mid-sprint.
Reality: Story grows to 8 points. Metrics are wrong. Team feels behind.
Fix: Stories must be complete at planning time. Mid-sprint scope changes
become separate stories in next sprint.

Mistake 4: Varying point definitions per engineer
Engineer A thinks 5 points = 1 day. Engineer B thinks 5 points = 3 days.
Reality: Velocity is useless. Planning is fiction.
Fix: Calibrate upfront. Show same story to new and senior engineers,
ensure alignment. Periodically recalibrate (quarterly).
```

## Daily Standup (15 Minutes)

The standup is not a status report. It's a synchronization meeting to identify blockers quickly.

### Effective Standup Format

**Time-boxed: 15 minutes max. 2 minutes per person.**

```
Format:
1. What did you finish yesterday? (1 sentence)
2. What will you finish today? (1 sentence)
3. What's blocking you? (if any)

Bad standup (happens all the time):
Engineer A: "Yesterday I worked on the user avatar feature. Implemented the API
endpoint, added validation, wrote tests. Today I'll implement the frontend
component. No blockers."

Why bad? Too detailed. Wastes time.

Good standup:
Engineer A: "Shipped avatar API yesterday. Building the frontend UI today. Good
to go."

If someone shares a blocker:
Blocker: "Waiting on design approval for groups UI"
Action: PM says "I'll check on that today and get back to you by EOD"

Then move on. Detailed discussions happen offline (async Slack, 1-on-1s).

RULE: If the standup runs over 15 minutes, everyone else books a separate
meeting to discuss the blocker. Standup ends.
```

### Async Standup Alternative (Distributed Teams)

```
Slack format (post by 9 AM local time, answer comments by noon):

✅ Yesterday: Merged user auth refactor, 87 tests passing
📋 Today: Implementing password reset feature
🚧 Blocker: Need decision on email provider (SendGrid vs Resend)

Benefits:
- Timezone-friendly (async, not sync)
- Written record (easier to scan, share with async stakeholders)
- Less meeting overhead

Risks:
- Requires discipline (people skip it)
- Takes longer to identify and resolve blockers
- Can feel less connected as a team

Use async standup when:
- Team is >50% distributed across 3+ time zones
- Team is mature and self-organizing
- Blocker resolution is normally async (Slack, not meeting)
```

## Burndown Charts (Progress Tracking)

Burndown shows progress visually. It answers: "Will we finish on time?"

### Reading a Burndown Chart

```
BURNDOWN MECHANICS

Y-axis: Story points remaining
X-axis: Days in sprint (0-14 for 2-week sprint)

Ideal burndown: Linear. Start at 37 points, end at 0.
Day 1: 37 points (no progress expected, just planning)
Day 7: 18.5 points (50% complete)
Day 14: 0 points (done)

Real burndown: Jagged. Points don't burn evenly.

EXAMPLE: Good Burndown
Day 1: 37 points (backlog created)
Day 2: 35 points (2 small stories done)
Day 3: 33 points (minor work, estimation recalibration)
Day 4: 31 points (backend prep work)
Day 5: 28 points (API story started)
Day 6: 25 points (API story 60% done, frontend story starts)
Day 7: 20 points (midpoint, on track)
Day 8: 18 points (API story done, remaining work is UI-heavy)
Day 9: 14 points (UI story in progress)
Day 10: 12 points (testing found bugs, scope clarified)
Day 11: 8 points (bug fixes, acceptance criteria being met)
Day 12: 5 points (final polish, edge case handling)
Day 13: 2 points (documentation, final review)
Day 14: 0 points (release ready)

INTERPRETATION: On track to finish on time.

EXAMPLE: Concerning Burndown
Day 1: 37 points
Day 2: 36 points (slow start)
Day 3: 35 points
Day 4: 34 points (no progress, people still estimating)
Day 5: 32 points
Day 6: 30 points (midpoint, should be at 18.5, we're at 30)
Day 7: 28 points (missing the ideal line significantly)
Day 8: 25 points (acceleration starting)
Day 9: 20 points
Day 10: 15 points (catching up)
Day 11: 10 points
Day 12: 8 points
Day 13: 5 points
Day 14: 5 points (WON'T FINISH - 5 points incomplete)

ACTION: On Day 7, PM should pull 5-8 points out of sprint. Reduce scope or
extend sprint. Don't push team to overcommit.
```

### Burndown Anti-Patterns

```
Spike at the end (points added mid-sprint):
Cause: Scope creep (new stories added after planning)
Fix: New work goes to next sprint, unless it's a critical bug

Flat line (no progress for days):
Cause: Blocker, people waiting for something
Fix: Daily standup should identify. Swarm to unblock.

Burndown, then spike up (points added back):
Cause: Stories were underestimated. Acceptance criteria not met.
Fix: This is normal. Adjust estimates for future sprints. Add acceptance
criteria to your definition of done.

Perfect burndown (exactly linear):
This is fake. Real work is bursty. Very smooth burndown suggests
points are being reported optimistically or stories are too small.
```

## Retrospectives (Learning Cycles)

A retro is not complaining. It's structured reflection on: "What should we do differently next sprint?"

### Retro Format (45 Minutes for Team of 5-8)

```
RETRO: 45 MINUTES, 8 PEOPLE

Facilitator (usually Scrum Master, not manager): 5 minutes setup

1. What went well? (10 minutes)
   - Silent brainstorm: Everyone writes 2-3 things on sticky notes
   - Post on board under "Good" column
   - Cluster similar themes
   - Discuss top 3 themes

   Example good things:
   - "Pairing on the groups API saved us 2 days"
   - "Design was responsive to feedback, great collaboration"
   - "New onboarding doc helped us unblock the frontend engineer quickly"

   Action: Identify which "good" things to keep doing.
   Output: "Continue pairing on complex backend work"

2. What went badly? (10 minutes)
   - Silent brainstorm: Impediments, frustrations, issues
   - Post on board under "Bad" column
   - Cluster themes
   - Discuss top 3-5

   Example bad things:
   - "Stripe API docs were confusing, took 3 hours to find webhook retry logic"
   - "Waiting on design feedback for 2 days blocked UI work"
   - "Scope creep mid-sprint (Acme customer request added new feature)"

   Action: Identify root causes. Plan fixes.
   Output:
   - "PM to create 1-hour design review window every Monday"
   - "Store common Stripe API patterns in our docs"
   - "Lock scope after Day 1 of sprint. Urgent requests go to next sprint"

3. What should we try? (10 minutes)
   - Suggestions for next sprint
   - Experiments to run

   Examples:
   - "Let's try time-boxing the standup to 10 minutes, not 15"
   - "Can we do code review async (comments on PR) instead of in meeting?"
   - "Should we move deployments to Friday morning instead of Thursday?"

   Action: Pick ONE experiment for next sprint.
   Output: "We'll deploy on Friday 10 AM (instead of Thursday EOD) next sprint,
   measure if that reduces Friday emergency bugs"

4. Closing (5 minutes)
   - Summarize 3-5 action items
   - Assign owner and deadline (usually, do before next sprint starts)
   - Confirm team agreement

ACTION ITEMS FROM RETRO:
[ ] PM to create design review window (Monday 2-3 PM)
[ ] Engineer lead to document 3 common Stripe patterns
[ ] Team to lock scope on Day 1 of sprint
[ ] Experiment: Friday 10 AM deployments (measure emergency support tickets)
```

### Retro Anti-Patterns

```
Blame Retro:
"John committed too much work again"
"The product manager keeps changing requirements"
Why bad: Creates blame culture. People get defensive. No real improvement.
Fix: Focus on systems, not people. "How can we prevent scope creep?"
     not "Why does the PM change requirements?"

Venting Retro:
Team complains for 45 minutes. No action items result.
Why bad: Wastes time. Team leaves frustrated. Nothing changes.
Fix: Convert complaints to action items. "Design review is slow" →
     "PM owns design review. Lock-in 2-hour window Monday."

Silent Retro:
Same people talk, same issues come up, nothing new learned.
Why bad: Power dynamics silence junior engineers. Groupthink dominates.
Fix: Silent brainstorm first (no discussion). Everyone gets ideas out.
     Then discuss. Ensures all voices heard.

Retro Backlogs:
"We'll fix this next sprint"... never happens.
Why bad: Action items accumulate. Team loses trust in retro.
Fix: 3-5 items max per retro. Complete them before next retro.
     If item not done, revisit it (or drop it).
```

## RAID Log (Risk, Assumption, Issue, Decision)

Track project health continuously, not just at retros.

### RAID Log Structure

```
RAID LOG: Updated every standup, reviewed at steering meetings

| ID | Type | Status | Description | Owner | Due | Mitigated? |
|---|---|---|---|---|---|---|
| R-001 | Risk | Active | Stripe API rate limits may block testing | PaymentEng | Day 8 | Use sandbox, pre-generate test data |
| R-002 | Risk | Active | Designer sick leave May 15-20 (design block) | PM | Day 9 | Identify backup designer, frontload reviews |
| A-001 | Assumption | Active | Acme cohort can use groups in their workflow | PM | Day 7 | Confirm with customer this week |
| A-002 | Assumption | Active | Frontend can be built with existing auth system | FrontendLead | Day 5 | Spike completed, auth good for groups |
| I-001 | Issue | Resolved | Permissions model unclear to team | PlatformLead | Day 3 | Created decision doc, aligned on approach |
| I-002 | Issue | Active | Design feedback loop slow (>2 days) | PM | Day 5 | Instituted M/Th design reviews |
| D-001 | Decision | Closed | Use SendGrid for webhook retry logic | CTO | Day 4 | Agreed. PaymentEng to implement. |
| D-002 | Decision | Closed | Groups stored in Users table, not separate table | DBAdmin | Day 3 | Agreed. Reduces query complexity. |

Managing RAID:
- Add new risks/issues as they surface (daily)
- Review at standup if any blocker issues
- Retire items when mitigated or resolved
- Escalate unmitigated risks to steering committee
```

## Velocity Tracking (Predictability)

Velocity is story points completed per sprint. It lets you forecast finishing.

### Calculating Velocity

```
VELOCITY EXAMPLE

Sprint 1: Completed 28 points out of 35 committed (80% completion)
Sprint 2: Completed 32 points out of 40 committed (80% completion)
Sprint 3: Completed 25 points out of 37 committed (68% completion, big blocker)
Sprint 4: Completed 30 points out of 35 committed (86% completion)

Average velocity: (28 + 32 + 25 + 30) / 4 = 28.75 ≈ 29 points/sprint

What this means:
- You can reliably commit ~29 points per sprint
- If you have 100 points of backlog, it will take ~3.4 sprints (7 weeks)
- If you commit 40 points and only have velocity of 29, you'll miss

Using velocity to forecast:
Backlog: 200 points
Velocity: 29 points/sprint
Forecast: 200 / 29 = 6.9 sprints = ~14 weeks to complete backlog
(assuming consistent velocity and no scope creep)
```

### Improving Velocity

```
Velocity Stagnation:
Velocity flat for 4+ sprints. Team complaining of slowness.

Typical causes:
1. Too many interrupts (support, bug fixes, meetings)
2. Technical debt accumulating (code is slowing down development)
3. Underestimation (stories taking longer than expected)
4. Scope creep (stories expanding mid-sprint)

Solutions:
1. Block interrupt time (e.g., Friday = support day, preserve Mon-Thurs)
2. Allocate 1 sprint per quarter to tech debt paydown
3. Review estimation process (are we underestimating complexity?)
4. Enforce scope lock after Day 1 of sprint

Typical result: 2-4 sprint improvement cycle (6-8 weeks to see 20% velocity gain)
```

## Scrum vs Kanban: Choosing Your Model

### Scrum (Time-Boxed Iterations)

**Best for**: Teams with clear roadmap, stable requirements, need predictability

```
Scrum flow:
Planning → Sprint (1-4 weeks) → Demo → Retro → Repeat

Characteristics:
- Fixed time box (sprint length doesn't change)
- Scope can change (but only between sprints)
- Predictable velocity (enables forecasting)
- Clear milestones (end of sprint)

When to use Scrum:
- Building to a roadmap (clear feature priorities)
- Need velocity metrics for planning
- Team has high context switching (helps focus)
- Customer demands are batched (e.g., monthly release)

When NOT to use Scrum:
- Work is purely reactive (on-call, support)
- High variability in work (can't predict sprint scope)
- Small team (<4 people, ceremony overhead too high)
```

### Kanban (Continuous Flow)

**Best for**: Reactive work, variable prioritization, continuous deployment

```
Kanban flow:
Backlog → In Progress (WIP limit) → In Review → Done → Monitor

Characteristics:
- No time boxes (work flows continuously)
- WIP limits (control parallelism)
- Cycle time metrics (not velocity)
- Flexible priority (can jump queue for urgent work)

When to use Kanban:
- Reactive work (support, ops, on-call)
- Continuous deployment (ship multiple times/week)
- Variable work size (bug fixes, customer requests)
- Small team or individual contributor

When NOT to use Kanban:
- Need predictable forecast (roadmap commitment)
- Team new to software process (Scrum structure helps)
- Work requires long cycles (multi-month features)

Example Kanban board:
Backlog | In Progress (WIP: 5) | In Review (WIP: 3) | Done | Monitor (48h)
  40      [10 items]              [5 items]         [2/day] [check SLA]

Rules:
- If WIP exceeds limit, no new work starts
- In Review items must be completed before new work starts
- Monitor phase: Track for issues (SLA = <1 bug per 100 items)
```

### Hybrid Approach (Scrumban)

```
Use Scrumban when:
- Most work is Kanban-style (continuous)
- But some work is Scrum-style (predictable features)

Example:
- Kanban board for bug fixes and support (reactive)
- Sprint board for new features (planned)
- Team splits time: 20% on sprint work, 80% on Kanban

Works well for:
- Growing product orgs (features + support)
- Infrastructure teams (on-call rotations + planned work)
- Platforms with both reactive issues and proactive improvements

Typical split:
- Sprints for 3-5 planned features
- Kanban for bugs, support, tech debt
- Retros every sprint (covers both boards)
```

## Practical Checklist: Setting Up Agile at Scale

- [ ] Choose Scrum, Kanban, or hybrid based on work type
- [ ] Set sprint length (2 weeks is default for Scrum)
- [ ] Define story pointing baseline and Fibonacci scale
- [ ] Run kickoff Planning meeting with all ceremonies
- [ ] Set up physical or virtual Scrum board (Jira, Linear, etc.)
- [ ] Commit to daily standup (15 min, async-friendly for distributed teams)
- [ ] Track velocity for 2-3 sprints before using for forecasting
- [ ] Create and maintain RAID log (updated at standup)
- [ ] Run retro at end of each sprint (45 min, focus on 3-5 action items)
- [ ] Review burndown daily (identify risk early)
- [ ] Measure: velocity, cycle time, WIP, deployment frequency
- [ ] Adjust ceremony length/format quarterly based on team feedback

## Key Takeaway
Agile is feedback. Shorter cycles reveal problems faster. Metrics (velocity, burndown, cycle time) provide honest signals of team health. Use Scrum for planned work, Kanban for reactive work. The ceremony that matters most is the retro—if you're not improving weekly, you're not doing Agile, you're just doing process theater.
