# Phase-4-Inventar — Routing-Aussage pro Produkt

Stand 2026-06-28 23:57.
Quelle: Live-Read von produktdatenbank + map_slot_rules + map_conflict_rules + map_pool_filter.

Pro Produkt zusammengefasst, was das Routing-System über das Produkt aussagt — als Briefing für die PDF-Verifikation in Phase 4. Aussagen sind hierarchisch:

1. **Direkt-REQ**: REQ-Regeln, die das Produkt namentlich im `filter` referenzieren — triggert das Produkt aktiv.
2. **Linien-REQ**: REQ-Regeln, die die Produktlinie als filter haben — Produkt kann gewinnen, wenn es die Linie repräsentiert.
3. **Bool-Attribut-REQ**: REQ-Regeln mit Bool-Filter (`ist_hitzeschutz=TRUE` etc.) — Produkt qualifiziert sich, wenn das Bool-Flag in Stammdaten gesetzt ist.
4. **CON-Regeln**: schließen das Produkt aus.
5. **Stammdaten-Filter**: kopfhaut/haarstaerke/haarstruktur/haarzustand + ausschluss_bei + pflegelevel + slot_typ.

**Bereits in Phase 3 geprüft** (nicht hier): bond_iq_leave_in, bond_iq_night_day_serum, bond_iq_shampoo, bond_iq_spuelung, curl_creme, entwirrungsspray, moxie_mousse, volumen_spray.

---

## curl_auffrischer — MONAT Curl Perfection™ Auffrischungsspray

**Linie**: `curl_perfection` · **Slot**: `styling_3` · **Pflegelevel**: `LOW,MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `locken,auffrischung`
- nebenfunktionen: `feuchtigkeit,glanz,frizz_reduktion,definition,elastizitaet,staerkend`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `wellig,lockig,kraus` · haarstaerke: `alle` · haarzustand: `trocken,frizz`
- bool-Flags: `locken_geeignet`
- ausschluss_bei: `glatt`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-13` (required_conditional): WENN `curl_refresh_needed=TRUE` AND `wants_full_curl_line=TRUE` → slot `styling_3` (filter: `curl_auffrischer`)

---

## curl_gelee — MONAT Curl Perfection™ Gelée für Feuchtigkeit & Halt

**Linie**: `curl_perfection` · **Slot**: `styling_2` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `locken,definition,halt`
- nebenfunktionen: `feuchtigkeit,frizz_reduktion,glanz,elastizitaet,staerkend,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `wellig,lockig,kraus` · haarstaerke: `alle` · haarzustand: `frizz,trocken`
- bool-Flags: `locken_geeignet`
- ausschluss_bei: `glatt`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-12` (required_conditional): WENN `needs_curl_care=TRUE` AND `needs_curl_gelee_styling=TRUE` → slot `styling_2` (filter: `curl_gelee`)

---

## erweiterte_feuchtigkeit_spuelung — Erweiterte Feuchtigkeitsspülung

**Linie**: `erw_feuchtigkeit` · **Slot**: `spuelung` · **Pflegelevel**: `LOW,MID` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `glanz,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `trocken,glanzlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## essig_shampoo — Reinigendes Essig-Shampoo

**Linie**: `reinigende` · **Slot**: `shampoo` · **Pflegelevel**: `LOW,MID` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `reinigung,entgiftung`
- nebenfunktionen: `glanz,kopfhautpflege,frische`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `fettig` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `glanzlos`
- bool-Flags: `locken_geeignet`
- ausschluss_bei: `normal,trocken,juckend_empfindlich`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## essig_spuelung — Reinigende Essigspülung

**Linie**: `reinigende` · **Slot**: `spuelung` · **Pflegelevel**: `LOW,MID` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `reinigung,wash_alternative`
- nebenfunktionen: `glanz,feuchtigkeit,entgiftung,farbschutz,kopfhautpflege`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `glanzlos,trocken`
- bool-Flags: `locken_geeignet`
- ausschluss_bei: `normal,trocken,juckend_empfindlich`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## feuchtigkeits_shampoo — Erweitertes Feuchtigkeitsshampoo

**Linie**: `erw_feuchtigkeit` · **Slot**: `shampoo` · **Pflegelevel**: `LOW,MID` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `glanz,kaemmbarkeit,reinigung`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `trocken,glanzlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## fohncreme — MONAT STUDIO ONE™ Föhncreme

**Linie**: `studio_one` · **Slot**: `styling_1` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `frizz_reduktion,hitzeschutz`
- nebenfunktionen: `glanz`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `frizz`
- bool-Flags: `ist_hitzeschutz, locken_geeignet`
- ausschluss_bei: `wellig,lockig,kraus`

**Bool-Attribut-REQ-Routing** (Produkt erfüllt Bool-Bedingung):
- `REQ-04` (required_conditional): WENN `heat_use=yes|maybe` → slot `styling_1` (filter: `ist_hitzeschutz=TRUE`)

---

## hitzeschutzspray — MONAT STUDIO ONE™ Hitzeschutzspray

**Linie**: `studio_one` · **Slot**: `styling_1` · **Pflegelevel**: `LOW,MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `hitzeschutz`
- nebenfunktionen: `glanz,staerkend,elastizitaet`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `haarbruch`
- bool-Flags: `ist_hitzeschutz, locken_geeignet`

**Bool-Attribut-REQ-Routing** (Produkt erfüllt Bool-Bedingung):
- `REQ-04` (required_conditional): WENN `heat_use=yes|maybe` → slot `styling_1` (filter: `ist_hitzeschutz=TRUE`)

**CON-Regeln** (Produkt wird ausgeschlossen):
- `CON-07`: WENN `heat_use=no` → suppress_optional (match: produkt_key=hitzeschutzspray)

---

## ir_clinical_kopfhautserum — IR Clinical™ Kopfhautserum gegen dünner werdendes Haar

**Linie**: `ir_clinical` · **Slot**: `kopfhaut_taeglich` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `verdichtend,haarwuchs,kopfhautpflege`
- nebenfunktionen: `kopfhautpflege`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `trocken` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `duenn,kraftlos,haarbruch`
- bool-Flags: `ist_scalp_focus, locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-06` (required_conditional): WENN `hair_condition_contains=duenn` → slot `kopfhaut` (filter: `ir_clinical_kopfhautserum`)

---

## ir_clinical_shampoo — IR Clinical™ Verdickendes Shampoo

**Linie**: `ir_clinical` · **Slot**: `shampoo` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `verdichtend`
- nebenfunktionen: `reinigung,farbschutz,haarwuchs,staerkend,frische`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `duenn,kraftlos,haarbruch`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## ir_clinical_spuelung — IR Clinical™ Verdickende Spülung

**Linie**: `ir_clinical` · **Slot**: `spuelung` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `verdichtend`
- nebenfunktionen: `feuchtigkeit,farbschutz,haarwuchs,staerkend,kaemmbarkeit,frische`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `duenn,kraftlos,haarbruch`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## kopfhaut_peeling — Reinigungspeeling für die Kopfhaut

**Linie**: `reinigende` · **Slot**: `kopfhaut` · **Pflegelevel**: `LOW,MID` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `kopfhautpflege,reinigung`
- nebenfunktionen: `entgiftung,frische,feuchtigkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `fettig` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `glanzlos`
- bool-Flags: `ist_scalp_focus, locken_geeignet`
- ausschluss_bei: `juckend_empfindlich`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-24` (optional): WENN `primary_scalp_state=fettig` → slot `kopfhaut` (filter: `kopfhaut_peeling`)

---

## monat_black — MONAT BLACK™ Shampoo + Spülung

**Linie**: `monat_black` · **Slot**: `shampoo` · **Pflegelevel**: `LOW,MID` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `reinigung,verdichtend`
- nebenfunktionen: `staerkend`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `fettig` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `kraftlos,duenn`
- bool-Flags: `locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-30` (required_conditional): WENN `primary_scalp_state=fettig` AND `routine_preference=minimal` → slot `shampoo` (filter: `monat_black`)

---

## rejuvabeads — REJUVABEADS® Spliss-Versiegler

**Linie**: `basis` · **Slot**: `leave_in` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `reparatur,versiegelung`
- nebenfunktionen: `glanz,kaemmbarkeit,staerkend,frizz_reduktion`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `spliss,haarbruch,frizz`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## rejuveniqe_oel — REJUVENIQE® Pflegeöl

**Linie**: `basis` · **Slot**: `finish` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `glanz,feuchtigkeit`
- nebenfunktionen: `frizz_reduktion,kraeftigend,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `trocken,glanzlos,frizz`
- bool-Flags: `locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-17` (optional): WENN `styling_goal_glanz=TRUE` → slot `finish` (filter: `rejuveniqe_oel`)
- `REQ-17b` (optional): WENN `oil_need=maybe` AND `pflegelevel_numeric=>=3` → slot `finish` (filter: `rejuveniqe_oel`)

---

## renew_shampoo — Renew™ Hydrating Shampoo

**Linie**: `renew` · **Slot**: `shampoo` · **Pflegelevel**: `LOW,MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `glanz,reinigung,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `mittel,dick` · haarzustand: `trocken,glanzlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## renew_spuelung — Renew™ Hydrating Spülung

**Linie**: `renew` · **Slot**: `spuelung` · **Pflegelevel**: `LOW,MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `mittel,dick` · haarzustand: `trocken`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## replenish_maske — Replenish™ Feuchtigkeitsmaske

**Linie**: `renew` · **Slot**: `maske` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `glanz,kraeftigend,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `mittel,dick` · haarzustand: `trocken,glanzlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## restore_leave_in — Restore™ Leave-In Conditioner

**Linie**: `basis` · **Slot**: `leave_in` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `staerkend,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `mittel,dick` · haarzustand: `trocken`
- bool-Flags: `locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-23` (optional): WENN `pflegelevel_numeric=>=2` → slot `leave_in` (filter: `restore_leave_in`)

---

## revitalize_spuelung — Volumenverstärkende Revitalize™ Spülung

**Linie**: `volumen` · **Slot**: `spuelung` · **Pflegelevel**: `LOW,MID` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `volumen`
- nebenfunktionen: `feuchtigkeit,staerkend,kaemmbarkeit,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `kraftlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## revive_shampoo — Volumenverstärkendes Revive™ Shampoo

**Linie**: `volumen` · **Slot**: `shampoo` · **Pflegelevel**: `LOW,MID` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `volumen`
- nebenfunktionen: `reinigung,staerkend,feuchtigkeit,kaemmbarkeit,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `kraftlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## scalp_comfort_behandlung — MONAT Scalp Comfort™ Ausgleichende Kopfhautbehandlung

**Linie**: `scalp_comfort` · **Slot**: `kopfhaut` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `kopfhautpflege,ausgleichend`
- nebenfunktionen: `feuchtigkeit,reinigung,entgiftung,frische`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `juckend_empfindlich,schuppig,trocken` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `-`
- bool-Flags: `ist_scalp_focus, locken_geeignet`

**Linien-REQ-Routing** (filter referenziert produktlinie `scalp_comfort`):
- `REQ-05` (required_conditional): WENN `primary_scalp_state=juckend_empfindlich` → slot `kopfhaut` (filter: `scalp_comfort`)

---

## scalp_comfort_serum — MONAT Scalp Comfort™ Ausgleichendes Serum

**Linie**: `scalp_comfort` · **Slot**: `kopfhaut_taeglich` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `kopfhautpflege,ausgleichend`
- nebenfunktionen: `feuchtigkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `juckend_empfindlich,schuppig,trocken` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `-`
- bool-Flags: `ist_scalp_focus, locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-20` (optional): WENN `needs_scalp_focus=TRUE` AND `pflegelevel_numeric=>=2` → slot `kopfhaut_taeglich` (filter: `scalp_comfort_serum`)

**Linien-REQ-Routing** (filter referenziert produktlinie `scalp_comfort`):
- `REQ-05` (required_conditional): WENN `primary_scalp_state=juckend_empfindlich` → slot `kopfhaut` (filter: `scalp_comfort`)

---

## smoothing_deep_conditioner — Smoothing Anti-Frizz™ Deep Conditioner

**Linie**: `smoothing` · **Slot**: `spuelung` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `frizz_reduktion`
- nebenfunktionen: `feuchtigkeit,kaemmbarkeit,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `fein,mittel` · haarzustand: `frizz,trocken,haarbruch`
- bool-Flags: `locken_geeignet`

**CON-Regeln** (Produkt wird ausgeschlossen):
- `CON-11`: WENN `styling_goal_definition=TRUE` → exclude_product (match: produkt_key=smoothing_shampoo,smoothing_deep_conditioner,smoothing_fohn_spray)

---

## smoothing_fohn_spray — Smoothing Anti-Frizz™ Föhn-Spray

**Linie**: `smoothing` · **Slot**: `styling_1` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `leicht`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `frizz_reduktion,hitzeschutz`
- nebenfunktionen: `glanz,staerkend`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `frizz`
- bool-Flags: `ist_hitzeschutz, locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-04b` (required_conditional): WENN `prefers_straight_with_frizz=TRUE` AND `heat_use=yes|maybe` → slot `styling_1` (filter: `smoothing_fohn_spray`)

**Bool-Attribut-REQ-Routing** (Produkt erfüllt Bool-Bedingung):
- `REQ-04` (required_conditional): WENN `heat_use=yes|maybe` → slot `styling_1` (filter: `ist_hitzeschutz=TRUE`)

**CON-Regeln** (Produkt wird ausgeschlossen):
- `CON-11`: WENN `styling_goal_definition=TRUE` → exclude_product (match: produkt_key=smoothing_shampoo,smoothing_deep_conditioner,smoothing_fohn_spray)
- `CON-13`: WENN `needs_curl_care=TRUE` AND `hair_condition=frizz` → exclude_product (match: produkt_key=smoothing_fohn_spray)

---

## smoothing_shampoo — Smoothing Anti-Frizz™ Shampoo

**Linie**: `smoothing` · **Slot**: `shampoo` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `frizz_reduktion`
- nebenfunktionen: `feuchtigkeit,kaemmbarkeit,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `frizz,haarbruch`
- bool-Flags: `locken_geeignet`

**CON-Regeln** (Produkt wird ausgeschlossen):
- `CON-11`: WENN `styling_goal_definition=TRUE` → exclude_product (match: produkt_key=smoothing_shampoo,smoothing_deep_conditioner,smoothing_fohn_spray)

---

## smoothing_tiefenbehandlung — Smoothing Anti-Frizz™ Intensive Tiefenbehandlung

**Linie**: `smoothing` · **Slot**: `maske` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `frizz_reduktion`
- nebenfunktionen: `kaemmbarkeit,reparatur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `mittel,dick` · haarzustand: `frizz,haarbruch`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## super_feuchtigkeitsmaske — Super-Feuchtigkeitsmaske

**Linie**: `erw_feuchtigkeit` · **Slot**: `maske` · **Pflegelevel**: `MID,HIGH` · **Intensität**: `intensiv`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `feuchtigkeit`
- nebenfunktionen: `glanz,elastizitaet,kaemmbarkeit`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `wellig,lockig,kraus` · haarstaerke: `mittel,dick` · haarzustand: `trocken,glanzlos`
- bool-Flags: `locken_geeignet`

_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_

---

## the_champ — The Champ™ Pflegendes Trockenshampoo

**Linie**: `studio_one` · **Slot**: `finish` · **Pflegelevel**: `LOW,MID,HIGH` · **Intensität**: `alle`

**Stammdaten-Funktion** (für PDF-Verifikation):
- hauptfunktion: `reinigung,frische`
- nebenfunktionen: `volumen,textur`

**Stammdaten-Filter** (Zielgruppe laut Sheet):
- kopfhaut: `-` · haarstruktur: `alle` · haarstaerke: `alle` · haarzustand: `kraftlos`
- bool-Flags: `locken_geeignet`

**Direkt-REQ-Routing** (Produkt namentlich im filter):
- `REQ-14` (optional): WENN `needs_dry_shampoo=TRUE` → slot `finish` (filter: `the_champ`)

---
