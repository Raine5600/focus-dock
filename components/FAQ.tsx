import { FAQ_ITEMS } from "@/lib/product";

export function FAQ() {
  return (
    <section id="faq" className="border-t border-border bg-cream-dk py-20">
      <div className="mx-auto max-w-3xl px-5 sm:px-8">
        <div className="text-center">
          <p className="text-sm font-semibold uppercase tracking-wider text-mint">
            FAQ
          </p>
          <h2 className="mt-3 font-display text-3xl font-semibold text-navy-dark">
            Questions ADHD brains ask
          </h2>
        </div>
        <div className="mt-12 space-y-4">
          {FAQ_ITEMS.map((item) => (
            <details
              key={item.q}
              className="group rounded-2xl border border-border bg-white px-6 py-5 shadow-sm"
            >
              <summary className="cursor-pointer list-none font-display text-lg font-semibold text-navy-dark marker:content-none [&::-webkit-details-marker]:hidden">
                <span className="flex items-center justify-between gap-4">
                  {item.q}
                  <span className="text-coral transition group-open:rotate-45">+</span>
                </span>
              </summary>
              <p className="mt-4 leading-relaxed text-ink-mid">{item.a}</p>
            </details>
          ))}
        </div>
      </div>
    </section>
  );
}