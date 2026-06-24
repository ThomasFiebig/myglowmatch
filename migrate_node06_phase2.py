#!/usr/bin/env python3
"""
Migration #10 — Node 06 Phase 2 ins Sheet (2026-06-24).

Schema-Erweiterung `map_pflegelevel_scoring`:
  - Neue Spalte `max_punkte` zwischen `punkte` und `beschreibung`
  - 22 bestehende Regeln: max_punkte leer (kein Cap)
  - Neue Zeile PFL-23 mit Operator `array_count_except`

Operator-Semantik (Node 06 muss mit-aktualisiert werden):
  array_count_except: zählt Array-Werte ungleich bedingung_wert,
                       Punkte = min(count × punkte, max_punkte)

Vorbedingung: Backup in backups/sheets_20260624_pre_node06_phase2/.
"""

import argparse
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from sheets_writer import load_env, resolve_sa_path, DOC_ID, SCOPES

TAB = "map_pflegelevel_scoring"

HEADER = ["regel_id", "kategorie", "bedingung_typ", "bedingung_feld",
          "bedingung_wert", "punkte", "max_punkte", "beschreibung", "aktiv"]

# Bestehende 22 Regeln (max_punkte leer)
EXISTING_ROWS = [
    ("PFL-01", "haarzustand", "array_contains", "hair_condition", "stark_geschaedigt", "4", "", "Haarzustand stark geschädigt", "TRUE"),
    ("PFL-02", "haarzustand", "array_contains", "hair_condition", "haarbruch", "3", "", "Haarbruch (nur wenn nicht bereits stark_geschaedigt)", "TRUE"),
    ("PFL-03", "haarzustand", "array_contains", "hair_condition", "spliss", "3", "", "Spliss (nur wenn nicht bereits stark_geschaedigt)", "TRUE"),
    ("PFL-04", "haarzustand", "array_contains", "hair_condition", "trocken", "2", "", "Trockenes Haar", "TRUE"),
    ("PFL-05", "haarzustand", "array_contains", "hair_condition", "duenn", "2", "", "Dünner werdendes Haar", "TRUE"),
    ("PFL-06", "haarzustand", "array_contains", "hair_condition", "frizz", "1", "", "Frizz", "TRUE"),
    ("PFL-07", "haarzustand", "array_contains", "hair_condition", "glanzlos", "1", "", "Glanzloses Haar", "TRUE"),
    ("PFL-08", "haarzustand", "array_contains", "hair_condition", "kraftlos", "1", "", "Kraftloses Haar / wenig Volumen", "TRUE"),
    ("PFL-09", "struktur", "equals", "hair_structure", "glatt", "0", "", "Struktur glatt", "TRUE"),
    ("PFL-10", "struktur", "equals", "hair_structure", "wellig", "1", "", "Struktur wellig", "TRUE"),
    ("PFL-11", "struktur", "equals", "hair_structure", "lockig", "1", "", "Struktur lockig", "TRUE"),
    ("PFL-12", "struktur", "equals", "hair_structure", "kraus", "2", "", "Struktur kraus / coily", "TRUE"),
    ("PFL-13", "belastung", "equals", "hair_treatments", "blondiert", "2", "", "Haar ist blondiert", "TRUE"),
    ("PFL-14", "belastung", "equals", "hair_treatments", "gefaerbt", "1", "", "Haar ist gefärbt (nicht blondiert)", "TRUE"),
    ("PFL-15", "belastung", "in_list", "heat_frequency", "regelmaessig|sehr_haeufig", "2", "", "Hitze-Styling regelmäßig oder häufig", "TRUE"),
    ("PFL-16", "styling", "equals", "styling_effort", "lufttrocknen", "0", "", "Lufttrocknen / minimal", "TRUE"),
    ("PFL-17", "styling", "equals", "styling_effort", "leichtes_styling", "1", "", "Leichtes Styling", "TRUE"),
    ("PFL-18", "styling", "equals", "styling_effort", "regelmaessiges_styling", "2", "", "Regelmäßiges Styling", "TRUE"),
    ("PFL-19", "styling", "equals", "styling_effort", "aufwendiges_styling", "3", "", "Aufwendiges Styling", "TRUE"),
    ("PFL-20", "zeit", "equals", "time_commitment", "sehr_wenig", "0", "", "Zeit-Commitment sehr wenig", "TRUE"),
    ("PFL-21", "zeit", "equals", "time_commitment", "mittel", "1", "", "Zeit-Commitment mittel", "TRUE"),
    ("PFL-22", "zeit", "equals", "time_commitment", "bewusst_regelmaessig", "2", "", "Zeit-Commitment bewusst & regelmäßig", "TRUE"),
]

# Neue Regel PFL-23 — Phase 2 deklarativ
NEW_ROW = (
    "PFL-23", "ziele", "array_count_except", "care_goals", "gesunde_kopfhaut",
    "1", "2", "Bis zu 2 Punkte für nicht-kopfhaut-Pflegeziele (Migration #10, 2026-06-24)", "TRUE",
)


def build_grid():
    grid = [HEADER]
    for row in EXISTING_ROWS:
        grid.append(list(row))
    grid.append(list(NEW_ROW))
    return grid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true", help="Schreibe ins Sheet. Ohne diesen Flag: dry-run.")
    args = ap.parse_args()

    grid = build_grid()
    print(f"Plan: {len(grid)-1} Zeilen + Header in Tab '{TAB}' (vorher: 22 Zeilen / 8 Spalten, nachher: 23 / 9)")
    print(f"Header: {grid[0]}")
    print(f"\nNeue Regel:")
    print(f"  R{len(grid)}: {grid[-1]}")
    print(f"\nStichprobe bestehende Regel mit leerer max_punkte-Spalte:")
    print(f"  R02: {grid[1]}")

    if not args.commit:
        print("\n(dry-run — nichts geschrieben. Mit --commit ausfuehren.)")
        return 0

    base = Path.cwd()
    env = load_env(base / ".env")
    sa = resolve_sa_path(env, base)
    creds = Credentials.from_service_account_file(str(sa), scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(DOC_ID)
    ws = sh.worksheet(TAB)

    ws.clear()
    end_col = chr(ord("A") + len(HEADER) - 1)
    ws.update(f"A1:{end_col}{len(grid)}", grid, value_input_option="RAW")

    rows_after = [r for r in ws.get_all_values() if any(c.strip() for c in r)]
    print(f"\nWrote {len(grid)} rows ({len(HEADER)} cols). Sheet has {len(rows_after)} non-empty rows.")
    if len(rows_after) != len(grid):
        print("WARN: row-count mismatch", file=sys.stderr)
        return 1
    for i, (planned, actual) in enumerate(zip(grid, rows_after), start=1):
        if planned != actual:
            print(f"DIFF R{i}: planned={planned}\n        actual ={actual}", file=sys.stderr)
            return 1
    print("Re-Read: all rows verbatim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
