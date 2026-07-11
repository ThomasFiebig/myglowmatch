#!/usr/bin/env python3
"""
Engine-Präzisierung Node 12 (2026-07-09 v2).

Ersetzt naive .includes()-Substring-Semantik im Wirkungs-Filter-Block
durch exakten Token-Match:
  - produkt_key / produktlinie: exakte Gleichheit
  - hauptfunktion / nebenfunktionen: exakter CSV-Token-Match via csvToArr()

Boolean-Flag-Syntax (ist_hitzeschutz=TRUE) bleibt unverändert.
Der Migration-#20-Substring-Block (Zeilen 240-251) bleibt ebenfalls unverändert —
das ist der Slot-Override-Pfad und arbeitet mit produkt_key-Literals.

Vorbedingung: REQ-08.filter='rejuveniqe_oel' (nicht 'rejuveniqe'),
REQ-03.aktiv=FALSE. Beide via Sheet-Fix vor diesem Patch gesetzt.

Aufruf:
    python3 patch_engine_filter_precision.py             # PUT
    python3 patch_engine_filter_precision.py --dry-run   # nur diff
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env

WORKFLOW_ID = "pwSWA5NatKiLhueB"
BACKUP_DIR = Path(__file__).parent / "backups"


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
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags",
              "shared", "active", "meta", "isArchived", "homeProject", "scopes",
              "pinData", "activeVersion", "activeVersionId", "sourceWorkflowId",
              "nodeGroups", "versionCounter", "description", "staticData"):
        wf.pop(k, None)
    for k in list(wf.get("settings", {}).keys()):
        if k not in ("executionOrder", "saveDataErrorExecution", "saveDataSuccessExecution",
                     "saveExecutionProgress", "saveManualExecutions", "timezone",
                     "executionTimeout", "errorWorkflow"):
            wf["settings"].pop(k, None)


def find_node(wf, name):
    for n in wf.get("nodes", []):
        if n.get("name") == name:
            return n
    raise RuntimeError(f"Node '{name}' nicht gefunden.")


# Wirkungs-Filter-Block (Zeilen 253-269 im Live-Workflow)
OLD_BLOCK = """  if (filterStr && filterStr !== '') {
    const filters = filterStr.split('|');
    const filtered = candidates.filter(prod =>
      filters.some(fStr => {
        const flagMatch = fStr.match(/^([a-zA-Z_][a-zA-Z0-9_]*)=(TRUE|FALSE)$/);
        if (flagMatch) {
          const field = flagMatch[1];
          const expected = flagMatch[2] === 'TRUE';
          return boolVal(prod[field]) === expected;
        }
        return prod.produkt_key?.includes(fStr)
            || prod.produktlinie?.includes(fStr)
            || prod.hauptfunktion?.includes(fStr);
      })
    );
    if (filtered.length > 0) candidates = filtered;
  }"""

NEW_BLOCK = """  if (filterStr && filterStr !== '') {
    const filters = filterStr.split('|').map(s => s.trim()).filter(Boolean);
    const filtered = candidates.filter(prod => {
      const hfSet = new Set(csvToArr(prod.hauptfunktion));
      const nfSet = new Set(csvToArr(prod.nebenfunktionen));
      return filters.some(fStr => {
        const flagMatch = fStr.match(/^([a-zA-Z_][a-zA-Z0-9_]*)=(TRUE|FALSE)$/);
        if (flagMatch) {
          const field = flagMatch[1];
          const expected = flagMatch[2] === 'TRUE';
          return boolVal(prod[field]) === expected;
        }
        // PATCH 2026-07-09 v2: exakter Token-Match statt Substring
        // (Vorherige .includes()-Semantik lud unbeabsichtigte Kandidaten in Wirkungs-Filtern)
        return prod.produkt_key === fStr
            || prod.produktlinie === fStr
            || hfSet.has(fStr)
            || nfSet.has(fStr);
      });
    });
    if (filtered.length > 0) candidates = filtered;
  }"""


def main():
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

    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_engine_precision.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/4] Backup → {backup_path.relative_to(repo_dir)}")

    print(f"[3/4] Node-Patch Node 12 Filter-Auswertung …")
    n12 = find_node(wf, "12 Scoring & Slot-Befüllung")
    js = n12["parameters"]["jsCode"]
    if OLD_BLOCK not in js:
        print("FEHLER: altes Block-Snippet nicht exakt gefunden. Live-Workflow prüfen.", file=sys.stderr)
        return 1
    if NEW_BLOCK in js:
        print("  ! Patch bereits angewendet — skip.")
        return 0
    n12["parameters"]["jsCode"] = js.replace(OLD_BLOCK, NEW_BLOCK, 1)
    print(f"  ✓ Block ersetzt ({len(OLD_BLOCK)} → {len(NEW_BLOCK)} chars)")

    if args.dry_run:
        local = BACKUP_DIR / f"workflow_engine_precision_patched_{ts}.json"
        local.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"[4/4] Dry-run: Patched-Snapshot → {local.relative_to(repo_dir)}")
        return 0

    strip_readonly(wf)
    print(f"[4/4] PUT workflow …")
    api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    print(f"      ✓ PUT erfolgreich.")

    verified = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    v12 = find_node(verified, "12 Scoring & Slot-Befüllung")
    ok = "hfSet.has(fStr)" in v12["parameters"]["jsCode"] and "produkt_key === fStr" in v12["parameters"]["jsCode"]
    print(f"      Verify Node 12: {'✓' if ok else '✗'}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
