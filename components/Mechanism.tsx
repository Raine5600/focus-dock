"use client";

import { motion } from "motion/react";
import { Reveal } from "./motion";

const EASE = [0.21, 0.47, 0.32, 0.98] as const;

const GHOST_DBS = [
  "Habits", "Moods", "Areas", "Resources", "Goals", "Journal", "Books",
  "Finances", "Meals", "Reviews", "Archive", "Someday", "Trackers", "Notes",
];

const CORE_DBS = [
  {
    name: "Brain Dump",
    tag: "[BRAIN]",
    desc: "2-second capture. No tags, no guilt.",
    accent: "border-mint",
    chip: "bg-mint/15 text-mint",
  },
  {
    name: "Today",
    tag: "[TODAY]",
    desc: "One visible next task. Sequences hide the rest.",
    accent: "border-coral",
    chip: "bg-coral/15 text-coral",
  },
  {
    name: "Projects",
    tag: "[PROJECTS]",
    desc: "Parking lot for someday. Visited weekly, not daily.",
    accent: "border-yellow",
    chip: "bg-yellow/20 text-[#a07800]",
  },
];

export function Mechanism() {
  return (
    <section className="bg-cream py-20 sm:py-24" id="method">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            The 3-database method
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            Less system. More done.
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            Before: fourteen databases you&apos;re afraid to open. After: one
            task, visible, always. The bridge is a protocol you follow once —
            in one sitting.
          </p>
        </Reveal>

        <div className="mt-14 grid items-center gap-10 lg:grid-cols-[1fr_auto_1.2fr]">
          {/* BEFORE — the template you abandoned */}
          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-80px" }}
            className="rounded-3xl border border-border bg-white p-6"
          >
            <p className="text-xs font-bold uppercase tracking-wider text-ink-lt">
              Your last template
            </p>
            <div className="mt-4 flex flex-wrap gap-2">
              {GHOST_DBS.map((db, i) => (
                <motion.span
                  key={db}
                  variants={{
                    hidden: { opacity: 0 },
                    show: {
                      opacity: 0.45,
                      transition: { delay: i * 0.04, duration: 0.3 },
                    },
                  }}
                  className="rounded-lg border border-border bg-cream-dk px-3 py-1.5 text-xs font-medium text-ink-lt line-through decoration-ink-lt/40"
                >
                  {db}
                </motion.span>
              ))}
            </div>
            <p className="mt-4 text-sm text-ink-lt">
              14 databases · 12 decisions per open · abandoned in 19 days
            </p>
          </motion.div>

          {/* Arrow */}
          <div className="hidden justify-center lg:flex" aria-hidden>
            <motion.svg
              width="64"
              height="48"
              viewBox="0 0 64 48"
              fill="none"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              viewport={{ once: true }}
              transition={{ delay: 0.5, duration: 0.4 }}
            >
              <motion.path
                d="M4 24 H52 M40 12 L54 24 L40 36"
                stroke="var(--coral)"
                strokeWidth="3"
                strokeLinecap="round"
                strokeLinejoin="round"
                initial={{ pathLength: 0 }}
                whileInView={{ pathLength: 1 }}
                viewport={{ once: true }}
                transition={{ delay: 0.55, duration: 0.5, ease: EASE }}
              />
            </motion.svg>
          </div>

          {/* AFTER — Focus Dock */}
          <motion.div
            initial="hidden"
            whileInView="show"
            viewport={{ once: true, margin: "-80px" }}
            variants={{
              hidden: {},
              show: { transition: { staggerChildren: 0.12, delayChildren: 0.3 } },
            }}
            className="space-y-3"
          >
            {CORE_DBS.map((db) => (
              <motion.div
                key={db.name}
                variants={{
                  hidden: { opacity: 0, x: 24 },
                  show: { opacity: 1, x: 0, transition: { duration: 0.45, ease: EASE } },
                }}
                className={`flex items-center gap-4 rounded-2xl border-l-4 ${db.accent} border-y border-r border-border bg-white p-4 shadow-sm`}
              >
                <span
                  className={`rounded-lg px-2.5 py-1 font-mono text-[0.65rem] font-bold ${db.chip}`}
                >
                  {db.tag}
                </span>
                <div>
                  <p className="font-display font-semibold text-navy-dark">
                    {db.name}
                  </p>
                  <p className="text-sm text-ink-mid">{db.desc}</p>
                </div>
              </motion.div>
            ))}

            <motion.div
              variants={{
                hidden: { opacity: 0, y: 16 },
                show: { opacity: 1, y: 0, transition: { duration: 0.45, ease: EASE } },
              }}
              className="rounded-2xl bg-navy-dark p-5 text-white"
            >
              <p className="text-xs font-bold uppercase tracking-wider text-mint">
                [HOME] — what you actually see
              </p>
              <p className="mt-2 font-display text-lg font-semibold">
                One task. A capture box. Nothing else.
              </p>
              <p className="mt-1 text-sm text-white/60">
                Two formulas hide every sequenced step except the next one.
              </p>
            </motion.div>
          </motion.div>
        </div>
      </div>
    </section>
  );
}
