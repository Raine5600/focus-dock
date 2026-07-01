# Focus Dock — Guide Writing Blueprint (v2)

**Date:** July 1, 2026  
**Purpose:** Replace the plain, hard-to-follow v1 PDF structure with an ADHD-first reading flow  
**Audience:** Adults with ADHD who've abandoned 2+ Notion templates  
**Deliverable:** ~29-page PDF generated from `scripts/generate_pdf.py`

---

## Why v1 Fails ADHD Readers

| Problem in v1 | Fix in v2 |
|---------------|-----------|
| 18 numbered parts + appendices scattered mid-doc | 5 **lanes** only: Start → Win → Install → Daily → Reference |
| Theory before action (Part 1 before Part 2) | **Do first, understand later** — 5-min win before "why" |
| Part 8 labeled "read first" but sits after Part 0 | Self-check folded into START HERE (30 sec) |
| Long `body` paragraphs, few exit ramps | **Max 3 sentences** per paragraph; box every 150 words |
| Clinical section titles ("Executive Dysfunction") | Plain labels ("When big tasks freeze you") |
| Deep dives interrupt momentum | All lookup material **after page break into Reference** |
| Same voice throughout | **Warm coach** for action sections; **punchy tables** for reference |

**Banned word:** `plansturbation` — never in guide copy, headings, cover bullets, or glossary. Use replacement terms from [Glossary](#replacement-glossary-banned-terms) only.

---

## Voice & Tone

### You are
- A friend who's been through the template graveyard
- Direct, not preachy
- Short sentences. One idea per line when possible.
- Okay with humor, never at the reader's expense

### You are not
- A therapist
- A Notion influencer selling aesthetics
- A textbook citing Barkley before telling them what to click

### Sentence rules
| Rule | Example |
|------|---------|
| **Lead with the verb** | "Open Notion. Count your pages." not "The first step involves opening..." |
| **Cap paragraphs at 3 lines** | If it's longer, split or bullet |
| **Name the feeling, then the fix** | "That customizing high? Normal. Close the tab anyway." |
| **Numbers = anchors** | "47 minutes." "One task." "3 databases." |
| **No hedge stacks** | Delete "perhaps," "it might be helpful to consider" |
| **Second person always** | "You" not "users" or "ADHD individuals" |

### Tone samples

**❌ v1 (too clinical):**
> Research shows more options → less action. Your working memory is already taxed.

**✅ v2 (warm + direct):**
> Twelve databases = twelve decisions before breakfast.  
> Your brain is already tired. We're cutting that to **one visible task**.

**❌ v1:**
> That urge is plansturbation.

**✅ v2:**
> That urge? **Setup spiral.** Close Notion. Do one real thing.

### Formatting defaults (PDF styles)
- **h1** = lane title (yellow bar) — max 6 words
- **h2** = beat inside lane — verb-led
- **h3** = sub-step only in Install lane
- **callout** = ANCHOR, DO THIS NOW, CHECKPOINT, IF YOU DRIFT boxes
- **step** = numbered actions only — never prose
- **formula** = copy-paste blocks only in Reference
- **Tables** = decision lookup, not explanation

---

## Document Architecture (ADHD Flow)

```
COVER (promise, not essay)
  ↓
LANE 1 — START HERE (~2 pages)
  ↓
LANE 2 — 5-MINUTE WIN (~2 pages)     ← dopamine before setup
  ↓
LANE 3 — 47-MINUTE INSTALL (~8 pages)
  ↓
LANE 4 — DAILY USE (~8 pages)
  ↓
LANE 5 — REFERENCE (~9 pages)        ← appendix graveyard lives here
```

### Reading contract (page 2)
> **Don't read cover to cover.**  
> Pick a lane. Set a timer. Stop when the timer ends.

### Lane picker table (START HERE)

| If you… | Go to | Timer |
|---------|-------|-------|
| Need proof this is for you | Lane 1 → 30-sec self-check | 1 min |
| Want a win RIGHT NOW | Lane 2 — 5-Min Win | 5 min |
| Ready to build | Lane 3 — Install | 47 min |
| Already installed | Lane 4 — Daily Use | 3 min |
| Something broke / you're drowning | Lane 4 → Emergency **or** Lane 5 → Troubleshooting | 4–11 min |
| Looking something up | Lane 5 — Reference | skim |

**Default path:** Self-check (30 sec) → 5-Min Win → Install → do the one visible task → close Notion.

---

## Section Format Templates

Every content section in Lanes 1–4 uses **four box types**. Reference lane uses ANCHOR + tables only.

### 1. ANCHOR box (coral border, top of section)
*What is this? Why does it matter? How long?*

```
┌─ ANCHOR ─────────────────────────────────────┐
│ YOU ARE HERE: [Lane] → [Section name]        │
│ TIME: [X min]                                 │
│ WIN: [One sentence outcome]                   │
│ SKIP IF: [Optional — when to jump ahead]      │
└───────────────────────────────────────────────┘
```

**Word budget:** 25–40 words. No exceptions.

---

### 2. DO THIS NOW box (mint accent or bold `[>>]` prefix)
*Exact actions. Numbered. No theory.*

```
┌─ DO THIS NOW ────────────────────────────────┐
│ 1. [Physical action]                          │
│ 2. [Physical action]                          │
│ 3. [Physical action]                          │
└───────────────────────────────────────────────┘
```

**Rules:**
- 3–7 steps max per box
- Each step starts with a verb
- If a step needs a screenshot path, add `(see UI Map R-4)` — don't inline the whole table

**Word budget:** 15–80 words per box.

---

### 3. CHECKPOINT (inline callout, after each major beat)
*Binary success test. Reader knows if they can move on.*

```
┌─ CHECKPOINT ─────────────────────────────────┐
│ ✓ [Observable result]                         │
│ ✓ [Observable result]                         │
│ Stuck? → [Exact page/section pointer]         │
└───────────────────────────────────────────────┘
```

**Word budget:** 20–35 words.

---

### 4. IF YOU DRIFT (yellow tint or `⚠` prefix)
*ADHD wander recovery — no shame.*

```
┌─ IF YOU DRIFT ───────────────────────────────┐
│ Noticed yourself [common drift behavior]?     │
│ → [One recovery action]                       │
│ → Timer still running? Skip to [fallback].    │
└───────────────────────────────────────────────┘
```

**Word budget:** 25–45 words.  
**Required** after: every 5+ min block in Install, every h2 in Daily Use.

---

### Reference section template (Lane 5 only)

```
h1: [TOPIC] — REFERENCE
ANCHOR (25 words)
[Table or formula block]
[No DO THIS NOW unless "fix in 60 seconds"]
```

---

## Lane-by-Lane Outline + Word Budgets

**Total target:** ~8,500–9,500 words (29 pages at current density)  
**Per-page avg:** ~290 words — but **front-loaded action, back-loaded lookup**

---

### COVER (1 page · ~120 words)

| Element | Words | Notes |
|---------|-------|-------|
| Title + subtitle | 15 | "FOCUS DOCK / The ADHD Notion Recovery Guide" |
| 6 promise bullets | 60 | See [Cover bullets](#cover-bullets) — no banned terms |
| Tagline callout | 25 | "Stop building. Start doing." |
| Footer | 10 | Version · URL |

**Cover bullets (v2):**
- 47-minute recovery install (not another template)
- 3 databases — not 14
- One visible next task, always
- Task sequences for "I can't start"
- Copy-paste formulas included
- No streak shame · 11-min Sunday reset

---

### LANE 1 — START HERE (2 pages · ~550 words)

#### 1.1 Reading map (page 2)
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Lane picker table | 120 |
| Default path callout | 30 |
| DO THIS NOW: "Pick your lane" | 40 |

#### 1.2 30-second self-check (replaces old Part 8)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| "You need this if…" (5 checkboxes) | 80 |
| "Skip if…" (3 checkboxes) | 50 |
| CHECKPOINT: "3+ checks? → Lane 2" | 25 |
| IF YOU DRIFT: "Reading FAQ first" | 35 |

#### 1.3 What you'll build (preview only)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| 3 database one-liners + Home screen | 100 |
| DO THIS NOW: "Don't build yet" | 20 |

**Lane 1 total:** ~550 words

---

### LANE 2 — 5-MINUTE WIN (2 pages · ~650 words)

*Purpose: Task completion before Notion setup. Proves the protocol works.*

#### 2.1 The one-task rule
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Body (2 short paragraphs) | 80 |
| DO THIS NOW: Pick one avoided task | 50 |

#### 2.2 Shrink it (2-minute version)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| 3 examples (laundry, email, kitchen) | 90 |
| DO THIS NOW: Shrink YOUR task | 40 |
| CHECKPOINT: "Could do in 2 min?" | 25 |

#### 2.3 Do it on paper (no Notion yet)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| DO THIS NOW: Sticky note / notes app | 60 |
| CHECKPOINT: Task done | 20 |
| IF YOU DRIFT: Customizing phone notes app | 35 |

#### 2.4 Bridge to install
| Block | Words |
|-------|-------|
| Callout | 45 |
| "You just did the hard part" | 60 |
| DO THIS NOW: Set 47-min timer when ready | 30 |

**Lane 2 total:** ~650 words  
**v1 content absorbed:** Emergency shrink logic (Part 6), executive dysfunction examples (Part 3) — **action only, theory deferred**

---

### LANE 3 — 47-MINUTE INSTALL (8 pages · ~2,400 words)

*Purpose: Build the system. Zero philosophy.*

#### 3.0 Install preamble (½ page)
| Block | Words |
|-------|-------|
| ANCHOR | 40 |
| What you need (3 bullets) | 40 |
| RULE ZERO callout | 35 |
| IF YOU DRIFT: Tutorial videos | 40 |

**RULE ZERO (v2):**
> Urge to add a 4th database? **Setup spiral.** Close Notion. Do one real task.

#### 3.1 Minutes 0–5: Quarantine the graveyard
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| DO THIS NOW (4 steps) | 70 |
| CHECKPOINT | 25 |
| IF YOU DRIFT: Opening old dashboards | 35 |

#### 3.2 Minutes 5–15: Brain Dump
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| DO THIS NOW (6 steps) | 100 |
| Usage rule callout | 40 |
| CHECKPOINT | 25 |
| IF YOU DRIFT: Adding tags/properties | 35 |

#### 3.3 Minutes 15–30: Today + sequences
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Property list (bullets) | 80 |
| DO THIS NOW: Create properties | 90 |
| Formula pointer → `R-1 Formula Reference` | 25 |
| DO THIS NOW: Do This Next view | 60 |
| CHECKPOINT: One test task visible | 30 |
| IF YOU DRIFT: Gallery view aesthetics | 40 |

*Formulas: name + pointer only. Full paste blocks live in Reference R-1.*

#### 3.4 Minutes 30–40: Projects
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| DO THIS NOW (3 steps) | 70 |
| CHECKPOINT | 25 |

#### 3.5 Minutes 40–47: Home screen
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| DO THIS NOW (6 steps) | 100 |
| CHECKPOINT: Homepage set | 30 |
| IF YOU DRIFT: Sidebar customization | 35 |

#### 3.6 Install finish
| Block | Words |
|-------|-------|
| DO THIS NOW: One real task + mark done | 50 |
| Victory callout | 40 |

#### 3.7 Deep Dive: Minute-by-minute checklist (2 pages)
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Table minutes 0–23 | 400 |
| Table minutes 24–47 | 400 |
| CHECKPOINT | 30 |

*Absorbs v1 `INSTALL_MINUTES` table + `build_install_checklist`*

**Lane 3 total:** ~2,400 words

---

### LANE 4 — DAILY USE (8 pages · ~2,600 words)

*Purpose: Life after install. Routines, traps, recovery.*

#### 4.1 Daily workflow (3 minutes)
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Morning DO THIS NOW (3 steps) | 50 |
| During day (2 bullets) | 40 |
| Evening (2 bullets) | 40 |
| Success callout | 35 |
| CHECKPOINT | 25 |

#### 4.2 Task sequences — when big tasks freeze you
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| How it works (2 paragraphs max) | 80 |
| DO THIS NOW: Laundry example setup | 100 |
| 3 more examples (email, groceries, taxes) | 120 |
| Rule callout | 35 |
| IF YOU DRIFT: 14-step video sequence | 40 |

#### 4.3 Sequence library + worksheets (1½ pages)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| 6 pre-built sequences (table) | 350 |
| DO THIS NOW: "Pick one on a good day" | 30 |

*Absorbs v1 Part 10 + SEQUENCE_WORKSHEETS*

#### 4.4 Sunday reset (11 minutes)
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Minutes 0–3, 3–7, 7–11 blocks | 150 |
| Printable checklist pointer → `R-7` | 20 |
| CHECKPOINT | 25 |
| IF YOU DRIFT: 25-min review creep | 40 |

#### 4.5 Emergency / overwhelm (1 page)
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| 4-step DO THIS NOW | 80 |
| DO NOT list | 50 |
| Sticky-note fallback | 45 |
| Printable card pointer → `R-8` | 20 |

*Absorbs v1 Part 6 + Part 15*

#### 4.6 Days 2–7 playbook (table)
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| Day 2–7 table | 200 |
| CHECKPOINT | 25 |

#### 4.7 Week 1–4 rollout
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| 4 week blocks (bullets) | 180 |
| 21-day test callout | 40 |

#### 4.8 Maintenance — don't rebuild (replaces "ANTI-PLANSTURBATION")
| Block | Words |
|-------|-------|
| ANCHOR | 35 |
| Allowed after Day 8 | 50 |
| Banned until Day 30 | 60 |
| Setup spiral red flags table pointer → `R-5` | 25 |
| IF YOU DRIFT: "Just one new view" | 40 |

#### 4.9 Why your old system failed (MOVED from Part 1 — now optional context)
| Block | Words |
|-------|-------|
| ANCHOR: "Read when curious, not before install" | 35 |
| 3 failure modes (short) | 200 |
| Focus Dock fix callout | 40 |

*Reader hits this **after** they're using the system — not before.*

#### 4.10 Accountability without shame
| Block | Words |
|-------|-------|
| ANCHOR | 30 |
| 3 tactics + 3 avoids | 180 |

**Lane 4 total:** ~2,600 words

---

### LANE 5 — REFERENCE (9 pages · ~2,300 words)

*Everything skimmable. No narrative arc required.*

| ID | Section (v1 source) | Pages | Words |
|----|---------------------|-------|-------|
| R-1 | Formula Reference — Copy-Paste | 1 | 250 |
| R-2 | Notion UI Quick Map | 1 | 200 |
| R-3 | Property Reference Card | ½ | 150 |
| R-4 | When to Use What — Decision Table | ½ | 180 |
| R-5 | Setup Spiral Red Flags (was Plansturbation Red Flags) | 1 | 220 |
| R-6 | Troubleshooting (Appendix B + Part 13) | 1½ | 400 |
| R-7 | Sunday Reset Checklist — Printable (Part 15A) | 1 | 150 |
| R-8 | Emergency Card — Printable (Part 15) | 1 | 120 |
| R-9 | What to Delete from Old Templates (Part 9) | 1 | 250 |
| R-10 | Migration Checklist | ½ | 150 |
| R-11 | Brain Dump Processing Guide | ½ | 180 |
| R-12 | Energy Matching — Optional (Part 14) | ½ | 150 |
| R-13 | FAQ (Part 16) | 1 | 300 |
| R-14 | Glossary (Part 17 — rewritten) | ½ | 150 |
| R-15 | Research Notes (Part 18) | ½ | 150 |
| R-16 | You Made It + support | ½ | 100 |

**Lane 5 total:** ~2,300 words

---

## v1 → v2 Section Migration Map

| v1 Section | v2 Location | Change |
|------------|-------------|--------|
| Cover "anti-plansturbation" | Cover bullet rewrite | Banned term removed |
| HOW TO USE THIS GUIDE | Lane 1 + 3.0 preamble | Split; RULE ZERO in 3.0 |
| PART 8 Self-Assessment | Lane 1.2 | 30 sec, not "Part 8" |
| PART 1 Why old system failed | Lane 4.9 | **After** daily use |
| PART 2 Install | Lane 3 | + box templates |
| DEEP DIVE Install Checklist | Lane 3.7 | Stays with install |
| PART 3 Task Sequences | Lane 4.2 | Renamed, shorter intro |
| PART 4 Daily Workflow | Lane 4.1 | First in Daily lane |
| PART 5 Sunday Reset | Lane 4.4 | + drift box |
| PART 6 Emergency | Lane 4.5 | |
| PART 7 Anti-Plansturbation | Lane 4.8 | Renamed |
| PART 9 Delete from templates | R-9 | Reference |
| PART 10 Sequence library | Lane 4.3 | |
| PART 11 Week 1–4 | Lane 4.7 | |
| PART 12 Property ref | R-3 | Reference |
| PART 13 Common mistakes | R-6 | Merged w/ troubleshooting |
| PART 14 Energy | R-12 | Optional appendix |
| PART 15 / 15A Printables | R-7, R-8 | Reference tail |
| PART 16 FAQ | R-13 | |
| PART 17 Glossary | R-14 | Rewritten |
| PART 18 Research | R-15 | Last — never interrupt action |
| Brain Dump Guide | R-11 | |
| Notion UI Map | R-2 | |
| Formula Reference | R-1 | |
| Days 2–7 Playbook | Lane 4.6 | |
| Accountability | Lane 4.10 | |
| Plansturbation Red Flags | R-5 | Renamed |
| Migration Checklist | R-10 | |
| When to Use What | R-4 | |
| APPENDIX C You Made It | R-16 | |

---

## Replacement Glossary (Banned Terms)

### Primary ban
| ❌ Never use | ✅ Use instead | When |
|-------------|----------------|------|
| plansturbation | **setup spiral** | Default replacement |
| plansturbation | **productivity theater** | When describing *feeling* productive while not doing |
| plansturbation | **building instead of doing** | Verb-first headers, RULE ZERO |
| plansturbation | **template graveyard behavior** | When linking to abandoned templates |
| anti-plansturbation | **recovery protocol** | Cover, positioning |
| anti-plansturbation | **anti-rebuild rules** | Maintenance section title |
| plansturbation red flags | **setup spiral red flags** | Reference table title |
| plansturbation bait | **customization trap** | Install drift boxes |
| plansturbation bait | **aesthetic trap** | Minute 35 checklist row |
| "plansturbation crowd" | **template graveyard crowd** | Marketing only — not in PDF |
| "plansturbating" | **stuck in a setup spiral** | Any verb form |

### Keep (already good)
| Term | Notes |
|------|-------|
| template graveyard | Concrete image — keep |
| one visible next task | Product promise |
| choice overload | Research-backed, fine in R-15 |
| streak shame | Emotional, accurate |
| executive dysfunction | Use sparingly; prefer "can't start" in action lanes |
| brain dump | Brand language |
| Do This Next | View name — proper noun |

### Glossary entries (R-14 — v2 copy)

| Term | One-line definition |
|------|---------------------|
| **Setup spiral** | Tweaking your system instead of doing the task the system was for. |
| **Template graveyard** | Folder of abandoned Notion setups you avoid opening. |
| **Productivity theater** | Looks productive. Zero tasks finished. |
| **Task sequence** | Linked sub-tasks — only the next step shows. |
| **Brain dump** | 2-second capture. No tags. No guilt. |
| **Choice overload** | Too many options → you pick nothing. |
| **Visible state** | Dashboard junk that looks broken when you skip a day. |
| **Building instead of doing** | Saturday setup, Wednesday ghost. |

---

## IF YOU DRIFT — Standard Recovery Lines

Reusable copy. Swap `[X]` per section.

| Drift signal | Recovery line |
|--------------|---------------|
| Watching Notion tutorials | "Close YouTube. Open **R-2 UI Map**. Find the button. Move on." |
| Customizing colors/icons | "Aesthetic trap. Defaults are fine until Day 8." |
| Adding a 4th database | "Setup spiral. Close Notion. One real task. Return tomorrow." |
| Reading FAQ before install | "Lane 2 first. FAQ is **R-13**. Win before walls of text." |
| Perfecting formulas | "Copy from **R-1**. Good enough beats perfect." |
| Sunday reset past 11 min | "Timer's done. Stop. Incomplete beats skipped." |
| Building 14-step sequence | "Max 6 steps today. Break more later." |
| Opening template graveyard | "Don't open. Drag away. Curiosity is a trap." |

---

## Implementation Checklist for `generate_pdf.py`

When rewriting the PDF generator:

- [ ] Reorder `build_content()` to match Lanes 1–5
- [ ] Add helper: `anchor_box()`, `do_this_now()`, `checkpoint()`, `if_you_drift()`
- [ ] Rename `build_plansturbation_red_flags` → `build_setup_spiral_red_flags`
- [ ] Replace all 8 `plansturbation` strings in `generate_pdf.py` (grep confirm zero)
- [ ] Update `start_here_page()` lane picker to match v2 table
- [ ] Move Part 1 content block after Lane 4 maintenance
- [ ] Move Part 18 to final pages before R-16
- [ ] Cover bullet: "47-minute anti-plansturbation" → "47-minute recovery install"
- [ ] Part 7 title → "MAINTENANCE — ANTI-REBUILD RULES"
- [ ] Glossary: remove Plansturbation entry; add Setup spiral
- [ ] Word-count audit: no section body >120 words without a box interrupt

---

## Success Metrics (Is the rewrite working?)

| Signal | Target |
|--------|--------|
| Time to first **completed task** | < 5 min (Lane 2) |
| Time to first **Notion task done** | < 50 min (Lane 2 + 3) |
| Avg paragraph length | ≤ 3 sentences |
| Box interrupt frequency | ≥ 1 per page in Lanes 1–4 |
| Reader-reported "where am I?" | Lane picker answers in 10 sec |
| Banned term in PDF | **0** occurrences |

---

## One-Page Summary for Writers

1. **Warm, direct, short.** Verb-first. No clinical walls.
2. **Order:** START HERE → 5-min win → install → daily → reference.
3. **Every section:** ANCHOR → DO THIS NOW → CHECKPOINT → IF YOU DRIFT.
4. **Theory comes after action.** "Why you failed" is Lane 4.9, not page 3.
5. **Never say plansturbation.** Setup spiral. Productivity theater. Building instead of doing.
6. **Appendix is a graveyard for density** — formulas, printables, FAQ, research go last.
7. **Default path fits on a sticky note:** Check → Win → Install → One task → Close.

---

*Blueprint path:* `/Users/cameron/focus-dock/research/03-guide-writing-blueprint.md`