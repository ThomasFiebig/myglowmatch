# Session 2026-07-07 — Konzept-Ausbau: eigene Seiten, Demo-Integration, Framing-Feinschliff

**Business-Track-Session** (Fortsetzung von `2026-07-07_whitelabel-landing.md`).
Kein Code-Bau am Whitelabel-System selbst — Fokus auf Ausbau der Sina/Marcel-
Materialien: eigene Preis- und Bibliothek-Seiten, Bibliothek-Bereich in beide
Demos integriert, Framing-Schärfe an mehreren Stellen, Backlog-Erweiterung.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-07_konzept-ausbau.md`, `SAAS_BACKLOG.md`
> (Kapitel 0, 2.5, 2.6, 2.7) und `demo/whatsapp-marcel-2026-07-06.md`
> (letzte Ergänzung mit Bibliothek-Angebot für Sina).
>
> Kern-Aufgabe: **Rückmeldung von Sina/Marcel abwarten** oder — falls
> parallel möglich — **Domain-Verfügbarkeit MyBeautyKey.de prüfen**
> (`whois mybeautykey.de` bzw. Strato/INWX). Bei positivem Sina/Marcel-
> Feedback: **Whitelabel-Grundgerüst** als Route-Group
> `src/app/(whitelabel)/` starten (SAAS_BACKLOG Kapitel 3, Schritt 3).
> Details zum Bibliothek-UI stehen in `demo/bibliothek.html`, die
> Chip-Vokabular-Sets sind aus `map_priorities.csv` und `map_pool_filter.csv`
> ableitbar.

## Stand am Ende der Session

- **Konzept-Landing** unter `myglowmatch.de/konzept` mit sechs Karten,
  Warnbanner + Fallback-Sektion entfernt, zwei Lead-Absätze (Kurzfassung
  + „Wichtig fürs Verständnis: vollständige MONAT-Empfehlung möglich").
- **Konzept-Übersicht** (`demo/zoom-2026-07-06-update.html`) auf 10
  Punkte ausgebaut, Punkt 4 „Konkrete Anpassungen aus dem Zoom"
  eingesetzt, Punkt 7 „Bewusst weggelassen" wiedereingeführt, Punkt 10
  MONAT-Antrag komplett raus. Missverständnis-Callout in Punkt 2,
  Demo-Rolle in Punkt 4 klar von Free-Tarif abgegrenzt.
- **Eigene Preisseite** unter `/konzept/preise` — Karte 02 der Landing
  zeigt jetzt darauf statt auf einen Anker im Strategiepapier.
- **Eigene Bibliothek-Seite** unter `/konzept/bibliothek` mit visuellem
  Formular-Mockup (11 Felder, Chip-Vokabular aus n8n abgeleitet).
  Produktname-Erklärung schärft: keine Vorschlagsliste, keine Markennutzung
  durch die Plattform.
- **Dashboard-Demo** um Menüpunkt „📚 Meine Bibliothek" erweitert mit
  Team-Sharing-Panel (Team-Code `SINA-2M8K`, „7 Downlines nutzen deine
  Vorlage"), Übernehmen-Feld für Downlines, Sortiment gruppiert nach
  Slot, Pro-Lock-Overlay im Basic-Modus.
- **App-Demo** von 4 auf 5 Bottom-Tabs — neuer Tab „Bibliothek" mit
  kompakter Mobile-View (Team-Code-Card, Slot-Gruppen, Chip-Preview).
- **SAAS_BACKLOG** um Kapitel 2.6 „Compliance-Absicherung Whitelabel"
  und Kapitel 2.7 „Free-Modus Missbrauchs-Schutz" erweitert.
- **WhatsApp-Nachricht an Marcel** in `demo/whatsapp-marcel-2026-07-06.md`
  aktualisiert — 3-Satz-Ergänzung mit den letzten Änderungen, Bibliothek
  wird Sina zur Verfügung gestellt, MONAT-Kontakt nicht mehr dringend.

## Was in dieser Session passiert ist

### Phase 1 — Punkt 4 „Konkrete Anpassungen aus dem Zoom" ergänzt

Die alte 4.-Juli-Zoom-Übersicht hatte fünf Produkt-Anpassungen (Browser-
Ergebnis statt Mail, WhatsApp-Button, Verkaufsargumentations-Hilfe,
Demo, Zwei-Tarif-Modell). Bei der Whitelabel-Neufassung waren die
komplett rausgefallen. Neu eingesetzt als Punkt 4 mit fünf Item-Blöcken,
Verkaufsargumentations-Hilfe rausgelassen (war MONAT-Datenblatt-spezifisch),
Zwei-Tarif → Drei-Tarif. Alle Folgepunkte umnummeriert.

### Phase 2 — „Bewusst weggelassen" wieder rein, Punkt 10 MONAT-Antrag raus

Feedback von Thomas: fehlender „Bewusst weggelassen"-Abschnitt lässt
typische Rückfragen offen. Punkt 7 wieder aufgenommen mit vier Items
(Meta-API-WhatsApp, eigene Domain pro Beraterin, Testphase mit
Personalisierung, Team-Bundle mit Sammelaccount). Namensvorschlag um
„öffnet die Tür für Beraterinnen jenseits von MONAT" gekürzt
(Zielgruppen-Argument bleibt VERADEX-intern). Punkt 10 komplett raus,
inklusive Nach-Signal-Absatz zum MONAT-DACH-Ansprechpartner.

### Phase 3 — Landing-Fallback-Sektion raus

Analog zum entfernten Punkt 10: die Fallback-Sektion „MONAT-Antrag &
Vorspann · nicht aktiv" auf der Landing widersprach dem Signal.
Physische Files bleiben unter `public/konzept/` liegen, nur unverlinkt.

### Phase 4 — Widerspruch „Testphase" behoben

Feedback: „Bewusst weggelassen: kostenlose Testphase" passt nicht, wenn
der Free-Tarif genau diese Funktion übernimmt. Item aus Punkt 7 raus,
dort bleiben drei Auslassungen.

### Phase 5 — Free-Modus-Missbrauchs-Frage → Backlog Kapitel 2.7

Thomas fragt, wie wir das Free-Modul gegen Ausnutzung schützen. Diskussion:
Ökonomie ist stärkster Schutz (10 Fake-Accounts für 30 Beratungen kostet
mehr Aufwand als 9,90 € sparen). Drei Verteidigungs-Ebenen strukturiert:

1. **Launch dabei** (~2–3 h): E-Mail-Verifikation, Wegwerf-Domain-Blocklist,
   IP-Rate-Limit
2. **Konzept-Bestandteil**: Slug-Regeln — numerische Suffixe verweigern,
   Kollisions-Vorschläge nur mit Namens-Varianten
3. **Bei Bedarf nachträglich**: Browser-Fingerprint-Zusammenzug, wegen
   TDDDG § 25 mit Rechtsprüfung

Bewusst nicht: Kreditkarte für Free (Kaufhürde), SMS (Kosten), Captcha
(nervt ehrliche Nutzer). Als Kapitel 2.7 im Backlog fixiert, zusammen mit
Kapitel 2.6 (Compliance-Absicherung Whitelabel) in einem Commit.

### Phase 6 — Preisseite

Karte 02 verlinkte bisher auf einen `#preise`-Anker im 4-seitigen
Strategiepapier. Beim Klick wirkte das wie „hier ist das ganze
Strategiepapier". Neue eigene `preise.html` mit Hero, drei Preiskarten
(Free/Basic/Pro, Pro mit „Empfohlen"-Badge und Champagne-Gradient),
Fußnote mit USt./Wechsel-/Kündigungs-Konditionen, Zurück-Link. Karte 02
zeigt jetzt auf `/konzept/preise`.

### Phase 7 — Bibliothek-Seite

Ähnliches Problem bei Karte 03. Neue eigene `bibliothek.html` mit
visuellem Formular-Mockup: 11 Felder, ausgefüllt am Beispiel „Renew
Shampoo" für coloriertes trockenes Haar. Chip-Vokabular aus
`map_priorities.csv` und `map_pool_filter.csv` abgeleitet
(kopfhaut, haarstruktur, haarstaerke, haarzustand, hauptfunktion,
intensitaet, ausschluss_bei). Klare Trennung Chips vs. Freitext,
Team-Sharing-Callout am Ende. Zusatz-Iteration: Produktname-Erklärung
geschärft — die Plattform stellt keine Vorschlagsliste und kein
Autocomplete mit Marken/Produktnamen, die Beraterin tippt selbst
(deckt Kapitel 2.6 Falle 1 ab).

### Phase 8 — Bibliothek-Bereich in beide Demos integriert

Nachdem das Bibliothek-Konzept auf einer eigenen Seite lebt, mussten
beide Demos nachziehen.

**Dashboard-Demo** (`partner-portal.html`):
- Nav-Menüpunkt „📚 Meine Bibliothek" zwischen „Beratung starten" und
  „Mein Branding"
- Neue View mit Team-Sharing-Panel (Team-Code + Copy-Button, „7 Downlines
  nutzen deine Vorlage") und Übernehmen-Feld
- Sortiment gruppiert nach Slot (Shampoo, Spülung, Kur, Styling einzeln
  ausgeklappt, Leave-in/Serum/Kopfhaut kompakt)
- Produktkarten mit Chip-Preview und Team-Vorlage-Status
- Verdrahtet mit bestehendem `.pro-lock`-Mechanismus, Basic-Umschalter
  greift automatisch

**App-Demo** (`partner-app.html`):
- Bottom-Bar von 4 auf 5 Tabs (Übersicht · Kundinnen · Bibliothek ·
  Statistik · Konto), `grid-template-columns:repeat(5,1fr)`
- Neue `v-bibliothek`-View, Mobile-optimiert
- `titles` und `tabIndex`-Mapping mitgezogen

Nebenbei: Zur Farbfrage Lavendel entschieden — bewusst weiter nicht
anbieten. Positionierung „was Eigenes" bleibt, Plattform-Brand
Champagne/Rosé/Kupfer.

### Phase 9 — Klarstellung „vollständige MONAT-Empfehlung bleibt möglich"

Thomas' Beobachtung beim Testlesen: der markenneutrale Ansatz liest sich
so, als würde die Kundin am Ende nur eine „normale Analyse" ohne konkrete
Produkte bekommen. Das ist der zentrale Missverständnis-Punkt.

- **Landing**: zweiter Lead-Absatz („Wichtig fürs Verständnis") direkt
  unter dem ersten. Stellt klar: im Pro-Tarif sieht die Kundin trotzdem
  eine vollständige, konkrete MONAT-Empfehlung — nur läuft der Content
  über Sinas Bibliothek statt eine VERADEX-Datenbank.
- **Konzept-Übersicht Punkt 2**: neuer Callout vor dem rechtlichen
  Callout mit Titel „Damit kein Missverständnis aufkommt — vollständige
  MONAT-Empfehlung bleibt möglich". Konkrete Produktnamen-Beispiele
  (Renew Shampoo, Feuchtigkeitsspülung, Curl-Creme) und die Aussage
  „aus Sinas Sicht ändert sich am Ergebnis nichts".
- Bestehender „rechtlich"-Callout um „in der Plattform selbst" präzisiert.

### Phase 10 — „Kein Risiko fürs Team" ersetzt, Demo-Rolle geschärft

Feedback: „Kein Risiko fürs Team" war eine Haftungs-Aussage, die wir
nicht tragen können. Ab Pro-Modus mit eingepflegten MONAT-Produkten
haftet die Beraterin selbst.

- Item „Kein Risiko fürs Team" in Punkt 3 ersetzt durch „Alles in
  Beraterin-Hand" — die Beraterin entscheidet selbst was empfohlen wird,
  Team-Sharing als Skalierungs-Vorteil erwähnt.
- Demo-Rolle in Punkt 4 neu strukturiert: Free-Tarif beantwortet „wie
  fühlt es sich für mich als Beraterin an", öffentliche Pro-Demo
  beantwortet „was kann das obere Ende". Beide Wege koexistieren, keine
  Trial-Rolle mehr für die Demo.

### Phase 11 — WhatsApp-Ergänzung für Marcel

Zwei Iterationen mit Thomas. Kern der finalen Fassung: drei Sätze,
verweist auf die drei MONAT-Paragraphen als Umstellungs-Grund, listet
die neuen Konzept-Bestandteile auf (Preise, Bibliothek, Team-Sharing)
und stellt heraus, dass Thomas Sina die Bibliothek vorpflegt — Sina hat
null Aufwand, kann per Team-Code übernehmen und an Downlines weitergeben.
MONAT-DACH-Ansprechpartner nicht mehr dringend.

## Neue Artefakte

- `demo/preise.html` + `public/konzept/preise.html` — kompakte
  Preisseite (Free/Basic/Pro-Karten, Fußnote, Zurück-Link)
- `demo/bibliothek.html` + `public/konzept/bibliothek.html` — Bibliothek-
  Konzept mit Formular-Mockup und Chip-Vokabular
- SAAS_BACKLOG Kapitel 2.6 „Compliance-Absicherung Whitelabel"
- SAAS_BACKLOG Kapitel 2.7 „Free-Modus Missbrauchs-Schutz"
- Bibliothek-Bereich in `partner-portal.html` (Dashboard-View)
- Bibliothek-Tab in `partner-app.html` (5. Bottom-Tab + View)
- Aktualisierte `demo/whatsapp-marcel-2026-07-06.md` (Update-Ergänzung
  mit Bibliothek-Angebot)

## Git-Commits (auf `main`, chronologisch)

- `d2e1252` feat(konzept): Punkt 4 „Konkrete Anpassungen aus dem Zoom"
  ergänzt
- `89ea44e` feat(konzept): „Bewusst weggelassen" wieder rein, MONAT-Antrag-
  Punkt raus
- `286d185` fix(konzept): Fallback-Sektion aus Landing entfernt
- `cfdb5b8` fix(konzept): „Kostenlose Testphase" aus Punkt 7 entfernt
- `b47019e` docs(backlog): Kapitel 2.7 „Free-Modus Missbrauchs-Schutz"
  ergänzt (mit 2.6 mitgestaged)
- `95cbb28` feat(konzept): eigene Preisseite unter /konzept/preise
- `6a14656` feat(konzept): eigene Bibliothek-Seite mit Chip-Vokabular-Mockup
- `bb4cbab` fix(konzept): Produktname-Erklärung schärfer — keine
  Marken-Vorauswahl
- `272baf6` feat(demo): Bibliothek-Bereich in Dashboard- und App-Demo
  integriert
- `69d2f12` docs(konzept): Klarstellung „vollständige MONAT-Empfehlung
  bleibt möglich"
- `c3ce94d` fix(konzept): „Kein Risiko fürs Team" ersetzt, Demo-Rolle
  geschärft

## Bewusst NICHT in dieser Session gemacht

- **Whitelabel-Grundgerüst.** Weiter auf Sina/Marcel-Freigabe wartend.
- **Domain-Sicherung MyBeautyKey.de.** Kommt sobald Marcel den Namen
  bestätigt oder eine Alternative nennt.
- **Kapitel 2.6/2.7-Implementierung.** Konzept steht, Bau erst zusammen
  mit Whitelabel-Grundgerüst.
- **HANDOVER.md-Update.** Weiter n8n-fokussiert, SaaS-Track lebt im
  `SAAS_BACKLOG.md`.
- **Farbe Lavendel im Branding-Bereich.** Bewusst nicht aufgenommen —
  Positionierung „was Eigenes" bleibt.

## Folgepunkte für nächste Session

### Priorität 1: WhatsApp-Ergänzung senden

Text steht in `demo/whatsapp-marcel-2026-07-06.md` als „Update-
Nachricht 2026-07-07". Kopieren und an Marcel senden.

### Priorität 2: Domain-Verfügbarkeit MyBeautyKey.de prüfen

Parallel zur Marcel-Rückmeldung. Falls belegt: Alternativen sammeln
und Thomas zur Auswahl geben.

### Priorität 3: Bei positivem Feedback — Whitelabel-Grundgerüst starten

- Route-Group `src/app/(whitelabel)/` im bestehenden Repo
- Fragebogen aus `src/data/questions.ts` kopieren, MONAT-Vokabular raus
- Ergebnisseite markenneutral (Bedarfsprofil, kein Produkt)
- Regel-Engine wiederverwenden — sie liefert das Bedarfsprofil
- Details in `SAAS_BACKLOG.md` Kapitel 3

Realistischer Zeitrahmen (Backlog): ~14–18 Bau-Tage für Basic-Launch
inkl. ausgegrautem Pro-Dashboard.

## Konvention hinzugekommen (für spätere Sessions)

- **Keine Haftungs-Aussagen in Sina/Marcel-Dokumenten.** „Kein Risiko
  fürs Team" war zu weit — ab Pro haftet die Beraterin für die Content-
  Aussagen ihrer Bibliothek. Statt Haftungs-Versprechen: positive,
  ehrliche Vorteile („Alles in Beraterin-Hand", „Skalierbar über
  Team-Code" etc.).
- **Free-Tarif und öffentliche Demo koexistieren.** Free = eigener
  Test-Zugang, Demo = Vorschau auf Pro-Funktionen. Sie ersetzen sich
  nicht gegenseitig.
- **Missverständnis-Prävention aktiv testen.** Bei jeder größeren
  Konzept-Änderung fragen: „Wie liest sich das für jemanden, der die
  Diskussion nicht mitgemacht hat?" Beispiel dieser Session: Der
  markenneutrale Ansatz klang wie „nur noch Bedarfsanalyse" — die
  Klarstellung „vollständige MONAT-Empfehlung bleibt möglich" musste
  extra vorne eingesetzt werden.
