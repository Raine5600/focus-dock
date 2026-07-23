"use client";

import { motion, useScroll, useSpring } from "motion/react";

export function ScrollProgress() {
  const { scrollYProgress } = useScroll();
  const scaleX = useSpring(scrollYProgress, { stiffness: 200, damping: 30 });

  return (
    <motion.div
      className="pointer-events-none fixed left-0 top-0 z-[100] h-[2px] w-full origin-left bg-coral"
      style={{ scaleX }}
    />
  );
}
