"use client";

import { motion, useReducedMotion } from "motion/react";

const SPRING = { type: "spring", stiffness: 80, damping: 18, mass: 0.8 } as const;

type Props = {
  text: string;
  className?: string;
  wordClassName?: string;
  delay?: number;
  stagger?: number;
  /** Pass "word" (default) or "char" */
  split?: "word" | "char";
};

export function SplitText({
  text,
  className = "",
  wordClassName = "",
  delay = 0,
  stagger = 0.06,
  split = "word",
}: Props) {
  const reduced = useReducedMotion();
  const tokens = split === "char" ? text.split("") : text.split(" ");

  if (reduced) return <span className={className}>{text}</span>;

  return (
    <span className={`inline ${className}`} aria-label={text}>
      {tokens.map((token, i) => (
        <span
          key={i}
          className="inline-block overflow-hidden align-bottom"
          aria-hidden
        >
          <motion.span
            className={`inline-block ${wordClassName}`}
            initial={{ y: "110%", opacity: 0 }}
            whileInView={{ y: "0%", opacity: 1 }}
            viewport={{ once: true, margin: "-40px" }}
            transition={{ ...SPRING, delay: delay + i * stagger }}
          >
            {token}
            {split === "word" && i < tokens.length - 1 ? " " : ""}
          </motion.span>
        </span>
      ))}
    </span>
  );
}
