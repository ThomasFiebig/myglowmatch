#!/usr/bin/env python3
"""
Micro-Patch: Node 17 readable-Map um `keine_probleme` ergänzen.

Marcel-Case (2026-07-02): Sinas Ehemann bekam in der Beraterin-Mail
'keine_probleme' als Rohwert unter „Haarzustand", weil die Map in
Node 17 die Frontend-Option (Frage 4, hair_condition, exclusiveOption)
nicht abdeckt. `readable(_, value)` fällt auf `map[value] || value`
zurück.

Audit `src/data/questions.ts` gegen Live-Map: nur `keine_probleme`
fehlt aus den ~43 Enum-Werten. Ein Grenzfall bleibt bekannt und wird
NICHT hier gefixt: `curl_priority=glatt` kollidiert mit `hair_structure
=glatt` (readable() nutzt `key` nicht). Backlog.

Ablauf: GET Workflow → updatedAt vor PUT re-verifyen (Kollisions-Guard
für parallele Tabs) → Marker-freie einmalige String-Ersetzung im
`readable()`-Map-Block → PUT → GET-Verify (`keine_probleme` in Live).

Backup: backups/workflow_sync/workflow_backup_YYYYMMDD_HHMMSS_pre_node17_readable.json
"""

import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env

WORKFLOW_ID = "pwSWA5NatKiLhueB"
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_sync"

NODE_NAME = "17 Claude E-Mail formulieren"

# Die neue Zeile wird direkt hinter 'kraftlos' → 'kraftlos / wenig Volumen'
# eingefügt (bewahrt Reihenfolge Frage-4-Optionen aus questions.ts).
INSERT_ANCHOR = "    'kraftlos': 'kraftlos / wenig Volumen',\n    'duenn': 'dünner werdendes Haar',"
INSERT_REPLACEMENT = (
    "    'kraftlos': 'kraftlos / wenig Volumen',\n"
    "    'duenn': 'dünner werdendes Haar',\n"
    "    'keine_probleme': 'keine besonderen Probleme',"
)


def api_call(base_url, path, api_key, method="GET", body=None):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    data = None
    headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def strip_readonly(wf):
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


def main():
    env = load_env(Path(__file__).parent / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/6] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    initial_updated_at = wf.get("updatedAt")
    print(f"      updatedAt (Start-Snapshot): {initial_updated_at}")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_node17_readable.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/6] Backup → {backup_path}")

    print(f"[3/6] Patch Node '{NODE_NAME}' …")
    target = None
    for n in wf["nodes"]:
        if n.get("name") == NODE_NAME:
            target = n
            break
    if target is None:
        print(f"FEHLER: Node '{NODE_NAME}' nicht gefunden.", file=sys.stderr)
        return 1

    js = target["parameters"].get("jsCode", "")
    if "'keine_probleme'" in js:
        print("      → Map enthält bereits 'keine_probleme' — nichts zu tun. Abbruch.")
        return 0

    hits = js.count(INSERT_ANCHOR)
    if hits != 1:
        print(f"FEHLER: Insert-Anchor {hits}× gefunden (erwartet 1). "
              f"Vermutlich hat sich die Map seit Ausrichten des Skripts geändert.",
              file=sys.stderr)
        return 1

    new_js = js.replace(INSERT_ANCHOR, INSERT_REPLACEMENT, 1)
    target["parameters"]["jsCode"] = new_js
    print(f"      → +1 Map-Zeile ('keine_probleme': 'keine besonderen Probleme')")

    print(f"[4/6] Kollisions-Guard: updatedAt re-check …")
    wf_recheck = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    if wf_recheck.get("updatedAt") != initial_updated_at:
        print(f"FEHLER: Live-updatedAt hat sich seit GET geändert "
              f"({initial_updated_at} → {wf_recheck.get('updatedAt')}). "
              f"Paralleler Tab hat deployed — Abbruch, kein PUT.",
              file=sys.stderr)
        return 1
    print(f"      ✓ unverändert.")

    strip_readonly(wf)
    put_body_path = BACKUP_DIR / f"workflow_node17_readable_{ts}.json"
    put_body_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale PUT-Body-Kopie → {put_body_path.name}")

    print(f"[5/6] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    print("[6/6] GET-Verifikation …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    for n in wf_after["nodes"]:
        if n.get("name") == NODE_NAME:
            after_js = n["parameters"].get("jsCode", "")
            if "'keine_probleme': 'keine besonderen Probleme'" in after_js:
                print("      ✓ 'keine_probleme' im Live-Node 17 gefunden.")
                return 0
            print("      ✗ Post-PUT-Verify FAIL: 'keine_probleme' nicht im Live-Node.",
                  file=sys.stderr)
            return 1
    print(f"      ✗ Node '{NODE_NAME}' im Live-Workflow nicht mehr gefunden.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
