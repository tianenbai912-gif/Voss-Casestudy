import csv
from decimal import Decimal


def to_decimal(value):
    """Convert a CSV money field to Decimal, or None if it is blank."""
    if value is None or value.strip() == "":
        return None
    return Decimal(value)


def load_build_book(path="data/build_book.csv"):
    """Read the Build Book and return one dictionary per order."""
    orders = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            orders.append({
                "order_ref": row["order_ref"],
                "customer": row["customer"],
                "price": to_decimal(row["price_gbp"]),
                "deposit_paid": to_decimal(row["deposit_paid_gbp"]),
                "balance_due": to_decimal(row["balance_due_gbp"]),
                "reminders_sent": int(row["reminders_sent"]),
            })
    return orders


def candidates_by_amount(orders, amount):
    """Return orders whose balance due exactly equals the payment amount."""
    return [o for o in orders if o["balance_due"] == amount]


if __name__ == "__main__":
    orders = load_build_book()
    print(f"Orders loaded: {len(orders)}")
    for order in orders:
        print(f"{order['order_ref']}  {order['customer']:<16}  balance: {order['balance_due']}")

    payment = Decimal("2850.00")
    matches = candidates_by_amount(orders, payment)
    print(f"\nCandidates for GBP {payment}: {len(matches)}")
    for order in matches:
        print(f"  {order['order_ref']}  {order['customer']}")
