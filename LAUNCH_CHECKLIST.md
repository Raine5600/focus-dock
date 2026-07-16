# Focus Dock — Launch Checklist

Ordered steps for going live. **Do not skip ahead** — email outreach and affiliate promotion depend on a working domain, deliverable email, and live checkout.

**Product:** ADHD Notion Recovery Guide · $27 summer sale  
**Domain:** getfocusdock.com  
**Repo:** `/Users/cameron/focus-dock`

---

## Pre-flight (local)

- [ ] `npm install` completes without errors
- [ ] `npm run build` succeeds
- [ ] PDF exists at `private/downloads/Focus_Dock_ADHD_Notion_Recovery_Guide.pdf`
- [ ] `.env.local` filled from `.env.example` (Stripe keys can be test mode until Step 4)

---

## Step 1 — Domain registration

**Goal:** Own `getfocusdock.com` before email or Stripe branding.

1. Register **getfocusdock.com** at Cloudflare Registrar or Namecheap
2. Confirm you control DNS for the domain
3. Do **not** point email records to Zoho until Step 2

**Verify:**
- [ ] Domain registered and active in registrar dashboard
- [ ] DNS management accessible

---

## Step 2 — Zoho email setup (SPF / DKIM / DMARC)

**Goal:** `hello@getfocusdock.com` can send outreach without landing in spam.

Full detail: `marketing/zoho-setup.md`

1. Create Zoho Mail account → add domain `getfocusdock.com`
2. Verify domain via TXT record at registrar
3. Create mailboxes:
   - `hello@getfocusdock.com` — outreach + partnerships
   - `support@getfocusdock.com` — customer support
4. Generate **app-specific password** (not login password) for SMTP
5. Add DNS records:

| Record | Value |
|--------|-------|
| **SPF** (TXT) | `v=spf1 include:zoho.com ~all` |
| **DKIM** | Enable in Zoho Mail admin → publish CNAME/TXT as shown |
| **DMARC** (TXT) | `v=DMARC1; p=none; rua=mailto:hello@getfocusdock.com` |

6. Warm up mailbox: send 5–10 personal emails over 2 days before any campaign
7. Save credentials locally:
   ```
   SMTP_USER=hello@getfocusdock.com
   SMTP_APP_PASSWORD=<app-specific-password>
   ```

**Verify:**
- [ ] Send test email from Zoho webmail → arrives in Gmail inbox (not spam)
- [ ] [mail-tester.com](https://www.mail-tester.com) score ≥ 8/10
- [ ] SPF, DKIM, DMARC all pass in email headers

---

## Step 3 — Vercel deploy

**Goal:** Site live on production URL with custom domain.

1. Push repo to GitHub (if not already)
2. Import project at [vercel.com/new](https://vercel.com/new) → Framework: **Next.js**
3. Add environment variables (Production):

| Variable | Value |
|----------|-------|
| `NEXT_PUBLIC_APP_URL` | `https://getfocusdock.com` |
| `NEXT_PUBLIC_EMAIL_DOMAIN` | `getfocusdock.com` |
| `NEXT_PUBLIC_CONTACT_EMAIL` | `hello@getfocusdock.com` |
| `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` | `pk_live_...` |
| `STRIPE_SECRET_KEY` | `sk_live_...` |
| `ADMIN_PASSWORD` | Strong password for `/admin` |
| `BLOB_READ_WRITE_TOKEN` | Optional — Vercel Blob for purchase log |

4. Deploy → copy Vercel project URL
5. In registrar DNS, add records for custom domain:
   - **A** or **CNAME** per Vercel domain settings for `getfocusdock.com`
   - **www** → redirect to apex (optional)
6. Vercel → Project → Domains → add `getfocusdock.com` → wait for SSL

**Verify:**
- [ ] https://getfocusdock.com loads landing page
- [ ] https://getfocusdock.com/affiliates loads application form
- [ ] OG image and metadata render correctly
- [ ] `/admin` login works with `ADMIN_PASSWORD`

---

## Step 4 — Stripe products + webhook

**Goal:** Checkout works end-to-end; purchases log and deliver PDF.

### 4a. Stripe product

1. [Stripe Dashboard → Products](https://dashboard.stripe.com/products) → **Add product**
2. Name: `Focus Dock — ADHD Notion Recovery Guide`
3. Price: **$27.00 USD** one-time (or use existing Price ID in code)
4. Confirm `lib/product.ts` price matches Stripe (`price: 27`)

### 4b. Webhook

1. Deploy must be live at `https://getfocusdock.com`
2. [Stripe → Webhooks](https://dashboard.stripe.com/webhooks) → **Add endpoint**
3. URL: `https://getfocusdock.com/api/webhook`
4. Event: `checkout.session.completed`
5. Copy signing secret → add to Vercel as `STRIPE_WEBHOOK_SECRET`
6. **Redeploy** Vercel after adding webhook secret

### 4c. End-to-end test

1. Complete a **live** test purchase (refund immediately) or use Stripe test mode on preview deploy first
2. Confirm redirect to `/success` with download link
3. Confirm purchase appears at `/admin`
4. Confirm download delivers `Focus_Dock_ADHD_Notion_Recovery_Guide.pdf`

**Verify:**
- [ ] Checkout button opens Stripe Checkout
- [ ] Payment succeeds → success page → PDF downloads
- [ ] Webhook shows `200` in Stripe dashboard
- [ ] Purchase logged in `/admin`

---

## Step 5 — Pre-outreach sanity check

**Goal:** Nothing embarrassing goes out with a broken link or wrong price.

- [ ] Landing page shows $27 summer sale (matches Stripe)
- [ ] 14-day refund policy accurate in FAQ
- [ ] `hello@getfocusdock.com` replies work
- [ ] `support@getfocusdock.com` listed on site
- [ ] Affiliate page commission (40%) matches `affiliate-assets.md`
- [ ] Manual outreach templates reviewed: `marketing/manual-outreach-templates.md`

---

## Step 6 — Enable email campaign (ONLY after Steps 1–5)

**Do not run automated sends until domain, Vercel, and Stripe are verified.**

Outreach sends from **blacksheepdesignscontact@gmail.com** (Gmail). Full setup: `marketing/gmail-setup.md`.

Automated outreach targets creators with verified emails in `marketing/creator-outreach-list.json` (e.g., Mynd, Systems Made Better, August Bradley, Ruri Ohama). Future research should prioritize **5k–100k subscribers** — see `research/04-outreach-targeting.md`. Existing contacts stay sendable regardless of size.

```bash
cd /Users/cameron/focus-dock/marketing

# Check domain is live (must pass before sending)
python3 email-campaign.py --check-domain

# Preview first — always safe, no domain required
python3 email-campaign.py --dry-run

# Send ONLY after getfocusdock.com is live:
export DOMAIN_READY=true
export SMTP_USER=blacksheepdesignscontact@gmail.com
export SMTP_APP_PASSWORD=<gmail-app-password>
python3 email-campaign.py --send --limit 4
```

**Hard gate:** `--send` is blocked unless `DOMAIN_READY=true`, `https://getfocusdock.com` responds, and `SMTP_APP_PASSWORD` is set.

**Manual outreach (contact forms + LinkedIn)** — same day or after automated batch:

| Creator | Action |
|---------|--------|
| Jenna Redfield | Contact form — `manual-outreach-templates.md` §1 |
| Marie Poulin | Contact form |
| Meredith Marsh | Contact form |
| Jesper Dramsch | Contact form |
| Stuart Ridout | LinkedIn DM |
| ADHD reWired | LinkedIn DM |

Log every send in tracking table (`manual-outreach-templates.md` §4).

**Verify:**
- [ ] `--dry-run` output looks correct
- [ ] First `--send` batch: ≤ 4 emails, spaced 90+ seconds
- [ ] No bounces in Zoho sent folder
- [ ] Manual log updated

---

## Step 7 — Affiliate program go-live

**Goal:** Partners can apply, receive links, and get paid.

1. Confirm `/affiliates` form submits → email to `hello@getfocusdock.com` (check `lib/mail.ts`)
2. Prepare affiliate kit per partner:
   - Custom `https://getfocusdock.com/?ref=CREATOR_CODE`
   - Copy of `marketing/affiliate-assets.md`
   - Free PDF review copy
3. Define payout process: Net-30, $50 minimum, PayPal/Venmo
4. As partners accept, send **§5 follow-up** from `affiliate-assets.md`
5. When first mention goes live, send **§6 thank-you** email

**Verify:**
- [ ] Test affiliate application delivers to inbox
- [ ] `?ref=` parameter tracked (confirm in analytics or manual test)
- [ ] First partner has link + script + PDF
- [ ] Payout method documented for each active affiliate

---

## Launch complete criteria

All must be true:

| # | Criterion |
|---|-----------|
| 1 | getfocusdock.com resolves with valid SSL |
| 2 | hello@ / support@ email sending + receiving |
| 3 | SPF, DKIM, DMARC passing |
| 4 | Stripe checkout → webhook → download works |
| 5 | Email campaign dry-run approved; first batch sent OR manual outreach logged |
| 6 | Affiliate program accepting applications |

---

## Post-launch (week 1)

- [ ] Monitor Stripe webhook errors daily
- [ ] Reply to affiliate applications within 48 hours
- [ ] Send follow-ups (5 days) per `affiliate-assets.md` §4 for non-responders
- [ ] Cap outbound email at 15/day (`email-campaign.py` limit)
- [ ] Track manual outreach in spreadsheet (§4 of manual-outreach-templates.md)

---

## Reference files

| File | Purpose |
|------|---------|
| `marketing/manual-outreach-templates.md` | Contact form + LinkedIn copy |
| `marketing/affiliate-assets.md` | Scripts, follow-ups, ad copy |
| `marketing/gmail-setup.md` | Gmail outreach SMTP |
| `marketing/zoho-setup.md` | Zoho DNS (site email) |
| `research/04-outreach-targeting.md` | 5k–100k subscriber criteria |
| `marketing/email-campaign.py` | Automated email sends |
| `marketing/creator-outreach-list.json` | Full creator roster |
| `.env.example` | Required environment variables |