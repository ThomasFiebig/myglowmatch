# SAAS_BACKLOG — myglowmatch / VERADEX

**Zweck:** zentrale Referenz für alle Business-Track-Entscheidungen zum SaaS-Vertrieb.
Getrennt von `HANDOVER.md` (n8n / Regel-Engine) und `demo/BUILD_SPEC.md` (End-Zustand
für Partner).

**Stand:** 2026-07-06 (nach Konzept-Landing + Antragsschreiben).

**Rollen:**
- **Desirée Fiebig** (MONAT-Markenpartnerin Nr. 14038921) — fachliche und technische
  Owner:in: baut, verwaltet, entscheidet inhaltlich.
- **Thomas Fiebig / VERADEX** (MONAT-Markenpartner Nr. 14074120) — rechtliche Hülle:
  Vertragspartner der Beraterinnen, Rechnungsstellung, formaler MONAT-Antragsteller,
  DSGVO-Verantwortlicher, kaufmännischer Betrieb.

---

## 1 — Preismodell (fixiert 2026-07-06)

| | Monat | Jahr | Setup einmalig |
|---|---|---|---|
| **Basic** | 14,90 € | 179 € | 49,90 € (entfällt bei Jahresabo) |
| **Pro** | 29,90 € | 359 € | 49,90 € (entfällt bei Jahresabo) |

Alle Preise brutto inkl. 19 % USt. Rechnungsstellung durch VERADEX via Stripe.

**Setup-Fee-Logik:** einheitlich 49,90 € für beide Tiers. Grund: primär
Cherry-Picking-Schutz gegen Kurzzeit-Buchungen (bei ~8 € Netto-Gewinn pro
Basic-Monat lohnt sich ein Kunde erst nach dem dritten Monat). Gestaffelte
Setup-Fee wurde verworfen wegen Arbitrage-Risiko bei Upgrade.

**Jahresabo:** kein zusätzlicher Monatsrabatt, nur Setup-Erlass. Ersparnis
gegenüber Monatsabo mit Setup: ~22 %. Klares Verkaufsargument ohne
Marge-Verlust.

**Fallback-Modell** (nicht aktiv, aber dokumentiert für den Fall, dass Sinas
Downlines das Setup als Kaufhürde melden): kein Setup, dafür Basic auf
19,90 €/Monat und Pro auf 34,90 €/Monat anheben. Rechnerisch nach 10 Monaten
gleicher Umsatz.

---

## 2 — Feature-Split Basic ↔ Pro

| Funktion | Basic | Pro |
|---|---|---|
| Fragebogen + Analyse-System für Kundinnen | ✓ | ✓ |
| Ergebnisseite im Browser (Endkundin) | ✓ | ✓ |
| PDF-Download der Ergebnisseite für Kundin | ✓ | ✓ |
| WhatsApp-Kontakt-Button (`wa.me`) zur Beraterin | ✓ | ✓ |
| Beratungs-Mail an die Markenpartnerin nach jeder Analyse | ✓ | ✓ |
| Portal-Zugang mit Stammdaten (Name, Kontakt, Rechnung) | ✓ | ✓ |
| Dashboard mit Übersicht aller Beratungen | — | ✓ |
| Branding-Bereich (Portrait, Farbwahl inkl. Pastellpalette, Grußformel, Deckblatt-Austausch) | — | ✓ |
| Verkaufsargumentations-Hilfe pro Produkt (`warum_sinnvoll`) | — | ✓ |
| Push-Benachrichtigung aufs Handy | — | ✓ |
| Dashboard als App auf den Homebildschirm installieren (PWA) | — | ✓ |
| Zustellungs-Toggle (Mail / Push / nur Dashboard) | — | ✓ |

**Basic-Portal:** die Pro-Bereiche sind sichtbar, aber deaktiviert (ausgegraut
mit Upgrade-CTA). Verkaufspsychologisch stark — Basic-Partnerin sieht ständig,
was sie verpasst.

**Upgrade / Downgrade:**
- Upgrade jederzeit möglich, bezahlte Gebühren werden anteilig verrechnet
- Downgrade: keine Erstattung. Pro läuft ab bezahltem Zeitraum weiter und
  wechselt danach in Basic. Dashboard-Daten werden „eingefroren" (30 Tage
  Reaktivierungs-Fenster, DSGVO-Balance).

---

## 3 — Bau-Reihenfolge nach Namensfreigabe

Realistischer Weg vom heutigen Stand (n8n-Workflow, Landing für Konzept-Präsentation)
zum Basic-Launch:

1. **Namensfreigabe** durch Sina / Marcel (aktueller Vorschlag: **MyBeautyKey**)
2. **Domain sichern** + neues Logo finalisieren
3. **Öffentliche Demo** unter dem neuen Namen aufsetzen (`[name].de/demo`)
4. **Fragebogen + Ergebnisseite** auf neuen Namen umbauen
5. **Ergebnisseite-Refactor** — Ergebnis erscheint direkt im Browser statt per
   Mail. Node 17 wird zum HTML-Renderer (Kundinnenseite) + zur Beraterinnen-Mail
   (unverändert im Basic-Tarif)
6. **Basic-Version fertigstellen** — Fragebogen, Ergebnisseite,
   Beratungsmail an Partnerin, Minimal-Portal mit Settings + ausgegrauten
   Pro-Cards
7. **Pro-Version obendrauf bauen** — Dashboard, Branding-Bereich,
   `warum_sinnvoll` (K-04 strikt), Push/PWA, Zustellungs-Toggle
8. **Stripe-Anbindung** für Basic- und Pro-Buchung + Setup-Fee
9. **Übergabe der finalen Demo** an die ca. 10 Top-Leaderinnen unter Sina

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

### MONAT-DACH-Freigabe (blockierend für Vertrieb)

- Antragsstrategie: Variante C (Sinas persönlicher Vorspann + VERADEX-Antrag
  als PDF-Anhang)
- Beide Schreiben in `public/konzept/` fertig, Platzhalter für Ansprechpartner
- Ansprechpartner-Info von Sina erwartet
- Nach Antragsversand: 4–8 Wochen Wartezeit bis Rückmeldung realistisch
- **Wichtig:** Live-Demo mit Testzugang wird **nicht** mit dem Erstantrag
  mitgeschickt — nur auf MONAT-Anfrage im späteren Vorstellungstermin

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

---

## 6 — Konventionen für den SaaS-Track

### K-VerkaufsargumenteContent (aus Session 2026-07-06)

Für die neue Sheet-Spalte `warum_sinnvoll` (Pro-Feature) gilt **K-04 strikt**:
wortwörtliches Zitat aus dem MONAT-Produktdatenblatt mit Quellenverweis. Keine
Umschreibungen, keine freien Formulierungen. Zusatz-Spalte `warum_sinnvoll_quelle`
mit „IDEAL-Bullet 3" oder „WARUM Absatz 2" o. ä. für spätere
Audit-Nachvollziehbarkeit.

Grund: § 3.6.1 MONAT-Policy verlangt wortlautgetreue Produktclaims. Frei
formulierte Texte sind Policy-Bruch.

### K-Rollentrennung Antrag

MONAT gegenüber wird Desirée als **fachliche und technische** Owner:in
dargestellt, VERADEX als **rechtliche Hülle** (Vertrag, Betrieb formal,
DSGVO-Verantwortlicher). Formaler Antragsteller ist VERADEX.

### K-Ich-Perspektive Kundinnentexte

Alle Texte, die die Endkundin sieht, sind aus Beraterin-Perspektive geschrieben:
„Kontaktiere mich direkt per WhatsApp" statt „Frag Sina direkt". Beraterin
kann Grußformel + Vorstellungstext im Branding-Bereich (Pro) selbst pflegen,
sonst Standard-Vorlage.

### K-Compliance-Framing

Trennung im Antragsschreiben und in der Systemdokumentation:
- **Sichtbar für Endkundin:** Produktnamen + wörtliche Zitate mit Quellenverweis
  (§ 3.2.5 + § 3.6.1)
- **Intern als Datengrundlage:** Datenblatt-Auswertung für Auswahl-Logik,
  Kontraindikationen, Kombinierbarkeit (für Endkundin nicht sichtbar)

### K-Compliance-Zurückhaltung

Bei rechtlichen Themen im Antrag konservativ formulieren:
- **Keine** Selbstfestlegung zu Art. 9 DSGVO („Kopfhautdaten sind keine
  Gesundheitsdaten" — angreifbar). Neutrale Formulierung „mit erhöhter Sorgfalt
  behandelt".
- **Keine** proaktive Erwähnung von Themen, die MONAT nicht selbst anspricht
  (Urheberrecht Datenblätter, AVV). Öffnet nur Diskussion.

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
