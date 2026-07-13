#!/usr/bin/env python3
"""
Legt neuen Sheet-Tab 'beraterinnen' im MONAT_Produktdatenbank_KOMPLETT an.

Vorbereitung für Node-17-Refactor: Partner-Info kommt aus Sheet-Loader,
nicht mehr aus statischem jsCode-Objekt. Wenn Postgres-DB fertig ist,
wird nur der Loader-Typ umgestellt (Sheet → HTTP), Node 17 unverändert.

Idempotent: bricht ab, wenn Tab schon existiert.

Desiree-Werte 1:1 aus dem aktuellen Node-17-Hardcode übernommen (workflow_live_now.json Z. 43-51).
"""
import warnings
warnings.filterwarnings("ignore")
import sys
from pathlib import Path
sys.stderr = open("/dev/null", "w")
from sheets_writer import load_env, resolve_sa_path, open_sheet
sys.stderr = sys.__stderr__

TAB = "beraterinnen"

HEADER = [
    "partner_id",
    "name",
    "first_name",
    "email",
    "phone",
    "whatsapp",
    "photo_url",
    "title",
    "brand_partner_of",
    "aktiv",
]

ROWS = [
    # 1:1 aus Node 17 jsCode extrahiert (partners['desiree'])
    [
        "desiree",
        "Desirée Fiebig",
        "Desirée",
        "beratung@veradex.de",
        "0175 / 3742698",
        "491753742698",
        "https://myglowmatch.de/partners/desiree.jpg",
        "Deine MONAT Markenpartnerin",
        "MONAT",
        "TRUE",
    ],
]


def main():
    env = load_env(Path(__file__).parent / ".env")
    sa = resolve_sa_path(env, Path(__file__).parent)
    sheet = open_sheet(sa)

    existing = [ws.title for ws in sheet.worksheets()]
    if TAB in existing:
        print(f"ABORT: Tab '{TAB}' existiert bereits — idempotent kein Re-Create.", flush=True)
        print("Wenn du echte Neuanlage willst: Tab manuell im Google Sheet löschen.", flush=True)
        sys.exit(1)

    # Neu anlegen
    n_rows = len(ROWS) + 1  # +1 für Header
    n_cols = len(HEADER)
    ws = sheet.add_worksheet(title=TAB, rows=n_rows + 5, cols=n_cols)
    print(f"OK: Tab '{TAB}' angelegt ({n_rows} Zeilen × {n_cols} Spalten).", flush=True)

    # Header + Daten in einem Rutsch
    all_values = [HEADER] + ROWS
    ws.update("A1", all_values)
    print(f"OK: {len(all_values)} Zeilen geschrieben (Header + {len(ROWS)} Beraterin).", flush=True)

    # Verifikation via Re-Read
    read_back = ws.get_all_values()
    print(f"\n=== Verifikation ({len(read_back)} Zeilen aus Sheet gelesen) ===", flush=True)
    for i, row in enumerate(read_back):
        print(f"  L{i+1}: {row}", flush=True)


if __name__ == "__main__":
    main()
