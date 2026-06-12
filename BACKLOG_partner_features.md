# Backlog — Partner-Output-Steuerung & Kundenkommunikation

Gesammelt 2026-06-11. Noch nicht priorisiert, kein Umsetzungsdatum.

## F-01 — Routing-Toggle pro Partner
Partner wählt in Einstellungen:
- `direkt_an_kunde`: Ergebnis-Mail geht automatisch an Kunde (aktuelles Verhalten)
- `nur_an_partner`: Nur Partner bekommt Produktliste, Kunde bekommt keine Mail
- `beide`: Partner + Kunde erhalten Mail

Technisch: Feld `mail_routing` in Partner-Datenbank (aktuell hardcoded in Node 17), Abfrage vor Mail-Versand in Node 17/18/18b.

## F-02 — Vorformulierte WhatsApp-Nachricht für Partner
Bei `nur_an_partner`: Partner-Mail enthält fertigen WhatsApp-Text mit Produktliste + persönlicher Ansprache als Deeplink (`https://wa.me/KUNDENNUMMER?text=...`). 1-tap weiterleitbar. Text partner-gebrandet. Optional mehrere Textvarianten (professionell / herzlich / kurz).

## F-03 — Anwendungs-PDF (Spickzettel) für Kunden
Personalisiertes A4-PDF pro Kunde, automatisch generiert:
- Kundenname + Haartyp oben
- Pro Produkt: Name, Schritt-Nummer, Anwendungsanleitung (aus `anwendung`-Spalte), Häufigkeit
- Partner-Branding optional (Logo, Name, Kontakt)
- Druckoptimiert (schwarz-weiß tauglich, klare Struktur)
- Auslieferung: Attachment in Kunden-Mail oder Download-Link

Technische Optionen:
- Option A (einfach): HTML-Template → PDF via Puppeteer in n8n-Execute-Node → Base64 an Mail-Node
- Option B (sauber): Vercel-API-Route `/api/generate-pdf` → n8n HTTP-Request
- Option C (zero-infra): Print-CSS (`@media print`) im HTML-Mailblock — Kunde druckt direkt aus Mail ← Empfehlung für ersten Schritt

## F-04 — Anwendungsreihenfolge visuell
Ergänzung zu F-03: Routine als Morgen/Abend/Wöchentlich-Darstellung im PDF oder in der Mail. Braucht neue Spalte `anwendungszeit` in produktdatenbank (morgens / abends / wöchentlich / bei_bedarf).

## F-05 — PDF-Generierung technisch
Siehe F-03 Technische Optionen. Erst angehen wenn F-03-Konzept entschieden.

## F-06 — Persönlicher Mail-Ton (Beraterin schreibt, nicht System)
Kunden-Mail fühlt sich an wie persönliche Nachricht der Beraterin:
- Schreibstil: locker, erste Person ("Ich hab mir deine Antworten angeschaut und…")
- Kein System-Sprache ("Deine Routine wurde berechnet")
- Beraterin-Name + Foto prominent, nicht als Fußnote
- Betreff wie echte Nachricht ("Hey [Name], ich hab was für dich 💛")
- Kurze persönliche Einleitung passend zum Hauptproblem
- Technisch: Claude in Node 17 formuliert Mail in Stimme der Beraterin statt Template-Befüllung. Partner kann optional Stil-Satz in Einstellungen hinterlegen ("Ich schreibe herzlich und mit Emojis") als Kontext.

## Empfohlene Reihenfolge
1. F-01 + F-02 (reines Sheet/Node-17-Feature, kein neues Infra)
2. F-06 (Node-17-Umbau, Claude-Prompt-Anpassung)
3. F-03 mit Option C (Print-CSS, kein PDF-Generator)
4. F-04 (braucht erst `anwendungszeit`-Spalte im Audit)
5. F-05 wenn F-03 Option C nicht ausreicht
