# Phase-5-Audit: Trigger-Regeln vs. PDF-Belegung

**Datum:** 2026-07-01
**Scope:** 22 REQ-Regeln in `map_slot_rules` (nur Regeln mit `produkt_key`-Filter — pool-only-Produkte via Scoring nicht Teil dieses Audits).
**Methode:** Pro Regel Trigger-Bedingung mit PDF-Header-Untertitel / IDEAL-Bullet / WARUM ES FUNKTIONIERT abgleichen (Konventionen K-06/K-07/K-08).

## Gesamt-Ampel

| Klasse | Anzahl | Regeln |
|---|---|---|
| 🟢 sauber | 15 | REQ-02, REQ-05, REQ-06, REQ-07, REQ-11, REQ-11b, REQ-12, REQ-14, REQ-17, REQ-18, REQ-19, REQ-19b, REQ-21, REQ-22, REQ-24, REQ-30, REQ-04b, REQ-16b |
| 🟡 Präzisierung sinnvoll | 6 | REQ-03, REQ-08, REQ-11c, REQ-13, REQ-16, REQ-17b |
| 🟡 Design-Choice (Routine-Skalierung, nicht PDF-Widerspruch) | 2 | REQ-20, REQ-23 |
| 🔴 Trigger widerspricht PDF | 0 | — |

**Kein echter Routing-Bug**, aber 6 Regeln haben eine dünne PDF-Basis, die man schärfen könnte.

## Priorisierte Handlungs-Empfehlungen

### Priorität 1 — REQ-16 (moxie_mousse Halt-Trigger)
**Befund:** Regel schließt `hair_structure ∈ {lockig, kraus}` aus, PDF sagt aber Header „Alle Haarstrukturen" und FAQ „für feines bis mittleres Haar". Lockenträgerinnen mit aufwendigem Styling + Halt-Wunsch bekommen keine Mousse-Empfehlung, obwohl PDF sie explizit adressiert.
**Vorschlag:** Struktur-Bedingung entfernen — Trigger: `styling_effort = aufwendiges_styling` AND `hair_thickness ∈ {fein, mittel}`.

### Priorität 2 — REQ-03 (super_feuchtigkeitsmaske als Repair-Maske)
**Befund:** Trigger feuert nur bei `stark_geschaedigt / gefaerbt / blondiert` + HIGH, PDF nennt aber nur „trockenes Haar regenerieren" — kein Schaden-Bezug. Kundinnen mit normalem trockenem Haar + HIGH-Level bekommen die Maske nicht, obwohl sie im IDEAL-Bullet stehen.
**Vorschlag:** Trigger umstellen auf `hair_condition contains trocken` AND `pflegelevel_numeric >= 3`, oder Alternativregel REQ-03b für generisch-trocken.

### Priorität 3 — REQ-11c (Curl-Creme bei gelegentlicher Hitze)
**Befund:** „mit Diffusor föhnen" ist im PDF genannt, aber nicht als eigenständiger Empfehlungs-Grund. Migration #21 V5 hatte die Regel schon PDF-abgesegnet, der Beleg ist aber implizit.
**Vorschlag:** Regel behalten (semantisch sinnvoll), aber Doku-Zeile in `map_derived_variables` ergänzen: „Diffusor als PDF-belegter Hitze-Use-Case für Curl-Creme".

### Priorität 4 — REQ-13 (Curl-Auffrischer + seltene Wäschen)
**Befund:** „Curl-Reaktivator für den zweiten Tag" ist belegt, aber `wash_frequency ≠ taeglich` als expliziter Trigger nicht wörtlich im PDF.
**Vorschlag:** Wortlaut PDF-Header-Untertitel um „Zwischen-Wash-Anwendung" ergänzen (MONAT-Anfrage), ODER Trigger lockern auf nur `curl_priority = beides` (verliert wenig Präzision, weil `wants_full_curl_line` alle diese Kundinnen sowieso erfasst).

### Priorität 5 — REQ-08 / REQ-17b (rejuveniqe_oel Öl-Bedarf)
**Befund:** PDF fokussiert Glanz, Frizz, Feuchtigkeit-Erhalt. „deutlich_trocken" / „leicht_trocken" als Öl-Bedarfs-Trigger ist plausible Heuristik, aber nicht wörtlich.
**Vorschlag:** REQ-08 + REQ-17b konsolidieren mit REQ-17 (Glanz-Ziel) — Kundinnen mit trockenen Spitzen kreuzen typischerweise auch „Glanz" an, dann greift REQ-17 sowieso. Doppel-Trigger könnte weg.

## Design-Choice, kein PDF-Bug

### REQ-20 (scalp_comfort_serum bei MID/HIGH)
`pflegelevel_numeric >= 2` ist keine PDF-Aussage, sondern **Routine-Umfangs-Steuerung**: bei minimaler Routine soll nicht auch noch ein Tages-Serum drin sein. Bewusste Design-Entscheidung, nicht anfassen.

### REQ-23 (restore_leave_in als Fallback)
`pflegelevel_numeric >= 2` + `requires_not = REQ-07,REQ-18,REQ-21` = „Wenn kein anderes Leave-In gefunden wird, nimm RESTORE". Das ist Fallback-Logik, nicht produkt-spezifischer Trigger. PDF-Beleg über Zielgruppe „Leave-In für trockenes Haar" reicht — der Trigger ist Slot-Belegung, nicht Produkt-Empfehlung.

## Nicht auditiert (Scope)

- **CON-Regeln** (`map_conflict_rules`, 12 Zeilen) — pool-only-Konflikte, kein Trigger im engeren Sinn.
- **22 pool-only-Produkte** ohne REQ-Trigger — laufen über Scoring in Node 12, dort greift Phase-4-Audit (Stammdaten-Konformität).

## Nächste Schritte

1. Migration #24 vorbereiten für Priorität 1+2 (REQ-16 + REQ-03).
2. Priorität 3-5 als Doku-Refresh / optionale Präzisierung ohne Live-Deploy.
