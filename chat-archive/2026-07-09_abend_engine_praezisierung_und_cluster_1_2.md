# Session 2026-07-09/10 — Engine-Präzisierung + 23/26 REQ-Regeln markenneutral

**Kern-Session:** Neustart nach dem Vormittags-Fehlschlag. Engine-Filter-Semantik in Node 12 von naiver `.includes()`-Substring auf exakten Token-Match umgestellt, mit Zwischen-Fix zur sauberen Beweis-Führung. Anschließend 10 Cluster (Cluster 1 Bond-IQ, 2 Scalp-Comfort, 3a Trockenshampoo+2-in-1, 3b Curl-Perfection, 4 Öl-Familie, 5 Volumen, 5b Halt, 6 Kopfhaut-Peeling, 7 Restore, 8 Smoothing, 10 Entwirrung) markenneutral migriert. **23 von 26 Regeln migriert.** 10 saubere 0-Drift-Bulks in Folge, ein bewusst akzeptierter Drift (sarah moxie_mousse → volumen_spray, semantisch legitim). **Verbleibend: 3 Regeln (REQ-06, REQ-16b, REQ-03) am Slot-Override-Cluster.** Cluster-für-Cluster-Vorgehen bewährt sich.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-09_abend_engine_praezisierung_und_cluster_1_2.md`.
> Baseline: `test_results_20260710_125920.json` (14/14 grün, 0/14 Drift vs.
> `_120713`). **23/26 REQ-Regeln sind markenneutral**, Engine-Semantik ist
> exakt-Token-basiert (`===` bzw. `csvToArr(...).has(...)` in Node 12 Zeilen 253+).
>
> **Fokus dieser Session: Slot-Override-Cluster (letzte 3 Regeln).** Das war der
> Vormittags-Fehlschlag — Ursache damals war die naive `.includes()`-Semantik
> im Additional-Candidates-Block, nicht das Slot-Override-Konzept selbst. Die
> Engine-Präzisierung ist inzwischen live und stabil, damit sollte der ursprüngliche
> Design-Ansatz jetzt tragen.
>
> Zu erledigen:
>
> 1. **REQ-06 IR-Clinical Kopfhaut-Serum** — Regel-Slot=`kopfhaut` (wöchentlich),
>    Produkt-Slot=`kopfhaut_taeglich`. Filter aktuell = `ir_clinical_kopfhautserum`
>    (Produkt-Key). Braucht Slot-Override, dann markenneutralen Wirkungs-Filter
>    (Kandidat: `verdichtend` oder `haarwuchs`, prüfen).
> 2. **REQ-16b Moxie Volumen-Mousse (Locken)** — Regel-Slot=`styling_3`,
>    Produkt-Slot=`styling_1`. Filter aktuell = `moxie_mousse` (Produkt-Key).
>    Braucht Slot-Override + markenneutralen Filter (evtl. `volumen` mit
>    Ranking-Prüfung wie bei sarah/REQ-16 gehabt, oder Bool-Flag).
> 3. **REQ-03 reaktivieren** (aktuell `aktiv=FALSE`) — mit sauberem Wirkungs-
>    Filter, z.B. `hauptfunktion=feuchtigkeit`. Ziel: super_feuchtigkeitsmaske
>    bei trocken+HIGH. Slot-Vorfilter maske reicht wahrscheinlich für Disambi-
>    guierung, weil bond_iq-Maske im Katalog gar nicht existiert.
>
> **Kritische Vorbedingung: Design-Ansatz Slot-Override sauber überdenken.**
> Der Vormittags-Ansatz `slot_override_erlaubt=TRUE` als Sheet-Flag + Node-11-
> Durchreichen + Node-12-Additional-Candidates-Block ist konzeptuell OK, muss
> aber auf präziser Filter-Semantik (nicht Substring!) neu aufgebaut werden.
> `patch_layer1_engine.py` liegt noch — muss angepasst werden. **Bulk zwischen
> jedem Schritt** (Schema-Änderung → Engine-Patch → Filter-Migration einzeln).

## Verbleibende Cluster im Detail (für den neuen Tab)

### REQ-06 IR-Clinical Kopfhautserum
- **Regel-Kontext:** slot=kopfhaut, prio=required_conditional, trigger=hair_condition_contains(duenn), filter=`ir_clinical_kopfhautserum`, reason="IR Clinical Serum bei dünner werdendem Haar"
- **Konflikt:** ir_clinical_kopfhautserum.slot_typ ist `kopfhaut_taeglich`, REQ-06 will slot `kopfhaut` (wöchentlich). Ohne Slot-Override wird das Produkt vom Slot-Vorfilter aussortiert.
- **Katalog-Fakten:** ir_clinical_kopfhautserum hf=`verdichtend,haarwuchs,kopfhautpflege`. Andere Produkte mit `verdichtend` in HF: monat_black (slot=shampoo), volumen_spray (NF), revitalize_spuelung (NF). Andere mit `haarwuchs` in HF: keiner.
- **Vorschlag Filter nach Slot-Override:** `haarwuchs` — matched exakt nur ir_clinical_kopfhautserum. Sauber.

### REQ-16b Moxie Volumen-Mousse (Locken)
- **Regel-Kontext:** slot=styling_3, prio=required_conditional, trigger=wants_curl_volume(TRUE), filter=`moxie_mousse`, reason="Migration #20"
- **Konflikt:** moxie_mousse.slot_typ=`styling_1`, REQ-16b will styling_3.
- **Aktuell:** Wird bei nina korrekt empfohlen via Migration-#20-Substring-Block (Legacy-produkt_key-Literal-Path in Node 12 Zeilen 240-251). Der Block trägt noch, weil filter=`moxie_mousse` als Produkt-Key-Literal erkannt wird.
- **Denkfrage:** Muss die REQ-16b überhaupt markenneutral werden, oder reicht der Legacy-Path? Wenn markenneutral gewünscht: Slot-Override + Filter `volumen` mit Ranking-Prüfung (analog REQ-16 Diskussion).

### REQ-03 Feuchtigkeitsmaske
- **Regel-Kontext:** slot=maske, prio=required_conditional, trigger=hair_condition_contains(trocken) + pflegelevel_numeric(>=3), filter=`bond_iq|reparatur` (heute tot), reason="Intensiv-Feuchtigkeitsmaske bei trockenem Haar + HIGH"
- **Status:** `aktiv=FALSE` seit 2026-07-09 21:46 (Sheet-Zwischen-Fix vor Engine-Präzisierung).
- **Katalog-Fakten:** Nur 3 Masken im Katalog (replenish_maske, smoothing_tiefenbehandlung, super_feuchtigkeitsmaske). Keine bond_iq-Maske.
- **Vorschlag Filter:** `feuchtigkeit` als HF-Token → matched replenish_maske (HF) + super_feuchtigkeitsmaske (HF). Slot-Vorfilter maske reicht. Ranking entscheidet welche der beiden gewinnt; reason zielt auf „Intensiv" → wahrscheinlich super_feuchtigkeitsmaske.
- **Design-Frage:** reaktivieren jetzt oder erst nach Slot-Override-Migration? Empfehlung: **zuerst reaktivieren** (unkritisch, Slot-Override tangiert es nicht), dann Slot-Override-Cluster.

## Stand am Ende der Session

**Live-Workflow:**
- Node 12 Filter-Auswertung: **exakter Token-Match** (`===` bzw. `csvToArr(...).has(...)`) statt naiver `.includes()`. Boolean-Flag-Syntax bleibt erhalten. Migration-#20-Substring-Block (Slot-Override) bleibt unverändert.

**Sheet (`map_slot_rules`):**
- REQ-08 `filter=rejuveniqe_oel` (voll qualifizierter Produkt-Key, noch MONAT-spezifisch — für spätere Wirkungs-Migration reserviert)
- REQ-03 `aktiv=FALSE` (temporär; war effektiv tot, kommt mit Wirkungs-Filter zurück)
- REQ-02/21/22 `filter=ist_bonding=TRUE` (Cluster 1 Bond-IQ, markenneutral ✓)
- REQ-05/20 `filter=ausgleichend` (Cluster 2 Scalp-Comfort, markenneutral ✓)
- REQ-14 `filter=ist_trockenshampoo=TRUE` (Cluster 3a, markenneutral ✓)
- REQ-30 `filter=ist_zwei_in_eins=TRUE` (Cluster 3a, markenneutral ✓)
- REQ-08/17/17b `filter=ist_oel=TRUE` (Cluster 4 Öl-Familie, markenneutral ✓)
- REQ-11/11b/11c/12/13 `filter=locken` (Cluster 3b Curl-Perfection, markenneutral ✓)
- REQ-19/19b `filter=volumen` (Cluster 5, markenneutral ✓)
- REQ-16 `filter=halt` (Cluster 5b, markenneutral ✓, mit akzeptiertem sarah-Drift)
- REQ-24 `filter=ist_peeling=TRUE` (Cluster 6, markenneutral ✓)
- REQ-07/18 `filter=entwirren` (Cluster 10, markenneutral ✓)
- REQ-23 `filter=feuchtigkeit` (Cluster 7, markenneutral ✓)
- REQ-04b `filter=ist_smoothing=TRUE` (Cluster 8, markenneutral ✓)
- **Verbleibend MONAT-spezifisch:** REQ-06 `ir_clinical_kopfhautserum`, REQ-16b `moxie_mousse`
- **Verbleibend inaktiv:** REQ-03 (`aktiv=FALSE`)

**Sheet (`produktdatenbank`):**
- `bond_iq_shampoo.ist_bonding=TRUE`
- `bond_iq_spuelung.ist_bonding=TRUE`
- `bond_iq_night_day_serum.ist_bonding=TRUE`
- `bond_iq_leave_in.ist_bonding=TRUE` (war schon TRUE)
- `the_champ.ist_trockenshampoo=TRUE`
- `monat_black.ist_zwei_in_eins=TRUE`
- `rejuveniqe_oel.ist_oel=TRUE`
- `kopfhaut_peeling.ist_peeling=TRUE`
- `smoothing_deep_conditioner/fohn_spray/shampoo/tiefenbehandlung.ist_smoothing=TRUE`
- **Drei neue Spalten** (Grid von 26 → 29 Cols erweitert): `ist_oel`, `ist_peeling`, `ist_smoothing`. Alle nicht explizit gesetzten Produkte FALSE.

**Baselines der Bulk-Kette:**
| Zeit | File | Ergebnis | Zweck |
|---|---|---|---|
| 22:07 | `_220743.json` | 14/14, 0/14 Drift vs `_100243` | Sheet-Fix ohne Engine (REQ-08 rejuveniqe_oel + REQ-03 aktiv=FALSE) |
| 23:11 | `_223110.json` | 14/14, 0/14 Drift vs `_100243` | Nach Engine-Präzisierung |
| 23:11 | `_231150.json` | 14/14, 0/14 Drift vs `_223110` | Nach Cluster 1 Bond-IQ |
| 23:38 | `_233851.json` | 14/14, 0/14 Drift vs `_231150` | Nach Cluster 2 Scalp-Comfort |
| 00:19 | `_001952.json` | 14/14, 0/14 Drift vs `_233851` | Nach Cluster 3a Trockenshampoo+2-in-1 |
| 00:53 | `_005308.json` | 14/14, 0/14 Drift vs `_001952` | Nach Cluster 4 Öl-Familie |
| 01:26 | `_012624.json` | 14/14, 0/14 Drift vs `_005308` | Nach Cluster 5 (REQ-19/19b Volumen) |
| 01:55 | `_015548.json` | 14/14, 0/14 Drift vs `_012624` | Nach Cluster 6 Kopfhaut-Peeling |
| 02:24 | `_022438.json` | 14/14, 0/14 Drift vs `_015548` | Nach Cluster 10 Entwirrung |
| 09:30 | `_093015.json` | 14/14, 0/14 Drift vs `_022438` | Nach Cluster 3b Curl-Perfection (5 Regeln!) |
| 11:05 | `_110509.json` | 14/14, 0/14 Drift vs `_093015` | Nach Cluster 8 Smoothing/Föhn |
| 12:07 | `_120713.json` | 14/14, **1/14 Drift** vs `_110509` | Nach Cluster 5b (REQ-16 halt) — sarah moxie_mousse→volumen_spray, akzeptiert |
| 12:59 | `_125920.json` | 14/14, 0/14 Drift vs `_120713` | Nach Cluster 7 (REQ-23 feuchtigkeit) — **aktuelle Baseline** |

## Was in dieser Session passiert ist

### Phase 1 — Vor-Analyse der neuen Engine-Semantik

Vor dem eigentlichen Engine-Patch alle 20 aktiven Filter-Werte aus `map_slot_rules` simuliert: welche Produkte matchen alte Substring-Semantik vs. neue exakte Token-Semantik? Ergebnis: **2 Filter driften**, wenn man nur die Engine ändert:

- **REQ-08 `filter=rejuveniqe`** → alte Engine matched `rejuveniqe_oel` per Substring (`rejuveniqe ⊂ rejuveniqe_oel`), neue Engine matched null. Regel wäre tot.
- **REQ-03 `filter=bond_iq|reparatur`** → alte Engine matched null (Substring-Zufall, „reparatur" nur in nebenfunktionen die alte Engine gar nicht prüfte), neue Engine würde `smoothing_tiefenbehandlung` matchen (Token in nebenfunktionen). Regel wäre neu-lebendig.

Beide Fälle waren gestern übersehen worden. Skizze v1 hat auf die Boolean-Flag-Präzision vertraut und die Wirkungs-Substring-Falle nicht antizipiert. Neu-Erkenntnis: **jeder Refactor-Beweis-Test braucht Vor-Simulation der Filter-Diff pro Regel**.

### Phase 2 — Zwei-Stufen-Fix vor der Engine-Änderung

Statt Big-Bang zwei Zwischen-Schritte, um einen sauberen Beweis-Test zu bekommen:

1. **REQ-08 Sheet-Fix**: `filter=rejuveniqe` → `rejuveniqe_oel` (voller Produkt-Key). Semantisch äquivalent zur alten Substring-Bedeutung.
2. **REQ-03 Sheet-Fix**: `aktiv=TRUE` → `FALSE`. War ohnehin tot, wird in eigener Cluster-Runde mit Wirkungs-Filter reaktiviert.
3. Sheet-Backup + `sync_rules_to_workflow.py` + PUT.
4. Bulk `test_results_20260709_220743.json`: 14/14 grün, **0/14 Drift** vs `_100243`. Beweis: Sheet-Fixes sind neutral.

### Phase 3 — Engine-Präzisierung

Neues Skript `patch_engine_filter_precision.py` gebaut. Ersetzt in Node 12 den Wirkungs-Filter-Block:

```js
// ALT (naiv):
return prod.produkt_key?.includes(fStr)
    || prod.produktlinie?.includes(fStr)
    || prod.hauptfunktion?.includes(fStr);

// NEU (exakter Token-Match):
const hfSet = new Set(csvToArr(prod.hauptfunktion));
const nfSet = new Set(csvToArr(prod.nebenfunktionen));
return prod.produkt_key === fStr
    || prod.produktlinie === fStr
    || hfSet.has(fStr)
    || nfSet.has(fStr);
```

Boolean-Flag-Syntax (`ist_hitzeschutz=TRUE`) unverändert. Migration-#20-Substring-Block (Slot-Override) unverändert.

- Dry-Run + PUT + GET-Verifikation ✓
- Bulk `test_results_20260709_223110.json`: 14/14 grün, **0/14 Drift** vs `_100243`. **Beweis: Engine-Präzisierung ändert unter aktuellen Filter-Werten nichts.**

### Phase 4 — Cluster 1 Bond-IQ (3 Regeln)

Zielregeln: REQ-02 (spuelung), REQ-21 (leave_in), REQ-22 (nacht_serum).

**Design-Entscheidung**: Bool-Flag `ist_bonding=TRUE` statt hauptfunktion-Erweiterung. Rationale:
- „bonding" ist eine Technologie-Kategorie, kein Wirkeffekt — Bool-Flag semantisch sauberer
- `ist_bonding` bereits als Spalte in Produktdatenbank vorhanden (bisher nur bei bond_iq_leave_in TRUE)
- `ist_hitzeschutz=TRUE` läuft bei REQ-04 seit langem produktiv → gleiches Muster
- `ist_bonding` wird nirgends sonst in der Engine konsumiert (Grep bestätigt) → keine Nebenwirkungen

**Sheet-Änderungen:**
- `produktdatenbank`: `bond_iq_shampoo/spuelung/night_day_serum.ist_bonding=TRUE`
- `map_slot_rules`: REQ-02/21/22 `filter=ist_bonding=TRUE`

**Slot-Vorfilter macht Disambiguierung:** REQ-02 (slot=spuelung) → nur `bond_iq_spuelung`; REQ-21 (leave_in) → nur `bond_iq_leave_in`; REQ-22 (nacht_serum) → nur `bond_iq_night_day_serum`.

Bulk `test_results_20260709_231150.json`: 14/14 grün, **0/14 Drift** vs `_223110`.

### Phase 5 — Cluster 2 Scalp-Comfort (2 Regeln)

Zielregeln: REQ-05 (kopfhaut, wöchentlich), REQ-20 (kopfhaut_taeglich).

**Design-Entscheidung**: Wirkungs-Token `ausgleichend` (kein neuer Bool-Flag). Rationale:
- `ausgleichend` als Token in nebenfunktionen bei genau den 2 scalp_comfort-Produkten (behandlung + serum) und sonst nirgends
- Neue Engine prüft auch nebenfunktionen → exakter Match auf `ausgleichend` genügt
- `ir_clinical_kopfhautserum` (auch `ist_scalp_focus=TRUE`) hat NICHT `ausgleichend` → wird korrekt ausgeschlossen
- Slot-Vorfilter (kopfhaut vs. kopfhaut_taeglich) macht die Disambiguierung zwischen behandlung/serum

**Sheet-Änderung:**
- `map_slot_rules`: REQ-05/20 `filter=ausgleichend`

Bulk `test_results_20260709_233851.json`: 14/14 grün, **0/14 Drift** vs `_231150`.

## Neue Konventionen

- **Vor-Simulation vor Engine-Refactor**: bei jeder Engine-Semantik-Änderung erst pro-Filter-Simulation (ALT vs. NEU) gegen aktuelle Produktdatenbank fahren, um „latent tote" oder „latent versteckte" Regeln zu finden, die durch den Refactor lebendig oder tot würden. Vermeidet die Falle von Vormittag.
- **Bool-Flag vs. Wirkungs-Token**: Faustregel für Cluster-Design:
  - **Bool-Flag** (`ist_X=TRUE`), wenn das Attribut eine **Kategorie/Technologie** ist (bonding, hitzeschutz, trockenshampoo, 2-in-1). Vorteil: exakt kontrollierbar, kein CSV-Rauschen.
  - **Wirkungs-Token** (`hauptfunktion/nebenfunktionen`), wenn das Attribut eine **funktionale Wirkung am Haar** ist (ausgleichend, feuchtigkeit, reparatur, hitzeschutz-Effekt). Vorteil: Katalog-Autor kann per CSV-Zelle steuern ohne Schema-Änderung.
- **Cluster-Bulk-Pflicht**: 0-Drift-Bulk NACH jedem Cluster gegen die vorherige Cluster-Baseline. Bewährte Praxis.

## Neue/aktualisierte Artefakte

- `patch_engine_filter_precision.py` (Node 12 exakter Token-Match)
- `patch_layer1_engine.py` (aus Vormittag, für Slot-Override — noch nicht wieder angewendet; braucht Neu-Design mit präziser Filter-Semantik)
- Backups:
  - `backups/sheets_20260709_214600_pre_engine_precision/`
  - `backups/workflow_backup_20260709_221012_pre_engine_precision.json`
  - `backups/sheets_20260709_224934_pre_cluster1_bond_iq/`
  - `backups/sheets_20260709_231725_pre_cluster2_scalp/`

## Bewusst NICHT in dieser Session gemacht

- **REQ-03 Reaktivierung**: bleibt `aktiv=FALSE` bis eigene Cluster-Runde mit sauberem Wirkungs-Filter (z.B. `hauptfunktion=feuchtigkeit` → matched super_feuchtigkeitsmaske + replenish_maske; Slot-Vorfilter macht Rest).
- **Slot-Override-Refactor** (REQ-16b, `slot_override_erlaubt=TRUE`-Mechanik): aus Vormittag zurückgestellt, bis der Grund-Refactor komplett ist.
- **Route-Group** `src/app/(whitelabel)/`: erst nach Layer 1-3 stabil.
- **HANDOVER.md-Update**: keine Struktur-Änderungen die HANDOVER berühren.

## Offene Punkte für nächste Session

1. **Cluster 3**: entweder Curl-Perfection (6 Regeln, groß) oder the_champ+monat_black (2 Regeln, klein, mit vorbereiteten Bool-Spalten). Klein-erst-Empfehlung: die 2 Bool-Flag-Regeln, weil die Sheet-Struktur schon steht.
2. **REQ-08 restlich**: `rejuveniqe_oel` ist noch Produkt-Key. Migration wahrscheinlich auf neuen Bool-Flag `ist_oel` oder Wirkungs-Token. Braucht Katalog-Analyse: welche Produkte sind Öle?
3. **REQ-03 reaktivieren** in eigener Runde.
4. **Route-Group + Frontend**: erst nach Layer 1-3.

## Cluster-Roadmap (26 → verbleibend ~21)

| Cluster | Regeln | Vermutlicher Weg |
|---|---|---|
| ✅ 1 Bond-IQ | REQ-02, REQ-21, REQ-22 | Bool-Flag `ist_bonding` |
| ✅ 2 Scalp-Comfort | REQ-05, REQ-20 | Wirkungs-Token `ausgleichend` |
| ✅ 3a Trockenshampoo + 2-in-1 | REQ-14, REQ-30 | Bool-Flags `ist_trockenshampoo` + `ist_zwei_in_eins` |
| ✅ 4 Öl-Familie | REQ-08, REQ-17, REQ-17b | Bool-Flag `ist_oel` (neue Spalte) |
| ✅ 5 Volumen (partial) | REQ-19, REQ-19b | Wirkungs-Token `volumen` |
| ✅ 6 Kopfhaut-Peeling | REQ-24 | Bool-Flag `ist_peeling` (neue Spalte) |
| ✅ 10 Entwirrung | REQ-07, REQ-18 | Wirkungs-Token `entwirren` |
| ✅ 3b Curl-Perfection | REQ-11, REQ-11b, REQ-11c, REQ-12, REQ-13 | Wirkungs-Token `locken` |
| ✅ 8 Smoothing/Föhn | REQ-04b | Bool-Flag `ist_smoothing` (neue Spalte, 4 Produkte) |
| ✅ 5b Halt (REQ-16) | REQ-16 | Wirkungs-Token `halt` — **1 Drift akzeptiert** (sarah: moxie_mousse → volumen_spray, fachlich vertretbar) |
| ✅ 7 Restore/Leave-in | REQ-23 | Wirkungs-Token `feuchtigkeit` — 0 Drift (restore_leave_in war ohnehin nirgends in finaler Routine) |
| 9 IR-Clinical (Slot-Konflikt) | REQ-06 | Slot-Override-Cluster, eigene Runde |
| 16b Moxie Slot-Konflikt | REQ-16b | Slot-Override-Cluster, eigene Runde |
| 6 Kopfhaut-Peeling | REQ-24 | Wirkungs-Token `reinigung`+`kopfhautpflege` |
| 7 Restore/Bond-Comfort | REQ-23 | Wirkungs-Token oder Bool |
| 8 Smoothing/Föhn | REQ-04b | vermutlich `hitzeschutz`+`glaettend` |
| 9 IR-Clinical | REQ-06 (Slot-Override!) | eigene Runde nach Cluster 8 |
| 10 Entwirrung | REQ-07, REQ-18 | Wirkungs-Token `entwirrung` |
| 11 Monat-Black-Schluss | REQ-03 reaktivieren | Wirkungs-Token `feuchtigkeit` |
