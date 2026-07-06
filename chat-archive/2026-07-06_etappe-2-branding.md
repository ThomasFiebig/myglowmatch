# Session 2026-07-06 (2) — Etappe 2: Dashboard-Branding-Bereich gebaut

**Fortsetzung der Business-Track-Session vom selben Tag** (`2026-07-06_konzept-landing.md`).
Frische Session, weil Konzept-Landing + Antragsschreiben abgeschlossen waren und
Etappe 2 laut Wiedereinstieg-Prompt bewusst als 1–2h-Feature-Arbeit eingeplant war.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-06_etappe-2-branding.md`, `SAAS_BACKLOG.md` und
> `demo/BUILD_SPEC.md`. Nächster Schritt hängt an Namensfreigabe + MONAT-DACH-
> Ansprechpartner. Sobald Rückmeldung kommt: Adressat-Platzhalter in beiden
> Anschreiben ersetzen, PDFs neu generieren, `public/konzept/`
> synchronisieren, ggf. Domain-Umbenennung starten. Business-Track sonst
> ruhig — nächste Bau-Aktion erst nach Namensfixierung.

## Stand am Ende der Session

- **Etappe 2 fertig:** Branding-Bereich im Dashboard komplett — Portrait,
  Farbwelt (6 Pastell-Töne), Grußformel + Vorstellungstext, Deckblatt-Wahl
  (4 Presets + Custom-Slot), zweigeteilte Live-Vorschau (Fragebogen-Deckblatt
  + Empfehlungs-Mail), Basic↔Pro-Toggle mit Sperr-Overlay + Upgrade-CTA.
- **Landing-Kachel aktualisiert:** „Update in Arbeit"-Hinweis auf Kachel 05
  (Dashboard-Demo) durch „Neu · Branding-Bereich"-Beschreibung ersetzt.
- **Zwei Datei-Kopien synchron:** `demo/partner-portal.html` und
  `public/konzept/partner-portal.html` sind identisch (1080 Zeilen).
- **Commits gepusht:** `8c135c6` (feat: Branding-Bereich) auf `main`,
  Vercel-Deployment ausgelöst.

## Was gebaut wurde

### Struktur der neuen Branding-View

Linke Spalte (`col-5`), vier Cards untereinander:

1. **Grundlagen** (immer editierbar, Basic + Pro):
   Portrait-Upload · Anzeige-Name · Slogan · Signatur-Zeile ·
   Kontakt-E-Mail · Telefon/WhatsApp

2. **Farbwelt** (Pro-Card mit `.pro-lock`):
   Sechs Swatches — Rosé (Default) · Peach · Mint · Powder · Vanille ·
   Terracotta. **Kein Lila/Lavendel** (Compliance § 3 BUILD_SPEC).

3. **Persönliche Ansprache** (Pro):
   Grußformel-Input („Herzlich willkommen") · Vorstellungstext-Textarea.

4. **Deckblatt-Design** (Pro):
   Vier Presets als Vorschau-Kacheln — Rosé-Verlauf · Minimal-Champagne ·
   Elegant-Dunkel · Natur-Sage. Fünftes Kachel-Feld voller Breite als
   Custom-Upload-Slot.

Rechte Spalte (`col-7`), zwei Cards:

1. **Vorschau · Fragebogen-Deckblatt** — reagiert auf Palette (accent-Button),
   Deckblatt-Design (Hintergrund-Verlauf), Grußformel, Vorstellungstext,
   Portrait-Initialen aus Name.

2. **Vorschau · Empfehlungs-Mail** (bestehende Mail-Preview) — reagiert auf
   Palette (Hero-Gradient, Step-Chip, Partner-Card, Portrait-Kreis),
   Anzeige-Name, Signatur-Zeile.

### Basic/Pro-Gating (Demo-Umschalter)

Toggle oben rechts in der Branding-View (nur im Mockup — keine echte Tier-
Persistenz). Bei „Basic-Ansicht" bekommen alle drei Pro-Cards ein
Sperr-Overlay:

- Weißes Overlay mit `linear-gradient(180deg, rgba(255,255,255,.75) 0%,
  rgba(255,255,255,.96) 55%)`
- Zentrierter Lock-Icon + Titel + Kurztext + „Auf Pro upgraden"-Button
- Unterliegende Felder ausgegraut via `opacity:.45; filter:saturate(.6);
  pointer-events:none`

Zeigt Sina bzw. dem Downline-Publikum sofort, was ein Basic-Abo blockiert.

### Palette-Umsetzung

Rose = Default (via bestehendes CSS). Fünf weitere Paletten als Overrides
auf `.mail-preview-wrap.pal-XXX`:

- Peach — `#fbe4d4 / #e39a72 / #b6764a`
- Mint — `#e2f0e8 / #8ab89b / #5a7d64`
- Powder — `#e0eaf3 / #8ea8c2 / #5a7591`
- Vanille — `#f8ecc9 / #d4b96a / #9a7a2f`
- Terracotta — `#ecd0c2 / #b0745a / #8a5236`

Nur Mail-Hero, Step-Chip, Partner-Card + Portrait-Kreis werden gefärbt.
Body-Text, Divider, Footer bleiben neutral (weniger Angriffsfläche für
schlechte Palette-Wahl, plus Lesbarkeit).

### Deckblatt-Presets

Vier `.style-XXX`-CSS-Klassen mit voller Verlaufs-Definition:

- `style-rose` — Champagne → Rosegold → Kupfer (Default)
- `style-minimal` — Champagne → Blush (fast einfarbig)
- `style-elegant` — Anthrazit → Grau (dunkle Karte, heller Text)
- `style-natur` — Sage-Verlauf (grün-neutral)

Custom-Slot zeigt aktuell nur Upload-Hint (kein FileReader — reines Mockup).

### Live-Vorschau-Verdrahtung

Fünf Event-Listener via `bindLive()`:

- `brand-name` → `cp-name`, `mp-name`, `cp-portrait`, `mp-portrait`,
  `portrait-preview` (Initialen aus Vor- + Nachname)
- `brand-slogan` → `cp-slogan`
- `brand-gruss` → `cp-greeting`
- `brand-intro` → `cp-intro`
- `brand-signatur` → `mp-contact`

## Bewusste Design-Entscheidungen

### Palette getrennt vom Deckblatt-Design

Palette (6 Pastell-Töne) = accent-Farbe über alle Touchpoints hinweg.
Deckblatt-Design (4 Presets) = spezifischer Look der Fragebogen-Titelseite.
**Beide unabhängig wählbar** — Beraterin kann z. B. Peach-Palette + Elegant-
Dunkel-Deckblatt kombinieren. Beobachtete Sina-Argument: mehr Kombinations-
Freiheit erhöht das Gefühl von Personalisierung, ohne Wildwuchs zu
riskieren (24 gesamte Kombinationen bleiben marken-safe).

### Palette wirkt nicht auf gesamte UI

Der Portal-Chrome (Sidebar, KPI-Cards, Buttons) bleibt in myglowmatch-Rosé,
egal welche Palette gewählt ist. Nur die **Kundinnen-Sicht** (Deckblatt +
Mail) ändert die Farbe. Grund: sonst wären alle Screenshots des Portals
inkonsistent, wäre Support-belastend („warum sieht mein Portal anders aus
als in der Anleitung?").

### Basic-Sperre als Overlay statt Ausblendung

Basic-Ansicht zeigt die Pro-Sektionen sichtbar mit Overlay, nicht komplett
verschwunden. Verkaufspsychologisch bewusst gewählt (steht so auch im
SAAS_BACKLOG § 2): Basic-Partnerin sieht ständig, was sie verpasst.

### Portrait bleibt Basic-Feature

Auch wenn Portrait Teil der „Personalisierung" ist — Grundlagen-Card ist
komplett Basic. Portrait ist Minimalvoraussetzung, damit die Beraterin
überhaupt als Person auftritt. Farbwahl / Grußformel / Deckblatt-Wahl sind
das echte Upgrade-Argument.

## Neue Artefakte

- `demo/partner-portal.html` (1080 Zeilen, +295)
- `public/konzept/partner-portal.html` (Spiegel)
- `public/konzept/index.html` — Kachel-05-Hinweis aktualisiert
- `chat-archive/2026-07-06_etappe-2-branding.md` (diese Doku)

## Git-Commits (auf `main`, gepusht)

- `8c135c6` feat(dashboard-demo): Etappe 2 — Branding-Bereich mit Pro-Gating
- Landing-Kachel-Update + Session-Doku folgen als eigener Commit

## Offene Nachzieh-Punkte für den Live-Bau (post-MVP)

- Portrait-Upload-Backend (aktuell nur UI-Slot, kein FileReader/S3-Wire)
- Custom-Deckblatt-Upload-Backend (dito)
- Palette-Persistenz in `partner`-Tabelle (`palette` als Enum-Feld)
- Deckblatt-Design-Persistenz (`cover_style` als Enum-Feld + optional
  `cover_custom_url`)
- `greeting_line` und `intro_text` als Felder in `partner`-Tabelle
- Node 17 muss Deckblatt-Style + Palette bei Mail-Render berücksichtigen
- Fragebogen-Route (`src/app/[partner]/page.tsx`) braucht neuen Header
  mit Grußformel + Vorstellungstext, wenn `tier === 'pro'`

Diese Punkte gehören zum späteren Bau nach MONAT-Freigabe — hier als
Sammel-Liste dokumentiert, damit sie beim Live-Umbau nicht verloren gehen.

## Bewusst NICHT in dieser Session gemacht

- **Palette-CSS-Vars auf Portal-Chrome ausrollen** — bewusst enger Scope
  (nur Kundinnen-Sicht ändert Farbe, siehe Design-Entscheidung oben).
- **Echte Datei-Uploads** — Mockup-Status reicht für Sina/Marcel-
  Vorstellung.
- **HANDOVER.md-Update** — HANDOVER bleibt weiter der n8n/Regel-Engine-
  Faktografie vorbehalten; SaaS-Track dokumentiert sich in
  `SAAS_BACKLOG.md` + `chat-archive/`.
- **SAAS_BACKLOG-Status-Update auf „Etappe 2 erledigt"** — folgt in
  Housekeeping-Commit direkt nach dieser Doku (siehe unten).

## Folgepunkte für nächste Session

### Priorität 1: Namensfreigabe + Ansprechpartner-Info von Sina/Marcel

Sobald die Info kommt:
- Adressat-Platzhalter in beiden Anschreiben ersetzen
- PDFs neu generieren
- `public/konzept/` synchronisieren
- Ggf. Domain-Umbenennung starten (falls Name wechselt)

### Priorität 2: SAAS_BACKLOG-Statusfeld für Etappe 2 auf „erledigt"

Aktuell steht dort noch „Etappe 2 aktuell offen". Nach dieser Session
sollte das auf „Etappe 2 als Demo-Mockup fertig, Live-Bau nach MONAT-
Freigabe" umgestellt werden.

### Priorität 3: Business-Track sonst ruhig

Bis Namensfreigabe kein sinnvoller Bau-Schritt am kommerziellen Track.
n8n-Track (HANDOVER.md) läuft parallel weiter.
