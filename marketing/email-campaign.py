#!/usr/bin/env python3
"""
Focus Dock cold outreach email campaign.
Sends via Gmail SMTP (blacksheepdesignscontact@gmail.com).

IMPORTANT: Emails are BLOCKED until the domain is live.
Set DOMAIN_READY=true only after completing LAUNCH_CHECKLIST.md Steps 1-5.

Setup:
  1. Register getfocusdock.com + deploy site
  2. Create Gmail app password for blacksheepdesignscontact@gmail.com
  3. export DOMAIN_READY=true SMTP_APP_PASSWORD=...

Usage:
  python email-campaign.py --dry-run          # preview emails (always safe)
  python email-campaign.py --send             # send (requires DOMAIN_READY=true)
  python email-campaign.py --send --limit 3   # send first 3 (testing)
  python email-campaign.py --check-domain     # verify domain is reachable
"""

import argparse
import json
import os
import random
import smtplib
import sys
import ssl
import time
import urllib.error
import urllib.request
from datetime import datetime, timedelta
from typing import Optional
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

from outreach_utils import subscriber_count

DEFAULT_SMTP_USER = "blacksheepdesignscontact@gmail.com"
SMTP_HOST = os.environ.get("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USE_SSL = os.environ.get("SMTP_USE_SSL", "").lower() in ("1", "true", "yes")

# Gmail personal account limits — https://support.google.com/mail/answer/22839
# Hard cap: 500 emails/day (rolling 24h). We stay under with buffers.
GMAIL_DAILY_MAX = int(os.environ.get("GMAIL_DAILY_MAX", "400"))
GMAIL_HOURLY_MAX = int(os.environ.get("GMAIL_HOURLY_MAX", "50"))
GMAIL_BATCH_EVERY = int(os.environ.get("GMAIL_BATCH_EVERY", "25"))
GMAIL_BATCH_PAUSE_SECONDS = int(os.environ.get("GMAIL_BATCH_PAUSE", "180"))
# Warmup ramp (first campaign / cold outreach): slow start, then max safe throughput.
GMAIL_WARMUP_TIERS = (
    (10, 120),   # emails 1–10:  ~30/hour
    (40, 90),    # emails 11–40:  ~40/hour
    (9999, 72),  # emails 41+:    ~50/hour (matches GMAIL_HOURLY_MAX)
)

REQUIRED_DOMAIN = "getfocusdock.com"
REQUIRED_SITE_URL = f"https://{REQUIRED_DOMAIN}"

MARKETING_DIR = Path(__file__).parent
LIST_PATH = MARKETING_DIR / "creator-outreach-list.json"
MASTER_PATH = MARKETING_DIR / "affiliate-contacts-master.json"
FUTURE_PATH = MARKETING_DIR / "future-outreach-queue.json"
LOG_PATH = MARKETING_DIR / "email-send-log.json"
ENV_PATHS = (
    MARKETING_DIR / "outreach.env",
    MARKETING_DIR / ".env",
)

SUBJECT = "Quick idea for your ADHD/Notion audience"

BODY_TEMPLATE = """Hi {name},

{personalized_line}

I'm launching Focus Dock — a short PDF for viewers who keep abandoning ADHD Notion setups. It's not another template; it's a recovery protocol (minimal databases, executive-dysfunction-friendly tasks, no streak guilt). Complements what you already teach.

If it's a fit, I'd love to explore a paid mention or segment. Happy to send a free copy first.

Affiliate terms: 40% commission ($10.80 per $27 sale). Even a handful of conversions from your audience can add up quickly.

— Cameron
{reply_email}
"""


def load_dotenv_files():
    """Load SMTP credentials from local env files (does not override existing env)."""
    for path in ENV_PATHS:
        if not path.exists():
            continue
        for line in path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key and key not in os.environ:
                os.environ[key] = value


def load_creators(source: str = "outreach"):
    if source == "master":
        path = MASTER_PATH
    elif source == "future":
        path = FUTURE_PATH
    else:
        path = LIST_PATH
    with open(path) as f:
        data = json.load(f)
    if source in ("master", "future"):
        return [normalize_master_contact(c) for c in data]
    return data


def normalize_master_contact(c: dict) -> dict:
    """Map master list fields to outreach list shape."""
    out = dict(c)
    if "subscribers" not in out and "subscribers_or_audience" in out:
        out["subscribers"] = subscriber_count(c) or 0
    if "personalized_opening" not in out:
        out["personalized_opening"] = ""
    return out


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


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def parse_log_date(value: str) -> Optional[datetime]:
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


def sent_since(log: dict, *, hours: Optional[float] = None, days: Optional[float] = None) -> int:
    cutoff = datetime.now()
    if hours is not None:
        cutoff -= timedelta(hours=hours)
    elif days is not None:
        cutoff -= timedelta(days=days)
    else:
        return len(log.get("sent", []))

    count = 0
    for entry in log.get("sent", []):
        sent_at = parse_log_date(entry.get("date", ""))
        if sent_at and sent_at >= cutoff:
            count += 1
    return count


def delay_for_send_index(sent_today_before: int) -> int:
    """Seconds to wait before the next send; includes small jitter."""
    send_number = sent_today_before + 1
    delay = GMAIL_WARMUP_TIERS[-1][1]
    for up_to, seconds in GMAIL_WARMUP_TIERS:
        if send_number <= up_to:
            delay = seconds
            break
    jitter = random.randint(-5, 8)
    return max(45, delay + jitter)


def wait_for_hourly_capacity(log: dict):
    while sent_since(log, hours=24) >= GMAIL_DAILY_MAX:
        print(f"[THROTTLE] Daily cap ({GMAIL_DAILY_MAX}) reached — stopping until tomorrow.")
        return False

    while sent_since(log, hours=1) >= GMAIL_HOURLY_MAX:
        print(f"[THROTTLE] Hourly cap ({GMAIL_HOURLY_MAX}/hr) — waiting 60s...")
        time.sleep(60)
    return True


def print_gmail_policy():
    print("Gmail send policy:")
    print(f"  Daily max:     {GMAIL_DAILY_MAX} (Gmail hard limit: 500/rolling 24h)")
    print(f"  Hourly max:    {GMAIL_HOURLY_MAX}")
    print(f"  Warmup delays: 120s→90s→72s between sends (+ jitter)")
    print(f"  Batch pause:   {GMAIL_BATCH_PAUSE_SECONDS}s every {GMAIL_BATCH_EVERY} sends")


def get_sendable(creators, log, limit=None, include_all_priorities=False):
    sent_emails = {e["email"].lower() for e in log["sent"]}
    sent_24h = sent_since(log, hours=24)
    remaining_today = max(0, GMAIL_DAILY_MAX - sent_24h)

    targets = []
    seen = set()
    for c in creators:
        if not include_all_priorities and c.get("outreach_priority") not in ("high", "medium"):
            continue
        email = (c.get("contact_email") or "").strip().lower()
        if not email or c.get("contact_type") != "email":
            continue
        if email in sent_emails or email in seen:
            continue
        seen.add(email)
        targets.append(c)

    targets.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x.get("outreach_priority"), 9),
            -(subscriber_count(x) or 0),
        )
    )

    requested = limit if limit is not None else len(targets)
    cap = min(requested, remaining_today)
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
        reply_email=smtp_user,
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
    if "http://" in body.lower() or "https://" in body.lower():
        issues.append("Body contains URL (withheld until site is live)")
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

    smtp_user = os.environ.get("SMTP_USER", DEFAULT_SMTP_USER)
    if "@" not in smtp_user:
        reasons.append(f"SMTP_USER must be a valid email address (got {smtp_user})")

    if not os.environ.get("SMTP_APP_PASSWORD", ""):
        reasons.append("SMTP_APP_PASSWORD not set (Gmail app password)")

    return len(reasons) == 0, reasons


def connect_smtp(smtp_user: str, smtp_pass: str):
    if SMTP_USE_SSL or SMTP_PORT == 465:
        server = smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT if SMTP_PORT != 587 else 465)
        server.login(smtp_user, smtp_pass)
        return server

    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(smtp_user, smtp_pass)
    return server


def safe_quit(server):
    if server is None:
        return
    try:
        server.quit()
    except Exception:
        try:
            server.close()
        except Exception:
            pass


RECONNECT_ERRORS = (
    smtplib.SMTPServerDisconnected,
    smtplib.SMTPSenderRefused,
    smtplib.SMTPDataError,
    smtplib.SMTPConnectError,
    smtplib.SMTPHeloError,
    OSError,
)


def send_one_email(smtp_user: str, smtp_pass: str, msg: MIMEMultipart):
    """Send a single email with fresh/reconnected SMTP (avoids Gmail idle timeout)."""
    last_exc = None
    for attempt in range(4):
        server = None
        try:
            server = connect_smtp(smtp_user, smtp_pass)
            server.send_message(msg)
            safe_quit(server)
            return
        except RECONNECT_ERRORS as exc:
            last_exc = exc
            safe_quit(server)
            err = str(exc).lower()
            print(f"[SMTP ERROR] {exc}", flush=True)
            if "limit" in err or "452" in err or "daily" in err:
                print("Gmail rate limit — pausing 30 minutes...", flush=True)
                time.sleep(1800)
            elif attempt < 3:
                wait = 15 * (attempt + 1)
                print(f"Reconnecting in {wait}s (attempt {attempt + 2}/4)...", flush=True)
                time.sleep(wait)
            else:
                raise
    if last_exc:
        raise last_exc


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--send", action="store_true")
    parser.add_argument("--check-domain", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument(
        "--source",
        choices=("outreach", "master", "future"),
        default="outreach",
        help="List: outreach (default), master (all), future (unsent queue)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Send all email contacts (all priorities, master list, ignore daily cap)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="DANGER: bypass domain gate (not recommended)",
    )
    args = parser.parse_args()
    load_dotenv_files()

    if args.all:
        args.source = "master"
        if args.limit is None:
            args.limit = 10_000

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

    creators = load_creators(args.source)
    log = load_log()
    targets = get_sendable(
        creators,
        log,
        args.limit,
        include_all_priorities=args.all,
    )

    email_count = sum(
        1 for c in creators
        if (c.get("contact_email") or "").strip() and c.get("contact_type") == "email"
    )
    smtp_user = os.environ.get("SMTP_USER", DEFAULT_SMTP_USER)
    print(f"SMTP: {smtp_user} via {SMTP_HOST}:{SMTP_PORT}")
    print_gmail_policy()
    sent_24h = sent_since(log, hours=24)
    print(f"Sent last 24h: {sent_24h}/{GMAIL_DAILY_MAX}")
    print(f"List ({args.source}): {len(creators)} creators, {email_count} with public emails")
    queue_label = "all email contacts" if args.all else "high/medium email"
    print(f"Sendable now ({queue_label}): {len(targets)}")

    if not targets:
        print("No sendable targets (need email + high/medium priority + not already sent).")
        return

    preview_count = min(len(targets), 3 if args.send else len(targets))
    print(f"\nPreviewing {preview_count} of {len(targets)} email(s):")
    for i, c in enumerate(targets[:preview_count]):
        msg = build_message(c["contact_email"], c, smtp_user)
        issues = verify_deliverability(msg)
        name = greeting_name(c)
        subs = subscriber_count(c)
        print(f"\n--- [{i+1}] {c['channel_name']} <{c['contact_email']}> ({subs or '?'} subs) ---")
        print(f"  Greeting: Hi {name},")
        if c.get("personalized_opening"):
            print(f"  Personalization: {c['personalized_opening'][:80]}...")
        if issues:
            print(f"  WARNINGS: {issues}")
        body = msg.get_payload()[0].get_payload(decode=True).decode("utf-8")
        print(body[:400] + ("..." if len(body) > 400 else ""))

    if args.dry_run or not args.send:
        print("\n[DRY RUN] No emails sent.")
        print("To send after domain is live:")
        print("  export DOMAIN_READY=true")
        print(f"  export SMTP_USER={DEFAULT_SMTP_USER}")
        print("  export SMTP_APP_PASSWORD=your_gmail_app_password")
        print("  python email-campaign.py --send")
        return

    if not args.force:
        allowed, reasons = domain_send_allowed()
        if not allowed:
            print("\n[BLOCKED] Email send prevented — domain not ready:")
            for r in reasons:
                print(f"  ✗ {r}")
            print("\nComplete LAUNCH_CHECKLIST.md, then:")
            print("  export DOMAIN_READY=true")
            print(f"  export SMTP_USER={DEFAULT_SMTP_USER}")
            print("  export SMTP_APP_PASSWORD=your_gmail_app_password")
            print("  python email-campaign.py --send --limit 3")
            return

    smtp_pass = os.environ.get("SMTP_APP_PASSWORD", "")
    if not smtp_pass:
        print("ERROR: Set SMTP_APP_PASSWORD env var with Gmail app password.")
        return

    print(f"\n[SENDING] Starting outreach to {len(targets)} contacts...")
    try:
        test_server = connect_smtp(smtp_user, smtp_pass)
        safe_quit(test_server)
    except smtplib.SMTPAuthenticationError:
        print(
            "\n[AUTH FAILED] Gmail rejected the login.\n"
            "Regular account passwords do not work for SMTP — you need a 16-character\n"
            "Gmail App Password (Google Account → Security → App passwords).\n"
            "Save it in marketing/outreach.env as SMTP_APP_PASSWORD=..."
        )
        return

    sent_this_run = 0
    try:
        for i, c in enumerate(targets):
            if not wait_for_hourly_capacity(log):
                print("[STOPPED] Daily Gmail limit reached. Re-run tomorrow for remaining contacts.")
                break

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

            send_one_email(smtp_user, smtp_pass, msg)

            log["sent"].append({
                "creator": c["channel_name"],
                "email": c["contact_email"],
                "date": datetime.now().isoformat(),
            })
            save_log(log)
            sent_this_run += 1
            sent_24h = sent_since(log, hours=24)
            print(
                f"Sent to {c['contact_email']} "
                f"({sent_24h}/{GMAIL_DAILY_MAX} today, "
                f"{sent_since(log, hours=1)}/{GMAIL_HOURLY_MAX} this hour)",
                flush=True,
            )

            if i >= len(targets) - 1:
                break

            if sent_this_run % GMAIL_BATCH_EVERY == 0:
                print(
                    f"[BATCH PAUSE] {GMAIL_BATCH_PAUSE_SECONDS}s after "
                    f"{sent_this_run} sends (keeps Gmail happy)...",
                    flush=True,
                )
                time.sleep(GMAIL_BATCH_PAUSE_SECONDS)

            delay = delay_for_send_index(sent_24h)
            print(f"[WAIT] {delay}s before next send...", flush=True)
            time.sleep(delay)
    finally:
        pid_file = MARKETING_DIR / "outreach-send.pid"
        if pid_file.exists():
            pid_file.unlink()

    sent_24h = sent_since(log, hours=24)
    remaining = max(0, len(targets) - sent_this_run)
    print(f"\nDone. Sent {sent_this_run} this run ({sent_24h}/{GMAIL_DAILY_MAX} in last 24h).")
    if remaining:
        print(f"{remaining} still queued — re-run tomorrow: python3 email-campaign.py --all --send --force")


if __name__ == "__main__":
    main()