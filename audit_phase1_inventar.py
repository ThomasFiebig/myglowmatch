#!/usr/bin/env python3
"""
Phase-1-Inventar für Routing-Regel-vs-PDF-Audit
================================================
Liest die 4 relevanten Routing-Tabs aus dem Google-Sheet und
erzeugt:
  - pro Tab eine CSV-Baseline in backups/phase1_inventar_<TS>/
  - eine Markdown-Inventar-Datei audit_phase1_inventar.md mit
    „Trigger → Effekt"-Zeilen je Regel.

Behandelte Tabs (siehe HANDOVER):
  - map_derived_variables   (16 JSON-Flag-Regeln)
  - map_slot_rules          (REQ-Regeln, aktiv=TRUE)
  - map_conflict_rules      (CON-Regeln, aktiv=TRUE)
  - map_pflegelevel_overrides (PFL-OV-Floor/Cap-Regeln)

map_pflegelevel_scoring ist Pflegelevel-Punktevergabe (kein
Produkt-Routing) und damit explizit ausgespart.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path
from textwrap import shorten

REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))

from sheets_writer import DOC_ID, load_env, open_sheet, resolve_sa_path

TABS = [
    "map_derived_variables",
    "map_slot_rules",
    "map_conflict_rules",
    "map_pflegelevel_overrides",
]

OUT_MD = REPO / "audit_phase1_inventar.md"


def dump_tab_csv(ws, out_dir: Path) -> list[dict]:
    values = ws.get_all_values()
    if not values:
        return []
    headers = values[0]
    rows = [dict(zip(headers, row + [""] * (len(headers) - len(row)))) for row in values[1:]]
    out_path = out_dir / f"{ws.title}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    print(f"  → {out_path.relative_to(REPO)} ({len(rows)} Zeilen)")
    return rows


def md_table(headers: list[str], rows: list[list[str]]) -> str:
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        cells = [str(c).replace("|", "\\|").replace("\n", " ") for c in row]
        out.append("| " + " | ".join(cells) + " |")
    return "\n".join(out)


def section_derived(rows: list[dict]) -> str:
    out = ["## map_derived_variables — Flag-Regeln (Phase 1: normalized → flags)",
           "",
           "Pro Zeile: aus welchen `normalized.*`/`flags.*`-Inputs entsteht das Flag, "
           "wer konsumiert es. Die `regel_json`-Spalte ist die autoritative "
           "Trigger-Bedingung (vollständig, JSON-kompakt).",
           ""]
    table_rows = []
    for r in rows:
        variable = r.get("variable") or r.get("flag") or "?"
        typ = r.get("typ", "")
        regel = r.get("regel_json", "")
        try:
            regel_compact = json.dumps(json.loads(regel), separators=(",", ":"), ensure_ascii=False)
        except Exception:
            regel_compact = regel
        konsumenten = r.get("konsumenten", "")
        doku = r.get("doku", "")
        table_rows.append([variable, typ, regel_compact, konsumenten, doku])
    out.append(md_table(["variable", "typ", "regel_json (vollständig)", "konsumenten", "doku"], table_rows))
    out.append("")
    return "\n".join(out)


def section_slot_rules(rows: list[dict]) -> str:
    out = ["## map_slot_rules — REQ-Regeln (Routing in Slots)",
           "",
           "Nur aktive Regeln. Spalten zur Trigger-Bedingung und zur Folge "
           "(welches Produkt in welchen Slot). `requires_not`/`overrides` "
           "modellieren Regel-zu-Regel-Beziehungen, `filter` schränkt den "
           "Produkt-Pool ein.",
           ""]
    active = [r for r in rows if (r.get("aktiv", "TRUE").upper() == "TRUE")]
    headers = ["regel_id", "prioritaet", "trigger", "slot_typ", "filter", "requires_not", "overrides", "reason"]
    table_rows = []
    for r in active:
        regel_id = r.get("regel_id", "?")
        prio = r.get("prioritaet", "")
        slot = r.get("slot_typ", "")
        filt = r.get("filter", "")
        reqn = r.get("requires_not", "")
        overr = r.get("overrides", "")
        reason = r.get("reason", "") or r.get("beschreibung", "")
        trigger_parts = []
        for key, val_key in [
            ("trigger_flag", "trigger_wert"),
            ("trigger_flag2", "trigger_wert2"),
            ("trigger_flag3", "trigger_wert3"),
        ]:
            f = r.get(key, "")
            v = r.get(val_key, "")
            if f:
                trigger_parts.append(f"{f}={v}" if v else f)
        trigger = " AND ".join(trigger_parts) if trigger_parts else "(immer)"
        table_rows.append([regel_id, prio, trigger, slot, filt, reqn, overr, reason])
    out.append(md_table(headers, table_rows))
    out.append("")
    out.append(f"_Inaktive Regeln ausgeblendet: {len(rows) - len(active)} von {len(rows)}._")
    out.append("")
    return "\n".join(out)


def section_conflict_rules(rows: list[dict]) -> str:
    out = ["## map_conflict_rules — CON-Regeln (Produkt-Exclude / Suppress)",
           "",
           "Nur aktive Regeln. CON-Regeln blocken oder verschieben Produkte, "
           "die durch REQ schon im Topf sind.",
           ""]
    active = [r for r in rows if (r.get("aktiv", "TRUE").upper() == "TRUE")]
    headers = ["konflikt_id", "trigger", "action", "match_typ", "match_wert", "beschreibung"]
    table_rows = []
    for r in active:
        konflikt_id = r.get("konflikt_id") or r.get("regel_id") or "?"
        trigger_parts = []
        for key, val_key in [
            ("trigger_flag", "trigger_wert"),
            ("trigger_flag2", "trigger_wert2"),
        ]:
            f = r.get(key, "")
            v = r.get(val_key, "")
            if f:
                trigger_parts.append(f"{f}={v}" if v else f)
        # Fallback: einzelne Spalte "trigger"
        if not trigger_parts and r.get("trigger"):
            trigger_parts.append(r["trigger"])
        trigger = " AND ".join(trigger_parts) if trigger_parts else "(immer)"
        action = r.get("action", "")
        match_typ = r.get("match_typ", "")
        match_wert = r.get("match_wert", "")
        desc = r.get("beschreibung", "") or r.get("reason", "")
        table_rows.append([konflikt_id, trigger, action, match_typ, match_wert, desc])
    out.append(md_table(headers, table_rows))
    out.append("")
    out.append(f"_Inaktive Regeln ausgeblendet: {len(rows) - len(active)} von {len(rows)}._")
    out.append("")
    return "\n".join(out)


def section_pflegelevel_overrides(rows: list[dict]) -> str:
    out = ["## map_pflegelevel_overrides — PFL-Floor/Cap-Regeln",
           "",
           "Hebt das Pflegelevel auf einen Mindestwert (`raise_to`) oder "
           "deckelt es (`cap_at`). Wirkt indirekt aufs Routing: das endgültige "
           "Pflegelevel beeinflusst `max_products` und Filter-Verhalten.",
           ""]
    active = [r for r in rows if (r.get("aktiv", "TRUE").upper() == "TRUE")]
    headers = ["regel_id", "prio", "bedingung1", "bedingung2", "aktion", "ziel_level", "beschreibung"]
    table_rows = []
    for r in active:
        regel_id = r.get("regel_id", "?")
        prio = r.get("prioritaet", "")
        b1_parts = [r.get("bedingung1_feld", ""), r.get("bedingung1_typ", ""), r.get("bedingung1_wert", "")]
        b1 = " ".join(p for p in b1_parts if p)
        b2_parts = [r.get("bedingung2_feld", ""), r.get("bedingung2_typ", ""), r.get("bedingung2_wert", "")]
        b2 = " ".join(p for p in b2_parts if p)
        aktion = r.get("aktion", "")
        ziel = r.get("ziel_level", "")
        desc = r.get("beschreibung", "")
        table_rows.append([regel_id, prio, b1, b2 or "—", aktion, ziel, desc])
    out.append(md_table(headers, table_rows))
    out.append("")
    out.append(f"_Inaktive Regeln ausgeblendet: {len(rows) - len(active)} von {len(rows)}._")
    out.append("")
    return "\n".join(out)


SECTION_FN = {
    "map_derived_variables": section_derived,
    "map_slot_rules": section_slot_rules,
    "map_conflict_rules": section_conflict_rules,
    "map_pflegelevel_overrides": section_pflegelevel_overrides,
}


def main() -> int:
    env = load_env(REPO / ".env")
    sa_path = resolve_sa_path(env, REPO)
    sheet = open_sheet(sa_path, DOC_ID)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = REPO / "backups" / f"phase1_inventar_{ts}"
    out_dir.mkdir(parents=True, exist_ok=True)
    print(f"CSV-Snapshots → {out_dir.relative_to(REPO)}/")

    tab_rows: dict[str, list[dict]] = {}
    for tab in TABS:
        print(f"– lese Tab '{tab}' …")
        ws = sheet.worksheet(tab)
        tab_rows[tab] = dump_tab_csv(ws, out_dir)

    md = [
        f"# Phase-1-Inventar Routing-Regeln (Stand {ts})",
        "",
        "Quelle: Live-Read der 4 Routing-Tabs aus dem Google-Sheet "
        f"`{DOC_ID}`. Pro Tab CSV-Baseline unter "
        f"`backups/phase1_inventar_{ts}/`.",
        "",
        "Verdacht-Spalte bleibt in Phase 1 leer — wird in Phase 2 manuell gefüllt.",
        "",
    ]
    for tab in TABS:
        md.append(SECTION_FN[tab](tab_rows[tab]))

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"\nInventar geschrieben: {OUT_MD.relative_to(REPO)}")
    print(f"Tabs gelesen: {len(TABS)}; Regeln gesamt: "
          f"{sum(len(v) for v in tab_rows.values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
