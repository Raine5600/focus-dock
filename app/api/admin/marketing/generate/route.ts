import { NextResponse } from "next/server";
import { isAdminAuthenticated } from "@/lib/admin";

export const runtime = "nodejs";

type Angle =
  | "social_proof"
  | "adhd_empathy"
  | "affiliate"
  | "testimonial"
  | "urgency"
  | `reddit_${string}`;

type GenerateBody = {
  angle: Angle;
  context: {
    totalSales: number;
    totalRevenue: number;
    subscriberCount: number;
  };
};

type GeneratedContent = {
  reddit: { title: string; body: string };
  twitter: string;
  bluesky: string;
  email: { subject: string; body: string };
};

const SYSTEM_PROMPT = `You are a marketing copywriter for Focus Dock — a $27 PDF guide (43 pages) that helps ADHD adults fix abandoned Notion setups in one sitting by installing a minimal 3-database system with copy-paste formulas.

Product facts:
- URL: getfocusdock.com
- Price: $27 (compare at $49)
- 14-day money-back guarantee
- 3 databases only: Brain Dump, Tasks, Projects
- Key promise: see exactly ONE next task every time you open Notion
- Audience: ADHD adults who bought too many templates and gave up

Platform rules:
- reddit_title: Under 80 chars, curiosity/value-first, NO promotional tone. Sound like a real person.
- reddit_body: 200–350 words. Value-first story or tip. Mention Focus Dock only in the LAST paragraph as "if you want the full system". Absolutely no affiliate links. No spam. For r/ADHD: no links in body at all (subreddit rule), add "(link in profile)" if referencing the site. Sound like authentic personal experience.
- twitter: Hook in first 8 words. Under 275 chars total. Include getfocusdock.com.
- bluesky: Similar to Twitter but can be 10–15 words longer. Max 290 chars. Include getfocusdock.com.
- email_subject: Under 50 chars, curiosity or value-driven, minimal emoji.
- email_body: 150–200 words. Plain text. Conversational, empathetic. Ends with soft CTA linking to getfocusdock.com.

Return ONLY valid JSON — no markdown fences, no preamble:
{
  "reddit": { "title": "...", "body": "..." },
  "twitter": "...",
  "bluesky": "...",
  "email": { "subject": "...", "body": "..." }
}`;

function buildUserMessage(angle: Angle, ctx: GenerateBody["context"]): string {
  const revenue = (ctx.totalRevenue / 100).toFixed(0);
  const stats = `Stats: ${ctx.totalSales} total sales, $${revenue} revenue, ${ctx.subscriberCount} email subscribers.`;

  const angleDescriptions: Record<string, string> = {
    social_proof: "Social proof angle — highlight real people getting results, use the sales/subscriber numbers as credibility signals.",
    adhd_empathy: "ADHD empathy hook — lead with the feeling of a broken system, not with the product. The reader should feel seen before they see any offer.",
    affiliate: "Affiliate opportunity angle — promote the affiliate program (40% commission, $10.80 per sale). Target creators in the ADHD/productivity/Notion space.",
    testimonial: "Testimonial spotlight angle — write as if sharing a real customer success story (composite, not fabricated). Focus on the transformation, not the product features.",
    urgency: "Urgency angle — current sale price ($27, down from $49) ends soon. Don't be fake-urgent; be specific and matter-of-fact about the deal.",
  };

  // Reddit subreddit-specific angles
  if (angle.startsWith("reddit_")) {
    const subreddit = angle.replace("reddit_", "");
    const subredditRules: Record<string, string> = {
      ADHD: "Writing for r/ADHD. Rules: no links in post body (say 'link in profile' instead), must sound like genuine personal experience, no promotional language at all.",
      Notion: "Writing for r/Notion. Can include links. Frame as a 'what worked for me' post with a practical system description.",
      productivity: "Writing for r/productivity. Can include links. Frame as a productivity insight or system, not a product pitch.",
      neurodivergent: "Writing for r/neurodivergent. No links in body. Lead with the emotional experience, be vulnerable and specific.",
    };
    return `Angle: Reddit post for r/${subreddit}. ${subredditRules[subreddit] ?? ""} ${stats}`;
  }

  return `Angle: ${angleDescriptions[angle] ?? angle}. ${stats}`;
}

export async function POST(req: Request) {
  if (!await isAdminAuthenticated()) {
    return NextResponse.json({ error: "Unauthorized" }, { status: 401 });
  }

  const apiKey = process.env.DEEPSEEK_API_KEY;
  if (!apiKey) {
    return NextResponse.json({ error: "DEEPSEEK_API_KEY not configured" }, { status: 500 });
  }

  const body = (await req.json()) as GenerateBody;
  const userMessage = buildUserMessage(body.angle, body.context);

  const res = await fetch("https://api.deepseek.com/chat/completions", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${apiKey}`,
    },
    body: JSON.stringify({
      model: "deepseek-chat",
      max_tokens: 1400,
      temperature: 0.85,
      messages: [
        { role: "system", content: SYSTEM_PROMPT },
        { role: "user", content: userMessage },
      ],
    }),
  });

  if (!res.ok) {
    const text = await res.text();
    return NextResponse.json({ error: `DeepSeek error: ${res.status}`, detail: text }, { status: 502 });
  }

  const json = await res.json();
  const raw: string = json.choices?.[0]?.message?.content?.trim() ?? "";

  // Strip markdown code fences if DeepSeek wraps the output
  const cleaned = raw.replace(/^```(?:json)?\n?/, "").replace(/\n?```$/, "").trim();

  try {
    const content = JSON.parse(cleaned) as GeneratedContent;
    return NextResponse.json(content);
  } catch {
    return NextResponse.json({ error: "Failed to parse AI response", raw }, { status: 500 });
  }
}
