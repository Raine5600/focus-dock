export function Problem() {
  const pains = [
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
  ];

  return (
    <section className="border-y border-border bg-white py-20">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <div className="mx-auto max-w-2xl text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-coral">
            Sound familiar?
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark sm:text-4xl">
            You&apos;re not broken. You&apos;ve been plansturbating.
          </h2>
          <p className="mt-4 text-lg text-ink-mid">
            Building Notion systems releases dopamine. Using them requires
            executive function. Focus Dock breaks that trap with a recovery
            protocol — not another template.
          </p>
        </div>
        <div className="mt-14 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {pains.map((item) => (
            <article
              key={item.title}
              className="rounded-2xl border border-border bg-cream p-6 shadow-sm"
            >
              <h3 className="font-display text-xl font-semibold text-navy-dark">
                {item.title}
              </h3>
              <p className="mt-3 leading-relaxed text-ink-mid">{item.body}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}