"""Translation architecture (U2.5, multilingual-intake adapted):
per-question strings in language packs; language fixed at
invitation time; client re-translation is a re-render with another
pack. One demonstration pack ships (es). Custom questions are not
translated (fx-0029): packs key on q.* question keys only, so cq.*
prompts pass through untouched. Machine-translation services are
post-v1 and approval-gated."""

import json
from pathlib import Path

PACKS_DIR = Path(__file__).resolve().parent.parent / "forms" / "translations"


def languages():
    """'en' plus every shipped pack."""
    return ["en"] + sorted(p.stem for p in PACKS_DIR.glob("*.json"))


def pack(lang):
    if lang == "en":
        return {}
    path = PACKS_DIR / f"{lang}.json"
    if not path.exists():
        raise ValueError(f"no language pack for {lang}")
    return json.loads(path.read_text(encoding="utf-8"))


def translate_items(items, lang):
    """Return intake items with labels swapped to the pack's strings
    where a translation exists; everything else stays English."""
    if lang == "en":
        return items
    strings = pack(lang)
    out = []
    for item in items:
        if item["key"] in strings:
            item = dict(item, label=strings[item["key"]])
        out.append(item)
    return out
