# Outreach targeting criteria

## Subscriber range (future research)

When researching **new** affiliate partners, prioritize creators with:

| Criterion | Value | Rationale |
|-----------|-------|-----------|
| Minimum | **5,000** subscribers | Large enough to drive meaningful affiliate revenue |
| Maximum | **100,000** subscribers | More likely to respond; mega-channels rarely do paid mentions at this tier |

**Inclusive range:** 5,000 ≤ subscribers ≤ 100,000

## Existing contacts — no exclusion

All contacts already in:

- `marketing/creator-outreach-list.json`
- `marketing/affiliate-contacts-master.json`

…remain valid outreach targets even if outside 5k–100k. Examples we still email:

- **Mynd | Systems For ADHD** (~2.6k) — perfect ICP, high priority
- **Ruri Ohama** (~1.5M) — if we pursue, she's already on the list

Apply the 5k–100k filter only when **adding new names** from YouTube search, podcasts, or manual research.

## How to tag new contacts

`scripts/merge_affiliate_contacts.py` sets `in_target_range` on each merged contact:

- `true` — within 5k–100k
- `false` — below 5k or above 100k
- omitted / `null` — subscriber count unknown

Helper: `marketing/outreach_utils.py` (`parse_subscribers`, `in_target_range`).

## Outreach channel

- **Automated email:** `blacksheepdesignscontact@gmail.com` (Gmail SMTP)
- **Manual:** contact forms, LinkedIn — `marketing/manual-outreach-templates.md`

## Priority tiers (unchanged)

1. **High** — ADHD + Notion overlap, sells digital products, direct email
2. **Medium** — adjacent niche (productivity, coaching)
3. **Low** — weak fit or no contact path

Sort send queue by priority, then subscriber count (descending within range).