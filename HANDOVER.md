# HANDOVER — Stand 2026-06-24

Faktische Momentaufnahme des MONAT-Haaranalyse-Systems. Kein Verlauf, keine Diskussion.

## System-Identifikation

| Element | Wert |
|---|---|
| n8n-Instanz | `https://veradex.app.n8n.cloud` |
| Workflow | `MONAT Haarpflege-Beratungssystem v1.0`, aktiv |
| Workflow-ID | `pwSWA5NatKiLhueB` |
| Webhook-URL | `https://veradex.app.n8n.cloud/webhook/glowmatch-haaranalyse` |
| Webhook-Secret (Header `x-glowmatch-secret`) | siehe `.env` / `.env.local` als `N8N_WEBHOOK_SECRET` (rotierbar) |
| Webhook-Response-Mode | `onReceived` (Frontend bekommt sofort `{"message":"Workflow was started"}`) |
| Google-Sheet-Doc-ID | `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A` |
| Sheet-Name | `MONAT_Produktdatenbank_KOMPLETT` |
| Google-Sheets-Credential-ID (n8n) | `zf5b37nhm7NZArlz` |

## Repo & Verzeichnisse

| Pfad | Inhalt |
|---|---|
| `/Users/thomasfiebig/Projekte/myglowmatch/` | Git-Repo (Branch `main`), Next.js-Frontend + Test-Suite |
| `~/Projekte/myglowmatch/chat-archive/` | Session-Dokus |
| `~/Projekte/myglowmatch/produktdatenblaetter/` | 37 Hersteller-PDFs, benannt nach `produkt_key.pdf` + `_produktliste_uebersicht.pdf` + `produkte_index.md` |
| `~/Projekte/myglowmatch/map_*.csv` | Import-Vorlagen der bisherigen Sheet-Migrationen |
| `~/Projekte/myglowmatch/workflow_backup_*.json` | Pre-PUT-Backups |
| `/Users/thomasfiebig/Projekte/myglowmatch/.env` | `N8N_API_KEY`, `N8N_BASE_URL` (gitignored) |
| `/Users/thomasfiebig/Projekte/myglowmatch/test_suite.py` | Test-Runner über Execution-API |
| `/Users/thomasfiebig/Projekte/myglowmatch/inspect_workflow.py` | Read-only Workflow-Inspektor |

## Google-Sheet-Tabs

**Wichtig:** `MONAT_Produktdatenbank_KOMPLETT` ist der **Sheet-Dokumenten-Name** (Doc-ID `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A`), nicht ein Tab-Name. Tabs werden im Code per Loader-Node mit ihrem exakten Namen referenziert.

### Vom aktuellen Workflow genutzte Tabs (10)

| Tab | Spalten / Zweck | Genutzt von |
|---|---|---|
| `produktdatenbank` | 37 Produkte × 25 Spalten (produkt_key, produktname_de, produktlinie, produkttyp, slot_typ, routine_schritt, kopfhaut, haarstruktur, haarstaerke, haarzustand, hauptfunktion, nebenfunktionen, pflegelevel, ausschluss_bei, ist_hitzeschutz, ist_bonding, ist_scalp_focus, locken_geeignet, kombinationen, kombi_optional, aktiv, produkt_url, anwendung, **intensitaet** (NEU 2026-06-18, Werte `leicht`/`intensiv`/`alle`), row_number) | Node 07 |
| `map_priorities` | scalp/condition-Priorisierung (Long-Format, Spalten: regel_id, kategorie, wert, reihenfolge, aktiv, beschreibung) | Node 04a |
| `map_pflegelevel_scoring` (Schema-Erw. 2026-06-24) | 23 Punktevergabe-Regeln, 9 Spalten (`regel_id \| kategorie \| bedingung_typ \| bedingung_feld \| bedingung_wert \| punkte \| max_punkte \| beschreibung \| aktiv`). Operatoren: `equals` / `in_list` / `array_contains` (Match → fixe Punkte) und `array_count_except` (count × punkte, gecappt auf `max_punkte`). PFL-23 (Migration #10) ist erste aggregate-Regel. | Node 06a |
| `map_pflegelevel_overrides` | Floor/Cap-Regeln (PFL-OV-01 bis PFL-OV-04) | Node 06b |
| `map_max_products` | 2D-Lookup `routine_preference × pflegelevel → max_products` | Node 06c |
| `map_profil_funktion` (NEU 2026-06-16) | Profil-Sprache → Wirkungs-Sprache (z.B. `hair_condition=trocken → feuchtigkeit`). 9 Mappings für `hair_condition`. Behebt das Vokabular-Gap für Node-12-Stufe-1. | Node 06d → Node 12 |
| `map_slot_rules` | REQ-Regeln (25 aktive Regeln, Trigger + Filter) | Node 10 |
| `map_conflict_rules` | CON-Regeln (CON-01 bis CON-12), match_typ + action | Node 13 |
| `map_pool_filter` | POOL-01 (Bonding) und POOL-03 (Locken-Styling). POOL-02 (Gewicht) bewusste Lücke. | Node 08a |
| `map_derived_variables` (umgebaut 2026-06-23, Cleanup 2026-06-24) | 14 JSON-Regeln für Bool-/Enum-Flags (`variable \| typ \| regel_json \| erlaubte_werte \| konsumenten \| doku`). Phase 1 R02-R12 nur `normalized.*`-Refs, Phase 2 R13-R15 mit `flags.*`-Refs auf vorherige Zeilen. Sheet-Reihenfolge = Auswertungs-Reihenfolge. | Node 05a → Node 05 |
| `beratungs_log` | Run-Log (1196 Zeilen Stand 2026-06-10) | Node 19 |

### Nicht vom Workflow geladene Tabs (4) — Audit 2026-06-10, `map_derived_variables` entfernt 2026-06-23 (jetzt live)

Beim Service-Account-Setup am 2026-06-10 sichtbar geworden, am selben Tag auditiert. **Alle 5 sind 0-Hit im Workflow-JSON** (Grep im neuesten Backup, Sanity-Check via Loader-Tabs 4–10 Hits). Inhalts-Status pro Tab:

| Tab | Zeilen | Header | Status | Folge-Aktion |
|---|---|---|---|---|
| `map_input_normalization` | 10 | `feld \| rohwert \| technischer_wert \| hinweis` | **verwaist (Migration entfallen)** — Tally-Pfad ist tot; Frontend liefert technische Werte direkt. Node 03 am 2026-06-10 entfernt statt migriert. | Bei nächster Bereinigung archivieren/löschen |
| `map_requirement_rules` | 19 | `regel_id \| bedingung \| action \| slot_typ \| filter \| beschreibung` | **verwaist (Vorgänger)** — gleiche Struktur wie Live-`map_slot_rules` (25 Regeln), aber älter/kürzer | Bei nächster Bereinigung archivieren/löschen |
| `map_priority_resolution` | 15 | `feld \| rang \| wert \| beschreibung` | **verwaist (Vorgänger)** — 4-Spalten-Variante; Live-`map_priorities` hat 6 Spalten | Bei nächster Bereinigung archivieren/löschen |
| `map_system_dictionary` | 25 | `feld \| technischer_wert \| anzeige_text \| kategorie` | **verwaist, latent nützlich** — Reverse-Lookup technisch→deutsch (z.B. `juckend_empfindlich → "juckend / empfindlich"`) | Liegenlassen (K-05). Für Output-Lokalisierung oder Frontend-Anzeige reaktivierbar |

**Migration #9 abgeschlossen 2026-06-23**: Node 05 (17 Bool-/Enum-Flags) auf `map_derived_variables` umgestellt. Sheet-Format-Umbau auf 6 Spalten + JSON.parse-bares `regel_json` vorab erledigt, Node 05 jsCode auf generischen Evaluator umgebaut, 0/36 Slot-Drift bestätigt. `map_input_normalization`-Migration wurde am 2026-06-10 verworfen: Frontend sendet bereits technische Werte, Node 03 war im Wesentlichen ein No-Op über Tally-Legacy-Maps → komplett entfernt statt migriert.

## Workflow-Nodes (26)

Datenflussreihenfolge (Hauptpfad):

| # | Name | Typ | Funktion |
|---|---|---|---|
| 1 | Webhook | webhook | POST-Endpunkt; Response-Mode `onReceived` (Browser bekommt sofort `{"message":"Workflow was started"}`) |
| 2 | Signature prüfen | if | `x-glowmatch-secret` gegen `N8N_WEBHOOK_SECRET` validieren (Expression `={{ $json.headers['x-glowmatch-secret'] }}`); true → Hauptpfad, false → Pipeline endet still (Eindringling sieht keine Differenz im Webhook-Response) |
| 3 | 02 Felder extrahieren | code | Body in flache Felder, Defaults (`'glatt'`/`'mittel'` u.a.), Array-Dedup; Output `{ normalized, raw_input, partner_id }`. Frontend liefert bereits technische Werte. |
| 4 | 04a Prioritäten laden | googleSheets | `map_priorities` |
| 5 | 04 Prioritäten auflösen | code | scalp_primary/secondary, condition_primary/secondary, generischer Auswerter; liest aus `$node["02 Felder extrahieren"]` |
| 6 | **05a map_derived_variables laden** (NEU 2026-06-23) | googleSheets | **`map_derived_variables`** — 14 JSON-Regeln |
| 7 | 05 Bool-Flags berechnen | code | **Generischer JSON-Regel-Evaluator** (Migration #9, deployed 2026-06-23; Cleanup-Welle 2026-06-24): 90 LOC. Liest `map_derived_variables` via `$items("05a …")`, evaluiert `regel_json` pro Zeile in Sheet-Reihenfolge, baut `flags`-Objekt. Output-Shape unverändert `{ normalized, priorities, flags }`. 14 Flags: 11 Phase-1 (heat_use, oil_need, needs_repair_focus, needs_scalp_focus, needs_lightweight_logic, needs_curl_care, detangling_need, needs_dry_shampoo, styling_goal_volumen, styling_goal_glanz, styling_goal_halt), 3 Phase-2 (curl_refresh_needed, styling_goal_definition, `wants_intense_care` für Node 12 v4 Stufe 11). 4 Flags eliminiert wegen 0 Konsumenten: `volume_sensitivity` (byte-identisches Duplikat zu `needs_lightweight_logic`, 2026-06-23) + `needs_detangling`/`styling_goal_natuerlich`/`needs_protection_focus` (Cleanup-Welle 2026-06-24). |
| 8 | 06a Pflegelevel-Scoring laden | googleSheets | `map_pflegelevel_scoring` |
| 9 | 06b Pflegelevel-Overrides laden | googleSheets | `map_pflegelevel_overrides` |
| 10 | 06c Max-Products laden | googleSheets | `map_max_products` |
| 11 | **06d Profil-Funktion-Mapping laden** | googleSheets | **`map_profil_funktion`** (NEU 2026-06-16) — Profil-Sprache → Wirkungs-Sprache |
| 12 | 06 Pflegelevel berechnen | code | **v4 (deployed 2026-06-24, Migration #10)**: vollständig sheet-getrieben. Phase 1+2 via `map_pflegelevel_scoring` (Operator `array_count_except` mit `max_punkte`-Cap für PFL-23 Ziele-Bonus), Phase 3 Schwellen (LOW/MID/HIGH) als System-Parameter im Code, Phase 4+5 via `map_pflegelevel_overrides`, Phase 6 via `map_max_products`. |
| 13 | 07 Produktdatenbank laden | googleSheets | Hauptpool 37 Produkte |
| 14 | 08a Pool-Filter laden | googleSheets | `map_pool_filter` |
| 15 | 08 Ausschluss-Filter | code | aktiv/produkt_key-Sanity, `ausschluss_bei`, `haarstaerke`, Pool-Regeln aus 08a, `pflegelevel`-Filter |
| 16 | 09 Pool validieren | code | Sanity-Check (Pool nicht leer) |
| 17 | 10 map_slot_rules | googleSheets | REQ-Regeln |
| 18 | 11 REQ-Regeln auswerten | code | **v2 (deployed 2026-06-24, Migration #11)**: vollständig sheet-getrieben. Phase 4 baut Slot-Listen aus `prioritaet ∈ {required_always, required_conditional, optional}`-Regeln. Phase 5 (NEU) wertet Side-Effect-Regeln aus: `prioritaet=suppress_optional` (`REQ-MIN-NO-OPT`) leert `slots.optional` wenn `routine_preference=minimal`. Inline-Block raus. |
| 19 | 13 Konfliktregeln laden | googleSheets | `map_conflict_rules` |
| 20 | 14 Konflikte auflösen | code | match_typ ∈ {produkt_key, produktlinie, key_contains}; `gewicht_eq` entfernt |
| 21 | 12 Scoring & Slot-Befüllung | code | **Ranking-Hierarchie v4** (deployed 2026-06-18): 11 Stufen lexikographisch + alphabetischer Determinismus-Fallback. Liest `map_profil_funktion` (hauptfunktion-Mapping) + Sheet-Spalte `intensitaet`. Profil-Heuristik `flags.wants_intense_care` aus Node 05. Output enthält `profile` (11 Match-Felder), `decision_stage`, `wants_intense`, `ranking_top5`. v3 (2026-06-17): +haarzustand_primary/coverage, +haarstruktur_exakt, +haarstaerke_exakt, +wildcard_alle (10 Stufen). v4: +Stufe 11 intensitaet. |
| 22 | 15 Routine sortieren | code | Finale Routine, Reihenfolge + Pflichtproduktauswahl |
| 23 | 17 Claude E-Mail formulieren | code | Templating, 517 LOC, CSS inline (mobile + desktop); liest `raw_input` aus `$node["02 Felder extrahieren"]` |
| 24 | 18 E-Mail senden | emailSend | An Kunde (`info@myglowmatch.de` in Tests) |
| 25 | 18b Partner-Mail senden | emailSend | An Partner |
| 26 | 19 Log speichern | googleSheets | Anhang an Log-Tab |

Hinweis: ehemals Node `03 Werte normieren` (160 LOC, 14 Tally-Aliase-Maps) am 2026-06-10 entfernt — Frontend liefert technische Werte direkt, Maps waren idempotent / toter Code. Logik-Reste (Defaults `'glatt'`/`'mittel'`, Array-Dedup, `{ normalized, raw_input, partner_id }`-Output) sind in Node 02 zusammengeführt.

Sticky Notes zählen nicht. Mail-Routing zwischen 18 und 18b geht aus Code-Quelle Node 17 hervor (kein eigener Router-Node).

## Migrationsstand

| Migration | Was | Sheet-Tab | Code-Status |
|---|---|---|---|
| #1 | Prioritäten (scalp/condition) | `map_priorities` | Node 04 generisch |
| #2 | Filter-Spezialfälle | (keine neue Sheet) | Node 12 generisch (Boolean-Regex-Parser); `ir_clinical_serum`-Special-Case entfernt (toter Code) |
| #3 | Pflegelevel Phase 4+5 | `map_pflegelevel_overrides` | Node 06 Phase 4+5 generisch |
| #4 | Pflegelevel Phase 6 | `map_max_products` | Node 06 Phase 6 generisch (2D-Lookup) |
| #5 | Pool-Filter | `map_pool_filter` | Node 08 generisch (Profil- + Produkt-Bedingungen); Inline-Filter Bonding/Gewicht/Locken entfernt; `gewicht_eq`-Case aus Node 14 entfernt |
| #6 | Node 03 entfernen (statt migrieren) | `map_input_normalization` verwaist | Node 03 gelöscht (Tally-Maps = toter Code); Logik-Reste in Node 02 (Defaults, Dedup, `normalized`-Output); Frontend-Edit `mehr_dichte → verdichtend` (questions.ts) fixt 🟡-Goal-Match |
| #7 | Node 12 Scoring auf Ranking-Hierarchie | `map_profil_funktion` (NEU) | Node 12 v2 (deployed 2026-06-16): Punkte-Scoring durch lexikographische 6-Stufen-Hierarchie ersetzt. Loader 06d hinzugefügt. Behebt Vokabular-Gap Profil-Sprache↔Wirkungs-Sprache (vorher: SCO-01 toter Code, 25 % Tie-Breaking via Sheet-Reihenfolge). 0/7 Routing-Drift bei 7 Test-Profilen, Erklärbarkeit pro Slot via `decision_stage`-Trace. |
| #8 | Node 12 v3+v4 — Filter-Spalten als Ranking-Stufen, Pflege-Intensitäts-Tiebreaker | Sheet-Spalte `intensitaet` (NEU 2026-06-18 in `produktdatenbank`) | **Node 12 v3** (deployed 2026-06-17): 6 → 10 Stufen. Reaktiviert haarzustand+haarstruktur+haarstaerke als eigene Ranking-Stufen (vorher scoring-tot per K-05). Reihenfolge: 1 hauptfunktion → 2 haarzustand_primary → 3 goal_coverage → 4 scalp_match → 5 curl_compat → 6 haarstruktur_exakt → 7 pflegelev_match → 8 haarstaerke_exakt → 9 haarzustand_coverage → 10 wildcard_alle. Drift 4/7 (Lena/Bianca/Vivien maske replenish→super_feuchtigkeitsmaske via Stufe 6; Julia styling_1 moxie_mousse→volumen_spray via Stufe 8). Alphabetischer Fallback 10/39 → 5/39 (halbiert). **Node 12 v4** (deployed 2026-06-18): +Stufe 11 `intensitaet`. Profil-Heuristik `wants_intense_care = needs_repair_focus \|\| (!needs_lightweight_logic && hair_treatments ∈ {gefaerbt, blondiert})` in Node 05. Sheet-Werte `leicht`/`intensiv`/`alle` (Default), PDF-belegt per K-08 für 8 Tie-Produkte: feuchtigkeits_shampoo/erweiterte_feuchtigkeit_spuelung/entwirrungsspray/kopfhaut_peeling=`leicht`; renew_shampoo/renew_spuelung/rejuvabeads/scalp_comfort_behandlung=`intensiv`. Drift v3→v4: 1/7 (Bianca shampoo+spuelung feuchtigkeits→renew, fachlich richtig wegen gefaerbt). **Alphabetischer Fallback 5/39 → 0/39** — jede Slot-Entscheidung ist jetzt fachlich begründet. |
| #9 | **Node 05 Bool-Flags Sheet-getrieben** (deployed 2026-06-23, Cleanup 2026-06-24) | `map_derived_variables` (Schema-Umbau 4→6 Spalten, 13→17→14 Einträge, parsbares JSON-Regel-Format) + neuer Loader-Node `05a` | **Node 05 v2** (deployed 2026-06-23): 76 LOC inline → 90 LOC JSON-Regel-Evaluator. Liest `map_derived_variables` via `$items("05a …")`, evaluiert `regel_json` pro Zeile in Sheet-Reihenfolge (Phase 1 R02-R12 nur normalized-Refs, Phase 2 R13-R15 mit flags.*-Refs). 8 Operatoren: `eq`/`neq`/`in`/`nin`/`includes`/`intersects`/`truthy`/`and`/`or`/`not`/`cases`. Pfad-Syntax `normalized.x`/`flags.x`/`priorities.x`. Output-Shape `{ normalized, priorities, flags }` unverändert. `volume_sensitivity` eliminiert (0 Konsumenten, byte-identisches Duplikat zu `needs_lightweight_logic`). Engine-Selbstkontrolle in Python vor Deploy. **0/36 Slot-Drift** (Executions 472-478 vs. Pre-Patch 464-470 vom 2026-06-22). Backup vor Schema-Umbau: `backups/sheets_20260623_pre_node05_schema/map_derived_variables.csv`; vor Workflow-Patch: `workflow_live_20260623.json`. **Cleanup-Welle 2026-06-24**: 3 weitere 0-Konsumenten-Flags entfernt (`needs_detangling`, `styling_goal_natuerlich`, `needs_protection_focus`). Konsumenten-Verifikation via frischem n8n-API-GET (0 jsCode-Refs) + 15-Tab-Vollscan im Sheet (0 Cross-Refs). `heat_use.konsumenten` mitbereinigt (Verweis auf `flags.needs_protection_focus` raus). 17→14 Zeilen via `cleanup_node05_sheet.py`. Validation Direct-API: Executions 493-499 vs. Baseline 472-478 = **0/36 Slot-Drift**. Backup: `backups/sheets_20260623_pre_node05_cleanup/map_derived_variables.csv`. |
| #10 | **Node 06 Phase 2 Sheet-getrieben** (deployed 2026-06-24) | `map_pflegelevel_scoring` (Schema-Erweiterung 8→9 Spalten: neue Spalte `max_punkte`, neue Regel PFL-23) | **Node 06 v4** (deployed 2026-06-24): Inline-Phase-2-Block (7 LOC, `goalCount = care_goals.filter(g !== gesunde_kopfhaut).length`, `Math.min(goalCount, 2)`) durch Sheet-Regel PFL-23 ersetzt. `evalBedingung()` → `applyRule()` umgebaut: gibt Punkte statt Boolean, neuer Operator `array_count_except` (zählt Array-Werte ungleich `bedingung_wert`, Punkte = `min(count × punkte, max_punkte)`). 22 bestehende Regeln unverändert (`max_punkte` leer = kein Cap, Match-Operatoren ignorieren die Spalte). **Damit ist Node 06 vollständig sheet-getrieben** — keine inline-Heuristik mehr im Routing-Pfad außer dem PFL-01/PFL-02/PFL-03-else-if-Special-Case (semantisch in Regeln versteckt, eine separate Sheet-Migration wäre möglich aber ohne Mehrwert). **0/36 Slot-Drift** (Executions 515-521 vs. Baseline 501-507, `pflegelevel_final` byte-identisch). Skripte: `migrate_node06_phase2.py`, `patch_node06_phase2.py`. Backup: `backups/sheets_20260624_pre_node06_phase2/map_pflegelevel_scoring.csv`, `workflow_backup_20260624_pre_node06_phase2.json`. Bemerkenswert: erster Trigger-Versuch lief 7/7 in error (transient Google-Sheets-`Service unavailable` an Node 06d, identisch zum gestrigen Sarah-Single-Fail); zweiter Versuch 7/7 success. Konvention: bei transient Sheet-Loader-Fehlern einfach erneut triggern, nicht Workflow patchen. |
| #11 | **Node 11 Suppress-Regel Sheet-getrieben** (deployed 2026-06-24) | `map_slot_rules` (eine neue Zeile `REQ-MIN-NO-OPT` mit `prioritaet=suppress_optional`, kein Schema-Edit) | **Node 11 v2** (deployed 2026-06-24): Inline-Block Z. 162-165 (`if routine_preference === 'minimal' → slots.optional = []`) durch Sheet-Regel `REQ-MIN-NO-OPT` ersetzt. Neue `prioritaet`-Klasse `suppress_optional`: Regel hat kein `slot_typ`, feuert wenn `routine_preference=minimal`, Side-Effect in Node 11 Phase 5 (neu, nach Slot-Bau): leert `slots.optional`. Phase 4 ignoriert `prioritaet.startsWith('suppress_')`-Regeln. Erweiterbar um künftige Suppress-Klassen ohne Schema-Edit. **Damit ist Node 11 vollständig sheet-getrieben** und alle Routing-Pfad-Inline-Heuristiken seit Migration #5 sind eliminiert. **0/36 Slot-Drift** (Executions 522-528 vs. Baseline 515-521). Sanity-Verifikation Anna's Execution 522: `applied_rules` enthält `REQ-MIN-NO-OPT`, `slot_assignments.optional=[]`, Final-Routine `[monat_black]` byte-identisch. Skripte: `patch_node11_minimal.py` (Sheet-Edit war 1-Zeilen-`append_row`, kein Migrate-Skript nötig). Backup: `backups/sheets_20260624_pre_node11_minimal/map_slot_rules.csv`, `workflow_backup_20260624_pre_node11_minimal.json`. |

Mini-Syntax in `map_pool_filter` und `map_pflegelevel_overrides`-ähnlichen Tabs:
- Bedingungen mit `;` getrennt, Liste `feld:operator[:wert]`
- Operatoren: `=`, `!=`, `is_true`, `is_false`, `in`, `not_in`
- Listenwerte bei `in`/`not_in` mit `|` getrennt
- Profil-Pfade: `flags.<feld>`, `normalized.<feld>`, `pflegelevel.<feld>`

## Audit-Konventionen (Datenblatt-Provenienz)

Etabliert im A–F-Audit am 2026-06-10. Verbindlich für künftige Sheet-Wert-Entscheidungen.

| # | Konvention | Quelle |
|---|---|---|
| K-01 | `ist_hitzeschutz = TRUE` ⟺ `hauptfunktion` enthält `hitzeschutz`. Sekundäre Hitzeschutz-Eigenschaft bleibt nur in `nebenfunktionen`. Analog ist als Default-Muster für andere Boolean-Eigenschafts-Flags (`ist_bonding`, `ist_scalp_focus` etc.) zu prüfen. | bond_iq_leave_in vs. hitzeschutzspray + smoothing_fohn_spray |
| K-02 | MONAT-Layering-Notation aus PDFs („Schritt-1-Prep" / „Schritt-2-Styling") **≠** unser `routine_schritt`. PDF-„Schritt-1-Prep" = funktional **nach Reinigung+Pflege, auf handtuchtrocknes Haar, vor Styling** → bei uns `slot_typ=leave_in` (`routine_schritt=5`). PDF-„Schritt-2-Styling" → unsere `styling_1` (7) / `styling_2` (8). | rejuvabeads-PDF, smoothing_tiefenbehandlung-PDF |
| K-03 | `haarstaerke` spiegelt die explizite **„Wer profitiert / Ideal für"-Hauptaussage** des PDFs (Bullet-Sektion oder FAQ-Q&A). **Nicht** Header-Schlagwörter, **nicht** Marketing-Description. Bei mehreren Empfehlungs-Aussagen: die mit dem konkretesten Sortiments-Signal gewinnt. | smoothing_tiefenbehandlung (`mittel,dick`) + moxie_mousse (`alle`) |
| K-04 | **PDF strikt**: Was nicht im Datenblatt belegt ist, kommt nicht ins Sheet. „Funktional besser" / „Beratungs-Praxis sagt" / „Kunden brauchen" sind **keine** legitimen Argumente, um nicht-PDF-belegte Sheet-Werte zu verteidigen. Beratungs-Heuristik gehört als **separate** Regel (REQ/CON) ins Sheet, nicht als impliziter Produktstammdaten-Wert. | essig-*.kopfhaut=schuppig nicht PDF-belegt — User-Klarstellung 2026-06-10 |
| K-05 | Sheet-Werte folgen PDF-Belegen **auch wenn aktuell kein Scoring-/Regel-Trigger darauf greift**. Scoring-Stille ist kein Grund für PDF-Verzicht — sie ist eine Folge der Migrations-Reihenfolge und ggf. ein eigener Folge-Punkt. | `staerkend` als nebenfunktion für monat_black akzeptiert, obwohl aktuell kein Profil-Goal darauf matched |
| K-06 | Eine haupt-/nebenfunktion zählt als belegt, wenn das PDF eine konkrete **Funktions-Aussage über die Wirkung am Haar** enthält — an beliebiger Stelle (Vorteils-Bullet, IDEAL-Bullet, FAQ, Test-Bullet ODER Beschreibungssatz). **NICHT** belegt: bloße Header/Taglines (Schlagwort ohne Aussage) und reine Inhaltsstoff-Mechanismus-Beschreibungen (z. B. „Lupinenprotein stabilisiert die Haarbindungen" = wie, nicht was am Haar passiert). Gilt **symmetrisch** für Hinzufügen/Behalten/Entfernen — keine historische Asymmetrie. | Negativbeispiel: `moxie_mousse.verdichtend` (nur Tagline „Volumen und Dichte" + CAPIXYL-Inhaltsstoff). Positiv-Kontrast: `monat_black.verdichtend` ist belegt (IDEAL-Bullet „Die Dichte verbessern und das Haar voller erscheinen lassen möchten"). |
| K-07 | Ein Test-Bullet zählt als Beleg **NUR** wenn die entsprechende Funktion auch im **Produktversprechen verankert** ist (WARUM / IDEAL / Beschreibung / Header — auch implizit). Test-Bullet ohne jede Produktversprechen-Verankerung = Nebenbeobachtung der Studie (35 Frauen, 14 Tage), zählt nicht als Produktfunktion. Gilt symmetrisch für Aufnahme und Entfernung. Grenzfall-Präzedenz: Inhaltsstoff-Mechanik als Verankerung zählt nicht — konsistent mit K-06 bond_iq-Entscheidung. | Negativbeispiel: `ir_clinical_spuelung.glanz` (94%-Test, aber Glanz nirgendwo im Produktversprechen). Konsistenz: K-06 schließt Inhaltsstoff-Mechanik als Verankerung aus (siehe bond_iq-Linie). |
| K-08 | Für **Filter-Spalten** (`kopfhaut`, `haarstaerke`, `haarstruktur`, `haarzustand`) zählt die strukturelle **Zielgruppen-Spezifikation im Header-Untertitel** des MONAT-PDFs (Format „Zustand / Haartyp / Haartextur / Step") als legitimer Beleg, **auch ohne** zusätzliche Verankerung in WARUM/IDEAL/Beschreibung. Begründung: Hersteller-Untertitel ist eine direkte „Für wen ist das"-Aussage, methodisch näher an K-03's „Wer profitiert"-Hauptaussage als an einer Werbe-Tagline. Abgrenzung zu K-06: Für **Funktions-Spalten** (`hauptfunktion`, `nebenfunktionen`) zählt der Header **weiter nicht** als Beleg (Werbe-Tagline ≠ Funktions-Aussage am Haar). K-03 bleibt der Konflikt-Löser: bei Widerspruch zwischen Header-Untertitel und IDEAL-Bullet gewinnt IDEAL. Gilt symmetrisch für Aufnahme/Behalten/Entfernen. | `monat_black.kopfhaut=fettig` + `.haarstaerke=fein,mittel` ausschließlich durch Header-Untertitel belegt (keine WARUM-/IDEAL-Verankerung). Abgrenzungskontrast: `essig_spuelung.kopfhaut=fettig` ist **nicht** durch K-08 belegbar — Header-Untertitel sagt nur „Kopfhautpflege", kein „Fettiges Haar". |

**bond_iq-Linie als Lehrbeispiel für K-06**: Die Bond-IQ-Produktlinie ist bewusst **nicht durchgängig bonding-klassifiziert** in `hauptfunktion`. `bond_iq_leave_in` behält `bonding` (eigener Funktions-Bullet „Stärkt die Haarstruktur und repariert Haarbindungen*"). `bond_iq_night_day_serum`, `bond_iq_shampoo`, `bond_iq_spuelung` haben `bonding` per K-06-Gegencheck verloren — bei ihnen ist Bindungs-Reparatur **nur** in der Inhaltsstoff-Beschreibung (Lupinenprotein „stabilisiert die inneren Haarbindungen") belegt, kein eigener Funktions-Bullet am Haar. Das ist PDF-Realität, kein Daten-Fehler. **Nicht "korrigieren"** in späteren Sessions.

**POOL-01-Architektur (K-06-Konsequenz)**: Das Bool-Flag `ist_bonding` hatte zwei Rollen vermischt — (a) Stammdatum „Produkt wirkt bonding am Haar" und (b) Routing-Proxy „Produkt gehört zur Reparatur-Linie". K-06 trennt sie: `ist_bonding` ist jetzt reines Wirkungs-Flag (analog `ist_hitzeschutz` per K-01). Das Routing der Bond-IQ-Linie liegt in POOL-01 jetzt explizit auf `produktlinie:=:bond_iq` statt auf `ist_bonding:is_true`. **`ist_bonding` darf in anderen Regeln nicht als Linien-Proxy verwendet werden** — wer das findet, behandelt es als Bug (Folge-Punkt: Sheet auf weitere Linien-Proxy-Misuses prüfen).

**Wichtige Beobachtung aus dem Vollrun (2026-06-10):** Sheet-Werte ohne PDF-Beleg sind nicht nur Doku-Schuld, sie produzieren aktiv falsche Empfehlungen. Beispiel: `monat_black.nebenfunktionen=volumen` (PDF-untreu, PDF spricht von „Dichte" und „Verdichtend") führte dazu, dass Maria + Julia (`scalp=normal`, `goal=volumen`) das falsche Shampoo bekamen — monat_black ist laut PDF für **fettige Kopfhaut**. Nach Fix gewinnt revive_shampoo (`hauptfunktion=volumen`), das funktionsspezifisch richtige Shampoo. K-04 hat damit direkten Output-Effekt auf die Kundenempfehlung.

## Audit-Workflow (Test-Disziplin)

Konventionen für **wie** auditiert wird, ergänzend zu den K-Datenkonventionen (K-01..K-08).

| # | Regel | Begründung |
|---|---|---|
| T-01 | **Isolations-Regel**: Edits, die potenziell dieselbe Slot-Entscheidung berühren, werden einzeln getestet (ein Edit → ein Full-Run → Drift-Analyse), nicht gekoppelt. Im Zweifel — wenn Slot-Disjunktheit nicht verifiziert ist — gilt isoliert als Default. Maskierung ist möglich, wenn zwei Edits dieselbe Slot-Entscheidung beeinflussen (Pool-Veränderung **oder** Score-Verschiebung im selben Slot). **Zwei Test-Modi unterscheiden**: (a) **strikt-isoliert** = nur der zu testende Edit ist aktiv im Sheet während des Runs; (b) **diff-isoliert** = mehrere Edits sind aktiv, der einzelne Effekt wird per Diff zum vorherigen Run extrahiert. Beide Modi sind nur bei verifizierter Slot-Disjunktheit äquivalent; bei unklarer Disjunktheit ist strikt-isoliert der Default. Mehraufwand pro Edit ~1 Run, Erkenntnis-Verlust 0. | Block-2-Stufe-1, 2026-06-13: Edit A strikt-isoliert (nur A im Sheet), Edit C diff-isoliert (A+C im Sheet, C-Effekt per Diff zum A-Run). Disjunkte Slots verifiziert → diff-isoliert war zulässig. |
| T-02 | **System-State-Belegpflicht**: Aussagen in HANDOVER über System-State — was der Workflow tut/nicht tut, welcher Node was konsumiert, wie ein Filter/Score wirkt, **welche Inputs/Test-Profile definiert sind, welche Sheet-Werte gesetzt sind** — müssen mit konkretem Zitat aus der **autoritativen Quelle** belegt sein: Code-Zeile (file:line oder Workflow-Backup Node+Z.), Sheet-Read, `test_suite.py`-Zeile, `.env`-Eintrag. **HANDOVER-Doku ist abgeleitete Information und darf nicht als Beleg für Aussagen über System-State dienen** — sie kann unvollständig oder veraltet sein. Beobachtungs-Befunde (Run-Output, Sheet-Stand, JSON-Inspektion) sind ohne Quell-Verifikation gültig, dürfen aber **nicht** zu Architektur-Schlüssen extrapoliert werden. Stop-Frage vor jeder System-State-Aussage: „Habe ich die autoritative Quelle dazu gelesen, oder reproduziere ich nur eine andere Doku-Stelle?" | Block-2-Stufe-1, 2026-06-13: zwei Fehler-Klassen abgedeckt. (a) **Mechanismus**: „kopfhaut-Spalte filtert nicht" basierte auf Beobachtungs-Extrapolation (Maria's Pool unverändert), nicht auf Code-Inspektion. Korrektur erst nach Tomi-Rückfrage: Node 12 Z. 26 zeigt Score-Bonus +2 statt Filter. (b) **Daten**: „anna scalp_status=keine_probleme" basierte auf HANDOVER-Eingabe-Kurzform (Z. 335 dokumentiert hair_condition als „keine_probleme") statt test_suite.py-Read (Z. 62: `scalp_status=['fettig']`). HANDOVER war die Doku-Quelle, nicht die autoritative — test_suite.py ist autoritativ. Korrektur erst nach Tomi-Rückfrage. |
| T-03 | **API↔API-Drift-Check** statt test_suite-Polling: bei Pipeline-Latenz >90 s (Standard mit 6 Sheet-Loadern + Cold-Start) timed test_suite-Polling ab. Workaround = direkter n8n-API-Read der success-Executions, Set-Vergleich `final_routine.produkt_key` pro `first_name` zwischen Pre-Edit-Baseline und Post-Edit-Lauf. Vorgehen: (1) Pre-Edit-Baseline-Execution-IDs notieren; (2) Edits + test_suite.py starten; (3) `until python3 -c "…sys.exit(0 if succ>=7 else 1)"; do sleep 30; done` bis 7 neue success-Executions; (4) pro Execution Node `15 Routine sortieren` → `final_routine.produkt_key` extrahieren; (5) Set-Vergleich. **Polling-Bug-Warnung**: niemals `until python3 -c "…" 2>&1 \| grep …; do …; done` — grep returnt immer 0 und überschreibt python-Exit-Status → Loop exited fälschlich nach 1. Iteration. Entweder `set -o pipefail` setzen oder grep weglassen (stderr für Status, stdout = leer). | Block 2 Stufe 3 Cluster 1 + 2A + 2B-1 (2026-06-16, 3 Sessions in Folge): test_suite-Polling alle 7 timed out, API-Direkt-Read war zuverlässige Wahrheits-Quelle. Grep-Bug in 2B-1 entdeckt nach 1-Iteration-Exit mit „0 success" Output. |

## Datenblatt-Provenienz-Audit (Stand 2026-06-13)

Spalten-Reihenfolge nach Scoring-Relevanz: Block 1 (scoring-kritisch: `hauptfunktion`, `nebenfunktionen`) → Block 2 (Filter: `haarstaerke`, `haarstruktur`, `haarzustand`, `kopfhaut`) → Block 3 (Bool-Flags + Level) → Block 4 (Doku). Produkt-Reihenfolge je Block in 4 Stufen nach Bug-Risiko (Multi-Funktion → seltene Tokens → A–F-Re-Verify → Singulär-Sanity).

**Block 1 Stufe 1** — 8 Produkte (Multi-Funktions-`hauptfunktion`: 4× bond_iq + 3× curl + moxie_mousse) — abgeschlossen 2026-06-11. 7 Zellen-Edits in `produktdatenbank.nebenfunktionen` (16 Token-Ergänzungen), alle K-04/K-05 strikt (eigener Vorteils-Bullet oder eigene FAQ-Aussage Pflicht; Tagline, reine Inhaltsstoff-Mechanismus-Beschreibung oder Nebensatz-Erwähnung zählen nicht):

| Produkt | nebenfunktionen ergänzt um | belegende Bullet-Kategorie |
|---|---|---|
| bond_iq_leave_in | `frizz_reduktion`, `kaemmbarkeit`, `glanz` | je eigener Vorteils-Bullet + Test 91 % für kaemmbarkeit |
| bond_iq_night_day_serum | `frizz_reduktion`, `kaemmbarkeit`, `elastizitaet` | Test 91 % für frizz_reduktion; eigener Bullet für elastizitaet |
| bond_iq_shampoo | `glanz`, `kaemmbarkeit` | je eigener Vorteils-Bullet |
| bond_iq_spuelung | `frizz_reduktion`, `glanz`, `elastizitaet` | Test 89 % für frizz_reduktion; eigener Bullet für glanz + elastizitaet |
| curl_creme | `kaemmbarkeit` | eigener Bullet + Test 91 % |
| curl_gelee | `frizz_reduktion`, `glanz` | Test 91 % für frizz_reduktion; eigener Bullet für glanz |
| curl_auffrischer | `frizz_reduktion`, `definition` | Test 91 % bzw. 94 % |

**Bewusst NICHT ergänzt** (Stand Stufe-1-Sammel-Entscheidung 2026-06-11; teilweise später per **K-06-Gegencheck** revidiert, siehe Block unten):
- `bonding` bei bond_iq_night_day_serum / bond_iq_shampoo / bond_iq_spuelung — nur via Inhaltsstoff-Beschreibung belegt, kein eigener Vorteils-Bullet. → **K-06-Gegencheck**: zusätzlich **entfernt** aus `hauptfunktion` der 3 Produkte.
- `moxie_mousse.verdichtend` — nur Header-Tagline + CAPIXYL-Inhaltsstoff → **K-06**: bleibt draußen (Negativbeispiel zu K-06).
- `moxie_mousse.definition` — vorher als „nur FAQ" abgelehnt → **K-06-Gegencheck**: nachträglich aufgenommen (FAQ-Q2 „sorgt bei Locken oder Wellen für definierte Form und Frizz-Kontrolle" ist konkrete Funktions-Aussage am Haar).

`hauptfunktion` aller 8 Produkte unverändert (Stufe 1); 3 bonding-Entfernungen erst im K-06-Gegencheck — siehe Block unten.

**Neu im Sheet-Vokabular**: `elastizitaet` (vorher nur bei `super_feuchtigkeitsmaske`, jetzt zusätzlich `bond_iq_night_day_serum`, `bond_iq_spuelung`). 0 Treffer in `map_slot_rules` / `map_conflict_rules` / `map_priorities` → kein Filter/REQ-Hard-Fail. Node 12 ohne care_goal-Match → +0 Score, kein Scoring-Effekt.

**Reihenfolge irrelevant**: Node 12 nutzt `csvToArr` + `.some()` → Set-Verhalten. Reihenfolge der Token in `nebenfunktionen` ohne funktionalen Effekt.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_010951_pre_block1_stufe1/produktdatenbank.csv` (38 Zeilen, Pre-Edit-Snapshot).

**Regression**: Full-Run 2026-06-11 — 7/7 Profile produkt_key-identisch zur 10.06.-Baseline. Erwartete Score-Drift nur für Lena (`mehr_glanz`-Goal, substring-Match auf neu-ergänztes `glanz` bei bond_iq + curl_gelee) — kein Slot-Shift, da Lenas Pool die jeweiligen Slots bereits via REQ-Routing (Renew, Hitzeschutzspray) bzw. ohne Konkurrenz (curl_gelee in styling_2) dominiert.

**Block 1 Stufe 2** — 8 Produkte (seltene/auffällige Tokens: monat_black, rejuvabeads, ir_clinical_kopfhautserum, the_champ, replenish_maske, super_feuchtigkeitsmaske, restore_leave_in, kopfhaut_peeling) — abgeschlossen 2026-06-11. 5 Zellen-Edits in `nebenfunktionen`, 7 Token-Ergänzungen, nach dem damals geltenden „eigener Vorteils-Bullet"-Kriterium (Stufe-1-Regel):

| Produkt | nebenfunktionen ergänzt um | belegender Bullet/Aussage |
|---|---|---|
| rejuvabeads | `kaemmbarkeit`, `staerkend`, `frizz_reduktion` | je eigener WARUM-/IDEAL-Bullet |
| ir_clinical_kopfhautserum | `staerkend` | Test-Bullet 82 % „zur Stärkung der Haare beiträgt" |
| replenish_maske | `kaemmbarkeit` | IDEAL „Verbesserte Haarstruktur und Kämmbarkeit wünschen" |
| super_feuchtigkeitsmaske | `kaemmbarkeit` | WARUM „Fördert die Elastizität und verbessert die Kämmbarkeit" |
| kopfhaut_peeling | `frische` | IDEAL „gereinigt und erfrischt hinterlassen möchten" |

Grenzfälle behalten (per Sammel-Entscheidung): `rejuvabeads.glanz` (Beschreibung „glatt, glänzend") + `replenish_maske.kraeftigend` (Beschreibung „stellt Glanz, Kraft und Vitalität wieder her"). Beide haben *keinen* eigenen Vorteils-Bullet, sind aber wörtliche PDF-Aussage über die Wirkung am Haar. Unter K-06 jetzt eindeutig belegt.

`hauptfunktion` aller 8 Produkte unverändert.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_015455_pre_block1_stufe2/produktdatenbank.csv`.

**Regression**: Full-Run 2026-06-11 — 7/7 produkt_key-identisch zur Pre-Stufe-2-Baseline.

### K-06-Gegencheck (2026-06-11)

Anlass: Nach Stufe 2 wurde die „Bullet-Pflicht" aus Stufe 1 zu K-06 in finaler Form ausgeweitet (Funktions-Aussage am Haar — egal an welcher Stelle — vs. Tagline/Inhaltsstoff-Mechanik). K-06 wirkt **symmetrisch** auf Hinzufügen/Behalten/Entfernen. Folge: rückwirkender Gegencheck über alle 16 Produkte aus Stufe 1+2.

**Aufnahmen** (13 Token über 7 Produkte, vorher übersehen oder per damals strenger Bullet-Pflicht ausgeschlossen):

| Produkt | Token | Beleg-Quelle |
|---|---|---|
| bond_iq_leave_in | +`staerkend` | Test 91 % „die Haarsträhnen stärkt" |
| bond_iq_night_day_serum | +`staerkend`, +`kraeftigend` | Bullets „Repariert und stärkt das Haar", „Baut Haarstruktur auf … für mehr Kraft" |
| bond_iq_shampoo | +`staerkend` | Test 89 % „das Haar fühlt sich kräftiger an" |
| bond_iq_spuelung | +`staerkend` | Test 89 % „stärkt die Haarfasern, reduziert Haarbruch" |
| curl_creme | +`elastizitaet` | Test 88 % „Locken Elastizität und Definition verleiht" |
| curl_gelee | +`elastizitaet`, +`staerkend`, +`reparatur` | Bullets „Elastizität wiederherzustellen", „Pflegt, stärkt und repariert welliges, lockiges und krauses Haar" |
| curl_auffrischer | +`elastizitaet`, +`staerkend` | Bullets „Verbessert die Haarelastizität", „Macht Locken stärker, weicher und glänzender" |
| moxie_mousse | +`definition` | FAQ-Q2 „sorgt bei Locken oder Wellen für definierte Form und Frizz-Kontrolle" |
| kopfhaut_peeling | +`feuchtigkeit` | Beschreibung „Angereichert mit REJUVENIQE® spendet es Feuchtigkeit und hinterlässt das Haar gereinigt und erfrischt" |

**Entfernungen aus `hauptfunktion`** (3 Token):
- bond_iq_night_day_serum: `reparatur,bonding` → `reparatur`
- bond_iq_shampoo: `reparatur,bonding` → `reparatur`
- bond_iq_spuelung: `reparatur,bonding` → `reparatur`

Begründung: bei diesen 3 Produkten ist Bonding **nur** über die Inhaltsstoff-Beschreibung Lupinenprotein belegt — Inhaltsstoff-Mechanik, kein Funktions-Bullet am Haar. K-06 verlangt symmetrische Konsequenz: Token raus. `bond_iq_leave_in.bonding` bleibt (eigener Bullet „repariert Haarbindungen*").

**K-01-Konsistenzkorrektur (3 Bool-Flags vorgezogen aus Block 3)**: `ist_bonding` bei bond_iq_night_day_serum, bond_iq_shampoo, bond_iq_spuelung von `TRUE` auf `FALSE` gesetzt. K-01 fordert `ist_bonding=TRUE ⟺ hauptfunktion enthält bonding` — nachdem `bonding` aus `hauptfunktion` raus ist, muss das Flag folgen. **Rest von Block 3 (übrige Bool-Flags, Pflegelevel-Audit) noch offen** — wurde nicht mit-erledigt, nur diese 3 K-01-Konsistenzfälle.

**POOL-01-Umstellung** (in `map_pool_filter`): `produkt_bedingungen` von `ist_bonding:is_true` auf `produktlinie:=:bond_iq`, `beschreibung` von „Bonding-Produkte nur bei Reparatur-Fokus zulassen" auf „Bond-IQ-Linie nur bei Reparatur-Fokus zulassen". Architektur-Hintergrund: siehe K-06-Block oben („POOL-01-Architektur"). Effekt: Routing-Verhalten bleibt funktional identisch zur Pre-K-06-Baseline, aber das Routing-Kriterium ist jetzt sauber an `produktlinie` gekoppelt statt am vermischten Stammdatum `ist_bonding`.

**Backups**:
- `~/Projekte/myglowmatch/backups/sheets_20260611_092835_pre_k06_gegencheck/produktdatenbank.csv`
- `~/Projekte/myglowmatch/backups/sheets_20260611_110432_pre_pool01_relink/map_pool_filter.csv`

**Regression**: Full-Run nach POOL-01-Umstellung — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline** (Stand nach Stufe 2). Sarah (needs_repair_focus=TRUE) bekommt weiter alle 4 Bond-IQ-Produkte; Lena/Bianca/Vivien wieder auf Renew/Feuchtigkeits-Linie wie vorher.

**Block 1 Stufe 3** — 8 Produkte (A–F-Re-Verify-Cluster + Smoothing-/Föhn-Doppelung: hitzeschutzspray, smoothing_fohn_spray, essig_shampoo, essig_spuelung, fohncreme, smoothing_shampoo, smoothing_deep_conditioner, smoothing_tiefenbehandlung) — abgeschlossen 2026-06-11. 7 Zellen-Edits in `nebenfunktionen` (16 Token-Ergänzungen über 7 Produkte + 1 K-06-konforme Entfernung; fohncreme unverändert):

| Produkt | nebenfunktionen ergänzt um (Entfernung in **fett**) | Belege |
|---|---|---|
| hitzeschutzspray | `staerkend`, `elastizitaet` | IDEAL „Stärke und Elastizität des Haares verbessern" + Test „mehr Stärke und Elastizität" + Beschreibung „stärkt und schützt das Haar" |
| smoothing_fohn_spray | `kaemmbarkeit`, `staerkend`, `elastizitaet`, `farbschutz` | Test 4x/3x Kämmbarkeit; WARUM „Stärkt das Haar"; Test „Gestärktes Haar, verbesserte Elastizität"; Test „Farbbrillanz bis zu 20 Haarwäschen erhalten" |
| essig_shampoo | `kopfhautpflege`, `frische` | WARUM „Reduziert überschüssiges Fett und stellt das Gleichgewicht der Kopfhaut wieder her"; IDEAL „Frisches, sauberes … Haar möchten" |
| essig_spuelung | `entgiftung`, `farbschutz`, `kopfhautpflege` | WARUM „Entfernt Produktrückstände" + Test 80 % „Feuchtigkeitsgehalts der Kopfhaut"; WARUM „bewahrt die Farbe für bis zu 20 Haarwäschen" + Test 83 % |
| smoothing_shampoo | `glanz`, `reparatur` | Test „24 % mehr Glanz"; WARUM „weniger Haarbruch" + Test „68 %" |
| smoothing_deep_conditioner | `glanz`, `reparatur` | Test „56 % mehr Glanz"; WIE „7x weniger Haarbruch" + Test „87 %" |
| smoothing_tiefenbehandlung | `kaemmbarkeit`, `glanz`, `reparatur`; **−`feuchtigkeit`** | Test 6x/5x Kämmbarkeit; Test „80 % mehr Glanz"; WIE „Reduziert Haarbruch um 91 %" |
| fohncreme | (keine) | hauptfunktion + Sheet-`glanz` PDF-belegt; keine weiteren Funktions-Aussagen am Haar |

**Erste K-06-konforme nebenfunktion-Entfernung**: `smoothing_tiefenbehandlung.feuchtigkeit` raus. Das Wort „Feuchtigkeit" kommt im PDF nicht vor; Wirkung nur indirekt über „Pflanzliche Buttern verwöhnen das Haar, machen es geschmeidig und weich" + Conditioner-Charakter ausgedrückt. Conditioner-Produkttyp-Rückschluss ist unter K-06 keine Funktions-Aussage am Haar. Symmetrie-Beleg für K-06: die Regel greift nicht nur bei `hauptfunktion`-Tokens (wie bei den 3 bond_iq-bondings), sondern auch bei nebenfunktion-Tokens. Auswirkung auf Routing: null (smoothing_tiefenbehandlung ist via CON-11 ohnehin aus allen 7 Profilpools).

`hauptfunktion` aller 8 Produkte unverändert.

**K-01-Konsistenz-Check** (zweite Block-3-Spot-Prüfung): `ist_hitzeschutz`-Flag bei allen 8 Produkten konsistent mit `hauptfunktion` — `hitzeschutzspray` (`hauptfunktion=hitzeschutz` → TRUE), `smoothing_fohn_spray` + `fohncreme` (enthält `hitzeschutz` → TRUE), übrige 5 (enthält nicht → FALSE). 8/8 konsistent, **keine weiteren Block-3-Vorziehungen** nötig.

**Vokabular-Beobachtung**: alle 9 verschiedenen ergänzten Tokens (`staerkend`, `elastizitaet`, `kaemmbarkeit`, `farbschutz`, `kopfhautpflege`, `frische`, `entgiftung`, `glanz`, `reparatur`) bereits im Vokabular etabliert — keine Neueinführungen. `farbschutz` war bisher nur bei `ir_clinical_shampoo` + `ir_clinical_spuelung` etabliert; Stufe 3 ist die erste Verwendung bei Styling- und Reinigungs-Produkten (`smoothing_fohn_spray`, `essig_spuelung`). Falls künftig eine Scoring-Regel `goal=farbschutz` auswertet, sind diese zwei Produkte jetzt korrekt im Pool — nur als Beobachtung, kein offener Punkt.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_210600_pre_block1_stufe3/produktdatenbank.csv`.

**Regression**: Full-Run nach den 7 Zell-Updates — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline** (Stand nach K-06-Gegencheck + POOL-01-Relink). Erwartung bestätigt: keiner der ergänzten Tokens matched ein direktes Profil-Goal, das einen Slot-Shift auslösen würde; die `feuchtigkeit`-Entfernung bei smoothing_tiefenbehandlung wirkt sich nicht aus, da CON-11 das Produkt in allen 7 Pools blockiert.

**Block 1 Stufe 4** — 13 Produkte (Singulär-Sanity: feuchtigkeits_shampoo, renew_shampoo, renew_spuelung, erweiterte_feuchtigkeit_spuelung, revive_shampoo, revitalize_spuelung, volumen_spray, rejuveniqe_oel, entwirrungsspray, scalp_comfort_behandlung, scalp_comfort_serum, ir_clinical_shampoo, ir_clinical_spuelung) — abgeschlossen 2026-06-12. **Block 1 damit vollständig**. 19 Zell-Updates in `nebenfunktionen` (26 Token-Aufnahmen über 12 Produkte + 10 Token-Entfernungen über 8 Produkte; fohncreme + scalp_comfort_serum unverändert):

| Produkt | Aufnahmen | Entfernungen | Quelle |
|---|---|---|---|
| feuchtigkeits_shampoo | `reinigung` | — | Stufe 4 |
| renew_shampoo | `reinigung`, `kaemmbarkeit` | — | Stufe 4 |
| renew_spuelung | `kaemmbarkeit` | **−`glanz`** (K-06: Glanz im PDF nicht erwähnt) | Stufe 4 |
| erweiterte_feuchtigkeit_spuelung | `kaemmbarkeit` | — | Stufe 4 |
| revive_shampoo | `staerkend`, `feuchtigkeit`, `kaemmbarkeit`, `reparatur` | — | Stufe 4 |
| revitalize_spuelung | `staerkend`, `kaemmbarkeit`, `reparatur` | — | Stufe 4 |
| volumen_spray | `verdichtend`, `staerkend` | — | Stufe 4 |
| rejuveniqe_oel | `kraeftigend`, `kaemmbarkeit` | — | Stufe 4 |
| entwirrungsspray | `glanz`, `staerkend`, `kaemmbarkeit` | — | Stufe 4 |
| scalp_comfort_behandlung | `reinigung`, `entgiftung`, `frische` | — | Stufe 4 |
| ir_clinical_shampoo | `haarwuchs`, `staerkend`, `frische` | — | Stufe 4 (4 weitere per K-07 gestrichen) |
| ir_clinical_spuelung | `haarwuchs`, `staerkend`, `kaemmbarkeit`, `frische` | — | Stufe 4 (glanz per K-07 gestrichen) |

**Erste K-06-konforme nebenfunktion-Entfernung außerhalb Stufe 3**: `renew_spuelung.glanz` — das Wort „Glanz" / „glänzend" kommt im renew_spuelung-PDF nirgendwo vor (kein WARUM, IDEAL, VORTEILE, Test oder Beschreibung). Cross-References in „FUNKTIONIERT GUT MIT" beziehen sich auf Replenish-Maske als Begleiter, nicht auf renew_spuelung selbst. Analog zu smoothing_tiefenbehandlung.feuchtigkeit-Entfernung aus Stufe 3.

**Vokabular-Beobachtung**:
- `frische` jetzt 5 Produkte: essig_shampoo, scalp_comfort_behandlung, ir_clinical_shampoo, ir_clinical_spuelung, the_champ (vorher nur the_champ; Stufe 3 ergänzte essig + kopfhaut_peeling; Stufe 4 ergänzte 3 weitere).
- `haarwuchs` jetzt **komplett bei IR-Clinical-Linie**: ir_clinical_kopfhautserum (Stufe 2) + ir_clinical_shampoo + ir_clinical_spuelung (Stufe 4). Konsistente Linien-Klassifikation.
- `verdichtend` neu als nebenfunktion bei volumen_spray — vorher nur als hauptfunktion bei IR-Clinical-Linie + monat_black. Erste Verwendung als sekundäre Funktion.
- `kraeftigend` neu bei rejuveniqe_oel — vorher nur replenish_maske + bond_iq_night_day_serum.
- Keine Neueinführungen ins Vokabular.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_234938_pre_stufe4_k07/produktdatenbank.csv`.

**Regression**: Full-Run nach den 19 Zell-Updates — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline**. Lena (`mehr_glanz`-Goal) trotz `renew_spuelung.glanz`-Entfernung unverändert: Score-Differenz reicht nicht für Slot-Wechsel; konkurrierende Spülungen (`erweiterte_feuchtigkeit_spuelung`, `revitalize_spuelung`) sind durch andere Kriterien dominiert.

### K-07-Gegencheck (2026-06-12)

Anlass: User-Befund zu `ir_clinical_spuelung.glanz` (Stufe-4-Vorschlag) — Glanz nur in 94%-Test, nirgendwo im Produktversprechen. K-07 als Präzisierung eingeführt (siehe Konventionen-Tabelle), rückwirkender Gegencheck über alle eingespielten Token aus Stufen 1+2+3+K-06.

**Rückwirkende Entfernungen aus eingespieltem Material** (10 Token-Entfernungen über 7 Produkte; davon 1 K-06-konform aus Stufe 4 oben + 9 K-07-konform):

| Produkt | Token | Quelle | Test-Wortlaut | Grund |
|---|---|---|---|---|
| bond_iq_spuelung | `frizz_reduktion` | Stufe 1 | „89 % … glättet die Schuppenschicht, reduziert Frizz und verbessert die Frisierbarkeit*" | Frizz nirgendwo in WARUM-Aussage-Bullets, IDEAL, Beschreibung |
| curl_creme | `elastizitaet` | K-06 | „88 % … Locken Elastizität und Definition verleiht" | Elastizität nirgendwo in WARUM, IDEAL, Beschreibung |
| smoothing_fohn_spray | `kaemmbarkeit` | Stufe 3 | „4x/3x bessere Kämmbarkeit" | Kämmbarkeit nirgendwo im Produktversprechen |
| smoothing_fohn_spray | `elastizitaet` | Stufe 3 | „Gestärktes Haar, verbesserte Elastizität …" | Elastizität nirgendwo im Produktversprechen |
| smoothing_fohn_spray | `farbschutz` | Stufe 3 | „Farbbrillanz bis zu 20 Haarwäschen erhalten" | Farbe nirgendwo im Produktversprechen |
| smoothing_shampoo | `glanz` | Stufe 3 | „24 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| smoothing_deep_conditioner | `glanz` | Stufe 3 | „56 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| smoothing_tiefenbehandlung | `glanz` | Stufe 3 | „80 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| ir_clinical_kopfhautserum | `staerkend` | Stufe 2 | „82 % … zur Stärkung der Haare beiträgt" | Verankerung nur via CAPIXYL-Inhaltsstoff-Mechanik (K-06-Grenzfall-Präzedenz: Mechanik zählt nicht) |

**Streichungen aus Stufe-4-Vorschlag** (9 Token, gar nicht erst geschrieben):
- feuchtigkeits_shampoo: `farbschutz` (Test, keine Produktversprechen-Verankerung)
- erweiterte_feuchtigkeit_spuelung: `farbschutz` (analog)
- ir_clinical_shampoo: `kopfhautpflege`, `glanz`, `kaemmbarkeit`, `feuchtigkeit` (4 Tokens; nur in Tests, nicht im Produktversprechen) — **K-01-Cascade entfällt**: `ist_scalp_focus` bleibt FALSE (kopfhautpflege nicht aufgenommen)
- ir_clinical_spuelung: `glanz` (K-07-Negativbeispiel)
- scalp_comfort_serum: `frische` (Test sagt „erfrischt", Produktversprechen sagt nur „kühlend" — semantisch verwandt aber kein wörtlicher Beleg)

**Vokabular nach K-07-Cleanup**: `farbschutz` jetzt nur noch IR-Clinical-Linie (`ir_clinical_shampoo`, `ir_clinical_spuelung` — `smoothing_fohn_spray` rausgeflogen). `elastizitaet` nur noch bei super_feuchtigkeitsmaske + bond_iq_night_day_serum + bond_iq_spuelung + curl_gelee + curl_auffrischer (curl_creme + hitzeschutzspray + smoothing_fohn_spray rausgeflogen).

**Regression**: 7/7 produkt_key-identisch zur HANDOVER-Baseline. Vorhersage bestätigt — keiner der entfernten Tokens matched ein direktes Profil-Goal, das einen Slot-Shift auslösen würde; betroffene Smoothing-Produkte sind via CON-11 ohnehin aus den Pools blockiert.

### Block 1 — Gesamt-Bilanz nach Abschluss

Stufen 1+2+K-06+3+4+K-07 zusammen:
- **32 Produkte angefasst** (5 unverändert: ir_clinical_shampoo war kein Stufe-1-Cluster, fohncreme + scalp_comfort_serum keine Edits, 2 weitere ohne fehlt-im-Sheet)
- **Netto-Aufnahmen**: ~73 Token-Ergänzungen über alle Stufen
- **Entfernungen**: 14 Token (3 bonding aus hauptfunktion via K-06, 11 nebenfunktion via K-06/K-07)
- **3 Konventionen geschärft**: K-06 (Wirkung am Haar vs. Schlagwort/Mechanik), K-07 (Test-Verankerung im Produktversprechen), K-01-Bond-IQ-Cascade (3 ist_bonding-Flags + POOL-01-Umstellung)
- **0 Routing-Drift über alle Stufen**: HANDOVER-Sollwerte unverändert

**Offen**: Block 2 Stufe 1 in Arbeit (`kopfhaut`-Spalte, siehe unten); Block 2 Stufen 2-3 (`haarstruktur`/`haarstaerke`/`haarzustand`) + Block 3 Rest (Bool-Flags ohne die 3 bei K-06-Gegencheck vorgezogenen + `pflegelevel` + `ausschluss_bei`) + Block 4 (Doku-Spalten: `anwendung`, `produkt_url`, `locken_geeignet`).

**Block 2 Stufe 1** — `kopfhaut`-Spalte, 6 Produkte mit non-Default-Wert + Cross-Check der 31 Default-Produkte — abgeschlossen 2026-06-15.

Audit-Befund pro Produkt (6 non-Default + ir_clinical_kopfhautserum als Cross-Check-Treffer):

| Produkt | Sheet-Wert | PDF-Beleg | Entscheidung |
|---|---|---|---|
| essig_shampoo | `fettig` | Header-Untertitel „Fettiges Haar und Kopfhaut" (K-08 ✓) + WARUM „Reduziert überschüssiges Fett und stellt das Gleichgewicht der Kopfhaut wieder her" (K-06 ✓) | Status Quo |
| **essig_spuelung** | `fettig` → **`-`** | Header-Untertitel sagt nur „Kopfhautpflege" (K-08 nicht einschlägig); WARUM-Bullet „Entfernt Produktrückstände, Schmutz und Öl" ist allgemeine Reinigungs-Aussage, kein Fett-spezifischer Beleg; „Talgablagerungen lösen" steht nur unter APFELESSIG-Inhaltsstoff-Erklärung → K-06 schließt Inhaltsstoff-Mechanik aus. Symmetrische K-06-Entfernung. | **Edit A** ✓ |
| kopfhaut_peeling | `fettig` | Header-Untertitel „Fettiges Haar und Kopfhaut" (K-08 ✓) + WARUM „Reduziert überschüssiges Öl und stellt das Gleichgewicht der Kopfhaut wieder her" (K-06 ✓) | Status Quo |
| monat_black | `fettig` | **Ausschließlich** Header-Untertitel „Fettiges Haar und Kopfhaut / Verdichtend / Feine bis mittlere Haartypen" (K-08 ✓). Keine weitere WARUM-/IDEAL-Verankerung — Anlass für K-08-Einführung. | Status Quo (K-08-Primärbeispiel) |
| scalp_comfort_behandlung | `juckend_empfindlich,schuppig,trocken` | Header + IDEAL „trockene, gereizte, juckende, schuppige und empfindliche Kopfhaut" + Test-Bullets 89/96/96 % — alle 3 Tokens dreifach belegt (K-06 + K-07 ✓) | Status Quo |
| scalp_comfort_serum | `juckend_empfindlich,schuppig,trocken` | analog scalp_comfort_behandlung (Header + IDEAL + Test); zusätzlich Test 87 % „schützende Feuchtigkeitsbarriere" | Status Quo |
| **ir_clinical_kopfhautserum** | `-` → **`trocken`** | Cross-Check-Fund (war auf Default trotz „Kopfhaut" im Produktnamen). IDEAL-Bullet 3 wörtlich „Trockene Kopfhaut haben" (K-06 ✓); Test 87 % „Kopfhaut mit Feuchtigkeit versorgt" mit K-07-Verankerung via IDEAL. Andere Tokens geprüft + abgelehnt: `juckend_empfindlich` (Test 77 % „weniger juckt", keine Produktversprechen-Verankerung → K-07 ausschließt), `fettig` (Test 85 % „weniger fettig", keine Verankerung → K-07), `schuppig` (nirgendwo). | **Edit C** |

**Architektur-Klärung zur `kopfhaut`-Produktspalte** (Code-verifiziert, T-02): Node 12 Z. 26 (workflow_backup_20260610_222030_pre_signature_fix.json, „12 Scoring & Slot-Befüllung"):
```javascript
if (kopfhaut.includes(p.primary_scalp_state) || kopfhaut.length === 0)
  score += (kopfhaut.includes(p.primary_scalp_state) ? 2 : 0);
```
→ `kopfhaut` wirkt als **Score-Bonus +2 bei scalp-Match**, **nicht als Pool-Filter**. Default `-` (leeres Array) lässt durch ohne Bonus. Werte ohne Match lassen ebenfalls durch ohne Bonus. Cross-Verifikation: `haarstaerke`-Spalte filtert aktiv (Maria fein → nur `fein,mittel`/`alle`-Produkte im Pool) — Block-2-Filter-Spalten haben damit **unterschiedliche Wirkmechanismen**, Cross-Check für `haarstruktur` + `haarzustand` separat nötig.

**Edit A — Drift-Analyse (strikt-isoliert, 2026-06-13)** — Sheet-Setup beim Run: nur Edit A aktiv:
- 7/7 Profile produkt_key-identisch zur Pre-Edit-A-Baseline (test_results_20260612_000047.json vs. test_results_20260613_012029.json)
- Edit A entfernt essig_spuelung's +2-Score-Bonus für scalp=fettig-Profile (Node 12 Z. 26). Aktueller Test-Suite-Stand: nur anna hat scalp=fettig (siehe 🔴-Folgepunkt zu anna), bei anna feuert CON-07 mit count=1 → essig_spuelung käme score-mäßig nicht ins Slot-Rennen.
- Zusätzlich erweitert Edit A essig_spuelung's nominelle Pool-Zugehörigkeit; **CON-12** (`exclude_product` bei `primary_scalp_state=normal|trocken|juckend_empfindlich`) fängt das für maria/julia/bianca/sarah/vivien sofort wieder ab; lena (scalp=normal) ebenfalls. Netto-Pool-Effekt null.
- K-05-Fall: Stammdaten-Korrektur ohne aktuellen Scoring-Trigger.

**Edit C — Drift-Analyse (diff-isoliert nach Edit A, 2026-06-13)** — Sheet-Setup beim Run: A+C beide aktiv, C-Effekt per Diff zum A-Run extrahiert (Slot-Disjunktheit A/C verifiziert, siehe T-01):
- 7/7 Profile produkt_key-identisch + 7/7 CON-Listen identisch zu Edit-A-Run (test_results_20260613_095740.json vs. _012029.json)
- ir_clinical_kopfhautserum bleibt im filtered_pool von maria/julia/bianca/sarah (`irck_in_pool` true→true) — konsistent mit Score-Bonus-Mechanik (kein Filter)
- Edit C fügt ir_clinical_kopfhautserum's +2-Score-Bonus für scalp=trocken neu hinzu. Keines der 7 Test-Profile hat scalp=trocken (lena hat `trocken` nur im **haarzustand**, nicht im scalp_status). Score-Effekt jetzt null, **aber für künftige Profile mit scalp=trocken hat Edit C Slot-Wirkung**.
- K-05-Fall: PDF-Provenienz-Korrektur mit potentiellem zukünftigen Score-Effekt.

**Methodische Einsicht aus essig_spuelung-Analyse**: HANDOVER-Stufen-Audit-Tabellen (Block 1 Stufen 1-4) listen **Stufen-Deltas** (Aufnahmen pro Stufe), **nicht** finale Zellwerte. Pre-Edit-Ist-Stand muss immer per Sheet-Read verifiziert werden, nie aus Delta-Tabelle abgeleitet. Während Frage-2-Audit (essig_spuelung.glanz) wurde `glanz,feuchtigkeit` als bereits etabliert übersehen → falscher Edit-B-Vorschlag. Beide Tokens sind K-06-belegt (IDEAL „glänzend macht" + WARUM/IDEAL „mit Feuchtigkeit versorgt"), kein rückwirkender Block-1-Edit nötig.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260612_225817_pre_block2_stufe1/produktdatenbank.csv`.

**Befund zur Baseline-Tabelle**: HANDOVER-Baseline (Z. 333 ff.) listete bei julia nur CON-12, alle Test-Runs seit 27.05. zeigen aber durchgängig **CON-07 + CON-12** (CON-07 routine-neutral, weil hitzeschutzspray bei julia ohnehin nicht in finale Routine geht). Cross-Check der anderen 6 Profile gegen Run-Output: alle 6 listen tatsächlich alle gefeuerten CONs (anna: CON-07; maria: CON-09,11,12; lena: CON-09,11; bianca: CON-02,09; vivien: CON-09,11,12; sarah: CON-09,11). **Implizite Konvention: „vollständig listen"** — julia war Update-Versäumnis (vermutlich 10.06.-A-F-Audit-Lücke, als count auf 4 + CON-12 aktualisiert wurde, CON-07 übersehen). Julia-Zeile heute korrigiert auf `CON-07, CON-12`. Kein offener Klärungspunkt mehr — Konvention ist implizit klar.

**Cross-Check der 32 Default-`kopfhaut`-Produkte** (2026-06-15, abschließend): Methode in 3 Stufen — (1) pypdf-Extraktion aller 32 PDFs, Keyword-Scan auf `kopfhaut`, `scalp`, `fettig`, `trocken`, `schuppig`, `juckend`, `empfindlich`, `gereizt`, `öl`, `talg`, `schuppen`, `irritation`; (2) Kontext-Extraktion (±200 Zeichen) um jeden Treffer der scalp-spezifischen Keywords; (3) Co-Occurrence-Filter `(trocken|schuppen|öl|talg)` ∧ `(kopfhaut|scalp)` als Sanity-Check über die schwachen Keywords. Sieben Kandidaten ergaben sich, alle nach K-06/K-07/K-08-Prüfung **abgelehnt**:

| Kandidat | Befund | Entscheidung |
|---|---|---|
| curl_auffrischer/creme/gelee | „Kopfhaut" in edukativem Block über Lockenhaar-Typen + LOC/LCO-Methode, keine Produkt-Funktions-Aussage | – |
| essig_spuelung | Header-Untertitel „Kopfhautpflege" allgemein, kein scalp-spezifischer Token (K-08 nicht einschlägig); zweite „scalp"-Erwähnung ist Cross-Reference auf kopfhaut_peeling | – (Edit A war Default-Setzung, korrekt) |
| ir_clinical_shampoo | „91 %/92 % Kopfhaut und Haar weniger fettig" + „97 % Kopfhaut gereinigt" nur in Test-Bullets; weder WARUM, IDEAL, Header noch Beschreibung enthalten Kopfhaut-Bezug → K-07-Verankerung fehlt (konsistent mit Stufe-4 K-07-Cleanup: `kopfhautpflege` damals aus selbem Grund abgelehnt) | – |
| ir_clinical_spuelung | „scalp" nur Cross-Reference auf Scalp Serum + Anwendungshinweis „von der Kopfhaut bis in die Spitzen auftragen" (= Anwendung, keine Zielgruppen-/Funktions-Aussage) | – |
| rejuveniqe_oel | „fettig" = Wiesenschaumkraut-Inhaltsstoff („ohne fettig zu wirken", K-06 ausschließt Inhaltsstoff-Mechanik); „schuppig" = Körperpflege-Hinweis „schuppige Haut" (nicht Kopfhaut) | – |
| the_champ | alle 7 „trocken"-Hits = Produktname „Trockenshampoo" oder dessen Kontext; einziger „Kopfhaut"-Bezug ist Anwendungs-Warnung „nicht auf die gesamte Kopfhaut" | – |
| bond_iq-Linie (Leave-In/Serum/Shampoo/Spülung) | alle „schuppen"-Hits = „Schuppenschicht" (Haar-Kutikula), nicht Kopfhautschuppen | – |

**Ergebnis Cross-Check**: 0 zusätzliche Edits. ir_clinical_kopfhautserum (Edit C, 13.06.) bleibt der einzige übersehene Treffer im Default-Pool. Stufe 1 damit vollständig: 6 non-Default + 1 Cross-Check-Treffer auditiert, 2 Edits (A+C) gefahren, 0/7 Routing-Drift.

**Block 2 Stufe 2a** — `haarstaerke`-Spalte (Pool-Filter, Node 08 Z. 110-113), abgeschlossen 2026-06-16. Audit aller 16 non-default-Produkte: alle K-08-belegt (Header-Untertitel sagt explizit „Feines/Mittleres/Dickes Haar"). Bei 2 smoothing-Produkten mit „Alle Haartypen"-Header gewinnt die konkretere IDEAL-FÜR-Bullet (K-03). Cross-Check der 21 Default-Produkte: 0 übersehene Treffer (curl_*-Anwendungs-Hinweise und FUNKTIONIERT-GUT-MIT-Cross-References zählen nicht als K-03/K-08-Beleg; moxie_mousse explizit „alle Haartypen" im Header + FAQ). **Keine Edits, keine Drift.**

**Block 2 Stufe 2b** — `haarstruktur`-Spalte (TOT in Node 12 v2, Stammdaten-Audit für künftige Reaktivierung), abgeschlossen 2026-06-16. Cross-Audit aller 37 PDFs: nur 4 von 37 differenzieren Locken-Eignung explizit (curl_auffrischer/creme/gelee bereits korrekt im Sheet, plus super_feuchtigkeitsmaske als übersehener Treffer). **1 Edit**: `super_feuchtigkeitsmaske.haarstruktur` = `wellig,lockig,kraus` (Header explizit „Locken, Wellen & Coils / Alle Haartypen / Mittlere bis dicke Haarstruktur"). K-05-Fall: Sheet-Edit ohne Routing-Drift (haarstruktur in Node 12 v2 nicht ausgewertet; Node 17 nutzt `data.normalized.hair_structure` aus Profil, nicht die Produkt-Spalte). Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_100840_pre_haarstruktur_super_maske/produktdatenbank.csv`.

**Block 2 Stufe 3** — `haarzustand`-Spalte (TOT in Node 12 v2), **in Arbeit**. K-08-Header-Audit über 37 PDFs (2026-06-16) ergab 4 Klassen:

| Klasse | Anzahl | Aktion |
|---|---|---|
| K-08-Match (Sheet = Header) | 9 | Status Quo ✓ |
| **K-08-Aufnahme** (Header hat Token, Sheet nicht) | 2 | **2 Edits durchgeführt** |
| K-08-Bestätigung mit Sheet-Plus (Header bestätigt nur Teil) | 8 | K-06-Audit nötig |
| Header fehlt / sagt anderes (Bond-IQ-Layout, curl-Linie, essig, monat_black, rejuvabeads/oel) | 18 | K-06-Vollaudit zwingend |

**Edits 2026-06-16** (K-08-Aufnahmen, beide K-05-Fälle):
- `moxie_mousse.haarzustand` = `kraftlos,frizz` → `kraftlos,frizz,duenn` (Header „Volumen und Dichte" → duenn-Profil)
- `volumen_spray.haarzustand` = `kraftlos` → `kraftlos,duenn` (Header „Volumen und Dichte" → duenn-Profil)

Vokabular-Mapping Wirkungs-Sprache (PDF-Header) → Profil-Sprache (Sheet/Profil):
- `Trockenheit` / `Trockenes Haar` → `trocken`
- `Volumen` → `kraftlos`
- `Verdichtend` / `Volumen und Dichte` → `duenn`
- `Frizz` → `frizz`
- `Schäden` / `Haarbruch` → `haarbruch`
- `Spliss` → `spliss`
- `glanzlos` / `stumpf` → `glanzlos`
- `stark geschädigt` → `stark_geschaedigt`

Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_110844_pre_haarzustand_k08_aufnahmen/produktdatenbank.csv`. Drift-Check via Code-Inspektion (T-02): Node 12 v2 hat keine Referenzen auf `haarzustand`, Node 17 nutzt `rawInput.hair_condition` aus Profil (nicht Produkt-Spalte). **0/7 Routing-Drift möglich, kein Test-Run nötig.**

**Stufe 3 K-06-Vollaudit Cluster 1** (Bond-IQ-Linie 4 + Curl-Linie 3) — abgeschlossen 2026-06-16. 4 Edits (alle Bond-IQ), Curl-Linie unverändert:

| Produkt | Vorher | Nachher | Begründung |
|---|---|---|---|
| `bond_iq_shampoo` | `stark_geschaedigt,haarbruch,spliss` | `stark_geschaedigt,haarbruch,trocken,frizz` | −spliss (K-06: nur Baobab-Inhaltsstoff, nicht Produktversprechen); +trocken („Spendet Feuchtigkeit" + 89%-Test „trockenem/strapaziertem Haar"); +frizz („Bändigt Frizz") |
| `bond_iq_spuelung` | `stark_geschaedigt,haarbruch,spliss` | `stark_geschaedigt,haarbruch,trocken,frizz` | −spliss (K-06: nur Baobab-Inhaltsstoff); +trocken („Spendet intensive Feuchtigkeit"); +frizz (89%-Test anchored „glättet die Schuppenschicht") |
| `bond_iq_leave_in` | `stark_geschaedigt,haarbruch` | `stark_geschaedigt,haarbruch,trocken,frizz` | +trocken („Versorgt trockenes und geschädigtes Haar mit tiefenwirksamer Feuchtigkeit"); +frizz („Glättet Frizz") |
| `bond_iq_night_day_serum` | `stark_geschaedigt,spliss` | `stark_geschaedigt,spliss,haarbruch,trocken,frizz` | +haarbruch („um Haarbruch vorzubeugen", 2× im Produktversprechen); +trocken („Spendet Feuchtigkeit"); +frizz („bändigt Frizz" + 91%-Test) |

Curl-Linie (`curl_auffrischer`, `curl_creme`, `curl_gelee`) unverändert auf `trocken,frizz` — PDF-Belege ausreichend, keine zusätzlichen Tokens belegt.

**2 Spliss-Entfernungen** (shampoo + spuelung) sind exakte K-06-Analogie zur Bond-IQ-bonding-Entfernung vom 2026-06-11 (Inhaltsstoff-Mechanik zählt nicht als Produktversprechen). Konsistenzprinzip: symmetrisch für Aufnahme/Entfernung.

Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_143526_pre_bondiq_haarzustand_k06/produktdatenbank.csv`. **Slot-Disjunktheit verifiziert** (4 Bond-IQ in 4 verschiedenen slot_typs: shampoo/spuelung/leave_in/nacht_serum), Edit-Modus diff-isoliert (1 Run nach allen 4). Test-Suite-Vollrun: alle 7 Profile pre↔post **Set-identisch** (0/7 Drift), via direktem API↔API-Vergleich verifiziert (ex393-400 vs ex401-407).

**Methodische Lehre**: Drift-Vergleich künftig immer direkt API↔API (Set-Vergleich), nicht gegen Listings in Session-Doku — die Session-Doku vom 2026-06-16 Vormittag listete Bianca und Maria mit zu wenigen Produkten, was beim ersten Vergleich falsche Drift-Treffer produzierte.

**Stufe 3 K-06-Vollaudit Cluster 2 Teil A** (4 ohne-K-08-Beleg: essig_shampoo, essig_spuelung, monat_black, rejuvabeads, rejuveniqe_oel) — abgeschlossen 2026-06-16 abends. 4 Edits, 1 unverändert:

| Produkt | Vorher | Nachher | Begründung |
|---|---|---|---|
| `essig_shampoo` | `glanzlos` | `glanzlos` (unverändert) | „glanzlos" explizit in WARUM-DU-Versprechen verankert; keine weiteren Tokens PDF-belegt (Apfelessig-Glanz an geschädigtem Haar = Inhaltsstoff-Mechanik, K-06 raus) |
| `essig_spuelung` | `glanzlos` | `glanzlos,trocken` | +trocken (WARUM „hydratisiert Haar"; IDEAL „mit Feuchtigkeit versorgt"; WARUM-DU „bewahren die Feuchtigkeit"; 12 %-Test). glanzlos bestätigt (WARUM-DU „Glanz", IDEAL „glänzend macht", 64 %-Test, SCHON-GEWUSST „stumpf und leblos") |
| `monat_black` | `kraftlos` | `kraftlos,duenn` | +duenn (K-08 Header-Untertitel „Verdichtend" + IDEAL „Die Dichte verbessern und das Haar voller erscheinen lassen"). Exakte Analogie zu moxie_mousse + volumen_spray vom Vormittag. kraftlos bestätigt („voller erscheinen") |
| `rejuvabeads` | `spliss,trocken,haarbruch` | `spliss,haarbruch,frizz` | **−trocken (K-06: nirgends im PDF erwähnt — weder „trocken" noch „Feuchtigkeit" noch „Trockenheit")**; +frizz (IDEAL „Verknotungen und Frizz … reduzieren möchten"). spliss + haarbruch via K-08 Header und WARUM/IDEAL/Beschreibung verankert |
| `rejuveniqe_oel` | `trocken,glanzlos` | `trocken,glanzlos,frizz` | +frizz (WARUM „Glättet die Schuppenschicht, um Frizz zu reduzieren", IDEAL „Frizz kontrollieren", ANWENDUNG „Frizz und abstehende Haare zu bändigen"). trocken + glanzlos PDF-verankert |

**Erste K-06-konforme haarzustand-Entfernung außerhalb Bond-IQ-Linie**: `rejuvabeads.trocken` raus. Das Wort „trocken" / „Feuchtigkeit" / „Trockenheit" kommt im rejuvabeads-PDF nirgendwo vor (kein WARUM, IDEAL, VORTEILE, Beschreibung, SCHON-GEWUSST). Cross-Reference auf REJUVENIQE-Inhaltsstoff zählt nicht (K-06 Mechanik-Ausschluss). Vermutlich ChatGPT-Erbe-Wert aus Vor-Audit-Zeit. Symmetrie-Bestätigung: K-06 wirkt nicht nur bei Funktions-Spalten (bond_iq.bonding, smoothing_tiefenbehandlung.feuchtigkeit, renew_spuelung.glanz, curl_creme.elastizitaet …), sondern auch bei Filter-Spalten.

Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_203135_pre_block2_stufe3_cluster2_4ohne_k08/produktdatenbank.csv`. **Slot-Disjunktheits-Befund**: 4 Edits in 4 verschiedenen `slot_typ` (spuelung, shampoo, leave_in, finish). Konflikt-Slot shampoo nur mit Variable monat_black (essig_shampoo unverändert), daher diff-isoliert sicher. Test-Suite-Vollrun: alle 7 Profile pre↔post **Set-identisch** (0/7 Drift), via direktem API↔API-Vergleich verifiziert (ex401-407 vs ex408-414). Pipeline-Latenz erneut ~3 min/Profil, Polling-Cascade-Workaround per API-Direkt-Read.

**Stufe-3-Gesamtbilanz** — abgeschlossen 2026-06-17:

| Klasse | Anzahl | Stand |
|---|---|---|
| Cluster 1 (Bond-IQ + Curl) | 7 | ✅ 4 Edits, 0/7 Drift |
| Cluster 2 Teil A (4 ohne-K-08 + monat_black) | 5 | ✅ 4 Edits, 0/7 Drift |
| Cluster 2 Teil B Sub-Cluster 2B-1 (5 Default-Produkte) | 5 | ✅ 3 Edits, 0/7 Drift |
| Cluster 2 Teil B Sub-Cluster 2B-2 bis 2B-6 (12 Produkte) | 12 | ✅ 10 Edits, 0/7 Drift |
| K-08-Aufnahme (moxie_mousse, volumen_spray) | 2 | ✅ Vormittag 2026-06-16 |
| K-08-Match (Sheet = Header exakt, Status Quo) | 6 | ✅ kein Audit nötig |
| **Gesamt** | **37** | **✅ 37/37 abgeschlossen** |

**Korrektur zur Vormittag-Klassifizierung**: 3 IR-Clinical-Produkte (`ir_clinical_kopfhautserum`, `ir_clinical_shampoo`, `ir_clinical_spuelung`) waren als K-08-Match geführt, sind streng aber K-08-Bestätigung: Sheet hat `duenn,kraftlos`, Header sagt nur „Verdichtend" → K-08 belegt nur `duenn` (Vokabular-Mapping: „Verdichtend"/„Volumen und Dichte" → duenn; „Volumen" → kraftlos sind getrennte Mappings). `kraftlos` braucht K-06-Verifikation. Pending-Anzahl somit 14 → 17.

**Stufe 3 K-06-Vollaudit Cluster 2 Teil B Sub-Cluster 2B-2 bis 2B-6** (12 Produkte: super_feuchtigkeitsmaske + Renew/Replenish-Trio + IR-Clinical-Trio + Smoothing-Trio + Feuchtigkeit-Duo) — abgeschlossen 2026-06-17. 10 Edits, 2 unverändert. **6 K-06/K-07-Entfernungen + 8 Aufnahmen** = größte Audit-Welle der gesamten Stufe 3:

| Sub | Produkt | Vorher | Nachher | Aktion |
|---|---|---|---|---|
| 2B-2 | `super_feuchtigkeitsmaske` | `trocken,frizz,glanzlos` | `trocken,glanzlos` | **−frizz K-06** (nur Inhaltsstoff-Bullets „Aminosäure-Komplex"/„Macadamia-Öl", kein Produktversprechen) |
| 2B-3 | `renew_shampoo` | `trocken,glanzlos` | unverändert | WARUM „Glanz" + IDEAL „glänzendes" verankert |
| 2B-3 | `renew_spuelung` | `trocken,glanzlos` | `trocken` | **−glanzlos K-06** (Wort „Glanz" / „glänzend" nirgendwo im renew_spuelung-PDF — Cross-Reference auf Replenish zählt nicht). Exakte Analogie zur `renew_spuelung.glanz`-Entfernung aus `nebenfunktionen` vom 2026-06-12 |
| 2B-3 | `replenish_maske` | `trocken,glanzlos` | unverändert | WARUM-DU „Glanz wiederherstellen" + WARUM/IDEAL verankert |
| 2B-4 | `ir_clinical_kopfhautserum` | `duenn,kraftlos` | `duenn,kraftlos,haarbruch` | +haarbruch (WARUM-DU „Haarbruch sofort reduziert" + IDEAL „Haarausfall beim Bürsten" + 92 %-Test) |
| 2B-4 | `ir_clinical_shampoo` | `duenn,kraftlos` | `duenn,kraftlos,haarbruch` | +haarbruch (WARUM „84 % Haarausfall" + „Schäden verhindern" + IDEAL „Haarbruch erleben"). 89 %-Glanz-Test ohne Versprechen → K-07 NICHT |
| 2B-4 | `ir_clinical_spuelung` | `duenn,kraftlos` | `duenn,kraftlos,haarbruch` | +haarbruch (WARUM „91 % Haarausfall" + „Schäden" + IDEAL „Haarbruch"). Glanz-94 %-Test bleibt draußen (K-07-Original-Präzedenz vom 2026-06-12 bestätigt) |
| 2B-5 | `smoothing_deep_conditioner` | `frizz,trocken` | `frizz,trocken,haarbruch` | +haarbruch (WARUM „7x weniger Haarbruch" + IDEAL „weniger Haarbruch wünschen" + 87 %-Test). 56 %-Glanz-Test ohne Versprechen → K-07 NICHT |
| 2B-5 | `smoothing_shampoo` | `frizz,glanzlos` | `frizz,haarbruch` | **−glanzlos K-07** (24 %-Test ohne Versprechen-Verankerung) + +haarbruch (WARUM „weniger Haarbruch" + 68 %-Test). Exakte Analogie zu `ir_clinical_spuelung.glanz`-Entfernung vom 2026-06-12 |
| 2B-5 | `smoothing_tiefenbehandlung` | `frizz,trocken` | `frizz,haarbruch` | **−trocken K-06** (Feuchtigkeit nirgendwo im PDF für die Maske selbst; nur Conditioner-Produkttyp-Rückschluss) + +haarbruch (WARUM „91 % Haarbruch" + Test). Exakte Analogie zur `smoothing_tiefenbehandlung.feuchtigkeit`-Entfernung aus `nebenfunktionen` vom 2026-06-11 |
| 2B-6 | `erweiterte_feuchtigkeit_spuelung` | `trocken,frizz` | `trocken,glanzlos` | **−frizz K-06** (Frizz nirgendwo im PDF — kein WARUM, IDEAL, ERGEBNISSE) + +glanzlos (WARUM-DU „strahlendem Glanz" + WARUM „glänzenderes" + 98 %-Test) |
| 2B-6 | `feuchtigkeits_shampoo` | `trocken,frizz` | `trocken,glanzlos` | **−frizz K-06** (Frizz nirgendwo im PDF) + +glanzlos (WARUM-DU „strahlendem Glanz" + WARUM „glänzenderes" + IDEAL „Glanz erhöhen" + 82 %-Test) |

**Drei historische K-06/K-07-Analogien bestätigt** für die haarzustand-Spalte:
- `renew_spuelung.glanzlos` ↔ `renew_spuelung.glanz` aus `nebenfunktionen` (2026-06-12, K-07)
- `smoothing_shampoo.glanzlos` ↔ `ir_clinical_spuelung.glanz` aus `nebenfunktionen` (2026-06-12, K-07)
- `smoothing_tiefenbehandlung.trocken` ↔ `smoothing_tiefenbehandlung.feuchtigkeit` aus `nebenfunktionen` (2026-06-11, K-06)

Damit ist die haarzustand-Spalte mit den gleichen K-06/K-07-Kriterien wie `nebenfunktionen` saniert. Spalten-übergreifende Konsistenz für jedes Produkt erreicht.

**Frizz-Erbe-Cluster in Feuchtigkeit-Linie**: erweiterte_feuchtigkeit_spuelung + feuchtigkeits_shampoo hatten beide `frizz` im Sheet, das in keinem der beiden PDFs erwähnt wird. Klassisches ChatGPT-Erbe (vermutlich thematische Nähe „glatteres Haar" → „weniger Frizz").

**IR-Clinical-Linie haarbruch-Lücke**: Alle 3 IR-Clinical-Produkte haben Haarausfall/Haarbruch als primäres Versprechen mit Tests (92 %/84 %/91 %), aber das Token fehlte komplett im Sheet. Klassisches K-08-Erbe (Header sagt nur „Verdichtend", also wurde „duenn" + „kraftlos" gesetzt; aber WARUM/IDEAL sind viel breiter).

Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_231557_pre_block2_stufe3_cluster2b_rest/produktdatenbank.csv`. **Slot-Konflikt verifiziert** (4 Edits in slot_typ=spuelung, 3 in shampoo, 2 in maske, 1 in kopfhaut_taeglich — nicht disjunkt). Aber haarzustand ist tot in Node 12 v2 (T-02 Code-verifiziert: keine Referenzen) → **diff-isoliert sicher trotz Konflikt, K-05-Fall, Routing-Wirkung null**. Test-Suite-Vollrun: alle 7 Profile pre↔post **Set-identisch** (0/7 Drift), via T-03 API↔API-Vergleich verifiziert (ex415-421 vs ex422-428).

---

**Stufe 3 K-06-Vollaudit Cluster 2 Teil B Sub-Cluster 2B-1** (5 Default-Produkte mit haarzustand=`-`: hitzeschutzspray, kopfhaut_peeling, scalp_comfort_behandlung, scalp_comfort_serum, the_champ) — abgeschlossen 2026-06-16 abends. 3 Aufnahme-Edits, 2 unverändert:

| Produkt | Vorher | Nachher | Begründung |
|---|---|---|---|
| `hitzeschutzspray` | `-` | `haarbruch` | +haarbruch (WARUM „Schäden und Haarbruch vermeiden" + IDEAL „Stärke und Elastizität verbessern" + SCHON-GEWUSST „Haarbruch" + Test „Stärke und Elastizität"). Glanz-95 %-Test NICHT aufgenommen: IDEAL sagt „Glanz **bewahren**" (vor Hitze-Verlust), nicht „glanzlos heilen" — K-04 strikt, Produkt adressiert nicht glanzlos-Profil |
| `kopfhaut_peeling` | `-` | `glanzlos` | +glanzlos (WARUM-DU explizit „abgestorbene Hautzellen, Produktablagerungen und Umweltschadstoffe aufzulösen, **die das Haar glanzlos erscheinen lassen**"). Feuchtigkeit-Erwähnung („Angereichert mit REJUVENIQE® spendet es Feuchtigkeit") in Verbund-Aussage zu schwach für trocken — Hauptthema Reinigung |
| `scalp_comfort_behandlung` | `-` (unverändert) | — | Alle „Trockenheit"-Erwähnungen (Header + 89 %-Test + 96 %-Test + IDEAL) sind explizit **Kopfhaut-Trockenheit**, nicht Haar. K-04-Disziplin: kopfhaut-Probleme gehören in `kopfhaut`-Spalte (dort `trocken,empfindlich,schuppig,gereizt` bereits belegt) |
| `scalp_comfort_serum` | `-` (unverändert) | — | Identische K-04-Grenzfall-Argumentation wie scalp_comfort_behandlung |
| `the_champ` | `-` | `kraftlos` | +kraftlos (WARUM „**Verleiht Volumen** und Textur"). Volumen → kraftlos per Vokabular-Mapping. Volumen-Boost ist bekannter Trockenshampoo-Effekt |

**Methodische Lehre — Spalten-Disziplin Kopfhaut vs. Haar**: Scalp-Comfort-Linie ist Lehrbeispiel für K-04 bei mehrdeutigen Begriffen. PDF erwähnt 4× „Trockenheit" + 2× „Feuchtigkeit" — aber alle Belege referenzieren explizit `Kopfhaut`, nicht Haar. Auf Vermutung „trocken hier auch im Haar?" zu setzen wäre genau der K-04-Fehler, den die Konvention verhindern soll. **Spalten-Trennung Sheet-architektonisch zwingend**: haarzustand-Vokabular gilt nur für Wirkungs-Aussagen am Haar, kopfhaut-Probleme gehören in die kopfhaut-Spalte.

**Methodische Lehre — Glanz „bewahren" vs. „heilen"**: hitzeschutzspray adressiert Glanz-Erhalt (Schutz vor Hitze-bedingtem Glanz-Verlust), nicht Glanz-Wiederherstellung am bereits glanzlosen Haar. K-04 strikt: ein Profil-Match „glanzlos" würde das Produkt fälschlich für Anti-glanzlos-Bedarf empfehlen, statt für Hitze-Styling-Schutz. Symptom-Profil ≠ Schutz-Funktion.

Backup: `~/Projekte/myglowmatch/backups/sheets_20260616_220153_pre_block2_stufe3_cluster2b1/produktdatenbank.csv`. **Slot-Disjunktheit verifiziert** (3 Edits in 3 verschiedenen slot_typs: styling_1/kopfhaut/finish), Edit-Modus diff-isoliert. Test-Suite-Vollrun: alle 7 Profile pre↔post **Set-identisch** (0/7 Drift), via direktem API↔API-Vergleich verifiziert (ex408-414 vs ex415-421).

**Stufe 3 ✅ ABGESCHLOSSEN 2026-06-17**: alle 37 Produkte K-06/K-07/K-08-auditiert. Gesamtbilanz Stufe 3: **24 Edits** (4 Cluster 1 + 4 Cluster 2A + 3 2B-1 + 10 2B-2-6 + 2 K-08-Aufnahmen Vormittag + 1 K-08-Aufnahme nebenwirkend) bei **0/7 Drift** über alle Edit-Wellen.

**Aggregierte Cluster-2-Teil-B-2-bis-6-Befunde** zeigen größtes Erbe-Risiko genau dort, wo es methodisch erwartet wurde: bei den K-08-Bestätigungen mit Sheet-Plus. 6 K-06/K-07-Entfernungen bei 12 auditierten Produkten = **50 % ChatGPT-Erbe-Quote in dieser Klasse**, vs. 1 Entfernung (rejuvabeads.trocken) bei 5 Cluster-2A-Produkten und 0 Entfernungen bei 7 Cluster-1-Produkten. Lehre: **K-08-Bestätigung-Klasse hatte die meisten unbelegten Plus-Tokens**, weil Header-Token korrekt ist und Plus-Tokens als „naheliegend" gesetzt wurden ohne PDF-Verifikation.

**Nächster Schritt: Node 12 v3 Reaktivierung** — `haarzustand` als zusätzliche Ranking-Stufe einbauen. Vorgehen:

1. Node 12 v2 → v3 Design: `haarzustand` als **Stufe 1.5** zwischen aktuell Stufe 1 (Hauptfunktion-Match via map_profil_funktion) und Stufe 2 (Score). `rawInput.hair_condition` → Produkt-`haarzustand`-Token-Match via Set-Schnittmenge, lexikographisch.
2. Parallel `haarstruktur` als Stufe 4 einbauen (3 PDF-belegte Differenzierungen aus 2026-06-16-Audit).
3. Vor Deploy: Trace-Update analog Node-12-v2-Deploy (`fired_rules` um `RANK-haarzustand` und `RANK-haarstruktur` ergänzen).
4. Regression: 7-Profil-Vollrun, **Routing-Drift erwartet** (anders als bisher) — manueller Profil-für-Profil-Check ob neue Differenzierungen sinnvoll sind. Bei Sarah z.B. spielt jetzt `stark_geschaedigt`-Match auf Bond-IQ-Linie eine Rolle.
5. Sobald validiert: Block 3 (Bool-Flags + Pflegelevel + ausschluss_bei) und Block 4 (Doku-Spalten) als Folge-Sessions.

## Scoring-Audit & Node-12-Trace (2026-06-15)

Anlass: Tomi-Grundsatzfrage zu Sinnhaftigkeit/Determinismus/Skalierbarkeit der Punkteverteilung. Audit zeigte: System A (Node 06 Pflegelevel) ist sheet-getrieben + plausibel (Doku-Schuld bei Punkt-Höhen, kein Logik-Bug); System B (Node 12 Produkt-Slot-Score, 6 Inline-Regeln) hat drei Quirks (haarstruktur-Asymmetrie, Doppelzählung Hauptfunktion+Goal, Tie-Breaking via Sheet-Reihenfolge) plus zwei Architektur-Probleme (Inline-Gewichte, keine Score-Aufschlüsselung im Output). Block-2-Audit ist **pausiert** bis Scoring-Reparatur, weil jeder neue `nebenfunktionen`-Token durch die ungeprüfte Doppelzählungs-Logik läuft.

**Schritt 1 abgeschlossen** — Node 12 Trace-Erweiterung (deployed 2026-06-15):

`scoreProduct(prod)` liefert jetzt `{score, fired_rules}` statt nur `score`. Pro Slot-Winner erscheint im Output:
- `fired_rules: [{regel_id, punkte, beschreibung}, …]` — je Score-Regel ein Eintrag mit konkretem Match-Beleg (z.B. „care_goal 'volumen' matcht funktion 'volumen' (Substring)")
- `score_competition: [{produkt_key, score}, …]` — Top-5 Konkurrenz für Tie-Breaking-Sichtbarkeit

6 Score-Regeln nummeriert: SCO-01 (hauptfunktion +3), SCO-02 (kopfhaut +2), SCO-03 (haarstruktur +1, Match-Asymmetrie explizit im Beschreibungstext kommentiert), SCO-04 (care_goal +1 pro Match), SCO-05 (pflegelev +1), SCO-06 (needs_curl_care +2). Score-Werte sind mathematisch identisch zur Pre-Edit-Logik — kein Routing-Drift möglich.

**Backup**: `~/Projekte/myglowmatch/workflow_backup_20260615_215307_pre_node12_trace.json`.

**Regression**: 6/7 Profile produkt_key-identisch zur Pre-Edit-Baseline (`test_results_20260613_095740.json`). Anna's Vollrun-Polling-Timeout (90s) ist Test-Suite-Artefakt (Cold-Start beim ersten Webhook), Einzel-Re-Run lief sauber durch mit identischer Routine. **0/7 echter Drift**.

**Beobachtungs-Beispiel** (Maria's shampoo-Slot): Winner revive_shampoo Score=4 (SCO-04 +1 volumen-Match, SCO-05 +1 mid-Match, SCO-06 +2 Curl-Bonus) gegen 3 Konkurrenten mit je Score=3 (feuchtigkeits_shampoo, ir_clinical_shampoo, monat_black). Curl-Bonus ist Slot-entscheidend — fragwürdig bei einem welligen Profil. Für Schritt-2-Diagnose vermerkt.

**Schritt 2 abgeschlossen** — 7-Profile-Trace-Analyse 2026-06-15 (Daten: test_results_20260615_220545.json + _223627.json):

- **SCO-01 (hauptfunktion +3) ist toter Code**: 0 von 36 Slots. Grund: `primary_hair_condition` ist Profil-Sprache (`trocken`, `kraftlos`, `stark_geschaedigt`, `keine_probleme`), `hauptfunktion` ist Wirkungs-Sprache (`feuchtigkeit`, `volumen`, `reparatur`, `reinigung`). Substring-Match findet keine Treffer. → **Vokabular-Gap** ist die Wurzel des Problems, nicht die Punkt-Werte.
- **Echte Hauptlogik ist SCO-04** (Goals, 33/36 Slots = 92 %). Funktioniert nur weil care_goals im Frontend bereits in Wirkungs-Sprache formuliert sind (`reparatur`, `feuchtigkeit`, `volumen`, `glanz`, `verdichtend`, `gesunde_kopfhaut`, `frizz_reduktion`) — glücklicher Zufall, kein Plan.
- **Doppelzählung-Befund: 0 Treffer**. Da SCO-01 nie feuert, kann es nie mit SCO-04 doppelt zählen. Mein ursprünglicher Audit-Punkt 3 ist nie eingetreten.
- **SCO-05 (pflegelev) +1 feuert in 100 %** — Konstant-Bias, differenziert nichts.
- **SCO-06 (Curl-Bonus +2) feuert in 86 %** — Maria's revive_shampoo gewinnt z.B. über monat_black nur wegen Curl-Bonus.
- **25 % der Slots werden per Sheet-Reihenfolge entschieden** (9 Ties in 36 Slots). Bianca bekommt 3 von 5 ihrer Routine-Produkte faktisch zufällig.

**Schritte 3-5 abgeschlossen** — Node 12 Rewrite auf Ranking-Hierarchie + map_profil_funktion (deployed 2026-06-16):

Statt Punkte-Scoring jetzt **lexikographische 6-Stufen-Hierarchie**. Erste Kriterium-Differenz entscheidet. Keine Punkte mehr addiert.

| Stufe | Kriterium | Wert | Quelle |
|---|---|---|---|
| 1 | hauptfunktion-Match | binär (1 wenn `hauptfunktion` enthält gemappten Funktions-Token) | `hauptfunktion` + `map_profil_funktion` (NEU) |
| 2 | Goal-Coverage | Anzahl exakter `care_goals ↔ funktion`-Matches | `care_goals` + Funktions-Spalten |
| 3 | Scalp-Match | binär | `kopfhaut`-Spalte |
| 4 | Curl-Kompatibilität | binär (`needs_curl_care ∧ locken_geeignet`) | `locken_geeignet` + Flags |
| 5 | Pflegelev-Match | binär | `pflegelev`-Spalte |
| 6 | Tie-Breaker | `produkt_key` alphabetisch (deterministisch) | letzter Ausweg |

**Architektur-Wechsel**:
- Mapping-Tabelle `map_profil_funktion` (NEU, 9 Zeilen): `hair_condition`-Werte → Funktions-Tokens. Sheet-getrieben. Behebt das Vokabular-Gap.
- Loader-Node 06d (NEU): lädt `map_profil_funktion`, eingehängt zwischen 06c → 06.
- Node 12 v2: Punkte-Scoring entfernt, Ranking-Hierarchie eingebaut. Pro Slot-Winner im Output: `profile` (alle 5 Match-Werte), `decision_stage` (auf welcher Stufe entschieden), `ranking_top5`, `primary_hf_token`.
- Workflow-Nodes: 24 → **25** (06d hinzugefügt).
- Goal-Match jetzt **exakt** statt Substring (saubere Determinismus).
- **haarstruktur fällt als Score-Faktor weg** — war im Punkte-System eine Asymmetrie-Quelle (Default = Match), bringt aktuell keinen Mehrwert.

**Backups**:
- `~/Projekte/myglowmatch/workflow_backup_20260616_081426_pre_node06d_loader.json` (Pre-Loader)
- `~/Projekte/myglowmatch/workflow_backup_20260616_085825_pre_node12_v2.json` (Pre-v2-Deploy)

**Regression nach v2**: **0/7 echte Routing-Drift**. Alle 7 Profile produkt_key-identisch zur Pre-Reform-Baseline. Vollrun-Polling-Timeouts (mehrere Profile) sind Test-Suite-Artefakt — direkter Execution-API-Read aller 7 success-Executions (ex393-397, ex399-400) bestätigt: gleiche Routinen.

**Decision-Stage-Verteilung** (39 Slots gesamt):

| Stage | Slots | % | Bedeutung |
|---|---|---|---|
| Stufe 1 (hauptfunktion) | 6 | 15.4 % | **NEU**: Mapping wirkt. Maria/Julia/Sarah shampoo+spuelung klar entschieden (vorher tot) |
| Stufe 6 (alphabetisch tie_breaker) | 10 | 25.6 % | Ersetzt das alte Sheet-Reihenfolge-Tie-Breaking — jetzt deterministisch |
| alone (Pool = 1) | 23 | 59.0 % | kein Wettbewerb |
| Stufe 2-5 | 0 | 0 % | in den 7 Profilen nie entscheidend (siehe Anmerkung) |

**Anmerkung Stufe 2-5**: In den 7 Test-Profilen sind die Top-Kandidaten meist in allen 5 Score-Kriterien identisch (Beispiel Bianca-shampoo: 4 Feuchtigkeits-Shampoos haben alle hf=1, goalCount=1, scalpMatch=0, curlMatch=1, plMatch=1 → Stufe 6 entscheidet). Das ist **keine Schwäche der Hierarchie**, sondern eine Aussage über die Produkt-Stammdaten (viele austauschbare Produkte für dasselbe Bedarfsprofil). Falls künftig stärkere Differenzierung gewünscht: eigene Stufe „Produktlinien-Konsistenz" oder neue Spalte „Wirkstärke" — als Folge-Idee notiert, aktuell kein Handlungsbedarf.

**Erklärbarkeits-Ergebnis**: Pro Kundenempfehlung jetzt sagbar — Sarah „Bond-IQ-Shampoo weil Reparatur deine Hauptanforderung ist" (Stufe 1), Bianca „feuchtigkeits_shampoo — 4 gleichwertige Feuchtigkeits-Shampoos verfügbar, deterministisch alphabetisch ausgewählt" (Stufe 6), Anna „MONAT BLACK — einziges Shampoo für deine fettige Kopfhaut" (alone). Keine willkürlichen Punkt-Werte mehr zu verteidigen.

**Block-2-Audit reaktiviert**: das Vokabular-Gap der Score-Engine war der einzige Pause-Grund. Audit kann mit Stufe 2 (`haarstruktur` + `haarstaerke`) fortgesetzt werden.

## Offene Punkte (priorisiert)

| Prio | Aufgabe | Stelle |
|---|---|---|
| 🟡 (in Arbeit) | Datenblatt-Provenienz-Audit — **Block 1 abgeschlossen** 2026-06-12; **Block 2 Stufe 1 (`kopfhaut`) abgeschlossen** 2026-06-15; **Block 2 Stufe 2a (`haarstaerke`) abgeschlossen** 2026-06-16 (0 Edits, 0 Funde); **Block 2 Stufe 2b (`haarstruktur` für Reaktivierung) abgeschlossen** 2026-06-16 (1 Edit super_feuchtigkeitsmaske, K-05); **Block 2 Stufe 3 (`haarzustand`) abgeschlossen** 2026-06-17 (K-06-Cluster 1 Bond-IQ+Curl 4 Edits 2026-06-16; Cluster 2 Teil A 4 Edits 2026-06-16; Cluster 2 Teil B Sub-Cluster 2B-1 3 Edits 2026-06-16; Sub-Cluster 2B-2..2B-6 10 Edits 2026-06-17 inkl. 6 K-06/K-07-Entfernungen; K-08-Aufnahmen 2 Edits Vormittag 2026-06-16 + 1 K-08-Aufnahme nebenwirkend; **gesamt 24 Edits über 37 Produkte, 0/7 Drift**); **Block 3 K-01-Bool-Flag-Konsistenz-Audit abgeschlossen** 2026-06-18 (1 Edit hauptfunktion+kopfhautpflege bei ir_clinical_kopfhautserum, 0/111 K-01-Inkonsistenzen, 0/35 Drift); **Block 3 Pflegelevel-Konzept-Klärung abgeschlossen** 2026-06-19 (kein PDF-strikter Stammdaten-Audit möglich — Pflegelevel ist Synthese-Größe ohne explizite Marker; Cross-Check `intensitaet↔pflegelevel` zeigt 12 mechanische Verstöße, aber alle 12 PDF-legitim); **Block 3 `ausschluss_bei`-Audit abgeschlossen** 2026-06-19 (Konvention K-10 etabliert, 37 PDFs auditiert via Agent, 0 neue Edits — Spalte legitim untergenutzt, MONAT-PDFs sprechen Whitelist statt Blacklist, 6 Redundanzen mit CON-02/09/12). **Block 2 + Block 3 damit komplett.** **Block 4 abgeschlossen 2026-06-22**: `locken_geeignet` (Konvention K-11 etabliert, 0 Edits, 37/37 TRUE PDF-haltbar); `anwendung` (17 Edits über 17 Produkte — 5 aus Agent-Pre-Verifikation + 2 K-04-Pflicht + 10 Konkretisierungen, 0 Routing-Drift erwartet weil Doku-Spalte für Node 17); `produkt_url` (37/37 leer, 0 Workflow-Konsumenten — Integration in der Vergangenheit als nicht umsetzbar verworfen, in „Bewusste Lücken" dokumentiert). **Datenblatt-Provenienz-Audit damit komplett über alle 4 Blöcke und 37 Produkte.** | siehe „Datenblatt-Provenienz-Audit" oben |
| 🟢 (erledigt 2026-06-17/18) | **Node 12 v3+v4 Reaktivierung `haarzustand`+`haarstruktur`+`haarstaerke`+`intensitaet`** als zusätzliche Ranking-Stufen. v3: 6→10 Stufen, 4/7 Drift (3× super_feuchtigkeitsmaske via Stufe 6, 1× volumen_spray via Stufe 8), alphabetischer Fallback 10/39→5/39. v4: +Stufe 11 `intensitaet` mit `wants_intense_care`-Heuristik (Node 05) + neue Sheet-Spalte `intensitaet` (`leicht`/`intensiv`/`alle`, 8 Tie-Produkte K-08-belegt, Rest Default), 1/7 Drift (Bianca shampoo+spuelung feuchtigkeits→renew), alphabetischer Fallback 5/39→**0/39**. Siehe Migration #8. | Node 12 v4, siehe „Datenblatt-Provenienz-Audit" Stufe 3 + Migrationsstand #8 oben |
| 🟢 (erledigt 2026-06-22) | **Block 4 Doku-Spalten-Audit abgeschlossen — Datenblatt-Provenienz-Audit damit komplett.** Drei Spalten: (1) **`locken_geeignet`** — Konvention **K-11 etabliert** (exakter Wortlaut der Konvention in der separaten Session-Doku, hier nur Befund): 37/37 als TRUE PDF-haltbar bestätigt, 0 Edits. (2) **`anwendung`** — 17 Edits über 17 Produkte (Backups: `backups/sheets_20260622_pre_block4_anwendung/`, `_klasse_a/`, `_klasse_b/`). Welle 1: 5 Pre-Edit-Verifikationen aus Agent-Vorschlägen (T-02-konform: PDFs selbst gelesen) — erweiterte_feuchtigkeit_spuelung, feuchtigkeits_shampoo, ir_clinical_kopfhautserum, ir_clinical_spuelung, renew_spuelung; davon 2 K-04-Drift-Behebungen (Sheet sagte 1–3 Min, PDF 1–2 bzw. 3–5 Min). Welle 2 (32 Produkte from-scratch ohne Agent): 2 K-04-Pflicht-Edits — `smoothing_fohn_spray` Copy-Paste-Bug (Sheet-Wert war wortgleich mit `fohncreme`, Produkte sind aber unterschiedlich: PDF sagt „Spray, gut schütteln, auf feuchtes Haar aufsprühen") + `smoothing_tiefenbehandlung` Frequenz-Widerspruch (Sheet „1-2 Mal pro Woche" vs PDF „ideal für die tägliche Pflege"). Welle 3: 10 Konkretisierungs-Edits (Methoden-/Mengen-/Trocknungs-/Einwirkzeit-Details, K-04-konform). Highlight: `rejuveniqe_oel` um die im PDF beschriebenen 3 Anwendungsvarianten (Vor-Shampoo / Intensiv-Behandlung / Leave-in Finish) erweitert, statt nur eine Variante zu zeigen. Restliche 20 Produkte: identisch oder marginal — keine Edits. **Drift Pre↔Post (Executions 458-464 ↔ 465-471): 0/36** — Validierungs-Full-Run am 2026-06-22 empirisch bestätigt, dass `anwendung` ausschließlich in Node 17 (E-Mail-Templating) gelesen wird, kein Filter/Score. T-03-Polling timed out (7/7), Direct-API-Read-Workaround stabil. (3) **`produkt_url`** — 37/37 leer, 0 Workflow-Konsumenten, kein Audit-Fall (PDFs enthalten keine URLs). Produkt-Link-Integration war Anfangsidee, wurde verworfen weil saubere Einbindung nicht gelang — in „Bewusste Lücken" verschoben. **Methodische Beobachtung**: Welle 2 ohne Agent (32 PDFs vom Hauptmodell direkt gelesen) erwies sich als praktikabel und förderte 2 K-04-Verstöße zutage, die der Agent in Welle 1 nicht im Scope hatte. Lehre: Agent-Delegation ist effizient für strukturierte Vollwellen, aber Hauptmodell-Direkt-Lesen findet auch Copy-Paste-Bugs und semantische Widersprüche zuverlässig. | Sheet `produktdatenbank.anwendung` + `locken_geeignet` |
| 🟢 (erledigt 2026-06-19) | **`ausschluss_bei`-Audit (Block 3 Abschluss) abgeschlossen — 0 neue Edits.** Spalte wirkt als Hard-Pool-Exclusion in Node 08 (Schritt 1 von 4): Token-Match gegen `scalp_status`+`hair_condition`+`hair_structure`+`hair_treatments` entfernt Produkt aus Pool. Baseline: 3/37 belegt (3× Curl mit `glatt`). Konvention K-10 etabliert (zählt: explizite Negativ-Aussagen + funktionale Inkompatibilität; zählt NICHT: Header-Whitelist-Targeting). Token-Vokabular aus `map_system_dictionary` fixiert. **37-PDF-Vollwelle via Agent** (general-purpose, 38 Tool-Uses, 233s): 3 Status-quo bestätigt, 6 Redundanz-Befunde mit CON-02/09/12 (essig_*, kopfhaut_peeling, fohncreme), 1 grenzwertiger Vorschlag (`erweiterte_feuchtigkeit_spuelung→kraus`) bei strikter K-10 abgewiesen (Header-Whitelist „Feine bis mittlere Haartexturen" zählt nicht als Blacklist; funktionales Argument ist Suboptimalität, keine Inkompatibilität), 0 Out-of-Vocabulary-Funde. **Befund**: Spalte legitim untergenutzt — MONAT-Hersteller-PDFs verwenden positives Header-Targeting („Ideal für…"), keine Negativ-Aussagen. Kontraindikationen liegen architektonisch richtig in `map_conflict_rules`. **Cross-Check `intensitaet↔pflegelevel`** (Block-3-Pflegelevel-Konzept) vorab durchgeführt: 12 mechanische Verstöße, alle 12 PDF-legitim — die zwei Spalten sind orthogonal (Wirkungstiefe vs Routine-Engagement), nicht hierarchisch; kein Bug, Cross-Check-Regel selbst zu streng. **Offene Architektur-Frage**: Migration CON-02/CON-09/CON-12 in `ausschluss_bei` (Logik-Verschiebung Sheet-Regel → Sheet-Spalte), wenn gewünscht — kein Stammdaten-Audit, daher separater Task. | Sheet `produktdatenbank.ausschluss_bei` |
| 🟢 (erledigt 2026-06-18) | **K-01-Bool-Flag-Konsistenz-Audit (Block 3 Einstieg) abgeschlossen.** Sheet-weite mechanische Prüfung der 3 ist_*-Spalten gegen `hauptfunktion`-Token (K-01: `ist_X=TRUE ⟺ hauptfunktion enthält X`): `ist_hitzeschutz` 3 TRUE/34 FALSE, `ist_bonding` 1 TRUE/36 FALSE, `ist_scalp_focus` 4 TRUE/33 FALSE. **1 Verdachtsfall** (ir_clinical_kopfhautserum: Flag=TRUE, aber hauptfunktion `verdichtend,haarwuchs` ohne `kopfhautpflege`). PDF-Befund: Kopfhautpflege ist im Produktversprechen verankert (Produktname „Kopfhautserum", direkter Kopfhaut-Auftrag, WARUM-„in Kopaut eindringen", 2/5 IDEAL-FÜR-Bullets Kopfhaut, 8/19 Test-Treffer auf Kopaut) — Gegensatz zu ir_clinical_shampoo (kopfhautpflege nur in Tests, nicht im Versprechen → nicht aufgenommen). **1 Edit**: `ir_clinical_kopfhautserum.hauptfunktion` → `verdichtend,haarwuchs,kopfhautpflege`; Flag bleibt TRUE. **Re-Verifikation**: 0/111 K-01-Inkonsistenzen sheet-weit (37 Produkte × 3 Flags). **Drift Pre↔Post (Executions 450-456 ↔ 458-464): 0/35** — kopfhautserum steht im `kopfhautserum`-Slot, keines der 7 Test-Profile bekommt diesen Slot vergeben (Maria/Bianca-Kopfhaut-Slots gehen an kopfhaut_peeling/scalp_comfort_behandlung). Belegung verbessert Erklärbarkeit, ohne Routing zu kippen — gleiches Muster wie K-08. T-03-Polling-Timeout erneut (7/7), Direct-API-Read-Workaround stabil. Backup: `backups/sheets_20260618_pre_k01_bool_flag_audit/produktdatenbank.csv`. | Sheet `produktdatenbank.hauptfunktion` |
| 🟢 (erledigt 2026-06-18) | **K-08-Audit `intensitaet`-Spalte für 29 Default-`alle`-Produkte abgeschlossen.** PDF-strikte Auswertung aller 29 Datenblätter nach Vokabular-Mapping (leicht: „leicht"/„schwerelos"/„ohne zu beschweren"/„federleicht"/„ultraleicht"; intensiv: „tiefenwirksam"/„intensive"/„reichhaltig"/„ultra-pflegend"/„revolutionär"). **20 Edits** (11 leicht + 9 intensiv), 9 Produkte bleiben `alle` (keine eindeutigen Vokabel-Marker). Verteilung Sheet: 4→15 leicht, 4→13 intensiv, 29→9 alle (Total 37). Drei Edits aus ambivalenten PDFs nach Review: `restore_leave_in`→intensiv (2× „intensive Pflege" vs 1× „ohne zu beschweren"), `rejuveniqe_oel`→intensiv (Produktname „Oil Intensive" + Anwendungs-Modus „Intensive Feuchtigkeitsbehandlung"), `ir_clinical_spuelung`→leicht (Test-Ergebnisse 97%/100%/86%/100% „leichter Conditioner"/„nicht beschwert" gewinnen über WARUM-„reichhaltig"). `bond_iq_leave_in` bleibt `alle` (PDF-Konflikt 3× intensiv-Marker vs explizite „leichte Formel"). **Drift v4→post-Audit: 0/35** (keine Slot-Änderung — Stufe 11 wirkt nur bei Ties, die bei den Audit-Produkten nicht auftraten). Alphabetischer Fallback bleibt 0/35. Backup: `backups/sheets_20260618_pre_k08_intensitaet_audit/produktdatenbank.csv`. | Sheet `produktdatenbank.intensitaet` |
| 🟢 (erledigt 2026-06-16) | **Scoring-Reparatur Node 12** abgeschlossen. Schritte 1-5 alle fertig: Trace eingebaut → Befunde gesammelt → Ranking-Hierarchie deployed (6 Stufen) → `map_profil_funktion`-Sheet als Mapping behebt das Vokabular-Gap → Sheet-First-Architektur konsistent zu Node 06. 0/7 Routing-Drift, Erklärbarkeit pro Slot, deterministisches Tie-Breaking. | siehe „Scoring-Audit & Node-12-Trace"-Block oben |
| 🟢 (erledigt 2026-06-18) | **`ist_bonding`-Linien-Proxy-Misuse-Check abgeschlossen.** Workflow-Code: 0 Treffer. Sheet: 2 Treffer in `map_slot_rules.filter` (REQ-02 `ist_bonding=TRUE` → `bond_iq`; REQ-03 `ist_bonding=TRUE\|reparatur` → `bond_iq\|reparatur`). Beide Filter waren post-K-06 toter Linien-Proxy (0 Match → ungefilterter Pool). Substring-Match auf `produktlinie`+`produkt_key`+`hauptfunktion` ersetzt das Wirkungs-Flag-Pattern. **0/7 Drift, REQ-02 wieder semantisch aktiv**: Sarah's Spülungs-Slot ist jetzt `decision_stage=alone` (REQ-02-Filter verengt Pool auf bond_iq_spuelung, ir_clinical_spuelung rausgefiltert) — vorher musste Stufe 1 zwischen 2 Kandidaten entscheiden. Backup: `backups/sheets_20260618_pre_req02_03_relink/map_slot_rules.csv`. | erledigt |
| 🟢 (geklärt) | `kopfhaut`-Spalte der Produktdatenbank: **Score-Bonus +2 bei scalp-Match, kein Pool-Filter** (Node 12 Z. 26, Code-Zitat im Block-2-Stufe-1-Block). Block-2-Edits wirken als Score-Faktor für künftige Profile mit passendem scalp_status, nicht als Pool-Filter. Cross-Check für `haarstruktur` + `haarzustand` separat noch offen (`haarstaerke` ist verifiziert aktiv als Filter). | Node 12 Z. 26 |
| 🟢 (geklärt 2026-06-13) | **anna/bianca scalp_status-Diskrepanz** war reine HANDOVER-Doku-Unvollständigkeit, kein Bug. test_suite.py ist autoritativ und korrekt: anna `scalp_status=['fettig']` + hair_condition `['keine_probleme']`, bianca `scalp_status=['juckend_empfindlich']` + hair_condition `['trocken']`. HANDOVER-Eingabe-Kurzform (Z. 333 ff.) listete nur hair_*-Felder, nicht scalp_status — daraus entstanden Fehlinterpretation als Test-Profil-Bug. Node 02 macht keine `keine_probleme → fettig`-Normalisierung (Z. 13: nur `dedupArr`). Anna's monat_black-Routine ist funktional korrekt (scalp=fettig + care_goal=gesunde_kopfhaut); bianca's scalp_comfort_behandlung wird durch REQ-05 + CON-02 (beide trigger auf juckend_empfindlich) ausgelöst. **Fix in dieser Session**: Baseline-Tabelle Z. 335-341 um explizite `scalp_status`-Spalte erweitert + Vermerk dass „trocken" bei bianca hair_condition ist. **Lehre**: T-02 (System-State-Belegpflicht) erweitert um Daten-Aussagen — HANDOVER ist abgeleitete Doku, nicht autoritative Quelle. | erledigt |
| 🟢 (erledigt 2026-06-24) | **Node 06 Phase 2 Sheet-getrieben — siehe Migration #10.** Inline-Block (7 LOC Ziele-Bonus mit Cap=2) ersetzt durch Sheet-Regel PFL-23. Neuer Operator `array_count_except`, neue Spalte `max_punkte` in `map_pflegelevel_scoring`. `evalBedingung()` → `applyRule()` (Punkte statt Boolean). 22 bestehende Regeln unverändert. **0/36 Slot-Drift**, `pflegelevel_final` byte-identisch zu Baseline 501-507. Damit ist Node 06 vollständig sheet-getrieben. | Migration #10 |
| 🟢 (erledigt 2026-06-23) | **Node 05 migriert — siehe Migration #9.** 76 LOC inline → 90 LOC JSON-Regel-Evaluator. `volume_sensitivity` als 0-Konsumenten-Duplikat eliminiert. 0/36 Slot-Drift. | Migration #9 |
| 🟢 (erledigt 2026-06-24) | **Cleanup-Welle für 3 unbenutzte Flags abgeschlossen** (`needs_detangling`, `styling_goal_natuerlich`, `needs_protection_focus`). Konsumenten-Verifikation: 0 jsCode-Refs im Live-Workflow (frischer n8n-API-GET in `workflow_live_now.json`), 0 Cross-Refs im 15-Tab-Vollscan (`produktdatenbank`/`map_*`/`beratungs_log`). `heat_use.konsumenten` mitbereinigt (stale Verweis auf `flags.needs_protection_focus` raus). 17→14 Sheet-Zeilen, Phase-Order erhalten. **Drift Pre↔Post (Executions 493-499 vs. Baseline 472-478): 0/36** via Direct-API-Diff (T-03-Pattern). Trigger-Erkenntnis: parallele Webhooks (7 in <1s) ratelimit-en Google-Sheets-API mit „too many requests" — sequenzieller Trigger mit 90s-Gap erforderlich. Backup: `backups/sheets_20260623_pre_node05_cleanup/map_derived_variables.csv`. Skripte: `cleanup_node05_sheet.py`, `validate_cleanup.py`. | Sheet `map_derived_variables` |
| 🟢 (erledigt 2026-06-24) | **T-03-Formalisierung in `test_suite.py` abgeschlossen.** Test-Suite v3 mit zwei Modi: (a) **single** (`--profile <name>`): Trigger + Polling auf 1 success-Execution mit `first_name`-Verifikation, Default-Timeout 360s; (b) **bulk** (`--profile all` / mehrere Profile): sequenzieller Trigger mit 90s-Gap (vermeidet Google-Sheets-Rate-Limit), dann Bulk-Polling alle 15s auf success-Count, dann Detail-Fetch + first_name-Zuordnung pro Profil. Default-Timeout 900s. Verifikations-Lauf 2026-06-24: 7/7 Profile success in ~4 Min (Trigger-Phase ~9 Min sequenziell, Polling-Phase ~4 Min auf letzte Execution). `test_results_*.json` enthält jetzt echte Outputs statt None. Slot-Belegung 36/36 byte-identisch zur Cleanup-Welle-Baseline. Code-Pfade: `run_single()` + `run_bulk()` + `fetch_new_success_executions()`. Konfigurierbar via `--wait` / `--gap`. | `test_suite.py` |
| 🟢 (erledigt 2026-06-24) | **Node 11 Suppress-Regel Sheet-getrieben — siehe Migration #11.** Inline-Block (4 LOC `if minimal → optional=[]`) ersetzt durch Sheet-Regel `REQ-MIN-NO-OPT` mit neuer `prioritaet`-Klasse `suppress_optional`. Phase 5 in Node 11 wertet Side-Effect-Regeln aus. Damit alle Routing-Pfad-Inline-Heuristiken eliminiert. **0/36 Slot-Drift**. | Migration #11 |
| ↑ | (Node 12 Score-Gewichte ⇒ siehe 🔴 Scoring-Reparatur oben) | Node 12 inline |
| 🟢 | `extract_routine_output()`-Workaround in Test-Suite aufräumen | `test_suite.py` (CONFLICT_NODE-Merge seit Pass-Through in Node 12 überflüssig) |
| 🟢 | Sheet-Spalte `gewicht` in Produktdatenbank löschen | (vermutlich bereits leer/weg — Google-Sheets-API liefert sie nicht mehr aus) |
| 🟢 | Sheet-Loader 06a/06b/06c parallelisieren | Performance-Tuning, nur falls Live-Latenz spürbar |

## Referenzprofile (Soll-Werte für Regression)

Test-Profile in `test_suite.py`, alle mit `partner_id=desiree`, `email=info@myglowmatch.de`, `consent_recommendation=true`, `consent_marketing=false`.

| Profil | hair_* Eingabe-Kurzform | **scalp_status** | Pflegelevel | Pkt | Cap | Count | CON-Regeln |
|---|---|---|---|---|---|---|---|
| anna   | glatt, mittel, keine_probleme, unbehandelt, Hitze gelegentlich, minimal | **fettig** | LOW | 0 | 3 | 1 | CON-07 |
| maria  | wellig, fein, duenn, kraftlos, gefaerbt, Hitze nie, ausgewogen | **normal** | MID | 7 | 5 | 5 | CON-09, CON-11, CON-12 |
| lena   | kraus, dick, trocken, frizz, gefaerbt, Hitze sehr_haeufig, bestmoeglich | **normal** | HIGH | 15 | 10 | 7 | CON-09, CON-11 |
| julia  | glatt, fein, kraftlos, unbehandelt, Hitze gelegentlich, ausgewogen | **normal** | MID | 4 | 5 | 4 | CON-07, CON-12 |
| bianca | wellig, mittel, trocken, gefaerbt, Hitze gelegentlich, ausgewogen | **juckend_empfindlich** | MID | 7 | 5 | 5 | CON-02, CON-09 |
| vivien | wellig, dick, keine_probleme, gefaerbt, Hitze regelmaessig, bestmoeglich | **normal** | MID | 4 | 7 | 7 | CON-09, CON-11, CON-12 |
| sarah  | lockig, fein, stark_geschaedigt+spliss+trocken, blondiert, Hitze sehr_haeufig, bestmoeglich | **normal** | HIGH | 18 | 10 | 7 | CON-09, CON-11 |

**Wichtig zur Eingabe-Kurzform**: Die zweite Spalte listet `hair_*`-Felder (hair_structure, hair_thickness, hair_condition, hair_treatments, heat_frequency, routine_preference). `scalp_status` ist **separat** in eigener Spalte — das sind zwei unabhängige Felder im Profil-Schema. **Spezifisch nicht verwechseln**: bianca's „trocken" in der Eingabe-Kurzform ist `hair_condition` (Haar), bianca's `scalp_status` ist `juckend_empfindlich` (Kopfhaut). Bei Doku-Updates beide Felder getrennt aus `test_suite.py` lesen, nicht eines aus dem anderen ableiten.

Sollwerte stand 2026-06-10-Full-Run nach Node-03-Removal. Vorherige Werte (julia count=5/CON-07,12; sarah count=8) reflektierten den Pre-A-F-Audit-Stand (vor monat_black- + smoothing_fohn_spray-Korrekturen). scalp_status-Spalte ergänzt 2026-06-13 nach test_suite.py-Read; siehe T-02-Anlass im Workflow-Block.

## Test-Suite

Aufrufe:
- `python3 test_suite.py --profile anna` — Einzelprofil (single-Modus, ~4 Min Polling-Limit)
- `python3 test_suite.py` — alle 7 Profile (bulk-Modus, ~13–14 Min: sequenzieller Trigger 9 Min + letzte Pipeline 4 Min)
- `python3 test_suite.py --save` — zusätzlich Ergebnis als `test_results_<ts>.json`
- `python3 test_suite.py --verbose` — voller JSON-Output statt formatierter Report
- `--wait N` — Wartezeit (Sek.) explizit setzen; Default single 360, bulk 900
- `--gap N` — Trigger-Gap (Sek.) im bulk-Modus; Default 90 (Google-Sheets-Rate-Limit-Schutz)

**v3 (2026-06-24, T-03-Formalisierung)** — siehe Folge-Punkte-Tabelle. Zwei Pfade:
- `run_single()`: Trigger + Polling auf eine success-Execution mit `first_name`-Verifikation (`POLL_INTERVAL_SINGLE=0.8s`)
- `run_bulk()`: sequenzieller Trigger (90s-Gap), dann Bulk-Polling (`POLL_INTERVAL_BULK=15s`) bis N success-Executions, dann Detail-Fetch + Profil-Zuordnung per `first_name`

Härtungsstand:
- `SINGLE_PROFILE_WAIT = 360`, `BULK_TOTAL_WAIT = 900`, `BULK_TRIGGER_GAP = 90`
- `TERMINAL_STATUSES = ("success",)` — Error-Executions nicht als gültig akzeptiert
- `first_name`-Verifikation verhindert Profil-Mix-Up bei Latenz und Bulk-Reihenfolge-Drift

Pipeline-Latenz ~3–5 Min pro Profil (Cold-Start + 6 Sheet-Loader: 04a, 05a, 06a, 06b, 06c, 06d, 08a). Bulk-Modus läuft Pipelines parallel, daher `BULK_TOTAL_WAIT=900` ≈ Trigger-Phase + letzte Pipeline, nicht Σ aller Pipelines.

## n8n REST API — Operationsregeln

PUT `/api/v1/workflows/{id}` Body-Whitelisting:
- Top-Level: nur `name`, `nodes`, `connections`, `settings`
- `settings` darf nur enthalten: `saveExecutionProgress`, `saveManualExecutions`, `saveDataErrorExecution`, `saveDataSuccessExecution`, `executionTimeout`, `errorWorkflow`, `timezone`, `executionOrder`
- Aktueller Workflow nutzt davon nur `executionOrder`
- Read-only Felder (`id`, `versionId`, `createdAt`, `updatedAt`, `active`, `tags`, `triggerCount`, `pinData`, `meta`, `shared`, `isArchived`, `staticData` etc.) müssen aus dem Body raus
- `active`-State bleibt nach PUT erhalten
- Vor jedem PUT: GET → Backup als `~/Projekte/myglowmatch/workflow_backup_<ts>_<kontext>.json`
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
- Spalte `produkt_url` in `produktdatenbank` — 37/37 leer, 0 Workflow-Konsumenten (Node 17 nutzt nur `mailto:`/WhatsApp/Impressum-Links). Produkt-Link-Integration wurde als Anfangsidee angetestet und verworfen (saubere Einbindung gelang nicht). **Nicht als Audit-Lücke behandeln.**
- `needs_lightweight_logic` in Node 05 wird **seit Migration #8** wieder gelesen — `wants_intense_care` (NEU 2026-06-18) leitet sich daraus + `hair_treatments`+`needs_repair_focus` ab. Zwischen Migration #5 und Migration #8 ungenutzt; seit Node 12 v4 ist es wieder Live-Konsument.
