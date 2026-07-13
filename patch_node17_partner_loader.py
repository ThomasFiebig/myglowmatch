#!/usr/bin/env python3
"""
Refactor Node 17: statisches partners-Objekt durch Loader-basierten Lookup ersetzen.

Vorher: partners = { desiree: {...}, DEFAULT: {...} }; partner = partners[partnerId]
Nachher: partner-Info aus $items("16z Partner-Info laden") per partner_id filtern,
         DEFAULT-Fallback bleibt inline (für Sheet-Ausfall).

Voraussetzung: Node „16z Partner-Info laden" ist bereits im Workflow (siehe
patch_add_beraterinnen_loader.py + fix_beraterinnen_loader_credentials.py).

Idempotent: bricht ab wenn refactor bereits durch (marker: `PARTNER-INFO — dynamisch`).
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

OLD_BLOCK = """// ============================================================
// PARTNER-DATENBANK
// ============================================================
const partners = {
  'desiree': {
    name: 'Desirée Fiebig',
    first_name: 'Desirée',
    email: 'beratung@veradex.de',
    phone: '0175 / 3742698',
    whatsapp: '491753742698',
    photo_url: 'https://myglowmatch.de/partners/desiree.jpg',
    title: 'Deine MONAT Markenpartnerin'
  },
  'DEFAULT': {
    name: 'myglowmatch',
    first_name: 'myglowmatch',
    email: 'info@myglowmatch.de',
    phone: '',
    whatsapp: '',
    photo_url: '',
    title: 'myglowmatch Team'
  }
};

const partner = partners[partnerId] || partners['DEFAULT'];"""

NEW_BLOCK = """// ============================================================
// PARTNER-INFO — dynamisch aus Sheet-Loader (Node 16z)
// DEFAULT-Fallback bleibt inline für Ausfallsicherheit
// (Sheet-Down / unbekannte partner_id → Kundin bekommt trotzdem Mail)
// ============================================================
const DEFAULT_PARTNER = {
  name: 'myglowmatch',
  first_name: 'myglowmatch',
  email: 'info@myglowmatch.de',
  phone: '',
  whatsapp: '',
  photo_url: '',
  title: 'Deine persönliche Beauty-Beraterin',
  brand_partner_of: '',
  aktiv: 'TRUE'
};

let partner = DEFAULT_PARTNER;
try {
  const partnerRows = $items("16z Partner-Info laden") || [];
  const found = partnerRows.find(function (item) {
    return item.json && String(item.json.partner_id) === String(partnerId);
  });
  if (found && String(found.json.aktiv).toUpperCase() === 'TRUE') {
    partner = found.json;
  }
} catch (e) {
  // Loader nicht verfügbar oder Datenfehler — bleibt bei DEFAULT_PARTNER
}"""

MARKER = "PARTNER-INFO — dynamisch"


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

    print(f"[1/5] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup_path = BACKUP_DIR / f"workflow_backup_{ts}_pre_node17_partner_loader.json"
    backup_path.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      Backup → {backup_path.relative_to(repo_dir)}")

    node = next((n for n in wf["nodes"] if n["name"] == NODE_NAME), None)
    if node is None:
        print(f"FEHLER: Node '{NODE_NAME}' nicht im Workflow.", file=sys.stderr)
        return 1

    js = node["parameters"].get("jsCode", "")
    if MARKER in js:
        print(f"[2/5] Marker '{MARKER}' bereits im jsCode — idempotent, kein Re-Patch.", file=sys.stderr)
        return 0

    print(f"[2/5] Suche alten Partner-Datenbank-Block in jsCode …")
    if OLD_BLOCK not in js:
        print(f"FEHLER: OLD_BLOCK nicht wörtlich gefunden. Manuelle Prüfung nötig.", file=sys.stderr)
        # Sanity: mindestens die zwei Landmark-Zeilen
        for landmark in ["const partners = {", "const partner = partners[partnerId]"]:
            print(f"  Landmark '{landmark[:40]}...' vorhanden: {landmark in js}")
        return 1

    print(f"[3/5] Ersetze Block ({len(OLD_BLOCK)} → {len(NEW_BLOCK)} chars) …")
    new_js = js.replace(OLD_BLOCK, NEW_BLOCK)
    node["parameters"]["jsCode"] = new_js

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_node17_partner_loader_{ts}.json"
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

    print("[5/5] Verifikation …")
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    node_after = next(n for n in wf_after["nodes"] if n["name"] == NODE_NAME)
    js_after = node_after["parameters"].get("jsCode", "")
    if MARKER not in js_after:
        print(f"      ✗ Marker nicht im Live-Node-Code.", file=sys.stderr)
        return 1
    if "const partners = {" in js_after and "'desiree':" in js_after:
        print(f"      ✗ Altes partners-Objekt noch im Code.", file=sys.stderr)
        return 1
    print(f"      ✓ Node 17 refactort — Partner-Info kommt jetzt aus Loader.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
