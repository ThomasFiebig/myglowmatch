# Session 2026-07-07 — Whitelabel-Konzept-Landing + Team-Sharing + Framing-Korrektur

**Business-Track-Session** (Fortsetzung von `2026-07-06_konzept-landing.md`
Nachtrag). Kein Code-Bau am Workflow — Fokus auf Umbau der Konzept-Landing
für die markenneutrale Strategie, Team-Sharing-Prominenz und juristisches
Framing.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-07_whitelabel-landing.md`, `SAAS_BACKLOG.md`
> (aktuelle Version inkl. Kapitel 2.5 „Team-Sharing" und uncommitted
> Kapitel 2.6 „Compliance-Absicherung Whitelabel") sowie
> `public/konzept/index.html`. Nächster konkreter Schritt: **Rückmeldung
> von Sina/Marcel abwarten** (Namensfreigabe MyBeautyKey + Feedback zum
> markenneutralen Konzept). Danach entweder Whitelabel-Grundgerüst als
> Route-Group `src/app/(whitelabel)/` starten oder — falls Zeit vorher —
> Kapitel 2.6 des Backlogs prüfen und ggf. Compliance-Absicherungen
> (Beraterin-Attribution auf Kundinnenseite, leere Bibliothek als Default,
> Impressum-Struktur) ins Konzept aufnehmen.

## Stand am Ende der Session

- **Neue Konzept-Landing live** unter `myglowmatch.de/konzept` mit
  sechs Karten (01 Neuer Ansatz, 02 Preise, 03 Bibliothek + Team-Sharing,
  04 App-Demo, 05 Dashboard-Demo mit Bibliothek-Ankündigung, 06 Live-
  Fragebogen). Warnbanner der Vor-Session raus. Fallback-Sektion für
  nicht-versendete MONAT-Antrag-Docs unten dran.
- **Neue Konzept-Übersicht** unter `demo/zoom-2026-07-06-update.html`
  (Kopie in `public/konzept/`). Neun Punkte, drei §-Blöcke in Punkt 1
  als Compliance-Begründung, Preistabelle 3-Karten, Feature-Matrix
  Free/Basic/Pro inkl. Team-Sharing-Zeile, Bibliothek-Konzept in 4
  Schritten mit strategischem Callout, Bau-Reihenfolge in 11 Schritten,
  MONAT-Antrag-Status als Reserve.
- **WhatsApp-Nachricht** für Marcel in `demo/whatsapp-marcel-2026-07-06.md`
  (zwei Varianten: kompakt + Chat-Style). Erwähnt §§ 3.2.1/3.2.5/3.6.1,
  markenneutralen Umschwung und Team-Sharing.
- **PDF neu generiert** über Chrome Headless — `Konzept-Uebersicht.pdf`
  im finalen Stand nach allen Korrekturen (464 KB).
- **Framing-Korrektur** durchgezogen: „Bekannter mit juristischem
  Know-how" statt „Jurist", keine Freigabewahrscheinlichkeit mehr,
  Compliance-Grund konkret als §§-Trio, „größere Zielgruppe" als
  VERADEX-interne Business-Rationale komplett aus Sina/Marcel-Sicht raus.
- **Uncommitted im Working-Tree**: `SAAS_BACKLOG.md` mit neuem Kapitel 2.6
  „Compliance-Absicherung Whitelabel" (drei Fallen: vorbelegte Bibliothek,
  Kundinnenseite mit Markennamen, ...). Parallel entstanden, thematisch
  separater Commit.

## Was in dieser Session passiert ist

### Phase 1 — Neubau der Konzept-Landing

Wiedereinstieg aus dem Nachtrag von `2026-07-06_konzept-landing.md`. Ziel:
den orangefarbenen Warnbanner der Vor-Session ersetzen durch eine
vollwertige Landing für die markenneutrale Strategie.

- **`demo/zoom-2026-07-06-update.html` gebaut** — komplette Neuschreibung
  der Konzept-Übersicht aus dem vorherigen 4.-Juli-Dokument. Cover mit
  neuer Kernaussage, neun Sachpunkte, Champagne-Rosé-Optik konsistent
  gehalten. Anker `#preise` und `#bibliothek` für Direktlinks aus der
  Landing.
- **`public/konzept/index.html` umgebaut** — Warnbanner raus,
  sechs Karten neu strukturiert. Karte 01 als „pinned" mit Champagne-
  Gradient hervorgehoben. Karten 02 + 03 mit Deep-Link-Ankern auf die
  Konzept-Übersicht. Karten 04 – 06 (Demos + Live-Fragebogen) inhaltlich
  gleich, aber Nummerierung angepasst. Neue Fallback-Sektion in dezenter
  Optik (dashed Border, muted Farben) für die nicht-versendeten
  MONAT-Antrag-Docs.
- **`demo/whatsapp-marcel-2026-07-06.md`** — Nachricht in zwei Varianten
  formuliert (ein Block empfohlen, drei kürzere für Chat-Style).
- **PDF-Generation** via Chrome Headless etabliert (Command im WhatsApp-
  Dokument nicht, aber im weiteren Verlauf sauber wiederverwendbar).

### Phase 2 — Team-Sharing prominent platziert

Zwischen Phase 1 und 2 hat Thomas Kapitel 2.5 „Team-Sharing" im
`SAAS_BACKLOG.md` ergänzt (Commit `60cf058`). Kernidee: Uplines wie Sina
generieren einen Team-Code, Downlines übernehmen die Bibliothek einmalig
per Kopie (nicht Live-Sync). Onboarding-Barriere sinkt von 45–90 Minuten
auf 30 Sekunden.

Session-Aufgabe: Team-Sharing in die drei Sina/Marcel-Dokumente einbauen.

- **Landing Karte 03** — Titel jetzt „Produkt-Bibliothek + Team-Sharing",
  zusätzlicher `.note`-Absatz mit Team-Code-Argument und Rechts-Rationale
  (Content-Verantwortung wandert beim aktiven Übernehmen zur Downline).
- **Konzept-Übersicht Punkt 6** — aus drei Schritten wurden vier.
  Schritt 4 „Uplines geben ihre Bibliothek an Downlines weiter" mit
  Team-Code-Beispiel `SINA-2M8K`, Kopie statt Live-Sync, Pull-Notification
  auf aktives Ja/Nein. Neuer grüner Callout „Strategischer Wert für Sinas
  Team" — Sina wird zur aktiven Team-Multiplikatorin statt nur
  Botschafterin, im Pro-Preis enthalten.
- **Feature-Matrix in Punkt 5** um Team-Sharing-Zeile ergänzt, damit
  Punkt 6 keinen Kontext-Sprung erzeugt.
- **WhatsApp-Nachricht** in beiden Varianten um einen Team-Code-Absatz
  erweitert.

### Phase 3 — Framing-Korrektur nach Thomas' Rückmeldung

Nach dem ersten Commit meldete Thomas vier Punkte zurück:

1. „Jurist" ist falsch — es war ein Bekannter mit juristischem Verständnis,
   kein offiziell mandatiertes Rechtsgespräch. Überall korrigieren.
2. Freigabewahrscheinlichkeit (15–30 %) rausnehmen. Spekulativ, keine
   belastbare Aussage.
3. Einleitung sollte den Compliance-Grund konkret nennen: welche
   MONAT-Paragraphen sind einschlägig, warum blockieren sie das
   ursprüngliche Konzept. Details damit prüfbar, nicht Bauchgefühl.
4. „Größere Zielgruppe" ist VERADEX-interne Business-Rationale — hat auf
   einer Sina/Marcel-Übersicht nichts zu suchen und wirkt eher wie
   Prahlerei.

Umsetzung:

- **Punkt 1 der Konzept-Übersicht komplett umgeschrieben** — statt einer
  Wahrscheinlichkeits-Aussage jetzt drei `.item`-Blöcke mit den
  wörtlichen Zitaten aus § 3.2.1 (Verbot eigener Geschäftsinstrumente),
  § 3.2.5 (MONAT-Marken/Produktnamen) und § 3.6.1 (wortwörtliche
  Herkunft der Aussagen). Konzeptbezug pro Paragraph erklärt. Callout
  am Ende: „Solange auch nur einer dieser drei Paragraphen greift, hängt
  das Projekt an einer schriftlichen Freigabe."
- **Cover-Subtitle** angepasst — verweist auf die drei Paragraphen als
  Umschwungs-Grund, nicht auf Marktkontrolle-Motive.
- **Punkt 3 Item „Größere Zielgruppe"** komplett gestrichen. Übrig
  bleiben zwei Vorteile: Sofort startfähig + Kein Risiko fürs Team.
- **Preistabellen-Erläuterung** — „Kompensation über die deutlich größere
  Zielgruppe" raus, ersetzt durch „weniger Auto-Magie, fairerer
  Einstiegspreis".
- **Landing Hero-Subtitle + Lead** — Bekannter-mit-juristischem-Know-how-
  Formulierung, Verweis auf die drei §§ als Umschwungs-Grund,
  Zielgruppen-Argument („funktioniert gleichzeitig für jede
  Beauty-Beraterin") raus.
- **Landing Karte 01** — Beschreibung präzisiert: nennt jetzt die drei
  Paragraphen als Blocker des ursprünglichen Konzepts.
- **Landing Karte 02 Note** — „20 – 50-fach größere Zielgruppe" gestrichen,
  Fokus rein auf Preisreduktions-Begründung.
- **WhatsApp beide Varianten** entsprechend umformuliert — nennt die
  drei Paragraphen beim Namen, Zielgruppen-Argument komplett raus.

### Phase 4 — Callout in Punkt 6 gestrichen

Letzte Rückmeldung: der Callout „Warum das der zentrale
Verkaufsargumentations-Punkt ist" (Zeitersparnis in Aktions-Wochen, Sinas
Kern-Argument im Zoom) gehört auch nicht in die Sina/Marcel-Übersicht.
Ersatzlos raus. Punkt 6 endet jetzt mit dem grünen „Strategischer
Wert"-Callout aus Phase 2.

## Neue Artefakte

- `demo/zoom-2026-07-06-update.html` — neue Konzept-Übersicht (drei
  Seiten, Anker `#preise` + `#bibliothek`)
- `public/konzept/zoom-2026-07-06-update.html` — Kopie für Deployment
- `demo/whatsapp-marcel-2026-07-06.md` — WhatsApp-Nachricht in zwei
  Varianten mit Hintergrund-Kontext
- `public/konzept/Konzept-Uebersicht.pdf` — überschrieben, jetzt aus
  neuer HTML generiert (464 KB, drei A4-Seiten)
- `public/konzept/index.html` — überschrieben, neue Landing

Die alte `zoom-2026-07-04-update.html` bleibt in `public/konzept/` liegen
(nicht mehr verlinkt), analog zum liegengebliebenen MONAT-Antrag.

## Git-Commits (auf `main`)

- `e196568` feat(konzept): Whitelabel-Landing + Team-Sharing für Sina/Marcel
- `7b11711` fix(konzept): Rücksprache-Framing korrigiert, §§ 3.2.1/3.2.5/3.6.1
  in Einleitung
- `c6c3af7` fix(konzept): Callout „zentraler Verkaufsargumentations-Punkt" aus
  Punkt 6 entfernt

Nicht committed: `SAAS_BACKLOG.md` mit Kapitel 2.6 „Compliance-Absicherung
Whitelabel" — parallel im Working-Tree entstanden, thematisch eigenständig.
Bewusst nicht mit den Sina/Marcel-Korrekturen vermischt.

## Bewusst NICHT in dieser Session gemacht

- **`SAAS_BACKLOG.md`-Commit für Kapitel 2.6.** Warten auf Thomas'
  Freigabe des Inhalts, dann eigener Commit.
- **Whitelabel-Grundgerüst als Route-Group `src/app/(whitelabel)/`.**
  Kommt erst nach Namensfreigabe durch Sina/Marcel, sonst doppelte Arbeit
  bei Umbenennung.
- **Bau-Umsetzung von Team-Sharing** (Team-Code-Generator im Portal,
  Import-Flow bei Downlines). Konzeptuell in Backlog Kapitel 2.5 + 3
  Schritt 9.a fixiert, Bau erst nach Basic-Modus.
- **HANDOVER.md-Update.** Weiter n8n-fokussiert, SaaS-Track läuft
  parallel im `SAAS_BACKLOG.md`.

## Folgepunkte für nächste Session

### Priorität 1: Rückmeldung von Sina/Marcel abwarten

- Namensfreigabe MyBeautyKey (oder Alternative)
- Feedback zum markenneutralen Konzept
- MONAT-DACH-Ansprechpartner ist nicht mehr dringend, kann später kommen

### Priorität 2: Kapitel 2.6 „Compliance-Absicherung Whitelabel"

- Inhalt mit Thomas durchgehen und ggf. verfeinern
- Als eigener Commit auf `main`
- Prüfen, ob die drei Fallen ins Konzept für Sina/Marcel gehören (eher
  nein — ist VERADEX-Selbstschutz, keine Team-Info)
- Ggf. relevante Punkte in `demo/BUILD_SPEC.md` durchziehen

### Priorität 3: Whitelabel-Bau vorbereiten

Wenn Sina/Marcel den Namen freigeben:
1. Domain sichern (`mybeautykey.de` oder finale Alternative)
2. Route-Group `src/app/(whitelabel)/` aufsetzen (parallel zum bestehenden
   MONAT-System)
3. Fragebogen kopieren, MONAT-Vokabular streichen
4. Ergebnisseite markenneutral bauen (Bedarfsprofil statt Produktnamen)
5. Free-Modus zuerst — kein Login, Limit 3 Beratungen/Monat

Details in `SAAS_BACKLOG.md` Kapitel 3.

## Konvention gelernt (für spätere Sessions)

Bei Sina/Marcel-Dokumenten strikt trennen:

- **Was Sina/Marcel wissen müssen** — Compliance-Grund, konkrete
  Paragraphen, Preise, Feature-Split, Bau-Reihenfolge, Team-Argument.
- **Was VERADEX-intern bleibt** — Zielgruppen-Erweiterung (20–50-fach),
  Marktkontroll-Motive von MONAT, Wahrscheinlichkeits-Schätzungen,
  Business-Case-Rechnungen. Gehört in `SAAS_BACKLOG.md`, nicht in
  Präsentations-Dokumente.

Formulierungs-Detail: wenn eine juristische Einschätzung von einer
Person außerhalb der Rechtsberatungs-Beziehung kommt, „Bekannter mit
juristischem Know-how" — nicht „Jurist", nicht „Rechts-Rücksprache".
Präzision zählt hier, weil ein Fehletikett das Gegenüber später fragen
könnte „wer war das genau?" und die Antwort peinlich wird.
