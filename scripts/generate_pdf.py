#!/usr/bin/env python3
"""Generate Focus Dock ADHD Notion Recovery Guide PDF (v2 — ADHD-first lanes + boxes).

Cover image: run scripts/generate_cover.py first (assets/focus_dock_cover.png).
"""

from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = str(ROOT / "private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide.pdf")
COVER_IMG = str(ROOT / "assets/focus_dock_cover.png")

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


def build_styles():
    base = getSampleStyleSheet()
    styles = {
        "title": ParagraphStyle(
            "title",
            parent=base["Title"],
            fontSize=28,
            leading=32,
            textColor=WHITE,
            alignment=TA_CENTER,
            spaceAfter=12,
            fontName="Helvetica-Bold",
        ),
        "subtitle": ParagraphStyle(
            "subtitle",
            parent=base["Normal"],
            fontSize=14,
            leading=18,
            textColor=MINT,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName="Helvetica",
        ),
        "lane_title": ParagraphStyle(
            "lane_title",
            parent=base["Heading1"],
            fontSize=16,
            leading=20,
            textColor=WHITE,
            spaceBefore=0,
            spaceAfter=0,
            fontName="Helvetica-Bold",
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontSize=14,
            leading=20,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "ref_h2": ParagraphStyle(
            "ref_h2",
            parent=base["Heading2"],
            fontSize=13,
            leading=18,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontSize=12,
            leading=18,
            textColor=CORAL,
            spaceBefore=12,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=11,
            leading=17,
            textColor=DARK_TEXT,
            spaceAfter=10,
            fontName="Helvetica",
        ),
        "callout_label": ParagraphStyle(
            "callout_label",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=DARK_TEXT,
            fontName="Helvetica-Bold",
        ),
        "callout_body": ParagraphStyle(
            "callout_body",
            parent=base["Normal"],
            fontSize=11,
            leading=17,
            textColor=DARK_TEXT,
            fontName="Helvetica",
        ),
        "lane_label": ParagraphStyle(
            "lane_label",
            parent=base["Normal"],
            fontSize=9,
            leading=13,
            textColor=MID_TEXT,
            fontName="Helvetica-Bold",
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["Normal"],
            fontSize=11,
            leading=17,
            textColor=NAVY,
            spaceBefore=4,
            spaceAfter=4,
            fontName="Helvetica-Bold",
        ),
        "step": ParagraphStyle(
            "step",
            parent=base["Normal"],
            fontSize=11,
            leading=15,
            textColor=DARK_TEXT,
            leftIndent=20,
            spaceAfter=6,
            fontName="Helvetica",
        ),
        "formula": ParagraphStyle(
            "formula",
            parent=base["Code"],
            fontSize=9,
            leading=12,
            textColor=WHITE,
            backColor=NAVY,
            borderPadding=8,
            fontName="Courier",
            spaceAfter=8,
        ),
        "footer": ParagraphStyle(
            "footer",
            parent=base["Normal"],
            fontSize=9,
            textColor=MID_TEXT,
            alignment=TA_CENTER,
        ),
        "toc": ParagraphStyle(
            "toc",
            parent=base["Normal"],
            fontSize=11,
            leading=16,
            textColor=DARK_TEXT,
            spaceAfter=6,
            fontName="Helvetica",
        ),
        "table_cell": ParagraphStyle(
            "table_cell",
            parent=base["Normal"],
            fontSize=8.5,
            leading=11,
            textColor=DARK_TEXT,
            fontName="Helvetica",
        ),
        "table_header": ParagraphStyle(
            "table_header",
            parent=base["Normal"],
            fontSize=9,
            leading=12,
            textColor=WHITE,
            fontName="Helvetica-Bold",
        ),
    }
    return styles


def _callout_table(label, body_html, styles, border_color, bg_color, label_color, border_width=2):
    label_para = Paragraph(
        f'<font color="{label_color.hexval()}"><b>{label}</b></font>',
        styles["callout_label"],
    )
    body_para = Paragraph(body_html, styles["callout_body"])
    t = Table([[label_para], [body_para]], colWidths=[CONTENT_W], splitByRow=1)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg_color),
        ("BOX", (0, 0), (-1, -1), border_width, border_color),
        ("LEFTPADDING", (0, 0), (-1, -1), 12),
        ("RIGHTPADDING", (0, 0), (-1, -1), 12),
        ("TOPPADDING", (0, 0), (-1, 0), 10),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 12),
        ("TOPPADDING", (0, 1), (-1, 1), 4),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    return t


def lane_banner(label, styles):
    """Single full-width lane header — avoids stacked yellow paragraph backgrounds."""
    t = Table([[Paragraph(label, styles["lane_title"])]], colWidths=[CONTENT_W])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY),
        ("LEFTPADDING", (0, 0), (-1, -1), 14),
        ("RIGHTPADDING", (0, 0), (-1, -1), 14),
        ("TOPPADDING", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 11),
    ]))
    return t


def inline_callout(text, styles):
    return _callout_table(">>", text, styles, CORAL, LIGHT_BG, NAVY, border_width=1)


def anchor_box(you_are_here, win, styles, skip_if=None):
    lines = [
        f"<b>YOU ARE HERE:</b> {you_are_here}",
        f"<b>WIN:</b> {win}",
    ]
    if skip_if:
        lines.append(f"<b>SKIP IF:</b> {skip_if}")
    return _callout_table("ANCHOR", "<br/>".join(lines), styles, CORAL, BOX_CORAL, CORAL)


def do_this_now(steps, styles):
    items = "".join(f"{i + 1}. {s}<br/>" for i, s in enumerate(steps))
    return _callout_table("DO THIS NOW", items, styles, MINT, BOX_MINT, NAVY)


def checkpoint(lines, stuck_pointer, styles):
    body = "<br/>".join(f"✓ {l}" for l in lines)
    body += f"<br/><b>Stuck?</b> → {stuck_pointer}"
    return _callout_table(
        "CHECKPOINT", body, styles, NAVY, LIGHT_BG, CHECK_GREEN, border_width=1
    )


def if_you_drift(signal, recovery, fallback, styles):
    body = (
        f"Noticed yourself {signal}?<br/>"
        f"→ {recovery}<br/>"
        f"→ Still in this section? Skip to <b>{fallback}</b>."
    )
    return _callout_table(
        "⚠ IF YOU DRIFT", body, styles, WARN_AMBER, BOX_YELLOW, WARN_AMBER
    )


def begin_lane(story, styles, doc, lane_label):
    doc.current_lane = lane_label
    story.append(PageBreak())
    story.append(lane_banner(lane_label, styles))
    story.append(Spacer(1, 18))


def emit_blocks(story, styles, blocks):
    for kind, text in blocks:
        if kind == "break":
            story.append(PageBreak())
        elif kind == "anchor":
            story.append(anchor_box(**text, styles=styles))
            story.append(Spacer(1, 8))
        elif kind == "do_now":
            story.append(do_this_now(text, styles))
            story.append(Spacer(1, 8))
        elif kind == "checkpoint":
            story.append(checkpoint(**text, styles=styles))
            story.append(Spacer(1, 8))
        elif kind == "drift":
            story.append(if_you_drift(**text, styles=styles))
            story.append(Spacer(1, 8))
        elif kind == "h2":
            story.append(Paragraph(text, styles["h2"]))
        elif kind == "h3":
            story.append(Paragraph(text, styles["h3"]))
        elif kind == "callout":
            story.append(inline_callout(text, styles))
            story.append(Spacer(1, 8))
        elif kind == "formula":
            story.append(Paragraph(text.replace("\n", "<br/>"), styles["formula"]))
        elif kind == "step":
            story.append(Paragraph(text, styles["step"]))
        elif kind == "spacer":
            story.append(Spacer(1, float(text)))
        elif kind == "table":
            story.append(text)
        else:
            story.append(Paragraph(text, styles["body"]))


def section(story, styles, title, blocks, page_break_after=False, ref=False):
    story.append(Spacer(1, 14))
    story.append(Paragraph(title, styles["ref_h2" if ref else "h2"]))
    story.append(HRFlowable(
        width="20%" if not ref else "100%",
        thickness=1.5 if not ref else 0.5,
        color=CORAL if not ref else LIGHT_BG,
        spaceBefore=2,
        spaceAfter=12,
    ))
    emit_blocks(story, styles, blocks)
    story.append(Spacer(1, 6))
    if page_break_after:
        story.append(PageBreak())


def draw_cover_page(canvas, doc):
    if Path(COVER_IMG).exists():
        canvas.drawImage(COVER_IMG, 0, 0, width=PAGE_W, height=PAGE_H)


def paint_page_bg(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(PAGE_BG)
    canvas.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    canvas.restoreState()


def add_page_number(canvas, doc):
    paint_page_bg(canvas, doc)
    canvas.saveState()
    lane = getattr(doc, "current_lane", "")
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_TEXT)
    left = f"Focus Dock · {lane} · getfocusdock.com" if lane else "Focus Dock · getfocusdock.com"
    canvas.drawString(MARGIN, 0.5 * inch, left)
    canvas.drawRightString(PAGE_W - MARGIN, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def start_here_page(styles, doc):
    """Lane 1 opening — reading map + lane picker."""
    doc.current_lane = "LANE 1 — START HERE"
    story = []
    story.append(lane_banner("LANE 1 — START HERE", styles))
    story.append(Spacer(1, 18))
    story.append(anchor_box(
        "Lane 1 → Reading map",
        "You know which lane to enter and when to stop reading.",
        styles,
        skip_if="You already finished install — jump to Lane 4.",
    ))
    story.append(Spacer(1, 8))
    story.append(
        Paragraph(
            "<b>Don't read cover to cover.</b> Pick a lane. Stop when you hit the checkpoint.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 8))

    rows = [
        [Paragraph("<b>If you…</b>", styles["table_header"]),
         Paragraph("<b>Go to</b>", styles["table_header"])],
        [Paragraph("Need proof this is for you", styles["toc"]),
         Paragraph("Lane 1 → Self-check", styles["toc"])],
        [Paragraph("Want a win RIGHT NOW", styles["toc"]),
         Paragraph("Lane 2 — Quick Win", styles["toc"])],
        [Paragraph("Ready to build", styles["toc"]),
         Paragraph("Lane 3 — Install", styles["toc"])],
        [Paragraph("Already installed", styles["toc"]),
         Paragraph("Lane 4 — Daily Use", styles["toc"])],
        [Paragraph("Something broke / drowning", styles["toc"]),
         Paragraph("Lane 4 → Emergency or Lane 5", styles["toc"])],
        [Paragraph("Looking something up", styles["toc"]),
         Paragraph("Lane 5 — Reference", styles["toc"])],
    ]
    toc_table = Table(rows, colWidths=[2.5 * inch, 4.0 * inch])
    toc_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.5, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))
    story.append(toc_table)
    story.append(Spacer(1, 10))
    story.append(inline_callout(
        "<b>Default path:</b> Self-check → Quick Win → Install → "
        "one visible task → close Notion.",
        styles,
    ))
    story.append(do_this_now([
        "Pick your lane from the table above.",
        "Open only that lane.",
        "Close the PDF when you hit the checkpoint.",
    ], styles))
    return story


def build_content(styles, doc):
    story = []

    # Lane 1 continued — self-check + preview
    story.append(PageBreak())
    story.append(anchor_box(
        "Lane 1 → Self-check",
        "You know if Focus Dock is for you.",
        styles,
    ))
    story.append(Spacer(1, 8))
    emit_blocks(story, styles, [
        ("h2", "You need this guide if…"),
        ("step", "[ ] You've abandoned 2+ Notion templates in the past year"),
        ("step", "[ ] You've spent 3+ hours setting up before doing one real task"),
        ("step", "[ ] You have habit trackers with broken streaks you avoid looking at"),
        ("step", "[ ] 'Do laundry' or 'email boss' sits on your list for 5+ days"),
        ("step", "[ ] You feel productive while customizing but not while working"),
        ("h2", "Skip this guide if…"),
        ("step", "[ ] You already use Notion daily without thinking about it"),
        ("step", "[ ] You enjoy building systems as a hobby (separate from productivity)"),
        ("step", "[ ] You have a coach/assistant who manages your task list"),
    ])
    story.append(checkpoint(
        ["3+ checks in 'need this'? → Lane 2", "0–2 checks? This guide may not be your bottleneck"],
        "Lane 5 → R-13 FAQ",
        styles,
    ))
    story.append(if_you_drift(
        "reading FAQ before doing anything",
        "Lane 2 first. FAQ is R-13. Win before walls of text.",
        "Lane 2 — Quick Win",
        styles,
    ))
    story.append(Spacer(1, 10))
    section(story, styles, "WHAT YOU'LL BUILD (PREVIEW ONLY)", [
        ("body", "<b>Database 1 — [BRAIN] Brain Dump:</b> 2-second capture. No tags, no projects, no guilt."),
        ("body", "<b>Database 2 — [TODAY] Today:</b> ONE visible next action. Task sequences hide future steps."),
        ("body", "<b>Database 3 — [PROJECTS] Projects:</b> Parking lot for someday. You visit weekly, not daily."),
        ("body", "<b>[HOME] Home Screen:</b> Single page. No sidebar maze. Open → see next task → do it."),
        ("do_now", ["Do NOT build yet. Finish Lane 2 first.", "Open Lane 2 when ready."]),
    ])

    # Lane 2 — quick win
    begin_lane(story, styles, doc, "LANE 2 — QUICK WIN")
    section(story, styles, "THE ONE-TASK RULE", [
        ("anchor", {"you_are_here": "Lane 2 → One-task rule",                    "win": "You picked one avoided task.", "skip_if": None}),
        ("body", "Twelve databases = twelve decisions before breakfast. Your brain is already tired."),
        ("body", "We're cutting that to <b>one visible task</b>. Notion comes later. Task completion comes now."),
        ("do_now", [
            "Name one task you've avoided 3+ days.",
            "Write it on paper — not in Notion.",
            "Say it out loud once.",
        ]),
    ])
    section(story, styles, "SHRINK IT SMALL", [
        ("anchor", {"you_are_here": "Lane 2 → Shrink task",                    "win": "Your task is small enough to start.", "skip_if": None}),
        ("body", "<b>Laundry</b> → put 3 items in hamper.<br/><b>Email boss</b> → open draft.<br/><b>Clean kitchen</b> → put 3 dishes in sink."),
        ("do_now", ["Rewrite YOUR task as the smallest version.", "If still too big, shrink again."]),
        ("checkpoint", {"lines": ["Could do the shrunk version right now?"],
                        "stuck_pointer": "Shrink again — smaller is better"}),
    ])
    section(story, styles, "DO IT ON PAPER (NO NOTION YET)", [
        ("anchor", {"you_are_here": "Lane 2 → Do the task",                    "win": "One real task finished.", "skip_if": None}),
        ("do_now", [
            "Do it now — phone in another room.",
            "Do the shrunk task. Phone in another room.",
            "Mark a check on paper when done.",
        ]),
        ("checkpoint", {"lines": ["Task done or you stopped"], "stuck_pointer": "Lane 4 → Emergency"}),
        ("drift", {"signal": "customizing your phone notes app",
                   "recovery": "Defaults are fine. Sticky note works.",
                   "fallback": "Do the tiny task on paper"}),
    ])
    section(story, styles, "BRIDGE TO INSTALL", [
        ("callout", ">> <b>You just did the hard part.</b> Starting beats any dashboard. Notion only holds the task — you already proved you can finish one."),
        ("body", "When you're ready: Lane 3 — Install. Same one-task energy."),
        ("do_now", ["Open Lane 3 when ready.", "Phone in another room. Open Notion only."]),
    ], page_break_after=True)

    # Lane 3 — Install
    begin_lane(story, styles, doc, "LANE 3 — INSTALL")
    section(story, styles, "INSTALL PREAMBLE", [
        ("anchor", {"you_are_here": "Lane 3 → Before you start",                    "win": "You know the rules before building.", "skip_if": "Already installed → Lane 4"}),
        ("body", "This is not a template to admire. It is a <b>recovery protocol</b>. Zero philosophy until Lane 4."),
        ("h2", "What you need"),
        ("step", "• Notion account (free tier works)"),
        ("step", "• One uninterrupted session (phone in another room)"),
        ("step", "• Permission to quarantine your template graveyard"),
        ("callout", ">> RULE ZERO: Urge to add a 4th database? <b>Setup spiral.</b> Close Notion. Do one real task."),
        ("drift", {"signal": "watching Notion tutorial videos",
                   "recovery": "Close YouTube. Open R-2 UI Map. Find the button.",
                   "fallback": "Quarantine the graveyard (start of install)"}),
    ])

    section(story, styles, "THE INSTALL", [
        ("anchor", {"you_are_here": "Lane 3 → Install",                    "win": "3 databases + homepage + one task done.", "skip_if": None}),
        ("h3", "Quarantine the graveyard"),
        ("step", "1. Open Notion sidebar. Count your productivity-related pages."),
        ("step", "2. If more than 5: create page titled <b>[GRAVEYARD] Template Graveyard</b>."),
        ("step", "3. Drag every abandoned dashboard, habit tracker, and PARA clone into it. Do not open them."),
        ("step", "4. Collapse the graveyard. You are not deleting — you're quarantining shame."),
        ("h3", "Create Database 1 — [BRAIN] Brain Dump"),
        ("step", "1. New page: <b>[BRAIN] Brain Dump</b> → type /table → Full page database."),
        ("step", "2. Rename default title property to <b>Thought</b>."),
        ("step", "3. Add property: <b>Captured</b> (Created time — auto)."),
        ("step", "4. Add property: <b>Processed?</b> (Checkbox)."),
        ("step", "5. Delete every other property. Yes, all of them."),
        ("step", "6. Create view <b>Inbox</b>: filter Processed? is unchecked. Sort: Captured ascending."),
        ("callout", "Usage rule: Capture in 2 seconds. Thought only. No tags. Process during Sunday reset or when Today is empty."),
        ("break", ""),
        ("h3", "Create Database 2 — [TODAY] Today"),
        ("step", "1. New page: <b>[TODAY] Today</b> → /table → Full page database."),
        ("step", "2. Properties to create:"),
        ("body", "• <b>Task</b> (Title)<br/>• <b>Done</b> (Checkbox)<br/>• <b>Due</b> (Date)<br/>• <b>Energy</b> (Select: [HIGH] High / [MED] Medium / [LOW] Low)<br/>• <b>Task Before</b> (Relation → Today, two-way)<br/>• <b>Task After</b> (Relation → Today, two-way)"),
        ("h3", "Roll-ups for task sequences"),
        ("step", "• <b>Before Done</b> — Rollup: Task Before → Done → Count checked"),
        ("step", "• <b>Before Due</b> — Rollup: Task Before → Due → Latest date"),
        ("h3", "Property: Hide Sequence (Formula checkbox)"),
        ("body", "Create a formula property named <b>Hide Sequence</b>. Paste this formula:"),
        ("formula", 'if(empty(prop("Task Before")), false, if(prop("Before Done") > 0, false, if(prop("Due") < prop("Before Due"), false, true)))'),
        ("h3", "Property: Hide (Formula)"),
        ("body", "Create a second formula property named <b>Hide</b>. Paste this formula:"),
        ("formula", 'prop("Hide Sequence")'),
        ("step", "7. View <b>Do This Next</b>: Filter Hide = unchecked AND Done = unchecked. Sort: Due ascending. Show 1 card if using gallery, or limit to top row."),
        ("callout", "This view is your entire daily driver. One task visible. Everything else is hidden by sequence logic."),
        ("h3", "Create Database 3 — [PROJECTS] Projects"),
        ("step", "1. New page: <b>[PROJECTS] Projects</b> → /table → Full page database."),
        ("step", "2. Properties: <b>Name</b> (Title), <b>Status</b> (Select: [IDEA] Idea / [ACTIVE] Active / [LOW] Paused / [DONE] Done), <b>Next Action</b> (Text)."),
        ("step", "3. View <b>Active</b>: Status = Active. Sort: manual (drag what matters to top)."),
        ("body", "You do NOT work from this database daily. During Sunday reset, pick one Next Action and move it to Today."),
        ("h3", "Build [HOME] Home Screen"),
        ("step", "1. New page: <b>[HOME] Focus Dock</b> (make this your Notion home)."),
        ("step", "2. Add heading: <b>Right now:</b>"),
        ("step", "3. Type /linked → link <b>Do This Next</b> view from Today (embedded, not full database)."),
        ("step", "4. Add heading: <b>Brain dump (2 sec):</b> → /linked → Brain Dump Inbox view."),
        ("step", "5. Add toggle: <b>Projects (Sunday only)</b> → link Active view."),
        ("step", "6. Settings → set <b>[HOME] Focus Dock</b> as homepage."),
        ("callout", "Done. Close Notion. Do the one visible task. You win."),
        ("do_now", ["Do one real task from Do This Next.", "Mark Done. Close Notion."]),
    ], page_break_after=True)

    story.extend(build_install_checklist(styles))

    # Lane 4 — Daily use
    begin_lane(story, styles, doc, "LANE 4 — DAILY USE")
    section(story, styles, "DAILY WORKFLOW", [
        ("anchor", {"you_are_here": "Lane 4 → Daily workflow",                    "win": "You know the morning/evening rhythm.", "skip_if": None}),
        ("h2", "Morning"),
        ("step", "1. Open [HOME] Focus Dock."),
        ("step", "2. Read the one task in Do This Next."),
        ("step", "3. Do it before opening email, Slack, or TikTok."),
        ("h2", "During the day"),
        ("step", "• Intrusive thought? → Brain Dump. One line. Close."),
        ("step", "• Finished task? → Check Done. Next sequence step appears automatically."),
        ("h2", "Evening"),
        ("step", "• If Today is empty: pull ONE task from Brain Dump or Projects."),
        ("step", "• Do NOT rebuild your dashboard. Do NOT add properties. Go to bed."),
        ("callout", "If you did nothing else today but open Focus Dock once and complete one task: <b>system success.</b>"),
        ("checkpoint", {"lines": ["You can describe the daily flow"],
                        "stuck_pointer": "R-4 When to Use What table"}),
    ])

    section(story, styles, "TASK SEQUENCES — WHEN BIG TASKS FREEZE YOU", [
        ("body", "Big tasks are lying to you. 'Do laundry' is 8 tasks. 'Make video' is 14. When all 8 show at once, your brain files them under 'not now.'"),
        ("h2", "How sequences work"),
        ("body", "Link tasks with Task Before / Task After relations. The Hide Sequence formula hides step 2 until step 1 is done. You only ever see the next physical action."),
        ("h2", "Example: Laundry sequence"),
        ("step", "1. Collect dirty clothes"),
        ("step", "2. Check gym bag → Task Before: #1"),
        ("step", "3. Start washer → Task Before: #2"),
        ("step", "4. Move to dryer → Task Before: #3"),
        ("step", "5. Fold → Task Before: #4"),
        ("step", "6. Put away → Task Before: #5"),
        ("h2", "Example: Email boss sequence"),
        ("step", "1. Open draft from last week"),
        ("step", "2. Write 3 bullet points only"),
        ("step", "3. Read aloud once"),
        ("step", "4. Hit send → Task Before: #3"),
        ("h2", "Example: Grocery run (6 steps)"),
        ("step", "1. Check fridge → 2. Write 5-item list max → 3. Grab bags → 4. Drive/walk → 5. Buy only list items → 6. Unload 3 items"),
        ("h2", "Example: Taxes (one sitting)"),
        ("step", "1. Find login → 2. Download one form → 3. Fill name/address → 4. One deduction section → 5. Save draft → 6. Schedule finish date"),
        ("callout", "Rule: Break until the step feels 'too small to fail.' If you still can't start, break it again."),
        ("drift", {"signal": "building a 14-step video sequence",
                   "recovery": "Max 6 steps today. Break more later.",
                   "fallback": "Laundry example above"}),
    ], page_break_after=True)

    section(story, styles, "SUNDAY RESET", [
        ("anchor", {"you_are_here": "Lane 4 → Sunday reset",                    "win": "Week prepped without guilt dashboard.", "skip_if": None}),
        ("body", "No guilt weekly review. No streak accounting."),
        ("h2", "Brain Dump triage"),
        ("step", "• Open Inbox. For each item: delete, move to Today, or move to Projects Next Action."),
        ("step", "• Check Processed? on handled items."),
        ("h2", "Today prep"),
        ("step", "• Clear Done tasks (archive or delete — your choice)."),
        ("step", "• Ensure 3–5 tasks max for the week, sequenced where needed."),
        ("step", "• Pick Monday's first task. Set Due = Monday."),
        ("h2", "Projects glance"),
        ("step", "• Open Active projects. Max 3 Active at once. Pause the rest."),
        ("step", "• Update one Next Action per active project."),
        ("callout", "Stop even if unfinished. Consistency beats completeness."),
        ("checkpoint", {"lines": ["Reset feels complete enough"], "stuck_pointer": "R-7 Sunday Reset printable"}),
        ("drift", {"signal": "Sunday reset running long",
                   "recovery": "Stop here. Incomplete beats skipped.",
                   "fallback": "R-7 printable checklist"}),
    ])

    section(story, styles, "EMERGENCY OVERWHELM PROTOCOL", [
        ("anchor", {"you_are_here": "Lane 4 → Emergency",                    "win": "You survived overwhelm with one tiny action.", "skip_if": None}),
        ("body", "For days when everything feels loud. Print Part 15. Tape it to your monitor."),
        ("callout", "[ALERT] OVERWHELM MODE — Do only these 4 steps:"),
        ("step", "1. <b>Box breathing:</b> 4 sec in, 4 hold, 4 out. Twice."),
        ("step", "2. <b>Brain dump 3 words</b> — not sentences. What's loudest?"),
        ("step", "3. <b>Shrink to smallest version:</b> 'Clean kitchen' → 'put 3 dishes in sink.'"),
        ("step", "4. <b>Do the smallest version.</b> Mark done. Stop. You survived."),
        ("body", "Do NOT: reorganize Notion, watch setup videos, download a new template, or redesign colors. That is the trap."),
        ("h2", "When to skip Notion entirely"),
        ("body", "If you haven't opened Focus Dock in 5+ days: use a sticky note for one task. Return to Notion only when the sticky works for 2 days straight."),
    ], page_break_after=True)

    section(story, styles, "MAINTENANCE — ANTI-REBUILD RULES", [
        ("h2", "Allowed changes (after Day 8)"),
        ("step", "• Adjust Energy labels"),
        ("step", "• Add ONE filter to Do This Next"),
        ("step", "• Change homepage label"),
        ("h2", "Banned until Day 30"),
        ("step", "• Habit trackers"),
        ("step", "• Mood logs"),
        ("step", "• PARA / Second Brain migrations"),
        ("step", "• New databases"),
        ("step", "• Aesthetic overhauls"),
        ("callout", "The 3-week test: If you're still using Focus Dock daily without thinking about it — you succeeded. If not, the system is still too complex. Delete one more thing."),
        ("drift", {"signal": "thinking 'just one new view'",
                   "recovery": "Customization trap. Defaults until Day 8.",
                   "fallback": "R-5 Setup Spiral Red Flags"}),
    ])

    story.extend(build_days_2_7_playbook(styles))

    section(story, styles, "WHY YOUR OLD SYSTEM FAILED (OPTIONAL)", [
        ("anchor", {"you_are_here": "Lane 4 → Context",                    "win": "You understand why templates failed — without shame.",
                    "skip_if": "Read when curious, not before install."}),
        ("body", "You are not lazy. Your old system was designed to produce screenshots, not completed tasks."),
        ("h2", "1. Dopamine spent on setup"),
        ("body", "Customizing Notion releases dopamine. By Saturday night the dopamine budget is empty."),
        ("h2", "2. Choice overload"),
        ("body", "Typical ADHD templates: 6+ databases. Each opening = 12 micro-decisions."),
        ("h2", "3. Streak shame"),
        ("body", "Miss one habit day → broken streak → you close the tab."),
        ("callout", "Focus Dock fix: Low setup cost. Low decision density. No visible state that punishes missed days."),
    ])

    section(story, styles, "TASK SEQUENCE LIBRARY", [
        ("anchor", {"you_are_here": "Lane 4 → Sequence library",                    "win": "You picked one pre-built sequence to copy.", "skip_if": None}),
        ("body", "Copy these into Today database. Link with Task Before relations. Adjust names to your life."),
        ("h2", "[HOME] Clean kitchen (8 steps)"),
        ("step", "1. Put 3 dishes in sink → 2. Fill sink with soap water → 3. Scrub dishes → 4. Rinse → 5. Load dishwasher → 6. Wipe counter → 7. Take out trash → 8. Sweep floor"),
        ("h2", "[EMAIL] Email boss (5 steps)"),
        ("step", "1. Open draft → 2. Write 3 bullets only → 3. Read aloud → 4. Fix typos → 5. Send"),
        ("h2", "[BED] Change bedsheets (6 steps)"),
        ("step", "1. Strip pillowcases → 2. Strip sheets → 3. Put in hamper → 4. Put new fitted sheet → 5. Put new flat sheet → 6. Pillowcases on"),
        ("h2", "[VIDEO] YouTube video (10 steps)"),
        ("step", "1. Pick topic → 2. Outline 5 bullets → 3. Write script → 4. Set up camera → 5. Record → 6. Transfer files → 7. Rough cut → 8. Thumbnail → 9. Upload → 10. Description + tags"),
        ("h2", "[RX] Refill prescription (7 steps)"),
        ("step", "1. Check pill bottle date → 2. Call pharmacy → 3. Confirm insurance → 4. Wait for ready text → 5. Drive/walk → 6. Pick up → 7. Put in weekly organizer"),
        ("h2", "[CLEAN] Quick room rescue"),
        ("step", "1. Trash bag in hand → 2. Pick up 5 items → 3. Put away 3 items → 4. Clear one surface → 5. Stop (done)"),
        ("callout", "Pre-build sequences on a good day. Reuse forever. This is your dopamine investment — not color palettes."),
        ("do_now", ["Pick one sequence on a good day.", "Copy into Today with Task Before links."]),
    ])

    story.extend(build_sequence_worksheets(styles))

    section(story, styles, "WEEK 1–4 ROLLOUT", [
        ("anchor", {"you_are_here": "Lane 4 → Week rollout",                    "win": "You know what each week adds.", "skip_if": None}),
        ("h2", "Week 1: Survival mode"),
        ("step", "• Day 1: Install only. No customization."),
        ("step", "• Days 2–7: One task per day minimum. Brain dump only when intrusive."),
        ("step", "• Banned: adding properties, new views, watching Notion tutorials"),
        ("h2", "Week 2: Add sequences"),
        ("step", "• Pick your most-delayed task. Break into sequence."),
        ("step", "• Add 2nd sequence only after first works 3 times"),
        ("h2", "Week 3: Sunday reset habit"),
        ("step", "• First Sunday reset. Stop even if messy."),
        ("step", "• If you skip: no catch-up. Next Sunday, fresh start."),
        ("h2", "Week 4: Evaluate"),
        ("body", "Ask: Am I opening Focus Dock without dread? If yes: success. If no: delete one more feature."),
        ("callout", "The 3-week test from research: systems that survive 21 days become automatic. You're building automatic."),
    ])

    story.extend(build_accountability_guide(styles))

    # Lane 5 — Reference
    begin_lane(story, styles, doc, "LANE 5 — REFERENCE")
    story.extend(build_formula_reference(styles))
    story.extend(build_notion_ui_map(styles))

    section(story, styles, "QUICK REFERENCE CARD", [
        ("body", "<b>Capture:</b> Brain Dump → Thought → close (2 sec)"),
        ("body", "<b>Work:</b> [HOME] Focus Dock → Do This Next → one task"),
        ("body", "<b>Sequence:</b> Task Before relation + Hide Sequence formula"),
        ("body", "<b>Weekly:</b> Sunday reset"),
        ("body", "<b>Emergency:</b> smallest-step shrink → do → stop"),
        ("body", "<b>Homepage:</b> [HOME] Focus Dock (not sidebar maze)"),
    ], ref=True)

    section(story, styles, "TROUBLESHOOTING", [
        ("h2", "I keep customizing instead of doing"),
        ("body", "Set a build budget: zero customizing on weekdays. Customization is Sunday only."),
        ("h2", "Too many tasks visible"),
        ("body", "Check Hide formula is applied. Filter Do This Next: Hide = unchecked."),
        ("h2", "Sequences not hiding"),
        ("body", "Confirm Task Before is two-way relation. Before Done rollup must count checked boxes."),
        ("h2", "I abandoned it for a week"),
        ("body", "No guilt dashboard. Delete done tasks, pull ONE from Brain Dump, continue. Streaks don't exist here."),
        ("h2", "Want more structure"),
        ("body", "Read that again. Wanting more structure is often productivity theater wearing a productivity costume. Stay at 3 databases for 30 days first."),
        ("h2", "Hide Sequence always shows true / everything hidden"),
        ("body", "Check Before Done rollup counts <i>checked</i> boxes on Task Before. Verify Task Before relation points to the correct prior step."),
        ("h2", "Do This Next is empty but I have tasks"),
        ("body", "Uncheck Done on active tasks. Confirm Due dates exist. If using sequences, ensure step 1 has no Task Before link."),
        ("h2", "Brain Dump inbox never empties"),
        ("body", "Normal. Inbox is capture, not completion. Process during Sunday reset only — max your reset window."),
        ("h2", "I added a 4th database"),
        ("body", "Delete it today. Move any useful items to Brain Dump or Projects. Do not migrate relations."),
    ], page_break_after=True, ref=True)

    section(story, styles, "WHAT TO DELETE FROM OLD TEMPLATES", [
        ("body", "When quarantining your Template Graveyard, these features are banned in Focus Dock:"),
        ("h2", "Delete or ignore permanently"),
        ("step", "• Habit streak counters"),
        ("step", "• Mood trackers (unless prescribed by therapist)"),
        ("step", "• Eisenhower matrices"),
        ("step", "• PARA 'Areas' and 'Resources' databases"),
        ("step", "• Weekly review dashboards with 20+ checkboxes"),
        ("step", "• Journal prompts you never read"),
        ("step", "• Finance dashboards (use bank app instead)"),
        ("h2", "Why each one fails ADHD brains"),
        ("body", "<b>Streaks:</b> One miss = shame monument.<br/><b>PARA:</b> 'Is this a Project or Area?' = decision paralysis.<br/><b>Weekly reviews:</b> 45 min of facing failure.<br/><b>Mood logs:</b> Evidence you're 'inconsistent.'"),
        ("callout", "If a feature requires daily maintenance to avoid looking broken, delete it."),
    ], ref=True)

    section(story, styles, "PROPERTY REFERENCE CARD", [
        ("h2", "Brain Dump database"),
        ("body", "• <b>Thought</b> (Title) — the capture<br/>• <b>Captured</b> (Created time)<br/>• <b>Processed?</b> (Checkbox)"),
        ("h2", "Today database"),
        ("body", "• <b>Task</b> (Title)<br/>• <b>Done</b> (Checkbox)<br/>• <b>Due</b> (Date)<br/>• <b>Energy</b> (Select: High/Medium/Low)<br/>• <b>Task Before</b> (Relation → Today)<br/>• <b>Task After</b> (Relation → Today)<br/>• <b>Before Done</b> (Rollup: count checked)<br/>• <b>Before Due</b> (Rollup: latest date)<br/>• <b>Hide Sequence</b> (Formula)<br/>• <b>Hide</b> (Formula)"),
        ("h2", "Projects database"),
        ("body", "• <b>Name</b> (Title)<br/>• <b>Status</b> (Select: Idea/Active/Paused/Done)<br/>• <b>Next Action</b> (Text)"),
        ("h2", "Do This Next view filters"),
        ("body", "Filter 1: Hide = unchecked<br/>Filter 2: Done = unchecked<br/>Sort: Due ascending"),
    ], ref=True)

    section(story, styles, "COMMON MISTAKES", [
        ("h2", "Mistake 1: Adding a 4th database"),
        ("body", "Fix: Delete it. You don't need a 'Someday/Maybe' or 'Reading List.' Brain Dump handles capture."),
        ("h2", "Mistake 2: Showing all tasks, not one"),
        ("body", "Fix: Check Hide formula. Gallery view with 1 card. Or table view sorted with only top row visible."),
        ("h2", "Mistake 3: Skipping Brain Dump"),
        ("body", "Fix: Intrusive thoughts will hijack focus. 2-second capture prevents 'I'll remember' lies."),
        ("h2", "Mistake 4: Sunday reset becomes too long"),
        ("body", "Fix: Hard stop at reset. Incomplete reset beats skipped reset."),
        ("h2", "Mistake 5: Rebuilding instead of using"),
        ("body", "Fix: If you haven't done a task today but you've opened Notion, close it. Setup spiral detected."),
        ("h2", "Mistake 6: Energy tags become a project"),
        ("body", "Fix: Energy is optional. Ignore it if choosing energy level causes decisions."),
    ], ref=True)

    section(story, styles, "ENERGY MATCHING (OPTIONAL)", [
        ("body", "Only use Energy tags if they help, not if choosing one causes paralysis."),
        ("h2", "[HIGH] High energy"),
        ("body", "Creative work, hard conversations, complex sequences, starting new projects."),
        ("h2", "[MED] Medium energy"),
        ("body", "Email, errands, admin, routine chores, continuing in-progress work."),
        ("h2", "[LOW] Low energy"),
        ("body", "Brain dump triage, tiny tasks, reading one paragraph, putting one item away."),
        ("callout", "On low days: filter Do This Next by Low energy OR ignore filter and do the smallest visible task."),
    ], ref=True)

    section(story, styles, "SUNDAY RESET CHECKLIST (PRINTABLE)", [
        ("body", "Print this page. Check boxes with pen during your Sunday reset. Stop when done."),
        ("step", "[ ] Open [BRAIN] Brain Dump Inbox — triage each item (delete / Today / Projects)"),
        ("step", "[ ] Mark Processed? on handled Brain Dump items"),
        ("step", "[ ] Archive or delete completed Today tasks"),
        ("step", "[ ] Today has 3–5 tasks max for the coming week"),
        ("step", "[ ] Monday's first task has Due = Monday"),
        ("step", "[ ] Max 3 [PROJECTS] Active — pause the rest"),
        ("step", "[ ] Each Active project has one Next Action written"),
        ("step", "[ ] Did NOT add properties, views, or databases"),
        ("step", "[ ] Reset feels complete enoughutes (even if unfinished)"),
        ("callout", ">> Incomplete reset beats skipped reset. Same time next Sunday — no catch-up guilt."),
    ], page_break_after=True, ref=True)

    section(story, styles, "PRINTABLE EMERGENCY CARD", [
        ("callout", "[CUT] CUT HERE — TAPE TO MONITOR [CUT]"),
        ("h2", "[ALERT] OVERWHELM MODE"),
        ("step", "1. Box breathe: 4 in, 4 hold, 4 out × 2"),
        ("step", "2. Brain dump 3 WORDS (not sentences)"),
        ("step", "3. Shrink to SMALLEST version"),
        ("step", "4. Do it. Mark done. STOP."),
        ("body", "<b>DO NOT:</b> Open Notion · Download templates · Reorganize · Watch setup videos"),
        ("body", "<b>IF 5+ DAYS AWAY:</b> Sticky note with ONE task. Return when sticky works 2 days."),
        ("callout", "You are not behind. You are not broken. One task is enough."),
    ], page_break_after=True, ref=True)

    section(story, styles, "FAQ", [
        ("h2", "Can I use this with medication?"),
        ("body", "Yes. Focus Dock is organizational, not medical. Keep your treatment plan."),
        ("h2", "What about mobile?"),
        ("body", "Notion mobile works. Add [HOME] Focus Dock to favorites. Brain dump from phone widget if available."),
        ("h2", "Can I share with my partner?"),
        ("body", "Personal license for one user. Partner needs own copy for their workspace."),
        ("h2", "Notion AI?"),
        ("body", "Skip it for now. AI features add decisions. Master the 3-database core first."),
        ("h2", "Migrate from Ultimate Brain / PARA?"),
        ("body", "Don't migrate. Quarantine old system. Fresh start prevents relation nightmares."),
        ("h2", "What if I need more than 3 databases eventually?"),
        ("body", "After 30 successful days, add ONE database. Not before. Prove the minimum works first."),
    ], ref=True)

    section(story, styles, "GLOSSARY", [
        ("body", "<b>Setup spiral:</b> Tweaking your system instead of doing the task the system was for."),
        ("body", "<b>Task sequence:</b> Linked sub-tasks where only the next step is visible."),
        ("body", "<b>Brain dump:</b> Frictionless capture inbox with no organization required."),
        ("body", "<b>Choice overload:</b> Too many options → paralysis → no action."),
        ("body", "<b>Executive dysfunction:</b> Knowing what to do but unable to initiate at the moment."),
        ("body", "<b>Template graveyard:</b> Collection of abandoned Notion setups you avoid opening."),
        ("body", "<b>Visible state:</b> Dashboard elements that break or look bad when not maintained."),
    ], ref=True)

    section(story, styles, "RESEARCH NOTES", [
        ("body", "Focus Dock design is informed by:"),
        ("step", "• Iyengar & Lepper (2000) — choice overload reduces action"),
        ("step", "• Volkow et al. (2009) — ADHD dopamine pathway differences"),
        ("step", "• Barkley (2012) — executive function as performance disorder"),
        ("step", "• Tuckman — externalize executive function to environment"),
        ("step", "• Lived experience: setup spiral threads in r/Notion and r/ADHD"),
        ("body", "This guide externalizes 'what's next' so your brain doesn't have to hold it."),
    ], page_break_after=True, ref=True)

    story.extend(build_brain_dump_guide(styles))
    story.extend(build_setup_spiral_red_flags(styles))
    story.extend(build_migration_checklist(styles))
    story.extend(build_when_to_use_what(styles))

    section(story, styles, "YOU MADE IT", [
        ("body", "If you're reading this, you built something most ADHD adults never finish: a system they actually use."),
        ("body", "Focus Dock isn't about perfect Notion. It's about <b>one visible next step</b> when your brain feels like static."),
        ("callout", "Questions? hello@getfocusdock.com · 14-day refund if it doesn't help — no guilt, same as the system."),
        ("body", "Now close this PDF and do the one task. [HOME]"),
    ], ref=True)

    return story


INSTALL_STEPS = [
    ("1", "Phone in another room. Open Notion desktop or browser only."),
    ("2", "Sidebar audit: count productivity pages. If 5+, create [GRAVEYARD] Template Graveyard page."),
    ("3", "Drag abandoned dashboards into graveyard. Do NOT open them. Collapse graveyard."),
    ("4", "Create new page: [BRAIN] Brain Dump. Type /table → Full page database."),
    ("5", "Rename title column to Thought. Delete all other default properties."),
    ("6", "Add Captured (Created time). Add Processed? (Checkbox). Save."),
    ("7", "Create Inbox view. Filter: Processed? unchecked. Sort: Captured ascending."),
    ("8", "Test capture: add 'test thought'. Confirm it appears in Inbox. Delete test."),
    ("9", "Create page [TODAY] Today. /table → Full page database."),
    ("10", "Add Task (title), Done (checkbox), Due (date), Energy (select)."),
    ("11", "Energy options: [HIGH] High, [MED] Medium, [LOW] Low. Save."),
    ("12", "Add Task Before relation to Today (two-way). Auto-creates Task After."),
    ("13", "Add Before Done rollup: Task Before → Done → Count checked."),
    ("14", "Add Before Due rollup: Task Before → Due → Latest date."),
    ("15", "Add Hide Sequence formula property (see R-1 Formula Reference)."),
    ("16", "Add Hide formula: prop(\"Hide Sequence\")."),
    ("17", "Create Do This Next view. Filter Hide unchecked, Done unchecked."),
    ("18", "Sort Do This Next by Due ascending. This is your daily driver."),
    ("19", "Add one test task 'Put 3 dishes in sink'. Confirm it shows in Do This Next."),
    ("20", "Create page [PROJECTS] Projects. /table → Full page database."),
    ("21", "Add Name, Status (Idea/Active/Paused/Done), Next Action (text)."),
    ("22", "Create Active view: Status = Active. Manual sort enabled."),
    ("23", "Add one project with Next Action text only. Do not add tasks here yet."),
    ("24", "Create page [HOME] Focus Dock. This becomes your home."),
    ("25", "Add heading: Right now. Embed linked Do This Next view from Today."),
    ("26", "Add heading: Brain dump. Embed linked Inbox view from Brain Dump."),
    ("27", "Add toggle: Projects (Sunday only). Embed Active view inside."),
    ("28", "Settings → set homepage to [HOME] Focus Dock."),
    ("29", "Close every other Notion tab. Only Focus Dock remains."),
    ("30", "Add first real task to Today. Not a test — something you've avoided."),
    ("31", "If task is big: stop. Break into 3-step sequence with Task Before links."),
    ("32", "Verify only step 1 visible in Do This Next. Steps 2-3 hidden."),
    ("33", "Move 3 Brain Dump items from old notes if any. Max 3. Check Processed."),
    ("34", "Review Projects: max 1 Active. Pause others."),
    ("35", "Delete any extra views you created during setup. Keep only essentials."),
    ("36", "Do NOT change colors, icons, or covers. Aesthetic trap — defaults are fine."),
    ("37", "Read Emergency Overwhelm Card. Bookmark mentally."),
    ("38", "Screenshot Focus Dock home for accountability. Do not post — private record."),
    ("39", "Write on paper: 'One task is enough.' Tape near desk."),
    ("40", "Calendar: recurring Sunday reset reminder."),
    ("41", "Do the one visible task NOW before closing guide."),
    ("42", "Mark Done. Watch next sequence step appear (if applicable)."),
    ("43", "If no next step: pull one item from Brain Dump to Today."),
    ("44", "Close Notion. Do not reopen until tomorrow morning."),
    ("45", "Journal one sentence: what made starting hard today?"),
    ("46", "Put guide PDF in easy-to-find folder. Name: Focus Dock Recovery."),
    ("47", "Text accountability buddy: 'Installed Focus Dock. One task done.'"),
    ("48", "You recovered. The graveyard can wait."),
]


SEQUENCE_WORKSHEETS = [
    ("GROCERIES", ["Check fridge", "Write 5-item list max", "Grab bags", "Drive/walk", "Buy only list items", "Unload 3 items"]),
    ("SHOWER", ["Get towel", "Get clean clothes", "Start water", "Shower", "Dry off", "Dress", "Hang towel"]),
    ("TAXES", ["Find login", "Download one form", "Fill name/address", "One deduction section", "Save draft", "Schedule finish date"]),
    ("CALL MOM", ["Write 2 topics", "Find quiet spot", "Dial", "Talk briefly", "Set next call date"]),
    ("WORKOUT", ["Put on shoes", "Fill water", "Short warmup", "Main exercise brief", "Cooldown", "Shower after"]),
]


def build_brain_dump_guide(styles):
    """Dense processing rules for Brain Dump inbox."""
    story = []
    section(story, styles, "BRAIN DUMP — PROCESSING GUIDE", [
        ("body", "Brain Dump is capture-only during the week. Processing happens in Sunday reset or when Today is empty."),
        ("h2", "The 10-second triage (per item)"),
        ("step", "1. <b>Delete</b> — noise, duplicates, 'someday' ideas you'll never do"),
        ("step", "2. <b>Today</b> — one physical action you could do this week"),
        ("step", "3. <b>Projects</b> — multi-step outcomes; write Next Action text only"),
        ("h2", "What NOT to do during triage"),
        ("step", "• Do not tag, categorize, or assign priority"),
        ("step", "• Do not create sub-pages or linked databases"),
        ("step", "• Do not process more than your reset window total"),
        ("h2", "When to capture (2 seconds)"),
        ("step", "• Intrusive thought during focused work"),
        ("step", "• 'I'll remember this' lie detected"),
        ("step", "• Partner asks you to do something while you're busy"),
        ("callout", ">> Capture is not commitment. Processing is not urgent. Today is the only daily driver."),
    ], page_break_after=True, ref=True)
    return story


def build_notion_ui_map(styles):
    """Where to click in Notion — reduces setup paralysis."""
    story = []
    rows = [
        [Paragraph("<b>Task</b>", styles["table_header"]),
         Paragraph("<b>Where in Notion</b>", styles["table_header"])],
        [Paragraph("Create database", styles["table_cell"]),
         Paragraph("New page → type <b>/table</b> → Full page", styles["table_cell"])],
        [Paragraph("Add property", styles["table_cell"]),
         Paragraph("Open database → <b>+</b> column header → pick type", styles["table_cell"])],
        [Paragraph("Formula property", styles["table_cell"]),
         Paragraph("Add property → Formula → paste from Part 2 or Formula Reference", styles["table_cell"])],
        [Paragraph("Relation", styles["table_cell"]),
         Paragraph("Add property → Relation → select same database → enable two-way", styles["table_cell"])],
        [Paragraph("Rollup", styles["table_cell"]),
         Paragraph("Add property → Rollup → pick relation → pick target property → pick calculation", styles["table_cell"])],
        [Paragraph("Filter view", styles["table_cell"]),
         Paragraph("View menu → Filter → add rule → Hide unchecked, Done unchecked", styles["table_cell"])],
        [Paragraph("Embed linked view", styles["table_cell"]),
         Paragraph("On [HOME] page → <b>/linked</b> → pick database → pick view only", styles["table_cell"])],
        [Paragraph("Set homepage", styles["table_cell"]),
         Paragraph("Settings & members → My settings → Homepage → [HOME] Focus Dock", styles["table_cell"])],
    ]
    table = Table(rows, colWidths=[1.4 * inch, 5.1 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))

    section(story, styles, "NOTION UI QUICK MAP", [
        ("body", "Lookup while installing. Do not watch tutorial videos — use this table instead."),
        ("table", table),
    ], page_break_after=True, ref=True)
    return story


def build_setup_spiral_red_flags(styles):
    """Recognize rebuild urges before they eat the day."""
    story = []
    flags = [
        ("New database idea", "You 'just need' a Reading List or Habits db. Use Brain Dump or Projects instead."),
        ("Color/icon session", "too long on aesthetics, zero tasks completed. Close Notion."),
        ("Tutorial spiral", "Watching 'ultimate Notion setup' videos during install week. Banned until Day 30."),
        ("Filter rabbit hole", "Adding 4th filter to Do This Next. Max one optional filter after Day 8."),
        ("Migration fantasy", "Planning to merge old PARA system into Focus Dock. Quarantine old system instead."),
        ("Weekly review creep", "Sunday reset running long. Hard stop — good enough beats perfect."),
        ("Streak mechanic", "Adding habit tracker to prove you're consistent. Streaks create shame monuments."),
        ("Property sprawl", "New properties: Priority, Context, Effort, Mood. Today has enough. Stop."),
    ]
    rows = [
        [Paragraph("<b>Red flag</b>", styles["table_header"]),
         Paragraph("<b>What to do instead</b>", styles["table_header"])],
    ]
    for flag, fix in flags:
        rows.append([
            Paragraph(flag, styles["table_cell"]),
            Paragraph(fix, styles["table_cell"]),
        ])
    table = Table(rows, colWidths=[1.5 * inch, 5.0 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))

    section(story, styles, "SETUP SPIRAL RED FLAGS", [
        ("body", "Catch these urges early. Each one feels productive. None complete tasks."),
        ("table", table),
        ("callout", ">> Ask: 'Will this help me see ONE next task tomorrow?' If no, don't do it."),
    ], page_break_after=True, ref=True)
    return story


def build_when_to_use_what(styles):
    """Decision tree — which database for which moment."""
    story = []
    rows = [
        [Paragraph("<b>Situation</b>", styles["table_header"]),
         Paragraph("<b>Use this</b>", styles["table_header"]),
         Paragraph("<b>Keep it</b>", styles["table_header"])],
        [Paragraph("Random thought while working", styles["table_cell"]),
         Paragraph("[BRAIN] Brain Dump — one line, close", styles["table_cell"]),
         Paragraph("2 seconds", styles["table_cell"])],
        [Paragraph("What should I do right now?", styles["table_cell"]),
         Paragraph("[HOME] Focus Dock — Do This Next view", styles["table_cell"]),
         Paragraph("90 seconds", styles["table_cell"])],
        [Paragraph("Big project with many steps", styles["table_cell"]),
         Paragraph("[TODAY] Today — break into sequence", styles["table_cell"]),
         Paragraph("Quick setup, then 1 step/day", styles["table_cell"])],
        [Paragraph("Someday idea, not this week", styles["table_cell"]),
         Paragraph("[PROJECTS] Projects — Idea status", styles["table_cell"]),
         Paragraph("Sunday reset only", styles["table_cell"])],
        [Paragraph("Overwhelmed, can't start", styles["table_cell"]),
         Paragraph("Part 15 emergency card — 2-min shrink", styles["table_cell"]),
         Paragraph("Keep it tiny", styles["table_cell"])],
        [Paragraph("Sunday weekly prep", styles["table_cell"]),
         Paragraph("Sunday reset checklist", styles["table_cell"]),
         Paragraph("your reset window hard stop", styles["table_cell"])],
        [Paragraph("Urge to add 4th database", styles["table_cell"]),
         Paragraph("Close Notion. Do one real task.", styles["table_cell"]),
         Paragraph("Now", styles["table_cell"])],
    ]
    table = Table(rows, colWidths=[2.0 * inch, 2.8 * inch, 1.7 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))

    section(story, styles, "WHEN TO USE WHAT — DECISION TABLE", [
        ("body", "If you're unsure where something goes, use this table. Wrong choice is fixable during Sunday reset."),
        ("table", table),
    ], page_break_after=True, ref=True)
    return story


def build_migration_checklist(styles):
    """Fresh-start migration from old Notion templates."""
    story = []
    section(story, styles, "MIGRATION CHECKLIST (FROM OLD TEMPLATES)", [
        ("body", "Do not migrate relations or dashboards. Quarantine and cherry-pick. Keep it short."),
        ("step", "[ ] Create [GRAVEYARD] Template Graveyard page"),
        ("step", "[ ] Drag old dashboards, habit trackers, PARA clones into graveyard"),
        ("step", "[ ] Collapse graveyard — do not open old pages during install week"),
        ("step", "[ ] Copy max 3 open loops into [BRAIN] Brain Dump (one line each)"),
        ("step", "[ ] Copy max 1 Next Action per real project into [PROJECTS] Projects"),
        ("step", "[ ] Do NOT import CSVs with 200 old tasks"),
        ("step", "[ ] Do NOT recreate Eisenhower matrix, mood log, or habit streak views"),
        ("step", "[ ] Set [HOME] Focus Dock as homepage before deleting bookmarks to old dashboards"),
        ("h2", "What to salvage vs leave behind"),
        ("body", "<b>Salvage:</b> Open tasks, project names, one-line next actions.<br/><b>Leave:</b> Relations, rollups, aesthetic layouts, archived 'someday' lists, broken streaks."),
        ("callout", ">> Fresh start beats perfect migration. Old system is quarantined, not deleted — you can retrieve later if needed."),
    ], ref=True)
    return story


def build_accountability_guide(styles):
    """External accountability without shame mechanics."""
    story = []
    section(story, styles, "ACCOUNTABILITY WITHOUT SHAME", [
        ("body", "ADHD brains respond to external structure, not internal guilt. Use these without streak counters."),
        ("h2", "Body doubling"),
        ("step", "• Video call or in-person: both work silently on one task"),
        ("step", "• No progress reports required — presence is the cue"),
        ("h2", "Text ping (not a streak)"),
        ("step", "• One message: 'Opened Focus Dock. Doing [task].'"),
        ("step", "• No reply needed. No daily obligation. Skip days without explanation."),
        ("h2", "Environmental cues"),
        ("step", "• Notion homepage = [HOME] Focus Dock (not sidebar)"),
        ("step", "• Phone: Notion widget or bookmark to Brain Dump only"),
        ("step", "• Desk: Part 15 emergency card taped at eye level"),
        ("h2", "What to avoid"),
        ("step", "• Habit streak apps tied to Focus Dock usage"),
        ("step", "• Public accountability threads where missed days = shame"),
        ("step", "• Reward systems that require perfect weeks"),
        ("callout", ">> One task completed beats seven days of dashboard tweaking. Measure completion, not opens."),
    ])
    return story


def build_sequence_worksheets(styles):
    """Compact worksheet table — all 5 sequences on one dense page."""
    story = []
    rows = [
        [
            Paragraph("<b>Sequence</b>", styles["table_header"]),
            Paragraph("<b>Steps (link each with Task Before)</b>", styles["table_header"]),
        ]
    ]
    for name, steps in SEQUENCE_WORKSHEETS:
        step_text = " · ".join(f"{i}. {s}" for i, s in enumerate(steps, 1))
        rows.append([
            Paragraph(f"<b>{name}</b>", styles["table_cell"]),
            Paragraph(step_text, styles["table_cell"]),
        ])

    table = Table(rows, colWidths=[1.1 * inch, 5.4 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))

    section(story, styles, "WORKSHEETS — BUILD YOUR SEQUENCES", [
        ("body", "Create in Today database. Link each step with Task Before. Only step 1 shows until step 1 is Done."),
        ("table", table),
    ], page_break_after=True)
    return story


def build_formula_reference(styles):
    """Full formula copy-paste reference page."""
    story = []
    section(story, styles, "FORMULA REFERENCE — COPY-PASTE", [
        ("body", "Create these as <b>Formula</b> properties in the [TODAY] Today database. Names must match exactly."),
        ("h2", "Hide Sequence (Formula checkbox)"),
        ("body", "Property name: <b>Hide Sequence</b> · Type: Formula · Return type: Checkbox"),
        ("body", "Paste this formula:"),
        ("formula", 'if(empty(prop("Task Before")), false, if(prop("Before Done") > 0, false, if(prop("Due") < prop("Before Due"), false, true)))'),
        ("body", "<b>What it does:</b> Returns true when a sequenced task should be hidden (predecessor not done, or due date conflict)."),
        ("h2", "Hide (Formula)"),
        ("body", "Property name: <b>Hide</b> · Type: Formula"),
        ("body", "Paste this formula:"),
        ("formula", 'prop("Hide Sequence")'),
        ("body", "<b>What it does:</b> Pass-through used by Do This Next view filter (Hide = unchecked)."),
        ("h2", "Required rollups (create before formulas)"),
        ("step", "• <b>Before Done</b> — Rollup on Task Before → property Done → Calculate: Count checked"),
        ("step", "• <b>Before Due</b> — Rollup on Task Before → property Due → Calculate: Latest date"),
        ("h2", "Do This Next view"),
        ("step", "• Filter: Hide is unchecked"),
        ("step", "• Filter: Done is unchecked"),
        ("step", "• Sort: Due ascending"),
        ("callout", ">> If too many tasks show: verify Hide Sequence formula exists and view filters Hide, not Hide Sequence directly."),
    ], page_break_after=True, ref=True)
    return story


def build_days_2_7_playbook(styles):
    """Dense day-by-day survival guide for first week after install."""
    story = []
    days = [
        ("Day 2", "Open [HOME] Focus Dock only. Complete one task. No new properties. Brain dump max 2 captures."),
        ("Day 3", "Same as Day 2. If task feels big, split into 3-step sequence. Do not add a 4th database."),
        ("Day 4", "Pull one item from Brain Dump to Today if Do This Next is empty. Still one visible task."),
        ("Day 5", "Midweek check: count Notion tabs open. Target = 1 (Focus Dock). Close the rest."),
        ("Day 6", "Optional: add one pre-built sequence from Part 10. Max one new sequence this week."),
        ("Day 7", "First Sunday reset. Stop even if messy."),
    ]
    rows = [
        [Paragraph("<b>Day</b>", styles["table_header"]),
         Paragraph("<b>Your only job</b>", styles["table_header"])],
    ]
    for day, job in days:
        rows.append([
            Paragraph(f"<b>{day}</b>", styles["table_cell"]),
            Paragraph(job, styles["table_cell"]),
        ])
    table = Table(rows, colWidths=[0.75 * inch, 5.75 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))

    section(story, styles, "DAYS 2–7 PLAYBOOK", [
        ("body", "Install day is Day 1. Days 2–7 are survival mode — no rebuilding, no tutorials, no new views."),
        ("table", table),
        ("callout", ">> Success metric: opened Focus Dock and finished one task. Notion time under minimal time/day."),
    ])
    return story


def _step_checklist_table(styles, steps_slice, header_label):
    """Build a dense two-column table for a slice of install steps."""
    rows = [
        [
            Paragraph(f"<b>{header_label}</b>", styles["table_header"]),
            Paragraph("<b>Action</b>", styles["table_header"]),
        ]
    ]
    for step_num, instruction in steps_slice:
        rows.append([
            Paragraph(f"<b>{step_num}</b>", styles["table_cell"]),
            Paragraph(instruction, styles["table_cell"]),
        ])

    table = Table(rows, colWidths=[0.55 * inch, 5.95 * inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("GRID", (0, 0), (-1, -1), 0.4, MID_TEXT),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ]))
    return table


def build_install_checklist(styles):
    """Dense 2-page install checklist."""
    story = []
    section(story, styles, "INSTALL CHECKLIST (PAGE 1 OF 2)", [
        ("body", "Steps 1–24. Follow in order during first install. If a step takes longer, keep going — do not add unlisted features."),
        ("callout", ">> Stuck? Skip aesthetics. Defaults are fine. Good enough beats perfect."),
        ("table", _step_checklist_table(styles, INSTALL_STEPS[:24], "Step")),
    ], page_break_after=True)

    section(story, styles, "INSTALL CHECKLIST (PAGE 2 OF 2)", [
        ("body", "Steps 25–48. Finish install, do one real task, close Notion."),
        ("table", _step_checklist_table(styles, INSTALL_STEPS[24:], "Step")),
        ("callout", ">> Done when: one task visible in Do This Next, one task marked Done, Notion closed."),
    ], page_break_after=True)
    return story


def main():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=MARGIN,
        bottomMargin=0.85 * inch,
        title="Focus Dock — ADHD Notion Recovery Guide",
        author="Focus Dock",
    )
    doc.current_lane = ""
    story = []
    story.extend(start_here_page(styles, doc))
    story.extend(build_content(styles, doc))
    doc.build(story, onFirstPage=draw_cover_page, onLaterPages=add_page_number)
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()