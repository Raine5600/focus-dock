export const BRAND = {
  name: "Focus Dock",
  tagline: "Stop the setup spiral. Start doing.",
  domain: "getfocusdock.com",
} as const;

export const SUMMER_DEAL = {
  active: true,
  label: "SUMMER SALE",
  headline: "Recovery guide just $27",
  endsAt: "2026-08-31T23:59:59-04:00",
  badge: "Summer sale — $27",
} as const;

export const PRODUCT = {
  id: "adhd-notion-recovery",
  name: "ADHD Notion Recovery Guide",
  fullName: "Focus Dock — ADHD Notion Recovery Guide",
  description:
    "A PDF protocol for ADHD adults who've abandoned too many Notion templates — install a 3-database system in 47 minutes with minute-by-minute steps, copy-paste formulas, task sequences, and an 11-minute Sunday reset.",
  price: 27,
  compareAt: 49,
  currency: "usd",
  fileName: "Focus_Dock_ADHD_Notion_Recovery_Guide.pdf",
  fileLabel: "PDF Guide",
  formulasFileName: "Focus_Dock_Formulas.txt",
} as const;

export const PACKAGE_ITEMS = [
  {
    num: "01",
    title: "47-Minute Install Protocol",
    description:
      "Step-by-step setup: Brain Dump, Today, and Projects databases — with exact property names and zero fluff.",
    accent: "navy",
  },
  {
    num: "02",
    title: "Task Sequence System",
    description:
      "Hide formulas and rollups for executive dysfunction — one sequence step visible at a time; keep 1–3 parallel tasks max.",
    accent: "coral",
  },
  {
    num: "03",
    title: "Daily 3-Minute Workflow",
    description: "Morning, midday capture, and evening rules designed for ADHD brains that hate maintenance.",
    accent: "mint",
  },
  {
    num: "04",
    title: "11-Minute Sunday Reset",
    description: "Weekly triage without guilt dashboards, streaks, or 45-minute reviews.",
    accent: "amber",
  },
  {
    num: "05",
    title: "Emergency Overwhelm Card",
    description: "Printable 4-step protocol for days when everything feels loud — no Notion required.",
    accent: "navy",
  },
] as const;

export const FAQ_ITEMS = [
  {
    q: "Is this another Notion template?",
    a: "No — and that's the point. Focus Dock is an implementation guide. You build a minimal 3-database system yourself in 47 minutes. No template file to abandon in three weeks.",
  },
  {
    q: "I've failed at Notion before. Will this work?",
    a: "This guide is specifically for the 'template graveyard' crowd. It addresses setup spirals, choice overload, and streak shame — the three reasons ADHD brains abandon Notion.",
  },
  {
    q: "Do I need Notion paid plan?",
    a: "Free tier works. Everything in the guide uses features available on Notion's free plan.",
  },
  {
    q: "How fast do I get access?",
    a: "Instantly after checkout. You'll land on a download page and can save the PDF immediately.",
  },
  {
    q: "What if it doesn't help?",
    a: "Email us within 14 days for a full refund. No hoops, no guilt — same energy as the system itself.",
  },
] as const;