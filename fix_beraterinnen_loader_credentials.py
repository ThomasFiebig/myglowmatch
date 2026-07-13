#!/usr/bin/env python3
"""
Fix: der bereits deployte Node '16z Partner-Info laden' hat falsche Credentials
(googleApi statt googleSheetsOAuth2Api) und falsche typeVersion (4.5 statt 4).

Ursache: erster Deploy-Versuch (patch_add_beraterinnen_loader.py, Vor-Fix)
schlug am API-Level fehl (HTTP 400 „Missing required credential"), aber
n8n hatte den Node bereits in die Workflow-Struktur übernommen.

Dieses Skript aktualisiert den Node in-place mit korrekten Werten aus dem
alten Reader-Template (Node 07 Backup 2026-05-27, vor Migration #27).
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
NODE_NAME = "16z Partner-Info laden"

SHEET_DOC_ID = "1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A"
SHEET_DOC_CACHED_NAME = "MONAT_Produktdatenbank_KOMPLETT"
SHEET_DOC_CACHED_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_DOC_ID}/edit?usp=drivesdk"
CREDENTIAL_ID = "zf5b37nhm7NZArlz"
CREDENTIAL_NAME = "Google Sheets OAuth2 API"


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

    print(f"[1/4] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_fix_credentials.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      Backup → {backup_path.relative_to(repo_dir)}")

    node = next((n for n in wf["nodes"] if n["name"] == NODE_NAME), None)
    if node is None:
        print(f"FEHLER: Node '{NODE_NAME}' nicht im Live-Workflow.", file=sys.stderr)
        return 1

    print(f"[2/4] Fix '{NODE_NAME}' …")
    old_creds = json.dumps(node.get("credentials"))
    old_tv = node.get("typeVersion")

    node["typeVersion"] = 4
    node["credentials"] = {
        "googleSheetsOAuth2Api": {
            "id": CREDENTIAL_ID,
            "name": CREDENTIAL_NAME,
        }
    }
    # documentId auf mode='list' mit cachedResult umbauen
    node["parameters"] = {
        "documentId": {
            "__rl": True,
            "value": SHEET_DOC_ID,
            "mode": "list",
            "cachedResultName": SHEET_DOC_CACHED_NAME,
            "cachedResultUrl": SHEET_DOC_CACHED_URL,
        },
        "sheetName": {
            "__rl": True,
            "value": "beraterinnen",
            "mode": "name",
        },
        "options": {},
    }
    print(f"      typeVersion: {old_tv} → {node['typeVersion']}")
    print(f"      credentials: {old_creds}")
    print(f"                 → {json.dumps(node['credentials'])}")

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_fix_credentials_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out.relative_to(repo_dir)}")

    print(f"[3/4] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    print("[4/4] Verifikation …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    node_after = next(n for n in wf_after["nodes"] if n["name"] == NODE_NAME)
    creds_key = list(node_after.get("credentials", {}).keys())
    if creds_key != ["googleSheetsOAuth2Api"]:
        print(f"      ✗ Credentials-Key falsch: {creds_key}", file=sys.stderr)
        return 1
    if node_after.get("typeVersion") != 4:
        print(f"      ✗ typeVersion falsch: {node_after.get('typeVersion')}", file=sys.stderr)
        return 1
    print(f"      ✓ Node '{NODE_NAME}' korrekt konfiguriert.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
