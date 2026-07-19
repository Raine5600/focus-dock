"use client";

import Image from "next/image";
import Link from "next/link";
import { useEffect, useState } from "react";
import { BRAND } from "@/lib/product";

export function Header() {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 8);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      className={`border-b bg-cream/90 backdrop-blur-md transition-shadow duration-300 ${
        scrolled ? "border-border shadow-md shadow-navy-dark/5" : "border-border/60"
      }`}
    >
      <div className="mx-auto flex max-w-6xl items-center justify-between px-5 py-4 sm:px-8">
        <Link href="/" className="group flex items-center gap-3">
          <Image
            src="/images/logo-mark.png"
            alt=""
            width={40}
            height={40}
            priority
            className="h-10 w-10 transition-transform group-hover:scale-105"
          />
          <div>
            <p className="font-display text-lg font-semibold leading-tight text-navy-dark">
              {BRAND.name}
            </p>
            <p className="hidden text-xs text-ink-lt sm:block">
              ADHD Notion recovery
            </p>
          </div>
        </Link>
        <nav className="flex items-center gap-6 text-sm font-medium text-ink-mid">
          <a href="#inside" className="hidden transition hover:text-navy-dark sm:inline">
            Look inside
          </a>
          <a href="#included" className="hidden transition hover:text-navy-dark sm:inline">
            What&apos;s included
          </a>
          <a href="#faq" className="hidden transition hover:text-navy-dark md:inline">
            FAQ
          </a>
          <Link
            href="/affiliates"
            className="hidden transition hover:text-navy-dark md:inline"
          >
            Affiliates
          </Link>
          <a
            href="#pricing"
            className="rounded-full bg-coral px-5 py-2.5 text-white shadow-sm transition hover:bg-[#e55a3a] hover:shadow-md"
          >
            Get the guide
          </a>
        </nav>
      </div>
    </header>
  );
}
