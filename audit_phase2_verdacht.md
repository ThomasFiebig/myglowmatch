# Phase-2-Plausibilitäts-Check Routing-Regeln

Stand 2026-06-28, basiert auf `audit_phase1_inventar.md` (58 Regeln).

**Methode**: pro Regel innere Plausibilität geprüft — passt der Trigger zur
Filter-/Produkt-Folge? Gibt es Inkonsistenzen zwischen Regeln? Gibt es
offensichtliche Profil-Lücken? **Ohne PDF-Lesen** (das ist Phase 3 nur
für Verdachtsfälle).

## Ampel

| Symbol | Bedeutung |
|---|---|
| 🟢 | plausibel, kein Phase-3-Bedarf |
| 🟡 | PDF-Verifikation in Phase 3 sinnvoll, kein klarer Bruch |
| 🔴 | klarer Plausibilitäts-Bruch, Phase 3 hat hohe Priorität |

## Übersicht

| Kategorie | 🟢 | 🟡 | 🔴 |
|---|---|---|---|
| map_derived_variables (19) | 16 | 3 | 0 |
| map_slot_rules aktiv (29) | 25 | 4 | 0 |
| map_conflict_rules aktiv (3) | 3 | 0 | 0 |
| map_pflegelevel_overrides (4) | 4 | 0 | 0 |
| **Summe (55)** | **48** | **7** | **0** |

Kein 🔴-Fund — der Trockenshampoo-Bug-Pattern hat sich nicht repliziert.
7 Verdachtsfälle für Phase 3.

---

## Verdachtsfälle für Phase 3

### V1 🟡 — Bond-IQ-Routing fasst `gefaerbt` nicht an

**Regeln**: `needs_repair_focus` (Trigger: `stark_geschaedigt` ODER
`blondiert`) — konsumiert von REQ-02 (Bond-IQ-Spülung), REQ-03
(Bond-IQ/Reparatur-Maske), REQ-21 (Bond-IQ Leave-In), REQ-22 (Bond-IQ
Night & Day Serum).

**Beobachtung**: `wants_intense_care` zählt sowohl `gefaerbt` als auch
`blondiert` als Auslöser für Intensitäts-Tiebreaker (Node 12 v4 Stufe
11). `needs_repair_focus` schließt `gefaerbt` aber aus. Inkonsistenz
zwischen den beiden Flag-Definitionen.

**Hypothese**: Gefärbtes Haar (ohne Blondierung) bekommt kein Bond-IQ-
Routing — falls Bond-IQ-PDFs „Färbeschäden" als Zielgruppe nennen, ist
das eine Lücke. Falls Bond-IQ explizit nur für Blondierung/starke
Schäden gedacht ist, ist die Inkonsistenz okay und die Doku könnte das
festhalten.

**Phase-3-Aufgabe**: bond_iq_leave_in.pdf, bond_iq_night_day_serum.pdf,
bond_iq_shampoo.pdf, bond_iq_spuelung.pdf lesen — gibt's „gefärbt" /
„Färbeschäden" in WARUM/IDEAL/FAQ-Sektionen?

**Test-Profile-Bezug**: Bianca (`trocken+gefaerbt`, MID) bekäme bei
Aufnahme der Regel REQ-02 (Bond-IQ-Spülung), REQ-21 (Bond-IQ-Leave-In).

---

### V2 🟡 — `detangling_need` ignoriert `kraus` ohne `deutlich_trocken`

**Regel**: `detangling_need` enum.
- `stark_verfilzt`: `haarbruch` ODER `spliss` ODER (`kraus` UND
  `deutlich_trocken`)
- `leicht_verfilzt`: (`trocken` UND NICHT `haarbruch`) ODER (`lockig`
  UND NICHT `keine_probleme`)
- sonst `problemlos`

**Beobachtung**: Krauses Haar mit z.B. `frizz` oder normalem Spitzen-
Zustand fällt in `problemlos`. `lockig` matcht den `leicht_verfilzt`-
Zweig, `kraus` nicht — obwohl `kraus` strukturbedingt verfilzungs-
anfälliger als `lockig` ist.

**Hypothese**: Lücke. Profil wie Sina (`kraus+juckend+schuppig`, ohne
`deutlich_trocken`) bekommt kein Entwirrungsspray.

**Phase-3-Aufgabe**: entwirrungsspray.pdf (oder das equivalent in MONAT
Curl-Linie) — ist krauses Haar Zielgruppe?

**Test-Profile-Bezug**: Sina (`kraus, juckend+schuppig`), Lena
(`kraus, gefaerbt+frizz`) — beide aktuell ohne entwirrungsspray-
Routing-Trigger über detangling_need (Sina könnte über REQ-23
restore_leave_in bei MID/HIGH greifen).

---

### V3 🟡 — `styling_goal_halt` triggert auf glatt/wellig, moxie_mousse-PDF spricht Locken an

**Regel**: `styling_goal_halt` = TRUE wenn `aufwendiges_styling` UND
`fein|mittel` UND `glatt|wellig`. Konsumiert von REQ-16 (optional →
moxie_mousse styling_1).

**Beobachtung**: moxie_mousse-Header (laut HANDOVER K-08-Beleg) ist
„Volumen-Mousse für lockiges, krauses, welliges Haar". Der Trigger
matcht aber explizit `glatt|wellig` (lockig/kraus haben in der Regel
nichts zu suchen). Wellig ist Schnittmenge, glatt nicht.

**Hypothese**: glatt+aufwendig+fein/mittel → moxie_mousse ist
PDF-kompatibel? Header schließt glatt nicht explizit aus.

**Phase-3-Aufgabe**: moxie_mousse.pdf — was sagt FAQ/IDEAL für glattes
Haar?

**Test-Profile-Bezug**: Julia (`glatt+fein, gelegentlich-Hitze`) +
care_goals enthalten `halt` und sie styled aufwendig → würde REQ-16
treffen.

---

### V4 🟡 — `REQ-06` triggert auf `hair_condition contains duenn` — gibt es diesen Wert?

**Regel**: REQ-06 trigger_flag=`hair_condition_contains`, trigger_wert
=`duenn`. Folge: `ir_clinical_kopfhautserum` in Slot `kopfhaut`.

**Beobachtung**: Standard-`hair_condition`-Optionen in Frontend
(questions.ts) sind typischerweise wie `trocken`, `fettig`, `frizz`,
`stark_geschaedigt`, `gefaerbt`, `keine_probleme`. `duenn` als
hair_condition-Wert ist mir aus dem HANDOVER nicht erinnerlich.

**Hypothese**: Entweder Toter Trigger (falsche Spaltenreferenz —
Dünn-Werdung ist eher `hair_thickness` oder eine eigene Frage) oder
historisch existierender Wert, der heute im Frontend fehlt.

**Phase-3-Aufgabe**: `src/data/questions.ts` checken — gibt es einen
Frontend-Optionen-Wert `duenn`? Falls nein, REQ-06 ist Toter Code.
ir_clinical_kopfhautserum.pdf parallel zur Zielgruppen-Klarstellung.

**Test-Profile-Bezug**: Kein Test-Profil scheint REQ-06 zu treffen
(kein Profil hat `duenn` in den dokumentierten hair_condition-Werten).

---

### V5 🟡 — `REQ-11` blockt curl_creme bei `heat_use=maybe`

**Regel**: REQ-11 trigger `needs_curl_care=TRUE AND heat_use=no` →
curl_creme styling_1. REQ-04 (Hitzeschutz) hat `requires_not =
REQ-11,REQ-11b,REQ-04b` — d.h. REQ-04 weicht WENN curl_creme greift.

**Beobachtung**: Nach Migration #18 ist `heat_use` 3-stufig
(yes/maybe/no). REQ-11 triggert nur bei `heat_use=no`. Bei
`heat_use=maybe` (gelegentlich Hitze) greift REQ-04, weil REQ-11 nicht
gefeuert hat → kein curl_creme styling_1. Außer der User wählt
`curl_priority=beides` → REQ-11b triggert auf `wants_full_curl_line`
ohne heat_use-Filter und gibt curl_creme.

**Hypothese**: Locken-User mit gelegentlicher Hitze und
`mehr_definition`-Priorität (nicht `beides`) bekommt kein curl_creme
styling_1, sondern Hitzeschutz. Das ist möglicherweise gewollt
(REQ-04b ist die explizite Kombi-Lösung für Locken+Glätt-Wunsch+Frizz
+ Hitze), aber für Locken+Definition+gelegentliche Hitze ohne Frizz
keine spezifische Lösung. Curl-Routing fällt aus.

**Phase-3-Aufgabe**: curl_creme.pdf — verträgt sich curl_creme mit
Föhn-/Glätteisen-Gebrauch (also: könnte REQ-11 auf `heat_use!=yes`
erweitert werden)?

**Test-Profile-Bezug**: Maria (`wellig+fein, MID, mehr_definition`)
oder Bianca (`wellig, juckend+empfindlich, trocken+gefaerbt`) — wenn
einer von beiden heat_use=maybe hat (Migration #18-Modus), könnte
curl_creme aus styling_1 fallen.

---

### V6 🟡 — `REQ-19` Volumen-Styling nur bei `hair_thickness=fein`

**Regel**: REQ-19 trigger `styling_goal_volumen=TRUE AND
hair_thickness=fein` → moxie_mousse|volumen_spray (styling_1 optional).

**Beobachtung**: Volumen-Ziel bei `mittel` oder `dick` triggert kein
spezifisches Volumen-Styling (außer User ist Locken+`mehr_volumen` →
REQ-16b). Maria (`wellig+fein, MID, mehr_definition`) hat `fein` aber
kein Volumen-Ziel, also greift REQ-19 nicht. Profile mit `mittel +
volumen`-Ziel haben keinen Volumen-Slot.

**Hypothese**: Volumen-Effekt physikalisch am stärksten bei feinem
Haar, deshalb bewusst auf `fein` beschränkt? Oder Lücke?

**Phase-3-Aufgabe**: moxie_mousse.pdf / volumen_spray.pdf — Zielgruppe
auch `mittel`? Header K-08-Beleg könnte schon reichen.

**Test-Profile-Bezug**: Aktuell kein Test-Profil mit `mittel + volumen
+ glatt|wellig` definiert. Wäre ein Coverage-Loch.

---

### V7 🟡 — `wants_intense_care` Asymmetrie zu `needs_repair_focus` (siehe V1)

Eigentlich Teil von V1 — beide nutzen `hair_treatments` aber
unterschiedlich. Phase-3-Frage ist dieselbe Bond-IQ-PDF-Frage.

Wenn V1 geklärt ist, ist V7 implizit beantwortet. Kein eigener
PDF-Read nötig.

---

## Geprüft und 🟢

Alles übrige (48 Regeln). Beispiele besonders kritischer Prüfungen:

- **REQ-14** (the_champ): Trigger `needs_dry_shampoo=TRUE` (Migration
  #17 PDF-belegt, Spec passt jetzt zum Trigger). Reason-Text in
  diesem Audit auf den Migration-#17-Stand synchronisiert.
- **CON-13** (smoothing_fohn_spray bei Locken+Frizz): Trigger und
  Match-Produkt sind plausibel, in Migration #14 PDF-belegt.
- **REQ-04b** (smoothing_fohn_spray bei prefers_straight+frizz+heat):
  Migration-#16-Konstrukt, PDF-belegt (Hitze + Frizz in einem
  Produkt).
- **PFL-OV-01..04**: Floor/Cap-Logik mit Pflegelevel-Schwellen ist
  konsistent zu HANDOVER-Konventionen.
- **REQ-30 + REQ-MIN-NO-OPT** (minimal-Routine): Zusammenspiel
  Monat-Black-Override und Optional-Suppress logisch sauber.
- **Curl-Routing-Cluster** (REQ-11/12/13/11b/16b + needs_curl_care +
  prefers_straight + wants_full_curl_line + wants_curl_volume +
  needs_curl_gelee_styling): mit Migrationen #15/#16/#20 konsistent
  durchgebaut, jede Curl-Variante hat einen designierten Pfad.

---

## Empfehlung für Phase 3

Reihenfolge nach Verdachts-Tragweite:

1. **V4** (REQ-06 / `duenn`) — schneller Code/Sheet-Check, evtl. Toter
   Code. 5 Min.
2. **V1+V7** (Bond-IQ + gefaerbt) — 4 PDFs lesen, ggf. derived-
   variable-Edit. Hohe Tragweite (4 REQ-Regeln betroffen).
3. **V2** (detangling_need + kraus) — 1 PDF lesen.
4. **V5** (REQ-11 + heat_use=maybe) — 1 PDF lesen, evtl. trigger-Edit.
5. **V3** (styling_goal_halt + glatt) — 1 PDF lesen (moxie_mousse).
6. **V6** (REQ-19 + hair_thickness=mittel) — 2 PDFs lesen
   (moxie_mousse + volumen_spray).

Insgesamt ~7–9 PDFs in Phase 3 — gut delegierbar an Agent (siehe
Memory: PDF-Wellen ab ~10 PDFs an Agent, hier knapp drunter).
