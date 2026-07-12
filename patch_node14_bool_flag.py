#!/usr/bin/env python3
"""
Node 14 Engine-Erweiterung:
  - neuer match_typ='bool_flag' (prüft prod[match_wert]==='TRUE')
  - optionaler slot_scope-Parameter (falls Regel gesetzt: prod.slot_typ === slot_scope)

Backward-compatible: bestehende Regeln (produkt_key/produktlinie/key_contains)
laufen unverändert; slot_scope undefined = kein Filter.

Ablauf:
  1) GET Workflow
  2) Backup
  3) productMatches-Funktion + Aufruf ersetzen (idempotent-safe via Signatur-Check)
  4) PUT + Verifikation
"""
import argparse
import json
import re
import sys
import urllib.request
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env
from sync_rules_to_workflow import (
    WORKFLOW_ID, BACKUP_DIR, api_call, strip_readonly, find_node,
)


OLD_FN = """function productMatches(prod, matchTyp, matchWert) {
  if (!matchTyp || !matchWert) return false;
  const werte = String(matchWert).split(',').map(s => s.trim());
  switch (matchTyp) {
    case 'produkt_key':  return werte.includes(prod.produkt_key);
    case 'produktlinie': return werte.includes(prod.produktlinie);
    case 'key_contains': return werte.some(w => prod.produkt_key?.includes(w));
    default: return false;
  }
}"""

NEW_FN = """function productMatches(prod, matchTyp, matchWert, slotScope) {
  if (!matchTyp || !matchWert) return false;
  if (slotScope && prod.slot_typ !== slotScope) return false;
  const werte = String(matchWert).split(',').map(s => s.trim());
  switch (matchTyp) {
    case 'produkt_key':  return werte.includes(prod.produkt_key);
    case 'produktlinie': return werte.includes(prod.produktlinie);
    case 'key_contains': return werte.some(w => prod.produkt_key?.includes(w));
    case 'bool_flag':    return werte.some(w => String(prod[w]).toUpperCase() === 'TRUE');
    default: return false;
  }
}"""

OLD_CALL = "productMatches(prod, rule.match_typ, rule.match_wert)"
NEW_CALL = "productMatches(prod, rule.match_typ, rule.match_wert, rule.slot_scope)"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(__file__).parent
    env = load_env(repo / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/4] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"workflow_backup_{ts}_pre_node14_bool_flag.json"
    backup.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"[2/4] Backup → {backup.relative_to(repo)}")

    node = find_node(wf, "14 Konflikte auflösen")
    code = node["parameters"]["jsCode"]

    # Idempotenz: schon gepatched?
    if "case 'bool_flag'" in code and "slotScope" in code:
        print("      = bereits gepatched (bool_flag + slotScope vorhanden). Kein Change.")
        return 0

    if OLD_FN not in code:
        print("      ✗ Alte productMatches-Signatur nicht gefunden. Manuell prüfen.", file=sys.stderr)
        return 1
    if OLD_CALL not in code:
        print("      ✗ Alter Aufruf productMatches(prod, rule.match_typ, rule.match_wert) nicht gefunden.", file=sys.stderr)
        return 1

    new_code = code.replace(OLD_FN, NEW_FN).replace(OLD_CALL, NEW_CALL)
    node["parameters"]["jsCode"] = new_code
    print(f"[3/4] Patch angewandt (Funktion + 1 Aufruf).")

    if args.dry_run:
        prev = BACKUP_DIR / f"workflow_dryrun_{ts}_node14_bool_flag.json"
        strip_readonly(wf)
        prev.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"      --dry-run → {prev.relative_to(repo)}")
        return 0

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_node14_bool_flag_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"      lokal → {out.relative_to(repo)}")

    print(f"[4/4] PUT + Verify …")
    api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    code_after = find_node(wf_after, "14 Konflikte auflösen")["parameters"]["jsCode"]
    assert "case 'bool_flag'" in code_after, "bool_flag-Case fehlt im Live-Workflow"
    assert "slotScope" in code_after, "slotScope fehlt im Live-Workflow"
    print("      ✓ Live-Workflow enthält bool_flag + slotScope")
    return 0


if __name__ == "__main__":
    sys.exit(main())
