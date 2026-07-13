#!/usr/bin/env python3
"""
Fügt googleSheets-Loader-Node '16z Partner-Info laden' in den Live-Workflow ein.

Verkabelung: Predecessor(Node 17) → 16z → Node 17
So kann Node 17 die Partner-Info aus dem beraterinnen-Sheet-Tab lesen,
statt statisch im jsCode zu hardcoden.

Idempotent: bricht ab, wenn 16z schon existiert.

Nächster Schritt nach diesem Patch: patch_node17_partner_loader.py
(refactort Node-17-jsCode, sodass es aus $node["16z ..."] liest).
"""
import argparse
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

NEW_NODE_NAME = "16z Partner-Info laden"
TARGET_NODE_NAME = "17 Claude E-Mail formulieren"

SHEET_DOC_ID = "1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A"
SHEET_DOC_CACHED_NAME = "MONAT_Produktdatenbank_KOMPLETT"
SHEET_DOC_CACHED_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_DOC_ID}/edit?usp=drivesdk"
SHEET_CREDENTIAL_ID = "zf5b37nhm7NZArlz"
SHEET_CREDENTIAL_NAME = "Google Sheets OAuth2 API"


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


def find_predecessor(conns, target):
    """Findet den Node, dessen main[0]-Verbindung auf target zeigt."""
    for src, spec in conns.items():
        for idx, targets in enumerate(spec.get("main", [])):
            if targets is None:
                continue
            for t in targets:
                if t.get("node") == target:
                    return src
    return None


def find_max_position_x(nodes):
    """Grob den x-Offset für den neuen Node bestimmen (Mitte zwischen pred und target)."""
    return max((n.get("position", [0, 0])[0] for n in nodes), default=0)


def build_loader_node(pred_position, target_position):
    """Baut einen googleSheets-Node analog zu bestehenden Loadern.

    Position: zwischen pred und target, leicht nach oben versetzt.
    """
    x = (pred_position[0] + target_position[0]) // 2
    y = min(pred_position[1], target_position[1]) - 100
    return {
        "parameters": {
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
        },
        "name": NEW_NODE_NAME,
        "type": "n8n-nodes-base.googleSheets",
        "typeVersion": 4,
        "position": [x, y],
        "credentials": {
            "googleSheetsOAuth2Api": {
                "id": SHEET_CREDENTIAL_ID,
                "name": SHEET_CREDENTIAL_NAME,
            }
        },
        "retryOnFail": True,
        "maxTries": 3,
        "waitBetweenTries": 5000,
    }


def rewire(conns, pred_name, loader_name, target_name):
    """Ersetzt Pred→Target durch Pred→Loader→Target.

    Ändert in-place: conns[pred] Kante, die auf target zeigte, zeigt jetzt auf loader.
    Fügt conns[loader] mit einer main[0]-Kante zu target hinzu.
    """
    spec = conns.get(pred_name, {})
    changed = False
    for idx, targets in enumerate(spec.get("main", [])):
        if targets is None:
            continue
        for t in targets:
            if t.get("node") == target_name:
                t["node"] = loader_name
                changed = True
    if not changed:
        raise RuntimeError(f"Kante {pred_name}→{target_name} nicht gefunden.")

    conns[loader_name] = {
        "main": [[{"node": target_name, "type": "main", "index": 0}]]
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/6] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_add_beraterinnen_loader.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/6] Backup → {backup_path.relative_to(repo_dir)}")

    node_names = {n["name"] for n in wf["nodes"]}
    if NEW_NODE_NAME in node_names:
        print(f"      ABORT: Node '{NEW_NODE_NAME}' existiert bereits — idempotent.", file=sys.stderr)
        return 1
    if TARGET_NODE_NAME not in node_names:
        print(f"      FEHLER: Zielnode '{TARGET_NODE_NAME}' nicht im Workflow.", file=sys.stderr)
        return 1

    conns = wf["connections"]

    pred_name = find_predecessor(conns, TARGET_NODE_NAME)
    if pred_name is None:
        print(f"      FEHLER: Kein Predecessor von '{TARGET_NODE_NAME}' gefunden.", file=sys.stderr)
        return 1
    print(f"[3/6] Predecessor identifiziert: '{pred_name}' → '{TARGET_NODE_NAME}'")

    # Positions für den neuen Loader
    pred_node = next(n for n in wf["nodes"] if n["name"] == pred_name)
    target_node = next(n for n in wf["nodes"] if n["name"] == TARGET_NODE_NAME)
    loader = build_loader_node(pred_node["position"], target_node["position"])
    wf["nodes"].append(loader)
    print(f"[4/6] Loader-Node hinzugefügt: '{NEW_NODE_NAME}' bei {loader['position']}")

    rewire(conns, pred_name, NEW_NODE_NAME, TARGET_NODE_NAME)
    print(f"[5/6] Verkabelung: '{pred_name}' → '{NEW_NODE_NAME}' → '{TARGET_NODE_NAME}'")

    if args.dry_run:
        strip_readonly(wf)
        preview = BACKUP_DIR / f"workflow_add_loader_dryrun_{ts}.json"
        preview.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[6/6] --dry-run: kein PUT. Preview → {preview.relative_to(repo_dir)}")
        return 0

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_add_loader_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out.relative_to(repo_dir)}")

    print(f"[6/6] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    # Verify
    print("      Verifikation …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    if NEW_NODE_NAME not in {n["name"] for n in wf_after["nodes"]}:
        print(f"      ✗ '{NEW_NODE_NAME}' nicht im Live-Workflow gefunden.", file=sys.stderr)
        return 1
    conns_after = wf_after["connections"]
    # Prüfe Loader→Target
    loader_targets = conns_after.get(NEW_NODE_NAME, {}).get("main", [[]])[0]
    if not any(t.get("node") == TARGET_NODE_NAME for t in loader_targets):
        print(f"      ✗ '{NEW_NODE_NAME}' zeigt nicht auf '{TARGET_NODE_NAME}'.", file=sys.stderr)
        return 1
    print(f"      ✓ Live-Workflow verifiziert: {NEW_NODE_NAME} → {TARGET_NODE_NAME}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
