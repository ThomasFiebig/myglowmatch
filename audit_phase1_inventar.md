# Phase-1-Inventar Routing-Regeln (Stand 20260628_211608)

Quelle: Live-Read der 4 Routing-Tabs aus dem Google-Sheet `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A`. Pro Tab CSV-Baseline unter `backups/phase1_inventar_20260628_211608/`.

Verdacht-Spalte bleibt in Phase 1 leer — wird in Phase 2 manuell gefüllt.

## map_derived_variables — Flag-Regeln (Phase 1: normalized → flags)

Pro Zeile: aus welchen `normalized.*`/`flags.*`-Inputs entsteht das Flag, wer konsumiert es. Die `regel_json`-Spalte ist die autoritative Trigger-Bedingung (vollständig, JSON-kompakt).

| variable | typ | regel_json (vollständig) | konsumenten | doku |
|---|---|---|---|---|
| heat_use | enum | {"cases":[{"when":{"in":["normalized.heat_frequency",["regelmaessig","sehr_haeufig"]]},"then":"yes"},{"when":{"eq":["normalized.heat_frequency","gelegentlich"]},"then":"maybe"}],"else":"no"} | map_slot_rules R6/R11/R12/R4b; map_conflict_rules R3 | Hitzeschutz-Trigger 3-stufig: regelmaessig\|sehr_haeufig=yes, gelegentlich=maybe, sonst no (Migration #18, 2026-06-26) |
| oil_need | enum | {"cases":[{"when":{"eq":["normalized.ends_condition","deutlich_trocken"]},"then":"yes"},{"when":{"eq":["normalized.ends_condition","leicht_trocken"]},"then":"maybe"}],"else":"no"} | map_slot_rules R10/R18 | REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand |
| needs_repair_focus | bool | {"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},{"eq":["normalized.hair_treatments","blondiert"]}]} | map_slot_rules R4/R5/R22/R23; map_pool_filter R2; flags.wants_intense_care | Bond-IQ-Trigger; starke Schaedigung oder Blondierung |
| needs_scalp_focus | bool | {"intersects":["normalized.scalp_status",["juckend_empfindlich","schuppig","trocken"]]} | map_slot_rules R21 | Scalp-Comfort-Trigger; problematische Kopfhaut |
| needs_lightweight_logic | bool | {"or":[{"eq":["normalized.hair_thickness","fein"]},{"includes":["normalized.hair_condition","kraftlos"]}]} | flags.wants_intense_care (POOL-02 gewicht-Filter ist bewusste Luecke) | Negativ-Input fuer wants_intense_care; feines oder kraftloses Haar will nichts Schweres |
| needs_curl_care | bool | {"and":[{"in":["normalized.hair_structure",["wellig","lockig","kraus"]]},{"neq":["normalized.curl_priority","glatt"]}]} | map_slot_rules R11/R12/R11b; flags.curl_refresh_needed; flags.styling_goal_definition; flags.wants_full_curl_line; flags.needs_curl_gelee_styling | Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15) |
| prefers_straight | bool | {"and":[{"in":["normalized.hair_structure",["wellig","lockig","kraus"]]},{"eq":["normalized.curl_priority","glatt"]}]} | flags.prefers_straight_with_frizz | User mit Locken/Wellen, will aber glatt tragen (Migration #15) |
| detangling_need | enum | {"cases":[{"when":{"or":[{"includes":["normalized.hair_condition","haarbruch"]},{"includes":["normalized.hair_condition","spliss"]},{"and":[{"eq":["normalized.hair_structure","kraus"]},{"eq":["normalized.ends_condition","deutlich_trocken"]}]}]},"then":"stark_verfilzt"},{"when":{"or":[{"and":[{"includes":["normalized.hair_condition","trocken"]},{"not":{"includes":["normalized.hair_condition","haarbruch"]}}]},{"and":[{"eq":["normalized.hair_structure","lockig"]},{"not":{"includes":["normalized.hair_condition","keine_probleme"]}}]}]},"then":"leicht_verfilzt"}],"else":"problemlos"} | map_slot_rules R9/R19 | REQ-07/18; 3-stufige Verfilzungs-Einstufung |
| needs_dry_shampoo | bool | {"and":[{"neq":["normalized.wash_frequency","taeglich"]},{"includes":["normalized.scalp_status","fettig"]}]} | map_slot_rules R15 | The-Champ-Trigger; the_champ ist PDF-belegter Oel-Absorber (4x 'Oel' in PDF). Nur sinnvoll bei FETTIGER Kopfhaut + NICHT-taeglicher Waesche. Trockene Kopfhaut braucht keinen Oel-Absorber. (Migration #17 verfeinert 2026-06-26) |
| styling_goal_volumen | bool | {"includes":["normalized.care_goals","volumen"]} | map_slot_rules R20 | Volumen-Ziel aus User-Auswahl |
| styling_goal_glanz | bool | {"includes":["normalized.care_goals","glanz"]} | map_slot_rules R17 | Glanz-Ziel aus User-Auswahl |
| styling_goal_halt | bool | {"and":[{"eq":["normalized.styling_effort","aufwendiges_styling"]},{"in":["normalized.hair_thickness",["fein","mittel"]]},{"in":["normalized.hair_structure",["glatt","wellig"]]}]} | map_slot_rules R16 | Moxie-Mousse-Trigger; aufwendiges Styling auf feinem/mittlerem glatten/welligem Haar |
| curl_refresh_needed | bool | {"and":[{"neq":["normalized.wash_frequency","taeglich"]},{"eq":["flags.needs_curl_care",true]}]} | map_slot_rules REQ-13 | Curl-Auffrischer-Trigger; alle Wasch-Frequenzen AUSSER taeglich + Locken (Migration #15) |
| styling_goal_definition | bool | {"and":[{"eq":["flags.needs_curl_care",true]},{"in":["normalized.curl_priority",["mehr_definition","beides"]]}]} | map_conflict_rules R5 | Curl-Definition-Trigger; matcht mehr_definition UND beides (Migration #15) |
| wants_full_curl_line | bool | {"and":[{"eq":["flags.needs_curl_care",true]},{"eq":["normalized.curl_priority","beides"]}]} | map_slot_rules REQ-11b; flags.needs_curl_gelee_styling | User mit Locken wuenscht komplette Curl-Linie (Definition + Volumen+Halt) (Migration #15) |
| needs_curl_gelee_styling | bool | {"or":[{"and":[{"eq":["flags.needs_curl_care",true]},{"neq":["flags.heat_use","no"]}]},{"eq":["flags.wants_full_curl_line",true]}]} | map_slot_rules REQ-12 | curl_gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie. Migration #16 — entkoppelt von heat_use, damit Sina (glaetteisen-frei) trotzdem curl_gelee bekommt. |
| prefers_straight_with_frizz | bool | {"and":[{"eq":["flags.prefers_straight",true]},{"includes":["normalized.hair_condition","frizz"]}]} | map_slot_rules REQ-04b | Locken-Traeger:in mit Glaett-Wunsch + Frizz: smoothing_fohn_spray priorisieren (Hitzeschutz + Frizz-Reduktion in einem). Migration #16. |
| wants_intense_care | bool | {"or":[{"eq":["flags.needs_repair_focus",true]},{"and":[{"eq":["flags.needs_lightweight_logic",false]},{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}]} | Node 12 v4 Stufe 11 (intensitaet-Tiebreaker) | Pflege-Intensitaets-Praeferenz fuer Node-12-Ranking; NEU 2026-06-18 |
| wants_curl_volume | bool | {"and":[{"eq":["flags.needs_curl_care",true]},{"eq":["normalized.curl_priority","mehr_volumen"]}]} | map_slot_rules REQ-16b | Locken-Traeger:in wuenscht mehr Volumen: triggert moxie_mousse-Slot. PDF-belegt FAQ Q2 (Locken/Wellen + Volumen). Migration #20 2026-06-27. |

## map_slot_rules — REQ-Regeln (Routing in Slots)

Nur aktive Regeln. Spalten zur Trigger-Bedingung und zur Folge (welches Produkt in welchen Slot). `requires_not`/`overrides` modellieren Regel-zu-Regel-Beziehungen, `filter` schränkt den Produkt-Pool ein.

| regel_id | prioritaet | trigger | slot_typ | filter | requires_not | overrides | reason |
|---|---|---|---|---|---|---|---|
| REQ-01 | required_always | (immer) | shampoo |  |  |  | Shampoo immer required |
| REQ-01b | required_always | (immer) | spuelung |  |  |  | Spülung immer required |
| REQ-02 | required_conditional | needs_repair_focus=TRUE | spuelung | bond_iq |  | REQ-01b | Bonding-Spülung bei Schaden/Blondierung (überschreibt Standard-Spülung) |
| REQ-03 | required_conditional | needs_repair_focus=TRUE AND pflegelevel_numeric=>=3 | maske | bond_iq\|reparatur |  |  | Reparaturmaske bei Reparatur + HIGH |
| REQ-04 | required_conditional | heat_use=yes\|maybe | styling_1 | ist_hitzeschutz=TRUE | REQ-11,REQ-11b,REQ-04b |  | Hitzeschutz required bei Hitze (Scoring entscheidet zwischen Spray/Föhncreme/Smoothing) |
| REQ-05 | required_conditional | primary_scalp_state=juckend_empfindlich | kopfhaut | scalp_comfort |  |  | Scalp Comfort Behandlung bei empfindlicher Kopfhaut (wöchentlich) |
| REQ-06 | required_conditional | hair_condition_contains=duenn | kopfhaut | ir_clinical_kopfhautserum |  |  | IR Clinical Serum bei dünner werdendem Haar |
| REQ-07 | required_conditional | detangling_need=stark_verfilzt | leave_in | entwirrungsspray |  |  | Entwirrungsspray bei stark verfilzt |
| REQ-08 | required_conditional | oil_need=yes | finish | rejuveniqe |  |  | Finish-Öl bei sehr trockenen Spitzen |
| REQ-11 | required_conditional | needs_curl_care=TRUE AND heat_use=no | styling_1 | curl_creme |  |  | Curl-Styling als primaeres Styling bei Locken/Wellen ohne Hitze |
| REQ-12 | required_conditional | needs_curl_care=TRUE AND needs_curl_gelee_styling=TRUE | styling_2 | curl_gelee |  |  | Curl-Gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie (Migration #16) |
| REQ-10 | optional | pflegelevel_numeric=>=2 | maske |  | REQ-03 |  | Pflegemaske optional bei MID+ |
| REQ-13 | required_conditional | curl_refresh_needed=TRUE AND wants_full_curl_line=TRUE | styling_3 | curl_auffrischer |  |  | Curl Auffrischer bei seltenen Waeschen + komplette Curl-Linie gewuenscht (Migration #15) |
| REQ-14 | optional | needs_dry_shampoo=TRUE | finish | the_champ |  |  | Trockenshampoo bei häufigem Waschen |
| REQ-16 | optional | styling_goal_halt=TRUE | styling_1 | moxie_mousse |  |  | Moxie Mousse bei Halt-Ziel |
| REQ-17 | optional | styling_goal_glanz=TRUE | finish | rejuveniqe_oel |  |  | REJUVENIQE bei Glanz-Ziel |
| REQ-17b | optional | oil_need=maybe AND pflegelevel_numeric=>=3 | finish | rejuveniqe_oel |  |  | REJUVENIQE bei HIGH + leicht trockenen Spitzen |
| REQ-18 | optional | detangling_need=leicht_verfilzt | leave_in | entwirrungsspray |  |  | Entwirrungsspray bei leicht verfilzt |
| REQ-19 | optional | styling_goal_volumen=TRUE AND hair_thickness=fein | styling_1 | moxie_mousse\|volumen_spray |  |  | Volumen-Styling bei Volumen-Ziel + feinem Haar |
| REQ-20 | optional | needs_scalp_focus=TRUE AND pflegelevel_numeric=>=2 | kopfhaut_taeglich | scalp_comfort_serum | REQ-05 |  | Scalp Comfort Serum täglich bei Kopfhaut-Fokus + MID/HIGH |
| REQ-21 | optional | needs_repair_focus=TRUE AND pflegelevel_numeric=>=2 | leave_in | bond_iq_leave_in |  |  | Bond IQ Leave-in bei Reparatur + MID/HIGH |
| REQ-22 | optional | needs_repair_focus=TRUE AND pflegelevel_numeric=>=3 | nacht_serum | bond_iq_night_day_serum |  |  | Bond IQ Night & Day Serum nachts bei Reparatur + HIGH |
| REQ-23 | optional | pflegelevel_numeric=>=2 | leave_in | restore_leave_in | REQ-07,REQ-18,REQ-21 |  | RESTORE Leave-In generisch bei MID/HIGH (nur ohne Entwirrungsspray oder Bond IQ Leave-In) |
| REQ-24 | optional | primary_scalp_state=fettig | kopfhaut | kopfhaut_peeling |  |  | Kopfhaut-Peeling bei fettiger Kopfhaut |
| REQ-30 | required_conditional | primary_scalp_state=fettig AND routine_preference=minimal | shampoo | monat_black |  | REQ-01,REQ-01b | MONAT Black 2-in-1 bei fettiger Kopfhaut + minimale Routine (ersetzt Shampoo + Spülung) |
| REQ-MIN-NO-OPT | suppress_optional | routine_preference=minimal |  |  |  |  | Bei routine_preference=minimal werden alle optional-Slots entfernt (Migration #11, 2026-06-24) |
| REQ-11b | required_conditional | wants_full_curl_line=TRUE | styling_1 | curl_creme |  |  | Curl-Creme als primaeres Styling bei Wunsch nach kompletter Curl-Linie (Migration #15) |
| REQ-04b | required_conditional | prefers_straight_with_frizz=TRUE AND heat_use=yes\|maybe | styling_1 | smoothing_fohn_spray |  |  | Smoothing Foehn-Spray bei Locken-Traeger:in mit Glaett-Wunsch + Frizz + Hitzestyling: Hitzeschutz + Frizz-Reduktion in einem (Migration #16) |
| REQ-16b | required_conditional | wants_curl_volume=TRUE | styling_3 | moxie_mousse |  |  | Moxie Volumen-Mousse bei Locken-Traeger:in mit Volumen-Wunsch (PDF FAQ Q2 + Header). Migration #20. |

_Inaktive Regeln ausgeblendet: 0 von 29._

## map_conflict_rules — CON-Regeln (Produkt-Exclude / Suppress)

Nur aktive Regeln. CON-Regeln blocken oder verschieben Produkte, die durch REQ schon im Topf sind.

| konflikt_id | trigger | action | match_typ | match_wert | beschreibung |
|---|---|---|---|---|---|
| CON-07 | heat_use=no | suppress_optional | produkt_key | hitzeschutzspray | Hitzeschutz ohne Hitze (sinnlos wenn nie gefoehnt/geglaettet wird) |
| CON-11 | styling_goal_definition=TRUE | exclude_product | produkt_key | smoothing_shampoo,smoothing_deep_conditioner,smoothing_fohn_spray | Smoothing-Produkte bei Definitions-Ziel (Glaetten zerstoert Locken/Wellen-Definition). Tiefenbehandlung ausgenommen: Datenblatt explizit auch fuer Locken. Linie deckt Haarstaerken komplementaer ab: smoothing_deep_conditioner (fein,mittel) und smoothing_tiefenbehandlung (mittel,dick) - keine Konkurrenz, sondern Sortiments-Trennung. |
| CON-13 | needs_curl_care=TRUE AND hair_condition=frizz | exclude_product | produkt_key | smoothing_fohn_spray | Smoothing Föhn-Spray bei Locken+Frizz blockieren — curl_creme behandelt Frizz bei Locken besser (MONAT Curl Perfection) |

_Inaktive Regeln ausgeblendet: 3 von 6._

## map_pflegelevel_overrides — PFL-Floor/Cap-Regeln

Hebt das Pflegelevel auf einen Mindestwert (`raise_to`) oder deckelt es (`cap_at`). Wirkt indirekt aufs Routing: das endgültige Pflegelevel beeinflusst `max_products` und Filter-Verhalten.

| regel_id | prio | bedingung1 | bedingung2 | aktion | ziel_level | beschreibung |
|---|---|---|---|---|---|---|
| PFL-OV-01 | 1 | hair_treatments equals blondiert | heat_frequency in_list regelmaessig\|sehr_haeufig | raise_to | HIGH | Blondiert + häufige Hitze → mindestens HIGH (maximaler Schutzbedarf) |
| PFL-OV-02 | 2 | hair_treatments equals blondiert | — | raise_to | MID | Blondiert allein → mindestens MID (Farbpflege) |
| PFL-OV-03 | 3 | hair_condition array_contains stark_geschaedigt | — | raise_to | HIGH | Stark geschädigt → mindestens HIGH (Reparatur priorisiert) |
| PFL-OV-04 | 10 | routine_preference equals minimal | — | cap_at | MID | Minimal-Präferenz cappt auf MID (außer Floor-Regel hat bereits höher gesetzt) |

_Inaktive Regeln ausgeblendet: 0 von 4._
