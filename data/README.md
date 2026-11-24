# Process C test data

Source: Voss Cycles case, Appendices D (Build Book), E3 (bank statement, 21-25 Sep 2026) and C5 (Castle invoice CPC-2609).

## Assumptions
- Build Book snapshot taken as at Thu 24 Sep 2026, 09:15. Payments after that time are not reflected.
- deposit_paid_gbp is inferred as price minus balance due, as no deposit column exists in the Build Book.
- Blank balance_due_gbp means the Build Book does not state a balance.
- reminders_sent counts only the reminders recorded in the case.
- Supplier bank details are not given in the case and are left blank.