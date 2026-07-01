# Focus Dock — Digital Product Storefront

**Repository:** https://github.com/Raine5600/focus-dock

**Affiliate database:** 261 verified contacts in `marketing/affiliate-contacts-by-type.xlsx` (148 email · 113 contact form)

A Next.js storefront for selling the **Focus Dock ADHD Notion Recovery Guide** PDF. Built for [Vercel](https://vercel.com) with [Stripe Checkout](https://stripe.com) payments, secure post-purchase downloads, and an affiliate application flow.

## Features

- Branded landing page with product details, summer deal pricing, and FAQ
- Stripe Checkout (one-time $27 purchase)
- Secure download — only verified paid sessions can access the PDF
- Success page with re-download support
- Affiliate program page (`/affiliates`) with application form (Zoho SMTP)
- Stripe webhook logs every purchase (view at `/admin`)
- SEO: `robots.txt`, `sitemap.xml`, Open Graph images, JSON-LD

## Quick start (local)

```bash
npm install
cp .env.example .env.local
# Add your Stripe test keys and other env vars to .env.local
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Test payments

Use [Stripe test cards](https://docs.stripe.com/testing#cards): `4242 4242 4242 4242`, any future expiry, any CVC.

### Local webhooks (optional)

```bash
stripe listen --forward-to localhost:3000/api/webhook
```

Copy the webhook signing secret into `STRIPE_WEBHOOK_SECRET`.

## Deploy to Vercel

### 1. Push to GitHub

```bash
git add .
git commit -m "Initial Focus Dock storefront"
git remote add origin https://github.com/YOUR_USERNAME/focus-dock.git
git push -u origin main
```

### 2. Import in Vercel

1. Go to [vercel.com/new](https://vercel.com/new)
2. Import your `focus-dock` repository
3. Framework preset: **Next.js** (auto-detected)
4. Deploy

### 3. Add environment variables

In Vercel → Project → Settings → Environment Variables:

| Variable | Required | Value |
|----------|----------|-------|
| `STRIPE_SECRET_KEY` | Yes | Your `sk_live_...` key |
| `STRIPE_WEBHOOK_SECRET` | Yes | From Stripe webhook (step 4) |
| `ADMIN_PASSWORD` | Yes | Password for `/admin` purchase log |
| `NEXT_PUBLIC_APP_URL` | Yes | `https://getfocusdock.com` |
| `NEXT_PUBLIC_EMAIL_DOMAIN` | Recommended | `getfocusdock.com` |
| `NEXT_PUBLIC_CONTACT_EMAIL` | Recommended | `hello@getfocusdock.com` |
| `SMTP_USER` | For affiliates | `hello@getfocusdock.com` |
| `SMTP_APP_PASSWORD` | For affiliates | Zoho app-specific password |
| `BLOB_READ_WRITE_TOKEN` | Recommended | Vercel → Storage → Blob → token |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | Optional | Not used by current checkout flow |

Redeploy after adding variables.

### 4. Connect Stripe webhook (purchase logging)

1. Deploy once so you have a live URL (e.g. `https://getfocusdock.com`)
2. [Stripe Dashboard → Webhooks](https://dashboard.stripe.com/webhooks) → **Add endpoint**
3. Endpoint URL: `https://getfocusdock.com/api/webhook`
4. Select event: **`checkout.session.completed`**
5. Click **Add endpoint** → reveal **Signing secret** (`whsec_...`)
6. Paste into Vercel as `STRIPE_WEBHOOK_SECRET` → **Redeploy**

Each completed purchase is logged automatically. View them at **`/admin`** (use your `ADMIN_PASSWORD`).

**Optional — persistent storage:** Vercel → your project → **Storage** → Create **Blob** store → connect to project → copy `BLOB_READ_WRITE_TOKEN` into env vars. Without this, `/admin` still works by reading from Stripe directly.

**Test webhook:** Stripe → Webhooks → your endpoint → **Send test event** → `checkout.session.completed`

### 5. Custom domain (optional)

Vercel → Project → Settings → Domains → add `getfocusdock.com`.

Update `NEXT_PUBLIC_APP_URL` to match.

## Product file

The downloadable PDF lives at:

```
private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide.pdf
```

To update the product, replace this file and redeploy. It is **not** publicly accessible — downloads go through `/api/download` after Stripe payment verification.

Regenerate the PDF locally:

```bash
python scripts/generate_pdf.py
```

## Project structure

```
app/
  page.tsx              # Landing page
  affiliates/page.tsx   # Affiliate program + application form
  success/page.tsx      # Post-purchase download page
  admin/page.tsx        # Purchase log (password protected)
  robots.ts             # robots.txt
  sitemap.ts            # sitemap.xml
  api/checkout/         # Creates Stripe Checkout session
  api/download/         # Serves PDF to paid customers
  api/webhook/          # Stripe event handler
  api/affiliate-apply/  # Affiliate application email
components/             # UI sections
lib/                    # Product config, Stripe, SEO helpers
private/downloads/      # Product PDF (server-only)
public/images/          # Marketing images
marketing/              # Outreach scripts and assets
```

## Support email

Support, hello, and partnerships addresses are configured via `NEXT_PUBLIC_CONTACT_EMAIL` and `NEXT_PUBLIC_EMAIL_DOMAIN` in `.env.local`. Defaults resolve to `support@getfocusdock.com`, `hello@getfocusdock.com`, and `partnerships@getfocusdock.com`.

## Tech stack

- Next.js 16 (App Router, Turbopack)
- Tailwind CSS 4
- Stripe Checkout
- Nodemailer (Zoho SMTP for affiliate applications)
- TypeScript