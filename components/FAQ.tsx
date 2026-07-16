"use client";

import { useState } from "react";
import { AnimatePresence, motion } from "motion/react";
import { FAQ_ITEMS } from "@/lib/product";
import { Reveal } from "./motion";

function FaqItem({
  q,
  a,
  open,
  onToggle,
}: {
  q: string;
  a: string;
  open: boolean;
  onToggle: () => void;
}) {
  return (
    <div className="overflow-hidden rounded-2xl border border-border bg-white shadow-sm">
      <button
        type="button"
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-4 px-6 py-5 text-left"
      >
        <span className="font-display text-lg font-semibold text-navy-dark">
          {q}
        </span>
        <motion.span
          animate={{ rotate: open ? 45 : 0 }}
          transition={{ duration: 0.2 }}
          className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-cream-dk text-lg font-semibold text-ink-mid"
          aria-hidden
        >
          +
        </motion.span>
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.28, ease: [0.21, 0.47, 0.32, 0.98] }}
          >
            <p className="px-6 pb-6 leading-relaxed text-ink-mid">{a}</p>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export function FAQ() {
  const [openIndex, setOpenIndex] = useState<number | null>(0);

  return (
    <section className="bg-cream py-20 sm:py-24" id="faq">
      <div className="mx-auto max-w-3xl px-5 sm:px-8">
        <Reveal className="text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            Questions
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            Questions ADHD brains ask
          </h2>
        </Reveal>

        <Reveal delay={0.08}>
          <div className="mt-12 space-y-4">
            {FAQ_ITEMS.map((item, i) => (
              <FaqItem
                key={item.q}
                q={item.q}
                a={item.a}
                open={openIndex === i}
                onToggle={() => setOpenIndex(openIndex === i ? null : i)}
              />
            ))}
          </div>
        </Reveal>
      </div>
    </section>
  );
}
