from decimal import Decimal

from rapidfuzz import fuzz, utils

from match_names import candidates_by_amount, load_build_book

PAYEE = "MR T H"
PAYMENT = Decimal("2850.00")

SCORERS = {
    "ratio": fuzz.ratio,
    "partial_ratio": fuzz.partial_ratio,
    "token_sort_ratio": fuzz.token_sort_ratio,
    "token_set_ratio": fuzz.token_set_ratio,
}


def score_candidate(payee, customer):
    """Return the score from every scorer for one payee and customer name."""
    return {
        name: scorer(payee, customer, processor=utils.default_process)
        for name, scorer in SCORERS.items()
    }


def decide(payee, candidates):
    """Suggest a match only if one candidate beats all others on every scorer.
    Otherwise return human review. Ties count as not beating."""
    if len(candidates) == 0:
        return ("unallocated", None)

    scored = [(order, score_candidate(payee, order["customer"])) for order in candidates]

    for order, scores in scored:
        others = [other for other_order, other in scored if other_order is not order]
        if all(scores[name] > other[name] for other in others for name in SCORERS):
            return ("suggested_match", order["order_ref"])

    return ("human_review", [order["order_ref"] for order in candidates])


if __name__ == "__main__":
    orders = load_build_book()
    candidates = candidates_by_amount(orders, PAYMENT)
    outcome, detail = decide(PAYEE, candidates)

    print(f"Payee {PAYEE!r}, amount GBP {PAYMENT}: {len(candidates)} candidate(s)")
    for order in candidates:
        scores = score_candidate(PAYEE, order["customer"])
        score_text = "  ".join(f"{name}={value:.1f}" for name, value in scores.items())
        print(f"  {order['order_ref']}  {order['customer']:<14} {score_text}")
    print(f"Outcome: {outcome}")
    print(f"Detail: {detail}")
