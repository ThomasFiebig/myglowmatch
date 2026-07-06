# Session 2026-07-06 — Konzept-Landing + Antragsschreiben MONAT + SaaS-Backlog fixiert

**Business-Track-Session** (Parallel zum n8n-Track). Kein Code-Bau am Workflow —
Fokus auf Vermarktung, MONAT-Compliance, Preismodell und Kommunikation an Sina/Marcel.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-06_konzept-landing.md`, `SAAS_BACKLOG.md` und
> `demo/BUILD_SPEC.md`. Nächster konkreter Bau-Task: **Etappe 2 —
> Dashboard-Update mit Branding-Bereich** (Portrait-Upload, Farbwahl inkl.
> Pastellpalette, Grußformel-Feld, Deckblatt-Austausch für den Fragebogen).
> Aktuelle Dashboard-Demo liegt in `demo/partner-portal.html` bzw.
> `public/konzept/partner-portal.html`. Nach Umbau `public/konzept/`-Version
> überschreiben, Landing bleibt gleich.

## Stand am Ende der Session

- **Konzept-Landing live** unter `myglowmatch.de/konzept` mit sechs Kacheln
  (Zoom-Update, VERADEX-Antrag, Sinas Vorspann, App-Demo, Dashboard-Demo,
  Live-Fragebogen). HTML + PDF pro Dokument, downloadbar. `noindex/nofollow`,
  kein Sitemap-Eintrag.
- **VERADEX-Antrag an MONAT-DACH** final: zweiseitig, VERADEX-Briefpapier-Look
  (Header + Footer aus Original-PDF-Vorlage als Vollflächen-Hintergrund),
  Corporate-Farben (Anthrazit + Cream + Stahlblau), Helvetica Neue Light.
- **Sinas Vorspann** final: myglowmatch-Champagne-Rosé-Look, drei
  Kern-Mehrwerte hervorgehoben (Aktionszeit-Tempo, einheitliche
  Beratungsgrundlage, 1:1-Datenblatt-Konformität).
- **Preismodell fixiert**: Basic 14,90 €/Monat oder 179 €/Jahr · Pro 29,90 €/Monat
  oder 359 €/Jahr · Setup einmalig 49,90 € (entfällt bei Jahresabo). Details
  in `SAAS_BACKLOG.md`.
- **Feature-Split Basic/Pro** definiert (siehe `SAAS_BACKLOG.md`).
- **Alle strategischen Entscheidungen** aus dieser Session in
  `SAAS_BACKLOG.md` konserviert.

## Was in dieser Session passiert ist

### Projekt-Setup Claude.ai

Beschreibung und Anweisung für das Claude.ai-Projekt formuliert und
weiterverfeinert. Kern der Anweisung: Denkpartner statt Ausführer, Deutsch/direkt,
Fach-Respekt für Desirée, Konservativität bei Rechtsthemen. Beschreibung
enthält Rollentrennung (Desirée = Owner:in, VERADEX = Rechtshülle).

### Preismodell-Iterationen

1. Erste Version: 29 €/Monat + 49,90 € Setup (aus SaaS-Session 3. Juli)
2. Basic/Pro-Split eingeführt: 14,90 € vs. 29,90 €
3. Setup-Fee-Diskussion: gestaffelt (29,90/49,90) vs. einheitlich (49,90/49,90)
   → einheitlich gewählt, weil gestaffelt Arbitrage bei Upgrade ermöglicht
4. Jahresabo: keine 2 Monate frei, nur Setup-Erlass = 22 % Ersparnis
5. Finale Tabelle: Basic 14,90 €/179 € · Pro 29,90 €/359 € · Setup 49,90 €
   (entfällt bei Jahresabo)

### Feature-Verschiebungen und -Streichungen

- **Verworfen: WhatsApp-Beratung per Meta-API** — Kostenlast bei Skalierung,
  Compliance-Sonderprüfung. Ersatz: Ergebnisseite im Browser + `wa.me`-Button
  zur privaten WhatsApp-Nummer der Beraterin (0 € Betriebskosten).
- **Verworfen: eigene Domain pro Beraterin** — Support-Aufwand vs. Nutzen.
  Ersatz: URL-Path mit Beraterin-Slug (`[name].de/[Beraterin]`).
- **Verworfen: kostenlose Testphase** — öffentliche Demo übernimmt die
  Trial-Funktion.
- **Neu als Pro-Feature: `warum_sinnvoll`-Spalte** in produktdatenbank — PDF-
  wörtliche Verkaufsargumente pro Produkt (Konvention K-04 strikt, nicht K-08
  wie zunächst diskutiert). Nur im Beraterinnen-Portal sichtbar, nie in der
  Kundinnen-Mail — klarer Upgrade-Trigger.
- **Neu als Pro-Feature: PWA-Installation** — Dashboard als App auf dem
  Homebildschirm der Beraterin.
- **Meinungsänderung: Pastellfarben + Deckblatt-Austausch** — waren am 3. Juli
  aus Marken-Konsistenz-Gründen verworfen, jetzt revidiert (Sinas Argument
  vom Zoom stärker: Beraterinnen wollen Personalisierung). Umsetzung in
  Etappe 2.

### MONAT-Antragsstrategie

Variante-Vergleich A/B/C durchgespielt:
- **A**: VERADEX schreibt direkt → Cold Call, geringes Standing bei MONAT.
- **B**: Sina schreibt allein als Markenpartnerin → exponiert sie unnötig.
- **C**: Sina persönlicher Vorspann + VERADEX-Antrag als PDF-Anhang →
  gewählt. Kombiniert Sinas Standing mit VERADEX' fachlicher Präzision.

### Antragsschreiben-Iterationen (zahlreich)

Der VERADEX-Antrag wurde in mehreren Runden geschärft:
- Zunächst SVG-Nachbau des Briefpapiers → wieder verworfen, echtes Briefpapier
  als PNG-Hintergrund (via `sips` aus PDF konvertiert)
- Layout-Umbau von `position:fixed` auf `.page`-Container mit Vollflächen-
  Hintergrund pro Seite (Chrome Print zuverlässiger)
- Rollen-Split korrigiert: Desirée fachlich UND technisch, Thomas/VERADEX =
  Rechtshülle (Vertrag, Betrieb formal, DSGVO-Verantwortlicher)
- „aktuell inaktiv" bei beiden Markenpartner-IDs entfernt (irrelevant, weckt
  unnötig Fragen)
- Paragraphen präzisiert (DE-Fassung 01.04.2026): § 3.2.1 Genehmigungspflicht,
  § 3.2.5 nur Produktnamen, § 3.6.1 Wortlaut-Treue, § 3.6.3 keine
  Einkommens-Claims, § 3.2.8 E-Mail-Pflichten, § 3.20/DSGVO, § 3.9.1
  Ambassador-Schutz
- Zwei Streichungen: (a) AVV-Satz raus („schlafende Hunde wecken"), (b) Art.-9-
  DSGVO-Aussage raus (Kopfhautprobleme könnten als Gesundheitsdaten
  qualifiziert werden, keine unnötige Selbstfestlegung)
- Zwei Ergänzungen: EU-Server bzw. Standardvertragsklauseln nach Art. 46
  DSGVO, TMG-Impressum + Datenschutzerklärung auf allen Kundinnen-Oberflächen
- Framing-Split: „was die Kundin wörtlich sieht" (Zitat + Quelle) klar
  getrennt von „intern als Datengrundlage" (Datenblatt-Auswertung)
- Ton: aktiv beantragend statt informativ anzeigend

### Sinas Vorspann-Iterationen

Aus dem sanften „ich habe getestet und bin überzeugt" wurde ein
Business-Argument mit drei konkret gehighlighteten Mehrwerten:
1. **Beratungstempo in Aktionszeiträumen** — direkter Umsatzeffekt für MONAT
2. **Einheitliche Beratungsgrundlage** — kein Bauchgefühl, kein
   „passt-schon-irgendwie"
3. **1:1-Datenblatt-Konformität** — Compliance-Schutz für Partnerin und MONAT

### Konzept-Landing gebaut

- `public/konzept/` als versteckter Bereich unter myglowmatch.de-Domain
- Alle sechs Dokumente (drei mit HTML+PDF, zwei Demos, ein Live-Link)
- Champagne-Rosé-Optik konsistent zum Rest der Vorschläge
- `noindex, nofollow` + kein Sitemap-Eintrag
- Fußzeile mit beiden Kontakten inkl. Markenpartner-Nummern
- `vercel.json` mit `Content-Disposition: attachment` für alle
  `/konzept/*.pdf`-Dateien — Downloads funktionieren jetzt sauber
- Absolute Links `/konzept/...` statt relative — sonst hätte Next.js
  `[partner]`-Route sie zum Fragebogen redirected

## Neue Artefakte

- `demo/veradex-anschreiben-monat.html` + `.pdf`
- `demo/sina-vorspann-monat.html` + PDF-Variante als
  `public/konzept/Sina-Vorspann_MONAT.pdf`
- `demo/zoom-2026-07-04-update.html` + PDF als
  `public/konzept/Konzept-Uebersicht.pdf`
- `demo/veradex_briefpapier.png` (aus VERADEX-Original-Briefpapier via `sips`)
- `public/konzept/index.html` (Landing)
- `public/konzept/*.pdf` (3 Downloads)
- `vercel.json` (Content-Disposition-Fix)
- `SAAS_BACKLOG.md` (Business-Track-Referenz)
- `chat-archive/2026-07-06_konzept-landing.md` (diese Doku)

## Git-Commits (auf `main`)

- `fccb362` feat(konzept): Landing unter /konzept mit HTML + PDF für Sina/Marcel
- `c02c5a5` fix(konzept): PDFs unter /konzept forciert als Download ausliefern
- `958d2f7` fix(konzept): Links absolut statt relativ
- Aktueller Commit für Session-Doku + SAAS_BACKLOG folgt

## Bewusst NICHT in dieser Session gemacht

- **Etappe 2 — Dashboard-Update mit Branding-Bereich**. Aufwand ~1–2 h
  konzentrierte Feature-Arbeit, gehört in frische Session. Enthält:
  - Portrait-Upload
  - Farbwahl inkl. Pastellpalette (revidierte Entscheidung)
  - Grußformel-Feld
  - Vorstellungstext-Feld (optional)
  - Deckblatt-Austausch für den Fragebogen
  - „Pro-Features gesperrt"-Zustand für Basic-Partnerinnen (ausgegraut mit
    Upgrade-CTA)
- **HANDOVER.md-Update** für den SaaS-Track. Nicht dringend, HANDOVER
  konzentriert sich weiter auf n8n/Regel-Engine.
- **MONAT-Antrag versenden** — wartet auf Namensfreigabe von Sina/Marcel +
  Ansprechpartner-Info.

## Folgepunkte für nächste Session

### Priorität 1: Etappe 2 — Dashboard-Update

Siehe Wiedereinstieg-Prompt oben. Aufwand ~1–2 h.

### Priorität 2: Namensfreigabe + Ansprechpartner-Info von Sina/Marcel abwarten

Sobald die Info kommt:
- Adressat-Platzhalter in beiden Anschreiben ersetzen
- PDFs neu generieren
- `public/konzept/` synchronisieren
- Ggf. Domain-Umbenennung starten (falls Name wechselt)

### Priorität 3: SAAS_BACKLOG.md als lebendes Dokument pflegen

Jede folgende Session mit Business-Bezug sollte den Backlog aktualisieren —
Status-Updates zu Bau-Reihenfolge, verworfene Ideen dokumentieren, neue
Entscheidungen einordnen.

## WhatsApp-Nachricht an Marcel (aus dieser Session)

Wurde am Ende formuliert, mit Link `myglowmatch.de/konzept` und der Bitte
um zwei Rückmeldungen: Namensfeedback + MONAT-DACH-Ansprechpartner.
