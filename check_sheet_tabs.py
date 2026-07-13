#!/usr/bin/env python3
"""Kurzer Check ob 'beraterinnen'-Tab schon im Sheet existiert."""
import warnings
warnings.filterwarnings("ignore")
import sys
from pathlib import Path
sys.stderr = open("/dev/null", "w")
from sheets_writer import load_env, resolve_sa_path, open_sheet
sys.stderr = sys.__stderr__

env = load_env(Path(__file__).parent / ".env")
sa = resolve_sa_path(env, Path(__file__).parent)
sheet = open_sheet(sa)
print(f"OK: Sheet-Titel = {sheet.title}", flush=True)
existing = sorted(ws.title for ws in sheet.worksheets())
print(f"Aktuelle Tabs ({len(existing)}):", flush=True)
for t in existing:
    print(f"  - {t}", flush=True)
print(f"\nberaterinnen existiert? {'JA' if 'beraterinnen' in existing else 'NEIN'}", flush=True)
