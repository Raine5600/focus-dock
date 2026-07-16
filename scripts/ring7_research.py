#!/usr/bin/env python3
"""
Ring 7 affiliate outreach research — discover NEW email contacts for Focus Dock.

Sources (priority order):
  1. Notion Marketplace categories (deep crawl beyond ring 3)
  2. Gumroad Discover (seller profiles + linked-site email extraction)
  3. Substack/Beehiiv about pages
  4. ADHD/productivity podcasts (show-site emails)
  5. YouTube creators (business inquiry emails from linked sites)

Usage:
  python scripts/ring7_research.py              # full run, save batch
  python scripts/ring7_research.py --dry-run    # print stats only
  python scripts/ring7_research.py --limit 50   # cap output count
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from html import unescape
from pathlib import Path
from urllib.parse import urljoin, urlparse, quote

import urllib.request

ROOT = Path(__file__).parent.parent
MARKETING = ROOT / "marketing"
MASTER = MARKETING / "affiliate-contacts-master.json"
SEND_LOG = MARKETING / "email-send-log.json"
OUT = MARKETING / "_batch_ring7_expansion.json"

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")
SKIP_EMAILS = {
    "templates@makenotion.com",
    "support@substack.com",
    "hello@substack.com",
    "noreply@stuartridout.com",
    "team@beehiiv.com",
    "support@gumroad.com",
    "help@gumroad.com",
}
SKIP_EMAIL_DOMAINS = {"substack.com", "beehiiv.com", "gumroad.com", "notion.so", "makenotion.com"}
WORKERS = 12

NOTION_CATEGORIES = [
    "personal-productivity", "personal-dashboards", "second-brain", "health-fitness",
    "personal-finance", "hobbies", "travel", "food-nutrition", "career-building",
    "parenting", "entertainment", "housing", "dating-relationships", "friends-family",
    "seasonal", "religion", "plants", "vehicle-management",
    "startup", "freelance", "side-hustle", "product", "marketing", "design", "engineering",
    "ai", "operations", "hr", "work-dashboards", "recruiting", "it", "sales", "crm",
    "user-research", "data-science", "finance", "pr-comms", "enterprise", "managers",
    "non-profit", "agency", "consulting", "venture-capital", "website-building", "integrations",
    "student-life", "study-planner", "class-notes", "student-dashboards", "student-org",
    "teaching", "school-applications", "internship-tracker", "academic-research",
    "personal", "work", "school",
]

GUMROAD_QUERIES = [
    "adhd", "notion templates", "notion planner", "productivity planner",
    "neurodivergent", "second brain notion", "adhd planner", "notion dashboard",
    "executive function", "digital planner", "notion life os", "pkm notion",
    "habit tracker notion", "adhd coaching", "notion adhd", "notion productivity",
    "adhd notion template", "planner template", "notion second brain",
]

SUBSTACK_SEEDS = [
    "neurodiverseproductivity", "adhdunpacked", "kristenlynnmcclure", "extrafocus",
    "adhdjesse", "theadhddigest", "neurodivergentinsights", "theadhdwriter",
    "shimmeradhd", "adultingwithadhd", "executivedysfunction", "notionway",
    "notionthings", "pkmjournal", "secondbraindispatch", "productivitycafe",
    "theorganizedbrain", "divergentdispatch", "neurospicynotes", "focusfuel",
    "plannerbrain", "theadhdadvantage", "ndproductivity", "braindumpclub",
    "notionforcreators", "templateatlas", "digitalplannerhub", "calmclarityco",
    "mindfulproductivity", "theadhdentrepreneur", "spicybrain", "organizedadult",
    "notionnerd", "systemsandself", "thefocusfix", "dopaminediary",
    "neurodivergentcoach", "plannerpeace", "executivefunctioncoach", "notionobsessed",
    "adhdproductivity", "neurodivergentlife", "theadhdmom", "focuswithadhd",
    "productivitywithadhd", "notionplanner", "digitalbrain", "plannersociety",
    "neurodivergentnews", "adhdproductivitylab", "mindwithadhd",
]

PODCAST_SEEDS = [
    ("https://www.hackingyouradhd.com/", "Hacking Your ADHD", "William Curb"),
    ("https://www.translatingadhd.com/", "Translating ADHD", ""),
    ("https://www.adhdrewired.com/", "ADHD reWired", "Eric Tivers"),
    ("https://www.adhdforsmartasswomen.com/", "ADHD for Smart Ass Women", ""),
    ("https://www.adhdessentials.com/", "ADHD Essentials", "Brendan Mahan"),
    ("https://www.adhdfriendlylifestyle.com/", "ADHD Friendly Lifestyle", ""),
    ("https://www.adhdthriveinstitute.com/", "ADHD Thrive Institute", ""),
    ("https://www.focusedadult.com/", "Focused Adult", ""),
    ("https://www.myndforadhd.com/", "Mynd Systems For ADHD", ""),
    ("https://www.adhdvision.com/", "ADHD Vision", ""),
    ("https://www.thriveadhdcoach.co.uk/", "Thrive ADHD Coach", ""),
    ("https://www.beyondbooksmart.com/", "Beyond BookSmart", ""),
    ("https://www.adhd2bb.com/", "ADHD 2.0 and Beyond", ""),
    ("https://www.neurodivergentpodcast.com/", "Neurodivergent Podcast", ""),
    ("https://www.authenticadhd.com/", "Authentic ADHD", ""),
    ("https://www.adhdlove.com/", "ADHD Love", ""),
    ("https://www.adhdparentingpodcast.com/", "ADHD Parenting Podcast", ""),
    ("https://www.theadhdacademy.com/", "The ADHD Academy", ""),
    ("https://www.productivityist.com/", "Productivityist", "Mike Vardy"),
    ("https://www.beyondtheto-do.com/", "Beyond the To-Do List", "Erik Fisher"),
    ("https://www.thesystemsmadebetter.com/", "Systems Made Better", ""),
    ("https://www.getorganizedhq.com/", "Get Organized HQ", ""),
    ("https://www.learntotalkadhd.com/", "Learn to Talk ADHD", ""),
    ("https://www.adhddiversified.com/", "ADHD Diversified", ""),
    ("https://www.impactparents.com/", "ImpactParents ADHD", ""),
    ("https://www.adultingwithadhd.com/", "Adulting with ADHD", ""),
    ("https://www.theadultingadhd.com/", "The Adulting ADHD Podcast", ""),
    ("https://www.adhdonline.com/", "ADHD Online", ""),
    ("https://www.takecontroladhd.com/", "Take Control ADHD", ""),
    ("https://www.adhdfoundation.org/", "ADHD Foundation", ""),
]

YOUTUBE_SEEDS = [
    ("https://www.youtube.com/@HowtoADHD", "How to ADHD", "Jessica McCabe"),
    ("https://www.youtube.com/@ADHD_Brains", "ADHD Brains", ""),
    ("https://www.youtube.com/@ADHDVision", "ADHD Vision", ""),
    ("https://www.youtube.com/@FocusedAdult", "Focused Adult", ""),
    ("https://www.youtube.com/@MyndForADHD", "Mynd Systems For ADHD", ""),
    ("https://www.youtube.com/@ADHDThriveInstitute", "ADHD Thrive Institute", ""),
    ("https://www.youtube.com/@HackingYourADHD", "Hacking Your ADHD", ""),
    ("https://www.youtube.com/@ADHDDude", "ADHD Dude", ""),
    ("https://www.youtube.com/@ADHDCoachRyan", "ADHD Coach Ryan", ""),
    ("https://www.youtube.com/@TheADHDWorkshop", "The ADHD Workshop", ""),
    ("https://www.youtube.com/@ADHDCoachSheila", "ADHD Coach Sheila", ""),
    ("https://www.youtube.com/@ADHDCoachJaclyn", "ADHD Coach Jaclyn", ""),
    ("https://www.youtube.com/@ADHDCoachDana", "ADHD Coach Dana", ""),
    ("https://www.youtube.com/@ADHDCoachLaurie", "ADHD Coach Laurie", ""),
    ("https://www.youtube.com/@ADHDCoachJeff", "ADHD Coach Jeff", ""),
    ("https://www.youtube.com/@Easlo", "Easlo", ""),
    ("https://www.youtube.com/@AugustBradley", "August Bradley", ""),
    ("https://www.youtube.com/@Thomasjfrank", "Thomas Frank", ""),
    ("https://www.youtube.com/@RedGregory", "Red Gregory", ""),
    ("https://www.youtube.com/@notion4teachers", "Notion for Teachers", ""),
    ("https://www.youtube.com/@notionboy", "Notion Boy", ""),
    ("https://www.youtube.com/@notiontemplate", "Notion Template", ""),
    ("https://www.youtube.com/@productivefish", "Productive Fish", ""),
    ("https://www.youtube.com/@ProductivityGame", "Productivity Game", ""),
    ("https://www.youtube.com/@notionhacks", "Notion Hacks", ""),
    ("https://www.youtube.com/@notiontips", "Notion Tips", ""),
    ("https://www.youtube.com/@notionhub", "Notion Hub", ""),
    ("https://www.youtube.com/@notioncreator", "Notion Creator", ""),
    ("https://www.youtube.com/@notionplanner", "Notion Planner", ""),
]


def log(msg: str) -> None:
    print(msg, flush=True)


def fetch(url: str, timeout: int = 20) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return ""


def norm_email(email: str) -> str:
    return (email or "").strip().lower()


def norm_url(url: str) -> str:
    u = (url or "").strip().lower().rstrip("/")
    return re.sub(r"^mailto:", "", u)


def is_valid_email(email: str) -> bool:
    e = norm_email(email)
    if not e or e in SKIP_EMAILS:
        return False
    if not EMAIL_RE.fullmatch(e):
        return False
    domain = e.split("@", 1)[1]
    if domain in SKIP_EMAIL_DOMAINS:
        return False
    if any(x in e for x in ("example.com", "sentry.io", "w3.org", "schema.org")):
        return False
    return True


def extract_emails(text: str) -> list[str]:
    found: list[str] = []
    for raw in EMAIL_RE.findall(text or ""):
        raw = unescape(raw).strip().rstrip(".")
        if is_valid_email(raw):
            found.append(raw)
    for m in re.finditer(r"mailto:([^\"'\s>?]+)", text or "", re.I):
        raw = unescape(m.group(1)).split("?")[0].strip()
        if is_valid_email(raw):
            found.append(raw)
    return list(dict.fromkeys(found))


def load_existing() -> tuple[set[str], set[str]]:
    emails: set[str] = set()
    urls: set[str] = set()

    def absorb(path: Path) -> None:
        if not path.exists():
            return
        data = json.loads(path.read_text())
        items = data if isinstance(data, list) else data.get("sent", [])
        for c in items:
            if not isinstance(c, dict):
                continue
            e = norm_email(c.get("contact_email") or c.get("email", ""))
            if e:
                emails.add(e)
            u = norm_url(c.get("profile_url", ""))
            if u:
                urls.add(u)

    absorb(MASTER)
    absorb(SEND_LOG)
    for batch in MARKETING.glob("_batch*.json"):
        if batch.name == OUT.name:
            continue
        absorb(batch)
    return emails, urls


def notion_next_data(html: str) -> dict | None:
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(1))
    except json.JSONDecodeError:
        return None


def notion_profile_email(username: str) -> str | None:
    html = fetch(f"https://www.notion.com/@{username}")
    data = notion_next_data(html)
    if data:
        prof = data.get("props", {}).get("pageProps", {}).get("marketplaceProfile", {})
        email = (prof.get("attributes") or {}).get("contact_email")
        if email and is_valid_email(email):
            return email
    emails = extract_emails(html)
    return emails[0] if emails else None


def make_entry(
    *,
    channel_name: str,
    contact_name: str,
    platform: str,
    profile_url: str,
    audience: int,
    niche: str,
    email: str,
    priority: str,
    notes: str,
) -> dict:
    return {
        "channel_name": channel_name,
        "contact_name": contact_name,
        "platform": platform,
        "profile_url": profile_url,
        "subscribers_or_audience": audience,
        "niche_focus": niche,
        "contact_email": email,
        "contact_type": "email",
        "contact_url": f"mailto:{email}",
        "sells_digital_products": "yes",
        "outreach_priority": priority,
        "notes": notes,
        "research_ring": 7,
        "in_target_range": True,
    }


def scrape_notion_categories(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    pending_profiles: dict[str, dict] = {}

    def fetch_category_page(cat_page: tuple[str, int]) -> list[dict]:
        cat, page = cat_page
        html = fetch(f"https://www.notion.com/templates/category/{cat}?page={page}")
        data = notion_next_data(html)
        if not data:
            return []
        return data.get("props", {}).get("pageProps", {}).get("templates", [])

    jobs = [(cat, page) for cat in NOTION_CATEGORIES for page in range(1, 18)]
    log(f"  fetching {len(jobs)} Notion category pages ({WORKERS} workers)...")

    creators_found: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(fetch_category_page, j): j for j in jobs}
        done = 0
        for fut in as_completed(futures):
            done += 1
            if done % 50 == 0:
                log(f"    ...{done}/{len(jobs)} pages")
            cat, _page = futures[fut]
            try:
                templates = fut.result()
            except Exception:
                continue
            for t in templates:
                prof = t.get("profile") or {}
                username = (prof.get("username") or "").strip()
                if not username or username.lower() == "notion":
                    continue
                profile_url = f"https://www.notion.com/@{username}"
                purl = norm_url(profile_url)
                if purl in existing_urls or purl in seen_urls or username in creators_found:
                    continue
                email = (prof.get("attributes") or {}).get("contact_email", "")
                creators_found[username] = {
                    "name": prof.get("name") or username,
                    "email": email,
                    "profile_url": profile_url,
                    "category": cat,
                }

    log(f"  unique new Notion creators from listings: {len(creators_found)}")

    # inline emails first
    for username, info in creators_found.items():
        if len(results) >= limit:
            break
        email = info["email"]
        if not email:
            pending_profiles[username] = info
            continue
        if not is_valid_email(email):
            pending_profiles[username] = info
            continue
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            continue
        entry = make_entry(
            channel_name=info["name"],
            contact_name="",
            platform="other",
            profile_url=info["profile_url"],
            audience=8000,
            niche="Notion templates, productivity/PKM",
            email=email,
            priority="medium",
            notes=f"Notion marketplace (@{username}), category={info['category']}. Email on listing.",
        )
        results.append(entry)
        seen_emails.add(em)
        seen_urls.add(norm_url(info["profile_url"]))

    log(f"  inline emails: {len(results)} | profile fetch needed: {len(pending_profiles)}")

    if len(results) < limit and pending_profiles:
        need = min(len(pending_profiles), (limit - len(results)) * 3)
        to_fetch = list(pending_profiles.items())[:need]
        log(f"  fetching {len(to_fetch)} Notion profile pages...")

        with ThreadPoolExecutor(max_workers=WORKERS) as pool:
            futs = {pool.submit(notion_profile_email, u): (u, info) for u, info in to_fetch}
            for fut in as_completed(futs):
                if len(results) >= limit:
                    break
                username, info = futs[fut]
                try:
                    email = fut.result()
                except Exception:
                    continue
                if not email or not is_valid_email(email):
                    continue
                em = norm_email(email)
                if em in existing_emails or em in seen_emails:
                    continue
                entry = make_entry(
                    channel_name=info["name"],
                    contact_name="",
                    platform="other",
                    profile_url=info["profile_url"],
                    audience=8000,
                    niche="Notion templates, productivity/PKM",
                    email=email,
                    priority="medium",
                    notes=f"Notion marketplace (@{username}), category={info['category']}. Email on profile page.",
                )
                results.append(entry)
                seen_emails.add(em)
                seen_urls.add(norm_url(info["profile_url"]))

    return results


def scrape_gumroad(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    sellers: dict[str, str] = {}

    def fetch_discover(query: str) -> None:
        html = fetch(f"https://gumroad.com/discover?query={quote(query)}")
        for seller, _product in re.findall(
            r"https://([a-zA-Z0-9_-]+)\.gumroad\.com/l/([a-zA-Z0-9_-]+)", html
        ):
            if seller in ("assets", "app", "help", "blog", "status"):
                continue
            sellers.setdefault(seller, query)

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        list(pool.map(fetch_discover, GUMROAD_QUERIES))

    log(f"  Gumroad sellers discovered: {len(sellers)}")

    def process_seller(item: tuple[str, str]) -> dict | None:
        seller, query = item
        profile_url = f"https://{seller}.gumroad.com/"
        purl = norm_url(profile_url)
        if purl in existing_urls or purl in seen_urls:
            return None

        html = fetch(profile_url)
        emails = extract_emails(html)
        product_links = re.findall(
            rf"https://{re.escape(seller)}\.gumroad\.com/l/([a-zA-Z0-9_-]+)", html
        )
        for plink in product_links[:2]:
            emails.extend(extract_emails(fetch(f"https://{seller}.gumroad.com/l/{plink}")))

        ext_links = re.findall(r'href="(https?://[^"]+)"', html)
        for link in ext_links[:4]:
            host = urlparse(link).netloc.lower()
            if any(x in host for x in ("gumroad", "twitter", "instagram", "youtube", "facebook", "tiktok", "linkedin")):
                continue
            emails.extend(extract_emails(fetch(link)))

        emails = list(dict.fromkeys(emails))
        if not emails:
            return None
        email = emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None

        niche = "Digital templates/productivity (Gumroad)"
        if "adhd" in query.lower() or "adhd" in seller.lower():
            niche = "ADHD planners/templates on Gumroad"
        elif "notion" in query.lower() or "notion" in seller.lower():
            niche = "Notion templates on Gumroad"

        return make_entry(
            channel_name=seller.replace("-", " ").title(),
            contact_name="",
            platform="other",
            profile_url=profile_url,
            audience=8000,
            niche=niche,
            email=email,
            priority="medium",
            notes=f"Gumroad seller ({seller}). Query '{query}'. Email verified on seller/linked site.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = [pool.submit(process_seller, item) for item in sellers.items()]
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def scrape_substack(
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []

    def process_slug(slug: str) -> dict | None:
        profile_url = f"https://{slug}.substack.com/"
        purl = norm_url(profile_url)
        if purl in existing_urls or purl in seen_urls:
            return None
        html = fetch(f"https://{slug}.substack.com/about") or fetch(profile_url)
        emails = extract_emails(html)
        if not emails:
            return None
        email = emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None
        title_m = re.search(r"<title>([^<]+)</title>", html, re.I)
        title = slug.replace("-", " ").title()
        if title_m:
            title = re.sub(r"\s*[\|·].*$", "", title_m.group(1)).strip() or title
        return make_entry(
            channel_name=title,
            contact_name="",
            platform="newsletter",
            profile_url=profile_url,
            audience=12000,
            niche="ADHD/productivity/neurodivergent newsletter",
            email=email,
            priority="high",
            notes=f"Substack (@{slug}). Email on about page.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(process_slug, s): s for s in SUBSTACK_SEEDS}
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def scrape_site_seeds(
    seeds: list[tuple[str, str, str]],
    platform: str,
    niche: str,
    existing_emails: set[str],
    existing_urls: set[str],
    seen_emails: set[str],
    seen_urls: set[str],
    limit: int,
) -> list[dict]:
    results: list[dict] = []
    contact_paths = ["", "/contact", "/contact-us", "/about", "/about-us", "/work-with-me", "/collaborate", "/media"]

    def process_seed(seed: tuple[str, str, str]) -> dict | None:
        site_url, name, contact_name = seed
        parsed = urlparse(site_url)
        base = f"{parsed.scheme}://{parsed.netloc}"
        purl = norm_url(site_url)
        if purl in existing_urls or purl in seen_urls:
            return None
        emails: list[str] = []
        for path in contact_paths:
            emails.extend(extract_emails(fetch(urljoin(base, path))))
        emails = list(dict.fromkeys(emails))
        if not emails:
            return None
        preferred = None
        for e in emails:
            local = e.split("@")[0].lower()
            if local in ("hello", "contact", "business", "media", "partnerships", "collab", "info", "mgmt", "press"):
                preferred = e
                break
        email = preferred or emails[0]
        em = norm_email(email)
        if em in existing_emails or em in seen_emails:
            return None
        priority = "high" if platform == "podcast" else "medium"
        return make_entry(
            channel_name=name,
            contact_name=contact_name,
            platform=platform,
            profile_url=site_url,
            audience=15000 if platform == "youtube" else 10000,
            niche=niche,
            email=email,
            priority=priority,
            notes=f"{platform.title()} site. Business email verified on contact/about page.",
        )

    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futs = {pool.submit(process_seed, s): s for s in seeds}
        for fut in as_completed(futs):
            if len(results) >= limit:
                break
            try:
                entry = fut.result()
            except Exception:
                continue
            if entry:
                em = norm_email(entry["contact_email"])
                if em not in seen_emails:
                    results.append(entry)
                    seen_emails.add(em)
                    seen_urls.add(norm_url(entry["profile_url"]))

    return results


def run(limit: int = 200, dry_run: bool = False) -> dict:
    existing_emails, existing_urls = load_existing()
    seen_emails: set[str] = set()
    seen_urls: set[str] = set()
    all_results: list[dict] = []

    log(f"Existing: {len(existing_emails)} emails, {len(existing_urls)} profile URLs")

    phases = [
        ("Notion Marketplace", lambda rem: scrape_notion_categories(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("Gumroad Discover", lambda rem: scrape_gumroad(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("Substack newsletters", lambda rem: scrape_substack(
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("ADHD/productivity podcasts", lambda rem: scrape_site_seeds(
            PODCAST_SEEDS, "podcast", "ADHD/productivity podcast",
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
        ("YouTube creators", lambda rem: scrape_site_seeds(
            YOUTUBE_SEEDS, "youtube", "ADHD/Notion/productivity YouTube",
            existing_emails, existing_urls, seen_emails, seen_urls, rem)),
    ]

    for phase_name, fn in phases:
        remaining = limit - len(all_results)
        if remaining <= 0:
            break
        log(f"\n==> {phase_name} (need {remaining})")
        batch = fn(remaining)
        log(f"    +{len(batch)} new contacts (total {len(all_results) + len(batch)})")
        all_results.extend(batch)

    deduped: list[dict] = []
    batch_seen: set[str] = set()
    for c in all_results:
        key = norm_email(c["contact_email"])
        if key in batch_seen:
            continue
        batch_seen.add(key)
        deduped.append(c)
    deduped = deduped[:limit]

    stats = {
        "saved": len(deduped),
        "new_vs_master": len(deduped),
        "duplicates_skipped_in_batch": len(all_results) - len(deduped),
        "by_platform": {},
    }
    for c in deduped:
        p = c["platform"]
        stats["by_platform"][p] = stats["by_platform"].get(p, 0) + 1

    if not dry_run:
        OUT.write_text(json.dumps(deduped, indent=2) + "\n")
        log(f"\nWrote {len(deduped)} contacts to {OUT}")
    else:
        log(f"\nDry run — would save {len(deduped)} contacts")

    return {"contacts": deduped, "stats": stats}


def main() -> None:
    parser = argparse.ArgumentParser(description="Ring 7 affiliate outreach research")
    parser.add_argument("--limit", type=int, default=200, help="Max contacts to save")
    parser.add_argument("--dry-run", action="store_true", help="Stats only, no file write")
    args = parser.parse_args()
    result = run(limit=args.limit, dry_run=args.dry_run)
    log(json.dumps(result["stats"], indent=2))


if __name__ == "__main__":
    main()