# Focus Dock — ADHD-Friendly PDF Design System Spec

**Date:** July 1, 2026  
**Purpose:** Evidence-based visual + writing rules for `scripts/generate_pdf.py` (ReportLab)  
**Audience:** Adults with ADHD who abandon long guides mid-read  
**Companion docs:** `03-guide-writing-blueprint.md` (content architecture), `01-pain-point-research.md` (user psychology)

---

## Executive Summary

ADHD readers don't fail guides because they lack intelligence — they fail because **attention wanders when cognitive load spikes**. Research across UX (NN/g), accessibility (WCAG, Recite Me, WebAIM), instructional design (eLearning Industry), and ADHD-specific publishing (ADDitude, Alphero) converges on one pattern:

> **Connected flow for action content** (clean hierarchy, whitespace, predictable boxes) + **controlled novelty** (color accents, checkpoints, progress signals) + **zero shame walls of text**.

This spec translates that into ReportLab constants, `ParagraphStyle` definitions, layout breakpoints, and helper functions a developer can implement without design guesswork.

---

## Design Principles (Ranked)

| Priority | Principle | Source | Implementation |
|----------|-----------|--------|----------------|
| 1 | **Chunk everything** | NN/g chunking; Miller 7±2 | Max 3 sentences/paragraph; box every ~150 words |
| 2 | **Action before theory** | ADDitude planner patterns; Focus Dock v2 blueprint | Lane order: win → install → daily → reference |
| 3 | **Progress is always visible** | HeyNova ADHD UX; eLearning Industry | Lane tracker in footer; CHECKPOINT after every beat |
| 4 | **High contrast, low noise** | WCAG 1.4.3; Recite Me | 4.5:1 body text; max 3 accent colors per page |
| 5 | **Tidy but not boring** | eLearning Industry (Gillan-Bronze) | Consistent box types; vary content inside, not chrome |
| 6 | **Matte, calm surfaces** | Alphero print research | Flat fills; no gradients; off-white body background |
| 7 | **Recovery without shame** | Focus Dock pain research | IF YOU DRIFT boxes; no red "failure" styling |

---

## Typography & Hierarchy

### Font Stack (ReportLab)

**Primary (register if available, else fallback):**

```python
# Preferred: Lexend or Verdana — ADHD/dyslexia-friendly sans-serifs
# Recite Me, Google Fonts research: clear shapes, generous spacing, moderate weight
FONT_REGULAR = "Helvetica"       # fallback built-in
FONT_BOLD    = "Helvetica-Bold"
FONT_MONO    = "Courier"         # formulas only

# Optional registration (ship TTF in scripts/fonts/):
# pdfmetrics.registerFont(TTFont("Lexend", "Lexend-Regular.ttf"))
# FONT_REGULAR = "Lexend"
```

**Why not decorative fonts:** ADHD-friendly type prioritizes legibility over personality — minimal letter shapes, clear ascenders/descenders, consistent x-height (Recite Me, BDA dyslexia style guide).

### Size Scale (pt)

| Style key | Use | fontSize | leading | fontName | spaceBefore | spaceAfter |
|-----------|-----|----------|---------|----------|-------------|------------|
| `title` | Cover H1 only | **28** | **42** (1.5×) | Bold | 0 | 12 |
| `subtitle` | Cover subhead | **14** | **21** | Regular | 0 | 20 |
| `lane_label` | Footer / progress | **9** | **13** | Bold | 0 | 0 |
| `h1` | Lane + section titles | **20** | **30** | Bold | 16 | 10 |
| `h2` | Beat inside lane | **15** | **22** | Bold | 14 | 8 |
| `h3` | Install sub-steps only | **12** | **18** | Bold | 10 | 6 |
| `body` | Prose | **11** | **17** (≥1.5×) | Regular | 0 | 10 |
| `callout_label` | Box type prefix | **9** | **13** | Bold | 0 | 4 |
| `callout_body` | Box content | **11** | **17** | Regular/Bold mix | 0 | 0 |
| `step` | Numbered actions | **11** | **17** | Regular | 0 | 6 |
| `formula` | Copy-paste blocks | **9** | **14** | Mono | 0 | 8 |
| `table_cell` | Dense reference | **8.5** | **13** | Regular | — | — |
| `table_header` | Table heads | **9** | **13** | Bold | — | — |
| `footer` | Page meta | **9** | **13** | Regular | 0 | 0 |

**WCAG 1.4.12 targets (apply to `body`, `step`, `callout_body`):**
- Line height ≥ **1.5×** font size → 11pt / 17pt leading ✓
- Paragraph spacing ≥ **2×** font size → `spaceAfter=10` minimum between paragraphs; use `Spacer(1, 14)` between sections
- Letter spacing: ReportLab lacks easy tracking; compensate with slightly wider margins and short line lengths

### Line Length

- **Target:** 50–75 characters per line (NN/g chunking)
- **Content width:** 6.5″ on letter with 0.75″ margins (= 8.5″ − 1.5″)
- **Rule:** If a paragraph exceeds ~75 chars/line visually, split into bullets

### Heading Rules

| Level | Max words | Visual treatment |
|-------|-----------|------------------|
| h1 | 6 | Yellow bar background (`backColor=YELLOW`, `borderPadding=8`) |
| h2 | 8 | Coral text, no background — verb-led ("Quarantine the graveyard") |
| h3 | 5 | Navy text — install sub-steps only |

**Never:** ALL CAPS blocks >3 words (reads as shouting + harder to track). Use caps only for box labels: `ANCHOR`, `DO THIS NOW`.

---

## Color Palette

### Core Tokens (implement as `reportlab.lib.colors.HexColor`)

```python
# --- Backgrounds ---
PAGE_BG     = "#FAF8F5"   # warm off-white (reduces glare vs pure white; dyslexia research)
LIGHT_BG    = "#F4F6FB"   # callout fill / table zebra
BOX_MINT    = "#E8FAF7"   # DO THIS NOW background
BOX_YELLOW  = "#FFF8E1"   # IF YOU DRIFT background
BOX_CORAL   = "#FFF0EC"   # ANCHOR background (light coral tint)

# --- Text ---
DARK_TEXT   = "#1A1A2E"   # body — contrast ~14:1 on PAGE_BG
MID_TEXT    = "#3D3D5C"   # secondary, footer
NAVY        = "#1A1F3D"   # headings, table headers

# --- Accents (max 2 per page besides navy) ---
CORAL       = "#FF6B4A"   # action, h2, borders — CTAs
MINT        = "#3DD6C3"   # success, completion, cover subtitle
YELLOW      = "#FFD93D"   # h1 bar, attention (not large fields)
WHITE       = "#FFFFFF"

# --- Semantic (icons-as-text prefixes, not full backgrounds) ---
CHECK_GREEN = "#2D936C"   # ✓ in CHECKPOINT only
WARN_AMBER  = "#E6A800"   # ⚠ in IF YOU DRIFT only
```

### Contrast Requirements (WCAG AA)

| Pair | Ratio | Pass |
|------|-------|------|
| DARK_TEXT on PAGE_BG | ~13.5:1 | ✓ AAA |
| DARK_TEXT on LIGHT_BG | ~12:1 | ✓ AAA |
| NAVY on YELLOW (h1 bar) | ~8:1 | ✓ AAA |
| WHITE on NAVY (tables) | ~14:1 | ✓ AAA |
| CORAL text on PAGE_BG | ~3.2:1 | ⚠ large text only — use for h2 at 15pt (3:1 large-text threshold) |

### Color Behavior Rules

1. **Page canvas:** Set `PAGE_BG` on all content pages (not pure white). Cover may use full-bleed NAVY.
2. **Accent budget:** No more than **2 accent hues** (coral, mint, yellow) in large areas on a single page.
3. **No color-only meaning:** Always pair color with text label (`✓`, `>>`, `⚠`, `[OK]`).
4. **Avoid:** Saturated red/green adjacent blocks; neon gradients; gray-on-gray below 4.5:1.
5. **Print-safe:** All fills matte flat — no transparency overlays (Alphero: glare reduction).

### Box Color Mapping

| Box type | Border | Background | Label color |
|----------|--------|------------|-------------|
| ANCHOR | CORAL 2pt | BOX_CORAL | CORAL |
| DO THIS NOW | MINT 2pt | BOX_MINT | NAVY |
| CHECKPOINT | NAVY 1pt | LIGHT_BG | CHECK_GREEN for ✓ lines |
| IF YOU DRIFT | WARN_AMBER 2pt | BOX_YELLOW | WARN_AMBER |

---

## Page Layout Rules

### Document Geometry

```python
PAGESIZE = letter          # 8.5 × 11 in (612 × 792 pt)
MARGIN   = 0.75 * inch     # all sides
CONTENT_W = 6.5 * inch     # 8.5 - 1.5
FOOTER_Y = 0.5 * inch      # page number band
```

### Word Density Limits

| Zone | Max words / section block | Max words / page | Box interrupt |
|------|---------------------------|------------------|---------------|
| Lanes 1–4 (action) | 120 body without box | ~220–260 | ≥1 box per page |
| Lane 5 (reference) | 200 (tables count as 1 block) | ~300 | ANCHOR only |
| Cover | 120 total | 1 page | N/A |

**Paragraph limits:**
- Body: **≤3 sentences** or **≤60 words**
- DO THIS NOW: **3–7 steps**, **15–80 words** total
- ANCHOR: **25–40 words** (hard cap)
- CHECKPOINT: **20–35 words**
- IF YOU DRIFT: **25–45 words**

### When to Page Break

| Trigger | Action |
|---------|--------|
| New lane (START → WIN → INSTALL → DAILY → REFERENCE) | `PageBreak()` before h1 |
| CHECKPOINT completes a 5+ min install block | Optional break if page >85% full |
| Deep-dive checklist | Force break between min 0–23 and 24–47 |
| Reference section | Each R-* topic may share pages; break before printables (R-7, R-8) |
| h1 would orphan at bottom | Insert `PageBreak()` if <1.5″ space remaining (use `KeepTogether` for box+checkpoint pairs) |

### Vertical Rhythm

```python
SPACE_SECTION = 14   # pt after h1 rule
SPACE_BOX     = 8    # pt before/after callout tables
SPACE_BEAT    = 10   # pt between h2 blocks
```

### White Space Targets

- **Minimum 30%** of action-lane pages should be non-text (boxes, spacing, rules) — eLearning "tidy slides" principle
- **Connected flow:** Action lanes use aligned left edge, consistent box width (`CONTENT_W`), predictable order: ANCHOR → body → DO THIS NOW → CHECKPOINT → IF YOU DRIFT

---

## Visual Elements

### 1. Callout Box System (ReportLab `Table` wrapper)

Implement four helpers — matches `03-guide-writing-blueprint.md`:

```python
def _callout_table(label, body_html, styles, border_color, bg_color, label_color):
    """Single-width callout. Returns Table flowable."""
    label_para = Paragraph(
        f'<font color="{label_color}"><b>{label}</b></font>',
        styles["callout_label"],
    )
    body_para = Paragraph(body_html, styles["callout_body"])
    t = Table(
        [[label_para], [body_para]],
        colWidths=[CONTENT_W],
    )
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), 2, border_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 8),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t

def anchor_box(you_are_here, time_min, win, skip_if=None, styles=...):
    lines = [
        f"<b>YOU ARE HERE:</b> {you_are_here}",
        f"<b>TIME:</b> {time_min}",
        f"<b>WIN:</b> {win}",
    ]
    if skip_if:
        lines.append(f"<b>SKIP IF:</b> {skip_if}")
    return _callout_table("ANCHOR", "<br/>".join(lines), styles, CORAL, BOX_CORAL, CORAL)

def do_this_now(steps: list[str], styles=...):
    items = "".join(f"{i+1}. {s}<br/>" for i, s in enumerate(steps))
    return _callout_table("DO THIS NOW", items, styles, MINT, BOX_MINT, NAVY)

def checkpoint(lines: list[str], stuck_pointer: str, styles=...):
    body = "<br/>".join(f"✓ {l}" for l in lines)
    body += f"<br/><b>Stuck?</b> → {stuck_pointer}"
    return _callout_table("CHECKPOINT", body, styles, NAVY, LIGHT_BG, CHECK_GREEN)

def if_you_drift(signal: str, recovery: str, fallback: str, styles=...):
    body = (
        f"Noticed yourself {signal}?<br/>"
        f"→ {recovery}<br/>"
        f"→ Timer still running? Skip to <b>{fallback}</b>."
    )
    return _callout_table("⚠ IF YOU DRIFT", body, styles, WARN_AMBER, BOX_YELLOW, WARN_AMBER)
```

### 2. Progress Tracker (Lane Indicator)

**Header strip (optional per lane start):**

```
LANE 2 OF 5 — 5-MINUTE WIN          [████░░░░░] ~2 pages
```

**Footer (every page after cover):**

```python
def add_page_number(canvas, doc):
    canvas.saveState()
    lane = getattr(doc, "current_lane", "")  # set before each lane
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_TEXT)
    canvas.drawString(MARGIN, 0.5 * inch, f"Focus Dock · {lane} · getfocusdock.com")
    canvas.drawRightString(PAGE_W - MARGIN, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()
```

**ADDitude / planner pattern:** Show *where you are*, *how long it takes*, and *what done looks like* — ANCHOR box handles micro-progress; footer handles macro.

### 3. Icon System (Text / Unicode Only)

Do **not** embed icon fonts or images for UI markers — ReportLab embedding is fragile. Use prefixed text tokens (already in `generate_pdf.py`):

| Token | Meaning | Usage |
|-------|---------|-------|
| `[OK]` | Promise / included feature | Cover bullets |
| `>>` | Immediate action / rule | RULE ZERO, callouts |
| `✓` | Binary success | CHECKPOINT |
| `⚠` | Wandering attention recovery | IF YOU DRIFT |
| `[BRAIN]` `[TODAY]` `[HOME]` | Database names | Install steps |
| `[ ]` | Checkbox (printable) | Self-assessment |
| `—` | Lane separator | Tables |

**Rule:** One icon max per line. Icons always left-aligned before text.

### 4. Dividers & Section Rules

```python
HRFlowable(width="100%", thickness=2, color=CORAL, spaceAfter=10)  # under h1
HRFlowable(width="30%", thickness=1, color=MID_TEXT, spaceAfter=6) # optional h2 subtle break
```

### 5. Tables (Reference Lane)

- Zebra rows: `WHITE` / `LIGHT_BG` alternating
- Header row: `NAVY` bg, `WHITE` text
- Cell padding: 6–8pt
- **Never** nest tables inside callout boxes

### 6. "Do This Now" Interrupts (Inline)

For short interrupts inside prose (not full box):

```python
Paragraph('<font color="#3DD6C3"><b>[>>]</b></font> Set a 5-minute timer. Pick one task.', styles["body"])
```

Use full `DO THIS NOW` box when ≥3 steps.

---

## Writing Rules

### Voice

- Second person (**you**), warm coach, verb-first
- Name the feeling → give the fix ("That customizing high? Normal. Close the tab.")
- Numbers as anchors: "47 minutes." "One task." "3 databases."

### Sentence & Structure

| Rule | Target | Rationale |
|------|--------|-----------|
| Sentence length | **≤20 words** body; **≤12 words** in steps | Working memory (Miller, NN/g) |
| Paragraph | **≤3 sentences** | Recite Me / chunking |
| Step lines | Start with **imperative verb** | Plain language (stylemanual.gov.au) |
| Jargon | Define on first use or defer to Reference | Cognitive load |
| Hedge words | Ban: perhaps, might consider, it may be helpful | Reduces decision fatigue |

### Headline Formula

```
h2 = [Verb] + [object]     → "Quarantine the graveyard"
h3 = [Minute/task label]   → "Roll-ups for sequences"
```

### Lists vs Prose

| Content type | Format |
|--------------|--------|
| Actions | Numbered `step` style |
| Options / examples | Bullets (max 5) |
| Lookup data | Table |
| Copy-paste | `formula` block in Reference only |

### Banned Patterns

- Walls of text (>120 words without box)
- Passive voice in instructions ("The database should be created")
- Shame language ("failed," "wrong," "non-compliant")
- Rhetorical questions before instructions
- More than one idea per step line

### Reading Level

- Target **Flesch-Kincaid grade 6–8**
- Max **3 clauses** per sentence
- One **concrete noun** per instruction (Notion page name, button label)

---

## Cover Page Design

### Layout (Full-Bleed Header Band)

```
┌─────────────────────────────────────────────┐
│████████████ NAVY FULL WIDTH ████████████████│  ← 30% page height
│              FOCUS DOCK (28pt white)         │
│     The ADHD Notion Recovery Guide (mint)    │
├─────────────────────────────────────────────┤
│  PAGE_BG body                                │
│  [OK] bullet 1                               │
│  [OK] bullet 2                               │  ← max 6 bullets
│  ...                                         │
│  ┌─────────────────────────────────────┐    │
│  │ Stop building. Start doing. (callout)│    │
│  └─────────────────────────────────────┘    │
│  Version 1.0 · July 2026 · getfocusdock.com  │
└─────────────────────────────────────────────┘
```

### Cover Rules

| Element | Spec |
|---------|------|
| Title placement | Vertical center of NAVY band (not page top) |
| Promise bullets | **6 max**, **≤10 words each**, verb or number-led |
| Subtitle | Clarifies audience + product type — not a paragraph |
| Tagline callout | **≤25 words**, single sentence |
| Imagery | **None** on cover — novelty comes from color blocks, not photos |
| White space | **≥40%** of page below band uncluttered |

### Cover Copy Pattern (from ADDitude / How to ADHD style)

- Lead with **timeboxed outcome** ("47-minute recovery install")
- Quantify constraints ("3 databases — not 14")
- State emotional relief ("No streak shame")
- Avoid feature dumps and clinical language on cover

---

## ReportLab Implementation Checklist

### Phase 1 — Constants & Styles

- [ ] Add `PAGE_BG` and box tint colors to palette
- [ ] Update `body` leading to 17pt (1.5×)
- [ ] Add `callout_label`, `callout_body`, `lane_label` styles
- [ ] Set `onPage` to paint `PAGE_BG` rectangle full page before content

```python
def paint_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, letter[0], letter[1], fill=1, stroke=0)
    canvas.restoreState()
    add_page_number(canvas, doc)
```

### Phase 2 — Box Helpers

- [ ] Implement `anchor_box`, `do_this_now`, `checkpoint`, `if_you_drift`
- [ ] Wrap each helper output in `KeepTogether([...])` to avoid orphan splits
- [ ] Add `section_v2()` builder accepting box flowables between prose blocks

### Phase 3 — Layout Enforcement

- [ ] Word-count lint in build step (warn if body block >120 words)
- [ ] Lane `PageBreak()` at Lanes 1–5 boundaries
- [ ] Footer lane label via `doc.current_lane` attribute

### Phase 4 — Cover

- [ ] NAVY band = `Table` with fixed height ~2.8″, full `CONTENT_W`
- [ ] Bullets use `[OK]` text icon only
- [ ] Remove banned terms from cover (per blueprint)

### Phase 3 Content Order

Align generator with `03-guide-writing-blueprint.md` lane architecture — design spec is agnostic to copy but **requires** box template on every action section.

---

## Patterns from Successful ADHD Resources

### ADDitude / ADHD Planners

- **Time estimates on every section** → ANCHOR `TIME:` field
- **Checkbox self-assessment before commitment** → Lane 1.2
- **Printable tear-out cards** → Reference R-7, R-8 with minimal ink
- **One job per page** in planner grids → maps to CHECKPOINT binary tests

### How to ADHD (video → PDF adaptation)

- **Relatable scenario first, theory later** → Lane 2 before Lane 4.9
- **Humor without condescension** → IF YOU DRIFT copy tone
- **"Body doubling" energy** → DO THIS NOW reads like a friend in the room
- **Explicit permission to skip** → ANCHOR `SKIP IF:`

### Anti-Patterns (What Fails)

| Pattern | Why it fails ADHD readers |
|---------|---------------------------|
| 18-part linear numbering | No exit ramps; working memory overload |
| Theory before first win | Dopamine depletion before payoff |
| Identical page templates | eLearning: boredom triggers attention scatter |
| Gamification / streaks | Hyperfocus + shame spiral |
| Pop-up style sidebars | Attention hijack mid-flow |

---

## Quick Reference Card (Developer)

```
TYPOGRAPHY:  11pt body / 17pt leading / Helvetica / h1 20pt yellow bar
COLORS:      #FAF8F5 page · #1A1A2E text · coral/mint/yellow accents (max 2/page)
LAYOUT:      0.75″ margins · 6.5″ content · ≤3 sentences · box every 150 words
BOXES:       ANCHOR → DO THIS NOW → CHECKPOINT → IF YOU DRIFT
BREAKS:      New lane = PageBreak · printables = own page
ICONS:       Text only: [OK] >> ✓ ⚠ [BRAIN] [TODAY]
COVER:       Full-bleed navy band · 6 bullets · tagline callout · no essay
```

---

## Sources

| Source | Key takeaway used |
|--------|-------------------|
| [NN/g — Chunking](https://www.nngroup.com/articles/chunking/) | Short paragraphs, 50–75 char lines, visual hierarchy, 3–6 item memory chunks |
| [Recite Me — ADHD-friendly fonts](https://reciteme.com/us/news/adhd-friendly-fonts/) | Lexend/Verdana, 1.5× line height, 4.5:1 contrast, 2–3 sentence paragraphs |
| [WCAG 2.2 — 1.4.12 Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html) | Leading 1.5×, paragraph spacing 2×, letter/word spacing floors |
| [Alphero — ADHD-friendly reading design](https://www.alphero.com/intelligence/articles/design-recommendations-for-adhd-friendly-reading-resources) | Connected flow for messages, matte/low glare, natural palette, A4 space |
| [HeyNova — Designing for ADHD](https://heynova.io/en-ca/insights/accessibility-tips/designing-for-people-with-adhd/) | Progress indicators, consistent labels, avoid attention hijacks |
| [eLearning Industry — ADHD-friendly eLearning](https://elearningindustry.com/adhd-friendly-elearning-tips-from-instructional-designer-with-add) | Tidy-not-boring, micro-chunks, progress roadmap, break reminders, praise |
| [ADDitude — ADHD planners](https://www.additudemag.com/slideshows/best-planners-for-adhd-minds/) | Time-boxed sections, checklist formats, external-brain metaphor |
| [BDA Dyslexia Style Guide](https://www.thedyslexia-spldtrust.org.uk/media/downloads/69-bda-style-guide-april14.pdf) | Off-white paper, sans-serif, generous spacing |
| Focus Dock `03-guide-writing-blueprint.md` | Lane architecture, box word budgets, ANCHOR/DO THIS NOW templates |
| Focus Dock `scripts/generate_pdf.py` | Existing palette, ReportLab style baseline |

---

*Spec path:* `/Users/cameron/focus-dock/research/02-adhd-pdf-design-spec.md`