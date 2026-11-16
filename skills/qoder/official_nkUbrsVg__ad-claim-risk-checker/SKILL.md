---
name: ad-claim-risk-checker
description: 在电商广告文案被转化为付费广告、创作者简报、产品详情页（PDP）文案或直播带货脚本之前，对其宣称风险进行审查。它有助于识别过度宣称、缺乏支持的承诺、绝对化措辞、暗示性保证以及可能触发广告审核问题或导致客户不信任的短语。
---

# Ad Claim Risk Checker

Review ecommerce ad copy for claim risk before it gets turned into paid ads, creator briefs, PDP language, or live selling scripts.

Use this skill when a user wants to pressure-test ad copy, hooks, product claims, or creator talking points that might create compliance, platform, or credibility risk. It is useful for spotting overclaims, unsupported promises, absolute wording, implied guarantees, and phrases likely to trigger ad review issues or customer distrust.

## Use when
- Reviewing paid ad copy before launch
- Checking creator talking points for risky wording
- Sanitizing PDP or landing page claims before amplification
- Comparing a bold claim version with a safer alternative
- Reducing platform review risk without making copy useless

## Do not use when
- The user needs formal legal advice or regulatory opinions
- There is no claim language to review
- The task is general brand writing with no risk concern

## Inputs to ask for
- Exact copy to review
- Channel: TikTok, Meta, landing page, PDP, live, creator script, email
- Product category
- Evidence level: testimonials, studies, internal data, none
- Market / geography if relevant
- Desired tone: aggressive / balanced / conservative

## Workflow
1. Extract the explicit and implied claims
2. Classify claim risk by type
3. Flag unsupported, absolute, or sensitive wording
4. Rewrite the copy into safer alternatives
5. Explain what changed and why

## Output requirements
Return:
1. Original claim breakdown
2. Risk rating by line or claim cluster
3. Why the risk exists
4. Safer rewrites
5. Optional stronger-but-still-safer variation

## Risk types to watch
- Absolute outcomes
- Time-bound guarantees
- Health / body / financial outcomes
- Unqualified superiority claims
- Unsupported quantified performance claims
- Implied certainty or universal fit

## Quality bar
- Practical for operators and growth teams
- Clear risk explanations
- Rewrites still usable in real ads
- Avoids robotic compliance-speak
- No fake legal certainty

## Example prompts
- Check this TikTok ad script for risky claims and rewrite it safely
- Review these creator talking points before we send the brief
- Flag the dangerous lines in this landing page hero copy
