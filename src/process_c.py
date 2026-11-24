from decimal import Decimal

from match_names import load_build_book
from reconcile import normalise_reference

DEPOSIT = Decimal("1000.00")  # Appendix A: deposit secures a build slot
MAX_AUTOMATED_REMINDERS = 2   # Nadia's rule 3: after two reminders, phone the customer


def match_payment(payment_ref, amount, orders):
    """Match a bank payment to an order using its reference and amount."""
    order_ref = normalise_reference(payment_ref)
    if order_ref is None:
        return ("no_reference", None)

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

    outcome, detail = match_payment("VC-2026-034 DEPOSIT", Decimal("1000.00"), orders)
    print("C1 Payment 'VC-2026-034 DEPOSIT' GBP 1000.00")
    print(f"  Outcome: {outcome}")
    print(f"  Detail: {detail}")

    outcome, detail = chase_balance("VC-2026-027", orders)
    print("C6 Balance VC-2026-027 (Chris Adeyemi)")
    print(f"  Outcome: {outcome}")
    print(f"  Detail: {detail}")
