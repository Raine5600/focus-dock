import { Reveal, Stagger, StaggerItem } from "./motion";

const FOR = [
  "You've abandoned 2+ Notion templates in the past year",
  "You've spent 3+ hours setting up before doing one real task",
  "'Do laundry' or 'email boss' sits on your list for 5+ days",
  "You feel productive while customizing — but not while working",
  "Broken habit-tracker streaks make you avoid opening the page",
];

const NOT_FOR = [
  "You already use Notion daily without thinking about it",
  "You want a 40-database life OS with dashboards for everything",
  "You enjoy building systems as a hobby (that's valid — this isn't that)",
  "You're looking for a template file to duplicate",
];

export function WhoItsFor() {
  return (
    <section className="border-y border-border bg-white py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            An honest filter
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            This is for a very specific person
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            The guide opens with this same self-check. If the left column
            isn&apos;t you, keep your $27.
          </p>
        </Reveal>

        <Stagger className="mt-14 grid gap-6 lg:grid-cols-2">
          <StaggerItem>
            <div className="h-full rounded-3xl border-2 border-mint/60 bg-mint-lt/40 p-8">
              <p className="font-display text-xl font-semibold text-navy-dark">
                Get it if…
              </p>
              <ul className="mt-5 space-y-3.5">
                {FOR.map((item) => (
                  <li key={item} className="flex items-start gap-3 text-ink-mid">
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-mint text-xs font-bold text-navy-dark">
                      ✓
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </StaggerItem>

          <StaggerItem>
            <div className="h-full rounded-3xl border border-border bg-cream p-8">
              <p className="font-display text-xl font-semibold text-navy-dark">
                Skip it if…
              </p>
              <ul className="mt-5 space-y-3.5">
                {NOT_FOR.map((item) => (
                  <li key={item} className="flex items-start gap-3 text-ink-mid">
                    <span className="mt-0.5 flex h-5 w-5 shrink-0 items-center justify-center rounded-full bg-cream-dk text-xs font-bold text-ink-lt">
                      ✕
                    </span>
                    {item}
                  </li>
                ))}
              </ul>
            </div>
          </StaggerItem>
        </Stagger>
      </div>
    </section>
  );
}
