"""Turn raw order emails into structured orders using pattern matching."""
import json
import re
from pathlib import Path

DATA = Path(__file__).parent / "data"
LINE_RE = re.compile(r"^\s*-?\s*(\d+)\s*(lb|lbs|cs|case|cases|dz|dozen)\s+(.+?)\s*$", re.I)


def extract(body):
    items = []
    for line in body.splitlines():
        m = LINE_RE.match(line)
        if m:
            items.append({"qty": int(m[1]), "unit": m[2].lower()[:2], "product": m[3].lower()})
    return {"items": items}


def main():
    emails = json.loads((DATA / "emails.json").read_text())
    orders = [
        {
            "email_id": e["id"],
            "customer": e["from"],
            "ordered_at": e["received_at"],
            **extract(e["body"]),
        }
        for e in emails
    ]
    (DATA / "orders.json").write_text(json.dumps(orders, indent=2))
    print(f"Extracted {len(orders)} orders -> data/orders.json")


if __name__ == "__main__":
    main()
