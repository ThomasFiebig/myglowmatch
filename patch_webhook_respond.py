#!/usr/bin/env python3
"""
patch_webhook_respond.py — Fügt einen „Respond to Webhook"-Node am Ende
des n8n-Workflows an und stellt den Webhook auf `responseMode: responseNode`.

Damit liefert n8n die berechnete Empfehlung als HTTP-Response an das
Frontend zurück (final_routine + normalized + routine_count + partner_id
aus Node 15 „Routine sortieren"). DemoResultScreen im Frontend rendert
dann echte Produkte statt Fake-Fallback.

Idempotent: wenn der Respond-Node bereits existiert und der Webhook
schon auf responseNode steht, ändert das Skript nichts.

Aufruf:
    python3 patch_webhook_respond.py            # deployt
    python3 patch_webhook_respond.py --dry-run  # nur Preview
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

from sheets_writer import load_env

WORKFLOW_ID = "pwSWA5NatKiLhueB"
BACKUP_DIR = Path(__file__).parent / "backups"
RESPOND_NODE_NAME = "20 Respond to Webhook"
WEBHOOK_NODE_NAME = "Webhook"
SOURCE_NODE_NAME = "15 Routine sortieren"

# Der Response-Body wird als n8n-Expression evaluiert und zieht die
# relevanten Felder aus Node 15. Wird als String übergeben, das ={{ ... }}
# ist wichtig.
RESPONSE_BODY_EXPR = (
    "={{ ({ "
    "final_routine: $('15 Routine sortieren').item.json.final_routine, "
    "routine_count: $('15 Routine sortieren').item.json.routine_count, "
    "normalized: $('15 Routine sortieren').item.json.normalized, "
    "partner_id: $('15 Routine sortieren').item.json.partner_id, "
    "pflegelevel: $('15 Routine sortieren').item.json.pflegelevel, "
    "priorities: $('15 Routine sortieren').item.json.priorities "
    "}) }}"
)


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


def find_node(wf: dict, name: str) -> dict | None:
    for n in wf.get("nodes", []):
        if n.get("name") == name:
            return n
    return None


def find_terminal_nodes(wf: dict) -> list[str]:
    """Nodes ohne ausgehende Verbindungen — der letzte in der Chain."""
    conns = wf.get("connections", {}) or {}
    all_names = {n.get("name") for n in wf.get("nodes", []) if n.get("name")}
    sources = set(conns.keys())
    # Ein terminal Node hat keine outgoing connection.
    return sorted(all_names - sources)


def compute_respond_position(source_node: dict) -> list[float]:
    pos = source_node.get("position", [3000, 200])
    return [float(pos[0]) + 220, float(pos[1])]


def patch_webhook_response_mode(webhook_node: dict) -> bool:
    """Setzt responseMode auf responseNode. Gibt True zurück wenn geändert."""
    params = webhook_node.setdefault("parameters", {})
    if params.get("responseMode") == "responseNode":
        return False
    params["responseMode"] = "responseNode"
    return True


def build_respond_node(source_node: dict) -> dict:
    return {
        "parameters": {
            "respondWith": "json",
            "responseBody": RESPONSE_BODY_EXPR,
            "options": {},
        },
        "type": "n8n-nodes-base.respondToWebhook",
        "typeVersion": 1.1,
        "position": compute_respond_position(source_node),
        "name": RESPOND_NODE_NAME,
    }


def attach_connection(wf: dict, from_node: str, to_node: str) -> bool:
    """Fügt from_node → to_node hinzu, falls nicht schon vorhanden."""
    conns = wf.setdefault("connections", {})
    outgoing = conns.setdefault(from_node, {})
    main = outgoing.setdefault("main", [])
    if not main:
        main.append([])
    # main[0] ist die primäre Ausgabe.
    entries = main[0]
    for entry in entries:
        if entry.get("node") == to_node:
            return False
    entries.append({"node": to_node, "type": "main", "index": 0})
    return True


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

    print(f"[1/6] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_respond.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/6] Backup → {backup_path.relative_to(repo_dir)}")

    print("[3/6] Webhook-Node auf responseNode-Modus stellen …")
    webhook = find_node(wf, WEBHOOK_NODE_NAME)
    if webhook is None:
        print(f"FEHLER: Node '{WEBHOOK_NODE_NAME}' nicht gefunden.", file=sys.stderr)
        return 1
    webhook_changed = patch_webhook_response_mode(webhook)
    print(f"      Webhook responseMode: {'geändert' if webhook_changed else 'schon responseNode'}")

    print(f'[4/6] Respond-Node "{RESPOND_NODE_NAME}" prüfen/anlegen …')
    respond_existing = find_node(wf, RESPOND_NODE_NAME)
    source_node = find_node(wf, SOURCE_NODE_NAME)
    if source_node is None:
        print(f"FEHLER: Source-Node '{SOURCE_NODE_NAME}' nicht gefunden.", file=sys.stderr)
        return 1

    added_node = False
    if respond_existing is None:
        respond_node = build_respond_node(source_node)
        wf["nodes"].append(respond_node)
        added_node = True
        print(f"      Respond-Node neu angelegt (position {respond_node['position']}).")
    else:
        # Wenn schon da, Response-Body aktualisieren, damit Änderungen greifen.
        respond_existing["parameters"]["responseBody"] = RESPONSE_BODY_EXPR
        respond_existing["parameters"].setdefault("respondWith", "json")
        respond_existing["parameters"].setdefault("options", {})
        print("      Respond-Node existiert — responseBody aktualisiert.")

    print("[5/6] Connection zum Respond-Node herstellen …")
    # Der terminal Node der Chain (kein outgoing) wird angepasst und feuert
    # dann den Respond-Node. So bekommt das Frontend erst die Antwort, wenn
    # der komplette Workflow durchgelaufen ist (Mail-Send + Log).
    terminals = find_terminal_nodes(wf)
    # Der neu angelegte Respond-Node selbst wäre nach dem Anlegen ein Terminal
    # (bevor die Connection dahin gelegt ist) — den ausschließen.
    terminals = [t for t in terminals if t != RESPOND_NODE_NAME]
    if not terminals:
        print("FEHLER: kein terminal Node gefunden, um daran anzuknüpfen.", file=sys.stderr)
        return 1
    # Bevorzugte Reihenfolge: 19 Log speichern > 18b Partner-Mail senden >
    # sonst der lexikografisch spätere.
    preferred = ["19 Log speichern", "18b Partner-Mail senden"]
    chosen_source = next((p for p in preferred if p in terminals), terminals[-1])
    conn_added = attach_connection(wf, chosen_source, RESPOND_NODE_NAME)
    print(f"      {chosen_source} → {RESPOND_NODE_NAME}: {'neu' if conn_added else 'schon vorhanden'}")

    strip_readonly(wf)

    if args.dry_run:
        preview_path = BACKUP_DIR / f"workflow_respond_dryrun_{ts}.json"
        preview_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[6/6] --dry-run: kein PUT. Preview → {preview_path.relative_to(repo_dir)}")
        return 0

    out_path = BACKUP_DIR / f"workflow_respond_{ts}.json"
    out_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out_path.relative_to(repo_dir)}")

    print(f"[6/6] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    except urllib.error.HTTPError as e:
        print(f"      ✗ HTTP {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        return 1
    print("      ✓ PUT erfolgreich.")

    # Verifikation
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    webhook_after = find_node(wf_after, WEBHOOK_NODE_NAME)
    respond_after = find_node(wf_after, RESPOND_NODE_NAME)
    ok = (
        webhook_after
        and webhook_after.get("parameters", {}).get("responseMode") == "responseNode"
        and respond_after is not None
    )
    print(f"      Verifikation: {'✓ ok' if ok else '✗ Diskrepanz'}")
    if added_node:
        print("      Workflow enthält jetzt einen zusätzlichen Node.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
