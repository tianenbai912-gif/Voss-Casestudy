import csv
from decimal import Decimal

VAT_RATE = Decimal("0.20")         # UK standard rate, stated in the case
INVOICE_TOTAL = Decimal("720.00")  # Castle invoice CPC-2609 total, including VAT
PENNY = Decimal("0.01")


def load_invoice_lines(path="data/supplier_invoices.csv"):
    """Read invoice lines, converting net amounts to Decimal and disputed to bool."""
    with open(path, newline="") as f:
        return [
            {
                "invoice_no": row["invoice_no"],
                "line_no": int(row["line_no"]),
                "description": row["description"],
                "order_ref": row["order_ref"],
                "net": Decimal(row["net_gbp"]),
                "disputed": row["disputed"].strip().lower() == "yes",
            }
            for row in csv.DictReader(f)
        ]


def split_invoice(lines):
    """Split an invoice into payable and held amounts, each with VAT added."""
    payable = [l for l in lines if not l["disputed"]]
    held = [l for l in lines if l["disputed"]]

    payable_net = sum((l["net"] for l in payable), Decimal("0.00"))
    held_net = sum((l["net"] for l in held), Decimal("0.00"))

    payable_gross = (payable_net * (1 + VAT_RATE)).quantize(PENNY)
    held_gross = (held_net * (1 + VAT_RATE)).quantize(PENNY)

    if payable_gross + held_gross != INVOICE_TOTAL:
        raise ValueError(f"Split does not reconcile to {INVOICE_TOTAL}")

    return {
        "outcome": "pay_undisputed_hold_disputed" if held else "pay_full",
        "payable_net": payable_net,
        "payable_gross": payable_gross,
        "held_net": held_net,
        "held_gross": held_gross,
        "held_lines": [l["line_no"] for l in held],
    }


if __name__ == "__main__":
    lines = load_invoice_lines()
    result = split_invoice(lines)
    print("C5 Castle Powder Coating invoice CPC-2609")
    print(f"  Outcome: {result['outcome']}")
    print(f"  Payable net GBP {result['payable_net']}, gross GBP {result['payable_gross']}")
    print(f"  Held net GBP {result['held_net']}, gross GBP {result['held_gross']}")
    print(f"  Held line numbers: {result['held_lines']}")
