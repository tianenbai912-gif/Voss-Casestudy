import csv
import re

# VC, an optional hyphen, four digits (year), an optional hyphen, three digits
ORDER_PATTERN = re.compile(r"VC-?(\d{4})-?(\d{3})", re.IGNORECASE)


def normalise_reference(reference):
    """Return the standard order number found in a bank reference, or None."""
    if not reference:
        return None
    match = ORDER_PATTERN.search(reference)
    if match is None:
        return None
    year, number = match.groups()
    return f"VC-{year}-{number}"


if __name__ == "__main__":
    with open("data/bank_lines.csv", newline="") as f:
        for row in csv.DictReader(f):
            ref = row["reference"]
            print(f"{ref!r:30} -> {normalise_reference(ref)}")