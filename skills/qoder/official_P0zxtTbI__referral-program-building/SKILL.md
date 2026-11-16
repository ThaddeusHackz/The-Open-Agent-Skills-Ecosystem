---
name: referral-program-building
description: Build viral referral programs for SaaS/digital products. Covers reward structures, platform selection, tracking, fraud prevention, email templates, and KPI metrics.
version: 1.0.0
---

# Referral Program Building

Build viral referral programs that drive 2-3x higher conversion rates with 37% better retention.

## When to Use

- Designing a refer-a-friend or viral growth loop for a SaaS or digital product
- Selecting a referral platform (Rewardful, ReferralCandy, Viral Loops, FirstPromoter)
- Implementing referral tracking, link generation, and attribution in code
- Setting up fraud detection for referral abuse
- Choosing reward structures (two-sided, tiered, cash vs. credit vs. product)
- Optimizing an existing referral program with KPI analysis
- Writing referral email sequences and reward fulfillment messages

## Quick Start

1. **Define Program Type** - Choose reward structure matching business model
2. **Select Platform** - Pick tool based on scale and integration needs
3. **Implement Tracking** - Set up attribution, fraud prevention, analytics
4. **Launch & Optimize** - Soft launch, measure KPIs, iterate

## Core Principles

- **Two-Sided Rewards:** Both referrer AND referee get incentives (68% higher participation)
- **Product Alignment:** Use product as reward when possible (Dropbox model)
- **Integration:** Embed in user workflow, not separate feature
- **Simplicity:** Explain in 2-3 bullet points or it's too complex

## References

### Strategy & Design
- [Reward Structures](references/reward-structures.md) - Incentive types, tiered rewards, real-world examples
- [Platform Selection](references/platform-selection.md) - Rewardful vs ReferralCandy vs Viral Loops comparison

### Implementation
- [Technical Guide](references/technical-implementation.md) - Database schema, API patterns, attribution
- [Fraud Prevention](references/fraud-prevention.md) - Detection mechanisms, validation rules

### Operations
- [Email Templates](references/email-templates.md) - Program intro, reminders, reward fulfillment
- [Metrics & KPIs](references/metrics-tracking.md) - Participation rate, ROI, CLV tracking

## Platform Quick Reference

| Platform | Best For | Price | Setup |
|----------|----------|-------|-------|
| Rewardful | SaaS subscriptions | $49/mo | 1 hour |
| ReferralCandy | Ecommerce | $49/mo | 1-click |
| Viral Loops | Custom campaigns | Custom | Visual builder |
| FirstPromoter | Recurring commissions | Custom | Dashboard |
| Voucherify | Enterprise API-first | Custom | API integration |

## Key Metrics

- **Participation Rate:** Target 5-9%
- **Referral Rate:** Target 5-10% (avg 2.3%)
- **CAC via Referral:** Should be 30-50% lower than other channels
- **Referred CLV:** 16-25% higher than non-referred
- **Program ROI:** Successful programs see 3:1 to 5:1

## Case Study Insights

**Dropbox (3900% Growth):**
- Product-aligned reward (500MB storage)
- Integrated into onboarding step 6
- Both parties benefit equally

**PayPal (100M Users):**
- $20+$20 aggressive cash incentives
- Aligned with payment product
- 7-10% daily growth rate

**Airbnb (900% YoY):**
- Altruistic messaging outperformed selfish
- Mobile-first optimization
- Data-driven A/B testing everything

## Common Mistakes

1. **One-sided rewards only** - Programs with only referrer rewards see 40% lower participation; always reward both parties
2. **Launching without fraud detection** - Self-referrals and fake accounts drain budget fast; add IP/email checks on day 1
3. **Too complex to explain** - If you can't describe the reward in 2-3 bullet points, simplify it
4. **Rewards misaligned with product** - Cash works for PayPal; storage works for Dropbox; generic Amazon gift cards feel cheap
5. **No reminder emails** - 80% of referral links go unused; a 3-email sequence doubles utilization
6. **Hiding the share link** - Referral entry points must be in onboarding, dashboard header, AND transactional emails
7. **Not tracking attribution source** - Without UTM + metadata you can't calculate true referral CAC or ROI

## Code Examples

**Referral link generation (Node.js)**
```typescript
import crypto from 'crypto';

function generateReferralCode(userId: string): string {
  // Deterministic short code — same user always gets same code
  return crypto.createHash('sha256').update(userId).digest('hex').slice(0, 8).toUpperCase();
}

function buildReferralLink(userId: string, baseUrl: string): string {
  const code = generateReferralCode(userId);
  return `${baseUrl}/signup?ref=${code}`;
}

// Track referral on signup
async function recordReferral(newUserId: string, refCode: string, db: any) {
  const referrer = await db.users.findOne({ referralCode: refCode });
  if (!referrer || referrer.id === newUserId) return; // Prevent self-referral
  await db.referrals.create({
    referrerId: referrer.id,
    refereeId: newUserId,
    status: 'pending', // → 'rewarded' after qualifying action
    createdAt: new Date(),
  });
}
```

**Fraud detection basics**
```typescript
async function validateReferral(referrerId: string, refereeEmail: string, refereeIp: string, db: any) {
  const [emailDomain, existingIp] = await Promise.all([
    db.users.findOne({ email: { $regex: `@${refereeEmail.split('@')[1]}$` }, id: referrerId }),
    db.referrals.findOne({ refereeIp, createdAt: { $gte: new Date(Date.now() - 86400000) } }),
  ]);
  if (emailDomain) throw new Error('Self-referral via email domain');
  if (existingIp) throw new Error('Multiple referrals from same IP within 24h');
}
```

## Report Output

**Activate:** `assets-organizing` skill for report file paths

Referral reports go to `assets/reports/performance/{date}-referral-program.md`
