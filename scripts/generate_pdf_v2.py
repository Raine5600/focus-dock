#!/usr/bin/env python3
"""Generate Focus Dock ADHD Notion Recovery Guide PDF — VERSION 2.

Separate from the v1 generator (generate_pdf.py). v2 adds: "Section" naming,
a Contents page with real page numbers (two-pass build), page numbers in the
R-index, per-section intros, purpose lines before action boxes, and up-next
transitions. Cover: scripts/generate_cover_v2.py.

v3 fixes over v2:
- Cover art gets its own page (content no longer overprints it)
- Footers show the correct section per page (section markers resolve at draw time)
- 5-segment section progress bar in every footer
- Callout boxes never split across pages (KeepTogether)
- ANCHOR boxes carry TIME estimates (design spec requirement)
- Reference section numbered R-1..R-16 so in-text pointers actually resolve
- Notion UI instructions updated to the current interface
- Removed stale v1 "Part N" pointers, broken find/replace artifacts, duplicate steps

Cover image: run scripts/generate_cover.py first (assets/focus_dock_cover.png).
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = str(ROOT / "private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide_v2.pdf")
COVER_IMG = str(ROOT / "assets/focus_dock_cover_v2.png")

MARGIN = 0.75 * inch
CONTENT_W = 6.5 * inch
PAGE_W, PAGE_H = letter

# ADHD-friendly palette (research/02-adhd-pdf-design-spec.md)
PAGE_BG = colors.HexColor("#faf8f5")
NAVY = colors.HexColor("#1a1f3d")
CORAL = colors.HexColor("#ff6b4a")
MINT = colors.HexColor("#3dd6c3")
YELLOW = colors.HexColor("#ffd93d")
WHITE = colors.white
LIGHT_BG = colors.HexColor("#f4f6fb")
BOX_MINT = colors.HexColor("#e8faf7")
BOX_YELLOW = colors.HexColor("#fff8e1")
BOX_CORAL = colors.HexColor("#fff0ec")
DARK_TEXT = colors.HexColor("#1a1a2e")
MID_TEXT = colors.HexColor("#3d3d5c")
CHECK_GREEN = colors.HexColor("#2d936c")
WARN_AMBER = colors.HexColor("#e6a800")
FAINT_LINE = colors.HexColor("#d9d4cc")

LANES = [
    "START HERE",
    "5-MINUTE WIN",
    "INSTALL",
    "DAILY USE",
    "REFERENCE",
]


# ---------------------------------------------------------------------------
# Document + per-page section tracking
# ---------------------------------------------------------------------------

class FocusDockDoc(SimpleDocTemplate):
    """Tracks the current section at draw time so footers are always correct."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lane_label = ""
        self.lane_index = 0  # 1-based; 0 = no section yet
        self.toc_pages = {}  # TOC key ("S1".."S5", "R-1".."R-16") -> page number

    def afterFlowable(self, flowable):
        key = getattr(flowable, "_toc_key", None)
        if key:
            self.toc_pages[key] = self.page

    def afterPage(self):
        if self.page == 1:  # cover
            return
        c = self.canv
        c.saveState()

        # rule above footer
        c.setStrokeColor(FAINT_LINE)
        c.setLineWidth(0.6)
        c.line(MARGIN, 0.62 * inch, PAGE_W - MARGIN, 0.62 * inch)

        c.setFont("Helvetica", 8)
        c.setFillColor(MID_TEXT)
        if self.lane_index:
            left = f"FOCUS DOCK  ·  SECTION {self.lane_index} OF 5 — {self.lane_label}"
        else:
            left = "FOCUS DOCK  ·  getfocusdock.com"
        c.drawString(MARGIN, 0.44 * inch, left)
        c.drawRightString(PAGE_W - MARGIN, 0.44 * inch, f"Page {self.page}")

        # 5-segment section progress bar
        if self.lane_index:
            seg_w, seg_h, gap = 16, 3.5, 3
            total = 5 * seg_w + 4 * gap
            x = PAGE_W - MARGIN - 52 - total  # left of the page number
            y = 0.44 * inch - 0.5
            for i in range(5):
                c.setFillColor(MINT if i < self.lane_index else FAINT_LINE)
                c.rect(x + i * (seg_w + gap), y, seg_w, seg_h, fill=1, stroke=0)
        c.restoreState()


class LaneMarker(Flowable):
    """Invisible flowable — updates the doc's section state when drawn."""

    def __init__(self, doc, label, index):
        super().__init__()
        self._doc = doc
        self._label = label
        self._index = index
        self.width = self.height = 0

    def wrap(self, availWidth, availHeight):
        return (0, 0)

    def draw(self):
        self._doc.lane_label = self._label
        self._doc.lane_index = self._index


def draw_cover_page(canvas, doc):
    if Path(COVER_IMG).exists():
        canvas.drawImage(COVER_IMG, 0, 0, width=PAGE_W, height=PAGE_H)
    else:  # fallback so a missing asset never ships a blank cover
        canvas.saveState()
        canvas.setFillColor(NAVY)
        canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
        canvas.setFillColor(WHITE)
        canvas.setFont("Helvetica-Bold", 34)
        canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.58, "FOCUS DOCK")
        canvas.setFillColor(MINT)
        canvas.setFont("Helvetica", 15)
        canvas.drawCentredString(PAGE_W / 2, PAGE_H * 0.52, "The ADHD Notion Recovery Guide")
        canvas.restoreState()


def paint_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------

def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "lane_eyebrow": ParagraphStyle(
            "lane_eyebrow", parent=base["Normal"],
            fontSize=9, leading=12, textColor=MINT,
            fontName="Helvetica-Bold", spaceAfter=2,
        ),
        "lane_title": ParagraphStyle(
            "lane_title", parent=base["Heading1"],
            fontSize=19, leading=24, textColor=WHITE,
            spaceBefore=0, spaceAfter=0, fontName="Helvetica-Bold",
        ),
        "lane_sub": ParagraphStyle(
            "lane_sub", parent=base["Normal"],
            fontSize=10, leading=14, textColor=colors.HexColor("#c9cee6"),
            fontName="Helvetica",
        ),
        "h2": ParagraphStyle(
            "h2", parent=base["Heading2"],
            fontSize=15, leading=22, textColor=NAVY,
            spaceBefore=4, spaceAfter=4, fontName="Helvetica-Bold",
        ),
        "ref_h2": ParagraphStyle(
            "ref_h2", parent=base["Heading2"],
            fontSize=13, leading=19, textColor=NAVY,
            spaceBefore=0, spaceAfter=0, fontName="Helvetica-Bold",
        ),
        "ref_chip": ParagraphStyle(
            "ref_chip", parent=base["Normal"],
            fontSize=10, leading=14, textColor=WHITE,
            alignment=TA_CENTER, fontName="Helvetica-Bold",
        ),
        "h3": ParagraphStyle(
            "h3", parent=base["Heading3"],
            fontSize=12, leading=18, textColor=CORAL,
            spaceBefore=10, spaceAfter=5, fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body", parent=base["Normal"],
            fontSize=11, leading=17, textColor=DARK_TEXT,
            spaceAfter=10, fontName="Helvetica",
        ),
        "callout_label": ParagraphStyle(
            "callout_label", parent=base["Normal"],
            fontSize=9, leading=13, textColor=DARK_TEXT,
            fontName="Helvetica-Bold",
        ),
        "callout_body": ParagraphStyle(
            "callout_body", parent=base["Normal"],
            fontSize=11, leading=17, textColor=DARK_TEXT,
            fontName="Helvetica",
        ),
        "callout": ParagraphStyle(
            "callout", parent=base["Normal"],
            fontSize=11, leading=17, textColor=NAVY,
            spaceBefore=2, spaceAfter=2, fontName="Helvetica-Bold",
        ),
        "step": ParagraphStyle(
            "step", parent=base["Normal"],
            fontSize=11, leading=16, textColor=DARK_TEXT,
            leftIndent=18, spaceAfter=5, fontName="Helvetica",
        ),
        "formula": ParagraphStyle(
            "formula", parent=base["Code"],
            fontSize=9, leading=13, textColor=WHITE,
            backColor=NAVY, borderPadding=8, fontName="Courier",
            spaceBefore=2, spaceAfter=10,
        ),
        "toc": ParagraphStyle(
            "toc", parent=base["Normal"],
            fontSize=10.5, leading=15, textColor=DARK_TEXT,
            spaceAfter=0, fontName="Helvetica",
        ),
        "table_cell": ParagraphStyle(
            "table_cell", parent=base["Normal"],
            fontSize=9, leading=12.5, textColor=DARK_TEXT,
            fontName="Helvetica",
        ),
        "table_header": ParagraphStyle(
            "table_header", parent=base["Normal"],
            fontSize=9, leading=13, textColor=WHITE,
            fontName="Helvetica-Bold",
        ),
        "card_title": ParagraphStyle(
            "card_title", parent=base["Normal"],
            fontSize=10.5, leading=14, textColor=NAVY,
            alignment=TA_CENTER, fontName="Helvetica-Bold",
        ),
        "card_body": ParagraphStyle(
            "card_body", parent=base["Normal"],
            fontSize=9, leading=13, textColor=MID_TEXT,
            alignment=TA_CENTER, fontName="Helvetica",
        ),
    }
    return styles


# ---------------------------------------------------------------------------
# Building blocks
# ---------------------------------------------------------------------------

def _callout_table(label, body_html, styles, border_color, bg_color, label_color,
                   border_width=1.4):
    label_para = Paragraph(
        f'<font color="{label_color.hexval()}"><b>{label}</b></font>',
        styles["callout_label"],
    )
    body_para = Paragraph(body_html, styles["callout_body"])
    t = Table([[label_para], [body_para]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), border_width, border_color),
        ("ROUNDEDCORNERS", [5, 5, 5, 5]),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 9),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 1),
        ("TOPPADDING", (0, 1), (-1, 1), 3),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 11),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def lane_banner(index, title, subtitle, styles):
    """Full-width navy section header with eyebrow label + progress context."""
    eyebrow = Paragraph(f"SECTION {index} OF 5", styles["lane_eyebrow"])
    title_p = Paragraph(title, styles["lane_title"])
    rows = [[eyebrow], [title_p]]
    if subtitle:
        rows.append([Paragraph(subtitle, styles["lane_sub"])])
    t = Table(rows, colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 3, CORAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, 0), 12),
        ("TOPPADDING", (0, 1), (-1, -1), 1),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -2), 1),
    ]))
    return t


def inline_callout(text, styles):
    return _callout_table(">>", text, styles, CORAL, LIGHT_BG, NAVY, border_width=1)


def anchor_box(you_are_here, time_est, win, styles, skip_if=None):
    lines = [
        f"<b>YOU ARE HERE:</b> {you_are_here}",
        f"<b>TIME:</b> {time_est}",
        f"<b>WIN:</b> {win}",
    ]
    if skip_if:
        lines.append(f"<b>SKIP IF:</b> {skip_if}")
    return _callout_table("ANCHOR", "<br/>".join(lines), styles, CORAL, BOX_CORAL, CORAL)


def do_this_now(steps, styles):
    items = "".join(f"{i + 1}. {s}<br/>" for i, s in enumerate(steps))
    return _callout_table("DO THIS NOW", items, styles, MINT, BOX_MINT, NAVY)


def checkpoint(lines, stuck_pointer, styles):
    body = "<br/>".join(
        f'<font color="{CHECK_GREEN.hexval()}">✓</font> {l}' for l in lines
    )
    body += f"<br/><b>Stuck?</b> → {stuck_pointer}"
    return _callout_table("CHECKPOINT", body, styles, NAVY, LIGHT_BG, CHECK_GREEN,
                          border_width=1)


def if_you_drift(signal, recovery, fallback, styles):
    body = (
        f"Noticed yourself {signal}?<br/>"
        f"→ {recovery}<br/>"
        f"→ Still in this section? Skip to <b>{fallback}</b>."
    )
    # "!" token, not "⚠" — base-14 Helvetica has no U+26A0 and renders a tofu box
    return _callout_table("! IF YOU DRIFT", body, styles, WARN_AMBER, BOX_YELLOW,
                          WARN_AMBER)


def ref_heading(num, title, styles):
    """R-number chip + title for Reference section sections."""
    chip = Paragraph(num, styles["ref_chip"])
    title_p = Paragraph(title, styles["ref_h2"])
    t = Table([[chip, title_p]], colWidths=[0.55 * inch, CONTENT_W - 0.55 * inch])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, 0), NAVY),
        ("ROUNDEDCORNERS", [4, 4, 4, 4]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 4),
        ("RIGHTPADDING", (0, 0), (0, 0), 4),
        ("TOPPADDING", (0, 0), (0, 0), 4),
        ("BOTTOMPADDING", (0, 0), (0, 0), 4),
        ("LEFTPADDING", (1, 0), (1, 0), 10),
        ("TOPPADDING", (1, 0), (1, 0), 0),
        ("BOTTOMPADDING", (1, 0), (1, 0), 0),
    ]))
    return t


def begin_lane(story, styles, doc, index, title, subtitle="", intro=None):
    story.append(PageBreak())
    story.append(LaneMarker(doc, title, index))
    banner = lane_banner(index, title, subtitle, styles)
    banner._toc_key = f"S{index}"
    story.append(banner)
    story.append(Spacer(1, 16))
    if intro:
        story.append(Paragraph(intro, styles["body"]))
        story.append(Spacer(1, 6))


def data_table(styles, header_row, rows, col_widths):
    table_rows = [[Paragraph(f"<b>{h}</b>", styles["table_header"]) for h in header_row]]
    for row in rows:
        table_rows.append([Paragraph(c, styles["table_cell"]) for c in row])
    t = Table(table_rows, colWidths=col_widths, repeatRows=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b8b2c9")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ("RIGHTPADDING", (0, 0), (-1, -1), 7),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))
    return t


def emit_blocks(story, styles, blocks, wrap_boxes=True):
    # wrap_boxes=False when the caller nests these into its own KeepTogether —
    # nested KeepTogethers make ReportLab force a page break before the group.
    wrap = KeepTogether if wrap_boxes else (lambda f: f)
    for kind, text in blocks:
        if kind == "break":
            story.append(PageBreak())
        elif kind == "anchor":
            story.append(wrap(anchor_box(**text, styles=styles)))
            story.append(Spacer(1, 8))
        elif kind == "do_now":
            story.append(wrap(do_this_now(text, styles)))
            story.append(Spacer(1, 8))
        elif kind == "checkpoint":
            story.append(wrap(checkpoint(**text, styles=styles)))
            story.append(Spacer(1, 8))
        elif kind == "drift":
            story.append(wrap(if_you_drift(**text, styles=styles)))
            story.append(Spacer(1, 8))
        elif kind == "h2":
            story.append(Paragraph(text, styles["h2"]))
        elif kind == "h3":
            story.append(Paragraph(text, styles["h3"]))
        elif kind == "callout":
            story.append(wrap(inline_callout(text, styles)))
            story.append(Spacer(1, 8))
        elif kind == "formula":
            story.append(Paragraph(text.replace("\n", "<br/>"), styles["formula"]))
        elif kind == "step":
            story.append(Paragraph(text, styles["step"]))
        elif kind == "spacer":
            story.append(Spacer(1, float(text)))
        elif kind == "table":
            story.append(text)
            story.append(Spacer(1, 8))
        else:
            story.append(Paragraph(text, styles["body"]))


def _heading_flowables(styles, title, ref_num=None):
    if ref_num:
        return [
            ref_heading(ref_num, title, styles),
            HRFlowable(width="100%", thickness=0.6, color=FAINT_LINE,
                       spaceBefore=6, spaceAfter=10),
        ]
    return [
        Paragraph(title, styles["h2"]),
        HRFlowable(width="22%", thickness=2, color=CORAL,
                   spaceBefore=1, spaceAfter=11, hAlign="LEFT"),
    ]


def section(story, styles, title, blocks, page_break_after=False, ref_num=None):
    story.append(Spacer(1, 12))
    head = _heading_flowables(styles, title, ref_num)

    # Keep the heading glued to the first content block so headers never orphan.
    first, rest = blocks[0] if blocks else (None, None), blocks[1:]
    lead = []
    emit_blocks(lead, styles, [first] if first[0] else [], wrap_boxes=False)
    # Tag the heading itself: KeepTogether dissolves into its children before
    # afterFlowable fires, so a tag on the wrapper would never register.
    if ref_num:
        head[0]._toc_key = ref_num
    story.append(KeepTogether(head + lead))
    emit_blocks(story, styles, rest)
    story.append(Spacer(1, 4))
    if page_break_after:
        story.append(PageBreak())


# ---------------------------------------------------------------------------
# Section 1 — Start here
# ---------------------------------------------------------------------------

def build_lane1(story, styles, doc):
    story.append(LaneMarker(doc, LANES[0], 1))
    banner = lane_banner(1, "START HERE",
                         "Two pages. Then you pick a section and go.", styles)
    banner._toc_key = "S1"
    story.append(banner)
    story.append(Spacer(1, 16))
    story.append(anchor_box(
        "Section 1 → Reading map",
        "1 min",
        "You know which section to enter and when to stop reading.",
        styles,
        skip_if="You already finished the install — jump to Section 4.",
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "<b>Don't read this cover to cover.</b> Pick a section. Stop when you hit a checkpoint.",
        styles["body"],
    ))
    story.append(data_table(
        styles,
        ["If you…", "Go to", "Timer"],
        [
            ["Need proof this is for you", "Section 1 → Self-check", "1 min"],
            ["Want a win RIGHT NOW", "Section 2 — 5-Minute Win", "5 min"],
            ["Are ready to build", "Section 3 — Install", "one sitting"],
            ["Already installed", "Section 4 — Daily Use", "3 min"],
            ["Something broke / are drowning", "Section 4 → Emergency, or Section 5 → R-6", "4 min"],
            ["Are looking something up", "Section 5 — Reference (R-1 to R-16)", "skim"],
        ],
        [2.5 * inch, 2.9 * inch, 1.1 * inch],
    ))
    story.append(Spacer(1, 12))
    story.append(inline_callout(
        "<b>Default path:</b> Self-check → 5-Minute Win → Install → "
        "one visible task → close Notion.",
        styles,
    ))
    story.append(Spacer(1, 8))
    story.append(KeepTogether(do_this_now([
        "Pick your section from the table above.",
        "Open only that section.",
        "Close the PDF when you hit its checkpoint.",
    ], styles)))

    # --- Self-check ---
    story.append(PageBreak())
    story.append(anchor_box(
        "Section 1 → Self-check",
        "30 sec",
        "You know if Focus Dock is for you.",
        styles,
    ))
    story.append(Spacer(1, 8))
    emit_blocks(story, styles, [
        ("h2", "You need this guide if…"),
        ("step", "[ ] You've abandoned 2+ Notion templates in the past year"),
        ("step", "[ ] You've spent 3+ hours setting up before doing one real task"),
        ("step", "[ ] You have habit trackers with broken streaks you avoid looking at"),
        ("step", "[ ] 'Do laundry' or 'email boss' has sat on your list for 5+ days"),
        ("step", "[ ] You feel productive while customizing but not while working"),
        ("h2", "Skip this guide if…"),
        ("step", "[ ] You already use Notion daily without thinking about it"),
        ("step", "[ ] You enjoy building systems as a hobby (separate from productivity)"),
        ("step", "[ ] You have a coach or assistant who manages your task list"),
    ])
    story.append(checkpoint(
        ["3+ checks in 'need this'? → Section 2",
         "0–2 checks? This guide may not be your bottleneck"],
        "Section 5 → R-13 FAQ",
        styles,
    ))
    story.append(if_you_drift(
        "reading the FAQ before doing anything",
        "Section 2 first. The FAQ is R-13. Win before walls of text.",
        "Section 2 — 5-Minute Win",
        styles,
    ))

    # --- Preview (heading + diagram kept together so neither orphans) ---
    story.append(Spacer(1, 12))
    story.append(KeepTogether(
        _heading_flowables(styles, "What you'll build (preview only)") + [
            Paragraph("Three databases and one home screen. That's the whole system.",
                      styles["body"]),
            _system_map(styles),
        ]
    ))
    story.append(Spacer(1, 10))
    story.append(KeepTogether(do_this_now(
        ["Do NOT build yet. Finish Section 2 first.", "Open Section 2 when ready."], styles)))
    story.append(Spacer(1, 8))
    story.append(KeepTogether(inline_callout(
        "<b>Up next → Section 2, The 5-Minute Win.</b> One real task, done on paper, "
        "before you touch Notion.", styles)))


def _system_map(styles):
    """Visual card row: 3 databases feeding the home screen."""
    cards = [
        ("[BRAIN] BRAIN DUMP", "2-second capture.<br/>No tags. No guilt."),
        ("[TODAY] TODAY", "ONE visible next task.<br/>Sequences hide the rest."),
        ("[PROJECTS] PROJECTS", "Parking lot for someday.<br/>Visited weekly, not daily."),
    ]
    card_w = (CONTENT_W - 0.3 * inch) / 3
    row = []
    for title, body in cards:
        inner = Table(
            [[Paragraph(title, styles["card_title"])],
             [Paragraph(body, styles["card_body"])]],
            colWidths=[card_w],
        )
        inner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), WHITE),
            ("BOX", (0, 0), (-1, -1), 1.2, MINT),
            ("ROUNDEDCORNERS", [5, 5, 5, 5]),
            ("TOPPADDING", (0, 0), (-1, 0), 8),
            ("BOTTOMPADDING", (0, -1), (-1, -1), 8),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]))
        row.append(inner)

    home = Table(
        [[Paragraph("[HOME] FOCUS DOCK — one page: next task + brain dump + weekly projects toggle",
                    styles["card_title"])]],
        colWidths=[CONTENT_W],
    )
    home.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BOX_CORAL),
        ("BOX", (0, 0), (-1, -1), 1.2, CORAL),
        ("ROUNDEDCORNERS", [5, 5, 5, 5]),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))

    arrow = ParagraphStyle("arrow", fontName="Helvetica-Bold", fontSize=11,
                           textColor=MID_TEXT, alignment=TA_CENTER)
    outer = Table(
        [row,
         [Paragraph("↓", arrow), Paragraph("↓", arrow), Paragraph("↓", arrow)],
         ],
        colWidths=[card_w + 0.1 * inch] * 3,
    )
    outer.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 1), (-1, 1), 2),
        ("BOTTOMPADDING", (0, 1), (-1, 1), 2),
    ]))
    wrapper = Table([[outer], [home]], colWidths=[CONTENT_W])
    wrapper.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return wrapper


# ---------------------------------------------------------------------------
# Section 2 — 5-minute win
# ---------------------------------------------------------------------------

def build_lane2(story, styles, doc):
    begin_lane(story, styles, doc, 2, "THE 5-MINUTE WIN",
               "One real task done before you touch Notion. Proof first.",
               intro="Before you build anything, you'll finish one real task — on "
                     "paper. It takes about five minutes and proves the method works "
                     "before you spend a whole sitting installing it. If it feels too "
                     "easy, good. Easy is the point.")
    section(story, styles, "The one-task rule", [
        ("anchor", {"you_are_here": "Section 2 → One-task rule", "time_est": "1 min",
                    "win": "You picked one avoided task.", "skip_if": None}),
        ("body", "Twelve databases = twelve decisions before breakfast. Your brain is already tired."),
        ("body", "We're cutting that to <b>one visible task</b>. Notion comes later. Task completion comes now."),
        ("do_now", [
            "Name one task you've avoided for 3+ days.",
            "Write it on paper — not in Notion.",
            "Say it out loud once.",
        ]),
    ])
    section(story, styles, "Shrink it small", [
        ("anchor", {"you_are_here": "Section 2 → Shrink task", "time_est": "1 min",
                    "win": "Your task is small enough to start.", "skip_if": None}),
        ("body", "<b>Laundry</b> → put 3 items in the hamper.<br/>"
                 "<b>Email boss</b> → open a draft.<br/>"
                 "<b>Clean kitchen</b> → put 3 dishes in the sink."),
        ("do_now", ["Rewrite YOUR task as the smallest version.",
                    "If it still feels too big, shrink it again."]),
        ("checkpoint", {"lines": ["Could you do the shrunk version right now?"],
                        "stuck_pointer": "Shrink again — smaller is better"}),
    ])
    section(story, styles, "Do it on paper (no Notion yet)", [
        ("anchor", {"you_are_here": "Section 2 → Do the task", "time_est": "2–3 min",
                    "win": "One real task finished.", "skip_if": None}),
        ("do_now", [
            "Put your phone in another room.",
            "Do the shrunk task now.",
            "Mark a check on the paper when done.",
        ]),
        ("checkpoint", {"lines": ["Task done — or you tried and stopped"],
                        "stuck_pointer": "Section 4 → Emergency"}),
        ("drift", {"signal": "customizing your phone's notes app",
                   "recovery": "Defaults are fine. A sticky note works.",
                   "fallback": "the tiny task on paper"}),
    ])
    section(story, styles, "Bridge to install", [
        ("callout", "<b>You just did the hard part.</b> Starting beats any dashboard. "
                    "Notion only holds the task — you already proved you can finish one."),
        ("body", "When you're ready: Section 3 — Install. Same one-task energy, one sitting."),
        ("do_now", ["Block 45–60 quiet minutes for the install.",
                    "Phone in another room. Open Notion only."]),
        ("callout", "<b>Up next → Section 3, The Install.</b> Five steps, one sitting, "
                    "everything spelled out."),
    ])


# ---------------------------------------------------------------------------
# Section 3 — Install
# ---------------------------------------------------------------------------

def build_lane3(story, styles, doc):
    begin_lane(story, styles, doc, 3, "THE INSTALL",
               "One sitting, about 45–60 minutes. Five steps. Zero philosophy.",
               intro="This section walks the whole build, start to finish, in five "
                     "steps. Each step says exactly what to click, roughly how long it "
                     "takes, and how to check that it worked. Follow the boxes in "
                     "order and you can't get lost — every step also names its rescue "
                     "page in the Reference section.")
    section(story, styles, "Before you start", [
        ("anchor", {"you_are_here": "Section 3 → Before you start", "time_est": "2 min",
                    "win": "You know the rules before building.",
                    "skip_if": "Already installed → Section 4"}),
        ("body", "This is not a template to admire. It is a <b>recovery protocol</b>. "
                 "Theory waits until Section 4."),
        ("h2", "What you need"),
        ("step", "• A Notion account (the free plan works)"),
        ("step", "• One uninterrupted sitting — phone in another room"),
        ("step", "• Permission to quarantine your template graveyard"),
        ("callout", "RULE ZERO: Urge to add a 4th database? <b>Setup spiral.</b> "
                    "Close Notion. Do one real task."),
        ("drift", {"signal": "watching Notion tutorial videos",
                   "recovery": "Close YouTube. Open R-2 (UI Map). Find the button.",
                   "fallback": "Step 1 — Quarantine the graveyard"}),
    ])

    section(story, styles, "Step 1 — Quarantine the graveyard", [
        ("anchor", {"you_are_here": "Section 3 → Step 1 of 5", "time_est": "~5 min",
                    "win": "Old templates out of sight, not deleted.", "skip_if": None}),
        ("body", "Why this comes first: while the old dashboards sit one click away, "
                 "your attention keeps leaking back into them. Quarantine isn't "
                 "tidying — it's removing the relapse trigger."),
        ("do_now", [
            "Open the Notion sidebar. Count your productivity-related pages.",
            "If more than 5: create a page titled <b>[GRAVEYARD] Template Graveyard</b>.",
            "Drag every abandoned dashboard, habit tracker, and PARA clone into it. Do not open them.",
            "Collapse the graveyard page.",
        ]),
        ("body", "You are not deleting anything — you're quarantining shame. "
                 "Everything stays retrievable."),
        ("checkpoint", {"lines": ["Sidebar shows 5 or fewer productivity pages"],
                        "stuck_pointer": "R-10 Migration Checklist"}),
        ("drift", {"signal": "opening old dashboards 'one last time'",
                   "recovery": "Don't open. Drag away. Curiosity is a trap.",
                   "fallback": "Step 2 — Brain Dump"}),
    ])

    section(story, styles, "Step 2 — Build [BRAIN] Brain Dump", [
        ("anchor", {"you_are_here": "Section 3 → Step 2 of 5", "time_est": "~10 min",
                    "win": "A 2-second capture inbox exists.", "skip_if": None}),
        ("body", "Brain Dump exists so stray thoughts have somewhere to go that isn't "
                 "your head — and isn't your task list. It stays deliberately bare: "
                 "three properties means capture takes two seconds and organizing is "
                 "impossible."),
        ("do_now", [
            "New page → type <b>/database</b> → choose <b>Database — Full page</b>. Name it <b>[BRAIN] Brain Dump</b>.",
            "Rename the default title property to <b>Thought</b>.",
            "Add property: <b>Captured</b> (Created time — fills itself).",
            "Add property: <b>Processed?</b> (Checkbox).",
            "Delete every other property. Yes, all of them.",
            "Create a view named <b>Inbox</b>: filter <b>Processed? is unchecked</b>, sort <b>Captured ascending</b>.",
        ]),
        ("callout", "Usage rule: capture in 2 seconds. Thought only. No tags. "
                    "Process during the Sunday reset or when Today is empty."),
        ("checkpoint", {"lines": ["Add a test thought — it appears in Inbox",
                                  "Delete the test thought"],
                        "stuck_pointer": "R-2 Notion UI Quick Map"}),
        ("drift", {"signal": "adding tags, categories, or priority properties",
                   "recovery": "Brain Dump has 3 properties. That's the feature.",
                   "fallback": "Step 3 — Today"}),
    ], page_break_after=True)

    section(story, styles, "Step 3 — Build [TODAY] Today + sequences", [
        ("anchor", {"you_are_here": "Section 3 → Step 3 of 5", "time_est": "~15 min",
                    "win": "One visible next task, powered by sequence logic.",
                    "skip_if": None}),
        ("body", "This is the heart of the system and the longest step. You'll add "
                 "plain properties first, then two roll-ups, then two formulas, then "
                 "one view — in that order, because each piece depends on the one "
                 "before it."),
        ("do_now", [
            "New page → <b>/database</b> → <b>Database — Full page</b>. Name it <b>[TODAY] Today</b>.",
            "Keep the title property. Rename it <b>Task</b>.",
            "Add <b>Done</b> (Checkbox), <b>Due</b> (Date), and <b>Energy</b> "
            "(Select with options: <b>[HIGH] High / [MED] Medium / [LOW] Low</b>).",
        ]),
        ("h3", "The sequence relation"),
        ("step", "1. Add property → <b>Relation</b> → pick this same <b>Today</b> database."),
        ("step", "2. Turn ON <b>Separate directions</b> (this creates a paired property)."),
        ("step", "3. Name the first direction <b>Task Before</b> and the paired one <b>Task After</b>."),
        ("h3", "Two roll-ups (create these before the formulas)"),
        ("step", "• <b>Before Done</b> — Rollup: relation <b>Task Before</b> → property <b>Done</b> → Calculate: <b>Checked</b> (count of checked)."),
        ("step", "• <b>Before Due</b> — Rollup: relation <b>Task Before</b> → property <b>Due</b> → Calculate: <b>Latest date</b>."),
        ("h3", "Two formulas (copy from this page)"),
        ("body", "Add a <b>Formula</b> property named <b>Hide Sequence</b>. Paste:"),
        ("formula", 'if(empty(prop("Task Before")), false, '
                    'if(prop("Before Done") > 0, false, '
                    'if(prop("Due") < prop("Before Due"), false, true)))'),
        ("body", "Add a second <b>Formula</b> property named <b>Hide</b>. Paste:"),
        ("formula", 'prop("Hide Sequence")'),
        ("body", "Full formula breakdown + troubleshooting live in <b>R-1</b>. "
                 "You don't need to understand them now."),
        ("h3", "The Do This Next view"),
        ("step", "1. Create a view named <b>Do This Next</b>."),
        ("step", "2. Filters: <b>Hide is unchecked</b> AND <b>Done is unchecked</b>."),
        ("step", "3. Sort: <b>Due ascending</b>."),
        ("callout", "This view is your entire daily driver. One task visible. "
                    "Everything else is hidden by sequence logic."),
        ("checkpoint", {"lines": ["Add test task 'Put 3 dishes in sink' — it shows in Do This Next"],
                        "stuck_pointer": "R-1 Formulas / R-6 Troubleshooting"}),
        ("drift", {"signal": "trying gallery views and card previews",
                   "recovery": "Aesthetic trap. A plain table works. Defaults until Day 8.",
                   "fallback": "Step 4 — Projects"}),
    ], page_break_after=True)

    section(story, styles, "Step 4 — Build [PROJECTS] Projects", [
        ("anchor", {"you_are_here": "Section 3 → Step 4 of 5", "time_est": "~5 min",
                    "win": "A parking lot for someday — out of your daily view.",
                    "skip_if": None}),
        ("body", "Projects is where 'someday' lives so it stops haunting your daily "
                 "view. You'll only open it during the Sunday reset."),
        ("do_now", [
            "New page → <b>/database</b> → <b>Database — Full page</b>. Name it <b>[PROJECTS] Projects</b>.",
            "Properties: <b>Name</b> (Title), <b>Status</b> (Select: [IDEA] Idea / [ACTIVE] Active / [PAUSED] Paused / [DONE] Done), <b>Next Action</b> (Text).",
            "Create a view named <b>Active</b>: filter <b>Status = Active</b>. Drag what matters to the top.",
        ]),
        ("body", "You do NOT work from this database daily. During the Sunday reset, "
                 "pick one Next Action and move it to Today."),
        ("checkpoint", {"lines": ["Projects exists with exactly 3 properties"],
                        "stuck_pointer": "R-3 Property Reference"}),
    ])

    section(story, styles, "Step 5 — Build the [HOME] home screen", [
        ("anchor", {"you_are_here": "Section 3 → Step 5 of 5", "time_est": "~10 min",
                    "win": "Open Notion → see one task. No sidebar maze.",
                    "skip_if": None}),
        ("body", "This page is what makes the system feel effortless: open Notion, "
                 "see one task, do it. No sidebar spelunking."),
        ("do_now", [
            "New page: <b>[HOME] Focus Dock</b>.",
            "Add a heading: <b>Right now:</b>",
            "Type <b>/linked</b> → link the <b>Do This Next</b> view from Today (embedded view, not the full database).",
            "Add a heading: <b>Brain dump (2 sec):</b> → /linked → the Brain Dump <b>Inbox</b> view.",
            "Add a toggle: <b>Projects (Sunday only)</b> → put the linked <b>Active</b> view inside it.",
            "Drag <b>[HOME] Focus Dock</b> to the top of your sidebar, and in Settings set Notion to open on the top page in your sidebar (search Settings for 'Open on start').",
        ]),
        ("checkpoint", {"lines": ["Opening Notion lands on [HOME] Focus Dock",
                                  "Exactly one task is visible under 'Right now'"],
                        "stuck_pointer": "R-2 Notion UI Quick Map"}),
        ("drift", {"signal": "reorganizing your whole sidebar",
                   "recovery": "Only [HOME] matters. The rest can stay messy.",
                   "fallback": "Finish the install (next box)"}),
    ])

    section(story, styles, "Finish — do one real task", [
        ("do_now", [
            "Add one real task to Today — something you've actually avoided.",
            "Do it now, before closing this guide.",
            "Mark it Done. Close Notion.",
        ]),
        ("callout", "Done. You installed a working system AND completed a real task in one sitting. "
                    "That's more than any template ever gave you."),
    ], page_break_after=True)

    story.extend(build_install_checklist(styles))


# ---------------------------------------------------------------------------
# Section 4 — Daily use
# ---------------------------------------------------------------------------

def build_lane4(story, styles, doc):
    begin_lane(story, styles, doc, 4, "DAILY USE",
               "Life after install: the 3-minute rhythm, sequences, resets, recovery.",
               intro="The system is built. This section is how you live with it: the "
                     "3-minute daily rhythm, what to do when a big task freezes you, "
                     "the short weekly reset, and how to recover on the loud days.")
    section(story, styles, "Daily workflow", [
        ("anchor", {"you_are_here": "Section 4 → Daily workflow", "time_est": "3 min/day",
                    "win": "You know the morning/evening rhythm.", "skip_if": None}),
        ("body", "The whole day runs on one loop: open, do the one visible task, "
                 "capture anything that pops up, close. Here's what that looks like "
                 "at each point of the day."),
        ("h2", "Morning"),
        ("step", "1. Open [HOME] Focus Dock."),
        ("step", "2. Read the one task in Do This Next."),
        ("step", "3. Do it before opening email, Slack, or TikTok."),
        ("h2", "During the day"),
        ("step", "• Intrusive thought? → Brain Dump. One line. Close."),
        ("step", "• Finished a task? → Check Done. The next sequence step appears automatically."),
        ("h2", "Evening"),
        ("step", "• If Today is empty: pull ONE task from Brain Dump or Projects."),
        ("step", "• Do NOT rebuild your dashboard. Do NOT add properties. Go to bed."),
        ("callout", "If you did nothing else today but open Focus Dock once and complete "
                    "one task: <b>system success.</b>"),
        ("checkpoint", {"lines": ["You can describe the daily flow from memory"],
                        "stuck_pointer": "R-4 When to Use What"}),
    ])

    section(story, styles, "Task sequences — when big tasks freeze you", [
        ("anchor", {"you_are_here": "Section 4 → Sequences", "time_est": "5 min to learn",
                    "win": "Big tasks become one small visible step.", "skip_if": None}),
        ("body", "Big tasks are lying to you. 'Do laundry' is 8 tasks. 'Make a video' is 14. "
                 "When all 8 show at once, your brain files them under 'not now.'"),
        ("h2", "How sequences work"),
        ("body", "Link tasks with the Task Before / Task After relation. The Hide Sequence "
                 "formula hides step 2 until step 1 is done. You only ever see the next "
                 "physical action."),
        ("h3", "Example: Laundry (6 steps)"),
        ("step", "1. Collect dirty clothes → 2. Check gym bag → 3. Start washer → "
                 "4. Move to dryer → 5. Fold → 6. Put away — each linked with Task Before to the previous one"),
        ("h3", "Example: Email boss (4 steps)"),
        ("step", "1. Open last week's draft → 2. Write 3 bullet points only → 3. Read it aloud once → 4. Hit send"),
        ("h3", "Example: Grocery run (6 steps)"),
        ("step", "1. Check fridge → 2. Write a 5-item list max → 3. Grab bags → 4. Drive/walk → "
                 "5. Buy only list items → 6. Unload 3 items"),
        ("h3", "Example: Taxes (one sitting)"),
        ("step", "1. Find login → 2. Download one form → 3. Fill name/address → "
                 "4. One deduction section → 5. Save draft → 6. Schedule a finish date"),
        ("callout", "Rule: break steps down until the next one feels 'too small to fail.' "
                    "If you still can't start, break it again."),
        ("drift", {"signal": "building a 14-step video sequence",
                   "recovery": "Max 6 steps today. Break more later.",
                   "fallback": "the Laundry example above"}),
    ])

    section(story, styles, "Task sequence library", [
        ("anchor", {"you_are_here": "Section 4 → Sequence library", "time_est": "pick one: 5 min",
                    "win": "One pre-built sequence copied into Today.", "skip_if": None}),
        ("body", "Copy these into the Today database. Link each step to the previous one "
                 "with Task Before. Rename steps to fit your life."),
        ("table", _sequence_library_table(styles)),
        ("callout", "Pre-build sequences on a good day. Reuse them forever. This is where "
                    "your dopamine investment goes — not color palettes."),
        ("do_now", ["Pick ONE sequence on a good day.",
                    "Copy it into Today with Task Before links."]),
    ])

    section(story, styles, "Sunday reset", [
        ("anchor", {"you_are_here": "Section 4 → Sunday reset", "time_est": "~10 min, hard stop at 15",
                    "win": "Week prepped without a guilt dashboard.", "skip_if": None}),
        ("body", "No guilt weekly review. No streak accounting. Three quick passes, then stop."),
        ("h2", "Pass 1 — Brain Dump triage (~4 min)"),
        ("step", "• Open Inbox. For each item: delete it, move it to Today, or write it into a Projects Next Action."),
        ("step", "• Check Processed? on handled items."),
        ("h2", "Pass 2 — Today prep (~4 min)"),
        ("step", "• Clear Done tasks (archive or delete — your choice)."),
        ("step", "• Keep 3–5 tasks max for the week, sequenced where needed."),
        ("step", "• Pick Monday's first task. Set Due = Monday."),
        ("h2", "Pass 3 — Projects glance (~2 min)"),
        ("step", "• Open Active projects. Max 3 Active at once — pause the rest."),
        ("step", "• Update one Next Action per active project."),
        ("callout", "At 15 minutes, stop even if unfinished. Consistency beats completeness."),
        ("checkpoint", {"lines": ["Reset done (or stopped at the hard stop)"],
                        "stuck_pointer": "R-7 printable checklist"}),
        ("drift", {"signal": "the reset stretching past 15 minutes",
                   "recovery": "Stop here. An incomplete reset beats a skipped one.",
                   "fallback": "R-7 printable checklist"}),
    ])

    section(story, styles, "Emergency overwhelm protocol", [
        ("anchor", {"you_are_here": "Section 4 → Emergency", "time_est": "4 min",
                    "win": "You survived overwhelm with one tiny action.", "skip_if": None}),
        ("body", "For days when everything feels loud. A printable version is <b>R-8</b> — "
                 "print it and tape it to your monitor."),
        ("callout", "OVERWHELM MODE — do only these 4 steps:"),
        ("step", "1. <b>Box breathing:</b> 4 seconds in, 4 hold, 4 out. Twice."),
        ("step", "2. <b>Brain dump 3 words</b> — not sentences. What's loudest?"),
        ("step", "3. <b>Shrink to the smallest version:</b> 'clean kitchen' → 'put 3 dishes in the sink.'"),
        ("step", "4. <b>Do the smallest version.</b> Mark done. Stop. You survived."),
        ("body", "Do NOT: reorganize Notion, watch setup videos, download a new template, "
                 "or redesign colors. That is the trap."),
        ("h2", "When to skip Notion entirely"),
        ("body", "If you haven't opened Focus Dock in 5+ days: use a sticky note for one task. "
                 "Return to Notion only when the sticky note works 2 days straight."),
    ])

    story.extend(build_days_2_7_playbook(styles))

    section(story, styles, "Week 1–4 rollout", [
        ("anchor", {"you_are_here": "Section 4 → Week rollout", "time_est": "2 min",
                    "win": "You know what each week adds.", "skip_if": None}),
        ("h2", "Week 1: Survival mode"),
        ("step", "• Day 1: install only. No customization."),
        ("step", "• Days 2–7: one task per day minimum. Brain dump only when a thought intrudes."),
        ("step", "• Banned: adding properties, new views, watching Notion tutorials."),
        ("h2", "Week 2: Add sequences"),
        ("step", "• Pick your most-delayed task. Break it into a sequence."),
        ("step", "• Add a 2nd sequence only after the first one works 3 times."),
        ("h2", "Week 3: Sunday reset habit"),
        ("step", "• First full Sunday reset. Stop at 15 minutes even if messy."),
        ("step", "• If you skip it: no catch-up. Next Sunday, fresh start."),
        ("h2", "Week 4: Evaluate"),
        ("body", "Ask: am I opening Focus Dock without dread? If yes: success. "
                 "If no: delete one more feature — the system is still too complex."),
        ("callout", "The 3-week test: systems that survive 21 days become automatic. "
                    "You're building automatic."),
    ])

    section(story, styles, "Maintenance — anti-rebuild rules", [
        ("anchor", {"you_are_here": "Section 4 → Maintenance", "time_est": "2 min",
                    "win": "You know what you may change, and when.", "skip_if": None}),
        ("h2", "Allowed changes (after Day 8)"),
        ("step", "• Adjust the Energy labels"),
        ("step", "• Add ONE filter to Do This Next"),
        ("step", "• Change the homepage label"),
        ("h2", "Banned until Day 30"),
        ("step", "• Habit trackers"),
        ("step", "• Mood logs"),
        ("step", "• PARA / Second Brain migrations"),
        ("step", "• New databases"),
        ("step", "• Aesthetic overhauls"),
        ("callout", "If you're still using Focus Dock daily without thinking about it — "
                    "you succeeded. If not, the system is still too complex. "
                    "Delete one more thing."),
        ("drift", {"signal": "thinking 'just one new view'",
                   "recovery": "Customization trap. Defaults until Day 8.",
                   "fallback": "R-5 Setup Spiral Red Flags"}),
    ])

    section(story, styles, "Why your old system failed (optional)", [
        ("anchor", {"you_are_here": "Section 4 → Context", "time_est": "3 min",
                    "win": "You understand why templates failed — without shame.",
                    "skip_if": "Read when curious, not before installing."}),
        ("body", "You are not lazy. Your old system was designed to produce screenshots, "
                 "not completed tasks."),
        ("h2", "1. Dopamine spent on setup"),
        ("body", "Customizing Notion releases dopamine. By Saturday night the dopamine "
                 "budget is empty — and no task got done."),
        ("h2", "2. Choice overload"),
        ("body", "Typical ADHD templates ship 6+ databases. Every time you open one, "
                 "you make a dozen micro-decisions before starting anything."),
        ("h2", "3. Streak shame"),
        ("body", "Miss one habit day → broken streak → you close the tab and never come back."),
        ("callout", "The Focus Dock fix: low setup cost, low decision density, and no "
                    "visible state that punishes missed days."),
    ])

    section(story, styles, "Accountability without shame", [
        ("anchor", {"you_are_here": "Section 4 → Accountability", "time_est": "3 min",
                    "win": "External structure without streak mechanics.", "skip_if": None}),
        ("body", "ADHD brains respond to external structure, not internal guilt. "
                 "Use these — no streak counters attached."),
        ("h2", "Body doubling"),
        ("step", "• Video call or in-person: both of you work silently on one task."),
        ("step", "• No progress reports required — presence is the cue."),
        ("h2", "Text ping (not a streak)"),
        ("step", "• One message: 'Opened Focus Dock. Doing [task].'"),
        ("step", "• No reply needed. No daily obligation. Skip days without explanation."),
        ("h2", "Environmental cues"),
        ("step", "• Notion opens on [HOME] Focus Dock (not the sidebar)."),
        ("step", "• Phone: a Notion widget or bookmark straight to Brain Dump."),
        ("step", "• Desk: the R-8 emergency card taped at eye level."),
        ("h2", "What to avoid"),
        ("step", "• Habit-streak apps tied to Focus Dock usage."),
        ("step", "• Public accountability threads where missed days = shame."),
        ("step", "• Reward systems that require perfect weeks."),
        ("callout", "One completed task beats seven days of dashboard tweaking. "
                    "Measure completion, not opens."),
        ("callout", "<b>Up next → Section 5, Reference.</b> Numbered R-1 to R-16 — "
                    "your lookup for when anything breaks."),
    ])


def _sequence_library_table(styles):
    seqs = [
        ("CLEAN KITCHEN", "1. Put 3 dishes in sink · 2. Fill sink with soapy water · 3. Scrub · "
                          "4. Rinse · 5. Load dishwasher · 6. Wipe counter · 7. Take out trash · 8. Sweep"),
        ("EMAIL BOSS", "1. Open draft · 2. Write 3 bullets only · 3. Read aloud · 4. Fix typos · 5. Send"),
        ("CHANGE SHEETS", "1. Strip pillowcases · 2. Strip sheets · 3. Hamper · 4. New fitted sheet · "
                          "5. New flat sheet · 6. Pillowcases on"),
        ("YOUTUBE VIDEO", "1. Pick topic · 2. Outline 5 bullets · 3. Write script · 4. Set up camera · "
                          "5. Record · 6. Transfer files · 7. Rough cut · 8. Thumbnail · 9. Upload · 10. Description + tags"),
        ("REFILL RX", "1. Check bottle date · 2. Call pharmacy · 3. Confirm insurance · 4. Wait for ready text · "
                      "5. Drive/walk · 6. Pick up · 7. Weekly organizer"),
        ("ROOM RESCUE", "1. Trash bag in hand · 2. Pick up 5 items · 3. Put away 3 items · "
                        "4. Clear one surface · 5. Stop (done)"),
        ("GROCERIES", "1. Check fridge · 2. 5-item list max · 3. Grab bags · 4. Drive/walk · "
                      "5. Buy only list items · 6. Unload 3 items"),
        ("SHOWER RESET", "1. Get towel · 2. Get clean clothes · 3. Start water · 4. Shower · "
                         "5. Dry off · 6. Dress · 7. Hang towel"),
        ("TAXES", "1. Find login · 2. Download one form · 3. Name/address · 4. One deduction section · "
                  "5. Save draft · 6. Schedule finish date"),
        ("CALL MOM", "1. Write 2 topics · 2. Find quiet spot · 3. Dial · 4. Talk briefly · 5. Set next call date"),
        ("WORKOUT", "1. Put on shoes · 2. Fill water · 3. Short warmup · 4. Main exercise · 5. Cooldown · 6. Shower"),
    ]
    return data_table(
        styles,
        ["Sequence", "Steps (link each with Task Before)"],
        [(f"<b>{n}</b>", s) for n, s in seqs],
        [1.25 * inch, 5.25 * inch],
    )


# ---------------------------------------------------------------------------
# Section 5 — Reference (R-1 .. R-16)
# ---------------------------------------------------------------------------

def build_lane5(story, styles, doc, toc_pages):
    begin_lane(story, styles, doc, 5, "REFERENCE",
               "Skimmable lookup. Numbered R-1 to R-16 — jump straight to what you need.",
               intro="Nothing here is meant to be read in order. When something "
                     "breaks — or you forget a detail — find the R-number in the "
                     "index below and jump straight to it.")

    # Section 5 opener: quick card + index
    section(story, styles, "Quick reference card", [
        ("body", "<b>Capture:</b> Brain Dump → type the thought → close (2 sec)<br/>"
                 "<b>Work:</b> [HOME] Focus Dock → Do This Next → one task<br/>"
                 "<b>Sequence:</b> Task Before relation + Hide Sequence formula<br/>"
                 "<b>Weekly:</b> Sunday reset (~10 min, hard stop at 15)<br/>"
                 "<b>Emergency:</b> smallest-step shrink → do it → stop<br/>"
                 "<b>Homepage:</b> [HOME] Focus Dock — never the sidebar maze"),
    ])
    section(story, styles, "Find it fast", [
        ("table", _find_it_fast_table(styles, toc_pages)),
    ], page_break_after=True)

    section(story, styles, "Formulas — copy-paste", [
        ("body", "Create these as <b>Formula</b> properties in the [TODAY] Today database. "
                 "Names must match exactly — the view filters depend on them."),
        ("h2", "Hide Sequence"),
        ("body", "Property name: <b>Hide Sequence</b> · Type: Formula"),
        ("formula", 'if(empty(prop("Task Before")), false, '
                    'if(prop("Before Done") > 0, false, '
                    'if(prop("Due") < prop("Before Due"), false, true)))'),
        ("body", "<b>What it does:</b> hides a sequenced task while its predecessor is "
                 "unfinished. Tasks with no Task Before always show."),
        ("h2", "Hide"),
        ("body", "Property name: <b>Hide</b> · Type: Formula"),
        ("formula", 'prop("Hide Sequence")'),
        ("body", "<b>What it does:</b> pass-through used by the Do This Next view filter "
                 "(Hide is unchecked). Filter on Hide, not on Hide Sequence directly."),
        ("h2", "Required roll-ups (create before the formulas)"),
        ("step", "• <b>Before Done</b> — Rollup: relation Task Before → property Done → Calculate: Checked (count of checked)"),
        ("step", "• <b>Before Due</b> — Rollup: relation Task Before → property Due → Calculate: Latest date"),
        ("h2", "Do This Next view"),
        ("step", "• Filter: Hide is unchecked"),
        ("step", "• Filter: Done is unchecked"),
        ("step", "• Sort: Due ascending"),
        ("callout", "If too many tasks show: verify the Hide Sequence formula exists and "
                    "the view filters on <b>Hide</b>, not Hide Sequence."),
    ], ref_num="R-1", page_break_after=True)

    section(story, styles, "Notion UI quick map", [
        ("body", "Lookup while installing. Use this table instead of tutorial videos. "
                 "(Notion moves menus occasionally — when in doubt, use the search box inside Settings.)"),
        ("table", data_table(styles, ["Task", "Where in Notion"], [
            ["Create a database", "New page → type <b>/database</b> → <b>Database — Full page</b>"],
            ["Add a property", "Open database → <b>+</b> at the right of the header row → pick type"],
            ["Formula property", "Add property → Formula → paste from <b>R-1</b>"],
            ["Relation (sequences)", "Add property → Relation → pick the same database → turn ON "
                                     "<b>Separate directions</b> → name both directions"],
            ["Rollup", "Add property → Rollup → pick relation → pick target property → pick calculation"],
            ["Filter a view", "Click the view name → Filter → add rule (Hide unchecked, Done unchecked)"],
            ["Embed a linked view", "On the [HOME] page → <b>/linked</b> → pick database → pick the view"],
            ["Open Notion on [HOME]", "Drag [HOME] to the top of the sidebar → Settings → search "
                                      "<b>'Open on start'</b> → Top page in sidebar"],
        ], [1.6 * inch, 4.9 * inch])),
    ], ref_num="R-2")

    section(story, styles, "Property reference card", [
        ("h2", "Brain Dump database (3 properties)"),
        ("body", "• <b>Thought</b> (Title) — the capture<br/>"
                 "• <b>Captured</b> (Created time)<br/>"
                 "• <b>Processed?</b> (Checkbox)"),
        ("h2", "Today database (10 properties)"),
        ("body", "• <b>Task</b> (Title)<br/>• <b>Done</b> (Checkbox)<br/>• <b>Due</b> (Date)<br/>"
                 "• <b>Energy</b> (Select: High / Medium / Low)<br/>"
                 "• <b>Task Before</b> (Relation → Today, separate directions)<br/>"
                 "• <b>Task After</b> (Relation → Today, the paired direction)<br/>"
                 "• <b>Before Done</b> (Rollup: count of checked Done)<br/>"
                 "• <b>Before Due</b> (Rollup: latest Due date)<br/>"
                 "• <b>Hide Sequence</b> (Formula — see R-1)<br/>"
                 "• <b>Hide</b> (Formula — see R-1)"),
        ("h2", "Projects database (3 properties)"),
        ("body", "• <b>Name</b> (Title)<br/>"
                 "• <b>Status</b> (Select: Idea / Active / Paused / Done)<br/>"
                 "• <b>Next Action</b> (Text)"),
        ("h2", "Do This Next view"),
        ("body", "Filter 1: Hide is unchecked · Filter 2: Done is unchecked · Sort: Due ascending"),
    ], ref_num="R-3")

    section(story, styles, "When to use what — decision table", [
        ("body", "If you're unsure where something goes, use this table. A wrong choice "
                 "is fixable during the Sunday reset."),
        ("table", data_table(styles, ["Situation", "Use this", "Keep it to"], [
            ["Random thought while working", "[BRAIN] Brain Dump — one line, close", "2 seconds"],
            ["What should I do right now?", "[HOME] Focus Dock — Do This Next view", "90 seconds"],
            ["Big project with many steps", "[TODAY] Today — break into a sequence", "6 steps max"],
            ["Someday idea, not this week", "[PROJECTS] Projects — Idea status", "Sunday reset only"],
            ["Overwhelmed, can't start", "R-8 emergency card — 2-minute shrink", "the smallest step"],
            ["Sunday weekly prep", "R-7 reset checklist", "~10 min, stop at 15"],
            ["Urge to add a 4th database", "Close Notion. Do one real task.", "now"],
        ], [2.0 * inch, 2.9 * inch, 1.6 * inch])),
    ], ref_num="R-4")

    section(story, styles, "Setup spiral red flags", [
        ("body", "Catch these urges early. Each one feels productive. None of them "
                 "completes a task."),
        ("table", data_table(styles, ["Red flag", "What to do instead"], [
            ["New database idea", "You 'just need' a Reading List or Habits database. "
                                  "Use Brain Dump or Projects instead."],
            ["Color/icon session", "30+ minutes on aesthetics, zero tasks completed. Close Notion."],
            ["Tutorial spiral", "Watching 'ultimate Notion setup' videos during install week. "
                                "Banned until Day 30."],
            ["Filter rabbit hole", "Adding a 4th filter to Do This Next. Max one optional filter, "
                                   "and only after Day 8."],
            ["Migration fantasy", "Planning to merge your old PARA system into Focus Dock. "
                                  "Quarantine the old system instead."],
            ["Weekly review creep", "The Sunday reset running past 15 minutes. Hard stop — "
                                    "good enough beats perfect."],
            ["Streak mechanic", "Adding a habit tracker to prove you're consistent. "
                                "Streaks become shame monuments."],
            ["Property sprawl", "New properties: Priority, Context, Effort, Mood. "
                                "Today has enough. Stop."],
        ], [1.5 * inch, 5.0 * inch])),
        ("callout", "Ask: 'Will this help me see ONE next task tomorrow?' If no, don't do it."),
    ], ref_num="R-5")

    section(story, styles, "Troubleshooting", [
        ("h2", "I keep customizing instead of doing"),
        ("body", "Set a build budget: zero customizing on weekdays. Changes happen during "
                 "the Sunday reset only — and count toward its 15-minute stop."),
        ("h2", "Too many tasks are visible"),
        ("body", "Check that the Hide formula exists and Do This Next filters on "
                 "<b>Hide is unchecked</b> (see R-1)."),
        ("h2", "Sequences aren't hiding"),
        ("body", "Confirm Task Before is a relation with separate directions, and the "
                 "Before Done rollup counts <i>checked</i> boxes. Verify each Task Before "
                 "link points to the correct prior step."),
        ("h2", "Do This Next is empty but I have tasks"),
        ("body", "Uncheck Done on active tasks and confirm Due dates exist. In a sequence, "
                 "make sure step 1 has no Task Before link — otherwise everything hides."),
        ("h2", "I skipped Brain Dump and my head is loud again"),
        ("body", "Intrusive thoughts hijack focus. The 2-second capture prevents the "
                 "'I'll remember it' lie. Capture, close, keep working."),
        ("h2", "The Brain Dump inbox never empties"),
        ("body", "Normal. The inbox is capture, not completion. Process it during the "
                 "Sunday reset only — never mid-week."),
        ("h2", "I abandoned it for a week"),
        ("body", "No guilt dashboard exists here. Delete done tasks, pull ONE item from "
                 "Brain Dump, continue. Streaks don't exist in Focus Dock."),
        ("h2", "The Sunday reset keeps running long"),
        ("body", "Hard stop at 15 minutes. An incomplete reset beats a skipped one."),
        ("h2", "I want more structure"),
        ("body", "Read that again. Wanting more structure is often productivity theater "
                 "wearing a productivity costume. Stay at 3 databases for 30 days first. "
                 "Already added a 4th? Delete it today — and don't migrate its relations."),
    ], ref_num="R-6", page_break_after=True)

    section(story, styles, "Sunday reset checklist (printable)", [
        ("body", "Print this page. Check the boxes with a pen during your Sunday reset. "
                 "Stop at 15 minutes, done or not."),
        ("step", "[ ] Open [BRAIN] Brain Dump Inbox — triage each item (delete / Today / Projects)"),
        ("step", "[ ] Mark Processed? on handled Brain Dump items"),
        ("step", "[ ] Archive or delete completed Today tasks"),
        ("step", "[ ] Today has 3–5 tasks max for the coming week"),
        ("step", "[ ] Monday's first task has Due = Monday"),
        ("step", "[ ] Max 3 [PROJECTS] Active — pause the rest"),
        ("step", "[ ] Each Active project has one written Next Action"),
        ("step", "[ ] Did NOT add properties, views, or databases"),
        ("step", "[ ] Stopped at 15 minutes (even if unfinished)"),
        ("callout", "An incomplete reset beats a skipped reset. Same time next Sunday — "
                    "no catch-up guilt."),
    ], ref_num="R-7", page_break_after=True)

    story.extend(build_emergency_card(styles))

    section(story, styles, "What to delete from old templates", [
        ("body", "When quarantining your Template Graveyard, these features stay banned "
                 "in Focus Dock:"),
        ("h2", "Delete or ignore permanently"),
        ("step", "• Habit streak counters"),
        ("step", "• Mood trackers (unless prescribed by your therapist)"),
        ("step", "• Eisenhower matrices"),
        ("step", "• PARA 'Areas' and 'Resources' databases"),
        ("step", "• Weekly review dashboards with 20+ checkboxes"),
        ("step", "• Journal prompts you never read"),
        ("step", "• Finance dashboards (your bank's app does this better)"),
        ("h2", "Why each one fails ADHD brains"),
        ("body", "<b>Streaks:</b> one miss = a shame monument.<br/>"
                 "<b>PARA:</b> 'Is this a Project or an Area?' = decision paralysis.<br/>"
                 "<b>Weekly reviews:</b> 45 minutes of facing failure.<br/>"
                 "<b>Mood logs:</b> evidence you're 'inconsistent.'"),
        ("callout", "If a feature requires daily maintenance to avoid looking broken, delete it."),
    ], ref_num="R-9")

    section(story, styles, "Migration checklist (from old templates)", [
        ("body", "Do not migrate relations or dashboards. Quarantine and cherry-pick. "
                 "Keep it short."),
        ("step", "[ ] Create the [GRAVEYARD] Template Graveyard page"),
        ("step", "[ ] Drag old dashboards, habit trackers, and PARA clones into it"),
        ("step", "[ ] Collapse the graveyard — do not open old pages during install week"),
        ("step", "[ ] Copy max 3 open loops into [BRAIN] Brain Dump (one line each)"),
        ("step", "[ ] Copy max 1 Next Action per real project into [PROJECTS] Projects"),
        ("step", "[ ] Do NOT import CSVs with 200 old tasks"),
        ("step", "[ ] Do NOT recreate Eisenhower matrices, mood logs, or streak views"),
        ("step", "[ ] Set [HOME] Focus Dock as your start page before deleting bookmarks to old dashboards"),
        ("h2", "What to salvage vs leave behind"),
        ("body", "<b>Salvage:</b> open tasks, project names, one-line next actions.<br/>"
                 "<b>Leave:</b> relations, rollups, aesthetic layouts, archived 'someday' "
                 "lists, broken streaks."),
        ("callout", "A fresh start beats a perfect migration. The old system is quarantined, "
                    "not deleted — you can retrieve things later if you truly need them."),
    ], ref_num="R-10")

    section(story, styles, "Brain dump — processing guide", [
        ("body", "Brain Dump is capture-only during the week. Processing happens in the "
                 "Sunday reset or when Today is empty."),
        ("h2", "The 10-second triage (per item)"),
        ("step", "1. <b>Delete</b> — noise, duplicates, 'someday' ideas you'll never do"),
        ("step", "2. <b>Today</b> — one physical action you could do this week"),
        ("step", "3. <b>Projects</b> — multi-step outcomes; write the Next Action text only"),
        ("h2", "What NOT to do during triage"),
        ("step", "• Do not tag, categorize, or assign priority"),
        ("step", "• Do not create sub-pages or linked databases"),
        ("step", "• Do not keep triaging past your reset's 15-minute stop"),
        ("h2", "When to capture (2 seconds)"),
        ("step", "• Intrusive thought during focused work"),
        ("step", "• 'I'll remember this' lie detected"),
        ("step", "• Someone asks you to do something while you're busy"),
        ("callout", "Capture is not commitment. Processing is not urgent. "
                    "Today is the only daily driver."),
    ], ref_num="R-11")

    section(story, styles, "Energy matching (optional)", [
        ("body", "Only use Energy tags if they help. If choosing a level causes paralysis, "
                 "ignore the property entirely — it's optional by design."),
        ("h2", "[HIGH] High energy"),
        ("body", "Creative work, hard conversations, complex sequences, starting new projects."),
        ("h2", "[MED] Medium energy"),
        ("body", "Email, errands, admin, routine chores, continuing in-progress work."),
        ("h2", "[LOW] Low energy"),
        ("body", "Brain dump triage, tiny tasks, reading one paragraph, putting one item away."),
        ("callout", "On low days: filter Do This Next by Low energy — or skip the filter "
                    "and just do the smallest visible task."),
    ], ref_num="R-12")

    section(story, styles, "FAQ", [
        ("h2", "Can I use this alongside medication?"),
        ("body", "Yes. Focus Dock is organizational, not medical. Keep your treatment plan."),
        ("h2", "What about mobile?"),
        ("body", "Notion mobile works. Favorite [HOME] Focus Dock, and add a Notion widget "
                 "for 2-second Brain Dump captures."),
        ("h2", "Can I share it with my partner?"),
        ("body", "The license covers one person. Your partner needs their own copy for "
                 "their own workspace."),
        ("h2", "Should I use Notion AI with this?"),
        ("body", "Skip it for now. AI features add decisions. Master the 3-database core first."),
        ("h2", "Can I migrate from Ultimate Brain / PARA?"),
        ("body", "Don't migrate. Quarantine the old system (R-10). A fresh start prevents "
                 "relation nightmares."),
        ("h2", "What if I need more than 3 databases eventually?"),
        ("body", "After 30 successful days, add ONE database. Not before. Prove the "
                 "minimum works first."),
    ], ref_num="R-13")

    section(story, styles, "Glossary", [
        ("body", "<b>Setup spiral:</b> tweaking your system instead of doing the task the "
                 "system was for."),
        ("body", "<b>Template graveyard:</b> the collection of abandoned Notion setups you "
                 "avoid opening."),
        ("body", "<b>Productivity theater:</b> looks productive. Zero tasks finished."),
        ("body", "<b>Task sequence:</b> linked sub-tasks where only the next step is visible."),
        ("body", "<b>Brain dump:</b> frictionless capture inbox — no organization required."),
        ("body", "<b>Choice overload:</b> too many options → paralysis → no action."),
        ("body", "<b>Executive dysfunction:</b> knowing what to do but being unable to "
                 "start it in the moment."),
        ("body", "<b>Visible state:</b> dashboard elements that look broken when you skip a day."),
    ], ref_num="R-14")

    section(story, styles, "Research notes", [
        ("body", "Focus Dock's design is informed by:"),
        ("step", "• Iyengar &amp; Lepper (2000) — more choices reduce action (choice overload)"),
        ("step", "• Volkow et al. (2009) — ADHD dopamine-pathway differences"),
        ("step", "• Barkley (2012) — executive function as a performance problem, not a knowledge problem"),
        ("step", "• Tuckman — externalize executive function into the environment"),
        ("step", "• Lived experience: setup-spiral threads across r/Notion and r/ADHD"),
        ("body", "This guide externalizes 'what's next' so your brain doesn't have to hold it."),
    ], ref_num="R-15")

    # R-16 — closing note, kept together as one unit so it never straddles pages
    closing = _heading_flowables(styles, "You made it", ref_num="R-16")
    closing[0]._toc_key = "R-16"
    emit_blocks(closing, styles, [
        ("body", "If you're reading this, you built something most ADHD adults never "
                 "finish: a system they actually use."),
        ("body", "Focus Dock isn't about perfect Notion. It's about <b>one visible next "
                 "step</b> when your brain feels like static."),
        ("callout", "The whole system fits on a sticky note: <b>Check → Win → Install → "
                    "one task → close Notion.</b> Repeat tomorrow."),
        ("body", "Questions? hello@getfocusdock.com · 14-day refund if it doesn't "
                 "help — no guilt, same as the system."),
        ("body", "Now close this PDF and do the one task."),
    ], wrap_boxes=False)
    story.append(Spacer(1, 12))
    story.append(KeepTogether(closing))


R_INDEX = [
    ("R-1", "Formulas — copy-paste"),
    ("R-2", "Notion UI quick map"),
    ("R-3", "Property reference card"),
    ("R-4", "When to use what"),
    ("R-5", "Setup spiral red flags"),
    ("R-6", "Troubleshooting"),
    ("R-7", "Sunday reset checklist (print)"),
    ("R-8", "Emergency card (print)"),
    ("R-9", "What to delete from old templates"),
    ("R-10", "Migration checklist"),
    ("R-11", "Brain dump processing"),
    ("R-12", "Energy matching (optional)"),
    ("R-13", "FAQ"),
    ("R-14", "Glossary"),
    ("R-15", "Research notes"),
    ("R-16", "You made it"),
]


def _find_it_fast_table(styles, toc_pages):
    """Two-column R-index with page numbers (filled on the second build pass)."""
    rows = []
    for i in range(8):
        left = R_INDEX[i]
        right = R_INDEX[i + 8]
        rows.append([
            left[0], f"{left[1]}  ·  p. {toc_pages.get(left[0], '—')}",
            right[0], f"{right[1]}  ·  p. {toc_pages.get(right[0], '—')}",
        ])
    return data_table(styles, ["#", "Section", "#", "Section"], rows,
                      [0.5 * inch, 2.75 * inch, 0.5 * inch, 2.75 * inch])


def build_contents(styles, toc_pages):
    """Contents page (page 2) — real page numbers land on the second pass."""
    story = []
    head = Table([[Paragraph("CONTENTS", styles["lane_title"])]], colWidths=[CONTENT_W])
    head.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LINEBELOW", (0, -1), (-1, -1), 3, CORAL),
        ("LEFTPADDING", (0, 0), (-1, -1), 16),
        ("RIGHTPADDING", (0, 0), (-1, -1), 16),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    story.append(head)
    story.append(Spacer(1, 16))
    story.append(Paragraph(
        "Five sections. Do Sections 1–4 in order, at your own pace. Keep Section 5 "
        "for looking things up. Page numbers below so you can jump straight in.",
        styles["body"],
    ))
    story.append(Spacer(1, 4))

    def pg(key):
        return str(toc_pages.get(key, "—"))

    story.append(data_table(
        styles,
        ["§", "Section", "What's in it", "Page"],
        [
            ["1", "<b>Start Here</b>", "Pick your path + a 30-second self-check", pg("S1")],
            ["2", "<b>The 5-Minute Win</b>", "One real task done before you touch Notion", pg("S2")],
            ["3", "<b>The Install</b>", "Build the 3-database system in one sitting — 5 steps", pg("S3")],
            ["4", "<b>Daily Use</b>", "The daily rhythm, task sequences, Sunday reset, recovery", pg("S4")],
            ["5", "<b>Reference</b>", "R-1 to R-16 lookup: formulas, fixes, printables, FAQ", pg("S5")],
        ],
        [0.4 * inch, 1.55 * inch, 3.55 * inch, 0.6 * inch],
    ))
    story.append(Spacer(1, 14))
    story.append(Paragraph(
        f"<b>Worth bookmarking:</b> copy-paste formulas (R-1, p. {pg('R-1')}) · "
        f"troubleshooting (R-6, p. {pg('R-6')}) · "
        f"printable emergency card (R-8, p. {pg('R-8')}).",
        styles["body"],
    ))
    story.append(Spacer(1, 10))
    story.append(Paragraph(
        "Sections 1–4 are things you <b>do</b>, in order, at your own pace. "
        "Section 5 is a reference you <b>look things up in</b> later. The whole guide "
        "is built from the same four boxes, so you always know what you're looking at:",
        styles["body"],
    ))
    for token, meaning in [
        ('<font color="#ff6b4a"><b>ANCHOR</b></font>',
         'where you are, how long it takes, and what "done" looks like'),
        ('<font color="#1a9c8c"><b>DO THIS NOW</b></font>',
         "the exact actions, numbered — nothing extra"),
        ('<font color="#1a1f3d"><b>CHECKPOINT</b></font>',
         "a quick test that proves it worked before you move on"),
        ('<font color="#e6a800"><b>! IF YOU DRIFT</b></font>',
         "the way back when attention wanders — no shame"),
    ]:
        story.append(Paragraph(f"• {token} — {meaning}", styles["step"]))
    story.append(Spacer(1, 10))
    story.append(inline_callout(
        "<b>Don't read cover to cover.</b> Pick a section. Stop at its checkpoint.",
        styles,
    ))
    story.append(PageBreak())
    return story


def build_emergency_card(styles):
    """R-8 — printable emergency card, framed for cutting out."""
    story = []
    story.append(Spacer(1, 12))
    r8_head = ref_heading("R-8", "Emergency card (printable)", styles)
    r8_head._toc_key = "R-8"
    story.append(r8_head)
    story.append(HRFlowable(width="100%", thickness=0.6, color=FAINT_LINE,
                            spaceBefore=6, spaceAfter=10))
    story.append(Paragraph(
        "Print this page. Cut along the dashes. Tape the card to your monitor.",
        styles["body"],
    ))
    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_TEXT,
                            dash=(4, 4), spaceAfter=0))

    label = ParagraphStyle("em_label", fontName="Helvetica-Bold", fontSize=13,
                           leading=18, textColor=CORAL, alignment=TA_CENTER)
    step = ParagraphStyle("em_step", fontName="Helvetica-Bold", fontSize=11.5,
                          leading=20, textColor=DARK_TEXT)
    small = ParagraphStyle("em_small", fontName="Helvetica", fontSize=9.5,
                           leading=14, textColor=MID_TEXT)
    card = Table([
        [Paragraph("OVERWHELM MODE", label)],
        [Paragraph("1. Box breathe: 4 in · 4 hold · 4 out — twice", step)],
        [Paragraph("2. Brain dump 3 WORDS (not sentences)", step)],
        [Paragraph("3. Shrink the task to its SMALLEST version", step)],
        [Paragraph("4. Do it. Mark done. STOP.", step)],
        [Paragraph("<b>DO NOT:</b> open Notion settings · download templates · "
                   "reorganize · watch setup videos", small)],
        [Paragraph("<b>AWAY 5+ DAYS?</b> Sticky note with ONE task. "
                   "Return when the sticky works 2 days straight.", small)],
        [Paragraph("You are not behind. You are not broken. One task is enough.", small)],
    ], colWidths=[CONTENT_W])
    card.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), WHITE),
        ("BOX", (0, 0), (-1, -1), 2, CORAL),
        ("ROUNDEDCORNERS", [8, 8, 8, 8]),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("RIGHTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, 0), 14),
        ("TOPPADDING", (0, 1), (-1, -1), 4),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 14),
        ("ALIGN", (0, 0), (0, 0), "CENTER"),
    ]))
    story.append(Spacer(1, 10))
    story.append(KeepTogether(card))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1, color=MID_TEXT,
                            dash=(4, 4), spaceAfter=0))
    story.append(PageBreak())
    return story


# ---------------------------------------------------------------------------
# Dense tables (install checklist, days 2–7)
# ---------------------------------------------------------------------------

INSTALL_STEPS = [
    ("1", "Phone in another room. Open Notion on desktop or in a browser only."),
    ("2", "Sidebar audit: count productivity pages. If 5+, create the [GRAVEYARD] Template Graveyard page."),
    ("3", "Drag abandoned dashboards into the graveyard. Do NOT open them. Collapse the graveyard."),
    ("4", "Create a new page: [BRAIN] Brain Dump. Type /database → Database — Full page."),
    ("5", "Rename the title property to Thought. Delete all other default properties."),
    ("6", "Add Captured (Created time). Add Processed? (Checkbox)."),
    ("7", "Create the Inbox view. Filter: Processed? unchecked. Sort: Captured ascending."),
    ("8", "Test capture: add 'test thought'. Confirm it appears in Inbox. Delete the test."),
    ("9", "Create the page [TODAY] Today. /database → Database — Full page."),
    ("10", "Add Task (title), Done (checkbox), Due (date), Energy (select)."),
    ("11", "Energy options: [HIGH] High, [MED] Medium, [LOW] Low."),
    ("12", "Add a relation to Today itself. Turn ON Separate directions."),
    ("13", "Name the directions Task Before and Task After."),
    ("14", "Add the Before Done rollup: Task Before → Done → Calculate: Checked."),
    ("15", "Add the Before Due rollup: Task Before → Due → Calculate: Latest date."),
    ("16", "Add the Hide Sequence formula property (copy from R-1)."),
    ("17", "Add the Hide formula: prop(\"Hide Sequence\")."),
    ("18", "Create the Do This Next view. Filters: Hide unchecked, Done unchecked."),
    ("19", "Sort Do This Next by Due ascending. This is your daily driver."),
    ("20", "Add a test task 'Put 3 dishes in sink'. Confirm it shows in Do This Next."),
    ("21", "Create the page [PROJECTS] Projects. /database → Database — Full page."),
    ("22", "Add Name, Status (Idea/Active/Paused/Done), Next Action (text)."),
    ("23", "Create the Active view: Status = Active. Manual sort enabled."),
    ("24", "Add one project with Next Action text only. Do not add tasks here."),
    ("25", "Create the page [HOME] Focus Dock. This becomes your home base."),
    ("26", "Add heading: Right now. Embed the linked Do This Next view from Today."),
    ("27", "Add heading: Brain dump. Embed the linked Inbox view from Brain Dump."),
    ("28", "Add toggle: Projects (Sunday only). Embed the Active view inside it."),
    ("29", "Drag [HOME] Focus Dock to the top of the sidebar. In Settings, set 'Open on start' to top page in sidebar."),
    ("30", "Close every other Notion tab. Only Focus Dock remains."),
    ("31", "Add your first real task to Today. Not a test — something you've avoided."),
    ("32", "If the task is big: stop. Break it into a 3-step sequence with Task Before links."),
    ("33", "Verify only step 1 is visible in Do This Next. Steps 2–3 hidden."),
    ("34", "Move up to 3 items from old notes into Brain Dump, if any. Max 3."),
    ("35", "Review Projects: max 1 Active for week one. Pause the others."),
    ("36", "Delete any extra views you created during setup. Keep only the essentials."),
    ("37", "Do NOT change colors, icons, or covers. Aesthetic trap — defaults are fine."),
    ("38", "Read the R-8 emergency card once. Bookmark it mentally."),
    ("39", "Screenshot your Focus Dock home — a private before/after record. Don't post it."),
    ("40", "Write on paper: 'One task is enough.' Tape it near your desk."),
    ("41", "Calendar: add a recurring Sunday reset reminder."),
    ("42", "Do the one visible task NOW, before closing this guide."),
    ("43", "Mark it Done. Watch the next sequence step appear (if it has one)."),
    ("44", "If nothing appears next: pull one item from Brain Dump into Today."),
    ("45", "Close Notion. Do not reopen it until tomorrow morning."),
    ("46", "One sentence on paper: what made starting hard today?"),
    ("47", "Save this PDF somewhere findable. Name it: Focus Dock Recovery."),
    ("48", "You recovered. The graveyard can wait."),
]


def build_install_checklist(styles):
    story = []
    half = 24
    section(story, styles, "Install checklist (1 of 2)", [
        ("body", "Steps 1–24: quarantine, Brain Dump, and Today. Follow in order during "
                 "your first install. If a step takes longer than expected, keep going — "
                 "do not add unlisted features."),
        ("callout", "Stuck? Skip aesthetics. Defaults are fine. Good enough beats perfect."),
        ("table", data_table(styles, ["Step", "Action"],
                             [(f"<b>{n}</b>", s) for n, s in INSTALL_STEPS[:half]],
                             [0.55 * inch, 5.95 * inch])),
    ], page_break_after=True)

    section(story, styles, "Install checklist (2 of 2)", [
        ("body", "Steps 25–48: Projects, home screen, and the first real task."),
        ("table", data_table(styles, ["Step", "Action"],
                             [(f"<b>{n}</b>", s) for n, s in INSTALL_STEPS[half:]],
                             [0.55 * inch, 5.95 * inch])),
        ("callout", "Done when: one task visible in Do This Next, one task marked Done, "
                    "Notion closed."),
        ("callout", "<b>Up next → Section 4, Daily Use.</b> The 3-minute rhythm that "
                    "keeps this system alive."),
    ], page_break_after=True)
    return story


def build_days_2_7_playbook(styles):
    story = []
    days = [
        ("Day 2", "Open [HOME] Focus Dock only. Complete one task. No new properties. "
                  "Brain dump max 2 captures."),
        ("Day 3", "Same as Day 2. If the task feels big, split it into a 3-step sequence. "
                  "Do not add a 4th database."),
        ("Day 4", "If Do This Next is empty, pull one item from Brain Dump into Today. "
                  "Still one visible task."),
        ("Day 5", "Midweek check: count your open Notion tabs. Target = 1 (Focus Dock). "
                  "Close the rest."),
        ("Day 6", "Optional: add one pre-built sequence from the Sequence Library (Section 4). "
                  "Max one new sequence this week."),
        ("Day 7", "First Sunday reset (~10 min, stop at 15). Stop even if it's messy."),
    ]
    section(story, styles, "Days 2–7 playbook", [
        ("body", "Install day is Day 1. Days 2–7 are survival mode — no rebuilding, "
                 "no tutorials, no new views."),
        ("table", data_table(styles, ["Day", "Your only job"],
                             [(f"<b>{d}</b>", j) for d, j in days],
                             [0.75 * inch, 5.75 * inch])),
        ("callout", "Success metric: you opened Focus Dock and finished one task. "
                    "Total Notion time under 10 minutes a day."),
    ])
    return story


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def build_story(styles, doc, toc_pages):
    story = []
    # Page 1 is the cover art only — content starts on page 2.
    story.append(Spacer(1, 1))
    story.append(PageBreak())
    story.extend(build_contents(styles, toc_pages))

    build_lane1(story, styles, doc)
    build_lane2(story, styles, doc)
    build_lane3(story, styles, doc)
    build_lane4(story, styles, doc)
    build_lane5(story, styles, doc, toc_pages)
    return story


def main():
    styles = build_styles()
    # Two passes: pass 1 records where every section lands (doc.toc_pages),
    # pass 2 rebuilds with real page numbers in the Contents and R-index.
    # Placeholder and final tables have identical column widths and row counts,
    # so pagination is stable between passes.
    toc_pages = {}
    for _ in range(2):
        doc = FocusDockDoc(
            OUTPUT,
            pagesize=letter,
            leftMargin=MARGIN,
            rightMargin=MARGIN,
            topMargin=MARGIN,
            bottomMargin=0.9 * inch,
            title="Focus Dock — The ADHD Notion Recovery Guide (Version 2)",
            author="Focus Dock · getfocusdock.com",
            subject="Install a minimal 3-database Notion system and stop the setup spiral.",
        )
        doc.build(build_story(styles, doc, toc_pages),
                  onFirstPage=draw_cover_page, onLaterPages=paint_page_bg)
        toc_pages = doc.toc_pages
    print(f"Generated: {OUTPUT} ({len(toc_pages)} TOC entries)")


if __name__ == "__main__":
    main()
