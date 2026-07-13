#!/usr/bin/env python3
"""
Fix: Node 17 muss data explizit aus Node 15 lesen, nicht aus $input.

Verkabelung nach patch_add_beraterinnen_loader.py:
  Node 15 → 16z Partner-Info laden → Node 17

Damit ist $input.item.json in Node 17 = Node 16z's Sheet-Row (partner-Info),
nicht mehr Node 15's { normalized, priorities, final_routine, ... }.

Fix: `const data = $input.item.json;` → `const data = $node["15 Routine sortieren"].json;`

Regression sichtbar in execution 1352: to_email leer, first_name = 'du' (Fallback).
"""
import json
import sys
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env

WORKFLOW_ID = "pwSWA5NatKiLhueB"
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_multitenant"
NODE_NAME = "17 Claude E-Mail formulieren"

OLD = "const data = $input.item.json;"
NEW = 'const data = $node["15 Routine sortieren"].json;'


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
    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/4] GET workflow …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_fix_node17_datasource.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      Backup → {backup_path.relative_to(repo_dir)}")

    node = next((n for n in wf["nodes"] if n["name"] == NODE_NAME), None)
    if node is None:
        print(f"FEHLER: Node '{NODE_NAME}' nicht gefunden.", file=sys.stderr)
        return 1

    js = node["parameters"].get("jsCode", "")
    if NEW in js:
        print("[2/4] Marker bereits vorhanden — idempotent, kein Re-Patch.")
        return 0
    if OLD not in js:
        print(f"FEHLER: OLD '{OLD}' nicht im jsCode gefunden.", file=sys.stderr)
        return 1

    print(f"[2/4] Ersetze data-Zugriff …")
    print(f"      alt: {OLD}")
    print(f"      neu: {NEW}")
    node["parameters"]["jsCode"] = js.replace(OLD, NEW, 1)

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_fix_node17_datasource_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out.relative_to(repo_dir)}")

    print(f"[3/4] PUT …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code}: {e.read().decode('utf-8', errors='replace')}")
        return 1
    print("      ✓")

    print("[4/4] Verify …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    node_after = next(n for n in wf_after["nodes"] if n["name"] == NODE_NAME)
    if NEW not in node_after["parameters"].get("jsCode", ""):
        print("      ✗ Fix nicht im Live-Node.", file=sys.stderr)
        return 1
    print("      ✓ Live: data kommt jetzt aus Node 15.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
