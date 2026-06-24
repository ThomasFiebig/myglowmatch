#!/usr/bin/env python3
"""
Patch Node 11 jsCode für Migration #11 (Suppress-Regel ins Sheet, 2026-06-24).

Eingang: workflow_live_now.json (frisch via n8n API)
Ausgang: workflow_node11_v2.json (zum n8n-PUT)

Änderung:
  - Inline-Block Z. 162-165 raus (`if minimal → optional=[]`)
  - Neue Phase 5 vor Return: alle finalFired-Regeln mit
    prioritaet=suppress_optional werten Side-Effects aus
    (slots.optional = []).

Sheet-Regel: REQ-MIN-NO-OPT (vorab via append_row eingefügt).
"""

import json
import sys
from pathlib import Path

IN_PATH = Path("workflow_live_now.json")
OUT_PATH = Path("workflow_node11_v2.json")
NODE11_NAME = "11 REQ-Regeln auswerten"

NODE11_V2_JSCODE = r"""// NODE 11 v2: REQ-Regeln vollständig deklarativ aus map_slot_rules
// =============================================================
// Liest alle Slot-Regeln aus dem Google Sheet "map_slot_rules".
// KEINE Regel mehr im Code. Tabelle = Wahrheit, Node = Auswerter.
//
// Tabellenspalten:
//   regel_id | slot_typ | prioritaet
//   | trigger_flag  | trigger_wert     ← Hauptbedingung
//   | trigger_flag2 | trigger_wert2    ← UND-Verknüpfung (optional)
//   | overrides                        ← regel_id(s) die ersetzt werden (CSV)
//   | requires_not                     ← Regel feuert nur wenn diese regel_id(s) NICHT gefeuert haben (CSV)
//   | filter | reason | aktiv
//
// prioritaet-Werte:
//   - required_always / required_conditional / optional → Slot wird in die jeweilige Liste eingefügt
//   - suppress_optional → Side-Effect-Regel (Migration #11, 2026-06-24): wenn sie feuert,
//     wird slots.optional komplett geleert. slot_typ bleibt leer.
//
// trigger_wert Syntax:
//   - "TRUE" / "FALSE"      → Boolean
//   - "yes" / "stark_..."   → String exakt
//   - "schuppig|fettig"     → ODER (mehrere erlaubte Werte)
//   - ">=2", ">3", "=1"     → Numerischer Vergleich
//   - hair_condition_contains + Wert → Array-Inklusion in n.hair_condition
//
// requires_not wird in zweiter Phase aufgelöst (nachdem alle anderen
// Regeln evaluiert wurden), damit Reihenfolge in der Tabelle egal ist.
// =============================================================

const profile = $node["08 Ausschluss-Filter"].json;
const n   = profile.normalized;
const f   = profile.flags;
const pl  = profile.pflegelevel;
const p   = profile.priorities;
const pool = profile.filtered_pool;

const ruleItems = $items("10 map_slot_rules");
const rules = ruleItems
  .map(it => it.json)
  .filter(r => String(r.aktiv).toUpperCase() === 'TRUE');

// ── Helpers ─────────────────────────────────────────────────

function normStr(v) {
  return v === undefined || v === null ? '' : String(v).trim();
}

function getFlagValue(flagName) {
  if (flagName in f)  return f[flagName];
  if (flagName in n)  return n[flagName];
  if (flagName in pl) return pl[flagName];
  if (flagName in p)  return p[flagName];
  return undefined;
}

function evalSingleTrigger(flag, wert) {
  flag = normStr(flag);
  wert = normStr(wert);
  if (flag === '') return true; // leer = immer wahr

  if (flag === 'hair_condition_contains') {
    return Array.isArray(n.hair_condition) && n.hair_condition.includes(wert);
  }

  const val = getFlagValue(flag);
  if (val === undefined) return false;

  // Numerischer Vergleich
  const numMatch = wert.match(/^(>=|<=|>|<|=)\s*(-?\d+(?:\.\d+)?)$/);
  if (numMatch) {
    const op = numMatch[1], num = parseFloat(numMatch[2]);
    const v = parseFloat(val);
    if (isNaN(v)) return false;
    switch (op) {
      case '>=': return v >= num;
      case '<=': return v <= num;
      case '>':  return v >  num;
      case '<':  return v <  num;
      case '=':  return v === num;
    }
  }

  // ODER-Liste
  if (wert.includes('|')) {
    const allowed = wert.split('|').map(s => s.trim().toLowerCase());
    return allowed.includes(String(val).toLowerCase());
  }

  // Boolean
  const wU = wert.toUpperCase();
  if (wU === 'TRUE')  return val === true  || String(val).toUpperCase() === 'TRUE';
  if (wU === 'FALSE') return val === false || String(val).toUpperCase() === 'FALSE';

  // String exakt (case-insensitive)
  return String(val).toLowerCase() === wert.toLowerCase();
}

function evalRule(r) {
  // UND-Verknüpfung beider Trigger
  if (!evalSingleTrigger(r.trigger_flag,  r.trigger_wert))  return false;
  if (!evalSingleTrigger(r.trigger_flag2, r.trigger_wert2)) return false;
  return true;
}

function csvList(v) {
  return normStr(v).split(',').map(s => s.trim()).filter(Boolean);
}

// ── Phase 1: Welche Regeln feuern grundsätzlich? ────────────

const firedIds = new Set();
const firedByRule = {};

for (const r of rules) {
  if (evalRule(r)) {
    firedIds.add(r.regel_id);
    firedByRule[r.regel_id] = r;
  }
}

// ── Phase 2: requires_not auflösen ─────────────────────────
//    Regel verwerfen wenn eine ihrer requires_not-IDs gefeuert hat.

const finalFired = new Set();
for (const id of firedIds) {
  const r = firedByRule[id];
  const blockedBy = csvList(r.requires_not);
  const isBlocked = blockedBy.some(bid => firedIds.has(bid));
  if (!isBlocked) finalFired.add(id);
}

// ── Phase 3: overrides auflösen ────────────────────────────
//    Wenn Regel X overrides=Y enthält, wird Y aus finalFired entfernt.

const overridden = new Set();
for (const id of finalFired) {
  const r = firedByRule[id];
  for (const oid of csvList(r.overrides)) overridden.add(oid);
}
for (const oid of overridden) finalFired.delete(oid);

// ── Phase 4: Slot-Assignments bauen ────────────────────────

const slots = {
  required_always:      [],
  required_conditional: [],
  optional:             [],
  disabled:             []
};

// Reihenfolge wie in Tabelle erhalten
for (const r of rules) {
  if (!finalFired.has(r.regel_id)) continue;

  const prio = normStr(r.prioritaet);
  // Side-Effect-Regeln (suppress_*) werden in Phase 5 behandelt
  if (prio.startsWith('suppress_')) continue;

  const entry = {
    slot_typ: normStr(r.slot_typ),
    filter:   normStr(r.filter),
    reason:   `${r.regel_id}: ${r.reason || ''}`.trim()
  };

  if (prio === 'required_always')           slots.required_always.push(entry);
  else if (prio === 'required_conditional') slots.required_conditional.push(entry);
  else if (prio === 'optional')             slots.optional.push(entry);
}

// ── Phase 5: Side-Effect-Regeln (Migration #11, 2026-06-24) ─
//    suppress_optional → leert slots.optional, slot_typ ignoriert.
//    Erweiterbar um suppress_required_conditional / suppress_required_always /
//    suppress_disabled, falls jemals nötig.

for (const r of rules) {
  if (!finalFired.has(r.regel_id)) continue;
  const prio = normStr(r.prioritaet);
  if (prio === 'suppress_optional') {
    slots.optional = [];
  }
}

return [{ json: {
  normalized:       n,
  priorities:       p,
  flags:            f,
  pflegelevel:      pl,
  filtered_pool:    pool,
  slot_assignments: slots,
  applied_rules:    Array.from(finalFired)
}}];
"""


def main():
    if not IN_PATH.exists():
        print(f"FEHLER: {IN_PATH} fehlt — erst Workflow per n8n-API holen.", file=sys.stderr)
        return 1

    wf = json.loads(IN_PATH.read_text())
    node11 = next((n for n in wf["nodes"] if n["name"] == NODE11_NAME), None)
    if not node11:
        print(f"FEHLER: Node {NODE11_NAME!r} nicht gefunden.", file=sys.stderr)
        return 1

    old_loc = len(node11["parameters"].get("jsCode", "").splitlines())
    node11["parameters"]["jsCode"] = NODE11_V2_JSCODE
    new_loc = len(NODE11_V2_JSCODE.splitlines())
    print(f"Node 11 jsCode: {old_loc} LOC → {new_loc} LOC")

    # Top-Level-Felder, die der PUT nicht akzeptiert (analog Migration #9/#10)
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags", "shared",
              "active", "meta", "isArchived", "homeProject", "scopes", "pinData",
              "activeVersion", "activeVersionId", "sourceWorkflowId", "nodeGroups",
              "versionCounter", "description", "staticData"):
        wf.pop(k, None)

    OUT_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))
    print(f"\nGeschrieben: {OUT_PATH}")
    print(f"Nodes: {len(wf['nodes'])}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
