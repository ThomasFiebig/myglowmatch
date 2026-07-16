#!/usr/bin/env python3
"""
Weg 1 (2026-07-16): 3 Fragen -> 1 Frage + Punkte-Rebalancing.

Aenderungen im Google-Sheet:
  1. map_pflegelevel_scoring:
     - PFL-16, PFL-17, PFL-18, PFL-19 (styling_effort) -> aktiv=FALSE
     - PFL-21 (mittel)              punkte 1 -> 2
     - PFL-22 (bewusst_regelmaessig) punkte 2 -> 5
  2. map_derived_variables:
     - styling_goal_halt umziehen: styling_effort=aufwendiges_styling
       -> time_commitment=bewusst_regelmaessig

Ergebnis: neue Frage im Fragebogen setzt aus einer Antwort routine_preference +
time_commitment aligned. Der styling_effort-Wert entfaellt komplett (weder im
Fragebogen noch in Regeln).

Sicherheitsstopps:
  - Backup jeder geaenderten Zelle vor Ueberschreibung
  - Verifikation durch Re-Read

Aufruf:
  python3 patch_weg1_pfl_und_moxie.py --dry-run
  python3 patch_weg1_pfl_und_moxie.py --yes
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from sheets_writer import load_env, open_sheet, resolve_sa_path

BACKUP_DIR = Path(__file__).parent / "backups"

# --- Aenderungen deklarativ -----------------------------------------------

SCORING_UPDATES = [
    # (regel_id, {spalte: neuer_wert})
    ("PFL-16", {"aktiv": "FALSE"}),
    ("PFL-17", {"aktiv": "FALSE"}),
    ("PFL-18", {"aktiv": "FALSE"}),
    ("PFL-19", {"aktiv": "FALSE"}),
    ("PFL-21", {"punkte": "2"}),
    ("PFL-22", {"punkte": "5"}),
]

NEW_STYLING_GOAL_HALT = {
    "and": [
        {"eq": ["normalized.time_commitment", "bewusst_regelmaessig"]},
        {"in": ["normalized.hair_thickness", ["fein", "mittel"]]},
        {"in": ["normalized.hair_structure", ["glatt", "wellig"]]},
    ]
}
NEW_STYLING_GOAL_HALT_DOKU = (
    "Moxie-Mousse-Trigger (Weg 1, 2026-07-16): bewusst_regelmaessig-Zeit-"
    "Wunsch auf feinem/mittlerem glatten/welligem Haar. Ersetzt Migration"
    " #? (aufwendiges_styling-Trigger auf styling_effort, das nun entfaellt)."
)


def update_scoring(ws, dry_run: bool, backups: dict) -> None:
    all_values = ws.get_all_values()
    header = all_values[0]

    rid_idx = header.index("regel_id")
    aktiv_idx = header.index("aktiv")
    punkte_idx = header.index("punkte")

    print("\n=== map_pflegelevel_scoring ===")
    for regel_id, updates in SCORING_UPDATES:
        # Zeile finden
        target_row = None
        for i, row in enumerate(all_values[1:], start=2):
            if len(row) > rid_idx and row[rid_idx] == regel_id:
                target_row = i
                current_row = row
                break
        if target_row is None:
            print(f"  ✗ {regel_id}: nicht gefunden — SKIP")
            continue

        # Backup + Update pro Spalte
        for col_name, new_val in updates.items():
            col_idx = header.index(col_name)
            old_val = current_row[col_idx] if len(current_row) > col_idx else ""
            backups.setdefault("scoring", {}).setdefault(regel_id, {})[col_name] = old_val
            print(f"  {regel_id}.{col_name}: {old_val!r} -> {new_val!r}")
            if not dry_run:
                ws.update_cell(target_row, col_idx + 1, new_val)


def update_derived_styling_goal(ws, dry_run: bool, backups: dict) -> None:
    all_values = ws.get_all_values()
    header = all_values[0]

    var_idx = header.index("variable")
    regel_idx = header.index("regel_json")
    doku_idx = header.index("doku")

    print("\n=== map_derived_variables ===")
    target_row = None
    for i, row in enumerate(all_values[1:], start=2):
        if len(row) > var_idx and row[var_idx] == "styling_goal_halt":
            target_row = i
            current = row
            break
    if target_row is None:
        print("  ✗ styling_goal_halt nicht gefunden — SKIP")
        return

    old_json = current[regel_idx] if len(current) > regel_idx else ""
    old_doku = current[doku_idx] if len(current) > doku_idx else ""
    backups["styling_goal_halt"] = {"regel_json": old_json, "doku": old_doku}

    new_json = json.dumps(NEW_STYLING_GOAL_HALT, separators=(",", ":"))
    print(f"  regel_json: {old_json[:80]}...")
    print(f"           -> {new_json[:80]}...")
    print(f"  doku      : (aktualisiert)")

    if not dry_run:
        ws.update_cell(target_row, regel_idx + 1, new_json)
        ws.update_cell(target_row, doku_idx + 1, NEW_STYLING_GOAL_HALT_DOKU)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--yes", action="store_true", help="Confirm ueberspringen")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    sa_path = resolve_sa_path(env, repo_dir)
    sh = open_sheet(sa_path)

    backups = {}

    ws_scoring = sh.worksheet("map_pflegelevel_scoring")
    update_scoring(ws_scoring, dry_run=True, backups=backups)  # zeigen

    ws_derived = sh.worksheet("map_derived_variables")
    update_derived_styling_goal(ws_derived, dry_run=True, backups=backups)  # zeigen

    # Backup schreiben
    BACKUP_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    bpath = BACKUP_DIR / f"weg1_pre_change_{ts}.json"
    bpath.write_text(json.dumps({"timestamp": ts, "backups": backups}, indent=2, ensure_ascii=False))
    print(f"\n✓ Backup: {bpath.relative_to(repo_dir)}")

    if args.dry_run:
        print("\n[dry-run] Kein Schreib-Zugriff.")
        return 0

    if not args.yes:
        ans = input("\nWirklich schreiben? (yes/no): ").strip().lower()
        if ans not in ("yes", "y", "ja", "j"):
            print("Abgebrochen.")
            return 1

    # SCHARF: gleiche Funktionen mit dry_run=False
    print("\n=== SCHARF SCHREIBEN ===")
    update_scoring(ws_scoring, dry_run=False, backups={})
    update_derived_styling_goal(ws_derived, dry_run=False, backups={})

    print(f"\n✓ Alle Aenderungen im Sheet gespeichert.")
    print(f"  Rollback: siehe {bpath.relative_to(repo_dir)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
