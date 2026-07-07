# Session 2026-07-07 — Whitelabel-Adapter + Isomorphie-Test

**Bau-Track-Session** (nach `2026-07-07_konzept-ausbau.md` am selben Tag).
Erste konkrete Bau-Arbeit für den Whitelabel-Umbau: Datenmodell-Adapter zwischen
Beraterin-UI (Chip-Formular) und produktdatenbank (25 Spalten, Node-07-Output).

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-07_wl-adapter-isomorphie.md` und `SAAS_BACKLOG.md`
> Kapitel 3 (Punkt 6 aktualisiert). Der WL-Adapter (`wl_adapter.py`) ist fertig
> und über alle 37 MONAT-Produkte isomorph belegt (5/162 harte Δ, alle
> strukturell im Sub-Slot-Design). Nächster Bau-Schritt: n8n-Workflow-Duplikat
> `myglowmatch_wl` per API aufsetzen (N8N_API_KEY in `.env`), MONAT-Datensatz
> via Adapter reinschreiben, 13 Test-Profile durch den Klon laufen → muss
> 0/36 Slot-Drift zeigen (Regressions-Beweis). Vorher offene Design-Frage
> klären: Sub-Slots (kopfhaut_taeglich, styling_2, styling_3, nacht_serum) im
> UI zusammenfassen (7 Slots) oder ausrollen (11 Slots)? Und der Mockup
> `demo/bibliothek.html` muss auf 27 Chips + 12. Feld Pflegelevel gebracht
> werden — Design-Arbeit für eine eigene Session.

## Stand am Ende der Session

- **wl_adapter.py** — 12-Felder-Datenklasse `LibraryEntry`, Forward-Funktion
  `to_produktdatenbank_row` und Reverse-Funktion `from_produktdatenbank_row`.
  Deterministisch, alle 25 DB-Spalten produziert, Format-Kompatibilität zu
  Node-07-Output verifiziert (TRUE/FALSE-Strings, Komma-CSV, "alle"/"-"
  Sonderwerte).
- **wl_isomorphie_test.py** — Werkstatt-Test, liest alle 37 MONAT-Produkte
  aus einem beliebigen `test_results_*.json`, misst Δ pro Spalte, schreibt
  `isomorphie_report.md`. Rein lokal, keine Sheet-Writes, keine n8n-Aufrufe.
- **isomorphie_report.md** — Endstand nach Kalibrierung: **5/162 harte Δ**,
  alle strukturell durch die UI-Konsolidierung der 4 Sub-Slots erklärt.

## Was in dieser Session passiert ist

### Phase 1 — HANDOVER-Explore und Bau-Entscheidungen

Der Explore-Agent hat aus HANDOVER.md die relevanten Fakten für den WL-Umbau
extrahiert. **Kern-Erkenntnis:** seit Migration #27 (2026-07-03) ist die
Regel-Engine (Nodes 04–15) bereits abstrakt gegen Produktnamen — die Regeln
lesen strukturierte Attribute (kopfhaut, haarstruktur, hauptfunktion, …),
keine hardcodierten MONAT-Referenzen. Die Produktdatenbank selbst wird
allerdings weiterhin live aus einem Google-Sheet geladen (Node 07,
`n8n-nodes-base.googleSheets`, Sheet `MONAT_Produktdatenbank_KOMPLETT`).

Damit verschiebt sich der Umbau grundlegend:

- **Frage (a) Parallelbetrieb:** weder Node-Fork noch Feature-Flag, sondern
  ein **separater n8n-Workflow** `myglowmatch_wl` als Duplikat. Der laufende
  MONAT-Test bleibt komplett unberührt, WL kann frei umgebaut werden.
- **Frage (b) Chip-Vokabular auf 25-Spalten-Tiefe:** kein UI-Umbau nötig,
  wenn der Adapter die 11 UI-Felder deterministisch in 25 DB-Spalten
  übersetzt (System-Felder werden abgeleitet oder default gesetzt).
- **Frage (c) Regel-Engine-Umbau:** **entfällt komplett.** Der Umbau
  reduziert sich auf einen Daten-Adapter zwischen der Beraterin-Bibliothek
  und dem 25-Spalten-Format, das Node 07 heute an Nodes 08+ liefert.

### Phase 2 — Reihenfolge festgelegt

Auf Thomas' Frage „was ist die sinnvollste Reihenfolge" empfohlen und
bestätigt:

1. Adapter formal definieren (Forward + Reverse)
2. **Isomorphie-Test** gegen die MONAT-produktdatenbank — beweist, dass die
   UI-Felder-Zahl genug Info trägt, um Desirées Sortiment 1:1 abzubilden
3. n8n-Workflow-Duplikat aufsetzen
4. **Regressions-Beweis** mit MONAT-Daten durch den WL-Klon: 13 Profile
   müssen 0/36 Slot-Drift zeigen
5. Sync-Skript `sync_rules_to_workflow.py` um `--workflow`/`--dataset`
   parametrisieren
6. Erst dann WL-eigene Bibliotheken (siehe Konvention unten)

### Phase 3 — Compliance-Klarstellung

Thomas hat berechtigt nachgefragt, ob durch den Test MONAT-Daten ins
WL-System wandern. Klargestellt: der Isomorphie-Test läuft rein lokal auf
dem Mac, liest MONAT-Daten einmal in ein Python-Objekt, misst Δ, wirft die
Daten weg. Nichts landet in Google Sheets oder n8n. Die WL-Produktdatenbank
startet später leer (Kapitel 2.6 Falle 1) und wird von der Beraterin selbst
gefüllt — Desirée darf ihre MONAT-Produkte als Markenpartnerin dort
eintragen (aktive Handlung, ihre Content-Verantwortung), VERADEX liefert
nichts vorbefüllt.

### Phase 4 — Adapter geschrieben, Iso-Test aufgesetzt

`wl_adapter.py` gebaut mit initialen 11 UI-Feldern nach `demo/bibliothek.html`
und Ableitungsregeln für die 25 DB-Spalten. Round-Trip auf dem Mockup-
Beispiel (Renew Shampoo) direkt bit-identisch, aber der erste Test mit einer
realen MONAT-Zeile (Entwirrungs-Spray) zeigte fünf Δ-Muster: Slugify-
Konvention, Vokabular-Lücken bei `nebenfunktionen`, pflegelevel-Ableitung
zu eng, produktlinie-Verlust (bewusst), kombi_optional-Verlust (bewusst).

### Phase 5 — Iterative Kalibrierung 162 → 32 → 5

**Iteration 1 (roh):** 162 harte Δ über 37 Produkte, aufgeschlüsselt nach
Spalte in `isomorphie_report.md`.

**Iteration 2 (Vokabular + System-Felder + Bool-Fix):** 32 harte Δ. Fixes:

- UI_HAUPTNUTZEN von 11 auf 27 Tokens erweitert (`verdichtend, staerkend,
  kaemmbarkeit, definition, elastizitaet, entgiftung, farbschutz, frische,
  haarwuchs, kraeftigend, reinigung, textur, versiegelung, wash_alternative,
  auffrischung, ausgleichend` ergänzt; Umstellung auf 1:1 UI-Slug = DB-Token
  vermeidet Bidir-Mapping-Fehler)
- UI_KOPFHAUT um `trocken`, UI_INTENSITAET um `alle`, UI_AUSSCHLUSS auf
  Union aller Struktur/Kopfhaut/Zustand-Tokens erweitert
- LibraryEntry um 3 System-Felder erweitert: `produkt_key`, `routine_schritt`,
  `produkttyp` — werden aus der DB-Zeile durchgereicht statt neu abgeleitet
- Bool-Flags (`ist_hitzeschutz`, `ist_bonding`, `ist_scalp_focus`) nur noch
  aus Haupt-Nutzen abgeleitet, nicht aus Sekundär (essig_shampoo hat
  kopfhautpflege sekundär, ist aber kein scalp_focus)

**Iteration 3 (pflegelevel als 12. UI-Feld + haarzustand='-'):** 5 harte Δ.

- Isomorphie-Test zeigte: pflegelevel ist real ein eigenständiges Kuratier-
  Feld, nicht aus haarzustand+intensitaet ableitbar (`fohncreme` hat
  `intensitaet=alle` und `pflegelevel=MID,HIGH` — keine deterministische
  Ableitung möglich). Konsequenz: LibraryEntry bekommt 12. Feld
  `pflegelevel: list[str]` als Chip-Multi (LOW/MID/HIGH). Adapter reicht
  durch wenn gesetzt, fällt sonst auf abwärtskompatible Ableitung zurück
- Reverse: `intensitaet='alle'` bleibt `'alle'` (UI kennt es inzwischen),
  `haarzustand='-'` wird als leere Liste behandelt

**Endstand:** 5 verbleibende harte Δ, alle in `slot_typ`. Betroffen sind die
5 Produkte in den Sub-Slots `kopfhaut_taeglich`, `styling_2`, `styling_3`,
`nacht_serum` (`ir_clinical_kopfhautserum`, `scalp_comfort_serum`,
`curl_auffrischer`, `curl_gelee`, `bond_iq_night_day_serum`). Kein Adapter-
Bug, sondern die bewusste UI-Konsolidierung im Mockup (7 Slot-Chips statt
11). Design-Entscheidung offen.

## Neue Artefakte

- `wl_adapter.py` (~330 Zeilen) — 12-Felder-LibraryEntry, Forward, Reverse,
  Vokabular-Konstanten, pflegelevel-Fallback-Ableitung, Self-Test
- `wl_isomorphie_test.py` (~140 Zeilen) — Werkstatt-Test, liest
  test_results-JSON, aggregiert Δ pro Spalte, schreibt Report
- `isomorphie_report.md` — Endstand der Kalibrierung (5 harte Δ + 2
  Design-Verluste kombinationen/kombi_optional)

## Bewusst NICHT in dieser Session gemacht

- **n8n-Workflow-Duplikat.** Kommt in nächster Session, braucht frischen
  Kopf und die Sub-Slot-Design-Entscheidung.
- **Mockup-Update (`demo/bibliothek.html`).** 11 → 27 Chips + 12. Feld
  Pflegelevel + intensitaet=alle + kopfhaut=trocken ist Design-Arbeit,
  gehört in eine eigene Session (nicht mit Sina/Marcel diskutieren, bevor
  der Mockup nachgezogen wurde).
- **HANDOVER.md-Update.** Der WL-Adapter existiert nur lokal, ist noch
  nicht im n8n-Workflow. Bis Schritt 3 gebaut ist, bleibt der SaaS-Track
  im Session-Archiv + SAAS_BACKLOG.
- **auto-Memory-Eintrag für myglowmatch.** CLAUDE.md des Projekts sagt
  explizit „HANDOVER.md gibt die Faktografie" — Projekt-Kontext lebt lokal,
  nicht im globalen Memory.

## Folgepunkte für nächste Session

### Priorität 1: Sub-Slot-Design-Entscheidung

Verschmelzen (7 UI-Slots, einfacher, 5 Zeilen mit Slot-Drift-Risiko) oder
ausrollen (11 UI-Slots, verlustfrei aber mehr Chips)? Prüfen mit dem
Regressions-Test in Schritt 4 — wenn 7 Slots keine Empfehlungs-Drift
verursachen, ist die einfachere Variante gerechtfertigt.

### Priorität 2: Mockup-Update

`demo/bibliothek.html` auf den echten Vokabular-Stand bringen. Chip-Gruppen
für die 27 Haupt-Nutzen-Tokens überlegen (evtl. „Pflege-Nutzen /
Reinigung / Styling / Special" als Sektionen, damit 27 Chips optisch
tragbar bleiben). Erst dann Sina/Marcel wieder aufgesetzt zeigen.

### Priorität 3: n8n-Workflow-Duplikat + Regressions-Beweis

- `myglowmatch_wl` per n8n-API klonen (N8N_API_KEY aus .env)
- Neuer Webhook-Path
- MONAT-Datensatz via Adapter → WL-Workflow embedden (oder aus Sheet
  laden — Design-Entscheidung: bleibt Node 07 googleSheets oder wird
  embedded?)
- 13 Test-Profile durch den Klon jagen, muss 0/36 Slot-Drift zeigen

### Priorität 4: Sync-Skript parametrisieren

`sync_rules_to_workflow.py` um `--workflow` und `--dataset`-Parameter
erweitern.

### Priorität 5: Zwei WL-Bibliotheken

- **Desirée-real:** Desirées MONAT-Vollsortiment über das Chip-UI
  eingetragen — harter Regressions-Test „liefert das System noch die
  richtigen Empfehlungen wie heute?"
- **Fantasie-Demo:** komplett erfundene Nicht-Marken-Produkte, für
  Werbung, Reels, öffentliche Demo — deckt Compliance-Kapitel 2.6 sauber
  ab (keine echten Markennamen in öffentlichen Kontexten)

## Konvention hinzugekommen

- **Chip-Vokabular = DB-Token.** UI-Slugs und DB-Tokens 1:1 identisch
  (Ausnahme: freundliche Anzeige-Labels im Mockup). Vermeidet
  Bidir-Mapping-Fehler und macht Adapter-Erweiterung trivial.
- **pflegelevel ist Kuratier-Feld, keine Ableitung.** Isomorphie-Test hat
  bewiesen: die Beraterin muss den Pflegelevel-Bedarfsbereich pro Produkt
  aktiv setzen (Chip-Multi LOW/MID/HIGH). Die algorithmische Ableitung aus
  haarzustand + intensitaet trifft nicht die realen Zuweisungen und darf
  nur als Fallback dienen.
- **Isomorphie-Test als Standard-Nachweis vor Datenmodell-Änderungen.**
  Wenn wir künftig Attribute in der Bibliothek ändern (neue Chips, neue
  Ableitungen, Feld-Umstellungen), läuft `wl_isomorphie_test.py` als
  Regressionsnetz gegen die 37 MONAT-Zeilen als Referenz-Datenmodell.
