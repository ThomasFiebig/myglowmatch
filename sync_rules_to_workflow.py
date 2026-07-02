#!/usr/bin/env python3
"""
Sync-Skript: Google Sheets → n8n-Workflow (embedded JSON).

POC für map_conflict_rules → Node 14 (siehe HANDOVER „Skalierungs-Roadmap").

Idee:
  Statt die Sheets zur Laufzeit im Workflow zu lesen (Rate-Limit-Bottleneck bei
  Bursts), wird der Sheet-Inhalt beim Sheet-Edit einmalig in den Node-jsCode
  einkompiliert. Live-Workflow liest die Konstante aus jsCode, kein Sheets-Call.

Ablauf:
  1) Sheet lesen (via sheets_writer.open_sheet)
  2) Workflow via n8n-API GET
  3) Zieldaten in Node-jsCode zwischen SYNC-Markern ersetzen
     - Erster Sync ersetzt die ursprüngliche `$items(...)`-Zeile durch Marker-Region.
     - Folgende Syncs ersetzen nur den Inhalt zwischen den Markern.
  4) Backup speichern
  5) PUT + GET-Verifikation

CLI:
  python3 sync_rules_to_workflow.py           # Sync aller SYNCS-Einträge
  python3 sync_rules_to_workflow.py --dry-run # nur Preview, kein PUT
"""

import argparse
import json
import re
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env, resolve_sa_path, open_sheet


WORKFLOW_ID = "pwSWA5NatKiLhueB"
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_sync"

# Sheet → Node.
# emit_style:
#   "stmt" → ersetzt komplette Deklaration `const {var} = $items(…).map(…);` durch
#            `const {var} = [...];` (Node 14).
#   "expr" → ersetzt nur den `$items(…).map(…)`-Sub-Ausdruck durch `[...]`. Bleibt
#            in Ausdrucks-Kette (z.B. `.filter(aktiv==TRUE)` danach).
SYNCS = [
    {
        "tab": "map_conflict_rules",
        "node": "14 Konflikte auflösen",
        "var": "rules",
        "emit_style": "stmt",
        # Regex für den ersten Sync — muss exakt einmal im jsCode matchen.
        "init_pattern": r'const rules = \$items\("13 Konfliktregeln laden"\)\.map\(item => item\.json\);',
    },
    {
        "tab": "map_priorities",
        "node": "04 Prioritäten auflösen",
        "var": "priorityRules",
        "emit_style": "expr",
        # Matcht mehrzeilig: `$items("04a Prioritäten laden")\n  .map(it => it.json)`
        "init_pattern": r'\$items\("04a Prioritäten laden"\)\s*\n\s*\.map\(it => it\.json\)',
    },
    {
        "tab": "map_slot_rules",
        "node": "11 REQ-Regeln auswerten",
        "var": "ruleItems",
        "emit_style": "expr",
        # `$items("10 map_slot_rules")` steht als einzeilige Zuweisung → nur den Aufruf ersetzen.
        "init_pattern": r'\$items\("10 map_slot_rules"\)',
        # Node 11 hat `.map(it => it.json)` in einer SEPARATEN Deklaration nach ruleItems.
        # Nach Sync enthält ruleItems Plain-Dicts → .map(it => it.json) muss weg.
        # Wird nur beim init einmalig angewandt; Folgesyncs berühren das nicht mehr.
        "post_init_replace": [
            (r"\s*\.map\(it => it\.json\)", ""),
        ],
    },
    {
        "tab": "map_pflegelevel_overrides",
        "node": "06 Pflegelevel berechnen",
        "var": "overrideRules",
        "emit_style": "expr",
        # Muster wie Node 04: `$items(…)\n.map(it => it.json)`. `.filter(aktiv==TRUE)` bleibt.
        "init_pattern": r'\$items\("06b Pflegelevel-Overrides laden"\)\s*\n\s*\.map\(it => it\.json\)',
    },
    {
        "tab": "map_max_products",
        "node": "06 Pflegelevel berechnen",
        "var": "maxRules",
        "emit_style": "expr",
        "init_pattern": r'\$items\("06c Max-Products laden"\)\s*\n\s*\.map\(it => it\.json\)',
    },
    {
        "tab": "map_pool_filter",
        "node": "08 Ausschluss-Filter",
        "var": "poolRules",
        "emit_style": "expr",
        # Nach der Region kommt noch `.filter(aktiv==TRUE).sort(prioritaet)` — bleibt intakt.
        "init_pattern": r'\$items\("08a Pool-Filter laden"\)\s*\n\s*\.map\(it => it\.json\)',
    },
]


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


def read_sheet_rows(sheet, tab: str) -> list[dict]:
    """Alle Zeilen als List[Dict] (header → value). Alles roh als String."""
    ws = sheet.worksheet(tab)
    values = ws.get_all_values()
    if not values:
        raise RuntimeError(f"Tab '{tab}' ist leer.")
    headers = values[0]
    rows = []
    for row in values[1:]:
        # Skip komplett leere Zeilen (gspread liefert manchmal Trailer-Rows)
        if not any(cell.strip() for cell in row):
            continue
        rows.append({h: (row[i] if i < len(row) else "") for i, h in enumerate(headers)})
    return rows


def build_marker_region(sync_cfg: dict, rows: list[dict]) -> str:
    """Erzeugt die vollständige Sync-Region inkl. Marker."""
    tab = sync_cfg["tab"]
    var = sync_cfg["var"]
    style = sync_cfg.get("emit_style", "stmt")
    ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    header = (
        f"// >>> SYNC:{tab} — synced {ts} — {len(rows)} rows — "
        f"do not edit between markers, run sync_rules_to_workflow.py"
    )
    footer = f"// <<< SYNC:{tab}"
    if style == "stmt":
        return f"{header}\nconst {var} = {payload};\n{footer}"
    if style == "expr":
        # Nur Array — bleibt in umgebender Ausdrucks-Kette (z.B. .filter(...))
        return f"{header}\n{payload}\n{footer}"
    raise RuntimeError(f"Unbekannter emit_style '{style}' für Tab '{tab}'.")


def patch_js_code(js_code: str, sync_cfg: dict, rows: list[dict]) -> tuple[str, str]:
    """Ersetzt die Sync-Region im jsCode. Gibt (neuer Code, Modus) zurück.

    Modus: 'init' bei erstem Sync, 'update' bei Folgesync.
    """
    tab = sync_cfg["tab"]
    marker_re = re.compile(
        rf"// >>> SYNC:{re.escape(tab)}\b.*?// <<< SYNC:{re.escape(tab)}",
        re.DOTALL,
    )
    new_region = build_marker_region(sync_cfg, rows)

    if marker_re.search(js_code):
        new_code, n = marker_re.subn(new_region, js_code)
        if n != 1:
            raise RuntimeError(
                f"SYNC-Marker für '{tab}' mehrfach gefunden ({n}×) — Node manuell prüfen."
            )
        return new_code, "update"

    # Erster Sync: init_pattern ersetzen
    init_re = re.compile(sync_cfg["init_pattern"])
    matches = list(init_re.finditer(js_code))
    if len(matches) != 1:
        raise RuntimeError(
            f"init_pattern für '{tab}' nicht eindeutig im Node '{sync_cfg['node']}' "
            f"gefunden ({len(matches)} Treffer). Bitte Node manuell prüfen."
        )
    new_code = init_re.sub(new_region, js_code, count=1)
    # Optionale einmalige Post-Init-Ersetzungen (nur bei init-Mode).
    # Nützlich, wenn `.map(it => it.json)` o.ä. in separater Deklaration steht und
    # nach Sync auf Plain-Dicts trifft.
    for pattern, replacement in sync_cfg.get("post_init_replace", []):
        pri_re = re.compile(pattern)
        pri_matches = list(pri_re.finditer(new_code))
        if len(pri_matches) != 1:
            raise RuntimeError(
                f"post_init_replace für '{tab}' pattern '{pattern}' nicht eindeutig "
                f"({len(pri_matches)} Treffer). Bitte Node manuell prüfen."
            )
        new_code = pri_re.sub(replacement, new_code, count=1)
    return new_code, "init"


def strip_readonly(wf: dict) -> None:
    """Top-Level- und settings-Felder entfernen, die n8n beim PUT ablehnt."""
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


def verify_embedded(js_code: str, tab: str, expected_rows: int) -> None:
    """GET-Verifikation: prüft dass die embedded Sync-Region im Live-Workflow steckt.

    Row-Count aus Marker-Header (`— N rows —`) — robust gegen emit_style-Varianten.
    """
    marker_re = re.compile(
        rf"// >>> SYNC:{re.escape(tab)}\b.*?// <<< SYNC:{re.escape(tab)}",
        re.DOTALL,
    )
    m = marker_re.search(js_code)
    if not m:
        raise RuntimeError(f"Post-PUT-Verify: SYNC-Marker für '{tab}' fehlt im Live-Workflow.")
    region = m.group(0)
    count_re = re.compile(r"— (\d+) rows —")
    cm = count_re.search(region)
    if not cm:
        raise RuntimeError(f"Post-PUT-Verify: row-Count für '{tab}' nicht aus Marker-Header lesbar.")
    live_rows = int(cm.group(1))
    if live_rows != expected_rows:
        raise RuntimeError(
            f"Post-PUT-Verify: erwartet {expected_rows} rows, gefunden {live_rows} (aus Marker-Header)."
        )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Kein PUT, nur Preview der Änderung.")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    sa_path = resolve_sa_path(env, repo_dir)
    sheet = open_sheet(sa_path)

    print(f"[1/5] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_sync.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/5] Backup → {backup_path.relative_to(repo_dir)}")

    print(f"[3/5] Sheet-Reads + Node-Patches ({len(SYNCS)} Sync-Einträge) …")
    verify_targets: list[tuple[str, str, int]] = []  # (node, tab, expected_rows)
    for cfg in SYNCS:
        tab = cfg["tab"]
        node_name = cfg["node"]

        rows = read_sheet_rows(sheet, tab)
        if not rows:
            raise RuntimeError(f"Sheet '{tab}' hat 0 Zeilen — Sync abgebrochen.")

        node = find_node(wf, node_name)
        js_code = node.get("parameters", {}).get("jsCode", "")
        if not js_code:
            raise RuntimeError(f"Node '{node_name}' hat keinen jsCode.")

        new_code, mode = patch_js_code(js_code, cfg, rows)
        node["parameters"]["jsCode"] = new_code
        print(f"      {tab} → {node_name}: {len(rows)} rows, mode={mode}")
        verify_targets.append((node_name, tab, len(rows)))

    if args.dry_run:
        preview_path = BACKUP_DIR / f"workflow_dryrun_{ts}.json"
        strip_readonly(wf)
        preview_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[4/5] --dry-run: kein PUT. Preview → {preview_path.relative_to(repo_dir)}")
        print("[5/5] Fertig (dry-run).")
        return 0

    strip_readonly(wf)
    out_path = BACKUP_DIR / f"workflow_sync_{ts}.json"
    out_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out_path.relative_to(repo_dir)}")

    print(f"[4/5] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    print("[5/5] GET-Verifikation …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    for node_name, tab, expected in verify_targets:
        node = find_node(wf_after, node_name)
        verify_embedded(node["parameters"]["jsCode"], tab, expected)
        print(f"      ✓ {tab} in '{node_name}': {expected} rows verified")

    return 0


if __name__ == "__main__":
    sys.exit(main())
