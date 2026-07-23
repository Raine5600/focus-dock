import { Reveal, Stagger, StaggerItem } from "./motion";
import { TiltCard } from "./TiltCard";

const TESTIMONIALS = [
  {
    quote:
      "I've tried every Notion template on YouTube. This is the first one I actually opened on a Monday and didn't immediately close. Three databases, that's it. My brain can hold three things.",
    name: "Mia R.",
    context: "Freelance designer, ADHD diagnosis at 27",
    initial: "M",
  },
  {
    quote:
      "The recovery section alone was worth it. I had six abandoned Notion setups and genuine shame about it. Reading that it's a design flaw, not a me flaw, hit different. Then the system actually worked.",
    name: "Jordan T.",
    context: "Software engineer, combined-type ADHD",
  },
  {
    quote:
      "Bought it at 11pm on a Tuesday, set it up that night, used it the next morning. I haven't done that with anything productivity-related in years. The 'one visible task' thing is genuinely magic.",
    name: "Priya S.",
    context: "PhD student, recently diagnosed",
    initial: "P",
  },
  {
    quote:
      "I was skeptical because $27 for a PDF felt steep. Then I did the math on every course and template I've bought that I never touched. This one I actually use. Daily.",
    name: "Alex K.",
    context: "Product manager, ADHD + anxiety",
    initial: "A",
  },
  {
    quote:
      "The brain dump section fixed the thing that always broke my systems — I'd think of something, have nowhere to put it, and lose the thread entirely. Now it takes two seconds and I forget about it until the right moment.",
    name: "Sam W.",
    context: "Teacher, inattentive ADHD",
    initial: "S",
  },
];

export function Testimonials() {
  return (
    <section className="bg-white py-20 sm:py-28">
      <div className="mx-auto max-w-6xl px-5 sm:px-8">
        <Reveal>
          <div className="mb-14 text-center">
            <p className="text-sm font-bold uppercase tracking-widest text-coral">
              Real results
            </p>
            <h2 className="mt-3 font-display text-3xl font-bold text-navy-dark sm:text-4xl">
              From people who gave Notion one last shot
            </h2>
          </div>
        </Reveal>

        <Stagger gap={0.07}>
          <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {TESTIMONIALS.map((t, i) => (
              <StaggerItem key={i}>
                <TiltCard className="h-full">
                <div className="flex h-full flex-col rounded-2xl border border-border bg-cream p-6 shadow-sm">
                  <span
                    className="mb-4 font-display text-5xl leading-none text-coral/25"
                    aria-hidden
                  >
                    &ldquo;
                  </span>
                  <p className="flex-1 text-base leading-relaxed text-ink-mid">
                    {t.quote}
                  </p>
                  <div className="mt-6 flex items-center gap-3">
                    <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-navy-dark text-sm font-bold text-white">
                      {(t.initial ?? t.name[0]).toUpperCase()}
                    </span>
                    <div>
                      <p className="font-semibold text-navy-dark">{t.name}</p>
                      <p className="text-xs text-ink-lt">{t.context}</p>
                    </div>
                  </div>
                </div>
                </TiltCard>
              </StaggerItem>
            ))}
          </div>
        </Stagger>
      </div>
    </section>
  );
}
