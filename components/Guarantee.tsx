import { Reveal } from "./motion";

export function Guarantee() {
  return (
    <section className="border-y border-border bg-white py-16">
      <div className="mx-auto max-w-4xl px-5 sm:px-8">
        <Reveal>
          <div className="flex flex-col items-center gap-6 rounded-3xl border-2 border-dashed border-mint bg-mint-lt/30 p-8 text-center sm:flex-row sm:text-left">
            <div className="flex h-24 w-24 shrink-0 flex-col items-center justify-center rounded-full bg-navy-dark text-white shadow-lg">
              <span className="font-display text-3xl font-bold leading-none">14</span>
              <span className="text-[0.6rem] font-bold uppercase tracking-wider text-mint">
                day refund
              </span>
            </div>
            <div>
              <h2 className="font-display text-2xl font-semibold text-navy-dark">
                Try the whole protocol. Risk nothing.
              </h2>
              <p className="mt-2 leading-relaxed text-ink-mid">
                Read it, install it, run a Sunday reset. If it doesn&apos;t fit
                your brain within 14 days, email us for a full refund — no
                questions, no hoops, no &ldquo;exit interview.&rdquo; You keep
                the 5-minute win either way.
              </p>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
