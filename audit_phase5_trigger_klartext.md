# Trigger-Klartext pro REQ-Regel

## REQ-02 → Produkt(e): bond_iq
- slot_typ: `spuelung` · prioritaet: `required_conditional`
- Trigger1: `needs_repair_focus = TRUE`
  - Doku: Bond-IQ-Trigger; starke Schaedigung oder Blondierung
  - regel_json: `{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}`
- Reason: Bonding-Spülung bei Schaden/Blondierung (überschreibt Standard-Spülung)

## REQ-03 → Produkt(e): bond_iq|reparatur
- slot_typ: `maske` · prioritaet: `required_conditional`
- Trigger1: `needs_repair_focus = TRUE`
  - Doku: Bond-IQ-Trigger; starke Schaedigung oder Blondierung
  - regel_json: `{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}`
- Trigger2 (AND): `pflegelevel_numeric = >=3`
- Reason: Reparaturmaske bei Reparatur + HIGH

## REQ-05 → Produkt(e): scalp_comfort
- slot_typ: `kopfhaut` · prioritaet: `required_conditional`
- Trigger1: `primary_scalp_state = juckend_empfindlich`
- Reason: Scalp Comfort Behandlung bei empfindlicher Kopfhaut (wöchentlich)

## REQ-06 → Produkt(e): ir_clinical_kopfhautserum
- slot_typ: `kopfhaut` · prioritaet: `required_conditional`
- Trigger1: `hair_condition_contains = duenn`
- Reason: IR Clinical Serum bei dünner werdendem Haar

## REQ-07 → Produkt(e): entwirrungsspray
- slot_typ: `leave_in` · prioritaet: `required_conditional`
- Trigger1: `detangling_need = stark_verfilzt`
  - Doku: REQ-07/18; PDF-belegt: Header-Untertitel "Haarbruch/Spliss" -> stark_verfilzt, IDEAL-Bullet "Frizz kontrollieren" -> leicht_verfilzt (Migration #23, 2026-07-01)
  - regel_json: `{"cases":[{"when":{"or":[{"includes":["normalized.hair_condition","haarbruch"]},{"includes":["normalized.hair_condition","spliss"]}]},"then":"stark_verfilzt"},{"when":{"includes":["normalized.hair_condition","frizz"]},"then":"leicht_verfilzt"}],"else`
- Reason: Entwirrungsspray bei stark verfilzt

## REQ-08 → Produkt(e): rejuveniqe
- slot_typ: `finish` · prioritaet: `required_conditional`
- Trigger1: `oil_need = yes`
  - Doku: REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand
  - regel_json: `{"cases":[{"when":{"eq":["normalized.ends_condition","deutlich_trocken"]},"then":"yes"},{"when":{"eq":["normalized.ends_condition","leicht_trocken"]},"then":"maybe"}],"else":"no"}`
- Reason: Finish-Öl bei sehr trockenen Spitzen

## REQ-11 → Produkt(e): curl_creme
- slot_typ: `styling_1` · prioritaet: `required_conditional`
- Trigger1: `needs_curl_care = TRUE`
  - Doku: Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15)
  - regel_json: `{"and":[{"in":["normalized.hair_structure",["wellig","lockig","kraus"]]},{"neq":["normalized.curl_priority","glatt"]}]}`
- Trigger2 (AND): `heat_use = no`
  - Doku: Hitzeschutz-Trigger 3-stufig: regelmaessig|sehr_haeufig=yes, gelegentlich=maybe, sonst no (Migration #18, 2026-06-26)
  - regel_json: `{"cases":[{"when":{"in":["normalized.heat_frequency",["regelmaessig","sehr_haeufig"]]},"then":"yes"},{"when":{"eq":["normalized.heat_frequency","gelegentlich"]},"then":"maybe"}],"else":"no"}`
- Reason: Curl-Styling als primaeres Styling bei Locken/Wellen ohne Hitze

## REQ-12 → Produkt(e): curl_gelee
- slot_typ: `styling_2` · prioritaet: `required_conditional`
- Trigger1: `needs_curl_care = TRUE`
  - Doku: Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15)
  - regel_json: `{"and":[{"in":["normalized.hair_structure",["wellig","lockig","kraus"]]},{"neq":["normalized.curl_priority","glatt"]}]}`
- Trigger2 (AND): `needs_curl_gelee_styling = TRUE`
  - Doku: curl_gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie. Migration #16 — entkoppelt von heat_use, damit Sina (glaetteisen-frei) trotzdem curl_gelee bekommt.
  - regel_json: `{"or":[{"and":[{"eq":["flags.needs_curl_care",true]},{"neq":["flags.heat_use","no"]}]},{"eq":["flags.wants_full_curl_line",true]}]}`
- Reason: Curl-Gelee styling_2: bei Locken+Hitze ODER komplette Curl-Linie (Migration #16)

## REQ-13 → Produkt(e): curl_auffrischer
- slot_typ: `styling_3` · prioritaet: `required_conditional`
- Trigger1: `curl_refresh_needed = TRUE`
  - Doku: Curl-Auffrischer-Trigger; alle Wasch-Frequenzen AUSSER taeglich + Locken (Migration #15)
  - regel_json: `{"and":[{"neq":["normalized.wash_frequency","taeglich"]},{"eq":["flags.needs_curl_care",true]}]}`
- Trigger2 (AND): `wants_full_curl_line = TRUE`
  - Doku: User mit Locken wuenscht komplette Curl-Linie (Definition + Volumen+Halt) (Migration #15)
  - regel_json: `{"and":[{"eq":["flags.needs_curl_care",true]},{"eq":["normalized.curl_priority","beides"]}]}`
- Reason: Curl Auffrischer bei seltenen Waeschen + komplette Curl-Linie gewuenscht (Migration #15)

## REQ-14 → Produkt(e): the_champ
- slot_typ: `finish` · prioritaet: `optional`
- Trigger1: `needs_dry_shampoo = TRUE`
  - Doku: The-Champ-Trigger; the_champ ist PDF-belegter Oel-Absorber (4x 'Oel' in PDF). Nur sinnvoll bei FETTIGER Kopfhaut + NICHT-taeglicher Waesche. Trockene Kopfhaut braucht keinen Oel-Absorber. (Migration #17 verfeinert 2026-06-26)
  - regel_json: `{"and":[{"neq":["normalized.wash_frequency","taeglich"]},{"includes":["normalized.scalp_status","fettig"]}]}`
- Reason: Trockenshampoo (the_champ) als Öl-Absorber bei fettiger Kopfhaut + nicht-täglicher Wäsche (Migration #17, 2026-06-26)

## REQ-16 → Produkt(e): moxie_mousse
- slot_typ: `styling_1` · prioritaet: `optional`
- Trigger1: `styling_goal_halt = TRUE`
  - Doku: Moxie-Mousse-Trigger; aufwendiges Styling auf feinem/mittlerem glatten/welligem Haar
  - regel_json: `{"and":[{"eq":["normalized.styling_effort","aufwendiges_styling"]},{"in":["normalized.hair_thickness",["fein","mittel"]]},{"in":["normalized.hair_structure",["glatt","wellig"]]}]}`
- Reason: Moxie Mousse bei Halt-Ziel

## REQ-17 → Produkt(e): rejuveniqe_oel
- slot_typ: `finish` · prioritaet: `optional`
- Trigger1: `styling_goal_glanz = TRUE`
  - Doku: Glanz-Ziel aus User-Auswahl
  - regel_json: `{"includes":["normalized.care_goals","glanz"]}`
- Reason: REJUVENIQE bei Glanz-Ziel

## REQ-17b → Produkt(e): rejuveniqe_oel
- slot_typ: `finish` · prioritaet: `optional`
- Trigger1: `oil_need = maybe`
  - Doku: REJUVABEADS- und REJUVENIQE-Oel-Trigger nach Spitzen-Zustand
  - regel_json: `{"cases":[{"when":{"eq":["normalized.ends_condition","deutlich_trocken"]},"then":"yes"},{"when":{"eq":["normalized.ends_condition","leicht_trocken"]},"then":"maybe"}],"else":"no"}`
- Trigger2 (AND): `pflegelevel_numeric = >=3`
- Reason: REJUVENIQE bei HIGH + leicht trockenen Spitzen

## REQ-18 → Produkt(e): entwirrungsspray
- slot_typ: `leave_in` · prioritaet: `optional`
- Trigger1: `detangling_need = leicht_verfilzt`
  - Doku: REQ-07/18; PDF-belegt: Header-Untertitel "Haarbruch/Spliss" -> stark_verfilzt, IDEAL-Bullet "Frizz kontrollieren" -> leicht_verfilzt (Migration #23, 2026-07-01)
  - regel_json: `{"cases":[{"when":{"or":[{"includes":["normalized.hair_condition","haarbruch"]},{"includes":["normalized.hair_condition","spliss"]}]},"then":"stark_verfilzt"},{"when":{"includes":["normalized.hair_condition","frizz"]},"then":"leicht_verfilzt"}],"else`
- Reason: Entwirrungsspray bei leicht verfilzt

## REQ-19 → Produkt(e): moxie_mousse|volumen_spray
- slot_typ: `styling_1` · prioritaet: `optional`
- Trigger1: `styling_goal_volumen = TRUE`
  - Doku: Volumen-Ziel aus User-Auswahl
  - regel_json: `{"includes":["normalized.care_goals","volumen"]}`
- Trigger2 (AND): `hair_thickness = fein`
- Reason: Volumen-Styling bei Volumen-Ziel + feinem Haar

## REQ-20 → Produkt(e): scalp_comfort_serum
- slot_typ: `kopfhaut_taeglich` · prioritaet: `optional`
- Trigger1: `needs_scalp_focus = TRUE`
  - Doku: Scalp-Comfort-Trigger; problematische Kopfhaut
  - regel_json: `{"intersects":["normalized.scalp_status",["juckend_empfindlich","schuppig","trocken"]]}`
- Trigger2 (AND): `pflegelevel_numeric = >=2`
- Reason: Scalp Comfort Serum täglich bei Kopfhaut-Fokus + MID/HIGH

## REQ-21 → Produkt(e): bond_iq_leave_in
- slot_typ: `leave_in` · prioritaet: `optional`
- Trigger1: `needs_repair_focus = TRUE`
  - Doku: Bond-IQ-Trigger; starke Schaedigung oder Blondierung
  - regel_json: `{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}`
- Trigger2 (AND): `pflegelevel_numeric = >=2`
- Reason: Bond IQ Leave-in bei Reparatur + MID/HIGH

## REQ-22 → Produkt(e): bond_iq_night_day_serum
- slot_typ: `nacht_serum` · prioritaet: `optional`
- Trigger1: `needs_repair_focus = TRUE`
  - Doku: Bond-IQ-Trigger; starke Schaedigung oder Blondierung
  - regel_json: `{"or":[{"includes":["normalized.hair_condition","stark_geschaedigt"]},{"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}]}`
- Trigger2 (AND): `pflegelevel_numeric = >=3`
- Reason: Bond IQ Night & Day Serum nachts bei Reparatur + HIGH

## REQ-23 → Produkt(e): restore_leave_in
- slot_typ: `leave_in` · prioritaet: `optional`
- Trigger1: `pflegelevel_numeric = >=2`
- Reason: RESTORE Leave-In generisch bei MID/HIGH (nur ohne Entwirrungsspray oder Bond IQ Leave-In)

## REQ-24 → Produkt(e): kopfhaut_peeling
- slot_typ: `kopfhaut` · prioritaet: `optional`
- Trigger1: `primary_scalp_state = fettig`
- Reason: Kopfhaut-Peeling bei fettiger Kopfhaut

## REQ-30 → Produkt(e): monat_black
- slot_typ: `shampoo` · prioritaet: `required_conditional`
- Trigger1: `primary_scalp_state = fettig`
- Trigger2 (AND): `routine_preference = minimal`
- Reason: MONAT Black 2-in-1 bei fettiger Kopfhaut + minimale Routine (ersetzt Shampoo + Spülung)

## REQ-11b → Produkt(e): curl_creme
- slot_typ: `styling_1` · prioritaet: `required_conditional`
- Trigger1: `wants_full_curl_line = TRUE`
  - Doku: User mit Locken wuenscht komplette Curl-Linie (Definition + Volumen+Halt) (Migration #15)
  - regel_json: `{"and":[{"eq":["flags.needs_curl_care",true]},{"eq":["normalized.curl_priority","beides"]}]}`
- Reason: Curl-Creme als primaeres Styling bei Wunsch nach kompletter Curl-Linie (Migration #15)

## REQ-04b → Produkt(e): smoothing_fohn_spray
- slot_typ: `styling_1` · prioritaet: `required_conditional`
- Trigger1: `prefers_straight_with_frizz = TRUE`
  - Doku: Locken-Traeger:in mit Glaett-Wunsch + Frizz: smoothing_fohn_spray priorisieren (Hitzeschutz + Frizz-Reduktion in einem). Migration #16.
  - regel_json: `{"and":[{"eq":["flags.prefers_straight",true]},{"includes":["normalized.hair_condition","frizz"]}]}`
- Trigger2 (AND): `heat_use = yes|maybe`
  - Doku: Hitzeschutz-Trigger 3-stufig: regelmaessig|sehr_haeufig=yes, gelegentlich=maybe, sonst no (Migration #18, 2026-06-26)
  - regel_json: `{"cases":[{"when":{"in":["normalized.heat_frequency",["regelmaessig","sehr_haeufig"]]},"then":"yes"},{"when":{"eq":["normalized.heat_frequency","gelegentlich"]},"then":"maybe"}],"else":"no"}`
- Reason: Smoothing Foehn-Spray bei Locken-Traeger:in mit Glaett-Wunsch + Frizz + Hitzestyling: Hitzeschutz + Frizz-Reduktion in einem (Migration #16)

## REQ-16b → Produkt(e): moxie_mousse
- slot_typ: `styling_3` · prioritaet: `required_conditional`
- Trigger1: `wants_curl_volume = TRUE`
  - Doku: Locken-Traeger:in wuenscht mehr Volumen: triggert moxie_mousse-Slot. PDF-belegt FAQ Q2 (Locken/Wellen + Volumen). Migration #20 2026-06-27.
  - regel_json: `{"and":[{"eq":["flags.needs_curl_care",true]},{"eq":["normalized.curl_priority","mehr_volumen"]}]}`
- Reason: Moxie Volumen-Mousse bei Locken-Traeger:in mit Volumen-Wunsch (PDF FAQ Q2 + Header). Migration #20.

## REQ-11c → Produkt(e): curl_creme
- slot_typ: `styling_1` · prioritaet: `required_conditional`
- Trigger1: `needs_curl_care = TRUE`
  - Doku: Curl-Produkte-Trigger; nicht-glatte Haarstruktur AUSSER User waehlt 'glatt' (Migration #15)
  - regel_json: `{"and":[{"in":["normalized.hair_structure",["wellig","lockig","kraus"]]},{"neq":["normalized.curl_priority","glatt"]}]}`
- Trigger2 (AND): `heat_use = maybe`
  - Doku: Hitzeschutz-Trigger 3-stufig: regelmaessig|sehr_haeufig=yes, gelegentlich=maybe, sonst no (Migration #18, 2026-06-26)
  - regel_json: `{"cases":[{"when":{"in":["normalized.heat_frequency",["regelmaessig","sehr_haeufig"]]},"then":"yes"},{"when":{"eq":["normalized.heat_frequency","gelegentlich"]},"then":"maybe"}],"else":"no"}`
- Reason: Curl-Creme als primaeres Styling bei Locken/Wellen + gelegentlicher Hitze (Migration #21 V5, PDF-belegt: curl_creme + Diffusor okay)

## REQ-19b → Produkt(e): moxie_mousse|volumen_spray
- slot_typ: `styling_1` · prioritaet: `optional`
- Trigger1: `styling_goal_volumen = TRUE`
  - Doku: Volumen-Ziel aus User-Auswahl
  - regel_json: `{"includes":["normalized.care_goals","volumen"]}`
- Trigger2 (AND): `hair_thickness = mittel`
- Reason: Volumen-Styling bei Volumen-Ziel + mittlerem Haar (Migration #21 V6, PDF-belegt: moxie_mousse FAQ + volumen_spray Header)

