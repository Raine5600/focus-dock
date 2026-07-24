import { list, put } from "@vercel/blob";
import { fetchBlobJson } from "@/lib/blob";

export type MarketingChannel = "email" | "bluesky" | "twitter" | "reddit";

export type MarketingLogEntry = {
  id: string;
  channel: MarketingChannel;
  sentAt: string;
  preview: string;
  recipientCount?: number;
  postUrl?: string;
  notes?: string;
};

export type BroadcastRecord = {
  id: string;
  sentAt: string;
  subject: string;
  sent: number;
  failed: number;
};

export async function logMarketingEntry(
  entry: Omit<MarketingLogEntry, "id">
): Promise<string> {
  const id = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
  await put(
    `marketing-log/${id}.json`,
    JSON.stringify({ ...entry, id }),
    { access: "public", addRandomSuffix: false }
  );
  return id;
}

export async function getMarketingLog(): Promise<MarketingLogEntry[]> {
  try {
    const { blobs } = await list({ prefix: "marketing-log/" });
    const entries = await Promise.all(
      blobs.map((b) => fetchBlobJson<MarketingLogEntry>(b.url))
    );
    return entries
      .filter((e): e is MarketingLogEntry => e !== null)
      .sort((a, b) => new Date(b.sentAt).getTime() - new Date(a.sentAt).getTime());
  } catch {
    return [];
  }
}

export async function getSubscriberEmailsForBroadcast(): Promise<string[]> {
  try {
    const { blobs } = await list({ prefix: "subscribers/" });
    const records = await Promise.all(
      blobs.map((b) => fetchBlobJson<{ email: string }>(b.url))
    );
    return records.flatMap((r) => (r?.email ? [r.email] : []));
  } catch {
    return [];
  }
}

export async function postToBluesky(
  text: string
): Promise<{ url: string; uri: string; cid: string }> {
  const handle = process.env.BLUESKY_HANDLE;
  const appPassword = process.env.BLUESKY_APP_PASSWORD;

  if (!handle || !appPassword) {
    throw new Error("BLUESKY_HANDLE and BLUESKY_APP_PASSWORD must be set");
  }

  const { BskyAgent, RichText } = await import("@atproto/api");
  const agent = new BskyAgent({ service: "https://bsky.social" });
  await agent.login({ identifier: handle, password: appPassword });

  const rt = new RichText({ text });
  await rt.detectFacets(agent);

  const result = await agent.post({
    text: rt.text,
    facets: rt.facets,
    createdAt: new Date().toISOString(),
  });

  const rkey = result.uri.split("/").pop()!;
  const cleanHandle = handle.startsWith("@") ? handle.slice(1) : handle;
  const url = `https://bsky.app/profile/${cleanHandle}/post/${rkey}`;

  return { url, uri: result.uri, cid: result.cid };
}

export async function postToTwitter(
  text: string
): Promise<{ url: string; id: string }> {
  const apiKey = process.env.X_API_KEY;
  const apiKeySecret = process.env.X_API_KEY_SECRET;
  const accessToken = process.env.X_ACCESS_TOKEN;
  const accessTokenSecret = process.env.X_ACCESS_TOKEN_SECRET;

  if (!apiKey || !apiKeySecret || !accessToken || !accessTokenSecret) {
    throw new Error("X API credentials not configured");
  }

  const { TwitterApi } = await import("twitter-api-v2");
  const client = new TwitterApi({
    appKey: apiKey,
    appSecret: apiKeySecret,
    accessToken,
    accessSecret: accessTokenSecret,
  });

  const tweet = await client.v2.tweet(text);
  const id = tweet.data.id;
  return { id, url: `https://x.com/i/web/status/${id}` };
}
