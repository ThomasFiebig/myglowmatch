# Session 2026-07-09 (Tag) — Intensitaet-Fixes + Layer-1-Refactor-Versuch (rolled back)

**Kern-Session:** 3 Intensitaet-Fixes aus PDF-Audit erledigt (rejuveniqe_oel, restore_leave_in, curl_gelee) — jeweils 0/14 Drift. Danach Anlauf für Layer-1-Whitelabel-Refactor gestartet (26 REQ-Regeln von Produkt-Key auf Wirkungs-Filter umstellen), gescheitert an unerwartet naiver Substring-Semantik des bestehenden Filter-Parsers. Live-Rollback abgeschlossen, keine Kundinnen betroffen. Konzeptionelle Skizze bleibt gültig, Umsetzung muss präziser designed werden.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-09_intensitaet-fixes-und-layer1-fehlschlag.md` und
> `refactor_req_wirkung_skizze.md`. Live-Workflow ist auf pre-Layer1-Stand, MONAT
> läuft normal, Baseline-Bulk `test_results_20260709_100243.json` (0/14 Drift
> gegen Vorabend). PDF-Audit ist damit abgeschlossen (35/37 auditiert, curl_gelee
> zuletzt erledigt).
>
> Nächster Anlauf: Whitelabel-Blocker „REQ-Produkt-Key-Abstraktion" (Backlog
> SAAS_BACKLOG.md Kap. 4). Grundsatz-Design bekannt, aber der bestehende
> Node-12-Filter macht **naiven Substring-Match** auf hauptfunktion — das war
> heute die Falle. Nächste Session braucht Engine-Refactor der Filter-Semantik
> BEVOR die 26 Regeln migriert werden (Details in Kap. „Neustart-Plan" unten).
>
> Offen für nächste Session (Priorität):
>
> 1. **Layer-1 Neustart** — Engine-Filter präzisieren (exakter Token-Match auf
>    hauptfunktion/nebenfunktion, keine naive `.includes()`-Substring), dann pro
>    Cluster migrieren mit Bulk-Verifikation nach jeder Regel-Gruppe.
> 2. **Layer 2/3** — `map_conflict_rules` (3 Regeln) und `map_pool_filter`
>    (2 Regeln) analog abstrahieren, wenn Layer 1 stabil.
> 3. **Route-Group** `src/app/(whitelabel)/` — erst NACH Layer 1-3, weil sonst
>    gegen bewegliches Backend gebaut wird.

## Stand am Ende der Session

- **Live-Workflow**: pre-Layer1-Stand (`workflow_backup_20260709_114902_pre_layer1_engine.json` restored via PUT), MONAT-Regel-Set produkt-key-basiert wie vorher. Sanity-Test Sina 9/9 identisch zur Baseline.
- **Sheet**: `map_slot_rules` alle 31 Regeln aus CSV-Backup restored (filter + slot_typ zurück, `slot_override_erlaubt` auf FALSE). `produktdatenbank.the_champ.ist_trockenshampoo=FALSE` und `produktdatenbank.monat_black.ist_zwei_in_eins=FALSE` zurückgesetzt.
- **Sheet-Schema-Erweiterungen bleiben** (unschädlich): `map_slot_rules.slot_override_erlaubt`-Spalte und `produktdatenbank.ist_trockenshampoo/ist_zwei_in_eins`-Spalten existieren jetzt strukturell, alle Werte FALSE. Die Original-Engine ignoriert sie.
- **3 Intensitaet-Fixes bleiben live**:
  - `rejuveniqe_oel.intensitaet: intensiv → leicht`
  - `restore_leave_in.intensitaet: intensiv → leicht`
  - `curl_gelee.intensitaet: intensiv → alle`
- **Baseline-Bulk** `test_results_20260709_100243.json` (14/14 grün, 0/14 Drift gegen Vorabend `_012817`) bleibt die aktuelle Referenz.
- **Backlog-Eintrag** „REQ-Produkt-Key-Abstraktion" in `SAAS_BACKLOG.md` Kap. 4 dokumentiert (26 Regeln, Design-Choice, Whitelabel-Blocker).
- **Skizze** `refactor_req_wirkung_skizze.md` liegt vor, ist konzeptuell gültig, muss aber um „Engine-Filter-Präzisierung als Vorbedingung" ergänzt werden.

## Was in dieser Session passiert ist

### Phase 1 — Prio 1 aus Vornacht: rejuveniqe_oel + restore_leave_in

PDF-Belege (aus Session 2026-07-09-nacht dokumentiert):
- rejuveniqe_oel-PDF: „Mehrzweck-Öl… täglicher Gebrauch / Behandlung vor Shampoo" → `leicht`
- restore_leave_in-PDF: „intensive Feuchtigkeit, ohne zu beschweren… tägl. Anwendung möglich" → `leicht`

Fix-Pipeline:
1. Backup `backups/sheets_20260709_090730_pre_intensitaet_fix/`
2. Sheet-Update via `sheets_writer.py` — beide auf `leicht`
3. `sync_rules_to_workflow.py` (10/10 SYNCS ✓)
4. `wl_libraries/sina_monat.json` gepatcht (2 Einträge)
5. `sync_wl_produktdatenbank.py --source` → Δ-Report zeigt genau die 2 Einträge
6. Bulk `test_results_20260709_091907.json`: 14/14 grün, **0/14 Drift** vs. Baseline `_012817`

Impact-Prognose bestätigt: `intensitaet` ist Node-12-Stufe-11-Tiebreaker, für die betroffenen Produkte gibt es in ihren Slots keine Ties → keine Empfehlungs-Änderung.

### Phase 2 — Prio 2: curl_gelee PDF-Audit + Fix

Agent-Audit vom Vorabend hatte curl_gelee als „ambivalent" markiert (PDF-Zugriffsproblem, nur Deckblatt gelesen). Manuell alle 15 PDF-Seiten geprüft:

- curl_creme (PDF S.6): Header „**leichte** Styling-Creme" → sheet-Wert `leicht` ✓
- curl_auffrischer (PDF S.8): Header „**ultraleichte** Styling-Spray" → sheet-Wert `leicht` ✓
- curl_gelee (PDF S.7): kein „leicht"/„intensiv"-Wort im Header oder Body, VORTEILE-Liste ambivalent („Pflegt tiefwirksam" vs. „ohne Steifheit/Rückstände")

Entscheidung: PDF-strikt-Konvention → bei echter Ambivalenz `alle` (Default, bias-frei). `intensiv` war nie PDF-belegt.

Fix-Pipeline analog Phase 1:
1. Backup `backups/sheets_20260709_095325_pre_curl_gelee_fix/`
2. Sheet-Update `curl_gelee.intensitaet: intensiv → alle`
3. Workflow-Sync ✓
4. WL-Bibliothek + Klon-Sync (Δ-Report exakt 1 Zeile)
5. Bulk `test_results_20260709_100243.json`: 14/14 grün, **0/14 Drift**

**PDF-Audit-Track damit abgeschlossen** — 35/37 Produkte PDF-strikt auditiert (die 2 verbleibenden Original-Mockup-Referenzen waren nie im Audit-Backlog).

### Phase 3 — Tomis Whitelabel-Frage: „bekommen wir das überhaupt hin?"

Tomi hat den REQ-12 Produkt-Key `curl_gelee` als whitelabel-untypisch erkannt (aus Backlog-Eintrag kurz davor). Nach seiner Nachfrage strukturelle Karte gebaut:

- **`map_slot_rules`**: 26/31 Regeln mit MONAT-Produkt-Keys + 2 mit Produktlinien = 28
- **`map_conflict_rules`**: 3/3 aktive mit MONAT-Produkt-Keys
- **`map_pool_filter`**: 2/2 aktive mit MONAT-Produktlinien
- **`produktdatenbank`**: 37 Zeilen embedded in Node 08 (tenant-spezifisch überschreibbar via Adapter)
- Restliche 6 Tabs sind bereits marken-neutral (Profil-Vokabular, Wirkungs-Mapping)

Antwort: Ja machbar, aber Route-Group anlegen ist Schritt 5, nicht 1. Reihenfolge: Regel-Engine marken-neutralisieren → Beweis mit fiktivem Nicht-MONAT-Katalog → dann Route-Group + Frontend.

### Phase 4 — Skizze `refactor_req_wirkung_skizze.md`

Vor Umsetzung eine detaillierte Skizze gebaut, Cluster-für-Cluster (14 Cluster für die 26 Regeln), mit Klärungspunkten:

1. **REQ-06 Slot-Widerspruch** — REQ-06.slot_typ=`kopfhaut` vs. ir_clinical_kopfhautserum.slot_typ=`kopfhaut_taeglich`, heute überbrückt via Engine-Patch #20 (nur wirksam bei produkt_key-Literal-Filter). Bei Wirkungs-Filter fällt Patch weg → REQ-06 wird tot.
2. **REQ-16b Slot-Konflikt** — moxie_mousse.slot_typ=`styling_1` vs. REQ-16b.slot_typ=`styling_3` (Migration #20-Fall).
3. **REQ-14 the_champ** — Trockenshampoo-Kategorie hat kein Wirkungs-Wort → neue Bool-Spalte `ist_trockenshampoo`.
4. **REQ-30 monat_black** — 2-in-1-Shampoo-Kategorie hat kein Wirkungs-Wort → neue Bool-Spalte `ist_zwei_in_eins`.

Zwischenerkenntnis: Node 12 unterstützt bereits eine Boolean-Flag-Syntax (`ist_hitzeschutz=TRUE` an REQ-04 produktiv) → kein Engine-Grundumbau nötig, nur Sheet-Cell-Migration. **Diese Einschätzung war die Falle** — der Filter-Parser war präzise beim Boolean-Fall, aber naiv beim Wirkungs-Fall (Substring).

### Phase 5 — Konsolidierungs-Diskussion Kopfhaut-Slots

Tomi hat die Slot-Trennung `kopfhaut` vs. `kopfhaut_taeglich` hinterfragt. Prüfung ergab: 4 Kopfhaut-Produkte teilen sich fachlich klar in 2 Gruppen (Ausspülen/Wöchentlich vs. Leave-in/Täglich). Die Slot-Namen sind kryptisch, die Trennung ist aber fachlich richtig. Tomi nutzt selbst beides parallel (Serum täglich + Peeling wöchentlich).

Entscheidung: **Trennung behalten**, nur REQ-06 Slot-Widerspruch korrigieren (Zelle-Edit). Slot-Umbenennung (kosmetisch) auf V2 verschoben, wenn Frontend die Slot-Namen sowieso menschenlesbar anzeigen muss.

### Phase 6 — Layer-1-Umsetzung (fehlgeschlagen)

Freigabe angenommen, Umsetzung in 7 Schritten:

1. ✓ Backup `sheets_20260709_113638_pre_layer1_refactor/` + Workflow-Backup `workflow_backup_20260709_114856_pre_layer1_engine.json`
2. ✓ Sheet-Schema erweitert: 3 neue Spalten (`ist_trockenshampoo`, `ist_zwei_in_eins`, `slot_override_erlaubt`)
3. ✓ Flag-Werte gesetzt: `the_champ.ist_trockenshampoo=TRUE`, `monat_black.ist_zwei_in_eins=TRUE`, `REQ-06.slot_typ=kopfhaut_taeglich`, `REQ-16b.slot_override_erlaubt=TRUE`
4. ✓ 26 REQ-Filter migriert (Batch-Update via gspread)
5. ✓ Engine-Patch via neues Skript `patch_layer1_engine.py`:
   - Node 11: `slot_override_erlaubt`-Feld in slot_assignments-Entry durchgereicht
   - Node 12: Patch #20 erweitert um `isSlotOverride`-Bedingung + Wirkungs-Match-Semantik
6. ✓ `sync_rules_to_workflow.py` + PUT + Verify ✓
7. **✗ Bulk `test_results_20260709_121528.json`: 8/14 success, 6/14 crashed (Node 19 Google-Sheets-Quota), aber bei den 8 grünen: 6/8 echte Empfehlungs-Drifts**

Konkrete Drifts (die 8 grünen Profile):
- **desi**: verliert curl_gelee + super_feuchtigkeitsmaske, bekommt rejuvabeads
- **eva**: verliert kopfhaut_peeling, bekommt monat_black (LOW-Profil!)
- **julia**: bekommt zusätzlich erweiterte_feuchtigkeit_spuelung
- **lena**: verliert curl_gelee + super_feuchtigkeitsmaske, bekommt bond_iq_leave_in + bond_iq_shampoo + curl_creme
- **maria**: verliert curl_creme + ir_clinical_kopfhautserum, bekommt curl_gelee + ir_clinical_shampoo
- **sina**: verliert super_feuchtigkeitsmaske, bekommt bond_iq_leave_in + bond_iq_shampoo

### Phase 7 — Root Cause Analyse

Node 12 Filter-Auswertung (Zeile 253-266 vor Refactor):
```js
return prod.produkt_key?.includes(fStr)
    || prod.produktlinie?.includes(fStr)
    || prod.hauptfunktion?.includes(fStr);
```

Das `.includes()` ist naiver JavaScript-String-Substring. Für den ursprünglichen Fall filter=`bond_iq` matched Substring in Produkt-Key/-Linie sinnvoll (weil `bond_iq` als Präfix in `bond_iq_shampoo` etc. steckt). Bei Wirkungs-Filtern mit CSV-Werten wie `hauptfunktion=reinigung,verdichtend` matched Substring `reinigung` ALLE Produkte, die irgendwo `reinigung` im CSV-String haben — inklusive `monat_black`, `essig_shampoo`, `kopfhaut_peeling`. Der Slot-Typ-Vorfilter fängt Cross-Slot-Falscheingaben ab, aber innerhalb desselben Slots verändert sich der Kandidaten-Pool → Ranking wählt anders → andere Empfehlung.

Beispiel eva (LOW-Profil, `routine_preference=ausgewogen`):
- Vorher: REQ-01 (Shampoo required_always, filter leer) hatte alle Shampoos im Pool, Ranking wählt smoothing_shampoo o.ä.
- Nach Refactor: irrelevant, weil REQ-01.filter leer
- ABER: irgendeine andere REQ-Regel matched jetzt monat_black als Shampoo-Kandidat und gewinnt via Ranking
- Detail-Analyse: braucht Trace pro Profil

Warum die Skizze das nicht vorhergesehen hat: die Skizze hat auf die vorhandene Boolean-Flag-Syntax vertraut („REQ-04 nutzt `ist_hitzeschutz=TRUE` produktiv seit langem"). Boolean-Flag ist präziser Regex-Match. Wirkungs-Substring ist nicht präzise. Dieser Unterschied wurde übersehen.

### Phase 8 — Rollback

Ausführung:
1. Workflow-PUT aus `workflow_backup_20260709_114902_pre_layer1_engine.json` (strip_readonly + settings-cleanup)
2. Sheet-map_slot_rules aus `backups/sheets_20260709_113638_pre_layer1_refactor/map_slot_rules.csv` (31 Regeln × 3 Zellen: filter + slot_typ + slot_override_erlaubt=FALSE)
3. Sheet-produktdatenbank: the_champ.ist_trockenshampoo=FALSE + monat_black.ist_zwei_in_eins=FALSE
4. `sync_rules_to_workflow.py` (neu-Sync ohne die alten SYNC-Marker-Reste)
5. Sanity-Bulk Sina (single profile) → 9/9 Produkte identisch zu Baseline

**Kein User-Impact**: der Refactor war während einer Test-Bulk-Phase auf dem MONAT-Workflow, echte Kundinnen laufen nur bei echten Fragebogen-Submissions. Zeitfenster war kurz genug, dass keine Live-Fragebogen-Empfehlung mit dem defekten Zustand rausging.

## Neustart-Plan für Layer-1 (nächste Session)

### Vorbedingung: Engine-Filter präzisieren

Node 12 Filter-Auswertung so umbauen, dass Wirkungs-Match **exakter Token-Match auf CSV-Zerlegung** ist, nicht Substring:

```js
// ALT (naiv):
return prod.produkt_key?.includes(fStr)
    || prod.produktlinie?.includes(fStr)
    || prod.hauptfunktion?.includes(fStr);

// NEU (Vorschlag):
const hfSet = new Set(csvList(prod.hauptfunktion));
const nfSet = new Set(csvList(prod.nebenfunktionen));
return prod.produkt_key === fStr
    || prod.produktlinie === fStr
    || hfSet.has(fStr)
    || nfSet.has(fStr);
```

**Beweis-Test vor Refactor**: Engine-Änderung alleine (ohne Sheet-Refactor) muss 0/14 Drift bringen, weil die aktuellen Filter (bond_iq als Produktlinie, curl_gelee als produkt_key) alle exakter Token-Match sind (nicht substring-abhängig).

**Wenn Beweis-Test grün**: erst DANN Cluster-weise Sheet-Refactor, mit Bulk zwischen jedem Cluster.

### Reihenfolge

1. **Engine-Präzisierung** (Zeile 253-266 Node 12) — Bulk-Beweis 0/14 Drift
2. **Cluster 1 Bond-IQ** (REQ-02, REQ-03, REQ-21, REQ-22) — 4 Regeln migrieren, Bulk
3. **Cluster 2 Scalp-Comfort** (REQ-05, REQ-20) — 2 Regeln, Bulk
4. **Cluster 3-14** einzeln, jeweils Bulk
5. **REQ-06 Slot-Fix** (kopfhaut → kopfhaut_taeglich) — separate Zellen-Edit
6. **REQ-16b Slot-Override** — Engine-Patch (c) auf präziser Basis
7. **the_champ + monat_black Bool-Flags** setzen
8. **Nicht-MONAT-Fixture** bauen + WL-Beweis-Test

Aufwand: eher 3-4 Stunden (nicht 2), wegen Cluster-für-Cluster-Vorgehen. Ohne diese Vorsicht: Wiederholung des Fehlschlags.

### Adapter-Erweiterung (WL) für Beweis-Test

`wl_adapter.py` muss die 2 neuen Bool-Flags kennen. Zwei Optionen:
- (a) Explizite Felder in `LibraryEntry`-Dataclass, Forward + Reverse
- (b) Aus Nutzen-Vokabular ableiten („trockenshampoo"/„zwei_in_eins" als neue Nutzen-Werte)

Empfehlung (a): explizite Bool-Felder, weil marken-neutral und semantisch klar.

## Neue Artefakte

- `refactor_req_wirkung_skizze.md` (Layer-1 Refactor-Skizze, Cluster-Auflistung, Klärungspunkte, Katalog-Anleitung) — bleibt gültig, muss um „Engine-Präzisierung als Vorbedingung" ergänzt werden
- `patch_layer1_engine.py` (Node 11+12 Patch-Skript) — bleibt liegen, muss für Neustart angepasst werden (Filter-Match-Semantik neu)
- Backups: `backups/sheets_20260709_113638_pre_layer1_refactor/`, `workflow_backup_20260709_114856_pre_layer1_engine.json`, `workflow_backup_20260709_114902_pre_layer1_engine.json`
- Bulk-Results: `test_results_20260709_091907.json` (nach Prio 1), `_100243.json` (nach Prio 2, aktuelle Baseline), `_121528.json` (Layer-1-Fehlschlag), `_131430.json` (Sina-Sanity-Test nach Rollback)
- Sheet-Schema-Erweiterungen (bleiben, mit FALSE-Defaults): `map_slot_rules.slot_override_erlaubt`, `produktdatenbank.ist_trockenshampoo`, `produktdatenbank.ist_zwei_in_eins`
- Backlog-Eintrag `SAAS_BACKLOG.md` Kap. 4 „REQ-Regel-Produkt-Key-Abstraktion — Whitelabel-Blocker"

## Konventionen hinzugekommen

- **Refactor-Vorbedingung „Engine-Präzisierung vor Regel-Migration"** — wenn ein Refactor eine bestehende Engine-Semantik neu belastet (z.B. Filter-Auswertung), muss die Engine-Semantik zuerst als eigenständige Änderung mit 0-Drift-Bulk verifiziert werden. Grund: heute wurde Sheet-Refactor + Engine-Patch in einem Rutsch deployed, Bug in Engine-Filter-Semantik wurde erst nachträglich sichtbar.
- **Cluster-für-Cluster-Deploy statt Big-Bang** — bei mehreren zusammenhängenden Regel-Änderungen (26 REQ) sollte pro Cluster deployed + verifiziert werden, nicht alle gleichzeitig. Rollback-Aufwand pro Cluster ist minimal, Root-Cause-Zuordnung bei Fehler trivial.
- **`.includes()` in n8n-JS ist Substring, nicht Token** — bei Wirkungs-Vergleich auf CSV-Feldern (hauptfunktion, nebenfunktionen) IMMER via `csvList()` in Set/Array zerlegen und dann `.has()`/`.includes()` — sonst matcht Teil-String unbeabsichtigt.
- **Skizzen-Iteration erlaubt** — die heutige Skizze hatte einen Denkfehler (Boolean-Präzision auf Wirkungs-Fall extrapoliert). Beim Neustart ist das ein Skizze-v2 mit Präzisions-Beweis, nicht ein Neu-Konzept. Skizze bleibt Referenz.

## Bewusst NICHT in dieser Session gemacht

- **Kopfhaut-Slot-Rename** `kopfhaut_taeglich` → `kopfhaut_leave_in` — kosmetisch aufgeschoben, hätte mehrere Nodes + Frontend berührt.
- **Layer 2/3** (map_conflict_rules, map_pool_filter) — blockiert bis Layer 1 stabil.
- **Route-Group** `src/app/(whitelabel)/` — bewusst nicht angefangen, weil Backend nicht marken-neutral.
- **HANDOVER.md-Update** — Session-Ergebnisse (3 intensitaet-Fixes) sind fachlich kleine Sheet-Edits, kein HANDOVER-relevanter Struktur-Wechsel. Der Layer-1-Fehlschlag ist Session-Historie, nicht HANDOVER-relevant.

## Bulk-Chronologie der Session

| Uhrzeit | File | Ergebnis | Zweck |
|---|---|---|---|
| 09:19 | `_091907.json` | 14/14, 0/14 Drift | Nach Prio 1 (rejuveniqe_oel + restore_leave_in) |
| 10:02 | `_100243.json` | 14/14, 0/14 Drift | Nach Prio 2 (curl_gelee) — **aktuelle Baseline** |
| 12:15 | `_121528.json` | 8/14 success + 6/14 Drifts | Layer-1-Fehlschlag (crashes = Sheets-Quota, Drifts = Substring-Match-Bug) |
| 13:14 | `_131430.json` | Single Sina, 9/9 identisch | Sanity nach Rollback |
