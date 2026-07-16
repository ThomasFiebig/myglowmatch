#!/usr/bin/env python3
"""
Weg B (2026-07-16): heat_use-Ableitung um heat_tools erweitern.

Aktuelle Regel liest NUR heat_frequency:
  - regelmaessig -> yes (Hitzeschutz zwingend)
  - gelegentlich -> maybe
  - nie_selten   -> no

Neue Regel liest heat_tools + heat_frequency zusammen:
  - Glaetteisen ODER Lockenstab + regelmaessig -> yes
  - Alle anderen Kombinationen mit Hitze       -> maybe
  - nie_selten                                  -> no

Effekt:
  - Reine Föhn-Nutzerin (heat_tools=[foehn]) bekommt heat_use=maybe
    -> REQ-11c triggert -> Lockentraegerin behaelt curl_creme
  - Glaetteisen-Nutzerin bekommt weiterhin heat_use=yes -> Hitzeschutz

Sicherheitsstopp:
  - Backup der alten regel_json wird gespeichert bevor überschrieben wird
  - Verifikation durch Re-Read nach Update

Aufruf:
  python3 patch_heat_use_rule_weg_b.py --dry-run
  python3 patch_heat_use_rule_weg_b.py           # scharf, aber mit Confirm
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from sheets_writer import load_env, open_sheet, resolve_sa_path

TAB = "map_derived_variables"
KEY_COL = "variable"
KEY_VAL = "heat_use"
BACKUP_DIR = Path(__file__).parent / "backups"

NEW_REGEL_JSON = {
    "cases": [
        {
            "when": {
                "and": [
                    {
                        "intersects": [
                            "normalized.heat_tools",
                            ["glaetteisen", "lockenstab"],
                        ]
                    },
                    {"eq": ["normalized.heat_frequency", "regelmaessig"]},
                ]
            },
            "then": "yes",
        },
        {
            "when": {"neq": ["normalized.heat_frequency", "nie_selten"]},
            "then": "maybe",
        },
    ],
    "else": "no",
}

NEW_DOKU = (
    "Hitzeschutz-Trigger 3-stufig (Weg B, 2026-07-16): Glaetteisen ODER "
    "Lockenstab + regelmaessig=yes; alle anderen Hitze-Kombinationen (Foehn "
    "allein, Glaetteisen/Lockenstab gelegentlich)=maybe; nie_selten=no. "
    "Ersetzt Migration #18 (2026-06-26). REQ-11c faengt Locken-Traegerinnen "
    "die nur foehnen ab (curl_creme bleibt, PDF-belegt Diffusor okay)."
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="Nur Diff anzeigen, nicht schreiben.")
    parser.add_argument("--yes", action="store_true", help="Confirm überspringen (fuer Skript-Aufrufe).")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    sa_path = resolve_sa_path(env, repo_dir)
    sh = open_sheet(sa_path)
    ws = sh.worksheet(TAB)

    # Header + Zeile lesen
    all_values = ws.get_all_values()
    header = all_values[0]
    rows = all_values[1:]

    # Spalten-Index bestimmen
    if KEY_COL not in header:
        raise SystemExit(f"Spalte '{KEY_COL}' nicht in Header: {header}")
    if "regel_json" not in header:
        raise SystemExit(f"Spalte 'regel_json' nicht in Header: {header}")
    if "doku" not in header:
        raise SystemExit(f"Spalte 'doku' nicht in Header: {header}")

    key_idx = header.index(KEY_COL)
    regel_json_idx = header.index("regel_json")
    doku_idx = header.index("doku")

    # Ziel-Zeile finden (1-basierter Row-Index für gspread, +1 für Header)
    target_row_num = None
    old_regel_json = None
    old_doku = None
    for i, row in enumerate(rows):
        if len(row) > key_idx and row[key_idx] == KEY_VAL:
            target_row_num = i + 2  # gspread: Header=1, erste Datenzeile=2
            old_regel_json = row[regel_json_idx] if len(row) > regel_json_idx else ""
            old_doku = row[doku_idx] if len(row) > doku_idx else ""
            break

    if target_row_num is None:
        raise SystemExit(f"Zeile mit {KEY_COL}={KEY_VAL!r} nicht gefunden in {TAB}")

    print(f"Ziel: {TAB}, Zeile {target_row_num} ({KEY_COL}={KEY_VAL!r})\n")
    print("=== ALTE regel_json ===")
    print(old_regel_json)
    print("\n=== NEUE regel_json ===")
    print(json.dumps(NEW_REGEL_JSON, indent=2))
    print("\n=== ALTE doku ===")
    print(old_doku[:200])
    print("\n=== NEUE doku ===")
    print(NEW_DOKU)

    # Backup
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"heat_use_pre_weg_b_{ts}.json"
    backup_path.write_text(json.dumps({
        "timestamp": ts,
        "tab": TAB,
        "row_num": target_row_num,
        "old_regel_json": old_regel_json,
        "old_doku": old_doku,
    }, indent=2, ensure_ascii=False))
    print(f"\n✓ Backup gesichert: {backup_path.relative_to(repo_dir)}")

    if args.dry_run:
        print("\n[dry-run] Kein Schreib-Zugriff.")
        return 0

    # Confirm
    if not args.yes:
        ans = input("\nWirklich schreiben? (yes/no): ").strip().lower()
        if ans not in ("yes", "y", "ja", "j"):
            print("Abgebrochen.")
            return 1

    # Update: regel_json + doku in einem Batch
    new_json_str = json.dumps(NEW_REGEL_JSON, separators=(",", ":"))
    ws.update_cell(target_row_num, regel_json_idx + 1, new_json_str)
    ws.update_cell(target_row_num, doku_idx + 1, NEW_DOKU)
    print("\n✓ regel_json und doku aktualisiert.")

    # Verifikation: Re-read
    reread = ws.get_all_values()[target_row_num - 1]
    if reread[regel_json_idx].strip() == new_json_str.strip():
        print("✓ Verifikation grün — Sheet hat den neuen Wert.")
    else:
        print("✗ Verifikation FEHLGESCHLAGEN — Wert stimmt nicht überein!")
        return 1

    print(f"\nRollback: python3 -c \"import json; d=json.load(open('{backup_path.relative_to(repo_dir)}')); print(d['old_regel_json'])\"")
    return 0


if __name__ == "__main__":
    sys.exit(main())
