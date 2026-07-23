"use client";

import Image from "next/image";
import { useCallback, useEffect, useState } from "react";
import { AnimatePresence, motion, useReducedMotion } from "motion/react";
import { PRODUCT, STATS } from "@/lib/product";
import { Reveal, Stagger, StaggerItem } from "./motion";
import { CountUp } from "./CountUp";

const PAGES = [
  { src: "/images/guide/cover.png", label: "Cover" },
  { src: "/images/guide/contents.png", label: "Contents — pick a section" },
  { src: "/images/guide/reading-map.png", label: "Reading map + self-check" },
  { src: "/images/guide/install-step.png", label: "Install protocol, step by step" },
  { src: "/images/guide/sequences.png", label: "Pre-built task sequences" },
  { src: "/images/guide/formulas.png", label: "Copy-paste formula reference" },
  { src: "/images/guide/emergency-card.png", label: "Printable emergency card" },
];

export function LookInside() {
  const reduced = useReducedMotion();
  const [lightbox, setLightbox] = useState<number | null>(null);

  const close = useCallback(() => setLightbox(null), []);

  useEffect(() => {
    if (lightbox === null) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") close();
      if (e.key === "ArrowRight")
        setLightbox((i) => (i === null ? null : (i + 1) % PAGES.length));
      if (e.key === "ArrowLeft")
        setLightbox((i) =>
          i === null ? null : (i - 1 + PAGES.length) % PAGES.length
        );
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [lightbox, close]);

  return (
    <section className="border-y border-border bg-white py-20 sm:py-24" id="inside">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            Look inside
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            These are the actual pages
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            No mystery box. {PRODUCT.pages} pages designed for ADHD reading —
            time-boxed steps, checkpoints, drift recovery, and a printable
            emergency card. Click any page to zoom.
          </p>
        </Reveal>

        <Stagger className="mt-12 grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-7">
          {PAGES.map((page, i) => (
            <StaggerItem key={page.src}>
              <motion.button
                type="button"
                onClick={() => setLightbox(i)}
                whileHover={
                  reduced ? undefined : { y: -6, scale: 1.03, rotate: -0.5 }
                }
                transition={{ type: "spring", stiffness: 300, damping: 22 }}
                className="group block w-full cursor-zoom-in text-left"
                aria-label={`Zoom: ${page.label}`}
              >
                <span className="block overflow-hidden rounded-xl border border-border shadow-sm transition-shadow group-hover:shadow-lg">
                  <Image
                    src={page.src}
                    alt={page.label}
                    width={340}
                    height={440}
                    className="h-auto w-full"
                  />
                </span>
                <span className="mt-2 block text-center text-xs font-medium text-ink-lt">
                  {page.label}
                </span>
              </motion.button>
            </StaggerItem>
          ))}
        </Stagger>

        <Reveal delay={0.1}>
          <div className="mt-12 grid grid-cols-2 gap-4 rounded-3xl border border-border bg-cream p-6 text-center sm:grid-cols-4">
            {STATS.map((stat) => (
              <div key={stat.label}>
                <p className="font-display text-3xl font-semibold text-navy-dark">
                  <CountUp to={Number(stat.value)} />
                </p>
                <p className="mt-1 text-sm text-ink-mid">{stat.label}</p>
              </div>
            ))}
          </div>
        </Reveal>
      </div>

      {/* Lightbox */}
      <AnimatePresence>
        {lightbox !== null && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 z-[80] flex items-center justify-center bg-navy-dark/90 p-4 backdrop-blur-sm"
            onClick={close}
            role="dialog"
            aria-modal="true"
            aria-label={PAGES[lightbox].label}
          >
            <motion.div
              initial={reduced ? false : { scale: 0.94, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={reduced ? undefined : { scale: 0.96, opacity: 0 }}
              transition={{ duration: 0.25, ease: [0.21, 0.47, 0.32, 0.98] }}
              className="relative max-h-full"
              onClick={(e) => e.stopPropagation()}
            >
              <Image
                src={PAGES[lightbox].src}
                alt={PAGES[lightbox].label}
                width={760}
                height={984}
                className="max-h-[85vh] w-auto rounded-xl shadow-2xl"
                priority
              />
              <p className="mt-3 text-center text-sm font-medium text-white/80">
                {PAGES[lightbox].label} · {lightbox + 1} / {PAGES.length}
              </p>
              <button
                type="button"
                onClick={close}
                className="absolute -right-3 -top-3 flex h-9 w-9 items-center justify-center rounded-full bg-white text-lg font-bold text-navy-dark shadow-lg transition hover:bg-cream"
                aria-label="Close preview"
              >
                ×
              </button>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </section>
  );
}
