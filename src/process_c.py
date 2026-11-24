from decimal import Decimal

from match_names import load_build_book
from reconcile import normalise_reference

DEPOSIT = Decimal("1000.00")  # Appendix A: deposit secures a build slot


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


if __name__ == "__main__":
    orders = load_build_book()
    outcome, detail = match_payment("VC-2026-034 DEPOSIT", Decimal("1000.00"), orders)
    print(f"Payment 'VC-2026-034 DEPOSIT' GBP 1000.00")
    print(f"Outcome: {outcome}")
    print(f"Detail: {detail}")
