# Session 2026-07-03 abends · SaaS-Vorbereitung Zoom Sina + Marcel

**Andere Session als `2026-07-03_session.md`** — die war Thomas' Migration-#27-Fortschritt. Diese hier ist Desirees strategische Vorbereitung des SaaS-Vertriebs.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-03_saas-vorbereitung-zoom-sina.md` und `demo/BUILD_SPEC.md`. **Fokus der nächsten Session:** das Pro-Tier-Feature „warum_sinnvoll" bauen — neue Spalte `warum_sinnvoll` in Sheet `produktdatenbank`, 37 PDF-belegte Sätze (K-08 strikt), Portal-Anzeige in Kundinnen-Detail-Ansicht **nur wenn `partner.tier === 'pro'`** (nicht in der Kundinnen-Mail!). Sind ca. 3-4 Stunden Arbeit davon 2 h PDF-Recherche. Zusätzlich: Zoom-Feedback von Desiree einholen falls noch offen (siehe Rückspiel-Punkte weiter unten).

## Ergänzung 2026-07-05 · Pro-Tier + Sync-Status + Bugfix-Diagnose

**Migration #27 komplett durch (bestätigt am 2026-07-05):** Live-Workflow hat nur noch 17 Nodes (vorher 27). Alle 10 Sheet-Loader entfernt, nur Node 19 (Log-Write) macht noch Sheet-Zugriff. End-to-End-Latenz der letzten Executions 4-5 Sekunden (Median 4,3 s) — vorher 15+ Sekunden. Skalierung ist damit strukturell möglich, Sheets ist kein Bottleneck mehr.

**Bugfix-Diagnose Tomi-Execution 793:** Desiree hatte gefragt warum Tomi „Smoothing Anti-Frizz Shampoo" bei No-Frizz-Profil bekommen hat. Analyse ergab: **kein Bug**. Das Shampoo wurde in Ranking-Stufe 3 (goal_coverage) gewählt, weil es als einziges Kandidaten-Shampoo die `reparatur`-nebenfunktion hat und Tomi genau das als care_goal wollte. Der intensMatch=1 ist neutral, weil `smoothing_shampoo.intensitaet = alle`. Der Produktname „Anti-Frizz" ist irreführend, aber die fachliche Wahl korrekt. Diese Erkenntnis motivierte das Pro-Tier-Feature.

**Neues Preis-Modell mit zwei Tiers (Desirees Idee 2026-07-05):**

| Tier | Monat | Jahr | Feature-Delta |
|---|---|---|---|
| Basic | 29 € | 290 € | Standard-Empfehlung wie bisher |
| **Pro** | **49 €** | **490 €** | Zusätzlich: `warum_sinnvoll`-Erklärung pro Produkt sichtbar für Beraterin im Portal (NICHT in der Kundinnen-Mail) |

**Warum das Konzept sauber ist:**
- Compliance-Vorteil: die Kundin sieht keine automatischen Produktclaims → § 3.6.1 leichter einzuhalten
- Wertwahrnehmung: Pro macht die Beraterin zur informierten Ansprechpartnerin, echter Business-Nutzen, kein künstlicher Feature-Split
- Sina bekommt als Botschafterin das **Pro-Tier kostenlos**

**Aktualisiert in dieser Session:**
- `memory/project-pricing-model.md` — komplett neu mit Basic+Pro
- `memory/project-backlog-partnerbereich.md` — „warum_sinnvoll" jetzt als Pro-Feature präzisiert
- `demo/BUILD_SPEC.md` — Kapitel 2 (Preise) und neues Kapitel 11a („Pro-Tier-Feature warum_sinnvoll") hinzugefügt

## Ursprüngliche Wiedereinstieg-Notiz (Zoom-Feedback)

Falls das Zoom-Feedback von Sina/Marcel noch nicht in Memory eingetragen ist, folgende Punkte einholen:

1. Sinas Reaktion auf Compliance-Realität — überrascht? wusste sie schon?
2. Nimmt Sina die Botschafter-Rolle an? Wie sichtbar?
3. Marcels Fragen zu Buchhaltung / rechtlicher Konstruktion
4. Sinas MONAT-DACH-Corporate-Kontakte
5. Was Sina konkret bereit ist zu tun für den MONAT-Antrag
6. Preis-Reaktion auf 29 €/290 € Basic bzw. 49 €/490 € Pro — fair, zu niedrig, zu hoch?
7. Nächster Termin

## Ausgangslage

Desiree (MONAT-Markenpartnerin, fachliche Owner:in des Systems) hatte am Abend Zoom mit Teamchefin Sina Hildmann + Ehemann Marcel (Buchhaltung). Sina hatte in dieser Woche das System zum ersten Mal gesehen und war begeistert — der Termin sollte klären, ob und wie das System an ihr Team ausgerollt werden kann. Kontextwechsel gegenüber vorheriger Sessions: bis dahin war das System als Desirees eigenes Endkundinnen-Tool gebaut. In dieser Session wurde erstmals die SaaS-Vermarktung an andere MONAT-Partnerinnen strategisch durchgeplant.

## Wichtigste strategische Entscheidungen

**Business-Modell:** myglowmatch wird SaaS an MONAT-Partnerinnen, **VERADEX ist Anbieter und Vertragspartner** (nicht Desiree persönlich). Trennt Markenpartnerin-Rolle vom SaaS-Verkauf, reduziert Compliance-Risiko für Desiree.

**Sinas Rolle (mehrfach präzisiert im Verlauf):**
- Erste Idee: Sina als „Kundin Nummer 1" mit eigenem Abo + Team-Bundle für Downlines
- Zwischenschritt: Team-Bundle raus, alle zahlen einzeln, Sina bekommt Rabatt bei ≥15 aktiven Downlines
- **Finale Entscheidung: Sina ist Botschafterin, kein Vertrag, kostenloser + unbefristeter Zugang**. Ihre Downlines buchen bei VERADEX direkt. Kein Cash-Fluss Sina↔VERADEX, keine Provision — schützt Sina vor § 3.9.1 (Anwerben für andere Direktvertriebe).

**Sinas Vertriebskanal geklärt:** boards.com ist externes Vertriebs-Tool (nicht MONAT), Sina nutzt es um Infos an ihre Downlines zu verteilen. **645 Board-Mitglieder = Sinas Downline**, WhatsApp-Gruppe (500) ist Teilmenge. Cross-Line-Risiko entfällt in diesem Kanal.

**Preise (nur relevant für Downline-Mitglieder, nicht für Sina):**
- Monatsabo: 29 €/Monat brutto + 49 € Setup einmalig
- Jahresabo: 290 €/Jahr brutto, Setup entfällt (empfohlen — 2 Monate gratis + Setup gespart = 107 € Vorteil im Jahr 1)
- Alle Preise brutto (19 % USt), Rechnungsstellung durch VERADEX direkt via Stripe

**Preisverlauf im Denkprozess:** Erst 79 €/Monat → Team-Bundles → verworfen weil zu teuer für Neu-Downlines. Landung bei 29 € weil Neu-Downlines anfangs 30-100 €/Monat verdienen und 29 € mit 1 zusätzlicher Kundinnen-Beratung refinanzierbar sein sollen.

## Compliance-Landkarte (Kernthema)

MONAT-Policies via WebFetch geprüft. Fünf einschlägige Klauseln, differenziert bewertet:

- **§ 3.2.1** = **der eigentliche Bruchpunkt** (keine eigenen Geschäftsinstrumente ohne Aufforderung). Greift auch bei sauberer Markenbehandlung — deshalb Genehmigung zwingend.
- **§ 3.2.5** = differenziert: **kritisch** bei Logos/Bildern/Branding, **vertretbar** bei reiner Text-Nennung von Produktnamen in 1:1-Empfehlungsmail (nominative Nennung, analog WhatsApp-Beratung der Partnerin).
- **§ 3.6.1** = Produktclaims nur wortwörtlich aus offizieller MONAT-Literatur.
- **§ 3.6.3** = keine Einkommens-Claims im Sales-Material.
- **§ 3.9.1** = kein Anwerben für andere Direktvertriebe. Durch Ambassador-Modell entschärft, im Board-Kanal kein Cross-Line.

**Zwei getrennte Haftungsstränge klar getrennt:**
- MONAT-Vertragshaftung (§ 3.6) — trifft nur die Partnerinnen (Kontosperrung, Downline-Verlust, Boni-Verlust)
- Markenrechtliche Haftung — trifft VERADEX / Thomas als Einzelunternehmer persönlich (Abmahnung, Unterlassungsklage, Schadensersatz)

**Konsequenz:** Vor SaaS-Vertriebsstart ist die schriftliche MONAT-DACH-Genehmigung Pflicht.

## Design-Entscheidungen für die Demo (chronologisch)

Farb-System und Look auf myglowmatch-Fragebogen-Optik umgestellt (Champagne-Hintergrund, Rosé-Akzent, Georgia-Serifen, weiche Karten). MONAT-Lila explizit ausgeschlossen und in Memory als Compliance-Marker hinterlegt.

Multi-Tenancy bereits im bestehenden Frontend angelegt (`src/app/[partner]/page.tsx` + `partner_id`-Flow). Ambassador-Modell setzt darauf auf.

**Rückzüge nach Diskussion in der Session:**
- Team-Bereich im Portal komplett raus (Missverständnis „Team-Bundle" = Sina zahlt einmal, alle nutzen → kostet Umsatz + schafft ungewollte MLM-Struktur)
- Farbwahl Pastell-Palette raus (Marken-Konsistenz > Personalisierung)
- Titelbild-Wechsel pro Partnerin raus (Vermeidung Design-Verwässerung + Support)
- Wöchentliche Zusammenfassungs-Mail raus (Wartungsaufwand > Nutzen)

**Portrait statt Logo** — realistischer für MONAT-Partnerinnen.
**Kunden-Follow-up-Mechanik** — Chips „🛒 Warenkorb versendet" + „🎁 Bestellt" pro Kundin, manuell gesetzt, wirken auf KPIs.

## Artefakte für den Zoom (alle in `demo/`)

- `partner-portal.html` — klickbares Desktop-Dashboard-Mockup
- `partner-app.html` — mobile App-Demo im iPhone-Frame
- `zoom-briefing.html` + `zoom-briefing.pdf` — 5-seitiges PDF im myglowmatch-Look
- `zoom-2026-07-03-talking-points.md` — synchrone MD-Fassung zum PDF
- `BUILD_SPEC.md` — **die Referenz für den späteren Build nach MONAT-Genehmigung**

## Was noch offen ist

**Vom Zoom-Feedback abhängig — Desiree soll folgende Punkte an Thomas/Claude zurückspielen:**
1. Sinas Reaktion auf Compliance-Realität (überrascht? wusste sie schon?)
2. Nimmt Sina die Botschafter-Rolle an? Wie sichtbar?
3. Marcels Fragen zu Buchhaltung / rechtlicher Konstruktion
4. Sinas MONAT-DACH-Corporate-Kontakte
5. Was Sina konkret bereit ist zu tun für den MONAT-Antrag
6. Preis-Reaktion auf 29 €/290 € — fair, zu niedrig, zu hoch?
7. Nächster Termin

**Für die Zeit bis MONAT-Genehmigung:**
- Volltext-Policies-PDF beschaffen (Sina hat evtl. Corporate-Zugriff)
- MONAT-DACH-Antrag formulieren (VERADEX als Anbieter)
- Antrag einreichen (Sina wegen Corporate-Kontakten)
- Warten 4-8 Wochen
- Kostenanalyse VERADEX konkretisieren mit Thomas (aktuelle n8n-Rechnung, Steuerberater-Pauschale, Berufshaftpflicht)

**Nach Genehmigung:** BUILD_SPEC.md ist die Bau-Referenz.

## Neue Memory-Einträge in dieser Session

Angelegt / aktualisiert im User-Memory-System:
- `user-desiree.md` — Desiree als aktive Session-Teilnehmerin (nicht Thomas)
- `project-business-model-saas.md` — White-Label-Abo-SaaS für MONAT-Partnerinnen
- `project-customer-pipeline-sina.md` — Sina + Marcel als erste Sales-Opportunity
- `project-legal-monat-compliance.md` — 5 Policy-Klauseln + zwei Haftungsstränge + MONAT-Lila-Verbot
- `project-pricing-model.md` — 29 €/290 €-Modell mit USt-Rechnung
- `project-sina-ambassador-model.md` — kein Vertrag, kostenloser Zugang, boards.com-Kanal
- `project-backlog-partnerbereich.md` — Feature-Backlog inkl. verworfener Ideen mit Begründung
- `project-backlog-marketing-kit.md` — Video-Konzept + Sharing-Paket

Alle in Memory-Index `MEMORY.md` verlinkt.
