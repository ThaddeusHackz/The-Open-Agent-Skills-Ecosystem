---
name: sales-pipeline-crm
description: >
  ServiceTitan-style sales pipeline and CRM for fence supply distribution:
  lead-to-close funnel tracking, contractor lifecycle management, win/loss
  analysis, counter sales performance, and outbound prospecting workflows.
  Use when building CRM features, sales dashboards, or contractor acquisition flows.
---

# Sales Pipeline & CRM

## Purpose

H&J has contractor records and order history, but no visibility into the
**sales funnel**: How many leads come in? How many convert? Where do they drop off?
Who's your best salesperson? This skill adds that layer.

## When to Use

- Building sales pipeline or funnel visualization
- Creating contractor lifecycle tracking
- Designing counter sales performance dashboards
- Planning outbound prospecting workflows
- Win/loss analysis on quotes
- Sales forecasting

---

## The H&J Sales Pipeline

```
┌─────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐
│  LEAD   │→ │ CONTACT  │→ │  QUOTED   │→ │ APPROVED │→ │  ORDERED  │→ │ RETAINED │
│         │  │  MADE    │  │           │  │          │  │           │  │          │
│ Prospect│  │ Talked   │  │ Received  │  │ Said yes │  │ Placed    │  │ Repeat   │
│ exists  │  │ to them  │  │ a quote   │  │ to quote │  │ an order  │  │ customer │
└─────────┘  └──────────┘  └───────────┘  └──────────┘  └───────────┘  └──────────┘
    ↓              ↓              ↓              ↓              ↓
  Inbound:     Jorge calls   Quote Builder   Follow-up     Fulfill +
  Walk-in,     or they        generates      call/text     excellent
  phone,       visit          proposal                     service
  referral,
  drive-by
```

### Pipeline Stages

| Stage | Definition | Owner | Typical Duration |
|---|---|---|---|
| **Lead** | We know they exist but haven't talked | Marketing / system | Varies |
| **Contact Made** | First conversation happened | Counter staff | 1-3 days |
| **Quoted** | Received a formal quote from H&J | Counter staff | 1-7 days |
| **Approved** | Customer agreed to the quote | Counter staff | 1-14 days |
| **Ordered** | First order placed and paid | Counter staff | Same day as approval |
| **Retained** | 2+ orders placed | Account management | Ongoing |

### Lead Sources

| Source | Type | Volume | Cost | Quality |
|---|---|---|---|---|
| **Walk-in** | Warm | 3-5/week | $0 | High — already at your door |
| **Phone call** | Warm | 5-10/week | $0 | High — asking questions |
| **Contractor referral** | Warm | 1-2/week | $0 | Highest — pre-trusted |
| **Google search** | Cold | Varies | $15-50/lead | Medium |
| **Homeowner lead → contractor** | Cold | 2-5/week | $0 (platform generated) | Medium |
| **Drive-by prospecting** | Cold | TBD | $0.50-1/postcard | Unknown (not launched) |
| **Cold outreach** | Cold | Depends on volume | Jorge's time | Low-medium |
| **Trade shows** | Cold | Event-based | $500-2K/event | Medium |

---

## Counter Sales Performance

### What to Track Per Salesperson

| Metric | How to Calculate | Why |
|---|---|---|
| **Quotes created** | Count of quotes created by user/day | Activity volume |
| **Quote-to-order rate** | Orders / Quotes | Effectiveness |
| **Average order value (AOV)** | Total revenue / Total orders | Upselling ability |
| **Attach rate** | % of orders with hardware/accessories | Cross-sell effectiveness |
| **Response time** | Avg time from lead to first contact | Speed to lead |
| **Revenue per day** | Total revenue from their orders/day | Overall output |
| **Customer satisfaction** | Post-delivery feedback scores | Service quality |

### Performance Dashboard

```
COUNTER SALES LEADERBOARD — This Week
┌──────────┬────────┬────────┬─────────┬──────────┬──────────┐
│ Name     │ Quotes │ Orders │ Revenue │ AOV      │ Close %  │
├──────────┼────────┼────────┼─────────┼──────────┼──────────┤
│ Jorge    │ 18     │ 14     │ $42,000 │ $3,000   │ 78%      │
│ Maria    │ 12     │ 9      │ $31,500 │ $3,500   │ 75%      │
│ New Hire │ 5      │ 2      │ $4,800  │ $2,400   │ 40%      │
└──────────┴────────┴────────┴─────────┴──────────┴──────────┘
```

---

## Contractor Lifecycle Management

### Lifecycle Stages with Automated Actions

| Stage | Criteria | Auto-Action |
|---|---|---|
| **New** | Account created, no orders | Onboarding sequence (see saas-growth-engine) |
| **Active** | Ordered in last 30 days | Monthly check-in call scheduled |
| **Growing** | 3+ consecutive months of increasing spend | Send "VIP" offer, consider tier upgrade |
| **At Risk** | No order in 30-60 days | Auto-text: "Hey, need anything?" |
| **Dormant** | No order in 60-90 days | Personal call from Jorge |
| **Churned** | No order in 90+ days | Win-back campaign: "We miss you + 10% off" |
| **Champion** | $50K+ annual spend, refers others | Personal relationship from Joe |

### Win/Loss Analysis

```
On every quote that was NOT converted to an order after 14 days:

LOST QUOTE FOLLOW-UP (auto-triggered):
→ Text: "Hey [Name], you had a quote with us for [description].
   Did you go with another supplier, or can we help?"

RESPONSE CAPTURE:
□ Went with competitor → WHO? WHY? (price, delivery, product availability)
□ Project canceled → homeowner backed out
□ Still deciding → follow up in 7 more days
□ Already ordered elsewhere → lost, log reason

MONTHLY WIN/LOSS REPORT:
├── Total quotes: 45
├── Won (ordered): 32 (71%)
├── Lost to competitor: 5 (11%) → [competitor names]
├── Lost to project cancel: 3 (7%)
├── Still pending: 5 (11%)
└── Top loss reason: "Price" (3 of 5 losses)
    → Action: Review pricing on lost products
```

---

## Outbound Prospecting Workflow

### Identifying Prospects

```
PROSPECT SOURCES:
1. Google Maps: "fence contractor [city]" for every city in 50mi radius
2. Contractor license databases (state-specific)
3. HomeAdvisor / Angi contractor listings
4. Facebook groups for fence contractors
5. Job site drive-bys (see drive-by-prospecting feature)
6. Trade shows and home shows

QUALIFYING QUESTIONS:
- Do they install fence? (not just general contractors)
- How many jobs/month? (determines spend potential)
- Where do they currently buy materials? (competitor intel)
- What's their biggest pain point with current supplier?
```

### Outbound Cadence

```
DAY 1: First touch
→ Phone call or job site visit
→ "Hi, I'm Jorge from H&J Fence Supply. We supply vinyl and aluminum
   fence materials to contractors in the area. Who handles your purchasing?"

DAY 3: Follow-up (if no response)
→ Text: "Hey [Name], Jorge from H&J. We've got contractor pricing on vinyl
   and aluminum. Any jobs coming up I can quote for you?"

DAY 7: Value-add
→ Email with pricing sheet or product catalog link
→ "Here's our current pricing. No pressure — just want you to have it."

DAY 14: Check-in
→ Call: "Just checking in. Any questions about the pricing I sent?"

DAY 30: Relationship
→ Add to monthly newsletter / seasonal promo list
→ Stop active outreach, move to nurture

RULE OF THUMB: It takes 5-8 touchpoints to convert a cold prospect.
```

---

## Forecasting

### Simple Revenue Forecast Model

```
Next Month Revenue = 
  (Active Contractors × Avg Monthly Spend × Retention Rate) +
  (Pipeline Quotes × Expected Close Rate × Avg Quote Value) +
  (New Leads × Lead-to-Customer Rate × Avg First Order)

Example:
(40 × $3,000 × 0.90) = $108,000 (existing customers)
(15 × 0.70 × $2,500) = $26,250 (pipeline)
(8 × 0.20 × $1,500)  = $2,400 (new leads)
FORECAST: $136,650

Accuracy improves monthly as you accumulate real close rates.
```
