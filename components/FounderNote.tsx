import { Reveal } from "./motion";

export function FounderNote() {
  return (
    <section className="bg-cream py-20 sm:py-24">
      <div className="mx-auto max-w-3xl px-5 sm:px-8">
        <Reveal>
          <div className="relative rounded-3xl border border-border bg-white p-8 shadow-sm sm:p-12">
            <span
              className="absolute -top-5 left-8 font-display text-7xl leading-none text-coral/30"
              aria-hidden
            >
              &ldquo;
            </span>
            <p className="text-lg leading-relaxed text-ink-mid">
              I built Focus Dock because I owned the graveyard. Five templates,
              two &ldquo;second brains,&rdquo; one $99 bundle — each one
              abandoned by week three, each one another piece of evidence that I
              was the problem.
            </p>
            <p className="mt-4 text-lg leading-relaxed text-ink-mid">
              I wasn&apos;t. The systems were built for brains that enjoy
              maintenance. So this is the opposite: three databases, two
              formulas, one visible task. Small enough to survive a bad week —
              and it starts with recovering from the templates, not pretending
              they never happened.
            </p>
            <p className="mt-4 text-lg leading-relaxed text-ink-mid">
              If it doesn&apos;t fit your brain, the refund is a two-line email.
              No hoops, no guilt. Same energy as the system.
            </p>
            <div className="mt-8 flex items-center gap-4">
              <span className="flex h-11 w-11 items-center justify-center rounded-full bg-navy-dark text-lg text-white">
                ⚡
              </span>
              <div>
                <p className="font-display font-semibold text-navy-dark">
                  Cameron
                </p>
                <p className="text-sm text-ink-lt">Builder of Focus Dock</p>
              </div>
            </div>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
