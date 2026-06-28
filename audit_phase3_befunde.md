# Phase-3-Befunde Routing-Regel-vs-PDF-Audit

Stand 2026-06-28. PDF-Lesung von 8 Datenblättern + Frontend-Check
`src/data/questions.ts`.

## Status-Übersicht

| Fall | Status | Migration-Bedarf |
|---|---|---|
| V1 | 🔴 Bug bestätigt | Edit `needs_repair_focus` |
| V2 | 🟡 Asymmetrie PDF-widrig | Edit `detangling_need` |
| V3 | 🟢 Routing okay | — |
| V4 | 🟢 Routing okay (Coverage-Lücke) | — |
| V5 | 🔴 Bug bestätigt | Edit REQ-11 |
| V6 | 🔴 Bug bestätigt | Edit REQ-19 |
| V7 | 🟢 (implizit durch V1) | — |

**3 Bugs + 1 PDF-widrige Asymmetrie → 4 Sheet-Edits, keine Code-Änderungen.**

---

## V1 — Bond-IQ-Linie & gefärbtes Haar (🔴 Bug)

**Aktueller Trigger** (`map_derived_variables.needs_repair_focus.regel_json`):
```json
{"or":[
  {"includes":["normalized.hair_condition","stark_geschaedigt"]},
  {"eq":["normalized.hair_treatments","blondiert"]}
]}
```

**PDF-Belege:**
- `bond_iq_leave_in.pdf` S.1 (WARUM): "Egal, ob Du Dein Haar regelmäßig
  stylst, **färbst** oder einfach stärkeres, gesünder aussehendes Haar
  möchtest"
- `bond_iq_leave_in.pdf` S.1 (Bullet): "Bekämpft Schäden durch
  **chemische Behandlungen**, Hitze-Styling, Umwelteinflüsse..."
- `bond_iq_shampoo.pdf` S.1 (WARUM): "eignet sich für die tägliche
  Haarwäsche – selbst bei **coloriertem oder chemisch behandeltem
  Haar**."
- `bond_iq_spuelung.pdf` S.1 (WARUM): "für sichtbar weicheres,
  glatteres und widerstandsfähigeres Haar – selbst nach dem **Färben**,
  Blondieren oder Hitzestyling."
- `bond_iq_night_day_serum.pdf` S.1 (Bullet): "hilft, Schäden durch
  Hitzestyling, **chemische Behandlungen** oder Umwelteinflüsse
  rückgängig zu machen" (Studien-Basis aber "blondiertes
  kaukasisches Haar" — Fußnote)

**Migration-Empfehlung**: `hair_treatments` als Trigger auf
`in [gefaerbt, blondiert]` erweitern.

```json
{"or":[
  {"includes":["normalized.hair_condition","stark_geschaedigt"]},
  {"in":["normalized.hair_treatments",["gefaerbt","blondiert"]]}
]}
```

**Folge**: Bianca (`trocken+gefaerbt`, MID) bekäme REQ-02 (Bond-IQ-
Spülung), REQ-21 (Bond-IQ-Leave-In). Konsistent mit
`wants_intense_care`, das `gefaerbt` bereits zählt — Asymmetrie aufgelöst.

---

## V2 — entwirrungsspray & krauses Haar (🟡 Asymmetrie)

**Aktueller Trigger** (`map_derived_variables.detangling_need.regel_json`,
relevanter Zweig `leicht_verfilzt`):
```json
{"or":[
  {"and":[
    {"includes":["normalized.hair_condition","trocken"]},
    {"not":{"includes":["normalized.hair_condition","haarbruch"]}}
  ]},
  {"and":[
    {"eq":["normalized.hair_structure","lockig"]},
    {"not":{"includes":["normalized.hair_condition","keine_probleme"]}}
  ]}
]}
```

**PDF-Belege:**
- `entwirrungsspray.pdf` S.1 (Header-Untertitel, K-08): "Schäden,
  Haarbruch & Spliss / **Alle Haartypen** / **Alle Haarstrukturen** /
  Vorbereitung"
- WARUM/IDEAL/FAQ: keine wörtliche Erwähnung von "kraus"/"krauses Haar".

**Befund**: Header-Untertitel "Alle Haarstrukturen" deckt nach K-08
auch `kraus` ab. Die `leicht_verfilzt`-Regel adressiert `lockig` ohne
`keine_probleme` — krauses Haar (struktur-bedingt verfilzungs-
anfälliger als lockig) muss derselben Logik folgen.

**Migration-Empfehlung**: `leicht_verfilzt`-Zweig um `kraus` erweitern.

```json
{"or":[
  {"and":[
    {"includes":["normalized.hair_condition","trocken"]},
    {"not":{"includes":["normalized.hair_condition","haarbruch"]}}
  ]},
  {"and":[
    {"in":["normalized.hair_structure",["lockig","kraus"]]},
    {"not":{"includes":["normalized.hair_condition","keine_probleme"]}}
  ]}
]}
```

**Folge**: Sina (`kraus, juckend+schuppig`) und Lena (`kraus,
gefaerbt+frizz`) bekommen REQ-18 (Entwirrungsspray optional). Achtung:
REQ-23 (restore_leave_in) hat `requires_not=REQ-07,REQ-18,REQ-21` —
Sina/Lena verlieren restore_leave_in dadurch. Drift-Risiko in Test
prüfen.

---

## V3 — moxie_mousse & glatt (🟢 okay)

**PDF-Belege:**
- `moxie_mousse.pdf` S.1 (Header-Untertitel, K-08): "...Locken & Wellen
  / **Alle Haartypen** / Alle Haarstrukturen / Styling"
- `moxie_mousse.pdf` S.1 (FAQ): "MONAT STUDIO ONE™ The Moxie™ Volumen-
  Mousse ist perfekt für **alle Haartypen** und -strukturen."
- `moxie_mousse.pdf` S.1 (FAQ): "Es verleiht **feinem bis mittlerem
  Haar** Fülle und Volumen und sorgt bei Locken oder Wellen für
  definierte Form und Frizz-Kontrolle."

**Befund**: "alle Haartypen" ist FAQ-belegt (K-06-konform) und nicht
nur Tagline. styling_goal_halt darf weiter auf `glatt|wellig` feuern.

**Migration-Empfehlung**: keine. Routing korrekt.

---

## V4 — REQ-06 (`hair_condition=duenn`) (🟢 okay)

**Frontend-Beleg** (`src/data/questions.ts` Z.125):
```ts
{ value: "duenn", label: "dünner werdendes Haar" }
```

**Befund**: `duenn` ist gültiger `hair_condition`-Wert (Frage 4,
Mehrfachauswahl). REQ-06 ist semantisch funktional. Kein Test-Profil
der aktuellen 11 wählt `duenn` → Coverage-Lücke, kein Bug.

**Migration-Empfehlung**: keine. Optional: Test-Profil mit
`duenn`-Auswahl hinzufügen, um REQ-06 ins Slot-Drift-Monitoring
einzubinden.

---

## V5 — REQ-11 (curl_creme) bei `heat_use=maybe` (🔴 Bug)

**Aktueller Trigger** (`map_slot_rules.REQ-11`):
- trigger_flag: `needs_curl_care`, trigger_wert: `TRUE`
- trigger_flag2: `heat_use`, trigger_wert2: `no`
- filter: `curl_creme`, slot_typ: `styling_1`

**PDF-Belege:**
- `curl_creme.pdf` S.6 (WIE MAN ES BENUTZT — Lockendefinierende Creme):
  "Nicht ausspülen. Nach Belieben **lufttrocknen, mit Diffuser föhnen
  oder stylen**."
- `curl_creme.pdf` S.7 (Gelée): "Nach Belieben lufttrocknen, mit einem
  Diffusor föhnen oder stylen."

**Befund**: curl_creme ist mit Föhn explizit PDF-kompatibel. Aktuelle
Beschränkung auf `heat_use=no` schließt Locken-Träger:innen mit
gelegentlicher Hitze unnötig vom Curl-Routing aus.

**Migration-Empfehlung**: REQ-11-Trigger auf `heat_use != yes`
erweitern. Da der bestehende equals-Operator das nicht direkt
ausdrückt, zwei Optionen:

- **Option A (kleinster Eingriff)**: zweite Regel REQ-11c mit
  `heat_use=maybe`, gleicher Filter `curl_creme`, gleicher slot_typ
  `styling_1`. REQ-04 `requires_not` um REQ-11c ergänzen.
- **Option B (sauberer)**: neue derived variable
  `can_use_curl_creme = needs_curl_care AND heat_use != yes`, REQ-11
  trigger darauf umstellen.

Empfehlung Option A — weniger Schema-Bewegung, parallel zur
bestehenden REQ-11/11b-Struktur. Option B ist eleganter, aber lohnt
sich erst, wenn weitere Trigger das gleiche Pattern brauchen.

**Folge**: Maria/Bianca etc. mit `wellig+heat_use=maybe` bekämen
curl_creme + Hitzeschutz parallel. Test-Coverage prüfen — kein
aktuelles Profil hat genau diese Konstellation.

---

## V6 — REQ-19 Volumen-Styling nur bei `fein` (🔴 Bug)

**Aktueller Trigger** (`map_slot_rules.REQ-19`):
- trigger_flag: `styling_goal_volumen`, trigger_wert: `TRUE`
- trigger_flag2: `hair_thickness`, trigger_wert2: `fein`
- filter: `moxie_mousse|volumen_spray`, slot_typ: `styling_1`

**PDF-Belege:**
- `moxie_mousse.pdf` S.1 (FAQ): "...verleiht **feinem bis mittlerem
  Haar** Fülle und Volumen..."
- `moxie_mousse.pdf` S.1 (FAQ): "alle Haartypen geeignet"
- `volumen_spray.pdf` S.1 (Header-Untertitel, K-08): "Volumen und
  Dichte / **Feines bis mittleres Haar** / Alle Haartypen und -texturen
  / Styling"
- `volumen_spray.pdf` S.1 (WARUM): "schwereloses Volumen sowie
  langanhaltende Fülle und Sprungkraft für **feines, plattes Haar**"
  (Hauptfokus fein, aber Header sagt explizit "feines bis mittleres")

**Befund**: Beide Filter-Produkte nennen "fein bis mittel" explizit.
Aktuelle Beschränkung auf `fein` widerspricht beiden Datenblättern.

**Migration-Empfehlung**: REQ-19-trigger_wert2 von `fein` auf
`fein|mittel` (wenn map_slot_rules pipe-Werte unterstützt — Vorbild
PFL-OV-01 `regelmaessig|sehr_haeufig` mit `in_list`-Operator). Da
REQ-Trigger-Operator default `equals` ist, evtl. neue Regel REQ-19b
mit `mittel` (Option A) oder neue derived variable
`hair_thickness_volumen_friendly = hair_thickness in [fein, mittel]`
(Option B). Empfehlung Option A (analog V5).

---

## V7 — implizit durch V1

`wants_intense_care` zählt bereits `gefaerbt`. Nach V1-Fix sind
`needs_repair_focus` und `wants_intense_care` konsistent.

---

## Konsolidiertes Migrations-Paket (Vorschlag)

**Migration #21 — PDF-Audit-Korrekturen** (4 Sheet-Edits, kein
Code-Edit, kein Schema-Edit):

| Edit | Tab | Zeile/Spalte | Alt → Neu |
|---|---|---|---|
| V1 | map_derived_variables | needs_repair_focus.regel_json | `eq`-Klausel auf `blondiert` → `in`-Klausel `[gefaerbt, blondiert]` |
| V2 | map_derived_variables | detangling_need.regel_json | `lockig`-Klausel im `leicht_verfilzt`-Zweig → `in [lockig, kraus]` |
| V5 | map_slot_rules | append_row REQ-11c (heat_use=maybe, gleicher Rest wie REQ-11) + REQ-04.requires_not um REQ-11c ergänzen |
| V6 | map_slot_rules | append_row REQ-19b (hair_thickness=mittel, gleicher Rest wie REQ-19) |

**Validation-Plan**:
- Pre-Edit-Baseline: Executions-IDs notieren
- 11 Test-Profile per `python3 test_suite.py --profile all --save`
- API-Direkt-Read der success-Executions, Set-Vergleich
  `final_routine.produkt_key` pro Profil
- Erwartete Drift dokumentieren: Bianca (V1 → Bond-IQ-Routing), Sina+
  Lena (V2 → Entwirrungsspray, evtl. restore_leave_in-Verlust).
  V5/V6: kein aktuelles Profil betroffen (Coverage-Lücke) — vor Edit
  ggf. Test-Profile ergänzen.

**Test-Profile-Coverage erweitern (Vorschlag)**:
- `Maria-mit-Hitze` (`wellig+fein, MID, mehr_definition`,
  `heat_use=maybe`) — deckt V5 ab
- `mittel-Volumen-Profil` (`glatt+mittel`, `volumen`-Ziel) — deckt V6 ab
- `duenn-Profil` — deckt REQ-06 (V4 Coverage-Lücke) ab
