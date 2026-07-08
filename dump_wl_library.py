#!/usr/bin/env python3
"""
dump_wl_library.py — Extrahiert die embedded produktdatenbank aus dem
Whitelabel-Klon und persistiert sie als LibraryEntry-JSON-Fixture.

Zweck: die Bibliothek als eigenständige Datenquelle für sync_wl_produktdatenbank.py
verfügbar machen. Bis heute war der Sync selbstreferenziell (embedded → Round-Trip
→ embedded); ab jetzt kann er auch aus einer JSON-Datei speisen. Damit ist der
Weg frei für zwei künftige WL-Bibliotheken (Sina-real, Fantasie-Demo).

Ablauf:
  1) GET WL-Klon
  2) Embedded JSON-Array zwischen SYNC-Markern in Node "08 Ausschluss-Filter"
     extrahieren
  3) Jede Zeile durch `from_produktdatenbank_row` reversen → LibraryEntry
  4) Alle Entries als List[Dict] persistieren (dataclasses.asdict)

Aufruf:
    python3 dump_wl_library.py                                # → wl_libraries/sina_monat.json
    python3 dump_wl_library.py --out wl_libraries/andere.json # anderer Zielpfad
"""

from __future__ import annotations

import argparse
import dataclasses
import json
import re
import sys
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env
from wl_adapter import from_produktdatenbank_row

CLONE_WORKFLOW_ID = "5lPLG0y235XiIpN1"
TARGET_NODE = "08 Ausschluss-Filter"
SYNC_TAB = "produktdatenbank"
DEFAULT_OUT = Path(__file__).parent / "wl_libraries" / "sina_monat.json"


def api_call(base_url: str, path: str, api_key: str):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
    req = urllib.request.Request(url, headers=headers, method="GET")
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def extract_embedded_rows(js_code: str, tab: str) -> list[dict]:
    """Analog zu sync_wl_produktdatenbank.py: JSON-Array zwischen Markern."""
    marker_re = re.compile(
        rf"// >>> SYNC:{re.escape(tab)}\b.*?// <<< SYNC:{re.escape(tab)}",
        re.DOTALL,
    )
    m = marker_re.search(js_code)
    if not m:
        raise RuntimeError(f"SYNC-Marker für '{tab}' nicht gefunden.")
    region = m.group(0)
    start = region.index("[")
    depth = 0
    end = -1
    in_str = False
    esc = False
    for i in range(start, len(region)):
        ch = region[i]
        if esc:
            esc = False
            continue
        if ch == "\\":
            esc = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                end = i
                break
    if end < 0:
        raise RuntimeError(f"Konnte JSON-Array in Sync-Region '{tab}' nicht abschließen.")
    return json.loads(region[start:end + 1])


def find_node(wf: dict, name: str) -> dict:
    for n in wf.get("nodes", []):
        if n.get("name") == name:
            return n
    raise RuntimeError(f"Node '{name}' nicht im Workflow gefunden.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT,
                        help=f"Ziel-Pfad für JSON-Fixture (Default: {DEFAULT_OUT}).")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    print(f"[1/4] GET WL-Klon {CLONE_WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{CLONE_WORKFLOW_ID}", api_key)
    node = find_node(wf, TARGET_NODE)
    js_code = node.get("parameters", {}).get("jsCode", "")

    print(f"[2/4] Embedded produktdatenbank extrahieren …")
    rows = extract_embedded_rows(js_code, SYNC_TAB)
    print(f"      {len(rows)} rows aus Klon-Node '{TARGET_NODE}' gelesen.")

    print("[3/4] Reverse durch wl_adapter.py …")
    entries: list[dict] = []
    all_warnings: list[tuple[str, str]] = []
    for row in rows:
        entry, warns = from_produktdatenbank_row(row)
        entries.append(dataclasses.asdict(entry))
        for w in warns:
            all_warnings.append((row.get("produkt_key", "?"), w))
    print(f"      {len(entries)} LibraryEntry-Objekte erzeugt.")
    if all_warnings:
        # Gruppieren nach Warnungs-Text
        by_msg: dict[str, list[str]] = {}
        for key, msg in all_warnings:
            by_msg.setdefault(msg, []).append(key)
        print(f"      Reverse-Warnungen ({len(all_warnings)} gesamt, {len(by_msg)} eindeutig):")
        for msg, keys in sorted(by_msg.items()):
            print(f"        • {msg}  ({len(keys)}× — z.B. {keys[:3]})")

    print(f"[4/4] Schreibe Fixture nach {args.out.relative_to(repo_dir)} …")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "meta": {
            "source": f"WL-Klon {CLONE_WORKFLOW_ID}, Node '{TARGET_NODE}'",
            "count": len(entries),
            "adapter_version": "12-Feld/11-Slot (2026-07-08)",
        },
        "entries": entries,
    }
    args.out.write_text(json.dumps(payload, indent=2, ensure_ascii=False))
    print(f"      ✓ {len(entries)} entries persistiert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
