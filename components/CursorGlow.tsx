"use client";

import { useEffect, useRef } from "react";
import { motion, useMotionValue, useSpring } from "motion/react";

export function CursorGlow() {
  const x = useMotionValue(-200);
  const y = useMotionValue(-200);
  const springX = useSpring(x, { stiffness: 120, damping: 20, mass: 0.5 });
  const springY = useSpring(y, { stiffness: 120, damping: 20, mass: 0.5 });
  const visible = useRef(false);

  useEffect(() => {
    function onMove(e: MouseEvent) {
      if (!visible.current) visible.current = true;
      x.set(e.clientX);
      y.set(e.clientY);
    }
    window.addEventListener("mousemove", onMove);
    return () => window.removeEventListener("mousemove", onMove);
  }, [x, y]);

  return (
    <motion.div
      className="pointer-events-none fixed z-[200] hidden md:block"
      style={{
        x: springX,
        y: springY,
        translateX: "-50%",
        translateY: "-50%",
        width: 320,
        height: 320,
        background:
          "radial-gradient(circle, color-mix(in srgb, var(--coral) 12%, transparent) 0%, transparent 70%)",
        borderRadius: "50%",
      }}
    />
  );
}
