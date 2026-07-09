# Refactor-Skizze: map_slot_rules Wirkungs-Abstraktion

**Stand:** 2026-07-09
**Zweck:** Whitelabel-Blocker — 26 MONAT-Produkt-Key-Filter durch Wirkungs-Formulierungen ersetzen, damit der Workflow marken-neutral wird und Nicht-MONAT-Kataloge (V1 Punkt 4 Backlog) grundsätzlich unterstützt werden.
**Freigabe erforderlich vor Umsetzung.**

---

## 1. Engine-Analyse — kein Umbau nötig

Node 12 unterstützt heute schon eine flexible Filter-Syntax (Zeilen 253-266 im jsCode):

```js
const filters = filterStr.split('|');           // OR-Verzweigung
filters.some(fStr => {
  const flagMatch = fStr.match(/^([a-zA-Z_][a-zA-Z0-9_]*)=(TRUE|FALSE)$/);
  if (flagMatch) return boolVal(prod[field]) === expected;   // Boolean-Flag
  return prod.produkt_key?.includes(fStr)                    // Substring-Match
      || prod.produktlinie?.includes(fStr)                   // auf 3 Feldern
      || prod.hauptfunktion?.includes(fStr);
});
```

Der Refactor braucht **nur `filter`-Zellen-Edits im Sheet**, keinen jsCode-Umbau in Node 11/12. Bereits produktiv im Ist-Zustand:
- REQ-04: `filter=ist_hitzeschutz=TRUE` (Wirkungs-Flag)
- REQ-03: `filter=bond_iq|reparatur` (Produktlinie ODER Wirkung — Hybrid)

Kandidaten-Pool wird zuvor bereits nach `slot_typ` diskriminiert (Zeile 237). Damit reicht in fast allen Fällen eine `hauptfunktion`-Substring, weil der Slot die Grob-Trennung macht.

**Migration-Patch #20 (Zeile 242-250):** Bei produkt_key-Literalfiltern werden Produkte mit passendem produkt_key aus dem Gesamtpool nachgeführt, um slot_typ-Mismatches (moxie_mousse styling_1↔styling_3) zu umgehen. **Bei Wirkungs-Filtern greift diese Sonderregel nicht** — Wirkungs-Regeln müssen mit dem Kandidaten-Pool der Stammdaten-slot_typ auskommen. Folge: REQ-16b braucht Sonderbehandlung (siehe Cluster 9).

---

## 2. Refactor pro Cluster

**Formatlegende pro Regel:**
- `filter (alt) → filter (neu)`
- MONAT-Produkt(e) hf/nf/linie/flags/slot_typ
- Rationale + Bulk-Impact-Prognose
- Was der Nicht-MONAT-Katalog dafür anbieten muss

---

### Cluster 1 — Bond-IQ-Reparatur-Linie (4 Regeln)

Bond-IQ ist bei MONAT die Repair-Bonding-Linie. Wirkungs-Signatur: `hauptfunktion=reparatur` (alle 4 Produkte), teilweise `bonding` (nur leave-in), `ist_bonding=TRUE` (nur leave-in).

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-02 | spuelung | `bond_iq` | `reparatur` | Slot-Typ-Vorfilter reduziert auf Spülungen mit hf=reparatur. Bei MONAT: nur bond_iq_spuelung. Nicht-MONAT-Katalog braucht mindestens 1 Spülung mit hauptfunktion enthält `reparatur`. |
| REQ-03 | maske | `bond_iq\|reparatur` | `reparatur` | Slot-Typ=maske. Bei MONAT: super_feuchtigkeitsmaske (hf=erw_feuchtigkeit? prüfen), replenish_maske. Achtung: die Cluster-Zuordnung ist hier evtl. weiter — REQ-03 will „irgendeine Repair-Maske", nicht spezifisch Bond IQ. |
| REQ-21 | leave_in | `bond_iq_leave_in` | `ist_bonding=TRUE` | Bond-IQ-Leave-In ist bei MONAT das einzige `ist_bonding=TRUE`-Produkt. Klar diskriminierend. Nicht-MONAT-Katalog: Produkt mit `ist_bonding=TRUE` anlegen. |
| REQ-22 | nacht_serum | `bond_iq_night_day_serum` | `reparatur` | Slot-Typ=nacht_serum. Bei MONAT: nur bond_iq_night_day_serum in diesem Slot. Nicht-MONAT-Katalog: Nachtserum mit hauptfunktion enthält `reparatur`. |

---

### Cluster 2 — Scalp-Comfort-Linie (2 Regeln)

MONAT: 2 Produkte, beide `hauptfunktion=kopfhautpflege,ausgleichend` und `ist_scalp_focus=TRUE`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-05 | kopfhaut | `scalp_comfort` | `ist_scalp_focus=TRUE\|ausgleichend` | Substring `ausgleichend` matcht hauptfunktion. Flag `ist_scalp_focus=TRUE` als Sicherheitsnetz. Bei MONAT: scalp_comfort_behandlung matched via slot_typ=kopfhaut. |
| REQ-20 | kopfhaut_taeglich | `scalp_comfort_serum` | `ist_scalp_focus=TRUE\|ausgleichend` | Slot-Typ=kopfhaut_taeglich isoliert scalp_comfort_serum + ir_clinical_kopfhautserum. Beide haben `ist_scalp_focus=TRUE`. Achtung: bei aktuellem Filter-Wert würde REQ-20 auch ir_clinical_kopfhautserum matchen — heute strikt `scalp_comfort_serum`. Ranking Node 12 sortiert. |

---

### Cluster 3 — IR Clinical Kopfhaut-Serum (1 Regel)

MONAT: `hauptfunktion=verdichtend,haarwuchs,kopfhautpflege`, `ist_scalp_focus=TRUE`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-06 | kopfhaut | `ir_clinical_kopfhautserum` | `haarwuchs\|verdichtend` | Slot-Typ=kopfhaut. Bei MONAT-Kopfhaut-Slot gibt es kopfhaut_peeling (kein `haarwuchs`), scalp_comfort_behandlung (`ausgleichend`, kein `haarwuchs`). Filter `haarwuchs` diskriminiert nur ir_clinical_kopfhautserum. |

⚠ **Achtung**: REQ-06 hat einen Slot-Typ-Mismatch (Migration #20 Bonus-Fix, ir_clinical_kopfhautserum.slot_typ=`kopfhaut_taeglich` aber REQ-06.slot_typ=`kopfhaut`). Wirkungs-Filter verliert die Patch-#20-Kompensation. Optionen:
- (a) REQ-06.slot_typ auf `kopfhaut_taeglich` korrigieren
- (b) Produkt-Slot-Typ auf `kopfhaut` migrieren
- (c) Patch #20 auf Wirkungs-Filter erweitern (Zeile 242 im Engine-jsCode)

Empfehlung: (a) — Sheet-Edit, kein Engine-Patch.

---

### Cluster 4 — Entwirrungsspray (2 Regeln)

MONAT: `hauptfunktion=entwirren`, `produktlinie=basis`, slot_typ=leave_in.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-07 | leave_in | `entwirrungsspray` | `entwirren` | Slot-Typ=leave_in reduziert auf leave-in-Produkte mit `entwirren` in hauptfunktion. Bei MONAT: nur entwirrungsspray. |
| REQ-18 | leave_in | `entwirrungsspray` | `entwirren` | Identisch. |

---

### Cluster 5 — Rejuveniqe-Öl (3 Regeln)

MONAT: `hauptfunktion=glanz,feuchtigkeit`, `produktlinie=basis`, slot_typ=finish.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-08 | finish | `rejuveniqe` | ⚠ **klärungsbedürftig** | Substring `rejuveniqe` matcht heute rejuveniqe_oel UND rejuvabeads (beide haben „rejuv" im produkt_key). Ist rejuvabeads (slot_typ=leave_in) im Slot=finish überhaupt Kandidat? Nein — Vorfilterung. Also nur rejuveniqe_oel. Vorschlag: `glanz` (hauptfunktion) — matcht rejuveniqe_oel und alle anderen Finish-Öle mit Glanz-Wirkung. |
| REQ-17 | finish | `rejuveniqe_oel` | `glanz` | Analog REQ-08. |
| REQ-17b | finish | `rejuveniqe_oel` | `glanz` | Analog. |

⚠ **Design-Frage**: REQ-08, REQ-17, REQ-17b filtern alle auf ein Öl-Produkt im finish-Slot. Ist das dreifache Regel-Set fachlich gerechtfertigt (verschiedene Trigger)? Falls ja, alle drei auf `glanz` migrieren. Falls nein: konsolidieren.

---

### Cluster 6 — Curl-Creme (3 Regeln)

MONAT: `hauptfunktion=locken,feuchtigkeit`, `produktlinie=curl_perfection`, `slot_typ=styling_1`, `locken_geeignet=TRUE`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-11 | styling_1 | `curl_creme` | `locken` | Slot-Typ=styling_1, Substring `locken` matcht hauptfunktion. Bei MONAT: nur curl_creme (curl_gelee ist styling_2, curl_auffrischer styling_3). |
| REQ-11b | styling_1 | `curl_creme` | `locken` | Analog. |
| REQ-11c | styling_1 | `curl_creme` | `locken` | Analog. |

---

### Cluster 7 — Curl-Gelée (1 Regel)

MONAT: `hauptfunktion=locken,definition,halt`, `produktlinie=curl_perfection`, `slot_typ=styling_2`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-12 | styling_2 | `curl_gelee` | `locken` | Slot-Typ=styling_2 isoliert curl_gelee bei MONAT. Nicht-MONAT-Katalog: styling_2-Produkt mit `locken` in hf. |

---

### Cluster 8 — Curl-Auffrischer (1 Regel)

MONAT: `hauptfunktion=locken,auffrischung`, `slot_typ=styling_3`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-13 | styling_3 | `curl_auffrischer` | `auffrischung` | Slot-Typ=styling_3. Substring `auffrischung` matcht curl_auffrischer und nichts sonst im MONAT-Katalog. |

---

### Cluster 9 — Volumen-Styling (4 Regeln)

MONAT-Produkte:
- moxie_mousse: hf=`volumen,halt`, slot_typ=styling_1
- volumen_spray: hf=`volumen`, slot_typ=styling_1

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-16 | styling_1 | `moxie_mousse` | `volumen\|halt` | Substring `volumen` matcht beide + jedes andere Volumen-Produkt im styling_1-Pool. Ranking entscheidet. Migration-#20-Slot-Typ-Patch fällt weg — moxie_mousse.slot_typ ist bereits styling_1, kein Konflikt. |
| REQ-16b | **styling_3** | `moxie_mousse` | ⚠ **braucht Engine-Patch oder Data-Fix** | Der Slot-Typ-Mismatch (moxie_mousse.slot_typ=styling_1, REQ-16b.slot_typ=styling_3) wurde von Migration #20 durch produkt_key-Literal-Bypass gelöst. Wirkungs-Filter greift diesen Bypass nicht. Optionen: (a) neue Datenzeile moxie_mousse_styling3 mit slot_typ=styling_3, (b) REQ-16b.slot_typ auf styling_1 anpassen und REQ-19b via requires_not koordinieren, (c) Engine-Patch: bei Wirkungs-Filter Slot-Typ-Override erlauben. Vorschlag: (b) — weniger invasiv. |
| REQ-19 | styling_1 | `moxie_mousse\|volumen_spray` | `volumen` | Klar. |
| REQ-19b | styling_1 | `moxie_mousse\|volumen_spray` | `volumen` | Klar. |

---

### Cluster 10 — Trockenshampoo (1 Regel)

MONAT: the_champ, hf=`reinigung,frische`, nf=`volumen,textur`, slot_typ=finish.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-14 | finish | `the_champ` | ⚠ **klärungsbedürftig** | Substring `frische` würde matchen, aber die semantische Kategorie ist „Trockenshampoo" — dafür gibt es kein Wirkungs-Wort im Vokabular. Vorschlag: neuer Boolean-Flag `ist_trockenshampoo=TRUE` im produktdatenbank-Schema; filter=`ist_trockenshampoo=TRUE`. Analog zu `ist_hitzeschutz`/`ist_bonding`/`ist_scalp_focus`. |

---

### Cluster 11 — Smoothing-Föhn-Spray (1 Regel)

MONAT: smoothing_fohn_spray, hf=`frizz_reduktion,hitzeschutz`, `ist_hitzeschutz=TRUE`, slot_typ=styling_1.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-04b | styling_1 | `smoothing_fohn_spray` | `ist_hitzeschutz=TRUE\|frizz_reduktion` | Kombiniert Hitzeschutz-Flag mit Frizz-Wirkung. Beim MONAT-Katalog matcht auch hitzeschutzspray (ist_hitzeschutz=TRUE, aber ohne frizz_reduktion?). Prüfen ob Ranking sauber diskriminiert. |

---

### Cluster 12 — Restore Leave-In (1 Regel)

MONAT: `hauptfunktion=feuchtigkeit`, `produktlinie=basis`, slot_typ=leave_in.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-23 | leave_in | `restore_leave_in` | ⚠ **klärungsbedürftig** | hauptfunktion `feuchtigkeit` ist unspezifisch — matched viele Produkte. Slot-Typ=leave_in reduziert auf leave-in-Kandidaten mit `feuchtigkeit`: bei MONAT nur bond_iq_leave_in (aber `hauptfunktion=reparatur,bonding`, matched nicht), rejuvabeads (leave_in, aber `hauptfunktion=reparatur,versiegelung`), entwirrungsspray (`hauptfunktion=entwirren`). Also nur restore_leave_in matched `feuchtigkeit`. OK — Vorschlag: `feuchtigkeit`. |

---

### Cluster 13 — Kopfhaut-Peeling (1 Regel)

MONAT: `hauptfunktion=kopfhautpflege,reinigung`, `produktlinie=reinigende`, `slot_typ=kopfhaut`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-24 | kopfhaut | `kopfhaut_peeling` | `reinigung` | Slot-Typ=kopfhaut isoliert auf Kopfhaut-Produkte, `reinigung` matcht kopfhaut_peeling. scalp_comfort_behandlung hat `kopfhautpflege,ausgleichend`, keine `reinigung`. ir_clinical hat auch keine `reinigung`. Klar diskriminierend. |

---

### Cluster 14 — MONAT Black 2-in-1 (1 Regel)

MONAT: `hauptfunktion=reinigung,verdichtend`, `slot_typ=shampoo`, produktlinie=`monat_black`.

| REQ | slot_typ | filter alt | filter neu | Bemerkung |
|---|---|---|---|---|
| REQ-30 | shampoo | `monat_black` | ⚠ **klärungsbedürftig** | Das ist eine bewusste 2-in-1-Regel (Anna-Minimal-Routine, siehe Session 2026-07-09 Phase 6). Die Wirkung „2-in-1" ist strukturell, keine Wirkungs-CSV-Kategorie. Vorschlag: neuer Boolean-Flag `ist_zwei_in_eins=TRUE` (für Kombi-Shampoo+Spülung); filter=`ist_zwei_in_eins=TRUE`. Analog `ist_hitzeschutz` etc. |

---

## 3. Zusammenfassung Klärungsbedarf (4 Punkte)

Nur diese vier Punkte brauchen deine Entscheidung, bevor der Sheet-Refactor deployt werden kann:

1. **REQ-06 Slot-Typ-Fix**: REQ-06.slot_typ von `kopfhaut` auf `kopfhaut_taeglich` korrigieren (Migration #20-Bypass fällt weg bei Wirkungs-Filter).
2. **REQ-16b Slot-Typ-Konflikt**: (a) neue Zeile moxie_mousse_styling3, (b) REQ-16b auf styling_1 anpassen + requires_not, oder (c) Engine-Patch. Empfehlung: (b).
3. **REQ-14 Trockenshampoo-Flag**: neuen Bool-Flag `ist_trockenshampoo=TRUE` in `produktdatenbank`-Schema einführen.
4. **REQ-30 2-in-1-Flag**: neuen Bool-Flag `ist_zwei_in_eins=TRUE` in `produktdatenbank`-Schema einführen.

Alle vier Punkte sind Datenmodell-Erweiterungen im Sheet (neue Bool-Spalten oder Slot-Typ-Korrekturen), kein Engine-jsCode-Umbau.

---

## 4. Anleitung für Nicht-MONAT-Katalog (V1 Punkt 4 Backlog)

Ein Kunden-Katalog braucht mindestens ein Produkt pro folgender Wirkung/Flag-Kombination, sonst fällt die jeweilige REQ-Regel tot:

| Slot | Bedarf | Wirkungs-Signatur (mindestens) |
|---|---|---|
| shampoo | Reparatur (Bond-IQ-Ersatz) | `hauptfunktion=reparatur` |
| spuelung | Reparatur | `hauptfunktion=reparatur` |
| maske | Reparatur | `hauptfunktion=reparatur` |
| leave_in | Bonding | `ist_bonding=TRUE` |
| leave_in | Feuchtigkeits-Leave-In | `hauptfunktion=feuchtigkeit` |
| leave_in | Entwirren | `hauptfunktion=entwirren` |
| nacht_serum | Reparatur | `hauptfunktion=reparatur` |
| kopfhaut_taeglich | Verdichtung/Haarwuchs | `hauptfunktion=haarwuchs` oder `verdichtend` |
| kopfhaut_taeglich | Kopfhautberuhigung | `hauptfunktion=ausgleichend` |
| kopfhaut | Kopfhautberuhigung | `hauptfunktion=ausgleichend` + `ist_scalp_focus=TRUE` |
| kopfhaut | Peeling | `hauptfunktion=reinigung` |
| finish | Glanz-Öl | `hauptfunktion=glanz` |
| finish | Trockenshampoo | `ist_trockenshampoo=TRUE` |
| styling_1 | Curl-Creme | `hauptfunktion=locken` + `locken_geeignet=TRUE` |
| styling_1 | Volumen | `hauptfunktion=volumen` |
| styling_1 | Hitzeschutz+Frizz | `ist_hitzeschutz=TRUE` |
| styling_2 | Curl-Gel | `hauptfunktion=locken` + `locken_geeignet=TRUE` |
| styling_3 | Curl-Auffrischer | `hauptfunktion=auffrischung` + `locken_geeignet=TRUE` |
| shampoo | 2-in-1 Minimal | `ist_zwei_in_eins=TRUE` |

Wenn ein Slot-Bedarf im Kunden-Katalog nicht abgedeckt ist, feuert die REQ-Regel trotzdem, aber der Slot bleibt leer (Node 12 `available.length === 0 → continue`). Die Kundin sieht eine unvollständige Routine — deshalb ist die Katalog-Anleitung ein **UI-Hinweis** wert bei Katalog-Anlage.

---

## 5. Beweis-Test-Plan

1. **Fiktive Nicht-MONAT-Katalog-Fixture** anlegen: `wl_libraries/wl_fiktiv_test.json` — 37 Einträge, andere Marken-Namen, aber identische Wirkungs-Signaturen wie MONAT.
2. **Klon-Sync** `python3 sync_wl_produktdatenbank.py --source wl_libraries/wl_fiktiv_test.json`
3. **Bulk** gegen WL-Klon-Webhook: `python3 test_suite.py --webhook-url https://…/mybeautykey-wl-haaranalyse --workflow-id 5lPLG0y235XiIpN1 --save --gap 30`
4. **Erwartung**: 14/14 grün, gleiche Slot-Assignments wie MONAT-Baseline (weil Wirkungs-Signaturen identisch). Drift = 0/14.
5. **Zweiter Bulk** gegen MONAT-Workflow direkt (mit gleichzeitig deploytem Wirkungs-Refactor): erwartete Drift 0/14 gegen `test_results_20260709_100243.json`. Wenn Drift > 0, ist der Refactor irgendwo enger als der produkt_key-Filter.

---

## 6. Migration-Reihenfolge

1. **Entscheidungen abklären** (4 Punkte in Kap. 3)
2. **Sheet-Erweiterungen** (falls Punkt 3+4 zustimmt): `produktdatenbank` neue Spalten `ist_trockenshampoo`, `ist_zwei_in_eins`; the_champ.ist_trockenshampoo=TRUE, monat_black.ist_zwei_in_eins=TRUE
3. **Slot-Typ-Fix** (Punkt 1+2): REQ-06.slot_typ=kopfhaut_taeglich, REQ-16b.slot_typ=styling_1 + requires_not-Anpassung
4. **Sheet-Filter-Migration**: 26 Zellen umschreiben
5. **`sync_rules_to_workflow.py`** ausführen
6. **MONAT-Regressions-Bulk** (Erwartung 0/14 Drift gegen Baseline)
7. **Nicht-MONAT-Fixture bauen + WL-Bulk** (Beweis-Test)
8. **Backlog-Eintrag „REQ-Produkt-Key-Abstraktion"** als erledigt markieren

Sobald das steht, kann Layer 2 (map_conflict_rules) angegangen werden, danach Layer 3 (map_pool_filter), dann Route-Group.

---

## 7. Aufwand grob

- Kap. 3-Entscheidungen: 15 Min Diskussion
- Sheet-Edits + Sync: 30 Min
- MONAT-Regressions-Bulk: 15 Min (Bulk-Laufzeit)
- Nicht-MONAT-Fixture bauen: 30 Min
- WL-Bulk + Analyse: 15 Min
- **Gesamt Layer 1**: ~2 Stunden

Layer 2 (map_conflict_rules, 3 Regeln): 30 Min. Layer 3 (map_pool_filter, 2 Regeln): 20 Min. Zusammen unter 3 Stunden bis marken-neutrale Engine.
