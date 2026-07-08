#!/usr/bin/env python3
"""
clone_workflow_wl.py — Klont den aktiven MONAT-Workflow zu einem neuen
Workflow-Objekt `MyBeautyKey Whitelabel Beratungssystem v1.0`.

Ziel: physisch getrenntes zweites Workflow-Objekt in n8n. Der MONAT-
Workflow wird nur gelesen (GET), nie modifiziert — die 0/36-Drift-
Baseline ist damit strukturell abgesichert. Der Klon startet inaktiv
mit eigenem Webhook-Path (`mybeautykey-wl-haaranalyse`) und neu
generierter webhookId.

Idempotent: wenn der Klon (Name-Match) schon existiert, bricht das
Skript ab und meldet die vorhandene ID — mit `--force` wird der alte
Klon gelöscht und neu erstellt.

Aufruf:
    python3 clone_workflow_wl.py             # deployt (POST)
    python3 clone_workflow_wl.py --dry-run   # nur Preview
    python3 clone_workflow_wl.py --force     # ersetzt vorhandenen Klon
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
import uuid
from datetime import datetime
from pathlib import Path

from sheets_writer import load_env

SOURCE_WORKFLOW_ID = "pwSWA5NatKiLhueB"
CLONE_NAME = "MyBeautyKey Whitelabel Beratungssystem v1.0"
CLONE_WEBHOOK_PATH = "mybeautykey-wl-haaranalyse"
WEBHOOK_NODE_NAME = "Webhook"
BACKUP_DIR = Path(__file__).parent / "backups"


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


def list_workflows(base_url: str, api_key: str) -> list[dict]:
    """Alle Workflows der n8n-Instanz (paginiert falls nötig)."""
    result: list[dict] = []
    cursor: str | None = None
    while True:
        path = "/workflows?limit=100"
        if cursor:
            path += f"&cursor={cursor}"
        page = api_call(base_url, path, api_key)
        result.extend(page.get("data", []))
        cursor = page.get("nextCursor")
        if not cursor:
            break
    return result


def find_existing_clone(base_url: str, api_key: str) -> dict | None:
    for wf in list_workflows(base_url, api_key):
        if wf.get("name") == CLONE_NAME:
            return wf
    return None


def rewire_webhook_for_clone(wf: dict) -> None:
    """
    Webhook-Node bekommt neuen Path und neue webhookId. Beides muss
    global-eindeutig sein, sonst kollidiert der Klon beim Aktivieren
    mit dem laufenden MONAT-Workflow.
    """
    webhook = find_node(wf, WEBHOOK_NODE_NAME)
    if webhook is None:
        raise SystemExit(f"FEHLER: Webhook-Node '{WEBHOOK_NODE_NAME}' im Source-Workflow nicht gefunden.")
    params = webhook.setdefault("parameters", {})
    params["path"] = CLONE_WEBHOOK_PATH
    # webhookId ist ein separates Top-Level-Feld auf Webhook-Nodes
    webhook["webhookId"] = str(uuid.uuid4())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true",
                        help="Kein POST — schreibt nur Preview-Datei mit dem Klon-Body.")
    parser.add_argument("--force", action="store_true",
                        help="Vorhandenen Klon (Name-Match) löschen und neu erstellen.")
    parser.add_argument("--activate", action="store_true",
                        help="Klon nach POST aktivieren (idempotent — wenn schon aktiv, Skip).")
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

    print(f"[1/6] GET Source-Workflow {SOURCE_WORKFLOW_ID} …")
    src = api_call(base_url, f"/workflows/{SOURCE_WORKFLOW_ID}", api_key)
    src_name = src.get("name")
    src_node_count = len(src.get("nodes", []))
    print(f"      Name: {src_name!r}, Nodes: {src_node_count}")

    src_backup = BACKUP_DIR / f"workflow_source_snapshot_{ts}.json"
    src_backup.write_text(json.dumps(src, indent=2, ensure_ascii=False))
    print(f"[2/6] Source-Snapshot → {src_backup.relative_to(repo_dir)}")

    print(f"[3/6] Prüfe ob Klon '{CLONE_NAME}' schon existiert …")
    existing = find_existing_clone(base_url, api_key)
    skip_post = False
    if existing is not None:
        existing_id = existing.get("id")
        if args.force:
            if args.dry_run:
                print(f"      DRY-RUN: würde DELETE Klon {existing_id} vor Neu-Anlage.")
            else:
                print(f"      --force: DELETE alten Klon {existing_id} …")
                api_call(base_url, f"/workflows/{existing_id}", api_key, method="DELETE")
        elif args.activate:
            print(f"      Klon existiert bereits (ID {existing_id}). POST überspringen — springe zu Aktivierung.")
            skip_post = True
            clone_id_existing = existing_id
        else:
            print(f"      Klon existiert bereits (ID {existing_id}). Abbruch ohne --force / --activate.")
            print(f"      Aufruf mit --force ersetzt den vorhandenen Klon, --activate aktiviert ihn.")
            return 1
    else:
        print("      Kein Klon vorhanden — Neu-Anlage.")

    if not skip_post:
        print("[4/6] Klon-Body vorbereiten (Name, Webhook-Path, webhookId, strip_readonly) …")
        clone = json.loads(json.dumps(src))  # tiefe Kopie
        clone["name"] = CLONE_NAME
        rewire_webhook_for_clone(clone)
        strip_readonly(clone)

        webhook_after = find_node(clone, WEBHOOK_NODE_NAME)
        print(f"      Webhook-Path im Klon: {webhook_after['parameters']['path']!r}")
        print(f"      Neue webhookId:       {webhook_after['webhookId']}")

        clone_path = BACKUP_DIR / f"workflow_wl_clone_{ts}.json"
        clone_path.write_text(json.dumps(clone, indent=2, ensure_ascii=False))
        print(f"      Klon-Body → {clone_path.relative_to(repo_dir)}")

        if args.dry_run:
            if args.activate:
                print("[5/6] --dry-run: kein POST, keine Aktivierung.")
            else:
                print("[5/6] --dry-run: kein POST.")
            print("[6/6] Fertig (dry-run).")
            return 0

        print("[5/6] POST /workflows …")
        try:
            created = api_call(base_url, "/workflows", api_key, method="POST", body=clone)
        except urllib.error.HTTPError as e:
            print(f"      ✗ HTTP {e.code} {e.reason}")
            print(e.read().decode("utf-8", errors="replace"))
            return 1
        clone_id = created.get("id")
        print(f"      ✓ POST erfolgreich. Klon-ID: {clone_id}")
    else:
        print("[4/6] Klon-Body-Vorbereitung übersprungen (Klon existiert).")
        clone_id = clone_id_existing
        print(f"[5/6] POST übersprungen — nutze bestehenden Klon {clone_id}.")

    print("[6/6] Verifikation (GET /workflows/{id}) …")
    verify = api_call(base_url, f"/workflows/{clone_id}", api_key)
    verify_webhook = find_node(verify, WEBHOOK_NODE_NAME)
    ok = (
        verify.get("name") == CLONE_NAME
        and verify_webhook is not None
        and verify_webhook.get("parameters", {}).get("path") == CLONE_WEBHOOK_PATH
        and len(verify.get("nodes", [])) == src_node_count
    )
    print(f"      Name:       {verify.get('name')!r}")
    print(f"      Path:       {verify_webhook.get('parameters', {}).get('path')!r}")
    print(f"      Node-Count: {len(verify.get('nodes', []))} (Source: {src_node_count})")
    print(f"      Aktiv:      {verify.get('active')}")
    print(f"      Verifikation: {'✓ ok' if ok else '✗ Diskrepanz'}")

    if args.activate:
        if verify.get("active"):
            print("      Aktivierung übersprungen — Klon ist schon aktiv.")
        else:
            print(f"      Aktiviere Klon {clone_id} …")
            try:
                api_call(base_url, f"/workflows/{clone_id}/activate", api_key, method="POST")
                verify_after = api_call(base_url, f"/workflows/{clone_id}", api_key)
                if verify_after.get("active"):
                    print(f"      ✓ Klon aktiv.")
                else:
                    print(f"      ✗ Aktivierung lief durch, aber active=False im Verify.")
                    ok = False
            except urllib.error.HTTPError as e:
                print(f"      ✗ Aktivierung HTTP {e.code} {e.reason}")
                print(e.read().decode("utf-8", errors="replace"))
                ok = False

    print()
    print(f"Webhook-URL für Tests:")
    print(f"  {base_url.rstrip('/')}/webhook/{CLONE_WEBHOOK_PATH}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
