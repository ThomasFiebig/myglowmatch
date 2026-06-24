#!/usr/bin/env python3
"""
Patch Live-Workflow für Node-05-Migration (2026-06-23).

Eingang: workflow_live_20260623.json (frisch via n8n API)
Ausgang: workflow_node05_v2.json (zum n8n-Import)

Änderungen:
1. Neue Node `05a map_derived_variables laden` (googleSheets) einfügen
2. Node 05 jsCode komplett ersetzen mit JSON-Regel-Evaluator
3. Connection 04 → 05 umverkabeln auf 04 → 05a → 05

Output-Shape von Node 05 bleibt identisch ({ normalized, priorities, flags }),
damit Folgenodes nichts merken.
"""

import json
import sys
import uuid
from pathlib import Path

IN_PATH = Path("workflow_live_20260623.json")
OUT_PATH = Path("workflow_node05_v2.json")

DOC_ID = "1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A"
DOC_NAME = "MONAT_Produktdatenbank_KOMPLETT"
DOC_URL = f"https://docs.google.com/spreadsheets/d/{DOC_ID}/edit?usp=drivesdk"

NEW_LOAD_NODE_NAME = "05a map_derived_variables laden"
NODE05_NAME = "05 Bool-Flags berechnen"
NODE04_NAME = "04 Prioritäten auflösen"

NODE05_V2_JSCODE = r"""// NODE 05 v2: Bool-Flags aus map_derived_variables auswerten
// ===========================================================
// Ersetzt 76 LOC Inline-Heuristiken durch generischen JSON-Regel-
// Evaluator. Regeln stammen aus Sheet 'map_derived_variables'
// (Spalten: variable, typ, regel_json, erlaubte_werte, konsumenten, doku).
//
// Sheet-Reihenfolge = Auswertungs-Reihenfolge.
// Phase 1 (R02-R14): nur normalized.* Refs
// Phase 2 (R15-R18): zusätzlich flags.* Refs
//
// VORAUSSETZUNG: Node 05a 'map_derived_variables laden' muss
// vor Node 05 ausgeführt werden (Verkabelung 04 → 05a → 05).
// ===========================================================

const item = $node["04 Prioritäten auflösen"].json;
const n = item.normalized;
const p = item.priorities;

const sheetRows = $items("05a map_derived_variables laden")
  .map(it => it.json)
  .filter(r => r.variable && r.regel_json);

function resolveRef(path, ctx) {
  const parts = path.split(".");
  const src = parts.shift();
  const root = src === "flags" ? ctx.flags
             : src === "normalized" ? ctx.normalized
             : src === "priorities" ? ctx.priorities
             : null;
  if (root === null) throw new Error(`Unknown ref source: ${src} (path: ${path})`);
  return parts.reduce((acc, k) => (acc == null ? acc : acc[k]), root);
}

function evalExpr(expr, ctx) {
  if (expr === true || expr === false) return expr;
  if (expr == null) throw new Error("null/undefined expression");
  const op = Object.keys(expr)[0];
  const v = expr[op];
  switch (op) {
    case "eq":  return resolveRef(v[0], ctx) === v[1];
    case "neq": return resolveRef(v[0], ctx) !== v[1];
    case "in":  return v[1].includes(resolveRef(v[0], ctx));
    case "nin": return !v[1].includes(resolveRef(v[0], ctx));
    case "includes": {
      const arr = resolveRef(v[0], ctx);
      return Array.isArray(arr) && arr.includes(v[1]);
    }
    case "intersects": {
      const arr = resolveRef(v[0], ctx);
      return Array.isArray(arr) && arr.some(x => v[1].includes(x));
    }
    case "truthy": {
      const x = resolveRef(v, ctx);
      return x !== undefined && x !== null && x !== "" && x !== false;
    }
    case "and": return v.every(e => evalExpr(e, ctx));
    case "or":  return v.some(e => evalExpr(e, ctx));
    case "not": return !evalExpr(v, ctx);
    default: throw new Error(`Unknown operator: ${op}`);
  }
}

function evalRule(rule, ctx) {
  if (rule.cases) {
    for (const c of rule.cases) {
      if (evalExpr(c.when, ctx)) return c.then;
    }
    return rule.else;
  }
  return evalExpr(rule, ctx);
}

const flags = {};
const ctx = { normalized: n, priorities: p, flags };

for (const row of sheetRows) {
  let rule;
  try {
    rule = JSON.parse(row.regel_json);
  } catch (e) {
    throw new Error(`map_derived_variables.${row.variable}: regel_json parse error: ${e.message}`);
  }
  try {
    flags[row.variable] = evalRule(rule, ctx);
  } catch (e) {
    throw new Error(`map_derived_variables.${row.variable}: eval error: ${e.message}`);
  }
}

return [{ json: { normalized: n, priorities: p, flags } }];
"""


def build_load_node(node05_pos):
    """Sheet-Load-Node analog zu 04a/06a, positioniert zwischen 04a (x=304) und 06a (x=688)."""
    x = node05_pos[0]  # gleiche X-Spalte wie Node 05
    y = -64            # gleiche Y-Höhe wie andere Load-Nodes
    return {
        "id": str(uuid.uuid4()),
        "name": NEW_LOAD_NODE_NAME,
        "type": "n8n-nodes-base.googleSheets",
        "typeVersion": 4.5,
        "position": [x, y],
        "parameters": {
            "documentId": {
                "__rl": True,
                "value": DOC_ID,
                "mode": "list",
                "cachedResultName": DOC_NAME,
                "cachedResultUrl": DOC_URL,
            },
            "sheetName": {
                "__rl": True,
                "value": "map_derived_variables",
                "mode": "name",
            },
            "options": {},
        },
        "credentials": {
            "googleSheetsOAuth2Api": None,  # wird beim ersten Speichern in n8n neu verknüpft
        },
    }


def main():
    if not IN_PATH.exists():
        print(f"FEHLER: {IN_PATH} fehlt — erst Workflow per n8n-API holen.", file=sys.stderr)
        return 1

    wf = json.loads(IN_PATH.read_text())

    # 1) typeVersion + credentials vom 04a übernehmen, damit der Patch stilkonsistent ist
    load_template = next((n for n in wf["nodes"] if n["name"] == "04a Prioritäten laden"), None)
    if not load_template:
        print("FEHLER: Template-Node '04a Prioritäten laden' nicht gefunden.", file=sys.stderr)
        return 1
    node05 = next((n for n in wf["nodes"] if n["name"] == NODE05_NAME), None)
    if not node05:
        print(f"FEHLER: Node {NODE05_NAME!r} nicht gefunden.", file=sys.stderr)
        return 1

    # Idempotenz: wenn 05a bereits existiert, nicht doppelt anlegen
    existing_05a = next((n for n in wf["nodes"] if n["name"] == NEW_LOAD_NODE_NAME), None)
    if existing_05a:
        load_node = existing_05a
        print(f"05a existiert bereits (id={load_node['id']}) — wird beibehalten")
    else:
        load_node = build_load_node(node05["position"])
        load_node["typeVersion"] = load_template.get("typeVersion", 4.5)
        # credentials-Struktur 1:1 übernehmen (verweist auf existierenden Credential-Eintrag)
        load_node["credentials"] = json.loads(json.dumps(load_template.get("credentials", {})))
        wf["nodes"].append(load_node)
        print(f"05a neu angelegt (id={load_node['id']})")

    # 2) Node 05 jsCode patchen
    old_loc = len(node05["parameters"].get("jsCode", "").splitlines())
    node05["parameters"]["jsCode"] = NODE05_V2_JSCODE
    new_loc = len(NODE05_V2_JSCODE.splitlines())
    print(f"Node 05 jsCode: {old_loc} LOC → {new_loc} LOC")

    # 3) Connections umverkabeln
    # vorher: 04 -> [05]
    # nachher: 04 -> [05a], 05a -> [05]
    conns = wf.setdefault("connections", {})

    # Backup vorhandener 04-Connections, dann auf 05a umlenken
    node04_conns = conns.get(NODE04_NAME, {}).get("main", [])
    if not node04_conns:
        print(f"FEHLER: {NODE04_NAME!r} hat keine main-Connections.", file=sys.stderr)
        return 1
    # main[0] ist die Standard-Output-Liste
    targets = node04_conns[0]
    new_targets = []
    rewired = False
    for t in targets:
        if t.get("node") == NODE05_NAME and not rewired:
            new_targets.append({"node": NEW_LOAD_NODE_NAME, "type": "main", "index": 0})
            rewired = True
        else:
            new_targets.append(t)
    if not rewired:
        # Falls 04 → 05 nicht direkt verknüpft war (z.B. schon migriert): kein Edit
        print(f"WARN: 04 → 05 nicht direkt verknüpft, lasse Connections unverändert")
    else:
        conns[NODE04_NAME]["main"][0] = new_targets
        print(f"04 → 05 umverkabelt auf 04 → 05a")

    # 05a → 05 hinzufügen
    load_conns = conns.setdefault(NEW_LOAD_NODE_NAME, {}).setdefault("main", [[]])
    if not any(t.get("node") == NODE05_NAME for t in load_conns[0]):
        load_conns[0].append({"node": NODE05_NAME, "type": "main", "index": 0})
        print(f"05a → 05 verkabelt")

    # 4) n8n-API-Felder, die beim PUT/Import stören könnten, entfernen.
    # activeVersion-Familie ergänzt 2026-06-24: n8n-Cloud liefert beim GET einen
    # Snapshot-Subtree mit dem Pre-Patch-State zurück; ohne pop bleibt der alte
    # jsCode im lokalen Output-File und verwirrt späteren Lokal-Grep
    # (siehe Session-Doku 2026-06-24 Teil 1 Erkenntnis 1).
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags", "shared",
              "active", "meta", "isArchived", "homeProject", "scopes", "pinData",
              "activeVersion", "activeVersionId", "sourceWorkflowId", "nodeGroups",
              "versionCounter", "description", "staticData"):
        wf.pop(k, None)

    OUT_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"\nGeschrieben: {OUT_PATH}")
    print(f"Nodes: {len(wf['nodes'])} (vorher {len(wf['nodes'])-1 if not existing_05a else len(wf['nodes'])})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
