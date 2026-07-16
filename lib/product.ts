export const BRAND = {
  name: "Focus Dock",
  tagline: "Stop the setup spiral. Start doing.",
  domain: "getfocusdock.com",
} as const;

export const SUMMER_DEAL = {
  active: true,
  label: "SUMMER SALE",
  headline: "Recovery guide summer sale",
  // Rolling countdown: restarts every `cycleDays` from the anchor, so the
  // banner never expires or disappears on its own.
  cycleAnchor: "2026-07-16T00:00:00-04:00",
  cycleDays: 7,
  badge: "Summer sale — $27",
} as const;

export const PRODUCT = {
  id: "adhd-notion-recovery",
  name: "ADHD Notion Recovery Guide",
  fullName: "Focus Dock — ADHD Notion Recovery Guide",
  description:
    "A 43-page PDF protocol for ADHD adults who've abandoned too many Notion templates — install a minimal 3-database system in one sitting, with copy-paste formulas, task sequences, and a short Sunday reset.",
  price: 27,
  compareAt: 49,
  currency: "usd",
  pages: 43,
  fileName: "Focus_Dock_ADHD_Notion_Recovery_Guide_v2.pdf",
  fileLabel: "PDF Guide",
  formulasFileName: "Focus_Dock_Formulas.txt",
} as const;

export const HERO = {
  headline: "You didn't fail Notion. Notion failed your brain.",
  subheadline:
    "Focus Dock is a 43-page recovery protocol — not another template. Install a minimal 3-database system in one sitting and see exactly one next task, every time you open Notion.",
  trustBar: ["Secure Stripe checkout", "Instant PDF download", "14-day guarantee"],
} as const;

export const STATS = [
  { value: "43", label: "pages, zero fluff" },
  { value: "3", label: "databases — not 14" },
  { value: "1", label: "sitting to install" },
  { value: "16", label: "part reference (R-1 to R-16)" },
] as const;

export const PACKAGE_ITEMS = [
  {
    num: "01",
    title: "Install Protocol",
    description:
      "Five timed steps with a 48-point checklist: Brain Dump, Today, and Projects databases — exact property names, exact clicks, zero fluff.",
    accent: "navy",
  },
  {
    num: "02",
    title: "Task Sequence System",
    description:
      "Copy-paste formulas and rollups that hide every step except the next one — plus an 11-sequence library (laundry, taxes, email boss…).",
    accent: "coral",
  },
  {
    num: "03",
    title: "Daily Workflow",
    description:
      "A 3-minute morning/evening rhythm designed for ADHD brains that hate maintenance.",
    accent: "mint",
  },
  {
    num: "04",
    title: "Sunday Reset",
    description:
      "A ~10-minute weekly triage with a hard stop at 15 — no guilt dashboards, no streaks, no marathon reviews.",
    accent: "amber",
  },
  {
    num: "05",
    title: "Printable Cards + Reference",
    description:
      "A printable emergency overwhelm card, a printable Sunday reset checklist, and a 16-part lookup section for when anything breaks.",
    accent: "navy",
  },
] as const;

export const FAQ_ITEMS = [
  {
    q: "How is this different from the templates I already bought?",
    a: "It's the opposite of one. Templates hand you 14 databases to maintain; Focus Dock is a protocol you follow once — you build 3 databases yourself in one sitting, so you understand every piece and there's nothing to abandon. No template file, no duplicating someone else's workspace.",
  },
  {
    q: "I've tried Notion and quit. Twice. Will this actually stick?",
    a: "This guide exists specifically for the template-graveyard crowd. It attacks the three reasons ADHD brains abandon Notion — setup spirals, choice overload, and streak shame — and it starts with a 5-minute win before you build anything.",
  },
  {
    q: "How long does setup actually take?",
    a: "One sitting, about 45–60 minutes, with a step-by-step checklist and time estimates on every step. You finish the session by completing one real task, not by admiring a dashboard.",
  },
  {
    q: "What if I'm not technical?",
    a: "Every step names the exact button, menu, and property. The two formulas are copy-paste — the guide even includes a Notion UI map so you never have to watch a tutorial video.",
  },
  {
    q: "Is this a Notion template file or a PDF?",
    a: "A PDF guide (43 pages) plus a copy-paste formulas file. You build the system inside your own Notion workspace — the free plan is enough.",
  },
  {
    q: "How fast do I get access?",
    a: "Instantly after checkout. You'll land on a download page and can save the PDF immediately.",
  },
  {
    q: "What if it doesn't help?",
    a: "Email us within 14 days for a full refund. No hoops, no guilt — same energy as the system itself.",
  },
  {
    q: "What if I have questions after buying?",
    a: "Email support and a human answers. The guide also ships with a 16-part reference section (troubleshooting, formulas, FAQ) that covers nearly everything readers ask.",
  },
] as const;
