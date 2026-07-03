#!/usr/bin/env python3
"""
Focus Dock cold outreach email campaign.
Uses Zoho SMTP (smtppro.zoho.com:465).

IMPORTANT: Emails are BLOCKED until the domain is live.
Set DOMAIN_READY=true only after completing LAUNCH_CHECKLIST.md Steps 1-5.

Setup:
  1. Register getfocusdock.com
  2. Create hello@getfocusdock.com in Zoho Mail
  3. Deploy site to https://getfocusdock.com
  4. Generate Zoho app-specific password
  5. export DOMAIN_READY=true SMTP_APP_PASSWORD=...

Usage:
  python email-campaign.py --dry-run          # preview emails (always safe)
  python email-campaign.py --send             # send (requires DOMAIN_READY=true)
  python email-campaign.py --send --limit 3   # send first 3 (testing)
  python email-campaign.py --check-domain     # verify domain is reachable
"""

import argparse
import json
import os
import smtplib
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

SMTP_HOST = "smtppro.zoho.com"
SMTP_PORT = 465
MIN_DELAY_SECONDS = 90
MAX_PER_DAY = 15
REQUIRED_DOMAIN = "getfocusdock.com"
REQUIRED_SITE_URL = f"https://{REQUIRED_DOMAIN}"

LIST_PATH = Path(__file__).parent / "creator-outreach-list.json"
LOG_PATH = Path(__file__).parent / "email-send-log.json"

SUBJECT = "Quick idea for your ADHD/Notion audience"

BODY_TEMPLATE = """Hi {name},

{personalized_line}

I'm launching Focus Dock, a PDF guide for people who've abandoned multiple ADHD Notion setups (the template graveyard crowd — spent Saturday building, ghosted it by Wednesday).

It's NOT a competing template. It's a step-by-step recovery protocol: 3 databases, task sequences for executive dysfunction, no streak shame. Complements what you already teach.

Would you be open to a paid mention or dedicated segment? Happy to send a free copy first — no strings.

40% commission ($10.80/sale), custom tracking link, and a script you can riff on in your own voice.

Either way, keep making stuff that doesn't make us feel broken.

— Cameron
hello@{domain}
{site_url}
"""


def load_creators():
    with open(LIST_PATH) as f:
        return json.load(f)


def load_log():
    if LOG_PATH.exists():
        with open(LOG_PATH) as f:
            return json.load(f)
    return {"sent": [], "skipped": []}


def save_log(log):
    with open(LOG_PATH, "w") as f:
        json.dump(log, f, indent=2, default=str)


def greeting_name(creator: dict) -> str:
    contact = (creator.get("contact_name") or "").strip()
    if contact:
        return contact.split()[0]
    channel = creator.get("channel_name", "")
    return channel.split("|")[0].split("-")[0].strip().split()[0]


def personalized_line(creator: dict) -> str:
    opening = (creator.get("personalized_opening") or "").strip()
    if opening:
        return opening
    niche = creator.get("niche_focus", "ADHD/Notion")
    return f"I've been watching your {niche} content — especially your work around Notion and executive dysfunction."


def get_sendable(creators, log, limit=None):
    sent_emails = {e["email"] for e in log["sent"]}
    today_count = sum(
        1 for e in log["sent"]
        if e.get("date", "").startswith(datetime.now().strftime("%Y-%m-%d"))
    )
    remaining_today = max(0, MAX_PER_DAY - today_count)

    targets = []
    for c in creators:
        if c.get("outreach_priority") not in ("high", "medium"):
            continue
        email = (c.get("contact_email") or "").strip()
        if not email or c.get("contact_type") != "email":
            continue
        if email in sent_emails:
            continue
        targets.append(c)

    targets.sort(key=lambda x: (0 if x["outreach_priority"] == "high" else 1, x["subscribers"]))
    cap = min(remaining_today, limit or remaining_today)
    return targets[:cap]


def build_message(to_email: str, creator: dict, smtp_user: str) -> MIMEMultipart:
    msg = MIMEMultipart("alternative")
    msg["Subject"] = SUBJECT
    msg["From"] = f'"Cameron — Focus Dock" <{smtp_user}>'
    msg["To"] = to_email
    msg["Reply-To"] = smtp_user
    msg["List-Unsubscribe"] = f"<mailto:{smtp_user}?subject=unsubscribe>"

    body = BODY_TEMPLATE.format(
        name=greeting_name(creator),
        personalized_line=personalized_line(creator),
        domain=REQUIRED_DOMAIN,
        site_url=REQUIRED_SITE_URL,
    )
    msg.attach(MIMEText(body, "plain", "utf-8"))
    return msg


def verify_deliverability(msg: MIMEMultipart) -> list[str]:
    issues = []
    body = msg.get_payload()[0].get_payload(decode=True).decode("utf-8")
    if len(body) < 100:
        issues.append("Body too short")
    spam_words = ["FREE!!!", "ACT NOW", "100% guaranteed", "click here"]
    for w in spam_words:
        if w.lower() in body.lower():
            issues.append(f"Spam trigger: {w}")
    if not msg.get("Reply-To"):
        issues.append("Missing Reply-To")
    if REQUIRED_SITE_URL not in body:
        issues.append(f"Missing site URL {REQUIRED_SITE_URL}")
    return issues


def check_domain_live(timeout: int = 10) -> tuple[bool, str]:
    """Verify production site responds at getfocusdock.com."""
    try:
        ctx = ssl.create_default_context()
        req = urllib.request.Request(
            REQUIRED_SITE_URL,
            headers={"User-Agent": "FocusDock-Outreach-Checker/1.0"},
        )
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            if 200 <= resp.status < 400:
                return True, f"{REQUIRED_SITE_URL} returned HTTP {resp.status}"
            return False, f"{REQUIRED_SITE_URL} returned HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            return True, f"{REQUIRED_SITE_URL} is reachable (HTTP {e.code})"
        return False, f"HTTP error: {e.code} {e.reason}"
    except Exception as e:
        return False, str(e)


def domain_send_allowed() -> tuple[bool, list[str]]:
    """Hard gate: no outreach until domain is explicitly enabled AND live."""
    reasons = []
    domain_ready = os.environ.get("DOMAIN_READY", "").lower() == "true"
    if not domain_ready:
        reasons.append(
            "DOMAIN_READY is not 'true'. Complete LAUNCH_CHECKLIST.md Steps 1-5 first, "
            "then: export DOMAIN_READY=true"
        )

    live, detail = check_domain_live()
    if not live:
        reasons.append(f"Domain not reachable: {detail}")

    smtp_user = os.environ.get("SMTP_USER", f"hello@{REQUIRED_DOMAIN}")
    if not smtp_user.endswith(f"@{REQUIRED_DOMAIN}"):
        reasons.append(
            f"SMTP_USER must be @{REQUIRED_DOMAIN} (got {smtp_user}). "
            "Zoho mailbox must match live domain."
        )

    if not os.environ.get("SMTP_APP_PASSWORD", ""):
        reasons.append("SMTP_APP_PASSWORD not set")

    return len(reasons) == 0, reasons


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--check-domain", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--force",
        action="store_true",
        help="DANGER: bypass domain gate (not recommended)",
    )
    args = parser.parse_args()

    if args.check_domain:
        live, detail = check_domain_live()
        allowed, reasons = domain_send_allowed()
        print(f"Domain check: {detail}")
        print(f"Send allowed: {allowed}")
        if reasons:
            print("Blockers:")
            for r in reasons:
                print(f"  - {r}")
        return

    creators = load_creators()
    log = load_log()
    targets = get_sendable(creators, log, args.limit)

    email_count = sum(
        1 for c in creators
        if (c.get("contact_email") or "").strip() and c.get("contact_type") == "email"
    )
    print(f"List: {len(creators)} creators, {email_count} with public emails")
    print(f"Sendable now (high/medium email): {len(targets)}")

    if not targets:
        print("No sendable targets (need email + high/medium priority + not already sent).")
        return

    smtp_user = os.environ.get("SMTP_USER", f"hello@{REQUIRED_DOMAIN}")

    print(f"\nPreviewing {len(targets)} email(s):")
    for i, c in enumerate(targets):
        msg = build_message(c["contact_email"], c, smtp_user)
        issues = verify_deliverability(msg)
        name = greeting_name(c)
        print(f"\n--- [{i+1}] {c['channel_name']} <{c['contact_email']}> ---")
        print(f"  Greeting: Hi {name},")
        if c.get("personalized_opening"):
            print(f"  Personalization: {c['personalized_opening'][:80]}...")
        if issues:
            print(f"  WARNINGS: {issues}")
        body = msg.get_payload()[0].get_payload(decode=True).decode("utf-8")
        print(body[:400] + "...")

    if args.dry_run or not args.send:
        print("\n[DRY RUN] No emails sent.")
        print("To send after domain is live: export DOMAIN_READY=true && python email-campaign.py --send")
        return

    if not args.force:
        allowed, reasons = domain_send_allowed()
        if not allowed:
            print("\n[BLOCKED] Email send prevented — domain not ready:")
            for r in reasons:
                print(f"  ✗ {r}")
            print("\nComplete LAUNCH_CHECKLIST.md, then:")
            print("  export DOMAIN_READY=true")
            print("  export SMTP_APP_PASSWORD=your_zoho_app_password")
            print("  python email-campaign.py --send --limit 3")
            return

    smtp_pass = os.environ.get("SMTP_APP_PASSWORD", "")
    if not smtp_pass:
        print("ERROR: Set SMTP_APP_PASSWORD env var with Zoho app-specific password.")
        return

    print("\n[SENDING] Domain gate passed. Starting outreach...")
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(smtp_user, smtp_pass)
        for i, c in enumerate(targets):
            msg = build_message(c["contact_email"], c, smtp_user)
            issues = verify_deliverability(msg)
            if issues:
                log["skipped"].append({
                    "creator": c["channel_name"],
                    "reason": issues,
                    "date": datetime.now().isoformat(),
                })
                save_log(log)
                continue
            server.send_message(msg)
            log["sent"].append({
                "creator": c["channel_name"],
                "email": c["contact_email"],
                "date": datetime.now().isoformat(),
            })
            save_log(log)
            print(f"Sent to {c['contact_email']}")
            if i < len(targets) - 1:
                time.sleep(MIN_DELAY_SECONDS)

    sent_today = len([
        s for s in log["sent"]
        if s.get("date", "").startswith(datetime.now().strftime("%Y-%m-%d"))
    ])
    print(f"\nDone. Sent {sent_today} today.")


if __name__ == "__main__":
    main()