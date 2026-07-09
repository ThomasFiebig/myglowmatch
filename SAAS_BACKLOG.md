# SAAS_BACKLOG — myglowmatch / VERADEX

**Zweck:** zentrale Referenz für alle Business-Track-Entscheidungen zum SaaS-Vertrieb.
Getrennt von `HANDOVER.md` (n8n / Regel-Engine) und `demo/BUILD_SPEC.md` (End-Zustand
für Partner).

**Stand:** 2026-07-08 spät (Cloud-Toolchain bestätigt, Google Sheets aus
Laufzeit-Kette, Zielgruppen-Erweiterung als Compliance-Firewall dokumentiert,
Datenmodell-Skizze Multi-Tenant als Kapitel 3.6 ergänzt).

**Rollen:**
- **Desirée Fiebig** (MONAT-Markenpartnerin Nr. 14038921) — fachliche und technische
  Owner:in: baut, verwaltet, entscheidet inhaltlich.
- **Thomas Fiebig / VERADEX** (MONAT-Markenpartner Nr. 14074120) — rechtliche Hülle:
  Vertragspartner der Beraterinnen, Rechnungsstellung, DSGVO-Verantwortlicher,
  kaufmännischer Betrieb.

---

## 0 — Strategie-Umkehr 2026-07-06 spät (aktive Strategie)

**Auslöser:** Marcels Freund (Rechtskenntnis) sagt: MONAT wird die Freigabe
für ein Fremdanbieter-Tool mit MONAT-Marken-Nennung nicht erteilen (Kern-Argument:
MONAT kontrolliert Distributionswege eng, hat null Interesse an Dritten die
„mitverdienen"). Realistische Freigabe-Wahrscheinlichkeit: 15–30 %.

**Neue Strategie: markenneutrale Beratungs-Software (Weg A-hart mit
Beraterin-eigener Produkt-Bibliothek).**

**Kernidee:**
- **Kundinnenseite ist markenneutral** — Ergebnis zeigt nur **Bedarfe**
  („feuchtigkeitsspendendes Shampoo für dickes Haar", „Hitzeschutz wichtig",
  „Volumen-Styling"), keine Markennamen, keine Produktnamen
- **Beraterin pflegt in ihrem privaten Portal eine eigene Produkt-Bibliothek**
  — jede Beraterin trägt ihre eigenen Sortiments-Produkte ein (kann MONAT,
  Younique, Mary Kay, Kevin Murphy, eigenes Coiffeur-Sortiment sein)
- **System matched Bedarfe auf die Beraterin-eigenen Produkte** und zeigt ihr
  die konkreten Empfehlungen für ihre Beratungsarbeit
- **`warum_sinnvoll`-Argumente schreibt die Beraterin selbst** — Freitext pro
  Produkt, keine automatisierten Zitate aus fremden Datenblättern

**Rechtliche Konsequenz für VERADEX:**
- Kein MONAT-Name im System — § 3.2.1, § 3.2.5, § 3.6.1 alle nicht mehr
  einschlägig
- VERADEX ist reiner Infrastructure-Anbieter (wie ein CRM oder Notiz-Tool)
- Content-Verantwortung liegt bei der Beraterin (sie tippt die Produkte selbst
  ein, sie empfiehlt sie der Kundin persönlich)
- **Kein MONAT-Antrag mehr nötig** — VERADEX-Anschreiben + Sinas Vorspann
  bleiben als „nicht abgesendet, aufbewahrt" liegen für den Fall eines späteren
  MONAT-Deals (Weg B)

**Sofort-Nutzbarkeit ohne Setup:**
- Beraterin kann direkt nach Buchung loslegen — Analyse-only-Modus zeigt
  Bedarfe, Beraterin übersetzt persönlich in ihre Markenwelt
- Erst bei Pro-Upgrade lohnt sich das Anlegen der Produkt-Bibliothek

**Business-Vorteil:**
- Zielgruppe wächst um Faktor 20–50 (alle Beauty-Beraterinnen, nicht nur
  MONAT-Partnerinnen)
- Keine Wartezeit auf MONAT-Freigabe → sofort startfähig nach Namens-Fix
- Bei späterem MONAT-Deal (Weg B): ihr verhandelt aus Position der Stärke
  (zahlende Kunden vorweisbar)

### Zielgruppen-Erweiterung und doppelte Motivation (Update 2026-07-08)

Offiziell beworben als **markenneutrales Haaranalyse-Tool** für Beauty-Profis
im DACH-Raum. Kern-Zielgruppen:

- Salons (Inhaberin + Team-Mitarbeiter, ab V2 Seat-basiert)
- Solo-Hair-Artists und Make-up-Artists
- Beauty-Studios
- MLM-Vertriebspartnerinnen (als **eine von vielen** Anwendungsgruppen,
  nicht als beworbene Kern-Zielgruppe)

**Doppelte Motivation für die breite Aufstellung:**

1. **Marktgröße** — TAM steigt um Faktor 50–100 gegenüber „nur
   MONAT-Beraterinnen". Instagram-Ads-Kampagnen sind für „Beauty-Profis"
   ansprechbarer als für ein enges MLM-Segment.
2. **Compliance-Firewall gegen MONAT-§3.2.1-Argument** — wenn wir öffentlich
   und in allen Marketing-Kanälen als generisches Haaranalyse-Tool
   auftreten, kann MONAT nicht plausibel behaupten, VERADEX habe „ein Tool
   speziell für unsere Vertriebsstruktur gebaut, um am Umsatz mitzuverdienen".
   Das ist die Kehrseite von Kapitel 2.6: nicht nur der Code muss neutral
   sein, auch die **Außendarstellung** entzieht der Marken-Attacke die
   Angriffsfläche.

Konsequenz für Marketing und Landingpage: Sina/Marcel-Kontext ist interne
Positionsklärung, aber die öffentliche Positionierung nutzt keine
MLM-Sprache und keinen MONAT-Bezug. Die MLM-Fähigkeit wird als eine
Anwendung neben Salon, Solo-Artist, Studio erwähnt — nicht in der Headline.

Skin-Analyse als V2-Erweiterung mitdenken (Datenmodell so bauen, dass eine
zweite Analyse-Domäne andockbar ist), aber nicht V1 bauen. Siehe Kapitel 3.6.

**Aufwand für Umstellung des gebauten Systems:**
- Regel-Engine (Node 04–15): bleibt zu 90 % identisch, arbeitet mit Bedarfsprofil
  statt konkreten Produkten
- Node 17 (E-Mail-Rendering): Umbau auf Bedarfsdarstellung + Beraterin-eigene
  Produktnamen (falls Pro-Modus)
- Frontend: neuer Bibliothek-Bereich im Beraterin-Portal (Etappe 2)

---

## 0.5 — Projektstruktur (Empfehlung)

Neuer markenneutraler Bau als **Route-Group im bestehenden Repo**:

```
myglowmatch/
├── src/app/
│   ├── (monat)/           # bestehendes MONAT-System (bleibt für n8n-Test aktiv)
│   └── (whitelabel)/      # NEU — markenneutrale Version
```

Vercel deployed weiterhin ein Projekt. Später (nach ersten zahlenden Kunden)
kann in eigenes Repo gesplittet werden via git-filter-repo.

Alternative: separates Repo `mybeautykey` (falls Verkauf/Lizenzierung in
Aussicht) — für den Start Overkill.

---

## 1 — Preismodell (nach Strategie-Umkehr 2026-07-06 spät)

| | Monat | Jahr | Setup einmalig |
|---|---|---|---|
| **Free** | 0 € | 0 € | 0 € |
| **Basic** | 9,90 € | 99 € | 29,90 € (entfällt bei Jahresabo) |
| **Pro** | 19,90 € | 199 € | 29,90 € (entfällt bei Jahresabo) |

Alle Preise brutto inkl. 19 % USt. Rechnungsstellung durch VERADEX via Stripe.

**Begründung Preisreduktion gegenüber MONAT-Konzept-Preis (14,90/29,90):**
Beraterin muss ihre Produktbibliothek selbst pflegen — weniger Auto-Magie
für sie, entsprechend niedrigerer Preis fair. Kompensation über größere
Zielgruppe (jede Beauty-Beraterin, nicht nur MONAT).

**Free-Tier — Umfang und Limits:**
- Analyse-only: Beraterin bekommt persönlichen Link, Kundinnen können
  Fragebogen ausfüllen, Ergebnis zeigt nur Bedarfe
- Limit: 2 Beratungen pro Monat (Rechenzeit-Schutz gegen Missbrauch)
- Keine Beratermail, keine persistenten Kundinnen-Daten
- Upgrade-Prompt bei Erreichen des Limits

**Setup-Fee-Logik:** einheitlich 29,90 € für Basic und Pro. Reduziert
gegenüber 49,90 € des MONAT-Konzepts, weil Einrichtung pro Beraterin
schlanker (keine Marken-Verifikation nötig, keine individuelle Konfiguration).

**Jahresabo:** kein zusätzlicher Monatsrabatt, nur Setup-Erlass. Ersparnis
gegenüber Monatsabo mit Setup: ~25 %. Klares Verkaufsargument.

**Break-Even-Rechnung für VERADEX:**
Bei 30 aktiven Basic-Downlines aus Sinas Team (297 €/Monat MRR) plus
5 Pro-Upgrades (99,50 €/Monat MRR) = ~400 €/Monat MRR aus dem Sina-Kanal
allein. Bei praktisch null Betriebskosten (Vercel Free-Tier, Supabase
Free-Tier, Anthropic API pay-per-use im Cent-Bereich pro Analyse) ist das
schnell profitabel.

---

## 2 — Feature-Split Free / Basic / Pro (neu nach Strategie-Umkehr)

| Funktion | Free | Basic | Pro |
|---|---|---|---|
| Fragebogen + Analyse-System für Kundinnen | ✓ | ✓ | ✓ |
| Ergebnisseite im Browser (Endkundin) — markenneutral, nur Bedarfe | ✓ | ✓ | ✓ |
| PDF-Download der Ergebnisseite für Kundin | ✓ | ✓ | ✓ |
| Persönlicher Beratungs-Link (`[name].de/[Beraterin]`) | limit 3/Monat | ✓ | ✓ |
| WhatsApp-Kontakt-Button zur Beraterin | — | ✓ | ✓ |
| Beratungs-Mail an die Beraterin nach jeder Analyse | — | ✓ | ✓ |
| Portal-Zugang mit Stammdaten (Name, Kontakt, Rechnung) | — | ✓ | ✓ |
| Kundinnen-Übersicht (letzte 10) im Portal | — | ✓ | ✓ |
| **Eigene Produkt-Bibliothek** (Beraterin trägt Sortiment ein) | — | — | ✓ |
| **Kundinnenseite zeigt konkrete Produktnamen** (aus Beraterin-Bibliothek) | — | — | ✓ |
| **`warum_sinnvoll`-Freitext** pro Produkt (Beraterin schreibt selbst) | — | — | ✓ |
| **Team-Sharing** — Bibliothek als Vorlage freigeben + Team-Code an Downlines | — | — | ✓ |
| **Team-Vorlage übernehmen** beim Setup per Team-Code (Kopie, kein Live-Sync) | — | — | ✓ |
| Vollständiges Dashboard mit allen Beratungen | — | — | ✓ |
| Branding-Bereich (Portrait, Farbwahl inkl. Pastellpalette, Grußformel, Deckblatt-Austausch) | — | — | ✓ |
| Push-Benachrichtigung aufs Handy | — | — | ✓ |
| Dashboard als App auf den Homebildschirm installieren (PWA) | — | — | ✓ |
| Zustellungs-Toggle (Mail / Push / nur Dashboard) | — | — | ✓ |
| **Follow-up-Kennzahlen** (Selbstauskunft der Beraterin, keine Kundinnen-PII) | — | — | ✓ |

**Follow-up-Kennzahlen — Design-Entscheidung 2026-07-08 spät**
Die Kennzahlen „Follow-ups offen" und „Follow-up-Quote" (Warenkorb →
Bestellung) im Dashboard beruhen ausschließlich auf **Beraterin-
Selbstauskunft**: pro Lead klickt die Beraterin manuell „Warenkorb
versendet" und/oder „Bestellt". Das System aggregiert nur diese Ticks.
Kein automatisches Tracking, keine Speicherung von Kundinnen-Verhalten,
kein Marketing-Attribution-Kram. Damit bleibt das „Endkundinnen-Daten
werden nicht persistiert"-Prinzip aus Kapitel 3.6 unverletzt, während
die Beraterin trotzdem ihre Conversion-Rate sieht. Datenmodell-Detail
siehe Kapitel 3.6, Tabelle `lead_status`.

**Kernunterschied Basic ↔ Pro (neu):**
- **Basic:** Kundinnen sehen Bedarfe („feuchtigkeitsspendendes Shampoo für
  dickes Haar"), Beraterin übersetzt persönlich in ihre Markenwelt
- **Pro:** Kundinnen sehen konkrete Produkte aus der Beraterin-eigenen
  Bibliothek („MONAT Renew Shampoo, weil…") — voll automatisiert

**Basic-Portal:** die Pro-Bereiche sind sichtbar, aber deaktiviert (ausgegraut
mit Upgrade-CTA). Verkaufspsychologisch stark — Basic-Beraterin sieht ständig,
was sie verpasst.

**Upgrade / Downgrade:**
- Upgrade jederzeit möglich, bezahlte Gebühren werden anteilig verrechnet
- Downgrade: keine Erstattung. Pro läuft ab bezahltem Zeitraum weiter und
  wechselt danach in Basic. Produkt-Bibliothek-Daten werden „eingefroren"
  (30 Tage Reaktivierungs-Fenster, DSGVO-Balance).

---

## 2.5 — Team-Sharing (Pro-Feature, kein extra Tier)

**Kernidee:** Uplines pflegen ihre Produkt-Bibliothek einmal, ihre Downlines
können sie als Startvorlage übernehmen. Reduziert die Onboarding-Hürde für
Neu-Downlines von 45–90 Minuten auf 30 Sekunden.

**Design-Prinzip: „Kopie beim Setup, Pull statt Push".**
- Upline generiert im Portal einen 8-stelligen Team-Code (z. B. `SINA-2M8K`)
- Downline gibt bei Setup den Code ein → Bibliothek wird **einmal kopiert**
- Ab dann: eigene Bibliothek, unabhängig von der Upline
- Bei Upline-Änderungen: Downline bekommt Notification „N Änderungen bei
  deiner Upline. Willst du sie übernehmen?" — aktives Ja/Nein, kein Auto-Sync

**Warum Pull statt Push:**
- Wenn Live-Sync: VERADEX würde MONAT-Marken automatisch an mehrere
  Downlines verteilen — Compliance-Risiko, weil VERADEX zum Content-
  Distributor wird
- Bei Kopie + aktivem Übernehmen: Content-Verantwortung wandert bei jedem
  Klick von Upline zu Downline. VERADEX bleibt neutrale Infrastruktur
- Rechtlich äquivalent zu „Excel-Vorlage weitergeben"

**Setup-Wege für Neu-Beraterinnen (drei Optionen im Onboarding):**
1. **Leer starten** — komplett eigene Bibliothek aufbauen
2. **Team-Vorlage übernehmen** — Team-Code eingeben, Bibliothek einmalig
   kopiert
3. **CSV-Import** — für Beraterinnen mit eigener Excel-Liste

**Upline-Portal-Zusätze:**
- Toggle „Als Team-Vorlage freigeben" pro Produkt oder pro Bibliothek
- Sichtbar: „N Downlines nutzen deine Vorlage" (rein zählend, keine
  Personennennung)
- Beim Aktualisieren: Broadcast-Notification an aktive Team-Mitglieder

**Preismodell-Konsequenz:** kein Aufpreis. Standard-Pro-Feature (19,90 €/Monat).
Grund: senkt die Neu-Downline-Barriere massiv → mehr Basic/Pro-Kunden im Team
→ mehr Umsatz für VERADEX. Team-Manager-Tier mit Analytics („welche meiner
Downlines nutzt was am meisten") als möglicher V2-Aufsatz.

**Rechtliches Detail:** beim Übernehmen einer Team-Vorlage bestätigt die
Downline aktiv „ich übernehme das Sortiment als eigene Empfehlung". Damit
wandert die Content-Verantwortung auf sie. AGB-Formulierung dazu vor Launch
finalisieren.

---

## 2.6 — Compliance-Absicherung Whitelabel (kritisch vor Launch)

**Grundprinzip:** VERADEX ist neutraler SaaS-Anbieter analog Salesforce,
Notion, Airtable. Wir speichern User-Generated Content der Beraterinnen. Sie
haften für ihre Markenreferenzen, wir für die Plattform-Neutralität. Diese
Position ist rechtlich tragfähig (§ 10 TMG „Speicherung von Informationen"
plus Standard-SaaS-Praxis), **wenn** wir drei Fallen konsequent vermeiden.

### Die drei Fallen und wie wir sie vermeiden

**Falle 1 — Vorbelegte Bibliotheken mit MONAT-Produkten**
Wenn wir eine fertige „37-Produkte-MONAT-Sortiment-Vorlage" zum Import
anbieten, sind wir aktiver Distributor → Markenverletzung.

*Absicherung:*
- Bibliothek startet immer **komplett leer**
- Kein Autocomplete oder Vorschlagsliste mit Markennamen
- Kein „Standard-Sortiment"-Import einer bestimmten Marke
- Beraterin muss jeden Produktnamen selbst tippen (oder eigenen CSV-Import)

**Falle 2 — Kundinnenseite mit Markennamen auf VERADEX-Domain**
Wenn die Kundin auf `[name].de/[Beraterin]` MONAT-Produktnamen sieht, könnte
MONAT argumentieren, VERADEX-Plattform verbreitet ihre Marke.

*Absicherung:*
- **Beraterin-Attribution prominent** auf jeder Kundinnen-Ergebnisseite
  („Diese Empfehlung ist von Sina Hildmann für dich zusammengestellt.")
- Damit ist rechtlich klar: Beraterin ist Autorin, VERADEX ist
  Anzeige-Infrastruktur
- Kundinnenseite hat ein sichtbares Impressum, aus dem klar wird: Beraterin
  ist Content-Verantwortliche, VERADEX ist Plattform-Betreiber

**Falle 3 — Team-Sharing als aktive Distribution**
Bei sehr großen Netzwerken (>50 Downlines pro Upline) könnte MONAT
argumentieren, VERADEX-Infrastruktur verbreitet Marken systematisch.

*Absicherung (siehe auch Kapitel 2.5):*
- Pull statt Push — Downlines übernehmen aktiv, kein Auto-Sync
- Bei jedem Übernehmen aktive Content-Bestätigung („Ich übernehme dieses
  Sortiment als meine eigene Empfehlung")
- Content-Verantwortung wandert bei jedem Klick

**Falle 4 — Einrichtungsservice (Update 2026-07-08)**
Wenn VERADEX als bezahltes Setup-Feature MONAT-Datenblätter der Beraterin
ins System einpflegt, könnten wir als aktiver Content-Distributor gelten
— trotz „im Auftrag der Kundin".

*Absicherung:*
- Der Einrichtungsservice verarbeitet **ausschließlich vom Kunden
  hochgeladenes Material** (PDFs, CSVs, Fotos) — nie vorgefertigte
  Marken-Kataloge aus VERADEX-Vorrat
- Buchungsstrecke fordert Upload explizit: „Lade deine Produktdaten oder
  Datenblätter hoch, wir übernehmen die Eingabe"
- Ergebnis landet zunächst im **Draft-Status** (nicht live sichtbar)
- Die Kundin sieht Preview des eingepflegten Katalogs
- **Aktiver Freigabe-Klick** durch die Kundin schaltet den Katalog live
  — dieser Klick ist gleichzeitig **Content-Verantwortungs-Übernahme**
- Content-Freigabe wird mit Zeitstempel, User-ID und AGB-Version
  protokolliert (siehe Kapitel 3.6, `consent_log`-Tabelle)
- Rechteversicherung beim Upload: Häkchen „Ich habe die Rechte, dieses
  Material zu verwenden und stelle VERADEX von Ansprüchen frei"

Ohne diesen Freigabe-Schritt wäre VERADEX Distributor. Mit dem Schritt
wandert die Content-Verantwortung dokumentiert auf die Kundin.

### Absicherungs-Checkliste vor Launch

**Technisch (im System):**
- Bibliothek startet leer, keine markenspezifische Vorbelegung
- Kein Autocomplete/Vorschlagsliste mit Markennamen
- Kundinnenseite mit prominenter Beraterin-Attribution + Impressum-Verweis
- Takedown-Endpoint für Marken-Beschwerden (E-Mail-Adresse im Impressum)
- Team-Sharing-Übernahme mit expliziter Content-Akzeptanz-Klick

**Vertraglich (AGB + Beraterin-Onboarding):**
- AGB-Klausel: „Content-Verantwortung liegt bei der Beraterin"
- AGB-Klausel: „Beraterin ist berechtigt, die eingepflegten Marken/Produkte
  zu verwenden (z. B. als Vertragspartnerin der Marke)"
- AGB-Klausel: „VERADEX ist neutraler Infrastruktur-Anbieter im Sinne
  § 10 TMG"
- AVV (Auftragsverarbeitungsvertrag) mit jeder Beraterin für DSGVO-Basis
- Bei Team-Sharing-Übernahme: separater Akzeptanz-Klick mit
  Content-Verantwortungs-Übernahme

**Marketing (öffentliche VERADEX-/Whitelabel-Kommunikation):**
- Landing-Seite markenneutral
- Kein „für MONAT-Beraterinnen" oder ähnliche Marken-Bezüge in Werbetexten
- Keine MONAT-Logos, keine Screenshots mit konkreten Marken-Produkten
- Testimonials / Case Studies ohne Markennamen der Sortimente

### Rechtsposition gegenüber MONAT bei Beschwerde

Wenn MONAT (oder eine andere Marke) sich beschwert, argumentieren wir:

> „VERADEX ist neutraler SaaS-Anbieter analog Salesforce oder Notion. Wir
> speichern User-Generated Content unserer Nutzerinnen (Beraterinnen). Die
> Content-Verantwortung liegt vertraglich bei den Nutzerinnen, die uns
> gegenüber die Berechtigung zur Verwendung der jeweiligen Marken zugesichert
> haben. Bei berechtigter Beschwerde einer Marke entfernen wir betroffene
> Inhalte im Rahmen unseres Takedown-Prozesses."

Diese Position vertreten Salesforce, Notion, Airtable, HubSpot mit Erfolg.

### Takedown-Prozess (§ 10 TMG-Standardpraxis)

Damit die neutrale-Plattform-Position tragfähig bleibt, muss ein
funktionierender Takedown-Prozess vor Launch stehen:

- **Takedown-Adresse** `takedown@[domain]` (oder `notice@`) prominent im
  Impressum
- **Bearbeitungs-SLA:** 48 Stunden ab Eingang einer begründeten
  Markenbeschwerde bis zur Sperrung des betroffenen Inhalts
- **Interne SOP**: dokumentierter Ablauf — Eingang → Prüfung
  Beschwerde-Substanz → Sperr-Aktion in Supabase (Feld `product.aktiv =
  FALSE` oder `catalog.blocked_at`) → Benachrichtigung an Kundin mit
  Widerspruchsmöglichkeit → Log-Eintrag
- **Sperr-Endpoint im Backend:** Admin-Funktion (nicht öffentlich), die
  eine einzelne `product`-Zeile oder einen ganzen `product_catalog`
  binnen Sekunden aus allen Kundinnenseiten entfernt
- **Notice-and-Counter-Notice:** die Beraterin kann der Sperrung
  widersprechen, dann prüfen wir erneut oder verweisen an eine
  Streit-Beilegungs-Stelle

Ohne diesen Prozess ist die § 10 TMG-Position nicht verteidigbar, weil
wir dann kein „unverzüglich" mehr im Sinne des Gesetzes zeigen können.

### Grauzone — Anwaltscheck vor Launch nötig

Zwei Punkte bleiben rechtlich Grauzone und brauchen Prüfung:

1. **Kundinnenseite mit Markennamen auf VERADEX-Domain** — Safe-Argument
   durch Beraterin-Attribution ist stark, aber nicht bulletproof
2. **Team-Sharing mit sehr großen Netzwerken** — je größer, desto eher
   Argument „systematische Distribution"

**Absicherung:** einmaliger Anwaltscheck der AGB + der genannten Klauseln
vor dem ersten zahlenden Kunden. Kosten grob 300–600 €. Nicht heute
dringend — vor Launch aber Pflicht.

---

## 2.7 — Free-Modus Missbrauchs-Schutz

**Frage aus 2026-07-07:** wie verhindern wir, dass jemand das Free-Modul
(2 Beratungen/Monat, kein Login-Zwang) dauerhaft mit immer neuen
E-Mail-Adressen ausnutzt statt Basic zu buchen?

### Ökonomische Vorüberlegung — der stärkste Schutz

Bevor wir bauen: Beraterinnen sind kein Massen-Consumer-Publikum. Um 30
Beratungen dauerhaft gratis zu bekommen, braucht es 10 Fake-Accounts pro
Monat — jeder mit neuer Adresse, neuem Slug, neuer Beraterin-Persona,
Bibliothek-Setup (bei Pro-Versuch), Weiterleitung der Kundinnen zum neuen
Link. Ersparnis: 9,90 € Basic. **Aufwand pro Fake-Account übersteigt die
Ersparnis deutlich.** Zielgruppe kommt über Sina-Empfehlung, Reels,
Multi-Level-Netzwerke — nicht über Betrugsforen.

Konsequenz: technische Verteidigung nach Aufwand, nicht nach maximaler
Härte. Drei Ebenen, sortiert nach Kosten/Nutzen.

### Ebene 1 — Standard-Hürden (kostenlos, ~2 h Bau, bei Launch dabei)

- **E-Mail-Verifikation** — Klick-Link vor erster Beratung, sonst kein
  Free-Zugang. Filtert Trivial-Tippfehler und Copy-Paste-Fakes.
- **Wegwerf-Domain-Blocklist** — `disposable-email-domains` npm-Package
  (täglich aktualisiert). Schließt `10minutemail.com`, `guerrillamail`,
  `mailinator`, `tempmail`, etc. Free-Registrierung von diesen Domains
  wird abgelehnt mit sachlichem Hinweis „bitte eine dauerhafte Adresse".
- **Rate-Limit pro IP-Adresse** — max. 3 Neu-Registrierungen pro Woche
  pro IP. Standard-Middleware (Vercel Edge Rate-Limit oder Upstash
  Redis). Macht Massen-Setup unbequem, VPN-Hoppen kostet Zeit.

### Ebene 2 — Beraterin-Slug als natürlicher Anker (kein Extra-Bau)

Der persönliche Beratungs-Link `[name].de/[Beraterin]` erzwingt einen
Slug. Wer einen zweiten Free-Slot will, braucht einen zweiten Slug —
sichtbar in der URL, potenziell peinlich beim Weitergeben an Kundinnen.
„beauty-mit-lisa" ist einmal frei; „beauty-mit-lisa-2" wirkt unseriös.

**Regeln fürs Slug-Handling:**
- Numerische Suffixe (`-2`, `-3`, `foo123`) grundsätzlich reservieren und
  in der UI verweigern — Wahl eines echten Namens erzwingen
- Kollisions-Vorschläge nur mit Namens-Varianten (`beauty-lisa`,
  `lisa-beratung`), nicht mit Zahlen
- Slug einmal vergeben — bei Free-Konto-Reaktivierung wird der Slug frei
  nach 90 Tagen Inaktivität (DSGVO-Balance)

Das ist bereits Bestandteil des Konzepts, nur die Slug-Regeln müssen
beim Bau explizit umgesetzt werden.

### Ebene 3 — Fingerprint-Zusammenzug (bei Bedarf, nachträglich)

Server-seitiger Browser-Fingerprint (`fingerprintjs` open-source Version
oder eigene Kombination aus Canvas-Hash, Timezone, Language, Screen).
Wenn drei aktive Free-Accounts vom selben Fingerprint kommen: Zusammenzug
(alle drei zählen als ein Kontingent = 2 Beratungen gesamt statt 2 pro
Account) oder Sperre bei nachweislichem Muster.

**Bewusst nicht sofort einbauen:**
- Rechtsfrage — Fingerprinting fällt unter TDDDG § 25 (Cookie-Nachfolger)
  und braucht saubere Einwilligung oder Ausnahme-Begründung
- Aufwand ~1–2 Bau-Tage inkl. Datenschutz-Konsultation
- Erst aktivieren, wenn Logs echte Missbrauchs-Muster zeigen — sonst
  Overengineering und Rechtsrisiko ohne Gegenwert

### Bewusst nicht getan

- **Kreditkarten-Hinterlegung für Free** — würde die Kaufhürde für
  ehrliche Interessentinnen zerstören. Free verliert seinen Sinn.
- **SMS-/Handy-Verifikation** — Betriebskosten (~5 Cent pro SMS bei
  Twilio o. ä.), zusätzliche personenbezogene Daten, kaum Zusatz-Nutzen
  bei unserer Zielgruppe.
- **Captcha auf jedem Registrierungs-Schritt** — nervt ehrliche Nutzer
  mehr als Betrüger, wenige zusätzliche Sicherheit.

### Umsetzungs-Entscheidung

**Launch-Version:** nur Ebene 1 (E-Mail-Verifikation, Wegwerf-Blocklist,
IP-Rate-Limit) + strenge Slug-Regeln aus Ebene 2. Zusammen ~2–3 h Bau.
Ebene 3 als optionaler Add-on aus dem Backlog, aktiviert bei
messbarem Missbrauch nach Launch.

### Metriken für spätere Beurteilung

Nach Launch beobachten:
- Free-Accounts pro Woche pro IP-Bereich
- Free-Accounts pro Fingerprint (auch ohne Zusammenzug — nur zählen)
- Verhältnis Free → Basic-Upgrade (Zielrichtung 5–15 %, bei viel weniger
  Verdacht auf Ausnutzung ohne Kaufabsicht)
- Verhältnis Free-Beratungen zu tatsächlichen WhatsApp-Kontakten (bei
  echter Nutzung: hoch, bei Ausnutzung: null)

---

## 3 — Bau-Reihenfolge V0 / V1 / V2 (Master-Reihenfolge, Stand 2026-07-08 spät)

**Prinzip:** eine einzige Reihenfolge, an der du „was ist als nächstes"
ablesen kannst. Kapitel 3.5 (Tooling-Details) und 3.6 (Datenmodell) sind
Nachschlagewerke, keine parallelen Aufgabenlisten.

Realistischer Zeitrahmen zum Basic-Launch: **~14–18 Bau-Tage** ab V1-Start,
V0 läuft parallel als Vorarbeit.

### V0 — Infrastruktur & Recht (parallel zum Bau, muss vor Launch stehen)

Diese Punkte blockieren V1 nicht (außer 1 und 2), können also nebenher
laufen. Nummerierung nach Blocker-Wirkung und Wartezeit:

1. **Domain sichern** — `mybeautykey.de` oder Alternative bei Strato,
   sobald Sina/Marcel den Namen bestätigt haben. Blockiert V1.
2. **Namensfreigabe** durch Sina/Marcel (aktueller Vorschlag MyBeautyKey).
   Blockiert Punkt 1. Rückmeldung ausstehend.
3. **Supabase-Projekt in `eu-central-1`** anlegen (Region ist irreversibel,
   deshalb früh und richtig).
4. **Vercel-Deployment** WL-Route-Group auf Region `fra1` fixieren.
5. **Paddle-Account** anlegen + Business-Verifikation starten (~1 Woche
   Wartezeit, deshalb früh).
6. **DKIM/SPF/DMARC** für neue Domain bei Strato einrichten (aktueller
   HANDOVER-🔴-Blocker).
7. **Brevo-Account** anlegen, Domain verifizieren, API-Key in n8n binden.
8. **AVV-Muster** aus Bitkom-Vorlage vorbereiten (~60 Min).
9. **Datenschutzerklärung + Impressum + AGB** entwerfen (~3–4 h
   eigenständig).
10. **DPAs unterschreiben** — Vercel, Supabase, Paddle, Sentry, Brevo,
    Google Workspace.
11. **Anwaltscheck** der AGB/AVV/Compliance-Klauseln — ~300–600 €, muss
    vor erstem zahlenden Kunden abgeschlossen sein.

Detail-Konfiguration und DPA-Übersicht: siehe Kapitel 3.5.

### V1 — Feature-Fundament (verkaufsfähig, ~14–18 Bau-Tage)

1. **Whitelabel-Grundgerüst** als Route-Group `src/app/(whitelabel)/` im
   bestehenden Repo.
2. **Fragebogen** markenneutral aus bestehendem System übernehmen,
   MONAT-spezifische Vokabular-Referenzen entfernen (neue Version im
   whitelabel-Ordner, `src/data/questions.ts` bleibt).
3. **n8n-Workflow-Klon** `myglowmatch_wl` via API aufsetzen — separater
   Webhook, separater Datenbestand, Regel-Engine (Nodes 04–15) unverändert
   übernommen. Details in `chat-archive/2026-07-07_wl-adapter-isomorphie.md`.
   **✓ Erledigt 2026-07-08:** Klon live als `MyBeautyKey Whitelabel
   Beratungssystem v1.0` (ID `5lPLG0y235XiIpN1`, Webhook
   `mybeautykey-wl-haaranalyse`), `clone_workflow_wl.py` idempotent, MONAT-
   Workflow physisch unangetastet. Verifikation via 4× Regressions-Bulk
   0/76 Slot-Drift gegen frische MONAT-Baseline; siehe
   `chat-archive/2026-07-08_wl-klon-adapter.md`.
4. **Produktbibliothek + Auswertung gegen eigene Produkt-DB** —
   Beraterin-UI mit Chip-Formular (12 Felder), Adapter übersetzt in
   25-Spalten-Format (siehe `wl_adapter.py`), Matching gegen die
   organisationseigene Produktbibliothek in Supabase.
   **Teilstand 2026-07-08:** Adapter auf 11 Slot-Chips + `produktlinie`-
   Feld ausgerollt (Sub-Slot-Design final, Iso-Priorität 1 geschlossen).
   Persistenz als JSON-Fixture `wl_libraries/sina_monat.json` (37 Einträge)
   via `dump_wl_library.py`. Sync-Pipeline `sync_wl_produktdatenbank.py
   --source` speist den Klon-Node 08, verlustfrei belegt. Offen für V1:
   Beraterin-UI (Frontend) und Supabase-Persistenz-Schicht statt JSON-
   Datei. Mockup `demo/bibliothek.html` muss auf 27 Nutzen-Chips + 11
   Slot-Chips + Pflegelevel-Feld aktualisiert werden.
5. **CSV/Excel-Import** per Drag-and-drop mit fertiger Spaltenvorlage,
   ODER manuelle Produkt-Anlage im UI (Alternative-Weg).
6. **Multi-Tenant-Datenmodell** in Supabase mit RLS und Provenienz-Triggern
   umsetzen (siehe Kapitel 3.6).
7. **Ergebnisseite markenneutral** — Analyse-Engine liefert Bedarfsprofil
   plus (im Pro-Modus) Produktvorschläge aus der Beraterin-Bibliothek mit
   prominenter Beraterin-Attribution.
8. **Free-Modus** — Beraterin bucht kostenlos, bekommt Link, Limit
   2 Beratungen/Monat, Upgrade-Prompt bei Erreichen.
9. **Basic-Modus** — Portal mit Login, Beratermail, Kundinnen-Übersicht,
   ausgegraute Pro-Cards.
10. **Pro-Modus** — Produktbibliothek-UI voll aktiv, `warum_sinnvoll`-
    Freitext, Dashboard, Branding-Bereich, PWA, Push.
11. **Einrichtungsservice-Buchung** — Kunde lädt Material hoch, wir pflegen
    ein, Draft-Katalog → aktive Kunden-Freigabe (siehe Kapitel 2.6
    Falle 4).
12. **Teilen/Kopieren per Team-Code** — 8-stelliger Code, Downline
    übernimmt als Kopie (kein Live-Sync), aktive Content-Bestätigung beim
    Übernehmen (siehe Kapitel 2.5).
13. **Compliance-Guardrails im Code** — Beraterin-Attribution auf
    Kundinnenseite, Takedown-Endpoint (siehe Kapitel 2.6), Consent-Log für
    alle rechtserheblichen Zustimmungen.
14. **Paddle-Anbindung** — Free-Upgrade auf Basic, Pro-Buchung + Setup-Fee,
    Webhook-Automation zur Onboarding-Mail und Supabase-Insert.
15. **Öffentliche Demo** unter dem neuen Namen (`[name].de/demo`) mit
    Analyse-only-Beispiel und Fantasie-Bibliothek (siehe Session-Archiv
    2026-07-07 zum Zwei-Bibliotheken-Konzept).
16. **Übergabe der finalen Demo** an Sina und die ca. 10 Top-Leaderinnen.

### V2 — Nachrüsten (nach ersten zahlenden Kunden)

- **Team-/Multi-Seat-Modell** — Organisation → Mitglieder → Rollen
  (Owner/Admin/Member/Viewer), Lead-Zuordnung pro Login. Schema-Andockstelle
  in `user.role` und `organization.seat_limit` bereits vorbereitet (siehe
  Kapitel 3.6).
- **Pro-Seat- oder Staffel-Preise** — Salon abonniert, Mitarbeiter-Seats.
- **Skin-Analyse** als zweite Analyse-Domäne — Datenmodell trägt es bereits
  über `product_catalog.analysis_type`, es fehlt nur das zweite Regel-Set
  im n8n-Workflow und ein zweiter Fragebogen.
- **Regel-Admin-UI in Supabase** — wenn Regeln pro Kunde overridebar
  werden sollen oder häufigere Regel-Anpassungen nötig werden. V1 bleiben
  Regeln embedded im Workflow (via CSV im Repo).
- **Analytics und Auswertungen** für zahlende Kunden — welche
  Produkte am häufigsten empfohlen, welche Bedarfsprofile am häufigsten
  auftreten.
- **Meta-API-WhatsApp** — falls Beraterinnen doch geführten Nachrichten-
  Flow wollen (heute bewusst verworfen, siehe Kapitel 5).

### Historisch — Etappe 2 als Demo-Mockup erledigt (2026-07-06)

Branding-Bereich mit Portrait-Slot, Farbwahl (6 Pastell-Töne, kein Lila),
Grußformel + Vorstellungstext, Deckblatt-Wahl (4 Presets + Custom-Slot),
zweigeteilte Live-Vorschau (Fragebogen-Deckblatt + Empfehlungs-Mail) sowie
Basic↔Pro-Toggle mit Sperr-Overlay + Upgrade-CTA. Live-Bau der Features
(Uploads, Persistenz in `partner`-Tabelle, Node-17-Anbindung) läuft in V1
Punkt 10 mit — Nachzieh-Liste in
`chat-archive/2026-07-06_etappe-2-branding.md`.

---

## 3.5 — Infrastruktur & Tooling (Stand 2026-07-08 spät)

**Prinzip — hart, nicht verhandelbar:** vor Markteintritt (erster zahlender
Kunde außerhalb Desirée) muss die gesamte Datenverarbeitung DSGVO-konform
und auf EU-Regionen konfiguriert sein. VERADEX darf bei einer Beschwerde
nicht angreifbar sein. Wir bauen sauber von Anfang an, nachträgliche
Region-Migrationen sind teuer bis unmöglich (Supabase-Region z. B. ist
irreversibel).

### Cloud vs. Self-Hosted — Entscheidung 2026-07-08 spät

**Cloud-Vendors mit EU-Region + SCC/DPA bleibt der Weg.** Self-hosted auf
Hetzner wurde erwogen, aber gegen den Ops-Aufwand entschieden — Server-
Administration, tägliche Backup-Restore-Tests, SSL-Renewal, PostgreSQL-
Upgrades, Security-Patches sind für ein Solo-Betreiber-Startup nicht
tragbar ohne DevOps-Kapazität.

**Ehrliche Schrems-II-Einordnung:**
Vercel + Supabase-Managed (beide US-Firmen mit EU-Region + Data
Processing Addendum + Standard Contractual Clauses) ist der aktuelle
Marktstandard für DSGVO-konforme SaaS-Bauten nach Schrems II. Es bleibt
ein Restrisiko durch den US-CLOUD-Act (US-Behörden könnten theoretisch
Zugriff auf Daten der US-Muttergesellschaften verlangen — auch wenn die
Daten physisch in EU liegen). Dieses Restrisiko wird mit **technischen
Zusatzmaßnahmen** minimiert:

- **Encryption at rest** in Supabase aktiv (Standard)
- **Verschlüsselte Client-Serverkommunikation** (TLS 1.3 Pflicht)
- **Access-Logs** aller Datenbank-Zugriffe (via Supabase Audit)
- **Minimalprinzip Endkundinnen-Daten:** Fragebogen-Antworten werden
  NICHT persistiert (nur durchgeleitet), n8n-Execution-Logs so
  konfiguriert dass Payloads nicht gespeichert werden. In Supabase
  liegen nur Kunden-Logins + deren Produktkataloge (Geschäftsdaten),
  KEINE Endkundinnen-PII

Das ist die Position, die auch von HubSpot, Notion, Salesforce, Airtable
in DACH mit Erfolg vertreten wird. Ein Umstieg auf 100%-EU-Firmen
(Cleura, Scaleway, IONOS Cloud) bleibt optional für später, falls
politischer Wind sich dreht.

### Google Sheets aus Laufzeit-Toolchain entfernt

Die aktuelle Nutzung von Google Sheets (Regeln + Log + Produktdatenbank
im MONAT-Test) wird für den WL-Bau **komplett eliminiert**:

- **Produktdaten:** wandern nach Supabase (Multi-Tenant, siehe
  Kapitel 3.6)
- **Regeln (map_priorities, map_pool_filter etc.):** bleiben V1
  **embedded im n8n-Workflow-JSON** (aktueller Stand nach Migration #27
  bereits so). Sync erfolgt aus CSV/YAML-Dateien im Git-Repo statt aus
  Sheets. Vorteil: versionierbar, kein Google-Vendor mehr in der Kette.
  Migration nach Supabase erst V2, wenn eine Admin-UI für Regel-
  Bearbeitung nötig wird oder pro-Kunden-Regel-Overrides eingeführt
  werden
- **Beratungs-Log (`beratungs_log`-Tab):** ersetzt durch anonymisiertes
  Supabase-Log ohne Endkundinnen-PII (nur Zeitstempel, Beraterin-ID,
  Empfehlungs-IDs — keine Kundinnen-Antworten, keine Namen)

Google Workspace bleibt für Business-Mail-Konten (`@veradex.de`,
`@mybeautykey.de`) mit EU-DPA — das ist reine Firmen-Kommunikation, kein
Kundinnen-Datenspeicher.

### Klarstellung Anthropic — nur Bau-Werkzeug, keine Laufzeit-Komponente

Der laufende n8n-Workflow ruft KEIN LLM auf. Der Node „17 Claude E-Mail
formulieren" ist Typ `n8n-nodes-base.code` — deterministisches HTML-
Templating aus vorgegebenen Feldern. Der Name „Claude" ist Legacy (Claude
hat beim Bau des Templates mitgeholfen, der Node selbst ist reine
JavaScript-String-Konkatenation). Verifiziert 2026-07-08 durch Scan aller
Node-Types im `workflow_live_now.json`: 0× Anthropic-Referenz, 0× lmChat,
0× langchain, 0× `api.anthropic.com`.

Konsequenz: Anthropic ist bei uns ausschließlich **Bau-Werkzeug** (Claude
Code im Terminal, Konzept-Assistenz), nicht Teil des produktiven
Datenflusses. DSGVO-neutral, kein Enterprise-Deal, kein PII-Prompt-Umbau
nötig. Regel-Engine liefert deterministische, nachvollziehbare Empfehlungen
— für DSGVO-Auskunftspflicht sogar besser als ein LLM.

### Laufzeit-Toolchain

| Kategorie | Tool | Firma | Region | DPA/SCC | Kosten V1 |
|---|---|---|---|---|---|
| Frontend-Hosting | Vercel | US | `fra1` pinnen | DPA | Free-Tier |
| App-Framework | Next.js | OSS | eigenes Deployment | — | — |
| DB | Supabase | US | `eu-central-1` (Frankfurt) | DPA | Free-Tier |
| Workflow-Engine | n8n.cloud | DE (n8n GmbH) | EU-Instanz verifizieren | Inhouse-EU | ~20 €/Monat |
| Bezahlsystem | Paddle | UK (Merchant of Record) | EU-Zahlungsströme | DPA | ~5% + Fee |
| Rechnungen (V1) | Paddle-Portal | UK | via Paddle | via DPA | inkl. |
| Rechnungen (V2) | sevDesk / lexoffice | DE | DE | inhouse-DE | ~15 €/Monat |
| Transactional Mail | Brevo | FR | EU | inhouse-EU | Free bis 300/Tag |
| Domain | Strato | DE | DE | inhouse-DE | ~1 €/Monat |
| Analytics | Plausible | EE (Estland) | EU | inhouse-EU | ~9 €/Monat |
| Error-Tracking | Sentry | US | EU-Region | DPA | Free-Tier |
| Business-Mail | Google Workspace | US | EU-DPA | DPA | ~6 €/Monat |

Geschätzte laufende Kosten V1 (ohne Umsatz-abhängige Paddle-Fee):
~50 €/Monat. Break-Even laut Kapitel 1 bei ~400 €/Monat MRR.

### Bau-Werkzeuge (kein Kunden-Datenzugriff)

- **Claude Code** (Anthropic, US) — Coding-Assistent im Terminal, sieht
  Code aber keine echten Kundinnen-Daten
- **GitHub** (US, EU-Server verfügbar) — privates Repo unter
  `fiebig-projects/`
- **macOS lokal** — Entwicklungsumgebung

DSGVO-neutral, weil kein Kundinnen-Datenzugriff. Wenn wir künftig doch mal
Testdaten mit realen PII verwenden würden, wird das explizit dokumentiert.

### Kritische Konfigurations-Punkte vor Markteintritt

**Region-Pinning (heute nachziehbar, kostet nichts, teilweise irreversibel):**
- Vercel-Projekt: Region auf `fra1` fixieren
- Supabase-Projekt: bei Erstellung `eu-central-1` wählen (nachträglich
  nicht änderbar — deshalb JETZT richtig entscheiden)
- n8n.cloud-Instanz-URL prüfen (aktuell `veradex.app.n8n.cloud`),
  ggf. auf EU-Instanz migrieren
- Sentry-Projekt bei Anlage EU-Region wählen
- Plausible EU-Server (Standard)

**Data Processing Addenda unterschreiben (jeweils ~10 Min via Dashboard):**
- Vercel DPA
- Supabase DPA
- Paddle DPA
- Google Workspace DPA (bei Business-Plan automatisch)
- Sentry DPA
- Brevo DPA

**Compliance-Dokumente vor Launch (Pflicht):**
- Datenschutzerklärung WL-System (eigenständig, nicht Copy von veradex.de)
- Impressum WL-Domain
- AGB WL (mit Klauseln aus Kapitel 2.6 — Content-Verantwortung liegt bei
  Beraterin, § 10 TMG-Neutralität)
- AVV-Vorlage als PDF (Bitkom-Muster als Basis, Anwaltscheck)
- TOM (Technische und Organisatorische Maßnahmen) als AVV-Anlage
- VVT (Verzeichnis von Verarbeitungstätigkeiten) — internes Dokument
- Löschkonzept (Kundinnen-Daten nach Beratungsende + Frist)
- Cookie-Banner nur wenn tracking-Cookies (bei Plausible NEIN — dann kein
  Banner nötig, das ist ein echter DSGVO-Vorteil)

**Anwaltscheck vor erstem zahlenden Kunden (~300–600 €):**
- AGB + AVV auf Compliance mit Kapitel 2.6 prüfen
- Prüfung der Klick-Wrap-AVV-Konstruktion für unsere Zielgruppe
- Klärung: Betriebs-Haftpflicht für SaaS-Anbieter?

### AVV-Modus: Klick-Wrap ist ausreichend

Art. 28 DSGVO verlangt „schriftlich oder elektronisch". Häkchen im Signup
mit vorher sichtbarem PDF-Link zum AVV gilt als elektronisch dokumentiert
— Marktstandard bei Salesforce, HubSpot, Notion, Slack. Voraussetzungen:

- Häkchen darf NICHT vorgehäkelt sein (aktive Zustimmung)
- PDF-Link muss vor dem Klick geöffnet werden können
- Zustimmung wird mit Zeitstempel + IP protokolliert (in Supabase)
- Downloadbare Kopie im Beraterin-Portal

Kein DocuSign nötig für unsere Zielgruppe (Beraterinnen als
Einzelnutzerinnen). Enterprise-Kunden würden echte Unterschrift verlangen,
die sind aber nicht die Zielgruppe.

### Bezahl-System: Paddle statt Stripe für V1

**Paddle als Merchant of Record** wickelt USt für alle EU-Länder ab. Wir
kriegen netto ausgezahlt, Paddle handelt die Voranmeldungen. Kostet ~5% +
Fixed Fee statt Stripes ~1,4% + 25c — bei ~400 €/Monat MRR sind das ~15 €
Mehrkosten, dafür entfällt die OSS-Registrierung und die
länderspezifischen USt-Voranmeldungen. Ab ~5.000 €/Monat MRR Wechsel auf
Stripe prüfen (dann rechnet sich der Buchhaltungs-Overhead).

### Was NICHT gebraucht wird (bewusst nicht)

- **Anthropic Enterprise / EU-Deployment** — Workflow nutzt kein LLM zur
  Laufzeit (heute verifiziert).
- **Stripe für V1** — Paddle als MoR spart USt-Voranmeldungen.
- **DocuSign für AVV** — Klick-Wrap reicht (siehe oben).
- **SMS-Verifikation** — Kosten- und PII-Nachteile, siehe Kapitel 2.7.
- **Google Analytics** — Plausible EU-first ohne Cookie-Banner-Pflicht.
- **Eigenes Custom-Domain-Setup pro Beraterin** — siehe Kapitel 5
  „Verworfene Ideen".
- **Klarnamen der Kundinnen in externen APIs** — trifft bei uns nicht zu,
  da kein LLM zur Laufzeit. Dokumentiert für den Fall künftiger
  LLM-Ergänzungen (dann PII-Prompt-Redaction einbauen).

### Prioritäten-Reihenfolge

**Umsetzungs-Reihenfolge ist nach Kapitel 3 V0 gewandert** (Master-
Reihenfolge, ein Ort für „was ist als nächstes"). Kapitel 3.5 bleibt reine
Nachschlage-Referenz: Tool-Details, Kosten, DPAs. Regionsan­forderungen,
Zeit-Schätzungen und Blocker-Reihenfolge stehen in Kapitel 3 V0.

### Metriken für DSGVO-Bereitschaft (interner Check vor Launch)

- Alle Region-Pinnings gesetzt und dokumentiert
- Alle DPAs unterschrieben und Kopien im `docs/dpa/`-Ordner
- Datenschutzerklärung / Impressum / AGB live und verlinkt
- AVV-PDF im Signup-Flow verlinkt und Häkchen-Test durchgeführt
- Anwaltscheck bestanden
- Löschkonzept dokumentiert und im Portal umsetzbar
- Auskunftsanfrage-Prozess getestet (Test-Account, Datenexport binnen 30 Tagen)

Wenn alle acht Haken gesetzt: Markteintritt möglich.

---

## 3.6 — Datenmodell Multi-Tenant + Provenienz (Stand 2026-07-08 spät)

**Zweck:** Bau-Vorbereitung für den Supabase-Migration und die
Compliance-Guardrails, die in den Code müssen (nicht optional).

### Kern-Prinzipien

1. **Multi-Tenant über Organisation als Vertragseinheit.** Jede zahlende
   Einheit (Salon, Solo-Artist, Studio, MLM-Beraterin) ist eine
   `organization`. Nutzer gehören zu einer Organization, Kataloge und
   Produkte hängen an der Organization — nicht am einzelnen User. Das ist
   die Grundlage für V2-Team-Seats: Owner + Mitarbeiter unter einem Dach.
2. **RLS ist die Isolationsgrenze.** Postgres Row-Level-Security-Policies
   verhindern, dass Organization A jemals Daten von Organization B sieht.
   Jeder Query läuft durch RLS, ohne Ausnahme. Vor Launch: automatisierte
   RLS-Regressionstests mit zwei Test-Nutzern.
3. **Provenienz ist Pflicht auf DB-Ebene.** Alle Content-Tabellen führen
   `created_by`, `created_at`, `updated_by`, `updated_at`, optional
   `source_document`. Postgres-Triggers setzen `created_by`/`updated_by`
   automatisch aus `auth.uid()` — der Client kann diese Felder nicht
   fälschen. Das ist der harte Beleg im Streitfall: „Diese Zeile wurde
   am X von User Y eingetragen."
4. **Endkundinnen-Daten werden NICHT persistiert.** Fragebogen-Antworten
   laufen durch n8n und Regel-Engine, das Ergebnis geht an die Beraterin
   und die Endkundin — es wird nirgendwo dauerhaft gespeichert. Das
   `beratungs_log` (falls überhaupt) enthält nur Zeitstempel + IDs, keine
   Antworten. Vorteil: DSGVO-Löschpflichten für Endkundinnen entfallen
   praktisch komplett.
5. **Consent-Log als Beweismittel.** Alle rechtserheblichen Zustimmungen
   (AGB, AVV, Team-Übernahme, Upload-Rechte) werden mit Zeitstempel, IP,
   User-Agent und Dokument-Version geloggt. Bei DSGVO-Auskunftsanfrage
   auskunftsfähig.

### Schema-Skizze (Supabase Postgres)

```
organization
  id                     uuid PK
  name                   text
  slug                   text unique
  plan                   enum (free, basic, pro)
  contract_started_at    timestamptz
  billing_customer_id    text            -- Paddle-Kundennummer
  seat_limit             int             -- V2
  created_at, updated_at

user
  id                     uuid PK, = auth.uid()
  organization_id        uuid FK → organization
  email                  text unique
  display_name           text
  role                   enum (owner, member)   -- V1: nur owner
  status                 enum (active, suspended)
  created_at, updated_at

product_catalog
  id                     uuid PK
  organization_id        uuid FK → organization
  name                   text                    -- z.B. "Sommer-Sortiment"
  is_default             bool
  analysis_type          enum (hair, skin)       -- V2: skin
  created_by             uuid FK → user
  created_at             timestamptz
  updated_by             uuid FK → user
  updated_at             timestamptz

product
  id                     uuid PK
  catalog_id             uuid FK → product_catalog
  -- 25 Spalten aus wl_adapter.py als typisierte Felder:
  produkt_key            text
  produktname_de         text
  slot_typ               enum
  hauptfunktion          text[]                  -- Postgres array
  nebenfunktionen        text[]
  haarstruktur           text[]
  haarstaerke            text[]
  haarzustand            text[]
  kopfhaut               text[]
  pflegelevel            text[]
  ausschluss_bei         text[]
  intensitaet            enum
  ist_bonding            bool
  ist_hitzeschutz        bool
  ist_scalp_focus        bool
  locken_geeignet        bool
  produkt_url            text
  anwendung              text                    -- warum_sinnvoll-Freitext
  aktiv                  bool default true       -- für Takedown
  -- Provenienz (Trigger-gesetzt):
  created_by             uuid FK → user
  created_at             timestamptz
  updated_by             uuid FK → user
  updated_at             timestamptz
  source_document        text nullable           -- Upload-Belegname

share_code
  id                     uuid PK
  code                   text unique, 8 char     -- z.B. SINA-2M8K
  source_catalog_id      uuid FK → product_catalog
  created_by             uuid FK → user
  created_at             timestamptz
  expires_at             timestamptz nullable
  usage_count            int

share_usage
  id                     uuid PK
  share_code_id          uuid FK → share_code
  target_organization_id uuid FK → organization
  accepted_at            timestamptz             -- aktive Content-Bestätigung
  accepted_by            uuid FK → user

consent_log
  id                     uuid PK
  user_id                uuid FK → user
  consent_type           enum (agb, avv, share_takeover,
                               upload_rights, catalog_release)
  document_version       text                    -- z.B. "AGB v1.3 2026-08"
  accepted_at            timestamptz
  ip_address             inet
  user_agent             text
  reference_id           uuid nullable           -- FK auf betroffene Entity

setup_service_upload
  id                     uuid PK
  organization_id        uuid FK → organization
  uploaded_at            timestamptz
  uploaded_by            uuid FK → user
  file_url               text                    -- Storage-Referenz
  file_hash              text                    -- SHA-256
  rights_confirmed       bool                    -- Häkchen-Bestätigung
  draft_catalog_id       uuid FK → product_catalog nullable
  released_at            timestamptz nullable    -- aktive Freigabe
  released_by            uuid FK → user nullable

lead_status                                       -- Beraterin-Selbstauskunft
  id                     uuid PK                  -- KEINE Kundinnen-PII
  organization_id        uuid FK → organization
  beraterin_id           uuid FK → user
  consultation_ref       text                     -- opaker Verweis (Hash
                                                  -- der Beratungs-Session,
                                                  -- kein Klarname)
  cart_sent_at           timestamptz nullable     -- Beraterin klickt "Warenkorb versendet"
  order_placed_at        timestamptz nullable     -- Beraterin klickt "Bestellt"
  created_at, updated_at
```

**Wichtig zu `lead_status`:** die Tabelle enthält KEINE Kundinnen-PII —
weder Name noch E-Mail noch Kontaktdaten. Nur die Beraterin sieht in
ihrem eigenen Portal, welche ihrer Beratungen sie noch nicht als
„Warenkorb versendet" markiert hat. Der `consultation_ref` ist ein
Hash, der die Beraterin an ihre eigene Notiz erinnert, aber keinen
Rückschluss auf die Kundin zulässt. Follow-up-KPIs im Dashboard
aggregieren nur diese Timestamps (`cart_sent_at IS NULL AND
created_at < now() - 5 days` = Follow-up fällig).

### RLS-Policies (Muster)

```sql
-- Organization: nur eigene sichtbar
CREATE POLICY org_own_read ON organization
  FOR SELECT USING (
    id = (auth.jwt() ->> 'organization_id')::uuid
  );

-- Katalog: nur eigener Organisation
CREATE POLICY catalog_own_all ON product_catalog
  FOR ALL USING (
    organization_id = (auth.jwt() ->> 'organization_id')::uuid
  );

-- Produkt: transitiv über Katalog
CREATE POLICY product_own_all ON product
  FOR ALL USING (
    catalog_id IN (
      SELECT id FROM product_catalog
      WHERE organization_id = (auth.jwt() ->> 'organization_id')::uuid
    )
  );
```

Der JWT-Claim `organization_id` wird beim Login von einer Supabase-Auth-
Function gesetzt (via User-Metadata-Lookup).

### Provenienz-Trigger (Muster)

```sql
CREATE FUNCTION set_provenance() RETURNS TRIGGER AS $$
BEGIN
  IF TG_OP = 'INSERT' THEN
    NEW.created_by := auth.uid();
    NEW.created_at := now();
  END IF;
  NEW.updated_by := auth.uid();
  NEW.updated_at := now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

CREATE TRIGGER product_provenance
  BEFORE INSERT OR UPDATE ON product
  FOR EACH ROW EXECUTE FUNCTION set_provenance();
```

Damit kann der Client die Provenienz-Felder nicht setzen — sie kommen
zwingend aus der authentifizierten Session.

### V2-Andockstellen

- **Team-Seats:** `user.role` existiert bereits (V1 nur owner).
  Erweiterung um `role IN ('owner','admin','member','viewer')` und
  `organization.seat_limit`-Enforcement. Kein Schema-Umbau, nur
  Feld-Nutzung.
- **Skin-Analyse:** `product_catalog.analysis_type` existiert bereits
  (V1 nur hair). Zweiter Wert `skin` schaltet einen zweiten Regel-Satz
  im n8n-Workflow frei. Datenmodell trägt beide Domänen ohne Umbau.
- **Regel-Overrides pro Organisation:** neue Tabelle `custom_rule` mit
  `organization_id` und Regel-JSON, RLS analog. Aktiviert
  Regel-Feintuning pro Kunde (nur in V2 nötig).

### Was NICHT in der DB liegt (bewusst)

- Fragebogen-Antworten der Endkundinnen
- Empfehlungs-Ergebnisse einzelner Beratungen
- Endkundinnen-Namen, -Mails, -Telefonnummern
- LLM-Prompt-Historie (weil kein LLM zur Laufzeit läuft, siehe Kapitel 3.5)

### Automatisierte Regressionstests vor Launch

- **RLS-Test:** zwei Test-Organisationen mit je einem User, jeder darf nur
  eigene Daten sehen. Alle CRUD-Operationen auf allen Content-Tabellen
  einmal cross-Org versuchen — alle müssen mit RLS-Denial fehlschlagen.
- **Provenienz-Test:** Insert einer Zeile → `created_by` muss = `auth.uid()`
  sein, egal was der Client sendet.
- **Consent-Log-Test:** AGB-Akzeptanz löst Log-Eintrag mit korrekter
  Version und IP aus.
- **Löschtest:** User-Löschung kaskadiert nicht auf `consent_log` (Belege
  bleiben mit anonymisierter `user_id` erhalten für DSGVO-Nachweispflicht).

---

## 4 — Offene Entscheidungen

### Namensfrage (blockierend)

Aktueller Vorschlag: **MyBeautyKey.de**. Alternativen offen. Rückmeldung von
Sina / Marcel erwartet. **Kein Bau-Schritt vor Fixierung**, sonst
doppelte Arbeit bei Umbenennung.

### MONAT-DACH-Freigabe — nach Strategie-Umkehr NICHT mehr aktiv

Ursprünglich als blockierend eingestuft. Nach Strategie-Umkehr auf
markenneutrales Konzept (siehe Kapitel 0) **nicht mehr erforderlich**, weil
das Whitelabel-System keine MONAT-Markenrechte berührt. VERADEX-Anschreiben
und Sinas Vorspann bleiben unter `public/konzept/` als „nicht abgesendet,
aufbewahrt" für einen späteren möglichen MONAT-Deal (Weg B — Verkauf/Lizenz
des Systems an MONAT).

### DKIM für veradex.de (Pre-Launch-Blocker)

Aus HANDOVER.md 🔴-Backlog: DKIM-Setup für `veradex.de` bei Strato fehlt.
Vor Go-Live mit echten Endkundinnen zwingend zu fixen. Bei Namenswechsel
sowieso auf der neuen Domain neu aufsetzen.

### DOI für Werbe-Mails (bedingter Blocker)

Aus HANDOVER.md 🔴-Backlog: Double-Opt-In für werbliche Mails aktuell nicht
eingebaut. Nur relevant, sobald Adressen mit `consent_marketing=true` in eine
Newsletter-/Werbe-Liste übernommen werden. Aktuell keine Marketing-Nutzung
der Adressen geplant → nicht dringend.

### REQ-Regel-Produkt-Key-Abstraktion — Whitelabel-Blocker (Stand 2026-07-09)

**Kern:** 26 von 31 Regeln in `map_slot_rules` haben harte MONAT-Produkt-Keys
im `filter`-Feld (curl_gelee, curl_creme, bond_iq_leave_in, rejuveniqe_oel,
moxie_mousse, monat_black, entwirrungsspray, scalp_comfort_serum u.a.). Zwei
weitere nutzen Produktlinien-Namen (`bond_iq`, `scalp_comfort`). Solange
ein Klon den byte-identischen MONAT-Katalog fährt (aktueller Sina-Klon via
`wl_libraries/sina_monat.json`), unproblematisch. Sobald ein Klon einen
Fremdkatalog reinbringt (Nicht-MONAT-Produkte), fallen 26 Regeln tot.

**Betroffen (Cluster):**
- Kernprodukte pro Slot: REQ-02/03/05/06/07/08/24
- Curl-Choreographie: REQ-11/11b/11c/12/13
- Volumen-Choreographie: REQ-16/16b/19/19b
- Optionale Empfehlungen: REQ-14/17/17b/18/20/21/22/23
- Minimal-Routine: REQ-30 (monat_black als 2-in-1)
- Smoothing-Sonderregel: REQ-04b

**Design-Choice bewusst so, kein Bug:** Node 12 (Ranking) ist
wirkungs-abstrahiert (`hauptfunktion`/`nebenfunktion` via `map_profil_funktion`),
Node 11 (REQ-Choreographie) ist produkt-spezifisch, weil manche Empfehlungen
NUR mit einem bestimmten Produkt fachlich Sinn ergeben (z.B. „bei Curl-Wunsch
MUSS die Curl-Creme in styling_1", nicht „irgendein Creme-Produkt").
Wirkungs-abstraktes REQ würde die Beraterinnen-Choreographie zerstören.

**Lösungs-Skizze (spätestens vor erstem Fremdkatalog-Kunden):**
- Neue Spalte `filter_typ ∈ {produkt_key, produktlinie, wirkung}` in `map_slot_rules`
- Node 11 verzweigt Filter-Auswertung nach `filter_typ`:
  - `produkt_key` → aktuelles Verhalten (Literalvergleich auf produkt_key-Spalte)
  - `produktlinie` → Vergleich auf produktlinie-Spalte (REQ-02/03/05 informell so)
  - `wirkung` → Vergleich gegen hauptfunktion ∪ nebenfunktionen des Kandidaten-Pools
- Kunden-Katalog-Anleitung: pro Slot mindestens ein Produkt mit passenden
  Wirkungen anlegen (Curl-Trio → 3 Produkte mit hauptfunktion `locken,definition,halt`
  und den drei Slot-Typen styling_1/2/3).

**Wann angehen?**
- Nicht vor V1-Launch mit Sina (MONAT-Katalog identisch, kein Blocker)
- **Spätestens vor erstem Kunden mit eigenem Fremdkatalog** — Fixture-Test
  mit fiktivem Nicht-MONAT-Katalog vorher fahren, um tote Regeln zu erkennen
- Alternativ als V2-Punkt formuliert, falls V1-Kunden alle MONAT-Ausroll bleiben

**Sichtbar geworden:** 2026-07-09 während PDF-strikt-Audit curl_gelee —
Tomi hat den Produkt-Key in REQ-12 als Whitelabel-untypisch erkannt und
den Umfang hinterfragt.

---

## 5 — Verworfene Ideen (mit Begründung)

**WhatsApp-Beratung per Meta-API** — laufende Kosten pro Nachricht (0,05–0,15 €
pro Conversation), Compliance-Sonderprüfung bei Meta als Auftragsverarbeiter,
Template-Zwang. Ersetzt durch: Ergebnis im Browser + `wa.me`-Button zur
privaten WhatsApp-Nummer der Beraterin. Null Betriebskosten, keine
Compliance-Zusatzprüfung.

**Eigene Domain pro Beraterin (Custom Domain)** — hoher Support-Aufwand
(DNS-Anleitungen, Cert-Automation), rechtliches Risiko (Beraterin könnte unter
eigener Domain Heilversprechen machen). Ersetzt durch: URL-Path mit
Beraterin-Slug `[name].de/[Beraterin]`.

**Kostenlose Testphase / Trial** — die öffentliche Demo (`[name].de/demo`)
übernimmt die Trial-Funktion. Wer bucht, hat schon gesehen was er bekommt.

**Team-Bundle für Sina** — würde Umsatz kosten (Sina zahlt einmal, alle
nutzen) und eine ungewollte MLM-Struktur schaffen. Sina bekommt stattdessen
Botschafter-Zugang kostenlos, ihre Downlines buchen einzeln bei VERADEX.

**Gestaffelte Setup-Fee (29,90 € Basic / 49,90 € Pro)** — Arbitrage-Risiko:
Kunde bucht Basic für niedrigeres Setup, upgraded sofort auf Pro und spart 20 €.
Ersetzt durch: einheitlich 49,90 €.

**7-Tage-Testversion mit persönlichen Daten (Modell C)** — untergräbt die
Setup-Fee-Logik („warum zahlen, wenn schon eingerichtet?"), Missbrauchs-Risiko
per neuer E-Mail-Adresse. Ersetzt durch: öffentliche Demo ohne
Personalisierung, kein Trial nach Buchung.

**Wöchentliche Zusammenfassungs-Mail an die Beraterin** — Wartungsaufwand vs.
Nutzen. Beraterin sieht ihre Beratungen im Dashboard (Pro) oder erhält
Einzel-Mails (Basic).

**Titelbild-Wechsel pro Beraterin (ursprünglich am 3. Juli verworfen)** —
Verworfen aus Marken-Konsistenz-Gründen. **2026-07-06 revidiert:** Sinas
Argument (Beraterinnen wollen personalisieren) hat sich durchgesetzt.
Kommt in Etappe 2.

**Pastellfarben zur Auswahl (ursprünglich am 3. Juli verworfen)** — analog:
verworfen wegen Marken-Konsistenz, 2026-07-06 revidiert. Kommt in Etappe 2.

**Persistente Speicherung des Ergebnis-Links (öffentlich abrufbar)** — DSGVO-
und Kosten-Frage. Ersetzt durch: PDF-Download clientseitig aus dem HTML
(z. B. jsPDF). Kein Server-Storage, keine DSGVO-Löschpflicht, null
Betriebskosten.

**MONAT-Freigabe-Antrag (Weg C aus Session 2026-07-06)** — Marcels Freund
mit Rechtskenntnis identifizierte strukturelles Problem: MONAT hat null
Interesse Dritte mitverdienen zu lassen, § 3.2.1 gibt MONAT die Handhabe
ohne Begründung „nein" zu sagen. Realistische Freigabe-Wahrscheinlichkeit
15–30 %. **2026-07-06 spät verworfen zugunsten markenneutraler Alternative
(Kapitel 0).** VERADEX-Anschreiben und Sinas Vorspann bleiben unter
`public/konzept/` liegen für einen späteren möglichen Weg-B-Deal
(Verkauf/Lizenz an MONAT).

**MONAT-spezifische `warum_sinnvoll`-Spalte mit K-04-strikter Zitate-Regel**
— nach Strategie-Umkehr nicht mehr sinnvoll. Neue Regel: Beraterin schreibt
`warum_sinnvoll` selbst als Freitext (Pro-Feature). Für ihre eigene
Beratungsarbeit, nicht in der Kundinnen-Sicht. Rechtsverantwortung liegt bei
der Beraterin, nicht bei VERADEX.

---

## 6 — Konventionen für den SaaS-Track

### K-Markenneutralität (Kernkonvention nach Strategie-Umkehr 2026-07-06 spät)

Das VERADEX-System enthält **keine** fremden Markennamen, Produktnamen,
Datenblatt-Zitate, Logos oder Marketing-Materialien. Weder in Code, Datenbank,
Kundinnen-Sicht noch in Beraterin-Sicht.

Ausnahmen (Beraterin-Content, den sie selbst einpflegt):
- Produkt-Bibliothek pro Beraterin: sie tippt Produktnamen selbst ein
- `warum_sinnvoll`-Freitext: sie schreibt Verkaufsargumente selbst
- Diese Inhalte sind rechtlich ihre Verantwortung, nicht die von VERADEX

Grund: VERADEX bleibt reiner Infrastruktur-Anbieter, kein Vertriebs-Instrument
einer Marke. Damit fallen alle Markenpartner-Richtlinien (MONAT §§ 3.2.1,
3.2.5, 3.6.1) für VERADEX weg.

### K-Ich-Perspektive Kundinnentexte

Alle Texte, die die Endkundin sieht, sind aus Beraterin-Perspektive geschrieben:
„Kontaktiere mich direkt per WhatsApp" statt „Frag Sina direkt". Beraterin
kann Grußformel + Vorstellungstext im Branding-Bereich (Pro) selbst pflegen,
sonst Standard-Vorlage.

### K-Compliance-Zurückhaltung

Bei rechtlichen Aussagen konservativ formulieren:
- **Keine** Selbstfestlegung zu Art. 9 DSGVO („Kopfhautdaten sind keine
  Gesundheitsdaten" — angreifbar). Neutrale Formulierung „mit erhöhter Sorgfalt
  behandelt".
- **Keine** proaktive Erwähnung von Themen, die niemand selbst anspricht
  (Urheberrecht Datenblätter, AVV etc.). Öffnet nur Diskussion.

### K-Rollen-Ownership

- **Desirée** — fachliche und technische Owner:in, baut und verwaltet
- **Thomas / VERADEX** — rechtliche Hülle, Vertragspartner der Beraterinnen,
  Rechnungsstellung, DSGVO-Verantwortlicher

---

## 7 — Referenz-Dokumente

- `demo/BUILD_SPEC.md` — End-Zustand für Bau nach MONAT-Freigabe
- `public/konzept/index.html` — Landing für Sina / Marcel (live unter
  `myglowmatch.de/konzept`)
- `public/konzept/veradex-anschreiben-monat.html` + PDF — formeller MONAT-Antrag
- `public/konzept/sina-vorspann-monat.html` + PDF — Sinas Vorspann-Text
- `public/konzept/zoom-2026-07-04-update.html` + PDF — Konzept-Überblick
- `HANDOVER.md` — n8n / Regel-Engine (nicht SaaS-Track)
- `chat-archive/2026-07-06_konzept-landing.md` — letzte Session-Doku

## 8 — Pflege des Backlogs

Jede folgende Business-Track-Session sollte diesen Backlog aktualisieren:
- Status-Updates zur Bau-Reihenfolge (in Arbeit / erledigt / verschoben)
- Neue verworfene Ideen mit Begründung
- Meinungsänderungen mit Datum und Grund
- Neue Konventionen bei Bedarf

Der Backlog ist bewusst länger als der Sina-Kommunikations-Content — hier geht
Wissenstiefe vor Präsentierbarkeit.
