#!/usr/bin/env python3
"""
Google-Sheets-Writer für die MONAT-Produktdatenbank
====================================================
Service-Account-basierter Lese-/Schreibzugriff via gspread + google-auth.

Library-Funktionen:
  - open_sheet(sa_path, doc_id) → gspread.Spreadsheet
  - read_row(sheet, tab, key_col, key_val) → dict (header → value)
  - update_cell(sheet, tab, key_col, key_val, col, new_val) → bool
  - update_row(sheet, tab, key_col, key_val, updates: dict) → bool

CLI:
  python3 sheets_writer.py read   --tab T --key-col K --key-val V [--col C]
  python3 sheets_writer.py update --tab T --key-col K --key-val V --col C --new-val NV
"""

import argparse
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials


SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
DOC_ID = "1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A"


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


def resolve_sa_path(env: dict, base_dir: Path) -> Path:
    raw = env.get("GOOGLE_SHEETS_SA_PATH")
    if not raw:
        raise RuntimeError("GOOGLE_SHEETS_SA_PATH nicht in .env gesetzt.")
    p = Path(raw).expanduser()
    if not p.is_absolute():
        p = (base_dir / p).resolve()
    if not p.exists():
        raise FileNotFoundError(f"Service-Account-Datei nicht gefunden: {p}")
    return p


def open_sheet(sa_path: Path, doc_id: str = DOC_ID):
    creds = Credentials.from_service_account_file(str(sa_path), scopes=SCOPES)
    gc = gspread.authorize(creds)
    return gc.open_by_key(doc_id)


def _find_row(ws, key_col: str, key_val: str):
    """Returns (row_idx_1based, headers, row_dict) or (None, headers, {})."""
    all_values = ws.get_all_values()
    if not all_values:
        return None, [], {}
    headers = all_values[0]
    if key_col not in headers:
        raise KeyError(
            f"Spalte '{key_col}' nicht in Tab '{ws.title}' gefunden. "
            f"Verfügbar: {headers}"
        )
    key_idx = headers.index(key_col)
    for i, row in enumerate(all_values[1:], start=2):
        if len(row) > key_idx and row[key_idx] == key_val:
            row_dict = {h: (row[j] if j < len(row) else "") for j, h in enumerate(headers)}
            return i, headers, row_dict
    return None, headers, {}


def read_row(sheet, tab: str, key_col: str, key_val: str) -> dict:
    ws = sheet.worksheet(tab)
    _, _, row_dict = _find_row(ws, key_col, key_val)
    return row_dict


def update_cell(sheet, tab: str, key_col: str, key_val: str, col: str, new_val: str) -> bool:
    ws = sheet.worksheet(tab)
    row_idx, headers, _ = _find_row(ws, key_col, key_val)
    if row_idx is None:
        raise KeyError(f"Keine Zeile mit {key_col}='{key_val}' in Tab '{tab}'")
    if col not in headers:
        raise KeyError(f"Spalte '{col}' nicht in Tab '{tab}'. Verfügbar: {headers}")
    col_idx = headers.index(col) + 1
    ws.update_cell(row_idx, col_idx, new_val)
    return True


def update_row(sheet, tab: str, key_col: str, key_val: str, updates: dict) -> bool:
    """Mehrere Spalten in einer Zeile sequenziell updaten."""
    ws = sheet.worksheet(tab)
    row_idx, headers, _ = _find_row(ws, key_col, key_val)
    if row_idx is None:
        raise KeyError(f"Keine Zeile mit {key_col}='{key_val}' in Tab '{tab}'")
    for col in updates:
        if col not in headers:
            raise KeyError(f"Spalte '{col}' nicht in Tab '{tab}'. Verfügbar: {headers}")
    for col, new_val in updates.items():
        col_idx = headers.index(col) + 1
        ws.update_cell(row_idx, col_idx, new_val)
    return True


def main():
    env = load_env(Path(__file__).parent / ".env")
    sa_path = resolve_sa_path(env, Path(__file__).parent)

    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_read = sub.add_parser("read", help="Eine Zeile lesen")
    p_read.add_argument("--tab", required=True)
    p_read.add_argument("--key-col", required=True)
    p_read.add_argument("--key-val", required=True)
    p_read.add_argument("--col", default=None)

    p_upd = sub.add_parser("update", help="Eine Zelle schreiben")
    p_upd.add_argument("--tab", required=True)
    p_upd.add_argument("--key-col", required=True)
    p_upd.add_argument("--key-val", required=True)
    p_upd.add_argument("--col", required=True)
    p_upd.add_argument("--new-val", required=True)

    args = parser.parse_args()

    sheet = open_sheet(sa_path, DOC_ID)

    if args.cmd == "read":
        row = read_row(sheet, args.tab, args.key_col, args.key_val)
        if not row:
            print(f"Keine Zeile mit {args.key_col}='{args.key_val}' in '{args.tab}'", file=sys.stderr)
            sys.exit(1)
        if args.col:
            if args.col not in row:
                print(f"Spalte '{args.col}' nicht in Tab '{args.tab}'", file=sys.stderr)
                sys.exit(1)
            print(f"{args.key_val}.{args.col} = {row[args.col]!r}")
        else:
            for k, v in row.items():
                print(f"  {k:25s} = {v}")
    elif args.cmd == "update":
        update_cell(sheet, args.tab, args.key_col, args.key_val, args.col, args.new_val)
        print(f"OK: {args.tab} / {args.key_val} / {args.col} ← {args.new_val!r}")


if __name__ == "__main__":
    main()
