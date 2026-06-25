#!/usr/bin/env python3
"""
Migration #15 — Curl-Routing-Refactor (2026-06-25).

Drei Sheet-Edits in einem Rutsch:

1. map_derived_variables — vollständiges Rewrite (Schema unverändert, 14→16 Zeilen):
   - needs_curl_care: zusätzliche AND-Bedingung (curl_priority != 'glatt')
   - styling_goal_definition: matcht jetzt 'mehr_definition' UND 'beides'
   - curl_refresh_needed: matcht wash_frequency != 'taeglich' (statt nur '1x_pro_woche')
   - NEU prefers_straight: Phase 1 (referenziert nur normalized)
   - NEU wants_full_curl_line: Phase 2 (referenziert flags.needs_curl_care)

2. produktdatenbank — curl_auffrischer.slot_typ: styling_2 → styling_3 (neuer Slot)

3. map_slot_rules — REQ-Regel-Refactor:
   - REQ-04 requires_not = REQ-11,REQ-11b (Hitzeschutz weicht für Curl-Creme)
   - REQ-11 filter = curl_creme nur (war curl_creme|curl_gelee)
   - REQ-11b NEU: wants_full_curl_line=TRUE → curl_creme styling_1, required_conditional
   - REQ-12 filter = curl_gelee nur, overrides leer (war REQ-13)
   - REQ-13 slot_typ=styling_3, prioritaet=required_conditional (war optional)
   - REQ-20 requires_not = REQ-05 (Scalp-Serum weicht, wenn Behandlung feuert)

Erwartung: 0/36 Routing-Drift für die 7 Standard-Test-Profile.
Sinas Routine bekommt curl_creme (styling_1) + curl_gelee (styling_2) +
curl_auffrischer (styling_3), Hitzeschutz weicht, scalp_comfort_serum
fällt weg.
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from sheets_writer import load_env, resolve_sa_path, update_cell, read_row, DOC_ID, SCOPES, open_sheet


# ── map_derived_variables: komplettes Grid ──
DERIVED_HEADER = ["variable", "typ", "regel_json", "erlaubte_werte", "konsumenten", "doku"]

DERIVED_ROWS = [
    # Phase 1 — nur normalized-Refs
    (
        "heat_use", "enum",
        {"cases": [{"when": {"in": ["normalized.heat_frequency", ["regelmaessig", "sehr_haeufig"]]}, "then": "yes"}], "else": "no"},
        "yes | no",
        "map_slot_rules R6/R11/R12; map_conflict_rules R3",
        "Hitzeschutz-Trigger; haeufige Hitze-Nutzung",
    ),
    (
        "oil_need", "enum",
        {"cases": [{"when": {"eq": ["normalized.ends_condition", "deutlich_trocken"]}, "then": "yes"}, {"when": {"eq": ["normalized.ends_condition", "leicht_trocken"]}, "then": "maybe"}], "else": "no"},
        "yes | maybe | no",
        "map_slot_rules R10/R18",
        "REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand",
    ),
    (
        "needs_repair_focus", "bool",
        {"or": [{"includes": ["normalized.hair_condition", "stark_geschaedigt"]}, {"eq": ["normalized.hair_treatments", "blondiert"]}]},
        "true | false",
        "map_slot_rules R4/R5/R22/R23; map_pool_filter R2; flags.wants_intense_care",
        "Bond-IQ-Trigger; starke Schaedigung oder Blondierung",
    ),
    (
        "needs_scalp_focus", "bool",
        {"intersects": ["normalized.scalp_status", ["juckend_empfindlich", "schuppig", "trocken"]]},
        "true | false",
        "map_slot_rules R21",
        "Scalp-Comfort-Trigger; problematische Kopfhaut",
    ),
    (
        "needs_lightweight_logic", "bool",
        {"or": [{"eq": ["normalized.hair_thickness", "fein"]}, {"includes": ["normalized.hair_condition", "kraftlos"]}]},
        "true | false",
        "flags.wants_intense_care (POOL-02 gewicht-Filter ist bewusste Luecke)",
        "Negativ-Input fuer wants_intense_care; feines oder kraftloses Haar will nichts Schweres",
    ),
    (
        "needs_curl_care", "bool",
        # GEÄNDERT Migration #15: zusätzlich AND curl_priority != 'glatt'
        {"and": [{"in": ["normalized.hair_structure", ["wellig", "lockig", "kraus"]]}, {"neq": ["normalized.curl_priority", "glatt"]}]},
        "true | false",
        "map_slot_rules R11/R12/R11b; flags.curl_refresh_needed; flags.styling_goal_definition; flags.wants_full_curl_line",
        "Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15)",
    ),
    (
        # NEU Migration #15
        "prefers_straight", "bool",
        {"and": [{"in": ["normalized.hair_structure", ["wellig", "lockig", "kraus"]]}, {"eq": ["normalized.curl_priority", "glatt"]}]},
        "true | false",
        "(noch ohne Sheet-Konsument; Smoothing-Produkte profitieren implizit ueber needs_curl_care=false)",
        "User mit Locken/Wellen, will aber glatt tragen (Migration #15)",
    ),
    (
        "detangling_need", "enum",
        {
            "cases": [
                {"when": {"or": [{"includes": ["normalized.hair_condition", "haarbruch"]}, {"includes": ["normalized.hair_condition", "spliss"]}, {"and": [{"eq": ["normalized.hair_structure", "kraus"]}, {"eq": ["normalized.ends_condition", "deutlich_trocken"]}]}]}, "then": "stark_verfilzt"},
                {"when": {"or": [{"and": [{"includes": ["normalized.hair_condition", "trocken"]}, {"not": {"includes": ["normalized.hair_condition", "haarbruch"]}}]}, {"and": [{"eq": ["normalized.hair_structure", "lockig"]}, {"not": {"includes": ["normalized.hair_condition", "keine_probleme"]}}]}]}, "then": "leicht_verfilzt"},
            ],
            "else": "problemlos",
        },
        "stark_verfilzt | leicht_verfilzt | problemlos",
        "map_slot_rules R9/R19",
        "REQ-07/18; 3-stufige Verfilzungs-Einstufung",
    ),
    (
        "needs_dry_shampoo", "bool",
        {"eq": ["normalized.wash_frequency", "taeglich"]},
        "true | false",
        "map_slot_rules R15",
        "The-Champ-Trigger; taegliches Waschen",
    ),
    (
        "styling_goal_volumen", "bool",
        {"includes": ["normalized.care_goals", "volumen"]},
        "true | false",
        "map_slot_rules R20",
        "Volumen-Ziel aus User-Auswahl",
    ),
    (
        "styling_goal_glanz", "bool",
        {"includes": ["normalized.care_goals", "glanz"]},
        "true | false",
        "map_slot_rules R17",
        "Glanz-Ziel aus User-Auswahl",
    ),
    (
        "styling_goal_halt", "bool",
        {"and": [{"eq": ["normalized.styling_effort", "aufwendiges_styling"]}, {"in": ["normalized.hair_thickness", ["fein", "mittel"]]}, {"in": ["normalized.hair_structure", ["glatt", "wellig"]]}]},
        "true | false",
        "map_slot_rules R16",
        "Moxie-Mousse-Trigger; aufwendiges Styling auf feinem/mittlerem glatten/welligem Haar",
    ),
    # Phase 2 — mit flags.*-Refs
    (
        "curl_refresh_needed", "bool",
        # GEÄNDERT Migration #15: neq 'taeglich' statt eq '1x_pro_woche'
        {"and": [{"neq": ["normalized.wash_frequency", "taeglich"]}, {"eq": ["flags.needs_curl_care", True]}]},
        "true | false",
        "map_slot_rules REQ-13",
        "Curl-Auffrischer-Trigger; alle Wasch-Frequenzen AUSSER taeglich + Locken (Migration #15)",
    ),
    (
        "styling_goal_definition", "bool",
        # GEÄNDERT Migration #15: 'in [mehr_definition, beides]' statt 'eq mehr_definition'
        {"and": [{"eq": ["flags.needs_curl_care", True]}, {"in": ["normalized.curl_priority", ["mehr_definition", "beides"]]}]},
        "true | false",
        "map_conflict_rules R5",
        "Curl-Definition-Trigger; matcht mehr_definition UND beides (Migration #15)",
    ),
    (
        # NEU Migration #15
        "wants_full_curl_line", "bool",
        {"and": [{"eq": ["flags.needs_curl_care", True]}, {"eq": ["normalized.curl_priority", "beides"]}]},
        "true | false",
        "map_slot_rules REQ-11b",
        "User mit Locken wuenscht komplette Curl-Linie (Definition + Volumen+Halt) (Migration #15)",
    ),
    (
        "wants_intense_care", "bool",
        {"or": [{"eq": ["flags.needs_repair_focus", True]}, {"and": [{"eq": ["flags.needs_lightweight_logic", False]}, {"in": ["normalized.hair_treatments", ["gefaerbt", "blondiert"]]}]}]},
        "true | false",
        "Node 12 v4 Stufe 11 (intensitaet-Tiebreaker)",
        "Pflege-Intensitaets-Praeferenz fuer Node-12-Ranking; NEU 2026-06-18",
    ),
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
    print(f"map_derived_variables: {len(grid)-1} Zeilen + Header (Migration #15: 14→{len(grid)-1})")
    new_rules = [r[0] for r in DERIVED_ROWS if 'NEU' in r[5] or 'Migration #15' in r[5]]
    print(f"  Neue/geaenderte Variablen: {new_rules}")

    if not args.commit:
        print("\n(dry-run — mit --commit ausfuehren)")
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
    print(f"\nmap_derived_variables: {len(rows_after)} non-empty rows")
    for i, (planned, actual) in enumerate(zip(grid, rows_after), start=1):
        if planned != actual:
            print(f"  DIFF R{i}: planned={planned}\n          actual ={actual}", file=sys.stderr)
            return 1
    print("  Re-Read: verbatim ✓")

    # 2) produktdatenbank.curl_auffrischer.slot_typ -> styling_3
    update_cell(sh, 'produktdatenbank', 'produkt_key', 'curl_auffrischer', 'slot_typ', 'styling_3')
    after = read_row(sh, 'produktdatenbank', 'produkt_key', 'curl_auffrischer')
    print(f"\nproduktdatenbank.curl_auffrischer.slot_typ = {after.get('slot_typ')!r}")

    # 3) map_slot_rules — diverse Edits
    # 3a) REQ-04: requires_not = REQ-11,REQ-11b
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-04', 'requires_not', 'REQ-11,REQ-11b')
    # 3b) REQ-11: filter nur curl_creme
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-11', 'filter', 'curl_creme')
    # 3c) REQ-11b neu anhaengen
    ws_slot = sh.worksheet('map_slot_rules')
    hdr = ws_slot.row_values(1)
    row_data = {
        'regel_id': 'REQ-11b',
        'slot_typ': 'styling_1',
        'prioritaet': 'required_conditional',
        'trigger_flag': 'wants_full_curl_line',
        'trigger_wert': 'TRUE',
        'trigger_flag2': '',
        'trigger_wert2': '',
        'overrides': '',
        'requires_not': '',
        'filter': 'curl_creme',
        'reason': 'Curl-Creme als primaeres Styling bei Wunsch nach kompletter Curl-Linie (Migration #15)',
        'aktiv': 'TRUE',
    }
    new_row = [row_data.get(h, '') for h in hdr]
    ws_slot.append_row(new_row, value_input_option='RAW')
    # 3d) REQ-12: filter nur curl_gelee, overrides leer
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-12', 'filter', 'curl_gelee')
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-12', 'overrides', '')
    # 3e) REQ-13: slot_typ=styling_3, prioritaet=required_conditional
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-13', 'slot_typ', 'styling_3')
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-13', 'prioritaet', 'required_conditional')
    # 3f) REQ-20: requires_not = REQ-05
    update_cell(sh, 'map_slot_rules', 'regel_id', 'REQ-20', 'requires_not', 'REQ-05')

    # Verifikation
    print(f"\nmap_slot_rules nach Edits:")
    for rid in ('REQ-04', 'REQ-11', 'REQ-11b', 'REQ-12', 'REQ-13', 'REQ-20'):
        r = read_row(sh, 'map_slot_rules', 'regel_id', rid)
        print(f"  {rid:8s} slot={r.get('slot_typ'):12s} prio={r.get('prioritaet'):22s} trigger={r.get('trigger_flag')}={r.get('trigger_wert')} filter={r.get('filter')!r} req_not={r.get('requires_not')!r} overrides={r.get('overrides')!r}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
