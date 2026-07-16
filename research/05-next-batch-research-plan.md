# Next Batch Research Plan — Ring Expansion

**Date:** July 13, 2026  
**Product:** Focus Dock ADHD Notion Recovery Guide ($27, 40% affiliate)  
**Goal:** Expand affiliate outreach list with **new** contacts (public emails, 5k–100k audience) without duplicating `affiliate-contacts-master.json`.

---

## Ring strategy (search outward)

| Ring | Focus | Method used | Result |
|------|-------|-------------|--------|
| **1** | ADHD + Notion overlap | Notion Marketplace creator scrape + keyword filter | **1** new (Dysfunctional Creative) |
| **2** | ADHD productivity / executive dysfunction | Podcast site contact pages, Lifestack/Feedspot channel lists | **2** new (Patricia Sung, ADHD Essentials) |
| **3** | Notion / PKM / second brain creators | Notion Marketplace category crawl (40 categories), Gumroad discover | **200** new |
| **4** | Neurodivergent newsletters | Substack about-page probe, ND community sites | **1** new (ND Out Loud) |
| **5** | ADHD coaches with YouTube + email | ADDCA/CHADD directories (mostly already in master) | **0** new |
| **6** | Productivity / planning / digital templates | Gumroad productivity sellers, batch contact_url re-probe | **1** new (Productivity HQ) |

### Why rings 1, 2, 4, 5, 6 are thin

The master list already captured most **named** ADHD YouTube/podcast/coach targets (Chris Punt, Marie Poulin, Order In The Court, 70+ ADDCA coaches, etc.). Fresh email discovery in those rings hit heavy deduplication:

- **Ring 5:** 70 ADDCA coaches already merged; CHADD directory has only 12 public profiles.
- **Ring 2:** ADHD Rewired, How to ADHD, I Have ADHD, Ryan Mayer Coaching — contact forms only, no public email found.
- **Ring 4:** Adulting ADHD, ADHD Lighthouse, Kristen Lynn McClure, Anita Goraya Substack pages — no public email on about pages.
- **Ring 1:** Most ADHD+Notion YouTube creators (Mynd, Systems Made Better, Jenna Redfield) already in master.

**Highest-yield gap:** Notion Marketplace creators with emails on official `@handle` profile pages — largely unmined vs. the master list.

---

## Gaps filled

1. **+200 Notion Marketplace sellers** with verified emails on `notion.com/@handle` pages — previously missing from master.
2. **+2 ADHD podcast hosts** with direct emails (Patricia Sung, Brendan Mahan / ADHD Essentials).
3. **+1 neurodivergent community** contact (ND Out Loud / ND Hive).
4. **+1 ADHD-adjacent Notion creator** (Dysfunctional Creative).
5. **+1 Gumroad productivity template shop** (Productivity HQ).

### Audience estimates

- **YouTube/podcast entries:** Subscriber counts from public channel data or existing research.
- **Notion Marketplace creators:** Estimated **8,000** audience (template sales + marketplace visibility). Conservative mid-range default for sellers without a public YouTube count; all fall within 5k–100k inclusive range.

### Emails verified on

- Notion Marketplace creator profile pages (`notion.com/@handle`)
- Official contact/about pages (patriciasung.com, adhdessentials.com, ndoutloud.com)
- Gumroad seller storefronts (productivityhq.gumroad.com, soltwagner.gumroad.com)

**Excluded:** Guessed emails, `example@` / `user@domain` placeholders, channels already in master by `channel_name` or `profile_url`.

---

## Batch output

**File:** `marketing/_batch_ring_expansion.json`

### Count by ring

| Ring | New prospects |
|------|---------------|
| 1 | 1 |
| 2 | 2 |
| 3 | 200 |
| 4 | 1 |
| 5 | 0 |
| 6 | 1 |
| **Total** | **205** |

### Priority breakdown

| Priority | Count |
|----------|-------|
| High | 9 |
| Medium | 196 |
| Low | 0 |

**High-priority new contacts:** Patricia Sung, ADHD Essentials, ND Out Loud, Dysfunctional Creative, Faissal Sharif, Hafsah, Ideala Templates, Desby Seb, Notomantra.

---

## Post-merge status (July 13, 2026)

| Metric | Count |
|--------|-------|
| Master contacts | **466** |
| Valid emails | **353** (target 300 ✅) |
| Future queue (unsent) | **321** |
| Future queue in 5k–100k | **220** |
| Contact forms (manual outreach) | 113 |

**Next send batch:** `python3 email-campaign.py --source future --all --send --force`

Rebuild queue after each campaign: `python3 scripts/build_future_queue.py`

---

## Progress toward 300 total emails

| Metric | Count |
|--------|-------|
| Emails in master (before merge) | 151 |
| New prospects in this batch | 205 |
| **Projected total after merge** | **356** |
| 5k–100k range in this batch | 205 (100%) |
| Target | 300 emails |
| **Surplus after merge** | +56 |

### Merge command

```bash
python3 scripts/merge_affiliate_contacts.py marketing/_batch_ring_expansion.json
```

---

## What’s still needed (next research sprint)

Even though 300 emails will be exceeded after merge, **quality diversification** remains:

| Ring | Gap | Suggested next actions |
|------|-----|------------------------|
| **1** | Only 1 new ADHD+Notion overlap | Search YouTube `"ADHD" "Notion"` 5k–50k subs; probe About pages + linked Gumroad |
| **2** | 2 new vs. many form-only | Try ADHD Rewired sponsor page, Taking Control ADHD, Attention Talk Radio sponsor inquiries |
| **4** | 1 newsletter | Beehiiv mental-health network; Substack leaderboards; probe `/@handle/about` for mailto |
| **5** | 0 new coaches | ICF/ADHD Coaches Organization directory; filter coaches with 5k+ YouTube + website email |
| **6** | 1 new | Body doubling (Caveday, Focusmate alternatives), planner TikTokers with Linktree emails |

### Recommended volume for balanced outreach

For a **balanced** portfolio (not just volume), aim for:

- 20–30 more **Ring 1–2** high-fit creators (ADHD + systems/templates)
- 15–20 more **Ring 4–5** newsletters/coaches
- Keep Ring 3 as volume backfill only when email is verified

---

## Send order recommendation

1. **High priority, Ring 1–2** (9 contacts) — send first, personalized ADHD/Notion angle
2. **Ring 3, sells templates** — batch 2, complement-not-compete framing
3. **Ring 4, 6** — batch 3
4. De-prioritize marketplace creators with generic Gmail if response rate is low (A/B test vs. named podcast hosts)

---

## Files touched

- `marketing/_batch_ring_expansion.json` — 205 new prospects
- `research/05-next-batch-research-plan.md` — this document