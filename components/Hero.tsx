"use client";

import { motion, useScroll, useTransform } from "motion/react";
import { useRef } from "react";
import { HERO, PRODUCT } from "@/lib/product";
import { CheckoutButton } from "./CheckoutButton";
import { DealBadge } from "./DealBadge";
import { TaskDemo } from "./TaskDemo";

const EASE = [0.21, 0.47, 0.32, 0.98] as const;

function Entrance({
  children,
  delay = 0,
  className,
}: {
  children: React.ReactNode;
  delay?: number;
  className?: string;
}) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.55, delay, ease: EASE }}
    >
      {children}
    </motion.div>
  );
}

export function Hero() {
  const ref = useRef<HTMLElement>(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ["start start", "end start"] });
  const blobAY = useTransform(scrollYProgress, [0, 1], [0, -120]);
  const blobBY = useTransform(scrollYProgress, [0, 1], [0, -80]);
  const contentY = useTransform(scrollYProgress, [0, 1], [0, 60]);

  return (
    <section ref={ref} className="noise relative overflow-hidden bg-navy-dark text-white">
      {/* Parallax aurora blobs */}
      <motion.div style={{ y: blobAY }} className="aurora aurora-a pointer-events-none absolute -left-32 -top-40 h-[28rem] w-[28rem] bg-mint/25" />
      <motion.div style={{ y: blobBY }} className="aurora aurora-b pointer-events-none absolute -right-24 top-10 h-[24rem] w-[24rem] bg-coral/20" />
      <div className="dot-grid pointer-events-none absolute inset-0 opacity-40 [mask-image:radial-gradient(ellipse_at_top,black_20%,transparent_70%)]" />

      <motion.div style={{ y: contentY }} className="relative mx-auto grid max-w-6xl gap-14 px-5 pb-24 pt-16 sm:px-8 lg:grid-cols-[1.1fr_1fr] lg:items-center lg:pt-24">
        <div>
          <Entrance>
            <div className="mb-5 flex flex-wrap items-center gap-2">
              <DealBadge />
              <p className="inline-flex rounded-full bg-mint/15 px-4 py-1.5 text-xs font-semibold uppercase tracking-wider text-mint ring-1 ring-mint/30">
                Not a template — the opposite of one
              </p>
            </div>
          </Entrance>

          <Entrance delay={0.08}>
            <h1 className="font-display text-[2.6rem] font-semibold leading-[1.08] sm:text-5xl lg:text-[3.4rem]">
              You didn&apos;t fail Notion.{" "}
              <span className="text-coral">Notion failed your brain.</span>
            </h1>
          </Entrance>

          <Entrance delay={0.16}>
            <p className="mt-6 max-w-xl text-lg leading-relaxed text-white/80">
              {HERO.subheadline}
            </p>
          </Entrance>

          <Entrance delay={0.24}>
            <div className="mt-8 flex flex-col gap-4 sm:flex-row sm:items-center">
              <CheckoutButton size="lg" />
              <p className="text-sm text-mint-lt">
                <span className="font-semibold text-white">${PRODUCT.price}</span>{" "}
                <span className="text-white/50 line-through">
                  ${PRODUCT.compareAt}
                </span>{" "}
                · one-time payment
              </p>
            </div>
            <ul className="mt-5 flex flex-wrap gap-x-6 gap-y-2 text-sm text-white/60">
              {HERO.trustBar.map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <svg
                    className="h-3.5 w-3.5 text-mint"
                    viewBox="0 0 16 16"
                    fill="none"
                    aria-hidden
                  >
                    <path
                      d="M4 8.5 6.5 11 12 5.5"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                  {item}
                </li>
              ))}
            </ul>
          </Entrance>

          <Entrance delay={0.34}>
            <ul className="mt-10 grid gap-3 text-sm text-mint-lt sm:grid-cols-2">
              {[
                "Step-by-step install protocol",
                "Task sequences + copy-paste formulas",
                "What to delete from old setups",
                "3-minute daily workflow",
                "~10-minute Sunday reset",
                "Printable emergency overwhelm card",
              ].map((item) => (
                <li key={item} className="flex items-center gap-2">
                  <span className="text-mint">✓</span>
                  {item}
                </li>
              ))}
            </ul>
          </Entrance>
        </div>

        <Entrance delay={0.3}>
          <TaskDemo />
        </Entrance>
      </motion.div>

      {/* Curved divider into next section */}
      <div className="absolute bottom-0 left-0 right-0 overflow-hidden leading-none">
        <svg viewBox="0 0 1440 48" fill="none" xmlns="http://www.w3.org/2000/svg" className="block w-full" preserveAspectRatio="none">
          <path d="M0 48 C360 0 1080 0 1440 48 L1440 48 L0 48 Z" fill="rgb(255 255 255)" />
        </svg>
      </div>
    </section>
  );
}
