#!/usr/bin/env python3
"""
Patch Node 06 jsCode für Migration #10 (Phase 2 ins Sheet, 2026-06-24).

Eingang: workflow_live_now.json (frisch via n8n API)
Ausgang: workflow_node06_v4.json (zum n8n-PUT)

Änderung: Phase-2-Inline-Block raus, evalBedingung() liefert Punkte
statt Boolean, neuer Operator `array_count_except` mit `max_punkte`-
Cap eingebaut.
"""

import json
import sys
from pathlib import Path

IN_PATH = Path("workflow_live_now.json")
OUT_PATH = Path("workflow_node06_v4.json")
NODE06_NAME = "06 Pflegelevel berechnen"

NODE06_V4_JSCODE = r"""// ============================================================
// NODE 06 v4: Pflegelevel berechnen — Regeln aus DB
// ============================================================
// Architektur-Prinzip: Tabelle = Wahrheit, Node = Auswerter.
// Punktevergabe-Regeln stehen in map_pflegelevel_scoring.
// Floor, Cap, Schwellen und max_products bleiben im Code,
// weil das System-Parameter sind, keine fachlichen Regeln.
//
// VORAUSSETZUNG: Node 06a Pflegelevel-Scoring laden muss im
// Workflow vor Node 06 ausgeführt werden (Verkabelung:
// 05 → 06a → 06).
//
// Migration #10 (2026-06-24): Phase 2 (Ziele-Bonus) jetzt
// als PFL-23 im Sheet via Operator `array_count_except` mit
// `max_punkte`-Cap. Inline-Block raus.
// ============================================================

// Profildaten aus Node 05 holen (analog zu Node 14 → Node 11)
const profile = $node["05 Bool-Flags berechnen"].json;
const n = profile.normalized;
const p = profile.priorities;
const f = profile.flags;

// Regeln aus DB laden (über $items aus 06a)
const scoringRules = $items("06a Pflegelevel-Scoring laden")
  .map(it => it.json)
  .filter(r => String(r.aktiv).toUpperCase() === 'TRUE');

// ── Helpers ──
// applyRule gibt Punkte (oder 0) statt Boolean — unterstützt
// sowohl Match-Operatoren (fixed punkte) als auch aggregate-
// Operatoren (count × punkte, gecappt auf max_punkte).
function applyRule(rule) {
  const feld = rule.bedingung_feld;
  const wert = String(rule.bedingung_wert || '').trim();
  const typ  = String(rule.bedingung_typ || '').trim();
  const pts  = parseInt(rule.punkte) || 0;
  const capRaw = rule.max_punkte;
  const cap  = (capRaw === '' || capRaw == null) ? null : (parseInt(capRaw) || null);
  const fieldValue = n[feld];

  if (typ === 'array_contains') {
    return (Array.isArray(fieldValue) && fieldValue.includes(wert)) ? pts : 0;
  }

  if (typ === 'equals') {
    return (String(fieldValue || '').toLowerCase() === wert.toLowerCase()) ? pts : 0;
  }

  if (typ === 'in_list') {
    const allowed = wert.split('|').map(s => s.trim().toLowerCase());
    return allowed.includes(String(fieldValue || '').toLowerCase()) ? pts : 0;
  }

  if (typ === 'array_count_except') {
    if (!Array.isArray(fieldValue)) return 0;
    const count = fieldValue.filter(v => v !== wert).length;
    const total = count * pts;
    return cap != null ? Math.min(total, cap) : total;
  }

  return 0;
}

// ── Phase 1+2: Regel-basierte Punkte aus DB ──
// Phase 2 (Ziele-Bonus PFL-23) ist seit Migration #10 ebenfalls
// im Sheet — kein Inline-Block mehr.

let pts = 0;
const firedRules = [];

// Spezialbehandlung: PFL-02/03 (haarbruch/spliss) sollen NICHT zusätzlich
// zu PFL-01 (stark_geschaedigt) feuern — Code-Logik: else if
const hasStarkGesch = (n.hair_condition || []).includes('stark_geschaedigt');

for (const rule of scoringRules) {
  if (hasStarkGesch && ['PFL-02', 'PFL-03'].includes(rule.regel_id)) continue;

  const earned = applyRule(rule);
  if (earned > 0) {
    pts += earned;
    firedRules.push({
      regel_id: rule.regel_id,
      kategorie: rule.kategorie,
      punkte: earned
    });
  }
}

// ── Phase 3: Rohlevel (LOW/MID/HIGH Schwellen) ──
// System-Parameter, kein fachlicher Regel-Inhalt
let level    = pts <= 3 ? 'LOW' : pts <= 7 ? 'MID' : 'HIGH';
let levelNum = level === 'LOW' ? 1 : level === 'MID' ? 2 : 3;

// ── Phase 4 + 5: Override-Regeln aus map_pflegelevel_overrides ──
// Tabelle = Wahrheit. raise_to setzt Floor, cap_at setzt Ceiling.
// Else-If-Semantik via prioritaet (erste passende raise-Regel stoppt die Kette).
// Cap-Regeln greifen nur, wenn keine raise-Regel gematcht hat (auch ohne Update).

const overrideRules = $items("06b Pflegelevel-Overrides laden")
  .map(it => it.json)
  .filter(r => String(r.aktiv).toUpperCase() === 'TRUE');

const LEVEL_TO_NUM = { LOW: 1, MID: 2, HIGH: 3 };
const NUM_TO_LEVEL = { 1: 'LOW', 2: 'MID', 3: 'HIGH' };

function evalSingleCondition(profileObj, feld, typ, wert) {
  if (!feld || !typ) return true;
  const val = profileObj[feld];
  const w = String(wert == null ? '' : wert);
  const t = String(typ).toLowerCase().trim();
  switch (t) {
    case 'equals':
      return String(val == null ? '' : val).toLowerCase() === w.toLowerCase();
    case 'in_list':
      return w.split('|').map(s => s.trim().toLowerCase())
        .includes(String(val == null ? '' : val).toLowerCase());
    case 'array_contains':
      return Array.isArray(val) && val.includes(w);
    default:
      return false;
  }
}

function evalOverrideRule(rule, profileObj) {
  if (!evalSingleCondition(profileObj, rule.bedingung1_feld, rule.bedingung1_typ, rule.bedingung1_wert)) return false;
  if (!evalSingleCondition(profileObj, rule.bedingung2_feld, rule.bedingung2_typ, rule.bedingung2_wert)) return false;
  return true;
}

// raise_to in prioritaet-Reihenfolge, erste passende Regel stoppt die Kette
const raiseRules = overrideRules
  .filter(r => String(r.aktion).toLowerCase() === 'raise_to')
  .sort((a, b) => (parseInt(a.prioritaet) || 999) - (parseInt(b.prioritaet) || 999));

let raiseMatched = null;
for (const rule of raiseRules) {
  if (evalOverrideRule(rule, n)) {
    raiseMatched = rule.regel_id;
    const target = LEVEL_TO_NUM[String(rule.ziel_level).toUpperCase()];
    if (target && levelNum < target) {
      levelNum = target;
      level = NUM_TO_LEVEL[target];
      firedRules.push({
        regel_id: rule.regel_id,
        kategorie: 'override_floor',
        ziel_level: rule.ziel_level
      });
    }
    break;
  }
}

// cap_at — nur wenn keine raise-Regel gematcht hat
const rp = n.routine_preference;
if (!raiseMatched) {
  const capRules = overrideRules.filter(r => String(r.aktion).toLowerCase() === 'cap_at');
  for (const rule of capRules) {
    if (evalOverrideRule(rule, n)) {
      const target = LEVEL_TO_NUM[String(rule.ziel_level).toUpperCase()];
      if (target && levelNum > target) {
        levelNum = target;
        level = NUM_TO_LEVEL[target];
        firedRules.push({
          regel_id: rule.regel_id,
          kategorie: 'override_cap',
          ziel_level: rule.ziel_level
        });
      }
    }
  }
}

// ── Phase 6: Max Products aus map_max_products ──
// Tabelle = Wahrheit. 2D-Lookup (routine_preference × pflegelevel) → max_products.
const maxRules = $items("06c Max-Products laden")
  .map(it => it.json)
  .filter(r => String(r.aktiv).toUpperCase() === 'TRUE');

let maxProducts = 7; // Safety-Default falls keine Regel matched
for (const rule of maxRules) {
  const sameRp    = String(rule.routine_preference).toLowerCase() === String(rp).toLowerCase();
  const sameLevel = String(rule.pflegelevel).toUpperCase() === String(level).toUpperCase();
  if (sameRp && sameLevel) {
    maxProducts = parseInt(rule.max_products) || 7;
    break;
  }
}

const pflegelevel = {
  pflegelevel_raw:     pts,
  pflegelevel_final:   level,
  pflegelevel_numeric: levelNum,
  max_products:        maxProducts,
  routine_preference:  rp,
  fired_rules:         firedRules
};

return [{ json: {
  normalized: n,
  priorities: p,
  flags: f,
  pflegelevel
}}];
"""


def main():
    if not IN_PATH.exists():
        print(f"FEHLER: {IN_PATH} fehlt — erst Workflow per n8n-API holen.", file=sys.stderr)
        return 1

    wf = json.loads(IN_PATH.read_text())
    node06 = next((n for n in wf["nodes"] if n["name"] == NODE06_NAME), None)
    if not node06:
        print(f"FEHLER: Node {NODE06_NAME!r} nicht gefunden.", file=sys.stderr)
        return 1

    old_loc = len(node06["parameters"].get("jsCode", "").splitlines())
    node06["parameters"]["jsCode"] = NODE06_V4_JSCODE
    new_loc = len(NODE06_V4_JSCODE.splitlines())
    print(f"Node 06 jsCode: {old_loc} LOC → {new_loc} LOC")

    # Top-Level-Felder, die der PUT nicht akzeptiert (analog Migration #9)
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
