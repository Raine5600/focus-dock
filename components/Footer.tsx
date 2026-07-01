import Link from "next/link";
import { BRAND } from "@/lib/product";
import { getContactEmail } from "@/lib/site";

export function Footer() {
  return (
    <footer className="border-t border-border bg-white py-12">
      <div className="mx-auto flex max-w-6xl flex-col gap-8 px-5 sm:px-8 md:flex-row md:items-start md:justify-between">
        <div>
          <p className="font-display text-xl font-semibold text-navy-dark">
            {BRAND.name}
          </p>
          <p className="mt-2 max-w-sm text-sm text-ink-mid">{BRAND.tagline}</p>
        </div>
        <div className="flex flex-col gap-8 text-sm text-ink-mid sm:flex-row sm:gap-16">
          <div>
            <p className="font-semibold text-navy-dark">Support</p>
            <a
              href={`mailto:${getContactEmail("support")}`}
              className="mt-2 block transition hover:text-coral"
            >
              {getContactEmail("support")}
            </a>
          </div>
          <div>
            <p className="font-semibold text-navy-dark">Partners</p>
            <Link
              href="/affiliates"
              className="mt-2 block transition hover:text-coral"
            >
              Affiliate program
            </Link>
          </div>
          <div>
            <p className="font-semibold text-navy-dark">Legal</p>
            <Link
              href="/privacy"
              className="mt-2 block transition hover:text-coral"
            >
              Privacy policy
            </Link>
            <Link
              href="/refund"
              className="mt-2 block transition hover:text-coral"
            >
              Refund policy
            </Link>
          </div>
        </div>
        <p className="max-w-xs text-xs leading-relaxed text-ink-lt md:text-right">
          Educational guidance only — not medical or therapeutic advice.
          © {new Date().getFullYear()} {BRAND.name}.
        </p>
      </div>
    </footer>
  );
}