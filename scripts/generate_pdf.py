#!/usr/bin/env python3
"""Generate Focus Dock ADHD Notion Recovery Guide PDF."""

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

OUTPUT = "/Users/cameron/focus-dock/private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide.pdf"

# High-contrast ADHD-friendly palette
NAVY = colors.HexColor("#1a1f3d")
CORAL = colors.HexColor("#ff6b4a")
MINT = colors.HexColor("#3dd6c3")
YELLOW = colors.HexColor("#ffd93d")
WHITE = colors.white
LIGHT_BG = colors.HexColor("#f4f6fb")
DARK_TEXT = colors.HexColor("#1a1a2e")
MID_TEXT = colors.HexColor("#3d3d5c")


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
        "h1": ParagraphStyle(
            "h1",
            parent=base["Heading1"],
            fontSize=20,
            leading=24,
            textColor=NAVY,
            spaceBefore=16,
            spaceAfter=10,
            fontName="Helvetica-Bold",
            backColor=YELLOW,
            borderPadding=8,
        ),
        "h2": ParagraphStyle(
            "h2",
            parent=base["Heading2"],
            fontSize=15,
            leading=19,
            textColor=CORAL,
            spaceBefore=14,
            spaceAfter=8,
            fontName="Helvetica-Bold",
        ),
        "h3": ParagraphStyle(
            "h3",
            parent=base["Heading3"],
            fontSize=12,
            leading=15,
            textColor=NAVY,
            spaceBefore=10,
            spaceAfter=6,
            fontName="Helvetica-Bold",
        ),
        "body": ParagraphStyle(
            "body",
            parent=base["Normal"],
            fontSize=11,
            leading=16,
            textColor=DARK_TEXT,
            spaceAfter=10,
            fontName="Helvetica",
        ),
        "callout": ParagraphStyle(
            "callout",
            parent=base["Normal"],
            fontSize=11,
            leading=15,
            textColor=NAVY,
            backColor=LIGHT_BG,
            borderColor=CORAL,
            borderWidth=2,
            borderPadding=10,
            spaceBefore=8,
            spaceAfter=8,
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


def cover_page(styles):
    story = []
    story.append(Spacer(1, 1.2 * inch))
    story.append(
        Table(
            [[Paragraph("FOCUS DOCK", styles["title"])]],
            colWidths=[6.5 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("TOPPADDING", (0, 0), (-1, -1), 30),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
            ]),
        )
    )
    story.append(
        Table(
            [[Paragraph("The ADHD Notion Recovery Guide", styles["subtitle"])]],
            colWidths=[6.5 * inch],
            style=TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), NAVY),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 30),
            ]),
        )
    )
    story.append(Spacer(1, 0.4 * inch))
    bullets = [
        "47-minute anti-plansturbation protocol",
        "3 databases — not 14",
        "One visible next task at all times",
        "Task sequences for executive dysfunction",
        "Copy-paste Notion formulas included",
        "No streak shame · 11-min Sunday reset",
    ]
    for b in bullets:
        story.append(
            Paragraph(f"<font color='#1a1f3d'><b>[OK]</b></font>  {b}", styles["body"])
        )
    story.append(Spacer(1, 0.5 * inch))
    story.append(
        Paragraph(
            "<b>Stop building. Start doing.</b><br/>"
            "For adults with ADHD who've abandoned one too many Notion templates.",
            styles["callout"],
        )
    )
    story.append(Spacer(1, 0.3 * inch))
    story.append(
        Paragraph("Version 1.0 · July 2026 · getfocusdock.com", styles["footer"])
    )
    story.append(PageBreak())
    return story


def start_here_page(styles):
    """One-page START HERE / TOC with navigation hints."""
    story = []
    story.append(Paragraph("START HERE", styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=CORAL, spaceAfter=10))
    story.append(
        Paragraph(
            "Do not read cover-to-cover. Pick your lane, set a timer, and go.",
            styles["body"],
        )
    )
    story.append(Spacer(1, 8))

    rows = [
        [Paragraph("<b>Your goal</b>", styles["table_header"]),
         Paragraph("<b>Go to</b>", styles["table_header"]),
         Paragraph("<b>Page hint</b>", styles["table_header"])],
        [Paragraph("Install now (47 min)", styles["toc"]),
         Paragraph("Part 2 — 47-Minute Install", styles["toc"]),
         Paragraph("Start timer · follow steps in order", styles["toc"])],
        [Paragraph("Minute-by-minute checklist", styles["toc"]),
         Paragraph("Deep Dive — Install Checklist", styles["toc"]),
         Paragraph("Dense 2-page table · all 48 minutes", styles["toc"])],
        [Paragraph("Daily reference", styles["toc"]),
         Paragraph("Part 4 + Appendix A", styles["toc"]),
         Paragraph("3-minute workflow · quick lookup card", styles["toc"])],
        [Paragraph("Emergency / overwhelm", styles["toc"]),
         Paragraph("Part 6 + Part 15", styles["toc"]),
         Paragraph("Print Part 15 · tape to monitor", styles["toc"])],
        [Paragraph("Am I the right audience?", styles["toc"]),
         Paragraph("Part 8 — Self-Assessment", styles["toc"]),
         Paragraph("Read before Part 2 if unsure", styles["toc"])],
        [Paragraph("Troubleshooting", styles["toc"]),
         Paragraph("Appendix B + Part 13", styles["toc"]),
         Paragraph("When something breaks or you quit for a week", styles["toc"])],
    ]
    toc_table = Table(rows, colWidths=[1.6 * inch, 2.4 * inch, 2.5 * inch])
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
    story.append(Spacer(1, 14))
    story.append(
        Paragraph(
            ">> <b>Default path:</b> Self-Assessment (2 min) → Part 2 install (47 min) "
            "→ do the one visible task → close Notion.",
            styles["callout"],
        )
    )
    story.append(PageBreak())
    return story


def section(story, styles, title, blocks, page_break_after=False):
    story.append(Paragraph(title, styles["h1"]))
    story.append(HRFlowable(width="100%", thickness=2, color=CORAL, spaceAfter=10))
    for kind, text in blocks:
        if kind == "break":
            story.append(PageBreak())
        elif kind == "h2":
            story.append(Paragraph(text, styles["h2"]))
        elif kind == "h3":
            story.append(Paragraph(text, styles["h3"]))
        elif kind == "callout":
            story.append(Paragraph(text, styles["callout"]))
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
    story.append(Spacer(1, 8))
    if page_break_after:
        story.append(PageBreak())


def self_assessment_section(styles):
    return [
        ("body", "Answer honestly. No judgment — this determines if Focus Dock is right for you."),
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
        ("callout", "3+ checkmarks in 'need this'? Start the 47-minute timer now."),
    ]


def build_content(styles):
    story = []

    section(story, styles, "HOW TO USE THIS GUIDE", [
        ("body", "This is not a template to admire. It is a <b>recovery protocol</b>. Set a 47-minute timer. Follow the steps in order. Do not customize colors until Day 8."),
        ("callout", ">> RULE ZERO: If you feel the urge to add a 4th database, close Notion and do one real task instead. That urge is plansturbation."),
        ("h2", "What you need"),
        ("step", "• Notion account (free tier works)"),
        ("step", "• 47 uninterrupted minutes (phone in another room)"),
        ("step", "• Permission to delete your old ADHD template graveyard"),
        ("h2", "What you'll build"),
        ("body", "<b>Database 1 — [BRAIN] Brain Dump:</b> 2-second capture. No tags, no projects, no guilt."),
        ("body", "<b>Database 2 — [TODAY] Today:</b> ONE visible next action. Task sequences hide future steps."),
        ("body", "<b>Database 3 — [PROJECTS] Projects:</b> Parking lot for someday. You visit weekly, not daily."),
        ("body", "<b>[HOME] Home Screen:</b> Single page. No sidebar maze. Open → see next task → do it."),
    ])

    section(story, styles, "PART 8 — SELF-ASSESSMENT (READ FIRST)", self_assessment_section(styles))

    section(story, styles, "PART 1 — WHY YOUR OLD SYSTEM FAILED", [
        ("body", "You are not lazy. Your old system was designed to produce screenshots, not completed tasks. Three predictable failure modes:"),
        ("h2", "1. Dopamine spent on setup"),
        ("body", "Customizing Notion releases dopamine: colors, icons, new views. Your ADHD brain prefers that over taxes, email, or laundry. By Saturday night the dopamine budget is empty."),
        ("h2", "2. Choice overload"),
        ("body", "Typical ADHD templates: Projects + Areas + Resources + Habits + Mood + Journal + Finance. Each opening = 12 micro-decisions. Research shows more options → less action. Your working memory is already taxed."),
        ("h2", "3. Streak shame"),
        ("body", "Miss one habit day → broken streak → dashboard becomes evidence of failure → you close the tab. ADHD brains avoid shame triggers aggressively."),
        ("callout", "The Focus Dock fix: Low setup cost. Low decision density. No visible state that punishes missed days."),
    ])

    section(story, styles, "PART 2 — THE 47-MINUTE INSTALL", [
        ("h2", "Minutes 0–5: Nuclear option (delete the graveyard)"),
        ("step", "1. Open Notion sidebar. Count your productivity-related pages."),
        ("step", "2. If more than 5: create page titled <b>[GRAVEYARD] Template Graveyard</b>."),
        ("step", "3. Drag every abandoned dashboard, habit tracker, and PARA clone into it. Do not open them."),
        ("step", "4. Collapse the graveyard. You are not deleting — you're quarantining shame."),
        ("h2", "Minutes 5–15: Create Database 1 — [BRAIN] Brain Dump"),
        ("step", "1. New page: <b>[BRAIN] Brain Dump</b> → type /table → Full page database."),
        ("step", "2. Rename default title property to <b>Thought</b>."),
        ("step", "3. Add property: <b>Captured</b> (Created time — auto)."),
        ("step", "4. Add property: <b>Processed?</b> (Checkbox)."),
        ("step", "5. Delete every other property. Yes, all of them."),
        ("step", "6. Create view <b>Inbox</b>: filter Processed? is unchecked. Sort: Captured ascending."),
        ("callout", "Usage rule: Capture in 2 seconds. Thought only. No tags. Process during Sunday reset or when Today is empty."),
        ("h2", "Minutes 15–30: Create Database 2 — [TODAY] Today"),
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
        ("h2", "Minutes 30–40: Create Database 3 — [PROJECTS] Projects"),
        ("step", "1. New page: <b>[PROJECTS] Projects</b> → /table → Full page database."),
        ("step", "2. Properties: <b>Name</b> (Title), <b>Status</b> (Select: [IDEA] Idea / [ACTIVE] Active / [LOW] Paused / [DONE] Done), <b>Next Action</b> (Text)."),
        ("step", "3. View <b>Active</b>: Status = Active. Sort: manual (drag what matters to top)."),
        ("body", "You do NOT work from this database daily. During Sunday reset, pick one Next Action and move it to Today."),
        ("h2", "Minutes 40–47: Build [HOME] Home Screen"),
        ("step", "1. New page: <b>[HOME] Focus Dock</b> (make this your Notion home)."),
        ("step", "2. Add heading: <b>Right now:</b>"),
        ("step", "3. Type /linked → link <b>Do This Next</b> view from Today (embedded, not full database)."),
        ("step", "4. Add heading: <b>Brain dump (2 sec):</b> → /linked → Brain Dump Inbox view."),
        ("step", "5. Add toggle: <b>Projects (Sunday only)</b> → link Active view."),
        ("step", "6. Settings → set <b>[HOME] Focus Dock</b> as homepage."),
        ("callout", "Done. Close Notion. Do the one visible task. Timer stops. You win."),
    ], page_break_after=True)

    section(story, styles, "PART 3 — TASK SEQUENCES (EXECUTIVE DYSFUNCTION)", [
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
    ], page_break_after=True)

    section(story, styles, "PART 4 — DAILY WORKFLOW (3 MINUTES)", [
        ("h2", "Morning (90 seconds)"),
        ("step", "1. Open [HOME] Focus Dock."),
        ("step", "2. Read the one task in Do This Next."),
        ("step", "3. Do it before opening email, Slack, or TikTok."),
        ("h2", "During the day (30 seconds each)"),
        ("step", "• Intrusive thought? → Brain Dump. One line. Close."),
        ("step", "• Finished task? → Check Done. Next sequence step appears automatically."),
        ("h2", "Evening (60 seconds)"),
        ("step", "• If Today is empty: pull ONE task from Brain Dump or Projects."),
        ("step", "• Do NOT rebuild your dashboard. Do NOT add properties. Go to bed."),
        ("callout", "If you did nothing else today but open Focus Dock once and complete one task: <b>system success.</b>"),
    ])

    section(story, styles, "PART 5 — 11-MINUTE SUNDAY RESET", [
        ("body", "No 45-minute weekly review. No streak accounting. Eleven minutes, timer visible."),
        ("h2", "Minutes 0–3: Brain Dump triage"),
        ("step", "• Open Inbox. For each item: delete, move to Today, or move to Projects Next Action."),
        ("step", "• Check Processed? on handled items."),
        ("h2", "Minutes 3–7: Today prep"),
        ("step", "• Clear Done tasks (archive or delete — your choice)."),
        ("step", "• Ensure 3–5 tasks max for the week, sequenced where needed."),
        ("step", "• Pick Monday's first task. Set Due = Monday."),
        ("h2", "Minutes 7–11: Projects glance"),
        ("step", "• Open Active projects. Max 3 Active at once. Pause the rest."),
        ("step", "• Update one Next Action per active project."),
        ("callout", "Stop at 11 minutes even if unfinished. Consistency beats completeness."),
    ])

    section(story, styles, "PART 6 — EMERGENCY OVERWHELM PROTOCOL", [
        ("body", "For days when everything feels loud. Print Part 15. Tape it to your monitor."),
        ("callout", "[ALERT] OVERWHELM MODE — Do only these 4 steps:"),
        ("step", "1. <b>Box breathing:</b> 4 sec in, 4 hold, 4 out. Twice."),
        ("step", "2. <b>Brain dump 3 words</b> — not sentences. What's loudest?"),
        ("step", "3. <b>Shrink to 2-minute version:</b> 'Clean kitchen' → 'put 3 dishes in sink.'"),
        ("step", "4. <b>Do the 2-minute version.</b> Mark done. Stop. You survived."),
        ("body", "Do NOT: reorganize Notion, watch setup videos, download a new template, or redesign colors. That is the trap."),
        ("h2", "When to skip Notion entirely"),
        ("body", "If you haven't opened Focus Dock in 5+ days: use a sticky note for one task. Return to Notion only when the sticky works for 2 days straight."),
    ], page_break_after=True)

    section(story, styles, "PART 7 — MAINTENANCE RULES (ANTI-PLANSTURBATION)", [
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
    ])

    section(story, styles, "APPENDIX A — QUICK REFERENCE CARD", [
        ("body", "<b>Capture:</b> Brain Dump → Thought → close (2 sec)"),
        ("body", "<b>Work:</b> [HOME] Focus Dock → Do This Next → one task"),
        ("body", "<b>Sequence:</b> Task Before relation + Hide Sequence formula"),
        ("body", "<b>Weekly:</b> 11-min Sunday reset"),
        ("body", "<b>Emergency:</b> 2-minute shrink → do → stop"),
        ("body", "<b>Homepage:</b> [HOME] Focus Dock (not sidebar maze)"),
    ])

    section(story, styles, "APPENDIX B — TROUBLESHOOTING", [
        ("h2", "I keep customizing instead of doing"),
        ("body", "Set a 'build budget': 0 minutes on weekdays. Customization is Sunday minutes 10–11 only."),
        ("h2", "Too many tasks visible"),
        ("body", "Check Hide formula is applied. Filter Do This Next: Hide = unchecked."),
        ("h2", "Sequences not hiding"),
        ("body", "Confirm Task Before is two-way relation. Before Done rollup must count checked boxes."),
        ("h2", "I abandoned it for a week"),
        ("body", "No guilt dashboard. Delete done tasks, pull ONE from Brain Dump, continue. Streaks don't exist here."),
        ("h2", "Want more structure"),
        ("body", "Read that again. Wanting more structure is often plansturbation wearing a productivity costume. Stay at 3 databases for 30 days first."),
        ("h2", "Hide Sequence always shows true / everything hidden"),
        ("body", "Check Before Done rollup counts <i>checked</i> boxes on Task Before. Verify Task Before relation points to the correct prior step."),
        ("h2", "Do This Next is empty but I have tasks"),
        ("body", "Uncheck Done on active tasks. Confirm Due dates exist. If using sequences, ensure step 1 has no Task Before link."),
        ("h2", "Brain Dump inbox never empties"),
        ("body", "Normal. Inbox is capture, not completion. Process during Sunday reset only — max 11 minutes."),
        ("h2", "I added a 4th database"),
        ("body", "Delete it today. Move any useful items to Brain Dump or Projects. Do not migrate relations."),
    ], page_break_after=True)

    section(story, styles, "PART 9 — WHAT TO DELETE FROM OLD TEMPLATES", [
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
    ])

    section(story, styles, "PART 10 — TASK SEQUENCE LIBRARY", [
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
        ("h2", "[CLEAN] 10-minute room rescue"),
        ("step", "1. Trash bag in hand → 2. Pick up 5 items → 3. Put away 3 items → 4. Clear one surface → 5. Stop (timer done)"),
        ("callout", "Pre-build sequences on a good day. Reuse forever. This is your dopamine investment — not color palettes."),
    ])

    story.extend(build_sequence_worksheets(styles))

    section(story, styles, "PART 11 — WEEK 1–4 ROLLOUT", [
        ("h2", "Week 1: Survival mode"),
        ("step", "• Day 1: Install only. No customization."),
        ("step", "• Days 2–7: One task per day minimum. Brain dump only when intrusive."),
        ("step", "• Banned: adding properties, new views, watching Notion tutorials"),
        ("h2", "Week 2: Add sequences"),
        ("step", "• Pick your most-delayed task. Break into sequence."),
        ("step", "• Add 2nd sequence only after first works 3 times"),
        ("h2", "Week 3: Sunday reset habit"),
        ("step", "• First 11-minute reset. Timer visible. Stop at 11 even if messy."),
        ("step", "• If you skip: no catch-up. Next Sunday, fresh start."),
        ("h2", "Week 4: Evaluate"),
        ("body", "Ask: Am I opening Focus Dock without dread? If yes: success. If no: delete one more feature."),
        ("callout", "The 3-week test from research: systems that survive 21 days become automatic. You're building automatic."),
    ])

    section(story, styles, "PART 12 — PROPERTY REFERENCE CARD", [
        ("h2", "Brain Dump database"),
        ("body", "• <b>Thought</b> (Title) — the capture<br/>• <b>Captured</b> (Created time)<br/>• <b>Processed?</b> (Checkbox)"),
        ("h2", "Today database"),
        ("body", "• <b>Task</b> (Title)<br/>• <b>Done</b> (Checkbox)<br/>• <b>Due</b> (Date)<br/>• <b>Energy</b> (Select: High/Medium/Low)<br/>• <b>Task Before</b> (Relation → Today)<br/>• <b>Task After</b> (Relation → Today)<br/>• <b>Before Done</b> (Rollup: count checked)<br/>• <b>Before Due</b> (Rollup: latest date)<br/>• <b>Hide Sequence</b> (Formula)<br/>• <b>Hide</b> (Formula)"),
        ("h2", "Projects database"),
        ("body", "• <b>Name</b> (Title)<br/>• <b>Status</b> (Select: Idea/Active/Paused/Done)<br/>• <b>Next Action</b> (Text)"),
        ("h2", "Do This Next view filters"),
        ("body", "Filter 1: Hide = unchecked<br/>Filter 2: Done = unchecked<br/>Sort: Due ascending"),
    ])

    section(story, styles, "PART 13 — COMMON MISTAKES", [
        ("h2", "Mistake 1: Adding a 4th database"),
        ("body", "Fix: Delete it. You don't need a 'Someday/Maybe' or 'Reading List.' Brain Dump handles capture."),
        ("h2", "Mistake 2: Showing all tasks, not one"),
        ("body", "Fix: Check Hide formula. Gallery view with 1 card. Or table view sorted with only top row visible."),
        ("h2", "Mistake 3: Skipping Brain Dump"),
        ("body", "Fix: Intrusive thoughts will hijack focus. 2-second capture prevents 'I'll remember' lies."),
        ("h2", "Mistake 4: Sunday reset becomes 45 minutes"),
        ("body", "Fix: Hard stop at 11 min. Incomplete reset beats skipped reset."),
        ("h2", "Mistake 5: Rebuilding instead of using"),
        ("body", "Fix: If you haven't done a task today but you've opened Notion, close it. Plansturbation detected."),
        ("h2", "Mistake 6: Energy tags become a project"),
        ("body", "Fix: Energy is optional. Ignore it if choosing energy level causes decisions."),
    ])

    section(story, styles, "PART 14 — ENERGY MATCHING (OPTIONAL)", [
        ("body", "Only use Energy tags if they help, not if choosing one causes paralysis."),
        ("h2", "[HIGH] High energy"),
        ("body", "Creative work, hard conversations, complex sequences, starting new projects."),
        ("h2", "[MED] Medium energy"),
        ("body", "Email, errands, admin, routine chores, continuing in-progress work."),
        ("h2", "[LOW] Low energy"),
        ("body", "Brain dump triage, 2-minute tasks, reading one paragraph, putting one item away."),
        ("callout", "On low days: filter Do This Next by Low energy OR ignore filter and do the smallest visible task."),
    ])

    section(story, styles, "PART 15A — SUNDAY RESET CHECKLIST (PRINTABLE)", [
        ("body", "Print this page. Check boxes with pen during your 11-minute reset. Stop when timer rings."),
        ("step", "[ ] Open [BRAIN] Brain Dump Inbox — triage each item (delete / Today / Projects)"),
        ("step", "[ ] Mark Processed? on handled Brain Dump items"),
        ("step", "[ ] Archive or delete completed Today tasks"),
        ("step", "[ ] Today has 3–5 tasks max for the coming week"),
        ("step", "[ ] Monday's first task has Due = Monday"),
        ("step", "[ ] Max 3 [PROJECTS] Active — pause the rest"),
        ("step", "[ ] Each Active project has one Next Action written"),
        ("step", "[ ] Did NOT add properties, views, or databases"),
        ("step", "[ ] Timer stopped at 11 minutes (even if unfinished)"),
        ("callout", ">> Incomplete reset beats skipped reset. Same time next Sunday — no catch-up guilt."),
    ], page_break_after=True)

    section(story, styles, "PART 15 — PRINTABLE EMERGENCY CARD", [
        ("callout", "[CUT] CUT HERE — TAPE TO MONITOR [CUT]"),
        ("h2", "[ALERT] OVERWHELM MODE"),
        ("step", "1. Box breathe: 4 in, 4 hold, 4 out × 2"),
        ("step", "2. Brain dump 3 WORDS (not sentences)"),
        ("step", "3. Shrink to 2-MINUTE version"),
        ("step", "4. Do it. Mark done. STOP."),
        ("body", "<b>DO NOT:</b> Open Notion · Download templates · Reorganize · Watch setup videos"),
        ("body", "<b>IF 5+ DAYS AWAY:</b> Sticky note with ONE task. Return when sticky works 2 days."),
        ("callout", "You are not behind. You are not broken. One task is enough."),
    ], page_break_after=True)

    section(story, styles, "PART 16 — FAQ", [
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
    ])

    section(story, styles, "PART 17 — GLOSSARY", [
        ("body", "<b>Plansturbation:</b> Building productivity systems instead of doing productive work."),
        ("body", "<b>Task sequence:</b> Linked sub-tasks where only the next step is visible."),
        ("body", "<b>Brain dump:</b> Frictionless capture inbox with no organization required."),
        ("body", "<b>Choice overload:</b> Too many options → paralysis → no action."),
        ("body", "<b>Executive dysfunction:</b> Knowing what to do but unable to initiate at the moment."),
        ("body", "<b>Template graveyard:</b> Collection of abandoned Notion setups you avoid opening."),
        ("body", "<b>Visible state:</b> Dashboard elements that break or look bad when not maintained."),
    ])

    section(story, styles, "PART 18 — RESEARCH NOTES", [
        ("body", "Focus Dock design is informed by:"),
        ("step", "• Iyengar & Lepper (2000) — choice overload reduces action"),
        ("step", "• Volkow et al. (2009) — ADHD dopamine pathway differences"),
        ("step", "• Barkley (2012) — executive function as performance disorder"),
        ("step", "• Tuckman — externalize executive function to environment"),
        ("step", "• Lived experience: plansturbation threads in r/Notion and r/ADHD"),
        ("body", "This guide externalizes 'what's next' so your brain doesn't have to hold it."),
    ], page_break_after=True)

    story.extend(build_brain_dump_guide(styles))
    story.extend(build_notion_ui_map(styles))
    story.extend(build_formula_reference(styles))
    story.extend(build_install_checklist(styles))
    story.extend(build_days_2_7_playbook(styles))
    story.extend(build_accountability_guide(styles))
    story.extend(build_plansturbation_red_flags(styles))
    story.extend(build_migration_checklist(styles))
    story.extend(build_when_to_use_what(styles))

    section(story, styles, "APPENDIX C — YOU MADE IT", [
        ("body", "If you're reading this, you built something most ADHD adults never finish: a system they actually use."),
        ("body", "Focus Dock isn't about perfect Notion. It's about <b>one visible next step</b> when your brain feels like static."),
        ("callout", "Questions? hello@getfocusdock.com · 14-day refund if it doesn't help — no guilt, same as the system."),
        ("body", "Now close this PDF and do the one task. [HOME]"),
    ])

    return story


INSTALL_MINUTES = [
    ("0", "Start 47-minute timer. Phone in another room. Open Notion desktop or browser only."),
    ("1", "Sidebar audit: count productivity pages. If 5+, create [GRAVEYARD] Template Graveyard page."),
    ("2", "Drag abandoned dashboards into graveyard. Do NOT open them. Collapse graveyard."),
    ("3", "Create new page: [BRAIN] Brain Dump. Type /table → Full page database."),
    ("4", "Rename title column to Thought. Delete all other default properties."),
    ("5", "Add Captured (Created time). Add Processed? (Checkbox). Save."),
    ("6", "Create Inbox view. Filter: Processed? unchecked. Sort: Captured ascending."),
    ("7", "Test capture: add 'test thought'. Confirm it appears in Inbox. Delete test."),
    ("8", "Create page [TODAY] Today. /table → Full page database."),
    ("9", "Add Task (title), Done (checkbox), Due (date), Energy (select)."),
    ("10", "Energy options: [HIGH] High, [MED] Medium, [LOW] Low. Save."),
    ("11", "Add Task Before relation to Today (two-way). Auto-creates Task After."),
    ("12", "Add Before Done rollup: Task Before → Done → Count checked."),
    ("13", "Add Before Due rollup: Task Before → Due → Latest date."),
    ("14", "Add Hide Sequence formula property (see Part 2 for formula)."),
    ("15", "Add Hide formula: prop(\"Hide Sequence\")."),
    ("16", "Create Do This Next view. Filter Hide unchecked, Done unchecked."),
    ("17", "Sort Do This Next by Due ascending. This is your daily driver."),
    ("18", "Add one test task 'Put 3 dishes in sink'. Confirm it shows in Do This Next."),
    ("19", "Create page [PROJECTS] Projects. /table → Full page database."),
    ("20", "Add Name, Status (Idea/Active/Paused/Done), Next Action (text)."),
    ("21", "Create Active view: Status = Active. Manual sort enabled."),
    ("22", "Add one project with Next Action text only. Do not add tasks here yet."),
    ("23", "Create page [HOME] Focus Dock. This becomes your home."),
    ("24", "Add heading: Right now. Embed linked Do This Next view from Today."),
    ("25", "Add heading: Brain dump. Embed linked Inbox view from Brain Dump."),
    ("26", "Add toggle: Projects (Sunday only). Embed Active view inside."),
    ("27", "Settings → set homepage to [HOME] Focus Dock."),
    ("28", "Close every other Notion tab. Only Focus Dock remains."),
    ("29", "Add first real task to Today. Not a test — something you've avoided."),
    ("30", "If task is big: stop. Break into 3-step sequence with Task Before links."),
    ("31", "Verify only step 1 visible in Do This Next. Steps 2-3 hidden."),
    ("32", "Move 3 Brain Dump items from old notes if any. Max 3. Check Processed."),
    ("33", "Review Projects: max 1 Active. Pause others."),
    ("34", "Delete any extra views you created during setup. Keep only essentials."),
    ("35", "Do NOT change colors, icons, or covers. Aesthetic = plansturbation bait."),
    ("36", "Read Emergency Overwhelm Card (Part 6). Bookmark mentally."),
    ("37", "Screenshot Focus Dock home for accountability. Do not post — private record."),
    ("38", "Write on paper: 'One task is enough.' Tape near desk."),
    ("39", "Calendar: recurring Sunday 11-min reset reminder."),
    ("40", "Do the one visible task NOW before closing guide."),
    ("41", "Mark Done. Watch next sequence step appear (if applicable)."),
    ("42", "If no next step: pull one item from Brain Dump to Today."),
    ("43", "Close Notion. Do not reopen until tomorrow morning."),
    ("44", "Journal one sentence: what made starting hard today?"),
    ("45", "Put guide PDF in easy-to-find folder. Name: Focus Dock Recovery."),
    ("46", "Text accountability buddy: 'Installed Focus Dock. One task done.'"),
    ("47", "Stop timer. You recovered. The graveyard can wait."),
]


SEQUENCE_WORKSHEETS = [
    ("GROCERIES", ["Check fridge", "Write 5-item list max", "Grab bags", "Drive/walk", "Buy only list items", "Unload 3 items"]),
    ("SHOWER", ["Get towel", "Get clean clothes", "Start water", "Shower", "Dry off", "Dress", "Hang towel"]),
    ("TAXES", ["Find login", "Download one form", "Fill name/address", "One deduction section", "Save draft", "Schedule finish date"]),
    ("CALL MOM", ["Write 2 topics", "Find quiet spot", "Dial", "Talk 10 min max", "Set next call date"]),
    ("WORKOUT", ["Put on shoes", "Fill water", "5-min warmup", "Main exercise 10 min", "Cooldown", "Shower after"]),
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
        ("step", "• Do not process more than 11 minutes total"),
        ("h2", "When to capture (2 seconds)"),
        ("step", "• Intrusive thought during focused work"),
        ("step", "• 'I'll remember this' lie detected"),
        ("step", "• Partner asks you to do something while you're busy"),
        ("callout", ">> Capture is not commitment. Processing is not urgent. Today is the only daily driver."),
    ], page_break_after=True)
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
    ], page_break_after=True)
    return story


def build_plansturbation_red_flags(styles):
    """Recognize rebuild urges before they eat the day."""
    story = []
    flags = [
        ("New database idea", "You 'just need' a Reading List or Habits db. Use Brain Dump or Projects instead."),
        ("Color/icon session", "30+ minutes on aesthetics, zero tasks completed. Close Notion."),
        ("Tutorial spiral", "Watching 'ultimate Notion setup' videos during install week. Banned until Day 30."),
        ("Filter rabbit hole", "Adding 4th filter to Do This Next. Max one optional filter after Day 8."),
        ("Migration fantasy", "Planning to merge old PARA system into Focus Dock. Quarantine old system instead."),
        ("Weekly review creep", "Sunday reset hits 25 minutes. Hard stop at 11 — set timer visible."),
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

    section(story, styles, "PLANSTURBATION RED FLAGS", [
        ("body", "Catch these urges early. Each one feels productive. None complete tasks."),
        ("table", table),
        ("callout", ">> Ask: 'Will this help me see ONE next task tomorrow?' If no, don't do it."),
    ], page_break_after=True)
    return story


def build_when_to_use_what(styles):
    """Decision tree — which database for which moment."""
    story = []
    rows = [
        [Paragraph("<b>Situation</b>", styles["table_header"]),
         Paragraph("<b>Use this</b>", styles["table_header"]),
         Paragraph("<b>Time budget</b>", styles["table_header"])],
        [Paragraph("Random thought while working", styles["table_cell"]),
         Paragraph("[BRAIN] Brain Dump — one line, close", styles["table_cell"]),
         Paragraph("2 seconds", styles["table_cell"])],
        [Paragraph("What should I do right now?", styles["table_cell"]),
         Paragraph("[HOME] Focus Dock — Do This Next view", styles["table_cell"]),
         Paragraph("90 seconds", styles["table_cell"])],
        [Paragraph("Big project with many steps", styles["table_cell"]),
         Paragraph("[TODAY] Today — break into sequence", styles["table_cell"]),
         Paragraph("5 min setup, then 1 step/day", styles["table_cell"])],
        [Paragraph("Someday idea, not this week", styles["table_cell"]),
         Paragraph("[PROJECTS] Projects — Idea status", styles["table_cell"]),
         Paragraph("Sunday reset only", styles["table_cell"])],
        [Paragraph("Overwhelmed, can't start", styles["table_cell"]),
         Paragraph("Part 15 emergency card — 2-min shrink", styles["table_cell"]),
         Paragraph("4 minutes max", styles["table_cell"])],
        [Paragraph("Sunday weekly prep", styles["table_cell"]),
         Paragraph("Part 15A checklist — 11 min timer", styles["table_cell"]),
         Paragraph("11 minutes hard stop", styles["table_cell"])],
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
    ], page_break_after=True)
    return story


def build_migration_checklist(styles):
    """Fresh-start migration from old Notion templates."""
    story = []
    section(story, styles, "MIGRATION CHECKLIST (FROM OLD TEMPLATES)", [
        ("body", "Do not migrate relations or dashboards. Quarantine and cherry-pick. Timer: 15 minutes max."),
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
    ])
    return story


def build_accountability_guide(styles):
    """External accountability without shame mechanics."""
    story = []
    section(story, styles, "ACCOUNTABILITY WITHOUT SHAME", [
        ("body", "ADHD brains respond to external structure, not internal guilt. Use these without streak counters."),
        ("h2", "Body doubling (5 minutes)"),
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
    ], page_break_after=True)
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
        ("Day 7", "First Sunday reset (11 min). Timer visible. Stop at 11 even if messy."),
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
        ("callout", ">> Success metric: opened Focus Dock and finished one task. Notion time under 5 minutes/day."),
    ])
    return story


def _minute_checklist_table(styles, minutes_slice, header_label):
    """Build a dense two-column table for a slice of install minutes."""
    rows = [
        [
            Paragraph(f"<b>{header_label}</b>", styles["table_header"]),
            Paragraph("<b>Action</b>", styles["table_header"]),
        ]
    ]
    for minute, instruction in minutes_slice:
        rows.append([
            Paragraph(f"<b>{minute}</b>", styles["table_cell"]),
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
    """Dense 2-page checklist replacing 48 one-minute-per-page sections."""
    story = []
    section(story, styles, "DEEP DIVE — 47-MINUTE INSTALL CHECKLIST (PAGE 1 OF 2)", [
        ("body", "Minutes 0–23. Follow in order during first install. If a step takes longer, keep going — do not add unlisted features."),
        ("callout", ">> Stuck? Skip aesthetics. Defaults are fine. Good enough beats perfect."),
        ("table", _minute_checklist_table(styles, INSTALL_MINUTES[:24], "Min")),
    ], page_break_after=True)

    section(story, styles, "DEEP DIVE — 47-MINUTE INSTALL CHECKLIST (PAGE 2 OF 2)", [
        ("body", "Minutes 24–47. Finish install, do one real task, close Notion."),
        ("table", _minute_checklist_table(styles, INSTALL_MINUTES[24:], "Min")),
        ("callout", ">> Done when: one task visible in Do This Next, one task marked Done, Notion closed."),
    ], page_break_after=True)
    return story


def add_page_number(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MID_TEXT)
    canvas.drawString(inch, 0.5 * inch, "Focus Dock · getfocusdock.com")
    canvas.drawRightString(letter[0] - inch, 0.5 * inch, f"Page {doc.page}")
    canvas.restoreState()


def main():
    styles = build_styles()
    doc = SimpleDocTemplate(
        OUTPUT,
        pagesize=letter,
        leftMargin=0.75 * inch,
        rightMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="Focus Dock — ADHD Notion Recovery Guide",
        author="Focus Dock",
    )
    story = []
    story.extend(cover_page(styles))
    story.extend(start_here_page(styles))
    story.extend(build_content(styles))
    doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)
    print(f"Generated: {OUTPUT}")


if __name__ == "__main__":
    main()