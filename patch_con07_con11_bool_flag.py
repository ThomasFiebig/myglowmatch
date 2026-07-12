#!/usr/bin/env python3
"""
Layer-2-Umbau CON-07 + CON-11.

CON-07: neues Bool-Flag `ist_hitzeschutz_solo` (nur hitzeschutzspray=TRUE).
        match_typ: produkt_key → bool_flag
        match_wert: hitzeschutzspray → ist_hitzeschutz_solo

CON-11: bool_flag=ist_smoothing + slot_scope-Liste (shampoo,spuelung,styling_1).
        match_typ: produkt_key → bool_flag
        match_wert: smoothing_shampoo,... → ist_smoothing
        slot_scope: (leer) → shampoo,spuelung,styling_1

Beide 0-Drift gegen test_results_20260712_003453.json.
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env, resolve_sa_path, open_sheet


NEW_PD_COL = "ist_hitzeschutz_solo"
PD_TRUE_KEYS = ["hitzeschutzspray"]

CON07_UPDATES = {
    "beschreibung": "Dediziertes Hitzeschutz-Produkt sinnlos ohne Glätteisen/Lockenstab",
    "match_typ": "bool_flag",
    "match_wert": "ist_hitzeschutz_solo",
    "slot_scope": "",
}
CON11_UPDATES = {
    "beschreibung": "Smoothing-Produkte bei Definitions-Ziel unterdrücken (glätten zerstört Locken/Wellen-Definition). Tiefenbehandlung ist eine Kur (Slot maske) und bleibt ausgenommen — datenblatt-belegt auch für Locken.",
    "match_typ": "bool_flag",
    "match_wert": "ist_smoothing",
    "slot_scope": "shampoo,spuelung,styling_1",
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


def set_flag_for_products(ws, col_idx: int, product_keys: list[str], value: str) -> list[str]:
    values = ws.get_all_values()
    headers = values[0]
    key_idx = headers.index("produkt_key")
    updated = []
    for i, row in enumerate(values[1:], start=2):
        if row[key_idx] in product_keys:
            ws.update_cell(i, col_idx, value)
            updated.append(row[key_idx])
    return updated


def update_rule(ws, konflikt_id: str, updates: dict) -> dict:
    values = ws.get_all_values()
    headers = values[0]
    id_idx = headers.index("konflikt_id")
    row_idx = None
    row_data = None
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
    out_dir = repo / "backups" / f"sheets_{ts}_con07_con11_pre"
    out_dir.mkdir(parents=True, exist_ok=True)

    ws_pd = sh.worksheet("produktdatenbank")
    ws_con = sh.worksheet("map_conflict_rules")

    print(f"[1/4] Backup → {out_dir.relative_to(repo)}/")
    for ws in (ws_pd, ws_con):
        backup_tab(ws, out_dir)
        print(f"      {ws.title}.csv")

    print(f"[2/4] Spalte '{NEW_PD_COL}' in produktdatenbank sicherstellen …")
    col_idx, added = ensure_column(ws_pd, NEW_PD_COL)
    print(f"      {'+' if added else '='} Position {col_idx}")
    updated = set_flag_for_products(ws_pd, col_idx, PD_TRUE_KEYS, "TRUE")
    missing = set(PD_TRUE_KEYS) - set(updated)
    for k in updated:
        print(f"      ✓ {k}.{NEW_PD_COL} = TRUE")
    if missing:
        print(f"      ⚠ Nicht gefunden: {missing}", file=sys.stderr)
        return 1

    print(f"[3/4] CON-07 umstellen …")
    diffs = update_rule(ws_con, "CON-07", CON07_UPDATES)
    for col, (old, new) in diffs.items():
        print(f"      {col}:")
        print(f"        alt: {old!r}")
        print(f"        neu: {new!r}")

    print(f"[4/4] CON-11 umstellen …")
    diffs = update_rule(ws_con, "CON-11", CON11_UPDATES)
    for col, (old, new) in diffs.items():
        print(f"      {col}:")
        print(f"        alt: {old!r}")
        print(f"        neu: {new!r}")

    print("\nFertig. Nächster Schritt: python3 sync_rules_to_workflow.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
