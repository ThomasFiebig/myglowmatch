# SAAS_BACKLOG — myglowmatch / VERADEX

**Zweck:** zentrale Referenz für alle Business-Track-Entscheidungen zum SaaS-Vertrieb.
Getrennt von `HANDOVER.md` (n8n / Regel-Engine) und `demo/BUILD_SPEC.md` (End-Zustand
für Partner).

**Stand:** 2026-07-06 spät (Strategie-Umkehr auf markenneutrale Alternative).

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
- Limit: 3 Beratungen pro Monat (Rechenzeit-Schutz gegen Missbrauch)
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
(3 Beratungen/Monat, kein Login-Zwang) dauerhaft mit immer neuen
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
(alle drei zählen als ein Kontingent = 3 Beratungen gesamt statt 3 pro
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

## 3 — Bau-Reihenfolge (angepasst nach Strategie-Umkehr)

Realistischer Weg vom heutigen Stand (n8n-Workflow mit MONAT-Produkten, Landing
für Konzept-Präsentation) zum Whitelabel-Launch:

1. **Namensfreigabe** durch Sina / Marcel (aktueller Vorschlag: **MyBeautyKey**
   passt zur markenneutralen Strategie)
2. **Domain sichern** + neues Logo finalisieren
3. **Whitelabel-Grundgerüst** als Route-Group `src/app/(whitelabel)/` im
   bestehenden Repo aufsetzen
4. **Fragebogen** aus bestehendem System kopieren, MONAT-spezifische
   Vokabular-Referenzen entfernen (bleibt in `src/data/questions.ts` erhalten,
   neue Version im whitelabel-Ordner)
5. **Ergebnisseite markenneutral** — Analyse-Engine liefert Bedarfsprofil
   (Slot-basierte Empfehlungen wie „shampoo=feuchtigkeit+dickes_haar"),
   Kundinnenseite zeigt Text ohne Produktnamen
6. **Regel-Engine (Node 04–15)** wiederverwenden: liefert das Bedarfsprofil,
   nicht mehr konkrete Produkte
7. **Free-Modus** implementieren — Beraterin bucht kostenlos, bekommt Link,
   Limit 3 Beratungen/Monat, Upgrade-Prompt bei Erreichen
8. **Basic-Modus** — Portal mit Login, Beratermail, Kundinnen-Übersicht,
   ausgegraute Pro-Cards
9. **Pro-Modus** — Produkt-Bibliothek-UI (Beraterin trägt Sortiment pro Slot
   ein, strukturierte Attribute per Chip-Auswahl aus n8n-Vokabular),
   `warum_sinnvoll`-Freitext, Matching Bedarfsprofil → Beraterin-Produkte,
   Dashboard, Branding-Bereich, PWA, Push
9.a **Team-Sharing** — Team-Code-Generator im Upline-Portal, Import-Flow
   für Downlines beim Setup, Pull-Notification bei Vorlage-Updates
   (siehe Kapitel 2.5)
9.b **Compliance-Absicherung** — AGB-Klauseln, Takedown-Endpoint, prominente
   Beraterin-Attribution auf Kundinnen-Ergebnisseite, Content-Akzeptanz-Klick
   bei Team-Sharing (siehe Kapitel 2.6). Anwaltscheck vor erstem zahlenden
   Kunden.
10. **Stripe-Anbindung** für Free-Upgrade auf Basic und Pro-Buchung + Setup-Fee
11. **Öffentliche Demo** unter dem neuen Namen (`[name].de/demo`) mit
    Analyse-only-Beispiel
12. **Übergabe der finalen Demo** an Sina und die ca. 10 Top-Leaderinnen

**Realistischer Zeitrahmen:** ~14–18 Bau-Tage für Basic-Launch inkl.
ausgegrautem Dashboard. Pro-Features als V1.1 unmittelbar danach.

**Etappe 2 als Demo-Mockup erledigt (2026-07-06):** Branding-Bereich mit
Portrait-Slot, Farbwahl (6 Pastell-Töne, kein Lila), Grußformel +
Vorstellungstext, Deckblatt-Wahl (4 Presets + Custom-Slot), zweigeteilte
Live-Vorschau (Fragebogen-Deckblatt + Empfehlungs-Mail) sowie Basic↔Pro-
Toggle mit Sperr-Overlay + Upgrade-CTA. Live-Bau der Features (Uploads,
Persistenz in `partner`-Tabelle, Node-17-Anbindung) folgt nach MONAT-
Freigabe — Nachzieh-Liste in `chat-archive/2026-07-06_etappe-2-branding.md`.

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
