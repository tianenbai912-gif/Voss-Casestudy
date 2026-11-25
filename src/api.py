from decimal import Decimal

from flask import Flask, request, jsonify

from match_names import load_build_book, candidates_by_amount
from score_names import decide
from process_c import match_payment, find_batch_duplicates, chase_balance
from balance_invoice import review_balance_invoice
from supplier_invoice import load_invoice_lines, split_invoice

app = Flask(__name__)


def jsonable(value):
    """Convert Decimal values to strings so Flask can return them as JSON."""
    if isinstance(value, Decimal):
        return str(value)
    if isinstance(value, dict):
        return {k: jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [jsonable(v) for v in value]
    return value


@app.post("/tools/match_payment")
def tool_match_payment():
    body = request.get_json()
    batch = body.get("batch") or [{"reference": body["reference"]}]
    dups = find_batch_duplicates(batch)
    outcome, detail = match_payment(
        body["reference"], Decimal(body["amount"]), load_build_book(), dups
    )
    return jsonify({"outcome": outcome, "detail": detail})


@app.post("/tools/match_batch")
def tool_match_batch():
    payments = request.get_json()["payments"]
    dups = find_batch_duplicates(payments)
    orders = load_build_book()
    results = []
    for p in payments:
        outcome, detail = match_payment(
            p["reference"], Decimal(p["amount"]), orders, dups
        )
        results.append({"reference": p["reference"], "outcome": outcome, "detail": detail})
    return jsonify({"results": results})


@app.post("/tools/name_candidates")
def tool_name_candidates():
    body = request.get_json()
    candidates = candidates_by_amount(load_build_book(), Decimal(body["amount"]))
    outcome, detail = decide(body["payee"], candidates)
    return jsonify({
        "outcome": outcome,
        "detail": detail,
        "candidates": [c["order_ref"] for c in candidates],
    })


@app.post("/tools/balance_invoice")
def tool_balance_invoice():
    body = request.get_json()
    outcome, detail = review_balance_invoice(body["order_ref"], load_build_book())
    return jsonify({"outcome": outcome, "detail": detail})


@app.post("/tools/split_invoice")
def tool_split_invoice():
    try:
        result = split_invoice(load_invoice_lines())
    except ValueError as e:
        return jsonify({"outcome": "stop", "detail": str(e)}), 422
    return jsonify(jsonable(result))


@app.post("/tools/chase_balance")
def tool_chase_balance():
    body = request.get_json()
    outcome, detail = chase_balance(body["order_ref"], load_build_book())
    return jsonify({"outcome": outcome, "detail": detail})


if __name__ == "__main__":
    app.run(port=8000)