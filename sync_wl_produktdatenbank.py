#!/usr/bin/env python3
"""
sync_wl_produktdatenbank.py — Ersetzt die embedded produktdatenbank im
Whitelabel-Klon durch den Adapter-Output aus wl_adapter.py.

Zweck: erster Regressions-Beweis für die WL-Bibliothek als Datenquelle.
Der Klon hat aktuell die byte-identische MONAT-produktdatenbank embedded
(aus Migration #27 sync_rules_to_workflow.py übernommen beim POST-Klon).
Dieses Skript

  1) extrahiert die 37 embedded Zeilen aus Klon-Node "08 Ausschluss-Filter",
  2) jagt jede Zeile durch den Adapter (Reverse → Forward),
  3) überschreibt drei Felder mit dem Original: `produktlinie` (workflow-
     relevant, aber hardcodiert 'eigen' im Adapter), `kombinationen` /
     `kombi_optional` (workflow-tot, aber saubere Payload-Symmetrie).
     Seit Sub-Slot-Ausroll 2026-07-08 wird `slot_typ` vom Adapter direkt
     korrekt erzeugt — kein Passthrough mehr nötig.
  4) schreibt die 37 Adapter-Zeilen zwischen die SYNC-Marker zurück,
  5) PUT + GET-Verifikation.

Damit wird bewiesen: das Chip-Vokabular des Adapters trägt die 21 aktiv
genutzten produktdatenbank-Spalten verlustfrei durch die Regel-Engine.

Nur der WL-Klon wird angefasst — MONAT bleibt physisch unberührt.

Aufruf:
    python3 sync_wl_produktdatenbank.py             # PUT
    python3 sync_wl_produktdatenbank.py --dry-run   # nur Preview
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env
from wl_adapter import (
    DB_COLUMNS,
    LibraryEntry,
    from_produktdatenbank_row,
    to_produktdatenbank_row,
)

CLONE_WORKFLOW_ID = "5lPLG0y235XiIpN1"
TARGET_NODE = "08 Ausschluss-Filter"
SYNC_TAB = "produktdatenbank"
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_wl_sync"

# Felder, die aus der Original-Zeile durchgereicht werden (nicht durch den
# Adapter transformiert). Begründung siehe Skript-Docstring.
PASSTHROUGH_FIELDS = ("produktlinie", "kombinationen", "kombi_optional")


def api_call(base_url: str, path: str, api_key: str, method: str = "GET", body=None):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    data = None
    headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_readonly(wf: dict) -> None:
    for k in (
        "id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags",
        "shared", "active", "meta", "isArchived", "homeProject", "scopes",
        "pinData", "activeVersion", "activeVersionId", "sourceWorkflowId",
        "nodeGroups", "versionCounter", "description", "staticData",
    ):
        wf.pop(k, None)
    allowed = {
        "executionOrder", "saveExecutionProgress", "saveManualExecutions",
        "saveDataErrorExecution", "saveDataSuccessExecution", "errorWorkflow",
        "timezone", "executionTimeout",
    }
    if isinstance(wf.get("settings"), dict):
        wf["settings"] = {k: v for k, v in wf["settings"].items() if k in allowed}


def find_node(wf: dict, name: str) -> dict:
    for n in wf.get("nodes", []):
        if n.get("name") == name:
            return n
    raise RuntimeError(f"Node '{name}' nicht im Workflow gefunden.")


def extract_embedded_rows(js_code: str, tab: str) -> list[dict]:
    """Liest das JSON-Array zwischen den SYNC-Markern.

    Bei emit_style='stmt' steht `const X = [ ... ];` — wir suchen das Array-
    Literal robust per Klammer-Balance.
    """
    marker_re = re.compile(
        rf"// >>> SYNC:{re.escape(tab)}\b.*?// <<< SYNC:{re.escape(tab)}",
        re.DOTALL,
    )
    m = marker_re.search(js_code)
    if not m:
        raise RuntimeError(f"SYNC-Marker für '{tab}' nicht gefunden.")
    region = m.group(0)
    # Erstes '[' bis passendes schließendes ']' (Klammer-Balance).
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
    payload = region[start:end + 1]
    rows = json.loads(payload)
    if not isinstance(rows, list):
        raise RuntimeError(f"Sync-Region '{tab}': Array-Payload erwartet, {type(rows).__name__} gefunden.")
    return rows


def round_trip_row(original: dict) -> tuple[dict, list[str]]:
    """Adapter Reverse → Forward mit Passthrough-Override der Design-Felder."""
    entry, warnings = from_produktdatenbank_row(original)
    row_number = int(original.get("row_number", 0) or 0)
    produktlinie = original.get("produktlinie", "eigen") or "eigen"
    forwarded = to_produktdatenbank_row(entry, row_number=row_number, produktlinie=produktlinie)
    # Passthrough-Overrides für Design-Verluste (siehe Docstring).
    for field in PASSTHROUGH_FIELDS:
        if field in original:
            forwarded[field] = original[field]
    # Spalten-Reihenfolge stabil halten (JSON.stringify ist ordered in n8n jsCode-Kontext).
    ordered = {c: forwarded.get(c, "") for c in DB_COLUMNS}
    return ordered, warnings


def library_entry_to_row(entry_dict: dict, index: int) -> dict:
    """
    File-Modus: rehydriert ein LibraryEntry aus JSON-Dict und rendert es
    per Forward-Adapter in eine 25-Spalten-DB-Zeile.

    Kein Passthrough: alle Werte kommen aus LibraryEntry-Feldern. `produktlinie`
    ist als LibraryEntry-Feld gepflegt (workflow-relevant). `kombinationen` /
    `kombi_optional` sind nicht Teil des Modells und bleiben leer (workflow-tot).
    """
    entry = LibraryEntry(**entry_dict)
    forwarded = to_produktdatenbank_row(entry, row_number=index + 1)
    return {c: forwarded.get(c, "") for c in DB_COLUMNS}


def build_sync_region(rows: list[dict]) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    header = (
        f"// >>> SYNC:{SYNC_TAB} — synced {ts} — {len(rows)} rows — "
        f"source: wl_adapter.py round-trip — do not edit between markers"
    )
    footer = f"// <<< SYNC:{SYNC_TAB}"
    return f"{header}\nconst allProducts = {payload};\n{footer}"


def patch_js_code(js_code: str, new_rows: list[dict]) -> str:
    marker_re = re.compile(
        rf"// >>> SYNC:{re.escape(SYNC_TAB)}\b.*?// <<< SYNC:{re.escape(SYNC_TAB)}",
        re.DOTALL,
    )
    new_region = build_sync_region(new_rows)
    new_code, n = marker_re.subn(new_region, js_code)
    if n != 1:
        raise RuntimeError(f"SYNC-Marker für '{SYNC_TAB}' {n}× gefunden (erwartet: 1).")
    return new_code


def report_column_diff(original: list[dict], patched: list[dict]) -> None:
    """Aggregierter Report über Spalten, in denen sich etwas verändert hat."""
    # row_number ist embedded ein Sheet-Zeilenindex, wird von keinem Node
    # gelesen (per grep 2026-07-08 verifiziert), damit workflow-tot.
    workflow_relevant = {
        "produkt_key", "produktname_de", "produktlinie", "produkttyp",
        "slot_typ", "routine_schritt", "kopfhaut", "haarstruktur",
        "haarstaerke", "haarzustand", "hauptfunktion", "nebenfunktionen",
        "pflegelevel", "ausschluss_bei", "ist_hitzeschutz", "ist_bonding",
        "ist_scalp_focus", "locken_geeignet", "aktiv", "anwendung",
        "intensitaet",
    }
    # kombinationen/kombi_optional/row_number/produkt_url = design/tot → separat gruppieren
    by_col: dict[str, list[str]] = {}
    for o, p in zip(original, patched):
        key = o.get("produkt_key", "?")
        for c in DB_COLUMNS:
            if str(o.get(c, "")) != str(p.get(c, "")):
                by_col.setdefault(c, []).append(key)
    if not by_col:
        print("      Keine Adapter-Δ — Round-Trip byte-identisch (unerwartet, weil hauptfunktion-Ordering variieren kann).")
        return
    for c in sorted(by_col.keys()):
        keys = by_col[c]
        marker = "  [workflow-relevant]" if c in workflow_relevant else "  [design/tot]"
        print(f"      Δ {c:20} {len(keys):>3} rows {marker} — z.B. {keys[:3]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Kein PUT, nur Preview.")
    parser.add_argument("--source", type=Path, default=None,
                        help=(
                            "Optional: JSON-Fixture mit LibraryEntry-Objekten "
                            "(z.B. wl_libraries/sina_monat.json). Ohne Flag: "
                            "Round-Trip aus embedded Klon-Zeilen (Default)."
                        ))
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[1/6] GET WL-Klon {CLONE_WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{CLONE_WORKFLOW_ID}", api_key)

    backup_path = BACKUP_DIR / f"workflow_clone_backup_{ts}_pre_adapter_sync.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/6] Backup → {backup_path.relative_to(repo_dir)}")

    print(f"[3/6] Embedded produktdatenbank aus Node '{TARGET_NODE}' extrahieren …")
    node = find_node(wf, TARGET_NODE)
    js_code = node.get("parameters", {}).get("jsCode", "")
    original_rows = extract_embedded_rows(js_code, SYNC_TAB)
    print(f"      {len(original_rows)} rows extrahiert (Baseline für Δ-Report).")

    if args.source is not None:
        src_path = args.source.resolve()
        try:
            src_display = src_path.relative_to(repo_dir)
        except ValueError:
            src_display = src_path
        print(f"[4/6] File-Modus: Forward-only aus {src_display} …")
        payload = json.loads(src_path.read_text())
        entries = payload.get("entries", payload if isinstance(payload, list) else [])
        if not entries:
            print(f"FEHLER: keine 'entries' in {args.source} gefunden.", file=sys.stderr)
            return 1
        patched_rows: list[dict] = []
        for i, entry_dict in enumerate(entries):
            patched_rows.append(library_entry_to_row(entry_dict, i))
        print(f"      {len(patched_rows)} rows aus {len(entries)} LibraryEntry-Objekten gerendert.")
    else:
        print("[4/6] Round-Trip-Modus (embedded → Reverse → Forward) …")
        patched_rows = []
        warning_total = 0
        for row in original_rows:
            new_row, warns = round_trip_row(row)
            patched_rows.append(new_row)
            warning_total += len(warns)
        print(f"      {len(patched_rows)} rows verarbeitet, {warning_total} Adapter-Warnungen aggregiert.")

    print(f"[4/6] Spalten-Δ-Report (Baseline vs. Adapter-Output):")
    report_column_diff(original_rows, patched_rows)

    print(f"[5/6] Node-jsCode patchen …")
    new_code = patch_js_code(js_code, patched_rows)
    node["parameters"]["jsCode"] = new_code

    strip_readonly(wf)

    if args.dry_run:
        preview_path = BACKUP_DIR / f"workflow_wl_adapter_dryrun_{ts}.json"
        preview_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[6/6] --dry-run: kein PUT. Preview → {preview_path.relative_to(repo_dir)}")
        return 0

    out_path = BACKUP_DIR / f"workflow_wl_adapter_synced_{ts}.json"
    out_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out_path.relative_to(repo_dir)}")

    print(f"[6/6] PUT WL-Klon {CLONE_WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{CLONE_WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    # Verifikation
    wf_after = api_call(base_url, f"/workflows/{CLONE_WORKFLOW_ID}", api_key)
    node_after = find_node(wf_after, TARGET_NODE)
    rows_after = extract_embedded_rows(node_after["parameters"]["jsCode"], SYNC_TAB)
    ok = len(rows_after) == len(patched_rows)
    print(f"      Verifikation: {len(rows_after)} rows im Live-Workflow ({'✓ ok' if ok else '✗ Diskrepanz'})")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
