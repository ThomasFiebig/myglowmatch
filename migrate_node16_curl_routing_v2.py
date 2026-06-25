#!/usr/bin/env python3
"""
Migration #16 — Curl-Routing Phase 2 + Smoothing-Hitzeschutz (2026-06-25).

Backend-Anpassungen ohne Workflow-Patch (Engine generisch).

A) map_derived_variables (Phase 2 erweitern):
   - NEU `needs_curl_gelee_styling` = (needs_curl_care AND heat_use=yes) OR wants_full_curl_line
     → ersetzt REQ-12 trigger_flag2=heat_use=yes, damit Sina (nach heat_frequency-
       Update auf nie_selten) trotzdem curl_gelee bekommt
   - NEU `prefers_straight_with_frizz` = prefers_straight AND hair_condition.includes('frizz')
     → Trigger für REQ-04b

B) map_slot_rules:
   - REQ-12 trigger_flag2: heat_use=yes → needs_curl_gelee_styling=TRUE
   - REQ-04 requires_not ergänzen um REQ-04b
   - REQ-04b NEU: prefers_straight_with_frizz=TRUE + heat_use=yes → smoothing_fohn_spray styling_1
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from sheets_writer import open_sheet, update_cell, read_row, load_env, resolve_sa_path, DOC_ID

DERIVED_HEADER = ["variable", "typ", "regel_json", "erlaubte_werte", "konsumenten", "doku"]

# Komplettes Grid für map_derived_variables (Phase-2-Erweiterung mit zwei neuen Variablen)
DERIVED_ROWS = [
    # Phase 1
    ("heat_use", "enum",
     {"cases": [{"when": {"in": ["normalized.heat_frequency", ["regelmaessig", "sehr_haeufig"]]}, "then": "yes"}], "else": "no"},
     "yes | no",
     "map_slot_rules R6/R11/R12/R4b; map_conflict_rules R3",
     "Hitzeschutz-Trigger; haeufige Hitze-Nutzung"),
    ("oil_need", "enum",
     {"cases": [{"when": {"eq": ["normalized.ends_condition", "deutlich_trocken"]}, "then": "yes"}, {"when": {"eq": ["normalized.ends_condition", "leicht_trocken"]}, "then": "maybe"}], "else": "no"},
     "yes | maybe | no",
     "map_slot_rules R10/R18",
     "REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand"),
    ("needs_repair_focus", "bool",
     {"or": [{"includes": ["normalized.hair_condition", "stark_geschaedigt"]}, {"eq": ["normalized.hair_treatments", "blondiert"]}]},
     "true | false",
     "map_slot_rules R4/R5/R22/R23; map_pool_filter R2; flags.wants_intense_care",
     "Bond-IQ-Trigger; starke Schaedigung oder Blondierung"),
    ("needs_scalp_focus", "bool",
     {"intersects": ["normalized.scalp_status", ["juckend_empfindlich", "schuppig", "trocken"]]},
     "true | false",
     "map_slot_rules R21",
     "Scalp-Comfort-Trigger; problematische Kopfhaut"),
    ("needs_lightweight_logic", "bool",
     {"or": [{"eq": ["normalized.hair_thickness", "fein"]}, {"includes": ["normalized.hair_condition", "kraftlos"]}]},
     "true | false",
     "flags.wants_intense_care (POOL-02 gewicht-Filter ist bewusste Luecke)",
     "Negativ-Input fuer wants_intense_care; feines oder kraftloses Haar will nichts Schweres"),
    ("needs_curl_care", "bool",
     {"and": [{"in": ["normalized.hair_structure", ["wellig", "lockig", "kraus"]]}, {"neq": ["normalized.curl_priority", "glatt"]}]},
     "true | false",
     "map_slot_rules R11/R12/R11b; flags.curl_refresh_needed; flags.styling_goal_definition; flags.wants_full_curl_line; flags.needs_curl_gelee_styling",
     "Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15)"),
    ("prefers_straight", "bool",
     {"and": [{"in": ["normalized.hair_structure", ["wellig", "lockig", "kraus"]]}, {"eq": ["normalized.curl_priority", "glatt"]}]},
     "true | false",
     "flags.prefers_straight_with_frizz",
     "User mit Locken/Wellen, will aber glatt tragen (Migration #15)"),
    ("detangling_need", "enum",
     {"cases": [
         {"when": {"or": [{"includes": ["normalized.hair_condition", "haarbruch"]}, {"includes": ["normalized.hair_condition", "spliss"]}, {"and": [{"eq": ["normalized.hair_structure", "kraus"]}, {"eq": ["normalized.ends_condition", "deutlich_trocken"]}]}]}, "then": "stark_verfilzt"},
         {"when": {"or": [{"and": [{"includes": ["normalized.hair_condition", "trocken"]}, {"not": {"includes": ["normalized.hair_condition", "haarbruch"]}}]}, {"and": [{"eq": ["normalized.hair_structure", "lockig"]}, {"not": {"includes": ["normalized.hair_condition", "keine_probleme"]}}]}]}, "then": "leicht_verfilzt"},
     ], "else": "problemlos"},
     "stark_verfilzt | leicht_verfilzt | problemlos",
     "map_slot_rules R9/R19",
     "REQ-07/18; 3-stufige Verfilzungs-Einstufung"),
    ("needs_dry_shampoo", "bool",
     {"eq": ["normalized.wash_frequency", "taeglich"]},
     "true | false",
     "map_slot_rules R15",
     "The-Champ-Trigger; taegliches Waschen"),
    ("styling_goal_volumen", "bool",
     {"includes": ["normalized.care_goals", "volumen"]},
     "true | false",
     "map_slot_rules R20",
     "Volumen-Ziel aus User-Auswahl"),
    ("styling_goal_glanz", "bool",
     {"includes": ["normalized.care_goals", "glanz"]},
     "true | false",
     "map_slot_rules R17",
     "Glanz-Ziel aus User-Auswahl"),
    ("styling_goal_halt", "bool",
     {"and": [{"eq": ["normalized.styling_effort", "aufwendiges_styling"]}, {"in": ["normalized.hair_thickness", ["fein", "mittel"]]}, {"in": ["normalized.hair_structure", ["glatt", "wellig"]]}]},
     "true | false",
     "map_slot_rules R16",
     "Moxie-Mousse-Trigger; aufwendiges Styling auf feinem/mittlerem glatten/welligem Haar"),
    # Phase 2
    ("curl_refresh_needed", "bool",
     {"and": [{"neq": ["normalized.wash_frequency", "taeglich"]}, {"eq": ["flags.needs_curl_care", True]}]},
     "true | false",
     "map_slot_rules REQ-13",
     "Curl-Auffrischer-Trigger; alle Wasch-Frequenzen AUSSER taeglich + Locken (Migration #15)"),
    ("styling_goal_definition", "bool",
     {"and": [{"eq": ["flags.needs_curl_care", True]}, {"in": ["normalized.curl_priority", ["mehr_definition", "beides"]]}]},
     "true | false",
     "map_conflict_rules R5",
     "Curl-Definition-Trigger; matcht mehr_definition UND beides (Migration #15)"),
    ("wants_full_curl_line", "bool",
     {"and": [{"eq": ["flags.needs_curl_care", True]}, {"eq": ["normalized.curl_priority", "beides"]}]},
     "true | false",
     "map_slot_rules REQ-11b; flags.needs_curl_gelee_styling",
     "User mit Locken wuenscht komplette Curl-Linie (Definition + Volumen+Halt) (Migration #15)"),
    # NEU Migration #16
    ("needs_curl_gelee_styling", "bool",
     {"or": [
         {"and": [{"eq": ["flags.needs_curl_care", True]}, {"eq": ["flags.heat_use", "yes"]}]},
         {"eq": ["flags.wants_full_curl_line", True]},
     ]},
     "true | false",
     "map_slot_rules REQ-12",
     "curl_gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie. Migration #16 — entkoppelt von heat_use, damit Sina (glaetteisen-frei) trotzdem curl_gelee bekommt."),
    # NEU Migration #16
    ("prefers_straight_with_frizz", "bool",
     {"and": [{"eq": ["flags.prefers_straight", True]}, {"includes": ["normalized.hair_condition", "frizz"]}]},
     "true | false",
     "map_slot_rules REQ-04b",
     "Locken-Traeger:in mit Glaett-Wunsch + Frizz: smoothing_fohn_spray priorisieren (Hitzeschutz + Frizz-Reduktion in einem). Migration #16."),
    ("wants_intense_care", "bool",
     {"or": [{"eq": ["flags.needs_repair_focus", True]}, {"and": [{"eq": ["flags.needs_lightweight_logic", False]}, {"in": ["normalized.hair_treatments", ["gefaerbt", "blondiert"]]}]}]},
     "true | false",
     "Node 12 v4 Stufe 11 (intensitaet-Tiebreaker)",
     "Pflege-Intensitaets-Praeferenz fuer Node-12-Ranking; NEU 2026-06-18"),
]


def build_derived_grid():
    grid = [DERIVED_HEADER]
    for var, typ, regel, erlaubt, konsum, doku in DERIVED_ROWS:
        grid.append([var, typ, json.dumps(regel, ensure_ascii=False), erlaubt, konsum, doku])
    return grid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true")
    args = ap.parse_args()

    grid = build_derived_grid()
    print(f"map_derived_variables: {len(grid)-1} Zeilen (Migration #16: 16→{len(grid)-1})")
    print(f"  Neue Variablen: needs_curl_gelee_styling, prefers_straight_with_frizz")

    if not args.commit:
        print("\n(dry-run)")
        return 0

    base = Path.cwd()
    env = load_env(base / ".env")
    sa = resolve_sa_path(env, base)
    sh = open_sheet(sa, DOC_ID)

    # 1) map_derived_variables komplett rewriten
    ws = sh.worksheet('map_derived_variables')
    ws.clear()
    end_col = chr(ord("A") + len(DERIVED_HEADER) - 1)
    ws.update(f"A1:{end_col}{len(grid)}", grid, value_input_option="RAW")
    rows_after = [r for r in ws.get_all_values() if any(c.strip() for c in r)]
    if len(rows_after) != len(grid):
        print(f"  WARN: {len(rows_after)} != {len(grid)}", file=sys.stderr)
        return 1
    print(f"  Re-Read: {len(rows_after)} rows verbatim ✓")

    # 2) map_slot_rules edits
    # REQ-12: trigger_flag2 von heat_use=yes auf needs_curl_gelee_styling=TRUE
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-12', 'trigger_flag2', 'needs_curl_gelee_styling')
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-12', 'trigger_wert2', 'TRUE')
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-12', 'reason',
                'Curl-Gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie (Migration #16)')
    # REQ-04 requires_not erweitern um REQ-04b
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-04', 'requires_not', 'REQ-11,REQ-11b,REQ-04b')

    # REQ-04b NEU anhaengen
    ws_slot = sh.worksheet('map_slot_rules')
    hdr = ws_slot.row_values(1)
    row_data = {
        'regel_id': 'REQ-04b',
        'slot_typ': 'styling_1',
        'prioritaet': 'required_conditional',
        'trigger_flag': 'prefers_straight_with_frizz',
        'trigger_wert': 'TRUE',
        'trigger_flag2': 'heat_use',
        'trigger_wert2': 'yes',
        'overrides': '',
        'requires_not': '',
        'filter': 'smoothing_fohn_spray',
        'reason': 'Smoothing Foehn-Spray bei Locken-Traeger:in mit Glaett-Wunsch + Frizz + Hitzestyling: Hitzeschutz + Frizz-Reduktion in einem (Migration #16)',
        'aktiv': 'TRUE',
    }
    new_row = [row_data.get(h, '') for h in hdr]
    ws_slot.append_row(new_row, value_input_option='RAW')

    print("\nVerifikation map_slot_rules:")
    for rid in ('REQ-04', 'REQ-04b', 'REQ-12'):
        r = read_row(sh, 'map_slot_rules', 'regel_id', rid)
        print(f"  {rid:8s} trigger={r.get('trigger_flag')}={r.get('trigger_wert')} + {r.get('trigger_flag2')}={r.get('trigger_wert2')} filter={r.get('filter')!r} req_not={r.get('requires_not')!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
