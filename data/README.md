# Process C test data

Source: Voss Cycles case, Appendices D (Build Book), E3 (bank statement, 21-25 Sep 2026) and C5 (Castle invoice CPC-2609).

## Assumptions
- Build Book snapshot taken as at Thu 24 Sep 2026, 09:15. Payments after that time are not reflected.
- deposit_paid_gbp is inferred for most orders as price minus balance due, as no deposit column exists in the Build Book.
- For VC-2026-025, the balance is already paid, so the £1,000 deposit is inferred from the £2,220 balance payment on 22 Sep (£3,220 price minus £2,220).
- Blank balance_due_gbp means the Build Book does not state a balance.
- reminders_sent counts only the reminders recorded in the case.
- Supplier bank details are not given in the case and are left blank.
