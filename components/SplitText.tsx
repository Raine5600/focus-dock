"use client";

import { motion, useReducedMotion } from "motion/react";

const SPRING = { type: "spring", stiffness: 260, damping: 28, mass: 1 } as const;

type Props = {
  text: string;
  className?: string;
  wordClassName?: string;
  delay?: number;
  stagger?: number;
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
        <motion.span
          key={i}
          className={`inline-block ${wordClassName}`}
          aria-hidden
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true, margin: "-40px" }}
          transition={{ ...SPRING, delay: delay + i * stagger }}
        >
          {token}
          {split === "word" && i < tokens.length - 1 ? " " : ""}
        </motion.span>
      ))}
    </span>
  );
}
