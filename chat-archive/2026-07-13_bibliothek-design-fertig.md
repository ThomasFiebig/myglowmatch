# Session 2026-07-13 — Bibliothek-UI konzeptionell fertig, ready für Dashboard-Portierung

**Kern-Session:** Das Bibliothek-Design-Gerüst („Neues Produkt hinzufügen") wurde finalisiert. Coverage-Audit gegen die 33 `produktdatenbank`-Spalten durchgeführt, Ableitungs-Regeln für alle System-Felder festgezurrt, Info-Toggles + Conditional Fields eingebaut, Konzept-Version und Live-Preview sauber getrennt. Bereit zur React-Portierung ins Dashboard.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-13_bibliothek-design-fertig.md`.
> **Bibliothek-Design ist konzeptionell fertig** und in
> [[project-bibliothek-design-locked]] + HANDOVER-Abschnitt „Bibliothek-UI"
> festgehalten. **Nicht neu diskutieren.** Zwei Dateien:
> `demo/bibliothek.html` (Konzept, live unter `/konzept/bibliothek.html`)
> und `demo/bibliothek-live.html` (Design-Referenz für React-Component).
> 9 Felder final, alle Ableitungs-Regeln zu `produktdatenbank`-Spalten
> dokumentiert. Nächste sinnvolle Schritte:
> (a) React-Portierung ins Dashboard,
> (b) CSS-Aufräumen in `bibliothek-live.html`,
> (c) Layer-2-Runde 2 (PFL-OV-01…04) — bereits geklärt: markenneutral,
> kein Umbau nötig (siehe [[project-bibliothek-design-locked]]).

## Was in dieser Session passiert ist

### Ausgangspunkt

Session startete mit Frage „womit anfangen nach Layer-2-Runde 1?". Analyse-Empfehlung: PFL-OV-01…04 prüfen (Node 06). Ergebnis der Analyse in wenigen Minuten: **PFL-OV-Regeln sind bereits markenneutral** — sie enthalten nur Fragebogen-Werte (`blondiert`, `stark_geschaedigt`, `minimal`), kein Marken-Vokabular. Node-06-Engine ist ebenfalls markenneutral. Layer-2-Analyse damit komplett — nur noch Bibliothek-UX und Task #6 im Backlog.

**Entscheidung Bibliothek-UX-Update zuerst** — reine Frontend-Arbeit, kein Sheet-Edit, kein Deploy-Risiko.

### Erste Runde: `ist_bonding_line`-Feld

Erste Ergänzung des Feldes „Bonding-/Repair-Linie" als Ja/Nein-Radio-Chip in `demo/bibliothek.html`. Legenden-Zeile bei Nutzen-Tabelle ergänzt zur automatischen Solo-Hitzeschutz-Ableitung („System erkennt Solo-Hitzeschutz aus einziger Haupt-Nutzen-Markierung, kein zusätzlicher Klick nötig").

### Datei-Governance-Klärung: `demo/` vs. `public/konzept/`

Bemerkt: `public/konzept/bibliothek.html` war eine ältere Struktur (7. Juli), nicht identisch mit `demo/bibliothek.html`. Nach User-Klärung: die `public/`-Version ist die Sina bereits gezeigte Original-Struktur, die `demo/`-Version ist die neue Listen-Version (übersichtlicher, für Beraterinnen einfacher zu pflegen).

**Umsetzung**: alte `public/`-Version umbenannt zu `bibliothek-v1-original.html` mit sichtbarem Deprecation-Banner + HTML-Kommentar im Head (Verweis auf aktuelle URL). Neue `demo/`-Version nach `public/konzept/bibliothek.html` kopiert, damit die zwei internen Buttons (Konzept-Übersicht + Partner-Portal-Mockup) auf den aktuellen Stand zeigen.

### Coverage-Audit: was fehlt der Bibliothek an Backend-Feldern?

Systematischer Vergleich der 33 `produktdatenbank`-Spalten gegen die aktuelle Bibliothek-UI. Erste Analyse identifizierte **8 fehlende Felder** (pflegelevel, intensitaet, anwendung, kombinationen, kombi_optional, ist_smoothing, ist_zwei_in_eins, ist_curl_volumen_booster).

**User-Reality-Check** — die Beraterin darf keine System-Kenntnisse haben. `pflegelevel` als LOW/MID/HIGH ist eine System-Klassifikation, nicht aus PDF ableitbar. Verweis auf frühere Session (paralleler Tab) mit intensiver Diskussion darüber.

### Datenanalyse zur Ableitbarkeit

Reverse-Engineering aus dem Live-Sheet-Backup (37 Produkte):

**`pflegelevel`** — Ergebnis: NICHT ableitbar aus einzelnem Feld. Aber **das bestehende „Zielgruppe laut PDF"-Feld ist bereits Multi-Chip** und deckt es semantisch ab (Chip 1 → +LOW, Chip 2 → +MID, Chip 3 → +HIGH). Meine erste Interpretation war falsch — es ist kein Radio-Chip, sondern Multi-Chip (2 selected im Mockup). Verifiziert an 4 Live-Beispielen: Renew (alle 3 Chips → LOW,MID,HIGH ✓), Bond IQ Night Day Serum (nur Chip 3 → HIGH ✓), Essig Shampoo (Chip 1+2 → LOW,MID ✓), Bond IQ Shampoo (Chip 2+3 → MID,HIGH ✓).

**`intensitaet`** — orthogonal zu allen anderen Feldern, wirklich nicht aus Funktionalität ableitbar. Kreuz-Tab pflegelevel × intensitaet zeigt volle Streuung. Nach Diskussion der drei Optionen (weglassen mit Bianca-Effekt / Slot-basierte Heuristik / PDF-freundliche Extra-Frage) User-Entscheidung: **Option C3 — Extra-Radio-Chip mit PDF-freundlicher Sprache** (Alltagspflege / Vielseitig (Default) / Intensiv-Pflege).

### Coverage-Ergebnis: schlanke Umsetzung

Statt 8 → nur 4 UI-Änderungen nötig, weil:
- `pflegelevel` durch bestehendes Zielgruppen-Feld bereits abgedeckt
- 9 Bool-Flags aus Nutzen-Tabelle + Passung ableitbar
- `anwendung`, `kombinationen`, `produkt_url` bewusst weggelassen (Beraterin packt in Verkaufsbegründung, produkt_url ist Legacy-Anfangsidee)
- `ist_curl_volumen_booster` aus Slot=Styling + Nutzen Volumen + Passung Lockig/Kraus ableitbar

### Die 5 finalen UI-Änderungen

1. **Slot-Typ + conditional 2-in-1-Zusatz** — visuell eingerückter Block mit ↳-Marker „Zusatz-Frage nur bei Shampoo", Ja/Nein
2. **Nutzen-Tabelle Legenden präzisiert** — „alle Zeilen starten auf —, du klickst nur bei tatsächlich zutreffenden Nutzen auf Haupt/Auch"
3. **Bonding-/Repair-Linie (Ja/Nein) → Multi-Chip „Spezielle Sub-Serie"** mit Bonding-/Repair-Linie + Smoothing-/Glättungs-Linie. Skalierbar für weitere Sub-Serien ohne UI-Umbau.
4. **Zielgruppen-Feld markenneutral** — „Zielgruppe laut PDF" → „Zielgruppe des Produkts" mit Hint „aus Datenblatt, Katalog oder Produktbeschreibung"
5. **NEU: Wirkstärke-Beschreibung** — Radio-Chip 3 Optionen, Default „Vielseitig"

### UX-Anpassungen aus User-Feedback

Nach erster Umsetzung drei UX-Wünsche:
- **2-in-1 nur bei Shampoo sichtbar** — mit CSS-Klasse `.conditional-block` (gestrichelter Border-Left, ↳-Marker, kupfer-farbenes Label)
- **Info-Texte einklappbar** — alle `form-help`-Blocks in `<details class="info-toggle"><summary>ⓘ …</summary><div class="info-body">…</div></details>` umgebaut. Nativer HTML-Toggle, kein JS. Beim ersten Ausfüllen sichtbar via Klick, danach bleibt zusammengeklappt.
- **Bezugsquelle-Link entfernt** — Memory-Verweis auf `project_produkt_url_aufgegeben`: Backend nutzt es nicht, Anfangsidee, Integration scheiterte. Feld raus.

### Live-Preview-Datei getrennt

Neue Datei `demo/bibliothek-live.html` gezogen als eigenständige Design-Referenz für die spätere React-Component im Dashboard. Konzept-Elemente entfernt: Hero, Info-Grid „Warum Buttons statt Freitext", Mockup-Titelbar, explain-cards, Team-Callout, Footer. Nur der reine Formular-Kern bleibt, eingebettet in schlanken `<main class="live-wrap">` + `<header class="live-header">` mit Breadcrumb.

Damit klare Trennung:
- `demo/bibliothek.html` = Konzept-Mockup (Sales/Erklär-Material für Sina & Co)
- `demo/bibliothek-live.html` = Design-Referenz für Dashboard-Component-Implementierung

## Persistenz-Aktionen am Session-Ende

Damit das Design-Ergebnis nicht in nächsten Chats neu diskutiert wird:

1. **Neuer Memory-File** `project-bibliothek-design-locked.md` — 9 Felder + Ableitungs-Regeln + UX-Prinzipien als Beschlussstand
2. **Update Memory** `project-bibliothek-ux-tracks-layer2.md` — Status „Design fertig 2026-07-13", Verweis auf locked-Memory, Sub-Serien-Multi-Chip-Prinzip ergänzt
3. **Update `MEMORY.md`-Index** — neue Zeile für locked-Memory
4. **Update `HANDOVER.md`** — neuer Abschnitt „Bibliothek-UI (Design fertig 2026-07-13)" mit vollständiger Faktografie
5. **Diese Session-Doku** — Verlauf + Wiedereinstieg-Prompt

## Was in dieser Session NICHT gemacht wurde

- **Layer-2-Runde 2** (weitere Regel-Umbauten) — nicht angefangen. PFL-OV war schon markenneutral, Task #6 (K-06-Follow-up mit `ist_bonding`-REQ-Regeln) blieb offen.
- **React-Portierung** in Dashboard — die Live-Preview ist die visuelle Referenz, aber die eigentliche interaktive Component ist noch zu bauen.
- **CSS-Aufräumen in `bibliothek-live.html`** — die Konzept-Klassen (`.hero`, `.info-grid`, `.mockup-wrap`, `.explain-*`, `.team-*`, `.footer`) sind noch im Style-Block enthalten, obwohl nicht mehr genutzt. Optimierung, nicht funktional relevant.
- **Commit** — Änderungen sind lokal, noch nicht gepusht.

## Offene Punkte für nächste Session(s)

1. **React-Portierung Dashboard-Component** — Bibliothek als interaktive Component in `src/app/(dashboard)/...` einbauen. `demo/bibliothek-live.html` als visuelle Referenz nutzen.
2. **CSS-Aufräumen** `bibliothek-live.html` — Konzept-Klassen im Style-Block entfernen (~10 KB Overhead, lohnt sich bei React-Portierung ohnehin).
3. **Task #6 K-06-Follow-up** — `ist_bonding`-REQ-Regeln in `map_slot_rules` prüfen und umbauen. Kombination aus `ist_bonding_line`-Filter + Bereinigung der `ist_bonding`-Datenpflege.
4. **Layer-2-Prinzip-Liste konsolidieren** in HANDOVER (mittlerweile 6+ Prinzipien).
5. **Backend-Migrations-Layer** — die Ableitungs-Regeln aus [[project-bibliothek-design-locked]] als Postgres-Migration umsetzen, wenn wir Sheets → Postgres migrieren.
