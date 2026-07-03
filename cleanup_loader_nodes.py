#!/usr/bin/env python3
"""
Loader-Cleanup nach Migration #27 (Sync 10/10).

Entfernt die 10 googleSheets-Read-Nodes aus dem Live-Workflow und verbindet
die zurückbleibende Chain direkt. Voraussetzung: alle 10 Sheets sind bereits
in Consumer-Node-jsCode einkompiliert (via sync_rules_to_workflow.py). Node 19
(Log-Write) bleibt als einziger Sheets-Call.

Chain vor Cleanup (aus workflow_sync_20260703_222027.json ermittelt):
  02 → 04a → 04 → 05a → 05 → 06a → 06b → 06c → 06d → 06 → 07 → 08a → 08
     → 09 → 10 → 11 → 13 → 14 → 12 → 15 → …

Chain nach Cleanup:
  02 → 04 → 05 → 06 → 08 → 09 → 11 → 14 → 12 → 15 → …

Ablauf: pred→loader→succ wird zu pred→succ; conns[loader] weg; loader aus nodes.
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
BACKUP_DIR = Path(__file__).parent / "backups" / "workflow_sync"

LOADERS = [
    "04a Prioritäten laden",
    "05a map_derived_variables laden",
    "06a Pflegelevel-Scoring laden",
    "06b Pflegelevel-Overrides laden",
    "06c Max-Products laden",
    "06d Profil-Funktion-Mapping laden",
    "07 Produktdatenbank laden",
    "08a Pool-Filter laden",
    "10 map_slot_rules",
    "13 Konfliktregeln laden",
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


def remove_loader(conns, loader):
    """Verkabelt pred direkt zu succ; entfernt conns[loader]. In-place.

    Return: (pred_name, succ_name) für Logging.
    """
    # Successor(s) von loader
    loader_out = conns.get(loader, {}).get("main", [])
    if not loader_out or not loader_out[0]:
        raise RuntimeError(f"Loader '{loader}' hat keinen Successor — Chain unerwartet.")
    if len(loader_out) > 1 or len(loader_out[0]) > 1:
        raise RuntimeError(f"Loader '{loader}' hat multiple Successors — unerwartet.")
    succ_ref = loader_out[0][0]  # {node, type, index}

    # Predecessor(s): alle Kanten, die auf loader zeigen, auf succ umlenken
    changes = []
    for src, spec in conns.items():
        for idx, targets in enumerate(spec.get("main", [])):
            if targets is None:
                continue
            for t in targets:
                if t.get("node") == loader:
                    t["node"] = succ_ref["node"]
                    t["type"] = succ_ref.get("type", "main")
                    t["index"] = succ_ref.get("index", 0)
                    changes.append(src)

    if not changes:
        raise RuntimeError(f"Loader '{loader}' hatte keine Predecessor-Kanten.")
    if len(changes) > 1:
        raise RuntimeError(f"Loader '{loader}' hatte {len(changes)} Predecessor-Kanten — unerwartet.")

    # conns[loader] entfernen
    del conns[loader]
    return changes[0], succ_ref["node"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/5] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_loader_cleanup.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/5] Backup → {backup_path.relative_to(repo_dir)}")

    conns = wf["connections"]

    # Sanity: alle Loader müssen präsent sein
    present_nodes = {n["name"] for n in wf["nodes"]}
    missing = [l for l in LOADERS if l not in present_nodes]
    if missing:
        print(f"FEHLER: Loader nicht im Workflow: {missing}", file=sys.stderr)
        return 1

    # Sanity: prüfe dass keiner der Consumer-Nodes noch $items("loader …") verwendet
    # (rein defensive Prüfung — Sync sollte diese Aufrufe alle ersetzt haben)
    for n in wf["nodes"]:
        js = n.get("parameters", {}).get("jsCode", "")
        for loader in LOADERS:
            if f'$items("{loader}")' in js:
                print(f"FEHLER: Node '{n['name']}' ruft noch $items(\"{loader}\") auf — Sync ist nicht abgeschlossen.",
                      file=sys.stderr)
                return 1

    print(f"[3/5] Loader-Cleanup ({len(LOADERS)} Nodes) …")
    for loader in LOADERS:
        pred, succ = remove_loader(conns, loader)
        print(f"      – {loader}: {pred} → {succ}")

    # Node-Liste kürzen
    before = len(wf["nodes"])
    wf["nodes"] = [n for n in wf["nodes"] if n["name"] not in LOADERS]
    after = len(wf["nodes"])
    print(f"      nodes: {before} → {after} (–{before - after})")

    if args.dry_run:
        strip_readonly(wf)
        preview = BACKUP_DIR / f"workflow_cleanup_dryrun_{ts}.json"
        preview.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[4/5] --dry-run: kein PUT. Preview → {preview.relative_to(repo_dir)}")
        print("[5/5] Fertig (dry-run).")
        return 0

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_cleanup_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {out.relative_to(repo_dir)}")

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
    after_names = {n["name"] for n in wf_after["nodes"]}
    still_present = [l for l in LOADERS if l in after_names]
    if still_present:
        print(f"      ✗ Live-Workflow enthält noch Loader: {still_present}", file=sys.stderr)
        return 1
    print(f"      ✓ Alle 10 Loader entfernt. Live-Workflow-Nodes: {len(wf_after['nodes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
