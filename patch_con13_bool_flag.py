#!/usr/bin/env python3
"""
Layer-2-Umbau CON-13 — hardcoded produkt_key `smoothing_fohn_spray` durch
markenneutrales `bool_flag` + `slot_scope` ersetzen.

Voraussetzung: Node 14 unterstützt bereits `match_typ='bool_flag'` und
`slot_scope` (siehe patch_node14_bool_flag.py).

Ablauf (idempotent):
  1) CSV-Backup map_conflict_rules
  2) Spalte `slot_scope` in map_conflict_rules sicherstellen
  3) CON-13-Zeile umstellen:
     match_typ  produkt_key         → bool_flag
     match_wert smoothing_fohn_spray → ist_smoothing
     slot_scope (leer)              → styling_1
     beschreibung: MONAT-Referenz raus
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env, resolve_sa_path, open_sheet


NEW_COL = "slot_scope"
CON13_UPDATES = {
    "beschreibung": "Smoothing-Styling-Produkt bei Locken-Pflege + Frizz blockieren — Curl-Styling behandelt Frizz bei Locken besser",
    "match_typ": "bool_flag",
    "match_wert": "ist_smoothing",
    "slot_scope": "styling_1",
}


def backup_tab(ws, out_dir: Path) -> Path:
    out = out_dir / f"{ws.title}.csv"
    with out.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows(ws.get_all_values())
    return out


def ensure_column(ws, col_name: str) -> tuple[int, bool]:
    headers = ws.get_all_values()[0]
    if col_name in headers:
        return headers.index(col_name) + 1, False
    new_idx = len(headers) + 1
    if ws.col_count < new_idx:
        ws.add_cols(new_idx - ws.col_count)
    ws.update_cell(1, new_idx, col_name)
    return new_idx, True


def update_rule(ws, konflikt_id: str, updates: dict) -> dict:
    values = ws.get_all_values()
    headers = values[0]
    id_idx = headers.index("konflikt_id")
    row_idx = None
    for i, row in enumerate(values[1:], start=2):
        if row[id_idx] == konflikt_id:
            row_idx = i
            row_data = row
            break
    if row_idx is None:
        raise KeyError(f"{konflikt_id} nicht in map_conflict_rules.")
    diffs = {}
    for col, new_val in updates.items():
        col_idx = headers.index(col) + 1
        old_val = row_data[col_idx - 1] if col_idx - 1 < len(row_data) else ""
        ws.update_cell(row_idx, col_idx, new_val)
        diffs[col] = (old_val, new_val)
    return diffs


def main() -> int:
    repo = Path(__file__).parent
    env = load_env(repo / ".env")
    sa = resolve_sa_path(env, repo)
    sh = open_sheet(sa)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    out_dir = repo / "backups" / f"sheets_{ts}_con13_pre"
    out_dir.mkdir(parents=True, exist_ok=True)

    ws = sh.worksheet("map_conflict_rules")
    print(f"[1/3] Backup → {out_dir.relative_to(repo)}/{ws.title}.csv")
    backup_tab(ws, out_dir)

    print(f"[2/3] Spalte '{NEW_COL}' sicherstellen …")
    col_idx, added = ensure_column(ws, NEW_COL)
    print(f"      {'+' if added else '='} Position {col_idx}")

    print(f"[3/3] CON-13 umstellen …")
    diffs = update_rule(ws, "CON-13", CON13_UPDATES)
    for col, (old, new) in diffs.items():
        print(f"      {col}:")
        print(f"        alt: {old!r}")
        print(f"        neu: {new!r}")

    print("\nFertig. Nächster Schritt: python3 sync_rules_to_workflow.py")
    return 0

from sheets_writer import resolve_sa_path  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
