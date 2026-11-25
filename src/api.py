from decimal import Decimal

from flask import Flask, request, jsonify

from match_names import load_build_book
from process_c import match_payment, find_batch_duplicates

app = Flask(__name__)


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


if __name__ == "__main__":
    app.run(port=8000)