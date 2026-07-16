# Gmail Outreach Setup (Focus Dock)

Affiliate cold outreach sends from **blacksheepdesignscontact@gmail.com** via Gmail SMTP.

Site purchase emails and affiliate form notifications still use Zoho (`hello@getfocusdock.com`) — see `zoho-setup.md`.

## 1. Enable Gmail app password

1. Sign in to [Google Account](https://myaccount.google.com/) for `blacksheepdesignscontact@gmail.com`
2. Turn on **2-Step Verification** (required for app passwords)
3. Go to **Security → App passwords**
4. Create an app password named `Focus Dock Outreach`
5. Copy the 16-character password (no spaces)

## 2. Environment variables

```bash
export SMTP_USER=blacksheepdesignscontact@gmail.com
export SMTP_APP_PASSWORD=your_16_char_app_password
export DOMAIN_READY=true   # only after getfocusdock.com is live
```

Optional overrides:

```bash
export SMTP_HOST=smtp.gmail.com
export SMTP_PORT=587          # STARTTLS (default)
export SMTP_USE_SSL=true      # use port 465 instead
```

## 3. Send limits (Gmail-tuned)

Google's hard cap for personal Gmail: **500 emails per rolling 24 hours**.

`email-campaign.py` maximizes throughput while staying safe:

| Setting | Value | Why |
|---------|-------|-----|
| Daily max | **400** | Buffer under Gmail's 500/day hard cap |
| Hourly max | **50** | Avoids burst-rate spam flags |
| Warmup delays | **120s → 90s → 72s** | Slow start, then ~50/hour steady state |
| Batch pause | **3 min every 25 sends** | Mimics human sending patterns |
| Jitter | ±5–8 sec random | Less robotic than fixed intervals |

Override via `outreach.env` if needed:
```
GMAIL_DAILY_MAX=400
GMAIL_HOURLY_MAX=50
GMAIL_BATCH_EVERY=25
GMAIL_BATCH_PAUSE=180
```

If Gmail returns a limit error, the script pauses 30 minutes and retries.
Remaining contacts auto-resume on the next run (already-sent addresses are skipped).

## 4. Run campaign

```bash
cd /Users/cameron/focus-dock/marketing

# Preview (always safe)
python3 email-campaign.py --dry-run

# Verify site is live before sending
python3 email-campaign.py --check-domain

# Send first test batch
export DOMAIN_READY=true
export SMTP_USER=blacksheepdesignscontact@gmail.com
export SMTP_APP_PASSWORD=your_app_password
python3 email-campaign.py --send --limit 3
```

## 5. Targeting (future research)

When finding new creators, prioritize **5,000–100,000 subscribers**. Existing contacts in `creator-outreach-list.json` and `affiliate-contacts-master.json` stay sendable regardless of size.

Full criteria: `research/04-outreach-targeting.md`

## 6. Manual outreach

Contact-form creators (no public email): `manual-outreach-templates.md`