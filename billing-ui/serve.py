"""Launch the casework UI from ANY working directory.

All paths resolve from this file's own location, so the command works
identically from workshop root, atlas, billing-ui, or anywhere else:

    python <path-to>/billing-ui/serve.py            fresh dated walk db
    python <path-to>/billing-ui/serve.py --seeded   gate-review db
    python <path-to>/billing-ui/serve.py --db x.db  explicit db

Default db is data/demo-walk-<today>.db under billing-ui (the dated
fresh database the demo-walk protocol requires -- the date is filled
in for you; rehearsal 1's pasted-placeholder failure cannot recur).
--seeded opens data/demo-billing.db (run verify/seed_demo.py first).
"""

import argparse
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
CASEWORK_UI = HERE.parent / "casework-ui"
sys.path.insert(0, str(CASEWORK_UI))


def main():
    ap = argparse.ArgumentParser(
        description="casework UI launcher (any-cwd)")
    ap.add_argument("--db", default=None,
                    help="db path (default: data/demo-walk-<today>.db)")
    ap.add_argument("--seeded", action="store_true",
                    help="open the seeded gate-review db instead")
    ap.add_argument("--port", type=int, default=8500)
    ap.add_argument("--client-port", type=int, default=8501)
    ap.add_argument("--no-prefill", action="store_true",
                    help="disable the demo login prefill")
    args = ap.parse_args()

    if args.seeded and args.db:
        ap.error("--seeded and --db are mutually exclusive")
    if args.seeded:
        db = HERE / "data" / "demo-billing.db"
        if not db.exists():
            print("seeded db missing -- run: python"
                  f" {HERE / 'verify' / 'seed_demo.py'}")
            return 2
    elif args.db:
        db = Path(args.db)
    else:
        db = HERE / "data" / f"demo-walk-{date.today().isoformat()}.db"

    fresh = "existing" if db.exists() else "fresh"
    from app_ui import server as ui_server
    httpd = ui_server.make_server(db, args.port, args.client_port)
    if not args.no_prefill:
        # gated item 5 (ruled IN 2026-08-10): this launcher serves
        # synthetic demo dbs exclusively, so the login screen may
        # prefill the seeded credentials. The conventions are pinned:
        # the walk sheet's setup step dictates demo-walk-pass; the
        # gate-review seed (verify/seed_demo.py) uses demo-seed-pass.
        httpd.demo_prefill = (
            ("demo.reviewer@synthetic.test", "demo-seed-pass")
            if args.seeded else
            ("demo.driver@synthetic.test", "demo-walk-pass"))
    host, port = httpd.server_address[:2]
    ui_server.serve_client(httpd)
    print(f"casework-ui on http://{host}:{port}")
    print(f"  db: {db} ({fresh}; first visit -> /setup on a fresh db)")
    print(f"  client surface: {httpd.client_base}")
    print("  stop with Ctrl+C")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
