"""Layout and rendering helpers. Server-rendered, zero JS in P0.

One inline style block; no static assets, no framework (goal.md
Forbidden). ASCII only.
"""

import html as _html

esc = _html.escape

STYLE = """
:root { color-scheme: light; }
* { box-sizing: border-box; }
body { font-family: 'Segoe UI', system-ui, sans-serif; margin: 0;
       background: #f4f5f7; color: #1a1d21; }
header { background: #1f2a3d; color: #e8ebf0; padding: 0.6rem 1.2rem;
         display: flex; align-items: baseline; gap: 1.5rem; }
header .brand { font-weight: 600; letter-spacing: 0.02em; }
nav a { color: #b9c4d4; text-decoration: none; margin-right: 1rem; }
nav a:hover { color: #ffffff; }
header .who { margin-left: auto; font-size: 0.85rem; color: #b9c4d4; }
header form { display: inline; }
header button { background: none; border: 1px solid #55627a;
                color: #b9c4d4; border-radius: 4px; padding: 0.15rem 0.6rem;
                cursor: pointer; }
main { max-width: 60rem; margin: 2rem auto; padding: 0 1.2rem; }
.card { background: #ffffff; border: 1px solid #d9dde3; border-radius: 6px;
        padding: 1.5rem 1.8rem; margin-bottom: 1.2rem; }
.card.narrow { max-width: 26rem; margin: 3rem auto; }
h1 { font-size: 1.25rem; margin: 0 0 1rem; }
label { display: block; margin: 0.8rem 0 0.25rem; font-size: 0.9rem;
        color: #4a5261; }
input { width: 100%; padding: 0.45rem 0.6rem; border: 1px solid #c3c9d2;
        border-radius: 4px; font-size: 1rem; }
button.primary { margin-top: 1.2rem; background: #2456a6; color: #fff;
                 border: none; border-radius: 4px; padding: 0.55rem 1.4rem;
                 font-size: 1rem; cursor: pointer; }
button.primary:hover { background: #1c468a; }
.error { background: #fdecec; border: 1px solid #e5b3b3; color: #8a2525;
         border-radius: 4px; padding: 0.6rem 0.9rem; margin-bottom: 1rem; }
.hint { color: #6a7383; font-size: 0.85rem; }
table.data { width: 100%; border-collapse: collapse; margin: 0.8rem 0; }
table.data th { text-align: left; font-size: 0.8rem; color: #6a7383;
                text-transform: uppercase; letter-spacing: 0.05em;
                border-bottom: 2px solid #d9dde3; padding: 0.4rem 0.6rem; }
table.data td { border-bottom: 1px solid #e7eaee;
                padding: 0.5rem 0.6rem; }
.actions { margin: 0.8rem 0; }
.actions a { display: inline-block; background: #2456a6; color: #fff;
             border-radius: 4px; padding: 0.45rem 1rem;
             text-decoration: none; margin-right: 0.6rem; }
.actions a.quiet { background: #eef1f5; color: #2456a6; }
.pill { display: inline-block; border-radius: 10px; padding: 0.1rem
        0.6rem; font-size: 0.8rem; background: #eef1f5; color: #4a5261; }
.pill.returned { background: #e6f4e6; color: #256325; }
.kv dt { float: left; clear: left; width: 11rem; color: #6a7383;
         font-size: 0.9rem; padding: 0.25rem 0; }
.kv dd { margin-left: 12rem; padding: 0.25rem 0; }
code.copy { background: #f0f2f5; border: 1px dashed #b9c0cb;
            border-radius: 4px; padding: 0.4rem 0.6rem; display: block;
            margin: 0.4rem 0; word-break: break-all; }
select { padding: 0.45rem 0.5rem; border: 1px solid #c3c9d2;
         border-radius: 4px; font-size: 1rem; }
.mailbox { background: #fbf7e9; border: 1px solid #e3d9b8;
           border-radius: 4px; padding: 0.8rem 1rem; margin: 0 0 1.2rem; }
.mailbox h2 { font-size: 0.95rem; margin: 0 0 0.4rem; color: #6e6338; }
.code-display { font-size: 2.2rem; font-weight: 600;
                letter-spacing: 0.35em; text-align: center;
                margin: 0.4rem 0 0.6rem; color: #1f2a3d; }
"""

NAV_ITEMS = [("Clients", "/contacts"), ("Matters", "/matters"),
             ("Billing", "/billing"),  # approved 2026-08-04 (gate 0)
             ("Calendar", "/calendar"), ("Files", "/files"),
             ("Tasks", "/tasks"), ("Notes", "/notes"),
             ("Search", "/search"), ("Settings", "/settings")]


def page(title, body, user_name=None):
    """Full document. Nav renders only for an authenticated user."""
    nav = ""
    who = ""
    if user_name is not None:
        links = "".join(f"<a href='{href}'>{esc(label)}</a>"
                        for label, href in NAV_ITEMS)
        nav = f"<nav>{links}</nav>"
        who = (f"<span class='who'>{esc(user_name)}"
               f" <form method='post' action='/logout'>"
               f"<button>Log out</button></form></span>")
    return (f"<!DOCTYPE html><html><head><meta charset='utf-8'>"
            f"<meta name='viewport' content='width=device-width,"
            f" initial-scale=1'><title>{esc(title)} -- casework</title>"
            f"<style>{STYLE}</style></head><body>"
            f"<header><span class='brand'>casework</span>{nav}{who}</header>"
            f"<main>{body}</main></body></html>").encode("utf-8")


def field(label, name, ftype="text", value="", autofocus=False,
          required=True, hint=None):
    af = " autofocus" if autofocus else ""
    req = " required" if required else ""
    h = f"<p class='hint'>{esc(hint)}</p>" if hint else ""
    return (f"<label>{esc(label)}</label>{h}"
            f"<input type='{ftype}' name='{name}' value='{esc(value)}'"
            f"{af}{req}>")


def table(headers, rows):
    """Plain data table; rows are lists of pre-escaped HTML cells."""
    head = "".join(f"<th>{esc(h)}</th>" for h in headers)
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) +
                   "</tr>" for r in rows)
    return (f"<table class='data'><thead><tr>{head}</tr></thead>"
            f"<tbody>{body}</tbody></table>")


def link(href, text):
    return f"<a href='{href}'>{esc(text)}</a>"


def error_box(message):
    return f"<div class='error'>{esc(message)}</div>" if message else ""


def empty_state(text):
    """Designed empty state; the browse sweep asserts this class on
    every empty surface (screen review 2, finding 1)."""
    return f"<p class='hint empty'>{esc(text)}</p>"
