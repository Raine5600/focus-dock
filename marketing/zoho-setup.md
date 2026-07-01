# Zoho Email Setup for Focus Dock

## 1. Register domain
- Register `getfocusdock.com` at Cloudflare or Namecheap
- Point DNS to Vercel for website

## 2. Create Zoho Mail account
1. Go to https://www.zoho.com/mail/
2. Add domain `getfocusdock.com`
3. Verify domain via TXT record
4. Create mailboxes:
   - `hello@getfocusdock.com` (outreach + partnerships)
   - `support@getfocusdock.com` (customer support)

## 3. Generate app-specific password
1. Zoho Mail → Settings → Security → App Passwords
2. Create password for "Focus Dock Campaign"
3. Copy to `.env.local`:
   ```
   SMTP_USER=hello@getfocusdock.com
   SMTP_APP_PASSWORD=your_app_password_here
   ```

## 4. Deliverability checklist
- [ ] SPF record: `v=spf1 include:zoho.com ~all`
- [ ] DKIM: enable in Zoho Mail admin
- [ ] DMARC: `v=DMARC1; p=none; rua=mailto:hello@getfocusdock.com`
- [ ] Warm up mailbox: send 5-10 personal emails first over 2 days
- [ ] Campaign script spaces emails 90 seconds apart
- [ ] Max 15 emails per day

## 5. Send outreach (ONLY after domain + site are live)

See `LAUNCH_CHECKLIST.md` Steps 1–5 first. Emails are **blocked** until then.

```bash
cd /Users/cameron/focus-dock/marketing

# Verify domain gate
python3 email-campaign.py --check-domain

# Preview (always safe)
python3 email-campaign.py --dry-run

# Send after getfocusdock.com is live:
export DOMAIN_READY=true
export SMTP_USER=hello@getfocusdock.com
export SMTP_APP_PASSWORD=your_password
python3 email-campaign.py --send --limit 4
```

Manual outreach for contact-form creators: `manual-outreach-templates.md`

## 6. Manual outreach (contact_form creators)
Use personalized templates in `manual-outreach-templates.md` via:
- Jenna Redfield: https://www.jennaredfield.com/contact
- Marie Poulin: https://mariepoulin.com/contact
- Meredith Marsh: https://www.videobrand.com/contact