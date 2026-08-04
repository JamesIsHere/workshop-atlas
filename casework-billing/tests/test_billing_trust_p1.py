"""P1 parity tests (authored before the engine, oracle-first): trust
bank accounts, trust ledger, trust disbursements. Criteria quoted from
../docketwise-spec/corpus/invoicing-and-trust-accounting.md; cite ids
in assertions so a red names its criterion.

Convention: casework spine style -- each test takes a fresh seeded
conn. Seeded contacts: 1=Dana, 2=Emil; matters: 1=Dana I-130.
"""
from app import ledger

D = "2026-08-02"


def _iolta(conn):
    return ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA", 1)


def test_invoicing_and_trust_accounting_trust_bank_accounts(conn):
    # criterion: create account of type Trust -> available for trust
    # transactions, shows its own balance and transaction list
    iolta = _iolta(conn)
    second = ledger.create_bank_account(conn, "trust_bank", "SYNTH IOLTA 2", 1)
    assert iolta != second, "unlimited trust accounts (fx-0069)"
    banks = ledger.list_bank_accounts(conn)
    kinds = {b["id"]: b["kind"] for b in banks}
    assert kinds[iolta] == "trust_bank" and kinds[second] == "trust_bank"

    ledger.record_trust_deposit(conn, iolta, contact_id=1,
                                amount_cents=500000, date=D, posted_by=1)
    banks = {b["id"]: b for b in ledger.list_bank_accounts(conn)}
    assert banks[iolta]["balance_cents"] == 500000, "account balance shown"
    assert banks[second]["balance_cents"] == 0, "balances are per-account"

    txns = ledger.account_transactions(conn, iolta)
    assert len(txns) == 1, "transaction list shown (fx-0069)"
    t = txns[0]
    # per-account rows show date, client, matter, type, amount (fx-0069)
    assert t["date"] == D and t["contact_id"] == 1
    assert t["type"] == "trust_deposit" and t["amount_cents"] == 500000


def test_invoicing_and_trust_accounting_trust_ledger(conn):
    # criterion: ledger overview in three tabs (firm/matter/client);
    # clicking a row -> detailed transactions with date, type,
    # description, amount (fx-0053)
    iolta = _iolta(conn)
    ledger.record_trust_deposit(conn, iolta, contact_id=1,
                                amount_cents=500000, date=D, posted_by=1,
                                memo="Retainer")
    ledger.record_trust_deposit(conn, iolta, contact_id=2, matter_id=2,
                                amount_cents=200000, date=D, posted_by=1,
                                memo="Filing funds")
    ledger.disburse(conn, iolta, contact_id=1, amount_cents=120000,
                    date=D, posted_by=1, counterparty="SYNTH-USCIS",
                    memo="Filing fee")

    view = ledger.trust_ledger_overview(conn)
    assert set(view) >= {"firm", "client", "matter"}, "three tabs"
    firm_ids = [r["account_id"] for r in view["firm"]]
    assert iolta in firm_ids
    # only clients/matters with trust activity AT THAT LEVEL are listed
    # (fx-0053): this test's deposits are Dana client-level and Emil
    # matter-level, so Emil must not appear on the client tab (his
    # client_trust exists only as tree parent). Seed-tolerant: assert
    # membership, not exact sets; contact 5 has no trust activity at all.
    client_contacts = {r["contact_id"] for r in view["client"]}
    assert 1 in client_contacts and 2 not in client_contacts, client_contacts
    assert 5 not in client_contacts, "no-activity client listed"
    matter_matters = {r["matter_id"] for r in view["matter"]}
    assert 2 in matter_matters and 1 not in matter_matters, matter_matters

    # drilldown on THIS test's account (seed activity lives on other
    # banks' sub-accounts; get-or-create returns ours under our iolta)
    acct = ledger.ensure_client_trust(conn, iolta, 1)
    assert acct in [r["account_id"] for r in view["client"]]
    txns = ledger.account_transactions(conn, acct)
    assert len(txns) == 2
    for t in txns:
        for field in ("date", "type", "description", "amount_cents"):
            assert field in t, "transactions carry %s (fx-0053)" % field
    # transactions-view filters: type, amount (fx-0053)
    only_disb = ledger.account_transactions(conn, acct, type="disbursement")
    assert [t["type"] for t in only_disb] == ["disbursement"]
    big = ledger.account_transactions(conn, acct, min_amount_cents=300000)
    assert [t["amount_cents"] for t in big] == [500000]


def test_invoicing_and_trust_accounting_trust_disbursements(conn):
    # criterion: Disburse Funds on a client or matter Trust Acct tab ->
    # available funds decrease by the amount, transaction listed (fx-0074)
    iolta = _iolta(conn)
    base = ledger.trust_account_tab(conn, contact_id=1)["available_cents"]
    ledger.record_trust_deposit(conn, iolta, contact_id=1,
                                amount_cents=500000, date=D, posted_by=1)
    tab = ledger.trust_account_tab(conn, contact_id=1)
    assert tab["available_cents"] == base + 500000

    ledger.disburse(conn, iolta, contact_id=1, amount_cents=120000,
                    date=D, posted_by=1, counterparty="SYNTH-USCIS",
                    memo="I-485 filing fee")
    tab = ledger.trust_account_tab(conn, contact_id=1)
    assert tab["available_cents"] == base + 380000, \
        "available decreased by the disbursed amount (fx-0074)"
    types = [t["type"] for t in tab["transactions"]]
    assert "disbursement" in types, "transaction is listed"

    # matter-level pot is distinct from client-level (fx-0061/fx-0069)
    mbase = ledger.trust_account_tab(conn, matter_id=1)["available_cents"]
    ledger.record_trust_deposit(conn, iolta, contact_id=1, matter_id=1,
                                amount_cents=100000, date=D, posted_by=1)
    mtab = ledger.trust_account_tab(conn, matter_id=1)
    assert mtab["available_cents"] == mbase + 100000
    ctab = ledger.trust_account_tab(conn, contact_id=1)
    assert ctab["available_cents"] == base + 380000, "client pot unchanged"
