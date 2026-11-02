"""Learn each customer's ordering rhythm and flag missed orders."""
import json
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

DATA = Path(__file__).parent / "data"
GRACE_DAYS = 1      # how late before we alert
MIN_SHARE = 0.5     # weekday must appear in >=50% of active weeks to count as "usual"


def load_orders():
    return json.loads((DATA / "orders.json").read_text())


def usual_weekdays(dates):
    weeks = {d.isocalendar()[:2] for d in dates}
    counts = Counter(d.weekday() for d in dates)
    return sorted(wd for wd, c in counts.items() if c / max(len(weeks), 1) >= MIN_SHARE)


def last_expected_day(weekdays, today):
    """Most recent day before today that falls on a usual weekday."""
    for back in range(1, 8):
        d = today - timedelta(days=back)
        if d.weekday() in weekdays:
            return d
    return None


def analyze(orders, today=None):
    today = today or date.today()
    by_customer = defaultdict(list)
    for o in orders:
        by_customer[o["customer"]].append(datetime.fromisoformat(o["ordered_at"]).date())

    results = []
    for customer, dates in by_customer.items():
        dates.sort()
        weekdays = usual_weekdays(dates)
        expected = last_expected_day(weekdays, today - timedelta(days=GRACE_DAYS - 1))
        last = dates[-1]
        overdue = expected is not None and last < expected
        results.append({
            "customer": customer,
            "usual_days": [date(2024, 1, 1 + wd).strftime("%a") for wd in weekdays],
            "last_order": last.isoformat(),
            "expected_by": expected.isoformat() if expected else None,
            "days_overdue": (today - expected).days if overdue else 0,
            "overdue": overdue,
            "total_orders": len(dates),
        })
    return sorted(results, key=lambda r: -r["days_overdue"])


if __name__ == "__main__":
    for r in analyze(load_orders()):
        flag = "OVERDUE" if r["overdue"] else "ok"
        print(f"{flag:8} {r['customer']:32} usual={','.join(r['usual_days']):12} last={r['last_order']}")
