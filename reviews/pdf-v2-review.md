# PDF v2 Agent Review — July 1, 2026

## Summary

| Review | Verdict | Notes |
|--------|---------|-------|
| Writing (`03-guide-writing-blueprint.md`) | **PARTIAL PASS** | 5 lanes, Lane 2 win, banned term removed, theory deferred. Box template not on every section; Lane 3 install still monolithic. |
| Design (`02-adhd-pdf-design-spec.md`) | **PARTIAL PASS** | PAGE_BG, box helpers, lane footers on content pages. Cover is full-bleed thumbnail-style PNG (user request) vs spec wireframe. Heading leading not fully scaled. |

## Writing review — top findings

1. **Lane 3 install** — Single long section; blueprint wants per-beat ANCHOR/CHECKPOINT/DRIFT and formula pointers only (not inline formulas).
2. **Box coverage** — Helpers exist but not every Lane 4 section has ANCHOR + drift (e.g. sequences intro, maintenance).
3. **Lane 4/5 placement** — Fixed: sequence library + week 1–4 moved back into Lane 4 before Reference.
4. **Reference naming** — Partially updated (`TROUBLESHOOTING`, `PROPERTY REFERENCE`); some `PART 12–18` labels remain.
5. **Voice** — PASS: warm, verb-first, setup spiral terminology throughout.

## Design review — top findings

1. **Cover** — Full-page PNG with title on top, high-contrast anchors (YouTube-thumbnail principles). Differs from spec’s navy-band + PAGE_BG split; matches user request.
2. **PAGE_BG + boxes** — PASS on content pages.
3. **Typography** — Body 11/17 PASS; h1–h3 leading below spec 1.5× targets.
4. **Footer** — Lane name in footer PASS; no `LANE X OF 5` progress bar yet.
5. **CHECKPOINT border** — 2pt like other boxes (spec says 1pt).

## Terminology purge

- `plansturbation` removed from: `generate_pdf.py`, site copy, email templates, affiliate assets, SEO keywords.
- Replacements: **setup spiral**, **template graveyard**, **productivity theater**, **anti-rebuild rules**.

## Deliverables

- `assets/focus_dock_cover.png` — full-page cover (regenerate: `python3 scripts/generate_cover.py`)
- `private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide.pdf` — 29 pages, v2 lane structure
- `research/02-adhd-pdf-design-spec.md`, `research/03-guide-writing-blueprint.md`

## Recommended follow-up (post-launch)

1. Split Lane 3 into timed subsections with full box sets; defer formulas to R-1 pointers only.
2. Add ANCHOR to every remaining Lane 1–4 section header.
3. Reorder Lane 5 strictly R-1 → R-16.
4. Tune heading leading to spec scale; optional `LANE N OF 5` footer.