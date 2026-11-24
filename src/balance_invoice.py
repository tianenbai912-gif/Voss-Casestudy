from decimal import Decimal

from match_names import load_build_book

# Overseas orders are identified by hand from the case, because the Build Book
# has no country field. VC-2026-028: Aoife Byrne, Dublin, Ireland (Appendix D).
OVERSEAS_ORDERS = {"VC-2026-028"}


def review_balance_invoice(order_ref, orders):
    """Decide whether a balance invoice can be issued automatically."""
    order = next((o for o in orders if o["order_ref"] == order_ref), None)
    if order is None:
        return ("unknown_order", order_ref)

    expected_balance = order["price"] - order["deposit_paid"]
    if order["balance_due"] != expected_balance:
        return ("balance_mismatch", order_ref)

    if order_ref in OVERSEAS_ORDERS:
        return ("hold_vat_and_delivery_review", order_ref)

    return ("issue_invoice_uk_vat", order_ref)


if __name__ == "__main__":
    orders = load_build_book()
    outcome, detail = review_balance_invoice("VC-2026-028", orders)
    print("C4 Balance invoice VC-2026-028 (Aoife Byrne, Dublin)")
    print(f"  Outcome: {outcome}")
    print(f"  Detail: {detail}")
