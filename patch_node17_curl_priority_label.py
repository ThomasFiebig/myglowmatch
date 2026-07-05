#!/usr/bin/env python3
"""
Micro-Patch: Node 17 readable() key-aware für curl_priority-Label-Kollision.

Problem: Die `readable(key, value)`-Funktion hat den `key`-Parameter, nutzt
ihn aber nicht — alle Lookups gehen gegen die globale Map. Der Wert `glatt`
kommt in zwei Feldern vor:
  - hair_structure=glatt  → Label „glatt" (Frage 2, questions.ts)
  - curl_priority=glatt   → Label „lieber glatt tragen" (Frage 2b)
Die Map kennt nur den einen `glatt → glatt`-Eintrag. Ergebnis in der
Beraterin-Mail: „Locken-Wunsch: glatt" statt „lieber glatt tragen".

Fix: Zwei kleine Änderungen — jeweils Anchor-basierte, eindeutige Ersetzung.
  A) `readable()`-Body um `perKey`-Overlay erweitern; bei Kontext-Match
     vor der globalen Map-Auflösung greifen.
  B) Aufrufstelle L367 (Locken-Wunsch-Row) übergibt Key 'curl_priority'
     statt Leerstring. Alle anderen 12 `readable('', …)`-Aufrufe bleiben
     unverändert — keine Kollisionen erkannt.

Kollisions-Guard: updatedAt-Re-Check vor dem PUT (paralleler Tab).
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
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_sync"
NODE_NAME = "17 Claude E-Mail formulieren"

# Edit A: readable()-Body um perKey-Overlay erweitern.
ANCHOR_A_OLD = (
    "function readable(key, value) {\n"
    "  const map = {"
)
ANCHOR_A_NEW = (
    "function readable(key, value) {\n"
    "  const perKey = {\n"
    "    curl_priority: {\n"
    "      'glatt': 'lieber glatt tragen',\n"
    "    },\n"
    "  };\n"
    "  const map = {"
)

# Edit B: Return-Zeile bekommt perKey-Vorrang.
ANCHOR_B_OLD = (
    "    'bewusst_regelmaessig': 'bewusst & regelmäßig'\n"
    "  };\n"
    "  return map[value] || value;"
)
ANCHOR_B_NEW = (
    "    'bewusst_regelmaessig': 'bewusst & regelmäßig'\n"
    "  };\n"
    "  if (perKey[key] && perKey[key][value] !== undefined) return perKey[key][value];\n"
    "  return map[value] || value;"
)

# Edit C: Aufrufstelle L367.
ANCHOR_C_OLD = (
    "if (rawInput.curl_priority) antwortenTabelleHTML += answerRow('Locken-Wunsch', "
    "readable('', rawInput.curl_priority), false);"
)
ANCHOR_C_NEW = (
    "if (rawInput.curl_priority) antwortenTabelleHTML += answerRow('Locken-Wunsch', "
    "readable('curl_priority', rawInput.curl_priority), false);"
)

EDITS = [
    ("readable() perKey-Overlay hinzufügen", ANCHOR_A_OLD, ANCHOR_A_NEW),
    ("readable() perKey vor Map-Return prüfen", ANCHOR_B_OLD, ANCHOR_B_NEW),
    ("Aufruf für curl_priority key-aware", ANCHOR_C_OLD, ANCHOR_C_NEW),
]


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
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_node17_curlkey.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/6] Backup → {backup_path.name}")

    print(f"[3/6] Patch Node '{NODE_NAME}' — 3 Anchor-Ersetzungen …")
    target = None
    for n in wf["nodes"]:
        if n.get("name") == NODE_NAME:
            target = n
            break
    if target is None:
        print(f"FEHLER: Node '{NODE_NAME}' nicht gefunden.", file=sys.stderr)
        return 1

    js = target["parameters"].get("jsCode", "")

    # Idempotenz-Check: wenn perKey schon drin ist, brechen wir ab.
    if "perKey" in js:
        print("      → readable() enthält bereits perKey — nichts zu tun. Abbruch.")
        return 0

    for label, old, new in EDITS:
        hits = js.count(old)
        if hits != 1:
            print(f"FEHLER: Anchor '{label}' {hits}× gefunden (erwartet 1).",
                  file=sys.stderr)
            return 1
        js = js.replace(old, new, 1)
        print(f"      ✓ {label}")

    target["parameters"]["jsCode"] = js

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
    put_body_path = BACKUP_DIR / f"workflow_node17_curlkey_{ts}.json"
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
            checks = [
                ("perKey-Overlay im Body", "curl_priority: {\n      'glatt': 'lieber glatt tragen'," in after_js),
                ("perKey-Vorrang im Return", "if (perKey[key] && perKey[key][value] !== undefined)" in after_js),
                ("Aufrufstelle key-aware", "readable('curl_priority', rawInput.curl_priority)" in after_js),
            ]
            ok = all(v for _, v in checks)
            for label, val in checks:
                mark = "✓" if val else "✗"
                print(f"      {mark} {label}")
            return 0 if ok else 1
    return 1


if __name__ == "__main__":
    sys.exit(main())
