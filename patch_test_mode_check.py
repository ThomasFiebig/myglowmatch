#!/usr/bin/env python3
"""
Workflow-Patch: Test-Mode-Check zwischen Node 17 und 18/18b (2026-06-25).

Ziel: bei Test-Profilen (first_name endsWith '-TEST') wird die E-Mail
NICHT versendet, Log bleibt aktiv.

Vor:
  17 → 18 (Kunden-Mail)
  17 → 18b (Partner-Mail)
  17 → 19 (Log)

Nach:
  17 → Test-Mode-Check (IF: first_name endsWith '-TEST')
    │
    ├─ true  → (nichts)
    └─ false → 18, 18b
  17 → 19 (Log bleibt direkt)

Damit laufen Test-Suite-Bulk-Runs ohne Mail-Versand, aber alle Pipeline-
Stufen werden trotzdem geloggt.
"""

import json
import sys
import uuid
from pathlib import Path

IN_PATH = Path("workflow_live_now.json")
OUT_PATH = Path("workflow_test_mode_check.json")

NODE17 = "17 Claude E-Mail formulieren"
NODE18 = "18 E-Mail senden"
NODE18B = "18b Partner-Mail senden"
NODE19 = "19 Log speichern"
IF_NODE = "Test-Mode-Check"


def build_if_node(position):
    return {
        "id": str(uuid.uuid4()),
        "name": IF_NODE,
        "type": "n8n-nodes-base.if",
        "typeVersion": 2.3,
        "position": position,
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "typeValidation": "strict",
                    "version": 3,
                },
                "conditions": [
                    {
                        "id": str(uuid.uuid4()),
                        "leftValue": "={{ $json.first_name }}",
                        "rightValue": "-TEST",
                        "operator": {"type": "string", "operation": "endsWith"},
                    }
                ],
                "combinator": "and",
            },
            "options": {},
        },
    }


def main():
    if not IN_PATH.exists():
        print(f"FEHLER: {IN_PATH} fehlt.", file=sys.stderr)
        return 1

    wf = json.loads(IN_PATH.read_text())

    # Idempotenz
    existing = next((n for n in wf["nodes"] if n["name"] == IF_NODE), None)
    if existing:
        print(f"{IF_NODE} existiert bereits — kein Edit.")
        return 0

    # Position: zwischen Node 17 und Node 18
    n17 = next((n for n in wf["nodes"] if n["name"] == NODE17), None)
    n18 = next((n for n in wf["nodes"] if n["name"] == NODE18), None)
    if not n17 or not n18:
        print(f"FEHLER: Node 17 oder 18 nicht gefunden.", file=sys.stderr)
        return 1

    # Mittig zwischen 17 und 18, leicht versetzt
    pos = [int((n17["position"][0] + n18["position"][0]) / 2),
           int((n17["position"][1] + n18["position"][1]) / 2) - 80]
    if_node = build_if_node(pos)
    wf["nodes"].append(if_node)
    print(f"IF-Node '{IF_NODE}' angelegt (id={if_node['id']}, pos={pos})")

    # Connections umverkabeln
    conns = wf.setdefault("connections", {})
    n17_main = conns.get(NODE17, {}).get("main", [[]])
    if not n17_main or not n17_main[0]:
        print("FEHLER: Node 17 hat keine main-Connections.", file=sys.stderr)
        return 1

    # Filter out 18 und 18b aus 17's outputs, behalte 19
    n17_targets = n17_main[0]
    new_n17_targets = []
    for t in n17_targets:
        if t.get("node") in (NODE18, NODE18B):
            continue  # weglinken, später über IF-Node
        new_n17_targets.append(t)
    # 17 → Test-Mode-Check hinzufügen
    new_n17_targets.append({"node": IF_NODE, "type": "main", "index": 0})
    conns[NODE17]["main"][0] = new_n17_targets

    # Test-Mode-Check: zwei main-Branches (true, false)
    conns[IF_NODE] = {
        "main": [
            [],  # index 0 = true → nichts
            [   # index 1 = false → 18 + 18b
                {"node": NODE18, "type": "main", "index": 0},
                {"node": NODE18B, "type": "main", "index": 0},
            ],
        ]
    }
    print(f"Connections: 17 → [..., {IF_NODE}], {IF_NODE} false → [18, 18b]")

    # Top-Level-Felder die n8n beim PUT nicht akzeptiert
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags", "shared",
              "active", "meta", "isArchived", "homeProject", "scopes", "pinData",
              "activeVersion", "activeVersionId", "sourceWorkflowId", "nodeGroups",
              "versionCounter", "description", "staticData"):
        wf.pop(k, None)

    OUT_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"\nGeschrieben: {OUT_PATH}")
    print(f"Nodes: {len(wf['nodes'])} (vorher 26, jetzt 27 mit IF)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
