"""Generate fake restaurant order emails for ~8 weeks.

Some restaurants "go quiet" on their latest expected order so the
detector has something to catch.
"""
import json
import random
from datetime import date, datetime, timedelta, time
from pathlib import Path

random.seed(7)

TODAY = date.today()
WEEKS = 8

# name, email, order weekdays (0=Mon), usual items, skips_latest
RESTAURANTS = [
    ("Joe's Oyster Bar", "joe@joesoyster.com", [1, 4], ["oysters", "king salmon"], False),
    ("Bluefin Sushi", "orders@bluefinsushi.com", [0, 3], ["bluefin tuna", "yellowtail", "salmon"], True),
    ("Harbor Grill", "chef@harborgrill.com", [2], ["halibut", "shrimp"], False),
    ("The Crab Shack", "info@crabshack.com", [1, 5], ["dungeness crab", "clams"], False),
    ("Mariner's Table", "kitchen@marinerstable.com", [0], ["cod", "scallops"], True),
    ("Poke Palace", "hello@pokepalace.com", [0, 2, 4], ["ahi tuna", "salmon"], False),
    ("Lighthouse Bistro", "lh@lighthousebistro.com", [3], ["sea bass", "mussels"], False),
    ("Saltwater Kitchen", "orders@saltwaterkitchen.com", [1], ["lobster", "shrimp"], True),
    ("Dockside Diner", "dock@docksidediner.com", [4], ["cod", "clams"], False),
    ("Coral Cafe", "coral@coralcafe.com", [2, 5], ["mahi mahi", "shrimp"], False),
]

UNITS = ["lb", "cs", "dz"]

TEMPLATES = [
    "Hi team,\n\nPlease send the following for {when}:\n{lines}\n\nThanks,\n{name}",
    "hey can we get\n{lines}\nfor {when}. thx",
    "Order for {name}:\n{lines}\nDeliver {when} morning please.",
    "Morning! Usual plus a bit extra this week:\n{lines}\n- {name}",
]


def order_lines(items):
    lines = []
    for item in items:
        if random.random() < 0.85:  # occasionally skip an item
            qty = random.randint(2, 20)
            unit = random.choice(UNITS)
            lines.append(f"{qty} {unit} {item}")
    return lines or [f"5 lb {items[0]}"]


def main():
    emails = []
    start = TODAY - timedelta(weeks=WEEKS)
    for name, addr, weekdays, items, skips_latest in RESTAURANTS:
        # orders are emailed the day before delivery
        order_days = [
            start + timedelta(days=d)
            for d in range(WEEKS * 7)
            if (start + timedelta(days=d)).weekday() in weekdays
            and start + timedelta(days=d) < TODAY
        ]
        if skips_latest:
            # drop the last two expected orders -> restaurant went quiet
            order_days = order_days[:-2] if len(weekdays) > 1 else order_days[:-1]
        for d in order_days:
            if random.random() < 0.05:  # random noise: a missed week
                continue
            sent = datetime.combine(d, time(random.randint(6, 20), random.randint(0, 59)))
            body = random.choice(TEMPLATES).format(
                when="tomorrow", lines="\n".join(order_lines(items)), name=name
            )
            emails.append({
                "id": f"msg_{len(emails):04d}",
                "from": addr,
                "received_at": sent.isoformat(),
                "body": body,
            })

    emails.sort(key=lambda e: e["received_at"])
    out = Path(__file__).parent / "data" / "emails.json"
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(emails, indent=2))
    print(f"Wrote {len(emails)} emails to {out}")


if __name__ == "__main__":
    main()
