# myglowmatch Partnerbereich · Build-Spezifikation

**Zweck dieses Dokuments:** Alle Design- und Produkt-Entscheidungen aus der Vorbereitungs-Session 2026-07-03, sauber strukturiert für den späteren Bau. Wenn nach MONAT-Genehmigung mit der Umsetzung begonnen wird, dient dies als Referenz — nicht die Chat-Historie durchsuchen, sondern hier nachlesen.

**Voraussetzung für Build-Start:** schriftliche MONAT-DACH-Genehmigung liegt vor. Vorher: keine Zeile Code für den kommerziellen Vertrieb.

**Ergänzende Dateien:**
- `demo/partner-portal.html` — Desktop-Ansicht als visuelles Referenz-Mockup
- `demo/partner-app.html` — mobile App-Ansicht als Referenz-Mockup
- `demo/zoom-briefing.pdf` — Compliance- und Preis-Skizze
- Session-Kontext: `chat-archive/2026-07-03_session.md`
- Memory-Verzeichnis (User-Memory-System) — begleitende Notizen

---

## 1. Geschäftsmodell (fix)

- **Anbieter:** VERADEX (Thomas Fiebig, veradex.de). Nicht Desiree persönlich.
- **Kundinnen:** MONAT-Markenpartnerinnen im Abo (kein B2C-Endkundinnen-Modell).
- **Verkauft wird:** White-Label-Beratungstool = eigener Beratungs-Link `myglowmatch.de/[name]` + Partner-Login-Portal + automatische Kundinnen-Empfehlungsmail + Follow-up-Verwaltung.
- **Sina Hildmann** (erste Kundin/Botschafterin): bekommt Tool **kostenlos, unbefristet**, kein Vertrag, kein Cash-Fluss zu VERADEX. Ihre Downlines buchen bei VERADEX direkt. Sinas Anreiz: bessere Beratung im Team → mehr MONAT-Provision aus MONAT. Dieses Modell ist skalierbar für weitere Botschafterinnen.

## 2. Preise (fix, brutto inkl. 19 % USt) · Basic + Pro-Tier

**Basic-Tier**

| Variante | Setup | Laufend | Vertrag |
|---|---|---|---|
| Monatsabo | 49,90 € einmalig | **14,90 €/Monat** | monatlich kündbar zum Monatsende |
| **Jahresabo (empfohlen)** | entfällt | **149 €/Jahr** | 12 Monate, autom. Verlängerung, Kündigung 1 Mo vor Ende |

**Pro-Tier**

| Variante | Setup | Laufend | Vertrag |
|---|---|---|---|
| Monatsabo | 49,90 € einmalig | **29,90 €/Monat** | monatlich kündbar |
| **Jahresabo (empfohlen)** | entfällt | **299 €/Jahr** | 12 Monate, autom. Verlängerung |

**Was Basic kann:** Fragebogen-Link, Kundinnen-Verwaltung, Empfehlungs-Mail an Kundinnen, Follow-up-Chips, Statistiken, Portrait/Signatur-Personalisierung.

**Was Pro zusätzlich kann:** die Beraterin sieht pro empfohlenes Produkt eine **„warum wurde das gewählt"-Erklärung** (PDF-belegt, aus Sheet-Spalte `warum_sinnvoll`). Nur im Partnerbereich sichtbar, **nicht in der Kundinnen-Mail** — die bekommt weiterhin nur den Produktnamen. Ermöglicht der Beraterin, ihre Kundin persönlich zu briefen und Rückfragen souverän zu beantworten. Compliance-Vorteil: § 3.6.1 wird nicht triggert weil die Erklärung intern bleibt.

**Zahlungsabwicklung:** Stripe (SEPA-Lastschrift bevorzugt, EU-Karten + PayPal als Alternative).
**Rechnungsstellung:** VERADEX direkt an das jeweilige Downline-Mitglied, USt separat ausgewiesen.
**Preis nicht verhandelbar über Volumen** (kein Team-Rabatt, kein Bundle — bewusste Design-Entscheidung gegen § 3.9.1).
**Tier-Wechsel:** Basic → Pro jederzeit möglich (proratiert). Pro → Basic zum nächsten Abrechnungszyklus.

## 3. Compliance-Regeln (bindend fürs Design)

- **Kein MONAT-Logo, keine offiziellen Produktbilder, kein MONAT-Branding** irgendwo in UI, Marketing, Mail
- **Kein Lila/Violett/Lavendel** in Farbwelt (MONAT-Markenfarbe)
- **Produkttexte 1:1 aus offiziellen MONAT-PDFs** (K-08-PDF-strikt-Konvention). Wortlaut nicht paraphrasieren.
- **Keine Einkommens-Claims** in Marketing oder UI
- **Kein Provisions-/Referrer-Modell** in irgendeiner Form (auch nicht mit anderer Bezeichnung)
- **VERADEX-Rechnung** direkt an Endkundin, nie über eine Partnerin geleitet (das wäre indirekte Provision)
- **Disclaimer im Footer:** „myglowmatch by VERADEX · unabhängig von MONAT"

## 4. Multi-Tenancy-Datenmodell

**Bereits im bestehenden Code angelegt:**
- Route `src/app/[partner]/page.tsx` — dynamische Partner-URL
- `partner_id`-Flow durch `src/components/Questionnaire.tsx` → `src/lib/submission.ts` → `/api/submit/route.ts` → n8n-Webhook
- Aktuelles Partners-Objekt hartcodiert in n8n Node 17 (`partners`-Dictionary mit Eintrag `desiree`)

**Muss beim Build entstehen:**
- Partner-Stammdaten-DB (Supabase Postgres empfohlen) mit Feldern:
  - `partner_id` (URL-Slug, klein, alphanumerisch)
  - `email` (Login + Rechnungsadresse + Antwort-Adresse für Kundinnen-Mails)
  - `display_name` (im Fragebogen-Header + Mail-Signatur)
  - `slogan` (optional, im Fragebogen-Header)
  - `signature_line` (personalisierte Abschluss-Zeile in der Mail)
  - `contact_phone` (optional, für Mail-Signatur)
  - `portrait_url` (rundes Bild, Fallback: farbiger Kreis mit Initialen)
  - **`tier`** (`basic` / `pro` / `ambassador`) — steuert Feature-Sichtbarkeit im Portal
  - `abo_type` (`month` / `year` / `free_ambassador`)
  - `abo_status` (`active` / `paused` / `cancelled`)
  - `stripe_customer_id` + `stripe_subscription_id`
  - `created_at`, `updated_at`
- Kundinnen-Lead-DB pro Partner:
  - `lead_id`, `partner_id`, `customer_email`, `customer_name`
  - Fragebogen-Antworten (JSON)
  - Empfehlungs-Ergebnis (Produkt-IDs + Reihenfolge)
  - `mail_sent_at`, `mail_opened_at` (optional Tracking)
  - `warenkorb_versendet` (bool, manuell durch Partnerin gesetzt)
  - `bestellt` (bool, manuell durch Partnerin gesetzt)
  - `follow_up_note` (optional Freitext)

- n8n Node 17 muss von hartcodiertem Objekt auf DB-Lookup umgestellt werden (`partners`-Objekt raus, Query per `partner_id`).

## 5. Partner-Portal — Feature-Set MVP

**Alle folgenden Ansichten sind in `demo/partner-portal.html` visualisiert.**

### 5.1 Login-Bereich
- E-Mail + Passwort (Standard-Auth via Supabase / Clerk / Better-Auth — Entscheidung offen)
- Passwort vergessen: Standard-Flow via E-Mail-Link
- Registrierung: **nicht public** — Zugang nur über Einladungs-Link (kommt bei erfolgreicher Buchung per Stripe-Webhook)

### 5.2 Sidebar-Navigation (6 Menüpunkte, kein Team-Bereich)
1. Übersicht
2. Meine Kundinnen
3. Beratung starten
4. Mein Branding
5. Statistiken
6. Einstellungen

### 5.3 Übersicht
- 4 KPI-Kacheln: Beratungen 30d · Warenkorb-Links versendet · Bestellungen · Follow-ups offen
- Beratungs-Link teilen (Kopieren/WhatsApp/QR-Code)
- Liste „zuletzt beraten" (5 Einträge, Klick öffnet Detail)

### 5.4 Meine Kundinnen
- Volltextsuche
- Filter-Chips: Alle / Heute / Diese Woche / 30 Tage / Follow-up offen / Bestellt
- Export als CSV
- Tabelle: Name, Profil, Beratung am, Follow-up-Chips (🛒 Warenkorb + 🎁 Bestellt, beide manuell durch Partnerin toggle-bar)
- Klick auf Zeile öffnet Detail-Ansicht: Profil, gesendete Mail, Follow-up-Notiz
- **Pro-Tier only:** In der Detail-Ansicht pro empfohlenes Produkt eine „warum wurde das gewählt"-Zeile aus Sheet-Spalte `warum_sinnvoll`. Rendering-Bedingung: `partner.tier === 'pro'`. Basic-Tier sieht die Zeilen nicht.

### 5.5 Beratung starten
Drei Wege als Action-Cards:
- Link teilen (Copy/WhatsApp)
- QR-Code (Download PNG/PDF)
- Vor Ort ausfüllen (Fragebogen direkt öffnen, wird als „vor Ort mit [Partnerin]" gespeichert)

Sowie Erklär-Block „Was passiert nach dem Ausfüllen?" mit 4 Schritten.

### 5.6 Mein Branding (nur folgende Felder — Rest bewusst verworfen)
- Portrait (rundes Bild, mind. 400×400, Fallback: Kreis mit Initialen)
- Anzeige-Name
- Slogan (optional)
- Signatur-Zeile
- Kontakt-E-Mail
- Telefon / WhatsApp (optional)
- **Live-Vorschau der Empfehlungs-Mail rechts** (rendert mit den Live-Werten)
- **NICHT im MVP:** Farbauswahl (immer myglowmatch-Rosé), Titelbild-Wechsel (immer Desirees Premium-Hero), Custom-CSS

### 5.7 Statistiken
- KPI-Kacheln: Beratungen / Warenkorb-Links / Bestellungen / Follow-up-Quote
- Chart Beratungen pro Woche (letzte 6 Wochen)
- Liste „am häufigsten empfohlen" (Top 5)
- Verteilungen: Haartyp-% und Top-Anliegen-%
- Zeitraum-Filter oben: 30 Tage / 90 Tage / Jahr

### 5.8 Einstellungen
- Konto: E-Mail ändern, Passwort ändern, 2FA
- Mein Abo: Typ, Preis, Startdatum, nächste Abbuchung, Laufzeit, Kündigen-Link
- Rechnungen: Liste als PDF-Download (VERADEX-Rechnungen, USt separat)
- Benachrichtigungen (Toggles):
  - Empfehlungs-Mail automatisch an Kundin senden (Default ON)
  - Kopie der Kundinnen-Mail an mich (Default ON)
  - Follow-up-Erinnerung (Default ON, wenn 5 Tage ohne Warenkorb-Link-Toggle)
  - Neuigkeiten von myglowmatch (Default OFF)

## 6. Mobile App (Phase 2 — später)

MVP: Portal ist **mobile-responsive**, kein natives App-Build. Das `partner-app.html`-Mockup zeigt konzeptuell, wie eine native App aussehen könnte — als PWA-Alternative im MVP realisierbar (fullscreen im Safari via Home-Screen).

**Native App (iOS + Android):** erst nach validiertem Product-Market-Fit. Zeitrahmen: 2-3 Monate Entwicklung nach MVP-Launch.

## 7. Kundinnen-Empfehlungs-Mail (bestehend, Node 17)

Bereits live und funktional. Beim Multi-Tenant-Umbau:
- Absender-Name = `display_name` der Partnerin
- Absender-E-Mail = `contact_email` (via SMTP-Provider mit SPF/DKIM für die Partner-Adresse — oder via `noreply@myglowmatch.de` mit Reply-To = Partnerin, einfacher aber weniger authentisch)
- Portrait in Signatur = `portrait_url`
- Signatur-Zeile = `signature_line`
- Kontakt-Block = `contact_phone`, `contact_email`, WhatsApp-Link falls Nummer vorhanden

## 8. Betriebs-Stack

**Empfohlen (Vorschlag, im Bau-Zeitpunkt final entscheiden):**

| Komponente | Provider |
|---|---|
| Frontend | Next.js auf Vercel Pro |
| Datenbank | Supabase (Postgres + Auth in einem) |
| Datei-Storage | Supabase Storage oder Cloudflare R2 |
| E-Mail-Versand | Postmark oder SendGrid (transaktional, hohe Zustellrate) |
| Payment | Stripe (Subscriptions + Customer Portal) |
| Backend-Logic | n8n Cloud (bestehend, `veradex.app.n8n.cloud`) |
| Beratungs-Regeln | Google Sheets → Sync-Skript in n8n Nodes (siehe Migration #27) |
| DNS/CDN | Cloudflare (Free) |
| Monitoring | Vercel Analytics + n8n interne Logs, ggf. Sentry für Fehler |

## 9. Onboarding-Flow (Stripe → Portal)

1. Interessentin klickt bei Sina auf Beitritts-Link (aus Sinas WhatsApp-/Board-Post)
2. Landing-Page mit Video, Vorteile, Preisen, Fragen zu Compliance-Absicherung
3. „Jetzt starten" → Stripe Checkout (SEPA / Karte) mit AGB-Checkbox + AVV-Zustimmung
4. Stripe-Webhook triggert n8n-Workflow:
   - Partner-Datensatz in DB anlegen (mit generiertem `partner_id`)
   - Auth-Account erstellen
   - Welcome-Mail mit URL `myglowmatch.de/[name]` + Login-Zugang
5. Partnerin loggt sich ein, sieht Onboarding-Wizard: Portrait hochladen, Signatur einrichten, Kontakt-Mail bestätigen
6. Fertig — Beratungs-Link ist scharf

## 10. Rechtliches — vor Launch klären

- **AGB** anwaltlich prüfen lassen (~300-500 €)
- **AVV** (Auftragsverarbeitungsvertrag) — Standard-Vorlage nutzen (Strato-Methode: Text + Klick + IP/Zeitstempel als Nachweis speichern, siehe HANDOVER)
- **Datenschutzerklärung** für myglowmatch.de + Partner-Portal — eRecht24 oder anwaltlich
- **Impressum** VERADEX
- **MONAT-Genehmigung** schriftlich vorliegend
- **Berufshaftpflicht** VERADEX-IT — vor Launch abschließen
- **USt-ID / Kleinunternehmer-Status VERADEX** prüfen — vermutlich regelbesteuernd nötig, weil B2B-Umsätze über Kleinunternehmer-Grenze

## 11. Explizit verworfene Ideen (mit Grund — nicht wieder aufmachen)

| Idee | Verworfen weil | Wiederaufnahme-Bedingung |
|---|---|---|
| Team-Bundle Preis für Sina | Reduziert Umsatz drastisch + schafft ungewollte MLM-Nebenstruktur (§ 3.9.1) | Nie |
| Provisions-/Referrer-Modell für Botschafterinnen | § 3.9.1-Verstoß, würde MONAT-Compliance direkt triggern | Nie |
| Farbauswahl pro Partnerin (Pastell-Palette) | Marken-Konsistenz > Personalisierung, weniger Support | Nur auf konkrete Nachfrage |
| Titelbild-Wechsel pro Partnerin | Design-Verwässerung durch schwache Handy-Fotos, Support-Aufwand | Nur auf konkrete Nachfrage |
| Wöchentliche Zusammenfassungs-Mail | Wartungsbaustelle bei geringem Wert — KPIs live im Dashboard | Wenn Skalierung > 500 Partnerinnen |
| Lavendel/Lila als Design-Element | Exakte MONAT-Markenfarbe → Compliance-Angriffspunkt | Nie |
| Team-Bereich im Portal (Sinas Downline sehen) | Sinas Rolle ist Botschafterin, nicht Team-Chefin im System | Nur wenn Modell auf Multi-Level-Botschafterinnen erweitert wird |

## 11a. Pro-Tier-Feature „warum_sinnvoll" (Spezial-Kapitel)

**Motivation:** Diagnose an Tomi-Execution 793 (2026-07-04) hat gezeigt, dass fachlich korrekte Produktwahlen wegen irreführender Produktnamen (Beispiel: „Smoothing Anti-Frizz Shampoo" bei No-Frizz-Profil, weil `reparatur`-nebenfunktion gewinnt) für Beraterinnen und Kundinnen intransparent wirken. Node 12 arbeitet korrekt — die Produktnamen führen in die Irre.

**Umsetzung im MVP-Build:**

1. **Sheet-Erweiterung:** neue Spalte `warum_sinnvoll` in `produktdatenbank`, 37 Produkte × 1 PDF-belegter Satz. K-08-Konvention strikt: wortwörtlich aus MONAT-Datenblatt, keine eigene Interpretation. Beispiel für `smoothing_shampoo`: „Bekämpft mit reparativem Wirkstoff-Komplex trockene, gespaltene Enden".

2. **Sync-Skript:** `sync_rules_to_workflow.py` muss `produktdatenbank`-Sync erweitern (aktueller Stand: `produktdatenbank` ist noch nicht gesynct — Migration #27 hat 6/10, `produktdatenbank` ist auf der Restliste).

3. **Portal-Anzeige:** in Kundinnen-Detail-Ansicht wird pro empfohlenem Produkt-Slot die `warum_sinnvoll`-Zeile darunter eingeblendet — **nur wenn `partner.tier === 'pro'`**.

4. **Nicht in der Kundinnen-Mail (§ 3.6.1):** Die Erklärung bleibt intern für die Beraterin. Compliance-Motivation: eigene Produktclaims an Kundinnen sind ohne offizielle MONAT-Autorisierung riskant. Die Beraterin darf die Erklärung mündlich/WhatsApp an ihre Kundin geben — sie ist die verantwortliche Beraterin, nicht das automatische System.

5. **Wirkung auf Preis:** rechtfertigt Pro-Tier-Aufpreis (29 → 49 € Monat, 290 → 490 € Jahr) durch echten Beraterin-Nutzen.

**Aufwand:** 3-4 Stunden davon 2h die PDF-Recherche für 37 Produkte. Wird in eigener Session gebaut, damit die K-08-Genauigkeit nicht leidet.

## 12. Backlog (nach MVP-Launch iterativ)

Diese Features nicht im MVP, aber konzeptuell durchdacht — im Memory-Ordner unter `project-backlog-partnerbereich.md` und `project-backlog-marketing-kit.md` detailliert:

- OG-Image für Beratungs-Link (dynamische Sharing-Preview mit Portrait + Slogan)
- Werbevideo 60-90s (Do-it-yourself Screen-Recording + Voiceover Desiree)
- WhatsApp-/Board-Post-Vorlagen für Botschafterinnen
- Story-Grafiken 9:16 (5 Motive)
- 1-Seiten-Onepager PDF für Interessentinnen
- FAQ-Dokument
- Native iOS/Android App

## 13. Kostenmodell VERADEX (Grob-Rahmen)

Detail in Chat-Session vom 2026-07-03 besprochen. Grobe Jahres-Rechnung bei 130 Abos aus Sinas Downline:

- Bruttoumsatz ~43 k €
- Nach USt (19 %), Stripe (~1 %), Hosting-Fixkosten (~4,2 k €), Einmal-Rechtskosten Jahr 1 (~1,8 k €), Gewerbesteuer über Freibetrag, ESt persönlich
- ≈ **18-20 k € Netto-Netto in Familienkasse Jahr 1**

Konkretisierung mit Thomas nach Zoom (aktuelle n8n-Rechnung, Steuerberater-Pauschale, Berufshaftpflicht-Angebot einholen).

## 14. Migration bestehender Systemzustand → SaaS-Bereit

Diese Punkte werden VOR Launch technisch nötig:

- **n8n Node 17:** von hartcodiertem `partners`-Objekt auf DB-Lookup umbauen — dabei auch die zwei offenen Punkte aus dem HANDOVER lösen (`project-node17-readable-map-fix` + `project-email-gender-neutral`)
- **Sheets-Sync abschließen** (Migration #27, 6/10 synchronisiert — verbleibend: `map_derived_variables`, `map_pflegelevel_scoring`, `map_profil_funktion`, `produktdatenbank`). Grund: Live-Workflow muss Google-Sheets-Quota-frei laufen, bevor Skalierung möglich ist
- **Verwaiste Loader-Nodes rausnehmen** (aus HANDOVER: 04a, 06b, 06c, 08a, 10, 13 verbrauchen weiter Quota trotz Sync)
- **Multi-Tenant-Bilder-Speicher** aufsetzen (Portraits pro Partnerin)
- **AGB-/AVV-Zustimmung im Stripe-Checkout** korrekt einholen und speichern
- **Rechnungs-PDF-Generator** in n8n (aus Stripe-Daten + VERADEX-Vorlage + USt-Ausweis)

---

**Letzte Aktualisierung:** 2026-07-03 · Vorbereitung Zoom Sina + Marcel · Session-Archiv `chat-archive/2026-07-03_session.md`
