# Session 2026-07-09 (nacht) — Split-Score + Pflichtartikel

**Kern-Session:** aus einem gescheiterten PDF-strikten Fixture-Audit ist die eigentliche Ursache aufgedeckt worden — `pflegelevel_final` mischte zwei semantische Achsen. Node 06 wurde in Split-Score umgebaut, Node 08 filtert jetzt gegen echten Bedarf, Shampoo + Spülung sind jetzt Pflicht-Slots.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-09_split-score-pflichtartikel.md` und
> `chat-archive/2026-07-08_wl-klon-adapter.md`. Der Kern-Bug im MONAT-
> Empfehlungssystem ist gefixt: Score-Split trennt Zustand (Haarschäden)
> von Investment (Pflege-Wunsch), Filter matcht gegen `pflegelevel_zustand_final`.
> Desi bekommt jetzt Renew statt Bond IQ, Anna hat MONAT Black (2-in-1).
>
> Live-Stand ist stabil, MONAT-Bulk 14/14 grün. Backup-Punkt:
> `backups/sheets_20260708_235530_pre_score_split/`.
>
> Offen für nächste Session (Priorität):
>
> 1. **PDF-Audit der 12 unangetasteten Sheet-Zeilen.** Wir haben nur 17
>    von 37 Produkten überhaupt geprüft (7 davon geändert, 12 als
>    PDF-strikt bestätigt). 20 Zeilen sind noch nie systematisch gegen
>    PDF geprüft worden. Agent-Delegation empfohlen.
> 2. **Fantasie-Demo-Bibliothek** (SAAS_BACKLOG 2.6 Falle 1). Noch offen
>    seit 2026-07-08.
> 3. **Whitelabel-Frontend** — Route-Group `src/app/(whitelabel)/`.

## Stand am Ende der Session

- **Score-Split live** — Node 06 gibt neben `pflegelevel_final` (Backward-
  Compat, Summe wie bisher) auch `pflegelevel_zustand_final` und
  `pflegelevel_investment_score` aus.
- **Filter präziser** — Node 08 + Node 12 nutzen `pflegelevel_zustand_final`
  für Match, mit Fallback auf `pflegelevel_final` falls Split nicht deployed.
- **Pflicht-Slots** — Shampoo + Spülung überspringen den pflegelevel-Filter
  in Node 08. Ranking in Node 12 wählt weiterhin das best-passende.
- **Sheet um Spalte `ziel_score`** — 24 Regeln in `map_pflegelevel_scoring`
  klassifiziert als `zustand` (11 Regeln, max 23 Pkte) oder `investment`
  (13 Regeln, max 14 Pkte).
- **Regressions-Bulk 14/14 grün** (13 Original + Desi neu):
  - `test_results_20260709_012817.json`
  - Desi: HIGH (final) / MID (zustand) / 9 (invest) — bekommt Renew Shampoo+Spülung, volle Curl-Linie, 8 Produkte total
  - sarah: HIGH/HIGH/8 — echter Schaden, HIGH bleibt
  - anna: LOW/LOW/0 — MONAT Black 2-in-1 (REQ-30)
  - lena/silvia/sina/tina: HIGH final, MID/HIGH zustand — bekommen jetzt Renew statt Bond IQ (fachlich sauberer)

## Was in dieser Session passiert ist

### Phase 1 — PDF-strikter Fixture-Audit (Runde 1+2)

Aus feedback_audit_pdf_strict.md abgeleitet: 6 Grenzfälle geprüft, in denen
`pflegelevel` in der Fixture nicht deterministisch aus `intensitaet + haarzustand`
via `_pflegelevel`-Regel ableitbar war. 4 der 6 wurden als Bauchgefühl-Fehler
korrigiert (Renew Shampoo/Spülung HIGH gestrichen, Föhncreme/Anti-Frizz-Spray
LOW ergänzt). Agent-Delegation für 17 weitere Abweichungen: 3 zusätzliche
Fehler gefunden (bond_iq_leave_in intensiv, curl_creme + entwirrungsspray LOW).

Sheet + MONAT-Workflow (physisch angetastet!) + Fixture + WL-Klon synchronisiert.
Regressions-Bulk 13/13 grün, 4 erwartete Empfehlungs-Änderungen dokumentiert.

### Phase 2 — Desis Live-Test bricht das Modell

Desi hat den Fragebogen persönlich durchgeklickt. Ergebnis: Shampoo + Spülung
fehlten komplett. Der User beobachtete das direkt in der Live-App.

Ursachen-Analyse (Execution 921):
- Desi hat `hair_treatments=nein`, `hair_condition=[trocken,frizz,kraftlos]`
  — kein einziger HIGH-Marker (kein Spliss, Haarbruch, blondiert, stark_geschaedigt)
- Aber `pflegelevel_final=HIGH` (raw=13) — falsch berechnet
- Score-Zerlegung: 4 Punkte aus Haarzustand + 9 Punkte aus Struktur/Styling/
  Zeit/Ziele → 13 total
- Der Filter Node 08 sucht Produkte mit `HIGH` in ihrer pflegelevel-Spalte
- Bond IQ Shampoo (MID,HIGH) fällt durch POOL-01 raus (`needs_repair_focus=false`)
- Renew Shampoo (nach Runde 1: LOW,MID) fällt raus, weil kein HIGH-Match
- Übrig: nur `smoothing_shampoo` → im Ranking zu wenig Score → Slot leer

### Phase 3 — Rollback

Full Rollback auf 17:04-Stand:
1. Sheet aus `backups/sheets_20260708_170412_pre_pflegelevel_pdf_audit/` restored
2. MONAT-Workflow via `sync_rules_to_workflow.py` neu synchronisiert
3. Fixture manuell zurück auf pre-audit-Werte
4. WL-Klon via `sync_wl_produktdatenbank.py --source` synchronisiert

### Phase 4 — Erkenntnis: pflegelevel ist konzeptuell falsch

Deep-Analyse ergab: `pflegelevel_final` aggregiert zwei völlig unabhängige
Dimensionen:
1. **Wie kaputt ist das Haar?** (haarzustand + belastung)
2. **Wie viel Pflege will die Kundin?** (struktur + styling + zeit + ziele)

Produkt-`pflegelevel` in der Datenbank bedeutet aber nur Dim. 1 — welche
Schadensgrade decke ich ab. Desi landet in Dim. 2 (Investment-HIGH), das
System sucht Produkte für Dim. 1 (Schaden-HIGH) → Bond IQ als Repair-Kur
für gesundes Haar wird empfohlen.

Sinas alte HIGH-Setzung bei Renew war ein Workaround für diesen Bug, kein
Bauchgefühl-Fehler — sie hat Renew HIGH gegeben, damit Kundinnen wie Desi
überhaupt ein Shampoo bekommen.

### Phase 5 — Score-Split (Weg B)

Impact-Analyse zuerst: 7 REQ-Regeln nutzen `pflegelevel_numeric`, keine
Conflict/Priority-Regel, 6/14 Profile kippen (fachlich alle richtiger).

Bau:
1. Sheet-Spalte `ziel_score` in `map_pflegelevel_scoring` — 11 zustand,
   13 investment
2. Node 06 Refactor: pts weiter Backward-Compat, zusätzlich zustandPts +
   investmentPts. Overrides (blondiert/stark_geschaedigt) wirken auf beide
   Levels parallel. Output erweitert um `pflegelevel_zustand_*` und
   `pflegelevel_investment_score`.
3. Node 08 Filter: `matchLevel = pl.pflegelevel_zustand_final || pl.pflegelevel_final`
4. Node 12 Scoring: analog

Regressions-Bulk 14/14 grün. Desi bekommt Renew + volle Curl-Linie.

### Phase 6 — Pflicht-Slots (Task #13)

Analyse zeigte: Anna (LOW-Profil, fettige Kopfhaut) hatte keine Spülung.
Aber: REQ-30 ist eine bewusste fachliche Regel — MONAT Black als 2-in-1
ersetzt Shampoo + Spülung bei minimaler Routine. Kein Bug.

Trotzdem eingebaut als Absicherung für zukünftige Profile: Filter Node 08
überspringt pflegelevel-Check für `slot_typ in ['shampoo', 'spuelung']`.
Ranking in Node 12 wählt weiterhin das best-passende.

## Neue Artefakte

- `map_pflegelevel_scoring` — Sheet-Spalte `ziel_score` (11 zustand + 13 investment)
- Node 06 jsCode — Split-Score-Refactor, 21050 Bytes (vorher 18494)
- Node 08 jsCode — `pflegelevel_zustand_final` + Pflicht-Slot-Ausnahme
- Node 12 jsCode — `pflegelevel_zustand_final` im plMatch
- `test_suite.py` — Desi als 14. Testprofil ergänzt
- 4 Regressions-Result-JSONs: `_004248` (nach Split), `_012817` (nach Pflicht),
  plus 2 Zwischenstände nach Sheet-Runden
- Backups: `backups/sheets_20260708_170412_pre_pflegelevel_pdf_audit/`,
  `_204039_pre_pdf_audit_round2/`, `_235530_pre_score_split/`

## Konventionen hinzugekommen

- **Split-Score-Prinzip** — `pflegelevel_final` bleibt Backward-Compat-Summe;
  neue Felder `pflegelevel_zustand_final` (echter Bedarf, Filter/Match) und
  `pflegelevel_investment_score` (Wunsch, max_products/Textbausteine).
  Grund: Match-Semantik konsistent zur Produkt-Datenspalte machen.

- **Pflichtslot-Ausnahme im Filter** — für Shampoo + Spülung fällt der
  `pflegelevel`-Filter in Node 08 weg. Ranking (Node 12) entscheidet.
  Grund: Sinas Prinzip "Shampoo + Spülung sind immer Teil der Empfehlung"
  darf nicht durch strikten Level-Filter gebrochen werden.

- **Testprofile müssen echte Beraterinnen-Profile abbilden** — Desi als
  14. Profil, weil der 13-Profil-Bulk ihr Problem nicht gefangen hätte.
  Grund: Regressions-Bulk muss reale Anforderer abdecken, nicht nur
  synthetische Profile.

- **PDF-Strikt ist gültig für strukturelle Felder, nicht für aggregierte
  Semantik-Felder wie pflegelevel** — feedback_audit_pdf_strict.md bleibt
  gültig für Slot, Nutzen, Passung, Ausschluss. `pflegelevel` ist ein
  System-Konstrukt (LOW/MID/HIGH sind kein PDF-Vokabular) — es kann nicht
  strikt aus PDFs abgeleitet werden.

## Bewusst NICHT in dieser Session gemacht

- **12 unangetastete Sheet-Zeilen** — Fixture-Audit ist nur für 17 der 37
  Produkte gelaufen. 20 sind ungeprüft. Nicht dringlich, weil der Score-Split
  das eigentliche Problem gelöst hat.
- **Fantasie-Demo-Bibliothek** — SAAS_BACKLOG 2.6 Falle 1, seit 2026-07-08 offen.
- **Whitelabel-Frontend Route-Group** — SAAS_BACKLOG 3 V1 Punkt 3 ff.
- **HANDOVER.md-Update** — bleibt MONAT-fokussiert. Wenn Score-Split-Konventionen
  in echte Kundinnen-Nutzung gehen, muss HANDOVER die neuen Felder dokumentieren.

## Folgepunkte für nächste Session

### Priorität 1: PDF-Audit der 12 unangetasteten Sheet-Zeilen

Wir haben von 37 Produkten nur 17 überhaupt gegen PDF geprüft (6 Grenzfälle
+ 17 Agent-analysiert, davon 12 als PDF-strikt bestätigt). 20 Produkte sind
komplett unauditiert. Nicht kritisch — der Score-Split hat das Match-Problem
gelöst — aber saubere Basis für weitere Beraterinnen wichtig.

Agent-Delegation für die 20, dann Sheet-Update für Bauchgefühl-Fehler, dann
Regressions-Bulk.

### Priorität 2: MONAT-Workflow ist jetzt nicht mehr "physisch unangetastet"

Bisher galt: MONAT-Workflow-Objekt wird nicht angefasst, damit die 0/36-Baseline
strukturell abgesichert bleibt (Session 2026-07-08). Heute haben wir Node 06,
08, 12 direkt refactored. Neue Konvention: MONAT-Workflow ist jetzt aktives
Bau-Objekt bis WL-Klon Live-Reife hat. HANDOVER.md sollte das reflektieren.

### Priorität 3: Rest wie in vorheriger Session-Doku

Siehe `2026-07-08_wl-klon-adapter.md` — Fantasie-Bibliothek, WL-Frontend.
