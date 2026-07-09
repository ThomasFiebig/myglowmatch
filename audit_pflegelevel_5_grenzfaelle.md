# Audit: 5 Grenzfälle Pflege-Intensität / Pflegelevel

**Stichtag:** 2026-07-08
**Anlass:** Wenn wir die Pflege-Intensität in der neuen Beraterinnen-UI **automatisch** aus dem Produktdatenblatt ableiten wollen, muss die aktuelle Sheet-Ausprägung PDF-strikt sein. Bei 5 von 37 Produkten weichen die aktuellen Werte von der reinen PDF-Ableitung ab. Bitte pro Fall entscheiden.

**Doktrin (aus früherer Migration):** Was nicht im PDF steht, kommt nicht ins Sheet. Erfahrungswissen der Beraterin darf ergänzen, muss aber explizit begründet werden.

**Wenn du dem Vorschlag zustimmst → einfach „OK" ankreuzen. Wenn du widersprichst → Grund kurz notieren, dann bleibt der aktuelle Wert.**

---

## Fall 1 — Erweitertes Feuchtigkeitsshampoo

**PDF-Header:** „Trockenheit / Feines bis mittleres Haar / Alle Haartypen / Vorbereitung"
**PDF-Warum:** „reinigt sanft, spendet Feuchtigkeit"
**PDF-Anwendung:** Standard-Shampoo-Anwendung, kein Kur-Charakter

**Aktueller Sheet-Wert:** intensitaet = `leicht`, pflegelevel = `LOW, MID`
**PDF-strikt:** Header sagt „Alle Haartypen" (spricht für `alle`), gleichzeitig spezifische Zielgruppe „Trockenheit + feines/mittleres Haar" (spricht für `leicht`). **Ambivalent.**

**Deine Entscheidung:**
- [ ] OK — bleibt `leicht` (Zielgruppe „Trockenheit" schlägt „Alle Haartypen")
- [ ] Ändern auf `alle` (Header-Signal ist stärker)
- [ ] Anderer Wert: _______________

---

## Fall 2 — Renew™ Hydrating Shampoo

**PDF-Header:** „Trockenes Haar / Alle Haartypen / Mittlere bis dicke Haarstruktur / Vorbereitung"
**PDF-Warum:** „sanftes Reinigungsmittel", „Ultra-Hydratisierung für trockenes Haar"
**PDF-Anwendung:** Standard, keine Wochen-Anwendung, kein Kur-Charakter

**Aktueller Sheet-Wert:** intensitaet = `intensiv`, pflegelevel = `LOW, MID, HIGH`
**PDF-strikt:** „Trocken" ist MID-Marker. PDF nennt weder „stark geschädigt" noch „blondiert" noch „Spliss" noch „Haarbruch" (das wären HIGH-Marker). PDF sagt explizit „sanft".

**Vorschlag:** intensitaet = `mittel`, pflegelevel = `LOW, MID` (HIGH streichen)

**Deine Entscheidung:**
- [ ] OK — auf `mittel` / `LOW, MID` ändern
- [ ] Nein, Renew wirkt in der Praxis intensiver als das PDF verspricht — Grund: _______________
- [ ] Anderer Wert: _______________

---

## Fall 3 — Renew™ Spülung

**PDF-Header:** „Trockenes Haar / Alle Haartypen / Mittlere bis dicke Haartexturen / Vorbereitung"
**PDF-Vorteile-Liste:** enthält wörtlich **„Ideal für den täglichen Gebrauch"**
**PDF-Warum:** „hilft essentielle Feuchtigkeit wiederherzustellen"

**Aktueller Sheet-Wert:** intensitaet = `intensiv`, pflegelevel = `LOW, MID, HIGH`
**PDF-strikt:** „Täglicher Gebrauch" schließt `intensiv` explizit aus. Zielgruppe „Trocken" = MID-Marker. Kein HIGH-Marker im PDF.

**Vorschlag:** intensitaet = `mittel`, pflegelevel = `LOW, MID` (HIGH streichen)

**Deine Entscheidung:**
- [ ] OK — auf `mittel` / `LOW, MID` ändern
- [ ] Nein, ich setze bewusst HIGH weil — Grund: _______________
- [ ] Anderer Wert: _______________

---

## Fall 4 — MONAT STUDIO ONE™ Föhncreme

**PDF-Header:** „Frizz / Hitzeschutz / **Alle Haartypen und -texturen** / Styling"
**PDF-Warum:** „luxuriöse Styling-Creme", „Sicher für coloriertes Haar"
**PDF-Anwendung:** Auf handtuchtrockenes Haar, föhne wie gewohnt (tägliche Styling-Anwendung)

**Aktueller Sheet-Wert:** intensitaet = `alle`, pflegelevel = `MID, HIGH`
**PDF-strikt:** Header sagt explizit „Alle Haartypen und -texturen" → LOW muss dabei sein. Kein Ausschluss für normales Haar.

**Vorschlag:** intensitaet bleibt `alle`, pflegelevel = `LOW, MID, HIGH` (LOW ergänzen)

**Deine Entscheidung:**
- [ ] OK — LOW ergänzen
- [ ] Nein, Föhncreme braucht niemand mit gesundem Haar — Grund: _______________

---

## Fall 5 — Smoothing Anti-Frizz™ Föhn-Spray

**PDF-Header:** „Frizz / **Alle Haartypen / Alle Haarstrukturen** / Vorbereitung"
**PDF-Ideal für alle:** „Ein **leichtes**, frizzreduzierendes Stylingprodukt"
**PDF-Ergebnisse:** „91 % weniger Spliss" (Spliss = HIGH-Marker)

**Aktueller Sheet-Wert:** intensitaet = `leicht`, pflegelevel = `MID, HIGH`
**PDF-strikt:** „Alle Haartypen und -strukturen" → LOW muss dabei sein. Spliss-Wirksamkeit rechtfertigt HIGH. intensitaet=`leicht` ist wörtlich im PDF benannt.

**Vorschlag:** intensitaet bleibt `leicht`, pflegelevel = `LOW, MID, HIGH` (LOW ergänzen)

**Deine Entscheidung:**
- [ ] OK — LOW ergänzen
- [ ] Nein, Anti-Frizz-Spray gehört nicht in Beratung für normales Haar — Grund: _______________

---

## Zusammenfassung — was passiert nach eurer Freigabe

Für alle Fälle mit „OK":
1. Backup vom `produktdatenbank`-Sheet in `backups/` ziehen
2. 4–5 Zeilen im MONAT-Google-Sheet aktualisieren (via `sheets_writer.py`)
3. `wl_libraries/sina_monat.json` aus dem korrigierten Klon neu dumpen
4. Regressions-Bulk fahren gegen frische MONAT-Baseline (Erwartung: definierte Δ, dokumentiert)
5. Adapter-Auto-Ableitung im UI aktivieren (kein Beraterinnen-Feld für Intensität mehr)

Für Fälle mit Widerspruch:
- Wert bleibt wie er ist
- Adapter braucht dann einen **Beraterinnen-Override** im UI für diesen Slot × Nutzen-Kombi
- Grund wird in `HANDOVER.md` oder Session-Archiv dokumentiert

---

**Freigabe Desiree:** ________________  **Datum:** ____________
