/** Fetch a private Vercel Blob's JSON content (blob URLs 403 without the token). */
export async function fetchBlobJson<T>(url: string): Promise<T | null> {
  const token = process.env.BLOB_READ_WRITE_TOKEN;
  if (!token) return null;
  try {
    const res = await fetch(url, {
      headers: { authorization: `Bearer ${token}` },
      cache: "no-store",
    });
    if (!res.ok) return null;
    return (await res.json()) as T;
  } catch {
    return null;
  }
}
