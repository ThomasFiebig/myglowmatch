# HANDOVER — Stand 2026-05-28

Faktische Momentaufnahme des MONAT-Haaranalyse-Systems. Kein Verlauf, keine Diskussion.

## System-Identifikation

| Element | Wert |
|---|---|
| n8n-Instanz | `https://veradex.app.n8n.cloud` |
| Workflow | `MONAT Haarpflege-Beratungssystem v1.0`, aktiv |
| Workflow-ID | `pwSWA5NatKiLhueB` |
| Webhook-URL | `https://veradex.app.n8n.cloud/webhook/glowmatch-haaranalyse` |
| Tally-Signatur (Header `x-tally-signature`) | `acf86723-a18d-4418-8788-cf5c5a4eaf54` |
| Webhook-Response-Mode | `onReceived` (Frontend bekommt sofort `{"message":"Workflow was started"}`) |
| Google-Sheet-Doc-ID | `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A` |
| Sheet-Name | `MONAT_Produktdatenbank_KOMPLETT` |
| Google-Sheets-Credential-ID (n8n) | `zf5b37nhm7NZArlz` |

## Repo & Verzeichnisse

| Pfad | Inhalt |
|---|---|
| `/Users/thomasfiebig/Projekte/myglowmatch/` | Git-Repo (Branch `main`), Next.js-Frontend + Test-Suite |
| `~/myglowmatch/chat-archive/` | Session-Dokus |
| `~/myglowmatch/produktdatenblaetter/` | 37 Hersteller-PDFs, benannt nach `produkt_key.pdf` + `_produktliste_uebersicht.pdf` + `produkte_index.md` |
| `~/myglowmatch/map_*.csv` | Import-Vorlagen der bisherigen Sheet-Migrationen |
| `~/myglowmatch/workflow_backup_*.json` | Pre-PUT-Backups |
| `/Users/thomasfiebig/Projekte/myglowmatch/.env` | `N8N_API_KEY`, `N8N_BASE_URL` (gitignored) |
| `/Users/thomasfiebig/Projekte/myglowmatch/test_suite.py` | Test-Runner über Execution-API |
| `/Users/thomasfiebig/Projekte/myglowmatch/inspect_workflow.py` | Read-only Workflow-Inspektor |

## Google-Sheet-Tabs

| Tab | Spalten / Zweck | Genutzt von |
|---|---|---|
| `MONAT_Produktdatenbank_KOMPLETT` | 37 Produkte × 24 Spalten (produkt_key, produktname_de, produktlinie, produkttyp, slot_typ, routine_schritt, kopfhaut, haarstruktur, haarstaerke, haarzustand, hauptfunktion, nebenfunktionen, pflegelevel, ausschluss_bei, ist_hitzeschutz, ist_bonding, ist_scalp_focus, locken_geeignet, kombinationen, kombi_optional, aktiv, produkt_url, anwendung, row_number) | Node 07 |
| `map_priorities` | scalp/condition-Priorisierung (Long-Format, Spalten: regel_id, kategorie, wert, reihenfolge, aktiv, beschreibung) | Node 04a |
| `map_pflegelevel_scoring` | Punktevergabe-Regeln pro Profilfeld | Node 06a |
| `map_pflegelevel_overrides` | Floor/Cap-Regeln (PFL-OV-01 bis PFL-OV-04) | Node 06b |
| `map_max_products` | 2D-Lookup `routine_preference × pflegelevel → max_products` | Node 06c |
| `map_slot_rules` | REQ-Regeln (25 aktive Regeln, Trigger + Filter) | Node 10 |
| `map_conflict_rules` | CON-Regeln (CON-01 bis CON-12), match_typ + action | Node 13 |
| `map_pool_filter` | POOL-01 (Bonding) und POOL-03 (Locken-Styling). POOL-02 (Gewicht) bewusste Lücke. | Node 08a |
| Log-Tab | Run-Log (von Node 19 geschrieben) | Node 19 |

## Workflow-Nodes (25)

Datenflussreihenfolge (Hauptpfad):

| # | Name | Typ | Funktion |
|---|---|---|---|
| 1 | Webhook | webhook | Tally-Endpunkt |
| 2 | Signature prüfen | if | `x-tally-signature` validieren |
| 3 | 02 Felder extrahieren | code | Tally-JSON in flache Felder |
| 4 | 03 Werte normieren | code | 13 Aliase-Maps (Tally → Workflow-Vokabular), 160 LOC |
| 5 | 04a Prioritäten laden | googleSheets | `map_priorities` |
| 6 | 04 Prioritäten auflösen | code | scalp_primary/secondary, condition_primary/secondary, generischer Auswerter |
| 7 | 05 Bool-Flags berechnen | code | 17 Heuristik-Flags (needs_repair_focus, needs_lightweight_logic …), 69 LOC, **noch inline** |
| 8 | 06a Pflegelevel-Scoring laden | googleSheets | `map_pflegelevel_scoring` |
| 9 | 06b Pflegelevel-Overrides laden | googleSheets | `map_pflegelevel_overrides` |
| 10 | 06c Max-Products laden | googleSheets | `map_max_products` |
| 11 | 06 Pflegelevel berechnen | code | Phase 1+3 (Scoring), Phase 2 (Ziele-Bonus, **noch inline**), Phase 4+5+6 sheet-getrieben |
| 12 | 07 Produktdatenbank laden | googleSheets | Hauptpool 37 Produkte |
| 13 | 08a Pool-Filter laden | googleSheets | `map_pool_filter` |
| 14 | 08 Ausschluss-Filter | code | aktiv/produkt_key-Sanity, `ausschluss_bei`, `haarstaerke`, Pool-Regeln aus 08a, `pflegelevel`-Filter |
| 15 | 09 Pool validieren | code | Sanity-Check (Pool nicht leer) |
| 16 | 10 map_slot_rules | googleSheets | REQ-Regeln |
| 17 | 11 REQ-Regeln auswerten | code | Slot-Trigger-Auswertung, generisch; Z. 163-164 `minimal → optional = []` **noch inline** |
| 18 | 13 Konfliktregeln laden | googleSheets | `map_conflict_rules` |
| 19 | 14 Konflikte auflösen | code | match_typ ∈ {produkt_key, produktlinie, key_contains}; `gewicht_eq` entfernt |
| 20 | 12 Scoring & Slot-Befüllung | code | Score-Gewichte 3/2/1 **noch inline**, generischer Filter (Boolean-Flags + Substring) |
| 21 | 15 Routine sortieren | code | Finale Routine, Reihenfolge + Pflichtproduktauswahl |
| 22 | 17 Claude E-Mail formulieren | code | Templating, 517 LOC, CSS inline (mobile + desktop) |
| 23 | 18 E-Mail senden | emailSend | An Kunde (`info@myglowmatch.de` in Tests) |
| 24 | 18b Partner-Mail senden | emailSend | An Partner |
| 25 | 19 Log speichern | googleSheets | Anhang an Log-Tab |

Sticky Notes zählen nicht. Mail-Routing zwischen 18 und 18b geht aus Code-Quelle Node 17 hervor (kein eigener Router-Node).

## Migrationsstand

| Migration | Was | Sheet-Tab | Code-Status |
|---|---|---|---|
| #1 | Prioritäten (scalp/condition) | `map_priorities` | Node 04 generisch |
| #2 | Filter-Spezialfälle | (keine neue Sheet) | Node 12 generisch (Boolean-Regex-Parser); `ir_clinical_serum`-Special-Case entfernt (toter Code) |
| #3 | Pflegelevel Phase 4+5 | `map_pflegelevel_overrides` | Node 06 Phase 4+5 generisch |
| #4 | Pflegelevel Phase 6 | `map_max_products` | Node 06 Phase 6 generisch (2D-Lookup) |
| #5 | Pool-Filter | `map_pool_filter` | Node 08 generisch (Profil- + Produkt-Bedingungen); Inline-Filter Bonding/Gewicht/Locken entfernt; `gewicht_eq`-Case aus Node 14 entfernt |

Mini-Syntax in `map_pool_filter` und `map_pflegelevel_overrides`-ähnlichen Tabs:
- Bedingungen mit `;` getrennt, Liste `feld:operator[:wert]`
- Operatoren: `=`, `!=`, `is_true`, `is_false`, `in`, `not_in`
- Listenwerte bei `in`/`not_in` mit `|` getrennt
- Profil-Pfade: `flags.<feld>`, `normalized.<feld>`, `pflegelevel.<feld>`

## Offene Punkte (priorisiert)

| Prio | Aufgabe | Stelle |
|---|---|---|
| 🟡 | Datenblatt-Provenienz-Audit | 37 Produkte × ~15 audit-relevante Spalten gegen `~/myglowmatch/produktdatenblaetter/` |
| 🟡 | Node 06 Phase 2 migrieren (Ziele-Bonus, max +2 Pkt) | Node 06 inline |
| 🟡 | Node 05 migrieren (17 Bool-Flag-Heuristiken) | Node 05 inline, 69 LOC; bei Gelegenheit `needs_lightweight_logic` mitentfernen (seit #5 ungenutzt) |
| 🟢 | Node 11 Z. 163-164: `minimal → optional = []` als REQ-Regel ins Sheet | Node 11 inline |
| 🟢 | Node 12 Score-Gewichte (6 Inline-Werte 3/2/1) optional in `map_scoring_weights` | Node 12 inline |
| 🟢 | `extract_routine_output()`-Workaround in Test-Suite aufräumen | `test_suite.py` (CONFLICT_NODE-Merge seit Pass-Through in Node 12 überflüssig) |
| 🟢 | Sheet-Spalte `gewicht` in Produktdatenbank löschen | (vermutlich bereits leer/weg — Google-Sheets-API liefert sie nicht mehr aus) |
| 🟢 | Sheet-Loader 06a/06b/06c parallelisieren | Performance-Tuning, nur falls Live-Latenz spürbar |

## Referenzprofile (Soll-Werte für Regression)

Test-Profile in `test_suite.py`, alle mit `partner_id=desiree`, `email=info@myglowmatch.de`, `consent_recommendation=true`, `consent_marketing=false`.

| Profil | Eingabe-Kurzform | Pflegelevel | Pkt | Cap | Count | CON-Regeln |
|---|---|---|---|---|---|---|
| anna   | glatt, mittel, keine_probleme, unbehandelt, Hitze gelegentlich, minimal | LOW | 0 | 3 | 1 | CON-07 |
| maria  | wellig, fein, duenn, kraftlos, gefaerbt, Hitze nie, ausgewogen | MID | 7 | 5 | 5 | CON-09, CON-11, CON-12 |
| lena   | kraus, dick, trocken, frizz, gefaerbt, Hitze sehr_haeufig, bestmoeglich | HIGH | 15 | 10 | 7 | CON-09, CON-11 |
| julia  | glatt, fein, kraftlos, unbehandelt, Hitze gelegentlich, ausgewogen | MID | 4 | 5 | 5 | CON-07, CON-12 |
| bianca | wellig, mittel, trocken, gefaerbt, Hitze gelegentlich, ausgewogen | MID | 7 | 5 | 5 | CON-02, CON-09 |
| vivien | wellig, dick, keine_probleme, gefaerbt, Hitze regelmaessig, bestmoeglich | MID | 4 | 7 | 7 | CON-09, CON-11, CON-12 |
| sarah  | lockig, fein, stark_geschaedigt+spliss+trocken, blondiert, Hitze sehr_haeufig, bestmoeglich | HIGH | 18 | 10 | 8 | CON-09, CON-11 |

## Test-Suite

Aufrufe:
- `python3 test_suite.py --profile anna` — Einzelprofil
- `python3 test_suite.py` — alle 7 Profile sequenziell
- `python3 test_suite.py --save` — zusätzlich Ergebnis als `test_results_<ts>.json`
- `python3 test_suite.py --verbose` — mehr Details

Härtungsstand (seit Session 3):
- `DEFAULT_MAX_WAIT = 90` (90 s Polling-Limit pro Profil)
- `TERMINAL_STATUSES = ("success",)` — Error-Executions nicht mehr als gültig akzeptiert
- `first_name`-Verifikation in `fetch_latest_execution()` — kein Profil-Mix-Up bei Latenz

Pipeline-Latenz aktuell ~38–47 s pro Profil (5 Sheet-Loader: 04a, 06a, 06b, 06c, 08a).

## n8n REST API — Operationsregeln

PUT `/api/v1/workflows/{id}` Body-Whitelisting:
- Top-Level: nur `name`, `nodes`, `connections`, `settings`
- `settings` darf nur enthalten: `saveExecutionProgress`, `saveManualExecutions`, `saveDataErrorExecution`, `saveDataSuccessExecution`, `executionTimeout`, `errorWorkflow`, `timezone`, `executionOrder`
- Aktueller Workflow nutzt davon nur `executionOrder`
- Read-only Felder (`id`, `versionId`, `createdAt`, `updatedAt`, `active`, `tags`, `triggerCount`, `pinData`, `meta`, `shared`, `isArchived`, `staticData` etc.) müssen aus dem Body raus
- `active`-State bleibt nach PUT erhalten
- Vor jedem PUT: GET → Backup als `~/myglowmatch/workflow_backup_<ts>_<kontext>.json`
- Eventually Consistency der Execution-Liste: Polling über `since_id > baseline_id` (nicht `since_ts`)

Neuer Sheet-Loader-Node — Pflichtfelder:
```json
{
  "id": "<uuid>",
  "name": "<Nr><Suffix> <Beschreibung>",
  "type": "n8n-nodes-base.googleSheets",
  "typeVersion": 4.7,
  "position": [x, y],
  "parameters": {
    "documentId": {"__rl": true, "value": "<doc-id>", "mode": "list", ...},
    "sheetName": {"__rl": true, "value": "<tab-name>", "mode": "name"},
    "options": {}
  },
  "credentials": {"googleSheetsOAuth2Api": {"id": "zf5b37nhm7NZArlz", "name": "Google Sheets OAuth2 API"}}
}
```

Loader-Position-Konvention: oberhalb des Hauptflusses (Hauptfluss `y=144`, Loader `y≈-176`).

Code-Node-Zugriffspattern wenn Loader zwischen Producer und Consumer liegt:
- Sheet-Daten: `$items("<loader-name>")`
- Produkt-/Profil-Daten vom Vorgänger: `$node["<name>"].json` oder `$items("<name>")` statt `$input.all()`

## Bewusste Lücken

- `POOL-02` in `map_pool_filter` fehlt absichtlich (Gewicht-Regel war Bauchgefühl ohne Datenblatt-Beleg, bei Migration #5 entfernt)
- Spalte `gewicht` in Produktdatenbank — entweder leer oder bereits gelöscht (Sheets-API liefert sie nicht aus)
- `needs_lightweight_logic` in Node 05 wird seit Migration #5 von keinem Konsumenten mehr gelesen, bleibt aber bis zur Node-05-Migration berechnet
