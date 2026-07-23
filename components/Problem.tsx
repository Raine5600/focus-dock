import { Reveal, Stagger, StaggerItem } from "./motion";
import { TiltCard } from "./TiltCard";

const PAINS = [
  {
    title: "The Saturday setup",
    body: "Four hours customizing colors and relations. Gorgeous screenshot. Haven't opened it since Wednesday.",
  },
  {
    title: "The template graveyard",
    body: "Five ADHD Notion templates this year. Habit trackers, mood logs, fourteen databases. All abandoned.",
  },
  {
    title: "The invisible tasks",
    body: "'Do laundry' is secretly 8 steps. When they all show at once, your brain files the whole thing under 'not now.'",
  },
  {
    title: "The guilt dashboard",
    body: "Miss one day on your habit tracker and the whole page becomes a monument to failure. Broken streaks make you close the tab.",
  },
  {
    title: "The micro-decision maze",
    body: "Projects or Areas? Journal or Tasks? Every open is 12 micro-decisions before you do anything — so you do nothing.",
  },
  {
    title: "The next template",
    body: "So you buy another one. $39 this time. It has even more databases. The cycle is the product.",
  },
];

export function Problem() {
  return (
    <section className="border-y border-border bg-white py-20 sm:py-24">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            Sound familiar?
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            You&apos;re not broken. You&apos;ve been stuck in the setup spiral.
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            Building Notion systems releases dopamine. Using them requires
            executive function. Templates sell you the first and abandon you at
            the second.
          </p>
        </Reveal>

        <Stagger className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {PAINS.map((item) => (
            <StaggerItem key={item.title}>
              <TiltCard className="h-full">
                <article className="h-full rounded-2xl border border-border bg-cream p-6 shadow-sm transition-shadow hover:shadow-lg">
                  <h3 className="font-display text-xl font-semibold text-navy-dark">
                    {item.title}
                  </h3>
                  <p className="mt-3 leading-relaxed text-ink-mid">{item.body}</p>
                </article>
              </TiltCard>
            </StaggerItem>
          ))}
        </Stagger>

        {/* Agitation — deliberately quiet. No animation flourish. */}
        <Reveal className="mx-auto mt-16 max-w-3xl" y={8}>
          <div className="rounded-3xl bg-navy-dark px-8 py-10 text-center sm:px-12">
            <p className="font-display text-xl font-semibold leading-relaxed text-white sm:text-2xl">
              The worst part isn&apos;t the wasted Saturdays or the $19–99 per
              template.
            </p>
            <p className="mt-4 text-lg leading-relaxed text-white/70">
              It&apos;s the story each abandoned dashboard tells you about
              yourself: <em className="text-mint not-italic">
                &ldquo;I&apos;m just not a person systems work for.&rdquo;
              </em>{" "}
              That story is false — and it ends at the next section.
            </p>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
