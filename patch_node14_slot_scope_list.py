#!/usr/bin/env python3
"""
Node 14 slot_scope-Liste unterstützen.

Backward-compatible: single value 'styling_1' verhält sich wie bisher,
kommagetrennte Liste 'shampoo,spuelung,styling_1' matcht wenn slot_typ in Liste.

Voraussetzung: patch_node14_bool_flag.py wurde bereits deployed.
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from sheets_writer import load_env
from sync_rules_to_workflow import WORKFLOW_ID, BACKUP_DIR, api_call, strip_readonly, find_node


OLD_LINE = "if (slotScope && prod.slot_typ !== slotScope) return false;"
NEW_BLOCK = (
    "if (slotScope) {\n"
    "    const _slots = String(slotScope).split(',').map(s => s.trim()).filter(Boolean);\n"
    "    if (_slots.length && !_slots.includes(prod.slot_typ)) return false;\n"
    "  }"
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(__file__).parent
    env = load_env(repo / ".env")
    api_key = env["N8N_API_KEY"]
    base_url = env["N8N_BASE_URL"]

    print(f"[1/3] GET workflow …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    backup = BACKUP_DIR / f"workflow_backup_{ts}_pre_slot_scope_list.json"
    backup.write_text(json.dumps(wf, indent=2, ensure_ascii=False))

    node = find_node(wf, "14 Konflikte auflösen")
    code = node["parameters"]["jsCode"]

    if "_slots.includes(prod.slot_typ)" in code:
        print("      = bereits gepatched. Kein Change.")
        return 0

    if OLD_LINE not in code:
        print("      ✗ Erwartete Zeile nicht gefunden — patch_node14_bool_flag.py vorher deployen?", file=sys.stderr)
        return 1

    node["parameters"]["jsCode"] = code.replace(OLD_LINE, NEW_BLOCK)
    print(f"[2/3] Patch angewandt (slot_scope-Liste).")

    if args.dry_run:
        prev = BACKUP_DIR / f"workflow_dryrun_{ts}_slot_scope_list.json"
        strip_readonly(wf)
        prev.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
        print(f"      --dry-run → {prev.relative_to(repo)}")
        return 0

    strip_readonly(wf)
    out = BACKUP_DIR / f"workflow_slot_scope_list_{ts}.json"
    out.write_text(json.dumps(wf, indent=2, ensure_ascii=False))

    print(f"[3/3] PUT + Verify …")
    api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf)
    wf_after = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    live = find_node(wf_after, "14 Konflikte auflösen")["parameters"]["jsCode"]
    assert "_slots.includes(prod.slot_typ)" in live, "slot_scope-Liste-Patch nicht live"
    print("      ✓ Live-Workflow enthält slot_scope-Liste-Support")
    return 0


if __name__ == "__main__":
    sys.exit(main())
