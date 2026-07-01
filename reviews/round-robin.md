# Focus Dock — Round-Robin Review Log

Each agent reviews prior findings + their domain. Format:
- **Gaps:** what's missing
- **Alternatives:** other angles worth considering
- **Verdict:** PASS / PASS WITH GAPS / FAIL

---

## Round 1 — Research & Positioning
**Reviewer:** Research Agent
**Verdict:** PASS WITH GAPS

### Gaps
- **No WTP validation.** Pain points are inferred from Reddit threads, blog posts, and competitor pricing — not from interviews, pre-orders, or a landing-page smoke test. $27 is *plausible* but unproven.
- **Buyer persona missing.** Research doesn't segment by: newly diagnosed vs. long-term ADHD, student vs. working adult vs. parent, Notion beginner vs. overbuilder, or "still on Notion" vs. "already quit for Obsidian/Reminders/Todoist."
- **Competitive blind spots.** Goblin.tools (free Magic ToDo) is cited as a source but absent from the competitor table — it directly solves task initiation without Notion. Same gap for Jesper Dramsch's free YouTube walkthrough (near-direct substitute for the sequence module). Also missing: Tiimo/Sunsama/Akiflow (app-switcher crowd), Marie Poulin Notion Mastery ($799 — complement angle in outreach, not in research), and Notion native AI as a "build me a system" alternative.
- **Underserved segments not explored.** (1) ADHD adults who abandoned Notion entirely — is a PDF that requires returning to Notion the right offer? (2) Neurotypical overwhelmed knowledge workers who plansturbate but don't identify as ADHD. (3) Creators' audiences who want a *file* to duplicate, not a 47-minute build — "not a template" may be a conversion blocker for part of the market.
- **Maintenance burden underweighted.** Ranked MEDIUM in research but "11-minute Sunday reset" and "daily 3-minute workflow" are strong differentiators vs. templates; they deserve equal billing with plansturbation in positioning hierarchy.
- **Internal inconsistencies.** Research claims "45+ page PDF"; `lib/product.ts` says "30-page PDF." Page count affects perceived value at $27 — align before launch.
- **"Plansturbation" term risk.** Memorable and on-brand for creator audiences, but unvalidated for cold traffic, email subjects, or audiences who find it crude/confusing. No fallback positioning tested (e.g. "template graveyard," "Notion rehab").
- **Price architecture thin.** $49 compare-at anchor is asserted, not justified with competitor screenshots or value stacking. No post–Aug 31 pricing story. No PPP/international consideration.
- **Distribution economics unstudied.** 40% affiliate commission ($10.80/sale) is generous — research doesn't model whether $16.20 net per sale supports paid acquisition or scales with creator volume.
- **Clinical/ethical boundary.** Affiliate assets warn against "cure ADHD" language; research doesn't codify what claims are safe (coaching vs. medical adjacency, medication mentions).

### Alternatives
- **Pricing:** $17 impulse tier (PDF only) / $27 standard (current) / $47–$57 with Loom install walkthrough or Notion duplicate file — tests whether "build it yourself" is friction.
- **Positioning variants:** Lead with **task sequences** for Jesper Dramsch / executive-dysfunction audiences; lead with **plansturbation** for Notion-overbuilder audiences. Same product, two hero messages.
- **Naming:** "Focus Dock" is abstract; test subheads that are literal: *Notion Rehab*, *Template Graveyard Recovery*, *The 3-Database Reset* — may convert better in search and cold email.
- **Product shape:** Optional **lite template export** as upsell ($37 bundle) — contradicts anti-template positioning but may increase completion rate and reduce refunds.
- **Segment pivot:** "Complement, don't compete" — sell explicitly as *step 0 before Mynd/Ruri/Thomas Frank templates* rather than anti-template. Outreach list already hints at this; research should own it.
- **Adjacent markets:** ADHD adults on **Apple Reminders / Google Tasks** who want structure without Notion; **workplace ADHD** angle (manager-friendly, no shame language) for B2B newsletter sponsors.
- **Channel alternatives:** Gumroad/Etsy discovery vs. creator-affiliate-only; ADHD coach wholesale (bulk license at $12/copy); free lead magnet (Emergency Overwhelm Card only) → $27 full guide.

### Strengths
- **#1 pain is monetizable.** Plansturbation / template graveyard is real, emotionally charged, and maps to documented sunk cost ($19–$129 prior purchases). Recovery framing is a credible reason to pay again.
- **Differentiation is sharp.** "Implementation protocol, NOT another template" is defensible and repeated consistently across research, `product.ts`, landing page (`Problem.tsx`, `Hero.tsx`), and affiliate scripts.
- **Pain-to-feature mapping is tight.** Brain Dump → capture friction; Today + sequences → initiation; no streaks → shame; 11-min reset → maintenance; Emergency Card → overwhelm days. Each PACKAGE_ITEM traces to a ranked complaint.
- **Anti-offer clarity.** Table of what people won't pay $27 for prevents feature creep and plansturbation-by-product-design.
- **Competitive wedge is coherent.** Undercuts $99–$129 systems, sidesteps free templates on psychology + maintenance + formulas, and doesn't compete head-on with Mynd's template catalog.
- **$27 price point fits the psychology.** Cheaper than the last template that failed; expensive enough to signal "protocol" vs. free TikTok tip; summer sale creates urgency without permanent devaluation if $49 returns Sept 1.

### Recommended actions
1. **Resolve 30 vs. 45+ page discrepancy** in `product.ts`, PDF, and all marketing before any creator sends traffic.
2. **Add 5–10 buyer interviews or a $50 ad smoke test** — validate conversion and which hook (plansturbation vs. sequences vs. guilt dashboard) drives clicks.
3. **Expand competitor table** with Goblin.tools, Dramsch free content, Akiflow/Tiimo, and Notion AI — document one-line "why we still win" for each.
4. **Write a one-page ICP:** "ADHD adult, 25–40, has spent $50+ on Notion templates, still has Notion installed, identifies with executive dysfunction" — use to filter outreach list (deprioritize pure Life OS / PPV creators).
5. **A/B hero copy** on landing page: plansturbation-led vs. "one visible next task"–led; track checkout starts.
6. **Codify post-summer pricing** in research doc: $49 standard, or permanent $27 with retired anchor — avoid orphan positioning after Aug 31.
7. **Add "complement" positioning paragraph** to research for affiliate use when pitching template sellers (Mynd, Marie Poulin): "your audience's step 0 when the template stalls."
8. **Model unit economics:** net $16.20/sale after Stripe + 40% affiliate; set max CAC and minimum creator conversion assumptions before scaling outreach.

## Round 2 — Product & PDF
*(pending)*

## Round 3 — Website & Conversion
*(pending)*

## Round 4 — Outreach & Email
*(pending)*

## Round 5 — Synthesis
**Reviewer:** Synthesis Agent
**Verdict:** **NOT READY TO LAUNCH** — fix P0 blockers first; product thesis is sound

*Inputs: R1 PASS WITH GAPS · R2 PASS WITH GAPS · R3 PASS WITH GAPS · R4 FAIL*

---

### P0 Blockers (must fix before launch)

| # | Issue | Source | Why it blocks |
|---|-------|--------|---------------|
| 1 | **Page count mismatch** — PDF is 29 pages; `product.ts` says 30; research/marketing says 45+ | R1, R2, R3 | Trust and perceived value at $27; creators will quote wrong numbers |
| 2 | **No post-purchase email / delivery flow** | R3 | Buyers pay and may never receive the PDF — refund risk and support load |
| 3 | **No privacy or refund policy pages** | R3 | Legal/trust minimum for Stripe checkout and affiliate traffic |
| 4 | **"One visible task" not enforced in Notion** | R2 | Core product promise is aspirational copy, not built into the template |
| 5 | **No screenshots in PDF** | R2 | 29-page build guide without visuals = high abandonment and refund requests |
| 6 | **Formula copy friction; no `formulas.txt`** | R2 | Users must manually retype Notion formulas — completion killer for ADHD audience |
| 7 | **Personalization notes sent verbatim as email openers** | R2, R4 | Active outreach failure; burns creator relationships on first send |
| 8 | **Affiliate `?ref=` tracking not wired** | R3, R4 | Cannot attribute or pay affiliates — distribution model breaks |

**P0 exit criteria:** A buyer can complete checkout → receive PDF → build the system in Notion using screenshots + copy-paste formulas → see exactly one task on Today view. All marketing copy matches actual page count. Legal pages live.

---

### P1 Improvements (fix before outreach)

| # | Issue | Source | Impact |
|---|-------|--------|--------|
| 1 | **Manual email templates missing for 8 high-priority creators** | R4 | Top-of-list outreach can't start without bespoke drafts |
| 2 | **Fix personalization pipeline** — notes are internal briefs, not send-ready copy | R4 | Prevents repeat of R4 FAIL on remaining 40+ contacts |
| 3 | **Canceled checkout recovery** (email or retargeting) | R3 | Recovers warm intent from summer-sale urgency |
| 4 | **Static hero countdown** — doesn't reflect real Aug 31 deadline | R3 | Urgency reads as fake once noticed; hurts conversion |
| 5 | **WTP smoke test** — 5–10 interviews or $50 ad to landing page | R1 | $27 is plausible but unproven; don't scale outreach on assumption |
| 6 | **"Complement, don't compete" positioning** for template sellers (Mynd, Marie Poulin, Thomas Frank) | R1, R4 | Outreach list already targets these creators; research doesn't arm affiliates with the pitch |
| 7 | **Align `product.ts` with PDF reality** — page count, feature claims, PACKAGE_ITEMS | R1, R2, R3 | Single source of truth before any creator sends traffic |
| 8 | **Expand competitor one-liners** — Goblin.tools, Dramsch free walkthrough, Notion AI | R1 | Affiliates and landing page need "why we still win" rebuttals |
| 9 | **Codify post–Aug 31 pricing story** | R1, R3 | Avoid orphan positioning when summer sale ends |
| 10 | **Unit economics model** — net ~$16.20/sale after Stripe + 40% affiliate | R1 | Set max CAC before paid acquisition or creator scale |

---

### P2 Nice-to-Haves

| # | Item | Source |
|---|------|--------|
| 1 | TikTok and newsletter channel exploration | R4 |
| 2 | Buyer persona / ICP one-pager (newly diagnosed vs. long-term, student vs. adult, Notion beginner vs. overbuilder) | R1 |
| 3 | **"Plansturbation" fallback copy** — "template graveyard," "Notion rehab" for cold traffic | R1 |
| 4 | Clinical/ethical claim boundaries (coaching vs. medical adjacency) | R1 |
| 5 | Optional lite template export or Loom install walkthrough ($37–$47 bundle) | R1 |
| 6 | Gumroad/Etsy discovery listing; ADHD coach wholesale license | R1 |
| 7 | Free lead magnet (Emergency Overwhelm Card only) → $27 upsell | R1 |
| 8 | PPP / international pricing consideration | R1 |
| 9 | Maintenance-burden messaging elevated in positioning hierarchy | R1 |
| 10 | Segment pivot for ADHD adults who abandoned Notion entirely | R1 |

---

### Alternative Angles Worth A/B Testing
*Consolidated from Rounds 1–4*

**Hero / positioning**
| Variant | Audience | Hypothesis |
|---------|----------|------------|
| A: **Plansturbation** — "stop decorating, start doing" | Notion overbuilders, template graveyard | Emotional hook; may fail cold traffic |
| B: **One visible next task** — executive dysfunction | Jesper Dramsch / initiation-pain audiences | Literal promise; matches built feature if P0 #4 fixed |
| C: **11-minute Sunday reset** — maintenance burden | Long-term ADHD, burned by complex systems | Differentiator vs. templates; underused in current copy |
| D: **Complement** — "step 0 before Mynd/Thomas Frank" | Template seller affiliates | Reduces adversarial framing; opens Mynd/Marie Poulin outreach |

**Naming / subheads**
- *Focus Dock* (current, abstract) vs. *Notion Rehab* vs. *Template Graveyard Recovery* vs. *The 3-Database Reset*

**Pricing**
| Tier | Offer | Tests |
|------|-------|-------|
| $17 | PDF only (impulse) | Price sensitivity floor |
| $27 | Current standard + summer sale | Baseline |
| $37–$47 | PDF + `formulas.txt` + Loom walkthrough or Notion duplicate | Whether "build it yourself" is conversion friction |
| $49 | Post–Aug 31 anchor (if sale ends) | Anchor credibility |

**Product shape**
- Protocol-only (current) vs. optional **lite template export** — contradicts anti-template positioning but may raise completion rate

**Channels**
- Creator affiliate-only (current plan) vs. Gumroad/Etsy discovery vs. ADHD coach bulk license vs. free Emergency Card lead magnet

**Landing page**
- Plansturbation-led hero vs. "one visible next task"–led hero → track checkout starts
- Real countdown vs. static deadline vs. no urgency

---

### Cross-Round Themes

1. **Promise–delivery gap** — Marketing and research describe a tighter system than the PDF/template actually enforces (page count, one visible task, formula UX).
2. **Distribution is wired on paper, broken in code** — 40% affiliate commission and creator list exist; `?ref=` and email personalization aren't production-ready.
3. **Thesis is strong, execution is mid-build** — Plansturbation pain, anti-template positioning, and pain-to-feature mapping are coherent and monetizable (R1). The gap is operational readiness, not concept.
4. **Outreach must not start until product and site are trustworthy** — R4 FAIL is a canary: sending traffic or emails now damages creator relationships and brand before a single validated sale.

---

### Final Verdict

| Dimension | Round | Status |
|-----------|-------|--------|
| Research & positioning | R1 | PASS WITH GAPS — pain is real, wedge is sharp, WTP unvalidated |
| Product & PDF | R2 | PASS WITH GAPS — content exists, delivery UX incomplete |
| Website & conversion | R3 | PASS WITH GAPS — page works, legal/delivery/tracking gaps |
| Outreach & email | R4 | **FAIL** — would burn list on send |
| **Overall** | R5 | **NOT READY TO LAUNCH** |

**Recommendation:** Hold all creator outreach. Fix P0 blockers (estimated 2–4 days focused work: PDF polish, Notion template constraint, legal pages, delivery email, affiliate tracking, email template rewrite). Run a minimal WTP smoke test (P1 #5) with 5–10 sends or $50 ads *after* P0 clears. Re-review in Round 7.

**Confidence if P0+P1 resolved:** Conditional launch approval — the $27 ADHD Notion recovery protocol is a defensible niche product with clear differentiation; success depends on completion rate and affiliate conversion, not concept validity.

## Round 6 — Implementation
**Reviewer:** Implementation Agent
**Verdict:** PASS WITH GAPS — 10 targeted fixes landed; 2 original P0s remain open

### Shipped (Round 6 scope)
- `personalized_opening` field in `creator-outreach-list.json` + `email-campaign.py` `personalized_line()`
- `?ref=` → `CheckoutButton` → `/api/checkout` `metadata.affiliate_ref` → webhook log
- `private/downloads/Focus_Dock_Formulas.txt`
- `/privacy`, `/refund` pages + Footer links
- `CanceledCheckoutBanner` on homepage (`?canceled=1`)
- `DealBadge` client component in `Hero` (live countdown via `lib/deal.ts`)
- 29-page count in `lib/product.ts`, `WhatsIncluded.tsx`, research doc; PDF confirmed 29 pages
- `manual-outreach-log.csv` + `email-send-log.json` templates
- `DOMAIN_READY` hard gate in `email-campaign.py`
- `npm run build` passes

### Not in Round 6 scope (still open from R5)
- Post-purchase delivery email (success-page download only)
- PDF screenshots / visual build guide
- `manual-outreach-templates.md` still says "30-page"

---

## Round 7 — Final Verification
**Reviewer:** Verification Agent
**Date:** July 1, 2026
**Verdict:** **NOT READY** (infrastructure) — **P0 code gaps closed**

### Round 7 P0 fixes (6/6 shipped)

| # | Fix | Status | Evidence |
|---|-----|--------|----------|
| 1 | Post-purchase delivery email | ✅ FIXED | `sendPurchaseDeliveryEmail()` in `lib/mail.ts`; webhook calls after `logPurchase()`; link `{appUrl}/success?session_id={id}`; skips with `console.warn` when `SMTP_APP_PASSWORD` unset — webhook does not fail |
| 2 | Page count in outreach templates | ✅ FIXED | `marketing/manual-outreach-templates.md` — both instances now say "29-page" |
| 3 | Formulas buyer download | ✅ FIXED | `/api/download?file=formulas` serves `Focus_Dock_Formulas.txt`; success page has secondary download button |
| 4 | Competitor one-liners (R1) | ✅ FIXED | `research/01-pain-point-research.md` — Goblin.tools, Dramsch, Notion AI table with "why we still win" |
| 5 | Complement positioning (R1) | ✅ FIXED | Same research doc — "step 0 when the template stalls" paragraph for template-seller affiliates |
| 6 | `npm run build` | ✅ PASS | Re-run after fixes (see command results below) |

### Round 6 fix checklist (10/10 verified)

| # | Fix | Status | Evidence |
|---|-----|--------|----------|
| 1 | `personalized_opening` in JSON + `email-campaign.py` | ✅ PASS | 6/11 high-priority creators have `personalized_opening`; script uses it in `personalized_line()`; fallback is generic but natural |
| 2 | `?ref=` → checkout metadata | ✅ PASS | `CheckoutButton.tsx` reads URL param → `affiliateRef` in POST body → `metadata.affiliate_ref` in `app/api/checkout/route.ts`; webhook logs on `checkout.session.completed` |
| 3 | `Focus_Dock_Formulas.txt` exists | ✅ PASS | `private/downloads/Focus_Dock_Formulas.txt` — Hide Sequence, Hide, rollups, Do This Next filters |
| 4 | `/privacy` + `/refund` + footer links | ✅ PASS | Static routes in build output; `Footer.tsx` links both under Legal |
| 5 | Canceled checkout banner | ✅ PASS | `CanceledCheckoutBanner` on `app/page.tsx`; shows on `?canceled=1`; links to `#pricing` |
| 6 | `DealBadge` client in Hero | ✅ PASS | `"use client"` component; `setInterval` tick every 60s; not static text |
| 7 | 29-page count aligned | ✅ PASS | `lib/product.ts`, `WhatsIncluded.tsx`, `research/01-pain-point-research.md`, `manual-outreach-templates.md`, PDF = 29 pages |
| 8 | Outreach log templates | ✅ PASS | `manual-outreach-log.csv` (header row); `email-send-log.json` (`sent`/`skipped` arrays) |
| 9 | `DOMAIN_READY` gate blocks sends | ✅ PASS | `--check-domain`: `Send allowed: False` — blocks on `DOMAIN_READY`, unreachable domain, missing `SMTP_APP_PASSWORD` |
| 10 | `npm run build` passes | ✅ PASS | Next.js 16.2.9 build succeeded; all routes generated |

### Command results

```
python3 marketing/email-campaign.py --dry-run
→ 5 sendable emails previewed; all personalized openers read naturally (no raw internal notes)

python3 marketing/email-campaign.py --check-domain
→ Send allowed: False (DOMAIN_READY unset, getfocusdock.com unreachable, SMTP_APP_PASSWORD unset)

npm run build
→ ✓ Compiled successfully; all routes generated
```

### Round 5 P0 comparison

| R5 # | Issue | R7 Status | Notes |
|------|-------|-----------|-------|
| 1 | Page count mismatch | ✅ FIXED | Site + PDF + research + outreach templates = 29 |
| 2 | Post-purchase email / delivery | ✅ FIXED | Webhook sends `sendPurchaseDeliveryEmail()` with success-page URL; graceful skip when SMTP unset |
| 3 | Privacy + refund pages | ✅ FIXED | Live in build |
| 4 | One visible task enforced | ⚠️ PARTIAL | PDF documents Hide Sequence formula + Do This Next view filters; buyer must build correctly — no Notion template file to enforce |
| 5 | Screenshots in PDF | ❌ **OPEN** | `generate_pdf.py` has zero image assets; 29-page text-only build guide |
| 6 | Formula copy friction | ✅ FIXED | `Focus_Dock_Formulas.txt` + inline formula pages in PDF; download API serves PDF and formulas separately |
| 7 | Personalization verbatim | ✅ FIXED | Dry-run confirms send-ready `personalized_opening` lines |
| 8 | Affiliate `?ref=` tracking | ✅ FIXED | End-to-end wired through checkout metadata |

**P0 exit criteria (R5):** Buyer checkout → PDF → build with screenshots + copy-paste formulas → one task on Today view. **Partially met** — delivery email + formulas download fixed; screenshots still missing; one-visible-task relies on user execution.

### Remaining gaps blocking launch

**P0 (product/code)**
1. **PDF screenshots** — no visual walkthrough for Notion property setup (high refund risk for ADHD audience)

**P0 (infrastructure — LAUNCH_CHECKLIST.md)**
2. **Domain not live** — `getfocusdock.com` DNS lookup fails
3. **Zoho SMTP not configured** — `SMTP_APP_PASSWORD` unset; delivery email code present but sends skipped until configured
4. **Production deploy unverified** — Stripe webhook, Vercel env vars, end-to-end checkout→download not confirmed on production URL

**P1 (before scaling outreach)**
5. WTP smoke test (5–10 sends or $50 ad) — still unvalidated
6. 5/11 high-priority creators lack `personalized_opening` (fallback generic line is acceptable but weaker)

### Dimension status

| Dimension | R5 | R7 (pre-fix) | R7 (final) |
|-----------|----|--------------|------------|
| Research & positioning | PASS WITH GAPS | PASS WITH GAPS | **PASS WITH GAPS** — competitor one-liners + complement positioning added; WTP unvalidated |
| Product & PDF | PASS WITH GAPS | PASS WITH GAPS | **PASS WITH GAPS** — formulas downloadable; screenshots still missing |
| Website & conversion | PASS WITH GAPS | PASS WITH GAPS | **PASS** — delivery email wired; legal/tracking/cancel-recovery complete |
| Outreach & email | FAIL | PASS WITH GAPS | **PASS WITH GAPS** — page count aligned; domain/SMTP block live sends |
| Infrastructure | — | NOT READY | **NOT READY** — domain, SMTP, deploy pending |
| **Overall** | NOT READY | NOT READY | **NOT READY** (infra only) |

### Recommendation

**Hold launch for infrastructure.** All Round 7 P0 code/research gaps are closed. One R5 product P0 remains (PDF screenshots). Delivery email will auto-send once `SMTP_APP_PASSWORD` is set on production.

**Minimum path to READY:**
1. Add 5–8 Notion UI screenshots to PDF (property creation, Do This Next view, Hide formula)
2. Complete LAUNCH_CHECKLIST.md Steps 1–5 (domain, Zoho, Vercel, Stripe live, smoke-test checkout)
3. Run 3-email outreach pilot (`--send --limit 3`) after domain gate passes

**Confidence after above:** Conditional launch approval for limited creator outreach.