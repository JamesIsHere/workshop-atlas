"""Synthetic bank-statement generator (P5 U5.1) -- the INDEPENDENT
WITNESS of goal.md's F7 independence clause: this module reads ONLY
external_events (plus the account roster for enumeration); it never
touches the journal. A statement derived from the journal would be
circular and void.

Clearing-lag model (goal.md decision default 5, red-pen r1): lags
exist DELIBERATELY so genuine reconciling items occur --
  deposit          clears T+2 days
  check_cut        clears T+3 days
  processor_batch  clears T+1 day
  chargeback       clears T+1 day
"""

from datetime import date as _date

CLEARING_LAG_DAYS = {"deposit": 2, "check_cut": 3,
                     "processor_batch": 1, "chargeback": 1}


def _plus_days(iso_day, days):
    return _date.fromordinal(
        _date.fromisoformat(iso_day).toordinal() + days).isoformat()


def clear_date(event_type, occurred_on):
    return _plus_days(occurred_on, CLEARING_LAG_DAYS[event_type])


def statement(conn, bank_account_id, period_end):
    """The bank's view of one account through period_end: every event
    whose CLEARED date falls inside the period becomes a line; events
    occurred but not yet cleared are the bank's pending file (returned
    for the recon engine's convenience -- still event-derived only).
    """
    lines, pending = [], []
    for r in conn.execute(
            "SELECT id, event_type, occurred_on, amount_cents, direction,"
            " counterparty, memo, invoice_id, payment_id FROM"
            " external_events WHERE bank_account_id=?"
            " ORDER BY occurred_on, id",
            (bank_account_id,)).fetchall():
        cleared = clear_date(r[1], r[2])
        row = {"event_id": r[0], "event_type": r[1], "occurred_on": r[2],
               "cleared_on": cleared, "amount_cents": r[3],
               "direction": r[4], "counterparty": r[5], "memo": r[6],
               "invoice_id": r[7], "payment_id": r[8]}
        if r[2] > period_end:
            continue  # not yet occurred as of the period
        if cleared <= period_end:
            lines.append(row)
        else:
            pending.append(row)
    balance = sum(l["amount_cents"] if l["direction"] == "in"
                  else -l["amount_cents"] for l in lines)
    return {"bank_account_id": bank_account_id, "period_end": period_end,
            "lines": lines, "pending": pending,
            "closing_balance_cents": balance}


def statement_csv(stmt):
    out = ["cleared_on,direction,amount_cents,event_type,counterparty,memo"]
    for l in stmt["lines"]:
        out.append("%s,%s,%d,%s,%s,%s"
                   % (l["cleared_on"], l["direction"], l["amount_cents"],
                      l["event_type"], l["counterparty"] or "",
                      (l["memo"] or "").replace(",", ";")))
    out.append("closing_balance_cents,%d" % stmt["closing_balance_cents"])
    return "\n".join(out) + "\n"
