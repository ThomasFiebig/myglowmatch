#!/usr/bin/env python3
"""
Retry-Patch für alle googleSheets-Loader-Nodes (Migration #25, 2026-07-01).

Setzt auf allen googleSheets-Nodes:
  - retryOnFail = True
  - maxTries = 3
  - waitBetweenTries = 5000 (ms)

Damit werden transient Google-Sheets-Fehler (Service unavailable, Rate-Limit)
abgefangen — statt stiller Fail bei Live-Kundinnen.

Ablauf:
  1. Aktuellen Workflow via n8n-API GET
  2. Backup als workflow_backup_20260701_pre_retry.json
  3. Alle googleSheets-Nodes patchen
  4. PUT zurück an n8n-API
"""

import json
import sys
import urllib.request
import urllib.error
from pathlib import Path

BACKUP_PATH = Path(__file__).parent / "workflow_backup_20260701_pre_retry.json"
OUT_PATH = Path(__file__).parent / "workflow_retry_v1.json"
GOOGLE_SHEETS_TYPE = "n8n-nodes-base.googleSheets"


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


def api_call(base_url: str, path: str, api_key: str, method: str = "GET", body=None):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    data = None
    headers = {
        "X-N8N-API-KEY": api_key,
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    env = load_env(Path(__file__).parent / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    # Workflow-ID aus HANDOVER
    wid = "pwSWA5NatKiLhueB"
    print(f"[1/4] GET workflow {wid} …")
    wf = api_call(base_url, f"/workflows/{wid}", api_key)

    print(f"[2/4] Backup → {BACKUP_PATH.name}")
    BACKUP_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))

    # Patch alle googleSheets-Nodes
    patched = 0
    for n in wf["nodes"]:
        if n.get("type") == GOOGLE_SHEETS_TYPE:
            n["retryOnFail"] = True
            n["maxTries"] = 3
            n["waitBetweenTries"] = 5000
            patched += 1
            print(f"      patched: {n['name']}")
    print(f"[3/4] {patched} googleSheets-Nodes gepatcht")

    # Cleanup Top-Level-Felder die n8n beim PUT nicht akzeptiert
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags", "shared",
             "active", "meta", "isArchived", "homeProject", "scopes", "pinData",
             "activeVersion", "activeVersionId", "sourceWorkflowId", "nodeGroups",
             "versionCounter", "description", "staticData"):
        wf.pop(k, None)

    # settings-Cleanup: n8n akzeptiert nur bekannte settings-Keys
    allowed_settings = {"executionOrder", "saveExecutionProgress", "saveManualExecutions",
                        "saveDataErrorExecution", "saveDataSuccessExecution", "errorWorkflow",
                        "timezone", "executionTimeout"}
    if "settings" in wf and isinstance(wf["settings"], dict):
        wf["settings"] = {k: v for k, v in wf["settings"].items() if k in allowed_settings}

    OUT_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {OUT_PATH.name}")

    print(f"[4/4] PUT workflow {wid} …")
    try:
        api_call(base_url, f"/workflows/{wid}", api_key, method="PUT", body=wf)
        print("      ✓ Deploy erfolgreich.")
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP-Fehler: {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
