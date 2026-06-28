#!/usr/bin/env python3
"""
Migration #21 — PDF-Audit-Korrekturen
======================================
Setzt 4 Befunde aus `audit_phase3_befunde.md` um:

  V1 (🔴): needs_repair_focus.regel_json — gefaerbt zusätzlich
           zu blondiert als Repair-Trigger.
  V2 (🟡): detangling_need.regel_json — kraus zusätzlich zu lockig
           im leicht_verfilzt-Zweig (PDF: „Alle Haarstrukturen").
  V5 (🔴): REQ-11c neu (heat_use=maybe + needs_curl_care → curl_creme
           styling_1) + REQ-04.requires_not um REQ-11c erweitert.
  V6 (🔴): REQ-19b neu (styling_goal_volumen + hair_thickness=mittel
           → moxie_mousse|volumen_spray styling_1).

Vor allen Edits: CSV-Backup beider betroffenen Tabs.
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))

from sheets_writer import DOC_ID, load_env, open_sheet, resolve_sa_path

TS = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP_DIR = REPO / "backups" / f"sheets_{TS}_pre_migration21"


V1_REGEL_OLD = (
    '{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},'
    '{"eq":["normalized.hair_treatments","blondiert"]}]}'
)
V1_REGEL_NEW = (
    '{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},'
    '{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}'
)

V2_REGEL_OLD = (
    '{"cases":['
    '{"when":{"or":['
    '{"includes":["normalized.hair_condition","haarbruch"]},'
    '{"includes":["normalized.hair_condition","spliss"]},'
    '{"and":[{"eq":["normalized.hair_structure","kraus"]},'
    '{"eq":["normalized.ends_condition","deutlich_trocken"]}]}'
    ']},"then":"stark_verfilzt"},'
    '{"when":{"or":['
    '{"and":[{"includes":["normalized.hair_condition","trocken"]},'
    '{"not":{"includes":["normalized.hair_condition","haarbruch"]}}]},'
    '{"and":[{"eq":["normalized.hair_structure","lockig"]},'
    '{"not":{"includes":["normalized.hair_condition","keine_probleme"]}}]}'
    ']},"then":"leicht_verfilzt"}'
    '],"else":"problemlos"}'
)
V2_REGEL_NEW = (
    '{"cases":['
    '{"when":{"or":['
    '{"includes":["normalized.hair_condition","haarbruch"]},'
    '{"includes":["normalized.hair_condition","spliss"]},'
    '{"and":[{"eq":["normalized.hair_structure","kraus"]},'
    '{"eq":["normalized.ends_condition","deutlich_trocken"]}]}'
    ']},"then":"stark_verfilzt"},'
    '{"when":{"or":['
    '{"and":[{"includes":["normalized.hair_condition","trocken"]},'
    '{"not":{"includes":["normalized.hair_condition","haarbruch"]}}]},'
    '{"and":[{"in":["normalized.hair_structure",["lockig","kraus"]]},'
    '{"not":{"includes":["normalized.hair_condition","keine_probleme"]}}]}'
    ']},"then":"leicht_verfilzt"}'
    '],"else":"problemlos"}'
)

REQ_11C = {
    "regel_id": "REQ-11c",
    "slot_typ": "styling_1",
    "prioritaet": "required_conditional",
    "trigger_flag": "needs_curl_care",
    "trigger_wert": "TRUE",
    "trigger_flag2": "heat_use",
    "trigger_wert2": "maybe",
    "overrides": "",
    "requires_not": "",
    "filter": "curl_creme",
    "reason": (
        "Curl-Creme als primaeres Styling bei Locken/Wellen + "
        "gelegentlicher Hitze (Migration #21 V5, PDF-belegt: "
        "curl_creme + Diffusor okay)"
    ),
    "aktiv": "TRUE",
}

REQ_19B = {
    "regel_id": "REQ-19b",
    "slot_typ": "styling_1",
    "prioritaet": "optional",
    "trigger_flag": "styling_goal_volumen",
    "trigger_wert": "TRUE",
    "trigger_flag2": "hair_thickness",
    "trigger_wert2": "mittel",
    "overrides": "",
    "requires_not": "",
    "filter": "moxie_mousse|volumen_spray",
    "reason": (
        "Volumen-Styling bei Volumen-Ziel + mittlerem Haar "
        "(Migration #21 V6, PDF-belegt: moxie_mousse FAQ "
        "+ volumen_spray Header)"
    ),
    "aktiv": "TRUE",
}

REQ_04_REQUIRES_NOT_OLD = "REQ-11,REQ-11b,REQ-04b"
REQ_04_REQUIRES_NOT_NEW = "REQ-11,REQ-11b,REQ-04b,REQ-11c"


def backup_tab(ws, out_dir: Path) -> int:
    values = ws.get_all_values()
    if not values:
        return 0
    out_path = out_dir / f"{ws.title}.csv"
    with out_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for row in values:
            w.writerow(row)
    print(f"  Backup: {out_path.relative_to(REPO)} ({len(values)-1} Zeilen)")
    return len(values) - 1


def find_row(ws, headers, key_col, key_val):
    all_values = ws.get_all_values()
    key_idx = headers.index(key_col)
    for i, row in enumerate(all_values[1:], start=2):
        if len(row) > key_idx and row[key_idx] == key_val:
            return i, dict(zip(headers, row + [""] * (len(headers) - len(row))))
    return None, None


def update_cell_verified(ws, headers, key_col, key_val, col, expected_old, new_val, *, json_compare=False):
    row_idx, row = find_row(ws, headers, key_col, key_val)
    if row_idx is None:
        raise RuntimeError(f"Zeile {key_col}={key_val} nicht gefunden in {ws.title}")
    cur = row.get(col, "")
    if json_compare:
        try:
            equal = json.loads(cur) == json.loads(expected_old)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Pre-Check {ws.title}/{key_val}/{col}: JSON-Parse-Fehler: {e}")
    else:
        equal = (cur == expected_old)
    if not equal:
        raise RuntimeError(
            f"Pre-Check {ws.title}/{key_val}/{col} fehlgeschlagen.\n"
            f"  Erwartet: {expected_old!r}\n"
            f"  Aktuell:  {cur!r}"
        )
    col_idx = headers.index(col) + 1
    ws.update_cell(row_idx, col_idx, new_val)
    print(f"  ✓ {ws.title} / {key_val} / {col} aktualisiert")


def append_row_dict(ws, headers, row_dict):
    row_id = row_dict.get("regel_id") or row_dict.get("konflikt_id", "?")
    # Sanity: regel_id darf noch nicht existieren
    existing_idx, _ = find_row(ws, headers, "regel_id", row_id)
    if existing_idx is not None:
        raise RuntimeError(f"regel_id {row_id} existiert bereits in {ws.title} (Zeile {existing_idx})")
    row = [row_dict.get(h, "") for h in headers]
    ws.append_row(row, value_input_option="USER_ENTERED")
    print(f"  ✓ {ws.title} append: {row_id}")


def main() -> int:
    env = load_env(REPO / ".env")
    sa_path = resolve_sa_path(env, REPO)
    sheet = open_sheet(sa_path, DOC_ID)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Backups → {BACKUP_DIR.relative_to(REPO)}/")

    ws_dv = sheet.worksheet("map_derived_variables")
    ws_sr = sheet.worksheet("map_slot_rules")
    backup_tab(ws_dv, BACKUP_DIR)
    backup_tab(ws_sr, BACKUP_DIR)

    dv_headers = ws_dv.row_values(1)
    sr_headers = ws_sr.row_values(1)
    print(f"\nmap_derived_variables headers: {dv_headers}")
    print(f"map_slot_rules headers: {sr_headers}")

    # Pre-Check für REQ-11c/REQ-19b — Spalten müssen alle bekannt sein
    unknown_11c = set(REQ_11C) - set(sr_headers)
    unknown_19b = set(REQ_19B) - set(sr_headers)
    if unknown_11c or unknown_19b:
        raise RuntimeError(
            f"Unbekannte Spalten — REQ-11c: {unknown_11c}, REQ-19b: {unknown_19b}"
        )

    print("\n— V1: needs_repair_focus.regel_json —")
    update_cell_verified(
        ws_dv, dv_headers,
        key_col="variable", key_val="needs_repair_focus",
        col="regel_json",
        expected_old=V1_REGEL_OLD, new_val=V1_REGEL_NEW,
        json_compare=True,
    )

    print("\n— V2: detangling_need.regel_json —")
    update_cell_verified(
        ws_dv, dv_headers,
        key_col="variable", key_val="detangling_need",
        col="regel_json",
        expected_old=V2_REGEL_OLD, new_val=V2_REGEL_NEW,
        json_compare=True,
    )

    print("\n— V5: REQ-04.requires_not erweitern —")
    update_cell_verified(
        ws_sr, sr_headers,
        key_col="regel_id", key_val="REQ-04",
        col="requires_not",
        expected_old=REQ_04_REQUIRES_NOT_OLD, new_val=REQ_04_REQUIRES_NOT_NEW,
    )

    print("\n— V5: REQ-11c anfügen —")
    append_row_dict(ws_sr, sr_headers, REQ_11C)

    print("\n— V6: REQ-19b anfügen —")
    append_row_dict(ws_sr, sr_headers, REQ_19B)

    # Sanity: JSON neu lesen und parsbar prüfen
    print("\n— Sanity-Check: regel_json beider geänderten Zeilen JSON-valide —")
    for var, expected_new in [
        ("needs_repair_focus", V1_REGEL_NEW),
        ("detangling_need", V2_REGEL_NEW),
    ]:
        _, row = find_row(ws_dv, dv_headers, "variable", var)
        cur = row.get("regel_json", "")
        if json.loads(cur) != json.loads(expected_new):
            raise RuntimeError(f"Post-Check {var}: Sheet-Wert weicht ab")
        print(f"  ✓ {var}: JSON-strukturgleich + valide")

    print(f"\nMigration #21 erfolgreich. Backup: {BACKUP_DIR.relative_to(REPO)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
