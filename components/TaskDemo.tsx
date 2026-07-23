"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";

const TASKS = [
  { task: "Put 3 dishes in the sink", meta: "Clean kitchen · step 2 of 8" },
  { task: "Open the email draft", meta: "Email boss · step 1 of 5" },
  { task: "Collect dirty clothes", meta: "Laundry · step 1 of 6" },
  { task: "Write 2 topics down", meta: "Call mom · step 1 of 5" },
] as const;

const CYCLE_MS = 3200;

/**
 * Live demo of the product's core promise: exactly one task visible.
 * The card auto-checks itself, slides away, and the next step appears —
 * mirroring the Hide Sequence formula behavior from the guide.
 */
export function TaskDemo() {
  const reduced = useReducedMotion();
  const [index, setIndex] = useState(0);
  const [checked, setChecked] = useState(false);

  useEffect(() => {
    if (reduced) return;
    const checkTimer = setTimeout(() => setChecked(true), CYCLE_MS - 900);
    const nextTimer = setTimeout(() => {
      setChecked(false);
      setIndex((i) => (i + 1) % TASKS.length);
    }, CYCLE_MS);
    return () => {
      clearTimeout(checkTimer);
      clearTimeout(nextTimer);
    };
  }, [index, reduced]);

  const current = TASKS[index];

  return (
    <div className="relative mx-auto w-full max-w-md lg:max-w-none">
      <div className="rounded-3xl border border-white/10 bg-white/5 p-6 pb-14 shadow-2xl backdrop-blur-sm">
        <div className="space-y-4">
          {/* One visible task — cycles */}
          <div className="relative min-h-[7.5rem] overflow-hidden rounded-2xl bg-navy border-l-4 border-coral">
            <AnimatePresence mode="wait" initial={false}>
              <motion.div
                key={index}
                initial={reduced ? false : { opacity: 0, y: 32 }}
                animate={{ opacity: 1, y: 0 }}
                exit={reduced ? undefined : { opacity: 0, y: -60, transition: { duration: 0.28, ease: [0.55, 0, 1, 0.45] } }}
                transition={{ duration: 0.38, ease: [0.21, 0.47, 0.32, 0.98] }}
                className="p-5"
              >
                <p className="text-xs font-bold uppercase tracking-wider text-coral">
                  Do this next
                </p>
                <div className="mt-2 flex items-center gap-3">
                  <motion.span
                    className={`flex h-6 w-6 shrink-0 items-center justify-center rounded-md border-2 text-sm font-bold ${
                      checked
                        ? "border-mint bg-mint text-navy-dark"
                        : "border-white/30 text-transparent"
                    }`}
                    animate={
                      checked && !reduced
                        ? { scale: [1, 1.4, 0.9, 1.1, 1] }
                        : undefined
                    }
                    transition={{ duration: 0.45, ease: "easeOut" }}
                    aria-hidden
                  >
                    ✓
                  </motion.span>
                  <p
                    className={`font-display text-xl font-semibold transition-colors ${
                      checked ? "text-white/50 line-through" : "text-white"
                    }`}
                  >
                    {current.task}
                  </p>
                </div>
                <p className="mt-2 pl-9 text-sm text-mint-lt/80">{current.meta}</p>
              </motion.div>
            </AnimatePresence>
          </div>

          {/* Brain dump strip */}
          <div className="rounded-2xl bg-white/10 p-4">
            <p className="text-xs font-bold uppercase tracking-wider text-mint">
              Brain dump — 2-second capture
            </p>
            <p className="mt-2 text-sm text-white/80">
              call dentist · email boss · buy milk
            </p>
          </div>

          <div className="flex flex-wrap gap-2">
            <span className="rounded-full bg-mint/20 px-3 py-1 text-xs font-semibold text-mint">
              3 databases
            </span>
            <span className="rounded-full bg-yellow/20 px-3 py-1 text-xs font-semibold text-yellow">
              0 streaks
            </span>
            <span className="rounded-full bg-coral/20 px-3 py-1 text-xs font-semibold text-coral">
              0 guilt
            </span>
          </div>
        </div>
      </div>

      {/* Floating price tag */}
      <motion.div
        className="absolute -bottom-5 -left-4 rounded-2xl bg-white px-5 py-4 shadow-xl sm:-left-8"
        initial={reduced ? false : { opacity: 0, y: 14, rotate: -3 }}
        animate={{ opacity: 1, y: 0, rotate: -2 }}
        transition={{ delay: 0.55, duration: 0.5, ease: [0.21, 0.47, 0.32, 0.98] }}
      >
        <p className="text-xs font-semibold uppercase tracking-wide text-coral">
          Summer sale
        </p>
        <p className="font-display text-2xl font-semibold text-navy-dark">
          <span className="text-ink-lt line-through">$49</span> $27
        </p>
      </motion.div>
    </div>
  );
}
