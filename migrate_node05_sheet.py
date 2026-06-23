#!/usr/bin/env python3
"""
Schema-Umbau map_derived_variables für Node-05-Migration (2026-06-23).

Alt:  4 Spalten (variable | berechnungslogik | erlaubte_werte | verwendung), 13 Zeilen
      davon 11 Node-05-Einträge (4 fehlend) + 2 Node-06-Einträge (R13/R14 stale)
      berechnungslogik = Freitext-Doku, nicht parsbar
Neu:  6 Spalten (variable | typ | regel_json | erlaubte_werte | konsumenten | doku), 17 Zeilen
      regel_json = JSON.parse-bar (siehe Session-Doku 2026-06-23 für Operator-Inventar)
      Sheet-Reihenfolge = Auswertungs-Reihenfolge: Phase 1 (nur normalized) → Phase 2 (mit flags.*)

Vorbedingung: Backup in backups/sheets_20260623_pre_node05_schema/map_derived_variables.csv.
"""

import argparse
import json
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")

import gspread
from google.oauth2.service_account import Credentials

from sheets_writer import load_env, resolve_sa_path, DOC_ID, SCOPES

TAB = "map_derived_variables"

HEADER = ["variable", "typ", "regel_json", "erlaubte_werte", "konsumenten", "doku"]

# (variable, typ, regel_dict, erlaubte_werte, konsumenten, doku)
ROWS = [
    # ── Phase 1: nur normalized-Refs ──
    (
        "heat_use",
        "enum",
        {"cases": [{"when": {"in": ["normalized.heat_frequency", ["regelmaessig", "sehr_haeufig"]]}, "then": "yes"}], "else": "no"},
        "yes | no",
        "map_slot_rules R6/R11/R12; map_conflict_rules R3; flags.needs_protection_focus",
        "Hitzeschutz-Trigger; haeufige Hitze-Nutzung",
    ),
    (
        "oil_need",
        "enum",
        {"cases": [{"when": {"eq": ["normalized.ends_condition", "deutlich_trocken"]}, "then": "yes"}, {"when": {"eq": ["normalized.ends_condition", "leicht_trocken"]}, "then": "maybe"}], "else": "no"},
        "yes | maybe | no",
        "map_slot_rules R10/R18",
        "REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand",
    ),
    (
        "needs_repair_focus",
        "bool",
        {"or": [{"includes": ["normalized.hair_condition", "stark_geschaedigt"]}, {"eq": ["normalized.hair_treatments", "blondiert"]}]},
        "true | false",
        "map_slot_rules R4/R5/R22/R23; map_pool_filter R2; flags.wants_intense_care",
        "Bond-IQ-Trigger; starke Schaedigung oder Blondierung",
    ),
    (
        "needs_scalp_focus",
        "bool",
        {"intersects": ["normalized.scalp_status", ["juckend_empfindlich", "schuppig", "trocken"]]},
        "true | false",
        "map_slot_rules R21",
        "Scalp-Comfort-Trigger; problematische Kopfhaut",
    ),
    (
        "needs_lightweight_logic",
        "bool",
        {"or": [{"eq": ["normalized.hair_thickness", "fein"]}, {"includes": ["normalized.hair_condition", "kraftlos"]}]},
        "true | false",
        "flags.wants_intense_care (POOL-02 gewicht-Filter ist bewusste Luecke)",
        "Negativ-Input fuer wants_intense_care; feines oder kraftloses Haar will nichts Schweres",
    ),
    (
        "needs_curl_care",
        "bool",
        {"in": ["normalized.hair_structure", ["wellig", "lockig", "kraus"]]},
        "true | false",
        "map_slot_rules R11/R12; flags.curl_refresh_needed; flags.styling_goal_definition",
        "Curl-Produkte-Trigger; nicht-glatte Haarstruktur",
    ),
    (
        "needs_detangling",
        "bool",
        {"or": [{"includes": ["normalized.hair_condition", "haarbruch"]}, {"includes": ["normalized.hair_condition", "spliss"]}, {"and": [{"eq": ["normalized.hair_structure", "kraus"]}, {"truthy": "normalized.ends_condition"}, {"neq": ["normalized.ends_condition", "weich_normal"]}]}]},
        "true | false",
        "(unbenutzt — Cleanup-Kandidat)",
        "Entwirrungs-Trigger; derzeit ohne aktiven Sheet-Konsumenten",
    ),
    (
        "detangling_need",
        "enum",
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
        "needs_dry_shampoo",
        "bool",
        {"eq": ["normalized.wash_frequency", "taeglich"]},
        "true | false",
        "map_slot_rules R15",
        "The-Champ-Trigger; taegliches Waschen",
    ),
    (
        "styling_goal_volumen",
        "bool",
        {"includes": ["normalized.care_goals", "volumen"]},
        "true | false",
        "map_slot_rules R20",
        "Volumen-Ziel aus User-Auswahl",
    ),
    (
        "styling_goal_glanz",
        "bool",
        {"includes": ["normalized.care_goals", "glanz"]},
        "true | false",
        "map_slot_rules R17",
        "Glanz-Ziel aus User-Auswahl",
    ),
    (
        "styling_goal_natuerlich",
        "bool",
        {"and": [{"eq": ["normalized.routine_preference", "minimal"]}, {"eq": ["normalized.styling_effort", "lufttrocknen"]}]},
        "true | false",
        "(unbenutzt — Cleanup-Kandidat)",
        "Natuerlicher Look; derzeit ohne aktiven Sheet-Konsumenten",
    ),
    (
        "styling_goal_halt",
        "bool",
        {"and": [{"eq": ["normalized.styling_effort", "aufwendiges_styling"]}, {"in": ["normalized.hair_thickness", ["fein", "mittel"]]}, {"in": ["normalized.hair_structure", ["glatt", "wellig"]]}]},
        "true | false",
        "map_slot_rules R16",
        "Moxie-Mousse-Trigger; aufwendiges Styling auf feinem/mittlerem glatten/welligem Haar",
    ),
    # ── Phase 2: mit flags.*-Refs ──
    (
        "needs_protection_focus",
        "bool",
        {"or": [{"eq": ["flags.heat_use", "yes"]}, {"in": ["normalized.hair_treatments", ["gefaerbt", "blondiert"]]}]},
        "true | false",
        "(unbenutzt — Cleanup-Kandidat)",
        "Hitze-/Chemie-Schutz-Trigger; derzeit ohne aktiven Sheet-Konsumenten",
    ),
    (
        "curl_refresh_needed",
        "bool",
        {"and": [{"eq": ["normalized.wash_frequency", "1x_pro_woche"]}, {"eq": ["flags.needs_curl_care", True]}]},
        "true | false",
        "map_slot_rules R14",
        "Curl-Auffrischer-Trigger; seltenes Waschen + Locken",
    ),
    (
        "styling_goal_definition",
        "bool",
        {"and": [{"eq": ["flags.needs_curl_care", True]}, {"eq": ["normalized.curl_priority", "mehr_definition"]}]},
        "true | false",
        "map_conflict_rules R5",
        "Curl-Definition-Trigger fuer Locken mit Definitionswunsch",
    ),
    (
        "wants_intense_care",
        "bool",
        {"or": [{"eq": ["flags.needs_repair_focus", True]}, {"and": [{"eq": ["flags.needs_lightweight_logic", False]}, {"in": ["normalized.hair_treatments", ["gefaerbt", "blondiert"]]}]}]},
        "true | false",
        "Node 12 v4 Stufe 11 (intensitaet-Tiebreaker)",
        "Pflege-Intensitaets-Praeferenz fuer Node-12-Ranking; NEU 2026-06-18",
    ),
]


def build_grid():
    grid = [HEADER]
    for var, typ, regel, erlaubt, konsum, doku in ROWS:
        grid.append([var, typ, json.dumps(regel, ensure_ascii=False), erlaubt, konsum, doku])
    return grid


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--commit", action="store_true", help="Schreibe ins Sheet. Ohne diesen Flag: dry-run.")
    args = ap.parse_args()

    grid = build_grid()
    print(f"Plan: {len(grid)-1} Zeilen + Header in Tab '{TAB}'")
    print(f"Header: {grid[0]}")
    print("Stichproben:")
    for i in (1, 2, 8, 14, 17):
        if i < len(grid):
            r = grid[i]
            print(f"  R{i+1:02d} {r[0]:30s} typ={r[1]:5s} regel_len={len(r[2])} konsumenten='{r[4]}'")

    if not args.commit:
        print("\n(dry-run — nichts geschrieben. Mit --commit ausfuehren.)")
        return 0

    base = Path.cwd()
    env = load_env(base / ".env")
    sa = resolve_sa_path(env, base)
    creds = Credentials.from_service_account_file(str(sa), scopes=SCOPES)
    gc = gspread.authorize(creds)
    sh = gc.open_by_key(DOC_ID)
    ws = sh.worksheet(TAB)

    ws.clear()
    end_col = chr(ord("A") + len(HEADER) - 1)
    ws.update(f"A1:{end_col}{len(grid)}", grid, value_input_option="RAW")

    rows_after = ws.get_all_values()
    print(f"\nWrote {len(grid)} rows ({len(HEADER)} cols). Sheet now has {len(rows_after)} rows.")
    if len(rows_after) != len(grid):
        print("WARN: row-count mismatch", file=sys.stderr)
        return 1
    for i, (planned, actual) in enumerate(zip(grid, rows_after), start=1):
        if planned != actual:
            print(f"DIFF R{i}: planned={planned}\n        actual ={actual}", file=sys.stderr)
            return 1
    print("Re-Read: all rows verbatim.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
