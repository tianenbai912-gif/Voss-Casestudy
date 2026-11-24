from collections import Counter
from decimal import Decimal

from match_names import load_build_book
from reconcile import normalise_reference

DEPOSIT = Decimal("1000.00")  # Appendix A: deposit secures a build slot
MAX_AUTOMATED_REMINDERS = 2   # Nadia's rule 3: after two reminders, phone the customer


def find_batch_duplicates(payments):
    """Return order refs that receive more than one payment in the same batch."""
    refs = [normalise_reference(p["reference"]) for p in payments]
    counts = Counter(r for r in refs if r is not None)
    return {ref for ref, n in counts.items() if n > 1}


def match_payment(payment_ref, amount, orders, duplicates=frozenset()):
    """Match a bank payment to an order using its reference, amount and batch."""
    order_ref = normalise_reference(payment_ref)
    if order_ref is None:
        return ("no_reference", None)

    if order_ref in duplicates:
        return ("potential_duplicate", order_ref)

    order = next((o for o in orders if o["order_ref"] == order_ref), None)
    if order is None:
        return ("unallocated", order_ref)

    if amount == DEPOSIT and order["deposit_paid"] == Decimal("0.00"):
        return ("deposit_matched", order_ref)

    return ("investigate", order_ref)


def chase_balance(order_ref, orders):
    """Decide the next action for an unpaid balance."""
    order = next((o for o in orders if o["order_ref"] == order_ref), None)
    if order is None:
        return ("unknown_order", order_ref)
    if order["balance_due"] in (None, Decimal("0.00")):
        return ("no_action", order_ref)
    if order["reminders_sent"] >= MAX_AUTOMATED_REMINDERS:
        return ("phone_customer", order_ref)
    return ("send_reminder_draft", order_ref)


if __name__ == "__main__":
    orders = load_build_book()

    # C1: J Okoro deposit (single payment in batch)
    payments_c1 = [{"reference": "VC-2026-034 DEPOSIT", "amount": Decimal("1000.00")}]
    dups_c1 = find_batch_duplicates(payments_c1)
    outcome, detail = match_payment("VC-2026-034 DEPOSIT", Decimal("1000.00"), orders, dups_c1)
    print("C1 Payment 'VC-2026-034 DEPOSIT' GBP 1000.00")
    print(f"  Outcome: {outcome}")
    print(f"  Detail: {detail}")

    # C2: H Doyle, two payments in the same batch (values from bank_lines.csv)
    payments_c2 = [
        {"reference": "VC2026035", "amount": Decimal("1000.00")},
        {"reference": "VC-2026-035 deposit", "amount": Decimal("1000.00")},
    ]
    dups_c2 = find_batch_duplicates(payments_c2)
    for p in payments_c2:
        outcome, detail = match_payment(p["reference"], p["amount"], orders, dups_c2)
        print(f"C2 Payment {p['reference']!r} GBP 1000.00")
        print(f"  Outcome: {outcome}")
        print(f"  Detail: {detail}")

    # C6: Chris Adeyemi, two reminders already sent
    outcome, detail = chase_balance("VC-2026-027", orders)
    print("C6 Balance VC-2026-027 (Chris Adeyemi)")
    print(f"  Outcome: {outcome}")
    print(f"  Detail: {detail}")
