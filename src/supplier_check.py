import csv

from rapidfuzz import fuzz


def load_supplier_domains(path="data/supplier_master.csv"):
    """Return a dict of supplier name to its known accounts email domain."""
    with open(path, newline="") as f:
        return {row["supplier"]: row["accounts_email_domain"] for row in csv.DictReader(f)}


def check_sender(sender_address, supplier, domains):
    """Pass only if the sender's domain exactly matches the domain on file.
    Any other domain is blocked, and RapidFuzz shows how similar it is."""
    known = domains.get(supplier)
    if known is None or known == "NOT IN CASE":
        return ("unknown_supplier", None)

    sender_domain = sender_address.split("@")[-1].strip().lower()
    if sender_domain == known:
        return ("sender_verified", 100.0)

    similarity = fuzz.ratio(sender_domain, known)
    return ("block_possible_spoof", round(similarity, 1))


if __name__ == "__main__":
    domains = load_supplier_domains()
    sender = "accounts@velocomponents-direct.co"
    outcome, score = check_sender(sender, "Velo Components Direct", domains)
    print("B4 sender check: Velo Components Direct invoice email (Appendix E2)")
    print(f"  Sender: {sender}")
    print(f"  Outcome: {outcome}")
    print(f"  Similarity to domain on file: {score}")
