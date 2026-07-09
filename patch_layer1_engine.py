#!/usr/bin/env python3
"""
Engine-Patches für Layer-1 Wirkungs-Refactor (2026-07-09).

Node 11 (11 REQ-Regeln auswerten):
  - slot_override_erlaubt-Spalte in slot_assignments-Entry durchreichen
    (aktuell hat entry: slot_typ, filter, reason — wir ergänzen slot_override_erlaubt).

Node 12 (12 Scoring & Slot-Befüllung):
  - Patch #20 (Zeile 239-250) erweitern:
      Slot-Typ-Override greift bei
        (a) produkt_key-Literal-Filter (Legacy)
        ODER
        (b) explizit erlaubten Regeln (slot_override_erlaubt=TRUE)
      Match-Semantik im Override-Block: identisch zu Wirkungs-Filter unten
      (Boolean-Flag ODER Substring-Match).

Nach dem Patch: PUT + GET-Verifikation.

Aufruf:
    python3 patch_layer1_engine.py             # PUT
    python3 patch_layer1_engine.py --dry-run   # nur diff
"""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env

WORKFLOW_ID = "pwSWA5NatKiLhueB"
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
    for k in list(wf.get("settings", {}).keys()):
        if k not in ("executionOrder", "saveDataErrorExecution", "saveDataSuccessExecution",
                     "saveExecutionProgress", "saveManualExecutions", "timezone",
                     "executionTimeout", "errorWorkflow"):
            wf["settings"].pop(k, None)


def find_node(wf: dict, name: str) -> dict:
    for n in wf.get("nodes", []):
        if n.get("name") == name:
            return n
    raise RuntimeError(f"Node '{name}' nicht gefunden.")


NODE11_OLD = """  const entry = {
    slot_typ: normStr(r.slot_typ),
    filter:   normStr(r.filter),
    reason:   `${r.regel_id}: ${r.reason || ''}`.trim()
  };"""

NODE11_NEW = """  const entry = {
    slot_typ: normStr(r.slot_typ),
    filter:   normStr(r.filter),
    reason:   `${r.regel_id}: ${r.reason || ''}`.trim(),
    slot_override_erlaubt: String(r.slot_override_erlaubt || '').toUpperCase() === 'TRUE'
  };"""


NODE12_OLD = """  // PATCH 2026-06-27 (Migration #20): bei produkt_key-Literal-Filter
  // sind REQ-Regel-Slot-Typ authoritative über Stammdaten-Slot-Typ.
  // Ermöglicht REQ-16b (moxie_mousse styling_3) trotz moxie_mousse.slot_typ='styling_1'.
  if (filterStr && filterStr !== '' && !filterStr.includes('=')) {
    const filterKeys = filterStr.split('|').map(s => s.trim());
    const additionalCandidates = pool.filter(p =>
      !candidates.includes(p) && filterKeys.includes(p.produkt_key)
    );
    if (additionalCandidates.length > 0) {
      candidates = candidates.concat(additionalCandidates);
    }
  }"""

NODE12_NEW = """  // PATCH 2026-06-27 (Migration #20) + 2026-07-09 (Layer-1 Wirkungs-Refactor):
  // Slot-Typ der REQ-Regel ist authoritative über Stammdaten-Slot-Typ, wenn
  //   (a) filter ein produkt_key-Literal ist (Legacy-Verhalten), ODER
  //   (b) die REQ-Regel explizit slot_override_erlaubt=TRUE hat (Wirkungs-Filter mit expliziter Erlaubnis).
  // Match-Semantik im Override-Block identisch zum Wirkungs-Filter unten.
  const isKeyLiteral = filterStr && filterStr !== '' && !filterStr.includes('=');
  const isSlotOverride = slotDef.slot_override_erlaubt === true;
  if (isKeyLiteral || isSlotOverride) {
    const filterSegs = filterStr.split('|').map(s => s.trim()).filter(Boolean);
    const additionalCandidates = pool.filter(p => {
      if (candidates.includes(p)) return false;
      return filterSegs.some(fStr => {
        const flagMatch = fStr.match(/^([a-zA-Z_][a-zA-Z0-9_]*)=(TRUE|FALSE)$/);
        if (flagMatch) {
          return boolVal(p[flagMatch[1]]) === (flagMatch[2] === 'TRUE');
        }
        return (p.produkt_key || '').includes(fStr)
            || (p.produktlinie || '').includes(fStr)
            || (p.hauptfunktion || '').includes(fStr);
      });
    });
    if (additionalCandidates.length > 0) {
      candidates = candidates.concat(additionalCandidates);
    }
  }"""


def apply_patch(node: dict, old: str, new: str, label: str) -> None:
    js = node["parameters"]["jsCode"]
    if old not in js:
        raise RuntimeError(f"Node-Patch '{label}': altes Snippet nicht exakt gefunden. Manuelle Prüfung erforderlich.")
    if new in js:
        print(f"  ! Node-Patch '{label}': neues Snippet bereits vorhanden — skip.")
        return
    node["parameters"]["jsCode"] = js.replace(old, new, 1)
    print(f"  ✓ Node-Patch '{label}' angewendet ({len(old)} → {len(new)} chars)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo_dir = Path(__file__).parent
    env = load_env(repo_dir / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    print(f"[1/4] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_layer1_engine.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/4] Backup → {backup_path.relative_to(repo_dir)}")

    print(f"[3/4] Node-Patches …")
    n11 = find_node(wf, "11 REQ-Regeln auswerten")
    n12 = find_node(wf, "12 Scoring & Slot-Befüllung")
    apply_patch(n11, NODE11_OLD, NODE11_NEW, "Node 11 slot_override_erlaubt-Durchreichen")
    apply_patch(n12, NODE12_OLD, NODE12_NEW, "Node 12 erweiterter Patch #20")

    if args.dry_run:
        print("[4/4] Dry-run: kein PUT.")
        local = BACKUP_DIR / f"workflow_layer1_patched_{ts}.json"
        local.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"      Patched-Snapshot lokal → {local.relative_to(repo_dir)}")
        return 0

    strip_readonly(wf)
    print(f"[4/4] PUT workflow …")
    api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    print(f"      ✓ PUT erfolgreich.")
    # Kurz-Verifikation
    verified = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    v11 = find_node(verified, "11 REQ-Regeln auswerten")
    v12 = find_node(verified, "12 Scoring & Slot-Befüllung")
    ok11 = 'slot_override_erlaubt: String' in v11["parameters"]["jsCode"]
    ok12 = 'isSlotOverride' in v12["parameters"]["jsCode"]
    print(f"      Verify Node 11: {'✓' if ok11 else '✗'}, Node 12: {'✓' if ok12 else '✗'}")
    return 0 if (ok11 and ok12) else 1


if __name__ == "__main__":
    sys.exit(main())
