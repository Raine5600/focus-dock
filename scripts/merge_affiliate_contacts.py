#!/usr/bin/env python3
import json
import re
from pathlib import Path

MARKETING = Path(__file__).parent.parent / "marketing"
BATCHES = [
    MARKETING / "creator-outreach-list.json",
    MARKETING / "_batch_adhd_coaches.json",
    MARKETING / "_batch_notion.json",
    MARKETING / "_batch_productivity.json",
    MARKETING / "_batch_misc.json",
]
OUT = MARKETING / "affiliate-contacts-master.json"


def norm_email(e):
    return (e or "").strip().lower()


def norm_url(u):
    u = (u or "").strip().lower().rstrip("/")
    u = re.sub(r"^mailto:", "", u)
    return u


def dedupe_key(c):
    email = norm_email(c.get("contact_email"))
    url = norm_url(c.get("contact_url"))
    if email:
        return f"email:{email}"
    if url:
        return f"url:{url}"
    return f"name:{(c.get('channel_name') or '').lower()}"


def normalize(c):
    ct = (c.get("contact_type") or "").strip()
    email = (c.get("contact_email") or "").strip()
    url = (c.get("contact_url") or "").strip()

    if ct not in ("email", "contact_form"):
        return None
    if ct == "email" and not email:
        return None
    if ct == "contact_form" and not url:
        return None
    if ct == "email" and not url:
        url = f"mailto:{email}"

    out = {
        "channel_name": c.get("channel_name", "").strip(),
        "contact_name": c.get("contact_name", "").strip(),
        "platform": c.get("platform", c.get("youtube_url") and "youtube" or "").strip() or "other",
        "profile_url": c.get("profile_url", c.get("youtube_url", "")).strip(),
        "subscribers_or_audience": c.get("subscribers_or_audience", c.get("subscribers", "")),
        "niche_focus": c.get("niche_focus", "").strip(),
        "contact_email": email,
        "contact_type": ct,
        "contact_url": url,
        "sells_digital_products": c.get("sells_digital_products", ""),
        "outreach_priority": c.get("outreach_priority", "medium"),
        "notes": c.get("notes", "").strip(),
    }
    if not out["channel_name"]:
        return None
    return out


def main():
    seen = {}
    order = []
    for path in BATCHES:
        if not path.exists():
            print(f"skip missing: {path}")
            continue
        with open(path) as f:
            data = json.load(f)
        if not isinstance(data, list):
            continue
        for raw in data:
            c = normalize(raw)
            if not c:
                continue
            k = dedupe_key(c)
            if k in seen:
                continue
            seen[k] = c
            order.append(c)

    order.sort(key=lambda x: (x["contact_type"], x["outreach_priority"], x["channel_name"].lower()))
    with open(OUT, "w") as f:
        json.dump(order, f, indent=2)

    by_type = {}
    for c in order:
        by_type[c["contact_type"]] = by_type.get(c["contact_type"], 0) + 1
    print(f"Total unique contacts: {len(order)}")
    for t, n in sorted(by_type.items()):
        print(f"  {t}: {n}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()