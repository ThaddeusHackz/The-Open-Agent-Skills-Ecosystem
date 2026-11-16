---
name: newsletter-curator
description: "Curate and write owner newsletters with relevant Smoky Mountain news, market data, and property insights. Use this skill whenever the user mentions owner newsletter, cabin owner update, market update email, news roundup, owner communication newsletter, monthly owner email, property owner digest, investment news, STR market news, or wants to surface and summarize relevant articles for cabin owners. Also trigger when the user mentions curating news, finding articles, or building a newsletter from current events related to the Smokies, short-term rentals, or cabin investment."
---

# Vantage Stays Newsletter Curator

## What This Does

Surfaces relevant news articles about the Smoky Mountain cabin market, short-term rental industry, local development, regulations, and tourism trends - then writes them up in the Vantage Stays owner voice for distribution as a monthly owner newsletter. The full pipeline: source articles, filter for relevance, summarize with context, write the newsletter, format for Mailchimp or Canva.

## The Voice

The Vantage owner newsletter voice is built from how the site already communicates with owners (see vantage-manage-final.html and owner-report skill). It is:

**Confident and direct.** No hedging, no "we think maybe." State the fact, then explain why it matters to them specifically as a cabin owner in this market.

**Concrete over abstract.** Use real numbers, real property names, real data points. "Occupancy tracked at 58% market-wide in Q1" not "the market is doing okay." "Dollywood's $50M NightFlight Expedition opens this spring" not "exciting new attractions are coming."

**Informed insider, not salesman.** The tone is a knowledgeable colleague sharing intel over coffee, not a marketing department writing ad copy. Owners are smart investors who want to understand the landscape and make informed decisions.

**Respects their time.** Each article summary should be 2-4 sentences. Lead with the implication for their property, then give the context. No padding, no filler, no "as always, we're here for you" platitudes.

**Grounded in local knowledge.** Reference specific locations, roads, communities, and landmarks by name. "The new Hilton dual-brand on Jake Thomas Road near Dollywood" not "a new hotel near popular attractions."

### Voice Prompt (for generating newsletter copy)

Use this prompt framework when writing newsletter content:

```
You are writing an owner newsletter for Vantage Stays, a luxury cabin management company in the Smoky Mountains (Gatlinburg, Pigeon Forge, Sevierville). Your audience is property owners who own 5-16 bedroom cabins valued at $500K-$3M+. They are sophisticated investors who want market intelligence, not cheerleading.

Voice rules:
- Write like a knowledgeable local who reads every relevant publication and distills what matters
- Lead every item with why it matters to their bottom line or their property
- Use specific numbers, names, and locations - never generic statements
- Keep summaries tight: 2-4 sentences per article, one clear takeaway per item
- No em dashes (use hyphens or commas instead)
- No emojis
- Never use the word "vibe"
- No exclamation points in body copy (one max in a subject line, only if earned)
- Avoid: "exciting," "amazing," "incredible," "game-changing," "revolutionize"
- Prefer: "notable," "significant," "worth watching," "relevant," "material"
- When mentioning Vantage's own services, be factual not promotional
- Use "in Pigeon Forge" not "on the Parkway" unless literally discussing the road itself
- Write in second person where appropriate ("your property," "your revenue")
- Contractions are fine. The tone is professional but not stiff.

Structure each news item as:
HEADLINE (brief, factual)
WHY IT MATTERS TO YOU: One sentence connecting this to their property/revenue
CONTEXT: 1-3 sentences with the details
SOURCE: Publication name and date
```

## News Categories to Monitor

Surface 5-8 articles per newsletter, pulling from these categories in rough priority order:

### 1. Market Data & Performance (always include 1-2)
- Occupancy rates, ADR, RevPAR for Sevier County
- Seasonal booking trends and year-over-year comparisons
- Supply growth (new cabin construction, new listings entering market)
- Demand indicators (park visitation, flight bookings, search trends)

**Why owners care:** This is their P&L context. They want to know if the market is tightening, softening, or stable - and how their property type specifically is performing relative to the average.

**Sources:** AirDNA, KeyData, Transparent Intelligence, Haven Vacation Rentals blog, StaySTRA, local tourism board reports

### 2. Regulatory & Tax (include when relevant)
- Tennessee STR legislation (especially the Private Property Vesting Rights bill)
- Sevier County permit requirements or changes
- Tax collection changes (hotel/motel tax, sales tax)
- Insurance market changes affecting mountain properties
- HOA or community rule changes

**Why owners care:** Regulation is the existential risk in STR investing. A single policy change can materially affect property values and income potential. Owners need to know what's coming and what it means.

**Sources:** Tennessee Lookout, Sevier County government, state legislature tracker, Tennessee REALTORS, Cedar Management blog

### 3. Local Development & Infrastructure (include 1-2)
- New attractions (Dollywood expansions, new entertainment venues)
- Hotel/resort construction that affects supply dynamics
- Road improvements, traffic infrastructure, new routes
- National Park changes (reservation systems, trail closures, new facilities)
- New restaurants or entertainment that enhance the guest experience

**Why owners care:** Development drives demand. A $50M Dollywood ride means more visitors booking cabins. A new 162-room hotel on their road means more competition for eyeballs. Both matter.

**Sources:** Pigeon Forge city news, WATE, WBIR, Knoxville News Sentinel, Dollywood press, NPS press releases, Smoky Mountain Starlight

### 4. Industry Trends (include 1 when noteworthy)
- Airbnb/VRBO policy changes affecting hosts
- Booking behavior shifts (lead time, length of stay, group size)
- Technology changes (dynamic pricing, smart home, guest communication)
- National STR market trends that contextualize local performance

**Why owners care:** Platform policy changes directly hit revenue and operations. If Airbnb loosens cancellation policies again, large-property owners feel it disproportionately (a cancelled 10-BR booking is much harder to replace than a 2-BR).

**Sources:** Skift, Phocuswire, AirDNA blog, Hostaway blog, VRMA news

### 5. Seasonal Color (include 1, rotate topics)
- Upcoming events that drive bookings (Rod Run, Winterfest, Dollywood festivals)
- Seasonal maintenance reminders tied to current weather
- Guest behavior patterns for the upcoming season
- Success stories or performance highlights from the portfolio

**Why owners care:** This keeps the newsletter from being all data and regulation. A well-timed note about "Rod Run is 6 weeks out and your calendar should already be showing movement" reminds them you're actively managing their property.

**Sources:** Events data, BrightSide booking data, internal portfolio performance

## Newsletter Structure

```
SUBJECT LINE: [Month] Owner Update: [Lead story hook]
PREVIEW TEXT: [Secondary hook, 80-100 chars]

---

HEADER: Vantage Stays - Owner Update - [Month Year]

---

LEAD ITEM (most impactful news)
[Full treatment: 4-6 sentences, clear owner implication]

---

MARKET SNAPSHOT (2-3 key metrics)
Occupancy: XX% (vs. XX% same month last year)
ADR: $XXX (trend direction)
Notable: [One sentence observation]
Source: [Data provider]

---

NEWS ROUNDUP (4-6 items)
Each item:
- Bold headline
- 2-4 sentence summary with owner angle
- Source attribution

---

ON THE HORIZON (upcoming dates/events)
- [Date]: [Event/deadline that affects bookings or operations]
- [Date]: [Event/deadline]
- [Date]: [Event/deadline]

---

FROM VANTAGE (brief, 1-2 sentences max)
[One operational update, new feature, or portfolio note. Not a sales pitch.]

---

FOOTER: Standard Vantage footer with contact info
```

## Process: End-to-End Newsletter Production

### Step 1: Source Articles (Web Search)
Search for articles published in the last 30 days using these queries:
- "Smoky Mountains" + (cabin OR rental OR STR OR vacation rental) + 2026
- "Sevier County" + (development OR regulation OR permit OR tax)
- "Pigeon Forge" OR "Gatlinburg" + (new OR opening OR construction)
- Tennessee + "short term rental" + (law OR regulation OR bill)
- "Great Smoky Mountains" + (visitation OR tourism OR park)
- Dollywood + 2026
- AirDNA OR KeyData + (Smoky Mountains OR Sevier County OR Gatlinburg)

### Step 2: Filter for Relevance
Score each article against these criteria:
- Does it directly affect cabin owner revenue? (high priority)
- Does it affect operations or compliance? (high priority)
- Does it affect demand in the market? (medium priority)
- Is it interesting context that builds market literacy? (lower priority)
- Is it actually new information, or a rehash? (discard rehashes)

Aim for 6-8 articles that together paint a complete picture of what happened this month in the owner's world.

### Step 3: Write the Newsletter
Apply the voice prompt above. Write each section following the newsletter structure. Keep the total newsletter under 800 words (owners scan, they don't read 2,000 word emails).

### Step 4: Format for Distribution
Two output options:

**Option A: HTML Email (Mailchimp)**
- Use the email brand styling from the email-campaign skill
- Navy header (#02373d) with Vantage wordmark
- Gold accents (#C9A96E) for section dividers
- Single column, 600px max width
- Mobile responsive
- Plain text fallback

**Option B: Canva Newsletter**
- Use existing Bear Camp Newsletter templates in Canva
- Follow the layout established in the July 2025 - April 2026 monthly newsletters
- Brand fonts and colors applied via brand kit

### Step 5: Review and Send
- Jessie reviews draft for accuracy and tone
- Schedule in Mailchimp for owner segment only
- Track opens/clicks for content optimization

## Data Integration

### BrightSide MCP
- `cabin_stats` - Portfolio-wide occupancy and revenue for market snapshot
- `get_specials` - Active promotions to mention in seasonal section
- `get_availability` - Booking pace indicators

### Revenue Data (`data/revenue-data.json`)
- Historical performance for year-over-year comparisons
- Per-cabin metrics if highlighting specific properties

### Events Data (`data/events-data.js`)
- Upcoming events for the "On the Horizon" section
- Seasonal booking drivers

## Example Newsletter Items (Voice Demonstration)

### Good:
**Dollywood's $50M NightFlight Expedition Opens Spring 2026**
WHY IT MATTERS: The largest single-attraction investment in Dollywood history is designed to extend visit length - guests staying an extra day means an extra night in your cabin. The 5.5-minute indoor ride (the park's longest) combines a coaster, whitewater raft, and boat ride, which signals Dollywood's strategy to compete with multi-day destinations. Expect booking lift in the Pigeon Forge corridor starting April.
Source: Dollywood Press, January 2026

### Good:
**Market-Wide Occupancy Holds at 53-58% Through Q1**
WHY IT MATTERS: Your 5+ bedroom property likely outperformed this number significantly. Investment-grade large cabins are tracking at 82% occupancy while the overall market (diluted by the surge of 2-3BR supply) sits 24 points lower. The gap between well-managed large properties and the average listing continues to widen, which is exactly the thesis Vantage operates on.
Source: Haven Vacation Rentals Q1 Report, April 2026

### Good:
**Tennessee "Private Property Vesting Rights" Bill Advances**
WHY IT MATTERS: If passed, this bill strengthens property owners' position against future local STR restrictions by requiring governments to compensate owners for regulations that reduce property value. For Sevier County owners, this is largely a backstop - the county already permits STRs and has clear licensing frameworks - but it adds a layer of protection against the kind of regulatory shifts that have hurt owners in Nashville and other Tennessee cities.
Source: Tennessee Lookout, March 2026

### Bad (too generic):
"The market is doing well and we expect a strong summer season."
(No numbers, no specifics, no real information.)

### Bad (too promotional):
"Thanks to our incredible team, your properties are outperforming the competition!"
(Cheerleading, not intelligence.)

### Bad (too long):
[Any item over 5 sentences that could have been said in 3.]

## Scheduling

- **Frequency:** Monthly (first week of month, covering previous month)
- **Send day:** Tuesday or Wednesday, 9-10am ET (highest open rates for B2B)
- **Segment:** Current property owners only (do NOT send to the full 124K guest list)

## Important Notes

- No em dashes anywhere in the newsletter
- No emojis
- Never use the word "vibe"
- Always attribute data sources - owners respect transparency
- If a news item could be perceived as negative for the market, don't spin it positive. Present it factually and explain what it means. Owners respect straight talk.
- Never reveal proprietary portfolio data (individual owner revenue, specific cabin performance) in a group newsletter. Aggregate only.
- If no significant news happened in a category, skip it. Don't pad with filler.
- The newsletter should feel like it took 3 minutes to read. If it takes longer, cut something.
