#!/usr/bin/env python3
"""Build future outreach queue from master list minus already-sent."""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "marketing"))
from outreach_utils import subscriber_count

MARKETING = Path(__file__).parent.parent / "marketing"
MASTER = MARKETING / "affiliate-contacts-master.json"
SENT_LOG = MARKETING / "email-send-log.json"
OUT = MARKETING / "future-outreach-queue.json"

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}


def load_sent_emails() -> set[str]:
    if not SENT_LOG.exists():
        return set()
    with open(SENT_LOG) as f:
        log = json.load(f)
    return {e["email"].lower() for e in log.get("sent", []) if e.get("email")}


def main():
    with open(MASTER) as f:
        master = json.load(f)

    sent = load_sent_emails()
    queue = []
    for c in master:
        email = (c.get("contact_email") or "").strip().lower()
        if c.get("contact_type") != "email" or not email:
            continue
        if email in sent:
            continue
        queue.append(c)

    queue.sort(
        key=lambda x: (
            PRIORITY_ORDER.get(x.get("outreach_priority"), 9),
            0 if x.get("in_target_range") else 1,
            -(subscriber_count(x) or 0),
        )
    )

    with open(OUT, "w") as f:
        json.dump(queue, f, indent=2)

    in_range = sum(1 for c in queue if c.get("in_target_range") is True)
    print(f"Future queue: {len(queue)} emails ({in_range} in 5k-100k target range)")
    print(f"Already sent (skipped): {len(sent)}")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()