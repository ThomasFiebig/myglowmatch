#!/usr/bin/env python3
"""
Layer-2-Umbau POOL-01 — Marken-Referenz `produktlinie=bond_iq` durch
markenneutrales Bool-Flag `ist_bonding_line` ersetzen.

Ablauf (idempotent):
  1) CSV-Backup produktdatenbank + map_pool_filter → backups/sheets_YYYYMMDD_HHMMSS_pool01_pre/
  2) Neue Spalte `ist_bonding_line` in produktdatenbank hinzufügen (falls fehlt).
  3) 4 Bond-IQ-Produkte auf TRUE setzen.
  4) POOL-01 in map_pool_filter auf `ist_bonding_line:is_true` umstellen +
     Beschreibung markenneutralisieren.

Kein Sync — der läuft danach manuell via sync_rules_to_workflow.py.
"""
import csv
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env, resolve_sa_path, open_sheet


NEW_COL = "ist_bonding_line"
BOND_IQ_PRODUCTS = [
    "bond_iq_leave_in",
    "bond_iq_night_day_serum",
    "bond_iq_shampoo",
    "bond_iq_spuelung",
]
POOL01_UPDATES = {
    "beschreibung": "Dedizierte Bonding-/Repair-Sub-Linie nur bei Reparatur-Fokus zulassen",
    "produkt_bedingungen": "ist_bonding_line:is_true",
}


def backup_tab(ws, out_dir: Path) -> Path:
    out = out_dir / f"{ws.title}.csv"
    values = ws.get_all_values()
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        for row in values:
            w.writerow(row)
    return out


def ensure_column(ws, col_name: str) -> tuple[int, bool]:
    """Fügt Spalte am Ende hinzu, falls fehlt. Gibt (col_idx_1based, was_added).
    Erweitert Grid, falls nötig (n8n-Sheet ist fix auf N Spalten begrenzt)."""
    values = ws.get_all_values()
    headers = values[0]
    if col_name in headers:
        return headers.index(col_name) + 1, False
    new_idx = len(headers) + 1
    if ws.col_count < new_idx:
        ws.add_cols(new_idx - ws.col_count)
    ws.update_cell(1, new_idx, col_name)
    return new_idx, True


def set_flag_for_products(ws, col_idx: int, product_keys: list[str], value: str) -> list[str]:
    """Setzt Spalte für gegebene produkt_key-Werte. Gibt Liste der aktualisierten Keys."""
    values = ws.get_all_values()
    headers = values[0]
    if "produkt_key" not in headers:
        raise KeyError("produkt_key nicht in produktdatenbank-Header.")
    key_idx = headers.index("produkt_key")
    updated = []
    for i, row in enumerate(values[1:], start=2):
        if row[key_idx] in product_keys:
            ws.update_cell(i, col_idx, value)
            updated.append(row[key_idx])
    return updated


def update_pool_rule(ws, regel_id: str, updates: dict) -> dict:
    """Findet Regel-Zeile via regel_id und aktualisiert Spalten. Gibt {col: (alt, neu)}."""
    values = ws.get_all_values()
    headers = values[0]
    id_idx = headers.index("regel_id")
    row_idx = None
    for i, row in enumerate(values[1:], start=2):
        if row[id_idx] == regel_id:
            row_idx = i
            row_data = row
            break
    if row_idx is None:
        raise KeyError(f"{regel_id} nicht in map_pool_filter.")
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
    out_dir = repo / "backups" / f"sheets_{ts}_pool01_pre"
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/4] Backup → {out_dir.relative_to(repo)}/")
    ws_pd = sh.worksheet("produktdatenbank")
    ws_pool = sh.worksheet("map_pool_filter")
    for ws in (ws_pd, ws_pool):
        p = backup_tab(ws, out_dir)
        print(f"      {p.name}")

    print(f"[2/4] Spalte '{NEW_COL}' in produktdatenbank sicherstellen …")
    col_idx, added = ensure_column(ws_pd, NEW_COL)
    if added:
        print(f"      + neue Spalte an Position {col_idx}")
    else:
        print(f"      = Spalte existiert bereits an Position {col_idx}")

    print(f"[3/4] Bond-IQ-Produkte (4) auf TRUE setzen …")
    updated = set_flag_for_products(ws_pd, col_idx, BOND_IQ_PRODUCTS, "TRUE")
    missing = set(BOND_IQ_PRODUCTS) - set(updated)
    for k in updated:
        print(f"      ✓ {k}.{NEW_COL} = TRUE")
    if missing:
        print(f"      ⚠ Nicht gefunden: {missing}", file=sys.stderr)
        return 1

    print(f"[4/4] POOL-01 in map_pool_filter umstellen …")
    diffs = update_pool_rule(ws_pool, "POOL-01", POOL01_UPDATES)
    for col, (old, new) in diffs.items():
        print(f"      {col}:")
        print(f"        alt: {old!r}")
        print(f"        neu: {new!r}")

    print("\nFertig. Nächster Schritt: python3 sync_rules_to_workflow.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
