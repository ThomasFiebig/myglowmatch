# Phase-4-Befunde Konsolidiert — 29 Produkte gegen Routing

Stand 2026-06-29. Audit der 29 Produkte, die in Phase 3 (Migration #21)
**nicht** geprüft wurden — restliche Stammdaten + Routing-Aussagen
gegen Hersteller-PDFs.

Quelle pro Welle:
- `audit_phase4_welle_a_befunde.md` (15 routing-aktive Produkte)
- `audit_phase4_welle_b_befunde.md` (14 pool-only Produkte)

## Status-Verteilung

| Klasse | Welle A (15) | Welle B (14) | Gesamt (29) |
|---|---|---|---|
| 🟢 PDF-konform | 11 | 7 | **18** |
| 🟡 Stammdaten-Edit empfohlen | 3 | 7 | **10** |
| 🔴 Routing-Bug (V1/V5/V6-Klasse) | 1* | 0 | **0** echt |

\* Welle A: `restore_leave_in` initial 🔴 klassifiziert wegen „REQ-23
ohne haarstärke-Trigger könnte auf `fein` feuern". Sanity-Check
relativiert auf 🟡: Node 08 (Pool-Filter) wendet `haarstaerke`-Stammdaten
**vor** Node 11 (REQ-Bau) an → `restore_leave_in` fällt bei
`fein`-Profilen aus dem Pool, REQ-23 kann es nicht „direkt setzen".
Verifiziert durch Pre-Lauf: Maria (fein) hatte kein restore_leave_in,
Vivien (dick) hatte's. **Routing korrekt, Defense-in-Depth-Verbesserung
optional.**

**Damit: 0 echte 🔴-Routing-Bugs in den 29 Produkten.**

## Drei wiederkehrende 🟡-Muster

### Muster 1 — `haarwuchs`-Inflation (Welle B)

Betroffen: `ir_clinical_shampoo`, `ir_clinical_spuelung`.

PDFs sagen „Haarausfall reduzieren" + „Verdichtung" — das ist
**Anti-Verlust**, nicht aktives Wachstum. K-04 nicht erfüllt.

**Routing-Effekt aktuell: keiner.** `haarwuchs` ist nicht als
care_goal im Frontend, nicht in Routing-Regeln, nicht in
map_profil_funktion. Toter Code in den Stammdaten. Edit ist
Sheet-Hygiene, kein Routing-Fix.

### Muster 2 — `reparatur`-Inflation (Welle B)

Betroffen: `rejuvabeads` (sogar als HAUPTfunktion!),
`revitalize_spuelung`, `revive_shampoo`, `smoothing_tiefenbehandlung`.

PDFs sagen „schützt", „Haarbruch vorbeugen", „versiegelt" —
Prävention oder Symptom-Kontrolle, nicht Reparatur beschädigter
Strukturen. K-04 nicht erfüllt.

**Routing-Effekt: latent vorhanden.** `reparatur` ist Frontend-
care_goal-Wert (`src/data/questions.ts`). Bei einem Profil wie
`mittel + reparatur-Goal + MID` würde z.B. revive_shampoo (das
VOLUMEN-Shampoo!) für den reparatur-Match unverdient punkten.
In den aktuellen 13 Test-Profilen kein Hit — Sarah und Sina haben
reparatur+HIGH, da dominiert Bond-IQ-Pool. Aber für MID+reparatur-
Profile fehlt die Differenzierung. **Echte Empfehlungs-Qualitäts-
Schwäche, latentes Risiko.**

### Muster 3 — `essig_spuelung.ausschluss_bei` widersprüchlich (Welle B)

`ausschluss_bei=normal,trocken,juckend_empfindlich` widerspricht
direkt PDF-Header „Alle Haartypen" + zentralen Feuchtigkeits-Bullets.
Außerdem Sheet-intern paradox: `trocken` steht GLEICHZEITIG in
`haarzustand` UND `ausschluss_bei`.

**Routing-Effekt: essig_spuelung wird in vielen Profilen ausgeschlossen,
wo es laut PDF passen würde.** Korrektur: `ausschluss_bei=juckend_empfindlich`.

## Welle-A-Detail-Befunde (🟡)

### `fohncreme` (Welle A)

`ausschluss_bei=wellig,lockig,kraus` widerspricht
`locken_geeignet=TRUE` UND PDF-Header „Alle Haartypen und -texturen".
Drei-Wege-Widerspruch in Stammdaten.

**Routing-Effekt: aktuell kontrolliert** — Migration #12 hatte
`fohncreme.ausschluss_bei=wellig,lockig,kraus` bewusst als
Architektur-Verlagerung von CON-09 gesetzt. Das war eine
Beratungs-Heuristik („Föhncreme glättet aktiv — schlecht für Locken").
**Konflikt mit PDF, aber semantisch gewollt.** K-04 sagt: gehört dann
als CON-Regel ins Sheet, nicht als Stammdatum. Architektur-Frage,
nicht Routing-Bug.

### `ir_clinical_kopfhautserum` (Welle A)

`kopfhaut=trocken` nur in IDEAL-Block belegt, nicht im Header-Untertitel.
K-08-Konventions-Frage: gilt IDEAL für FILTER-Spalten? Aktuell sagt K-08
nur „Header-Untertitel" — strikt wäre `trocken` zu streichen, weil nicht
im Header. Pragmatisch ist IDEAL aber „Wer profitiert" und K-03-nahe.

**Routing-Effekt: minimal.** REQ-06 triggert `kopfhaut`-unabhängig auf
`hair_condition=duenn`. Pool-Filter mit `kopfhaut=trocken` würde nur bei
expliziter kopfhaut-Profil-Konstellation greifen — selten.

### `rejuveniqe_oel` (Welle A)

`haarzustand=trocken,glanzlos,frizz` enger als PDF-Header „Alle Haartypen"
(Universal-Öl).

**Routing-Effekt: rejuveniqe_oel würde bei Profilen ohne diese
Zustands-Werte aus dem Pool fallen.** Aber REQ-08 (`oil_need=yes` →
rejuveniqe als Linien-Filter) deckt die primäre Anwendung ab.
Latent: User mit haarzustand=`keine_probleme + glanz-Goal` würde
rejuveniqe_oel nicht bekommen, obwohl PDF „alle Haartypen" sagt.

### `restore_leave_in` (Welle A, von 🔴 zu 🟡 relativiert)

REQ-23 triggert nur auf `pflegelevel_numeric>=2`, ohne haarstärke-
Bedingung. PDF-Header sagt „Mittlere bis dicke Haarstruktur / Für
trockenes Haar".

**Routing-Effekt: keiner** — Pool-Filter (Node 08) wendet
`haarstaerke=mittel,dick` aus Stammdaten vor Node 11 an. Verifiziert:
Maria (fein) hatte pre-#21 kein restore_leave_in, Vivien (dick) hatte's.

**Defense-in-Depth-Empfehlung**: REQ-23 explizit auf `hair_thickness IN
[mittel,dick]` triggern, damit das Routing-Statement selbst die Aussage
trägt. Aktuell ist die Filter-Disziplin nur per Pool-Layer abgesichert.
Optional, nicht dringend.

## Konkrete Stammdaten-Edits (Vorschlag Migration #22)

| Produkt | Spalte | Ist | Soll |
|---|---|---|---|
| essig_spuelung | ausschluss_bei | normal,trocken,juckend_empfindlich | juckend_empfindlich |
| ir_clinical_shampoo | nebenfunktionen | reinigung,farbschutz,**haarwuchs**,staerkend,frische | reinigung,farbschutz,staerkend,frische |
| ir_clinical_spuelung | nebenfunktionen | feuchtigkeit,farbschutz,**haarwuchs**,staerkend,kaemmbarkeit,frische | feuchtigkeit,farbschutz,staerkend,kaemmbarkeit,frische |
| rejuvabeads | hauptfunktion | **reparatur**,versiegelung | versiegelung,staerkend |
| rejuvabeads | nebenfunktionen | glanz,kaemmbarkeit,staerkend,frizz_reduktion | glanz,kaemmbarkeit,frizz_reduktion |
| revitalize_spuelung | nebenfunktionen | feuchtigkeit,staerkend,kaemmbarkeit,**reparatur** | feuchtigkeit,staerkend,kaemmbarkeit |
| revive_shampoo | nebenfunktionen | reinigung,staerkend,feuchtigkeit,kaemmbarkeit,**reparatur** | reinigung,staerkend,feuchtigkeit,kaemmbarkeit |
| smoothing_tiefenbehandlung | nebenfunktionen | kaemmbarkeit,**reparatur** | kaemmbarkeit |

**Optional (Welle-A-Detail, geringere Priorität):**
- ir_clinical_kopfhautserum: kopfhaut=trocken streichen (K-08-strikt)
- rejuveniqe_oel: haarzustand öffnen oder unverändert lassen (Universal-Öl-Charakter im Header)
- restore_leave_in: REQ-23 um haarstärke-Trigger ergänzen (Defense-in-Depth)
- fohncreme: Architektur-Entscheidung — bleibt es Stammdaten-Ausschluss (Migration-#12-Konstrukt) oder zurück als CON-Regel?

## Antwort auf die „kann ich vorstellen?"-Frage

**Ja.** 29 von 29 Produkten gegen PDF geprüft, **0 Trockenshampoo-
Niveau-Bugs**. Die 10 🟡-Funde sind Stammdaten-Inflation oder
Detail-Abweichungen — keine falschen Produkte in falschen Slots, sondern
zu großzügige Funktions-Zuschreibungen (haarwuchs/reparatur), die im
aktuellen Test-Profil-Set keinen sichtbaren Output-Effekt haben.

**Latentes Risiko**: `reparatur`-Inflation bei Volumen-Shampoo
(revive_shampoo) könnte bei einem hypothetischen Profil
`mittel + reparatur-Goal + MID` zur falschen Shampoo-Empfehlung führen.
Sollte vor Live-Skalierung gefixt werden, ist aber für Pilot/Beta-
Vorstellung kein Blocker.

## Empfehlung Migration #22

Reine Stammdaten-Cleanup, 8 Zellen-Edits in `produktdatenbank`:
- 0 Code-Änderungen
- 0 REQ/CON-Änderungen
- Erwartete Drift in 13 Test-Profilen: gering (rejuvabeads-Hauptfunktion-
  Umstellung könnte bei Sina/Sarah-Pool-Scoring Verschiebungen geben,
  aber rejuvabeads ist in der aktuellen Routine keiner Test-Profile)
- Coverage-Profil-Vorschlag: `mittel + reparatur-Goal + MID` als 14.
  Test-Profil, um den latenten Bug-Bereich abzudecken

**Nicht-blockierend für Vorstellung.** Kann nach dem ersten Partner-
Feedback gemacht werden.
