# Session 2026-07-08 — WL-Klon + Adapter-Ausroll + Fixture-Persistierung

**Bau-Track-Session** (Fortsetzung von `2026-07-07_wl-adapter-isomorphie.md`).
Erster produktiver Aufbau der Whitelabel-Kette: n8n-Workflow-Klon, Adapter
auf 11 Slot-Chips ausgerollt, LibraryEntry-Fixture als Datenmodell-Quelle.
Vier Regressions-Fahrten alle 0/76 Slot-Drift gegen frische MONAT-Baseline.

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-08_wl-klon-adapter.md`, `SAAS_BACKLOG.md`
> (Kapitel 3 Punkt 6 mit Bau-Stand), `wl_adapter.py`,
> `wl_libraries/sina_monat.json` und `demo/bibliothek.html`.
>
> Der WL-Klon `MyBeautyKey Whitelabel Beratungssystem v1.0`
> (ID `5lPLG0y235XiIpN1`, Webhook `mybeautykey-wl-haaranalyse`) ist live und
> beweisbar byte-identisch zur MONAT-Regel-Engine. Sinas Bibliothek liegt
> als markenneutrale LibraryEntry-Fixture in
> `wl_libraries/sina_monat.json` (37 Einträge, 12-Feld-Modell, 11-Slot-UI,
> 27 Nutzen-Chips). Der Fixture-→-Klon-Pipeline ist verlustfrei.
>
> Nächste konkrete Aufgaben — reihenfolge nach Priorität:
>
> 1. **Mockup `demo/bibliothek.html` aktualisieren** — aktuell 11 Chips /
>    7 Slots / 11 Felder, muss auf 27 Nutzen-Chips + 11 Slot-Chips +
>    12. Feld Pflegelevel gebracht werden. Design-Session.
> 2. **Fantasie-Demo-Bibliothek** — SAAS_BACKLOG Kapitel 2.6 Falle 1 +
>    Kapitel 3 Punkt 11. Zweite `wl_libraries/*.json` mit erfundenen
>    Produktnamen für öffentliche Demo/Reels/Werbung. Inhaltlich mit
>    Sina/Desirée abstimmen.
> 3. **Whitelabel-Frontend** — SAAS_BACKLOG Kapitel 3 Punkt 3 ff.
>    Route-Group `src/app/(whitelabel)/`. Mehrtägiger Bau, eigener Fokus.
>
> HANDOVER.md bleibt MONAT-fokussiert. WL-Track lebt weiter im Session-
> Archiv + `SAAS_BACKLOG.md` bis WL für echte Kundinnen live geht.

## Stand am Ende der Session

- **WL-Klon aktiv** in n8n: `5lPLG0y235XiIpN1`, Webhook `mybeautykey-
  wl-haaranalyse`, 17 Nodes byte-identisch zur MONAT-Regel-Engine.
- **MONAT-Workflow physisch unangetastet** (`pwSWA5NatKiLhueB`) — nur GET,
  kein PUT.
- **Adapter auf 11 Slot-Chips ausgerollt** — Sub-Slot-Design-Entscheidung
  aus Iso-Session Priorität 1 damit geschlossen: `kopfhaut_taeglich`,
  `nacht_serum`, `styling_2`, `styling_3` sind jetzt eigenständige UI-Slots.
- **`produktlinie` als LibraryEntry-Feld** — workflow-relevant, nicht mehr
  hardcodiert „eigen".
- **Fixture-Persistierung belegt** — `wl_libraries/sina_monat.json` enthält
  37 LibraryEntry-Dicts, Sync speist daraus fehlerfrei den Klon.
- **Vier Regressions-Fahrten alle 0/76 Slot-Drift** über 13 Test-Profile
  gegen frische MONAT-Baseline (`test_results_20260708_092544.json`):
  1. Rohkopie WL-Klon (2026-07-08 00:44)
  2. Round-Trip 7-Slot mit slot_typ-Passthrough (11:23)
  3. Round-Trip 11-Slot ohne slot_typ-Passthrough (12:28)
  4. Fixture-File → Adapter → Klon (13:01)
- **Verbleibender Passthrough** im Sync-Skript: nur noch `kombinationen`
  und `kombi_optional` (beide workflow-tot per grep-Verifikation).

## Was in dieser Session passiert ist

### Phase 1 — Klon vs. Fork-Nodes geklärt

Der Prompt sprach von „Fork-Nodes mit `_wl`-Suffix" (aus Konzept-Ausbau-Doku).
Die spätere Iso-Session hatte aber schon auf **kompletten Workflow-Klon**
umgeschwenkt. Ich habe den Widerspruch aufgezeigt und Rücksprache gehalten.
Tomi hat den Klon-Weg bestätigt („wenn wir am Ende das Whitelabel fertig
haben, wird der Ursprungsworkflow abgeschaltet und liegen gelassen").

Kern-Vorteil Klon: MONAT-Workflow-Objekt wird beim WL-Bau nie angefasst
→ 0/36-Baseline strukturell abgesichert. Fork-Nodes hätten die Baseline
nur prozedural geschützt (jeder Save-Zyklus geht über beide Zweige).

### Phase 2 — `clone_workflow_wl.py`

Idempotentes Skript nach Muster `patch_webhook_respond.py`:

- GET MONAT-Workflow via n8n-API
- `strip_readonly`-Sanitizing (analog Migrations-Skripte)
- Webhook-Node: neuer Path `mybeautykey-wl-haaranalyse`, neu generierte
  `webhookId` (UUID)
- POST /workflows → Klon entsteht mit eigener ID `5lPLG0y235XiIpN1`
- GET-Verifikation (Name, Path, Node-Count identisch zur Source)
- `--dry-run` für Preview, `--force` für Ersetzen bei bestehendem Klon,
  `--activate` für nachfolgende Aktivierung

Aktivierung: POST `/workflows/{id}/activate` — idempotent, prüft
`active`-Flag vor Call.

### Phase 3 — `test_suite.py` parametrisierbar

Zwei neue CLI-Flags: `--webhook-url` (überschreibt hardcoded MONAT-Webhook),
`--workflow-id` (überschreibt hardcoded MONAT-ID für Execution-Retrieval).
Damit lässt sich derselbe Bulk-Test gegen jeden Workflow fahren.

Ein subtiler Python-Bug: `global`-Deklaration muss VOR jeder Read-Referenz
stehen, nicht erst nach `parser.parse_args()`. Fix an den Anfang von `main()`.

### Phase 4 — Regressions-Fahrt 1: Rohkopie-Klon vs. MONAT

**Kritischer Nebeneffekt geprüft**: würde der Bulk-Run 26 Mails an Desirées
Postfach (`beratung@veradex.de`) feuern, wo gerade Sinas Testerinnen-
Kampagne läuft? Nein — der Workflow enthält einen `Test-Mode-Check`-IF-
Node zwischen Log und Mail-Send: wenn `first_name` mit `-TEST` endet
(alle 13 Test-Profile), werden Mail-Nodes übersprungen. Log-Zeilen im
Sheet sind unkritisch.

Erste MONAT-Baseline war der letzte 3.-Juli-Run — der ist unbrauchbar
(2/13 Profile mit `output`, Rest `None`, das war noch vor Migration-#27-
Loader-Cleanup). Frischer MONAT-Bulk gefahren (`test_results_20260708_
092544.json`), 13/13 grün, alle mit vollem `final_routine`.

Diff `test_results_20260708_013244.json` (WL) vs. `_092544.json` (MONAT):
**0/76 Slot-Drift** über 76 Slot-Entscheidungen bei 13 Profilen.

### Phase 5 — `sync_wl_produktdatenbank.py` (Round-Trip-Modus)

Erster echter Bau-Schritt Richtung WL: die embedded produktdatenbank im
Klon durch **Adapter-Output** ersetzen statt byte-identisch zur MONAT-
Source zu halten. Damit wird bewiesen, dass das Adapter-Vokabular alle
21 workflow-relevanten Spalten trägt.

Skript-Ablauf:
1. GET WL-Klon
2. Embedded JSON-Array zwischen SYNC-Markern in Node „08 Ausschluss-Filter"
   extrahieren (Klammer-balance-Parser, robust gegen Text-in-Strings)
3. Jede Zeile durch `from_produktdatenbank_row` → LibraryEntry → 
   `to_produktdatenbank_row`
4. Passthrough für 4 Design-Verlust-Felder aus dem Original
5. Neuen JSON-Block zwischen SYNC-Markern schreiben
6. PUT + GET-Verifikation

Kurzer grep-Check der Design-Verlust-Felder: `kombinationen` und
`kombi_optional` sind workflow-tot (keine jsCode-Referenz in Nodes 04–15).
`produktlinie` wird in Nodes 08/12/14 aktiv verwendet → muss durchgereicht
werden. `slot_typ` war zu diesem Zeitpunkt noch verschmolzen (7-Slot-UI).

Post-Sync-Bulk-Regressions-Fahrt gegen dieselbe MONAT-Baseline: **0/76
Slot-Drift**. Das Chip-Vokabular des Adapters deckt die 21 workflow-
relevanten Spalten verlustfrei ab.

### Phase 6 — Sub-Slot-Ausroll: Adapter 7 → 11 Slots

Der Passthrough auf `slot_typ` war nur ein Workaround. Iso-Session-
Priorität 1 verlangte eine Entscheidung: Sub-Slots verschmelzen (7-Slot-UI,
einfacher aber verlustbehaftet) oder ausrollen (11-Slot-UI, verlustfrei).

Adapter-Anpassung:
- `SLOT_MAP` von 7 auf 11 Einträge erweitert (`kopfhaut_taeglich`,
  `nacht_serum`, `styling_2`, `styling_3` als neue UI-Slot-Keys)
- `REVERSE_SLOT` von 11→7 Verschmelzung auf 1:1-Mapping umgestellt
- Verschmelzungs-Warnung in `from_produktdatenbank_row` entfernt
- Zwei bestehende `routine_schritt`-Defaults korrigiert: `styling` 6→7,
  `finish` 8→9 (aus Live-produktdatenbank-Verteilung abgeleitet)
- `slot_typ` aus `PASSTHROUGH_FIELDS` im Sync-Skript entfernt

Adapter-Selbsttest bestätigt: Reverse-Test der Entwirrungsspray-Zeile
hat jetzt keine slot_typ-Verschmelzungs-Warnung mehr.

Post-Ausroll-Bulk: **0/76 Slot-Drift**. Ausroll gewinnt — Iso-Session-
Priorität 1 damit geschlossen.

Δ-Report zeigte nur `row_number` als 37-Row-Δ. Per grep verifiziert:
`row_number` ist nirgendwo im Workflow-jsCode referenziert (workflow-tot,
war Sheet-Zeilenindex). Klassifikation im Report angepasst.

### Phase 7 — LibraryEntry-Persistierung + File-Mode-Sync

Bis hierhin selbstreferenziell: embedded → Round-Trip → embedded. Nächster
Schritt: die Bibliothek als **eigenständige Datenquelle** persistieren.

Adapter-Erweiterung: `LibraryEntry.produktlinie: str = ""` als System-
Feld. Forward nutzt `e.produktlinie or produktlinie` (Feld-Wert gewinnt
vor Parameter-Default). Reverse liest es aus der Row. `produktlinie`-
Warnung im Reverse entfernt (wird jetzt sauber transportiert).

**`dump_wl_library.py`**: GET WL-Klon → embedded extrahieren → jede Zeile
durch `from_produktdatenbank_row` → `dataclasses.asdict(entry)` → JSON-
Payload mit Meta-Header (Source, Count, Adapter-Version) und
`entries`-Liste. Ergebnis: `wl_libraries/sina_monat.json` mit 37
Einträgen. Einzige Warnung: `kombinationen/kombi_optional` gehen beim
Reverse verloren (35× — Design-Verlust wie erwartet).

**`sync_wl_produktdatenbank.py` `--source`-Modus**: statt Round-Trip
werden die Einträge aus einer JSON-Fixture rehydriert (`LibraryEntry(
**entry_dict)`) und per Forward-Adapter in 25-Spalten-Zeilen gerendert.
Kein Passthrough für `produktlinie` mehr (kommt aus LibraryEntry-Feld);
`kombinationen`/`kombi_optional` bleiben leer (workflow-tot).

Bulk gegen die Fixture-basierte Klon-Version: **0/76 Slot-Drift**.
Persistenz-Kette Bibliothek → Adapter → Klon ist verlustfrei belegt.

## Neue Artefakte

- `clone_workflow_wl.py` (~210 LOC) — idempotenter n8n-Workflow-Klon
- `sync_wl_produktdatenbank.py` (~250 LOC) — 2-Modi-Sync (Round-Trip,
  File-Fixture) für WL-Klon-Node 08
- `dump_wl_library.py` (~130 LOC) — Klon-embedded → LibraryEntry-Fixture
- `wl_libraries/sina_monat.json` — Sinas 37 MONAT-Produkte als
  markenneutrale Fixture (12-Feld-Modell, 11-Slot, 27 Nutzen)
- `wl_adapter.py` erweitert: SLOT_MAP 7→11, `LibraryEntry.produktlinie`,
  Reverse-Warnungs-Cleanup
- `test_suite.py` erweitert: `--webhook-url`, `--workflow-id`
- 4 MONAT/WL-Test-Result-JSONs unter `test_results_20260708_*.json`
- Backups unter `backups/workflow_wl_sync/` und `backups/workflow_source_
  snapshot_*.json`

## Regressions-Beweise (4× 0/76)

| Fahrt | WL-Zustand | MONAT-Baseline | Ergebnis |
|---|---|---|---|
| 1 | Rohkopie (POST-Klon, keine Änderungen) | test_results_20260708_092544.json | 0/76 |
| 2 | Round-Trip 7-Slot + slot_typ/produktlinie/kombi-Passthrough | idem | 0/76 |
| 3 | Round-Trip 11-Slot + nur produktlinie/kombi-Passthrough | idem | 0/76 |
| 4 | File-Fixture-Sync + nur kombi-Passthrough | idem | 0/76 |

## Bewusst NICHT in dieser Session gemacht

- **Mockup `demo/bibliothek.html`** — Design-Iteration mit Sina/Marcel-
  Zielgruppe im Kopf, verdient eigene Fokus-Session.
- **Fantasie-Demo-Bibliothek** — inhaltliche Fake-Marken-Frage, Sina/
  Desirée-Input nötig.
- **Whitelabel-Frontend Route-Group** — mehrtägiger Bau, SAAS_BACKLOG
  Kapitel 3 Punkt 3 ff.
- **HANDOVER.md-Update** — bleibt MONAT-fokussiert (Konvention aus Iso-
  Session-Doku bestätigt). WL-Track lebt im Session-Archiv +
  `SAAS_BACKLOG.md`.
- **Git-Commits** — alle Skripte + Fixture liegen unversioniert; Tomi
  entscheidet, wann committed wird (evtl. Split in 2–3 sinnvolle
  Commits: Klon-Skript, Adapter-Ausroll, Fixture-Persistierung).
- **Klon deaktivieren nach Test-Ende** — Klon bleibt `active=true` für
  einfache Wiederaufnahme. Falls das den n8n-Executions-Log unnötig
  füllt: manuell im UI deaktivieren.

## Folgepunkte für nächste Session

### Priorität 1: Mockup `demo/bibliothek.html` aktualisieren

Aktueller Mockup-Stand: 11 Nutzen-Chips + 7 Slot-Chips + 11 Felder + kein
Pflegelevel. Ziel: 27 Nutzen-Chips + 11 Slot-Chips + 12 Felder (Pflegelevel
als Chip-Multi LOW/MID/HIGH).

Design-Herausforderung: 27 Nutzen-Chips optisch tragbar machen (evtl. in
Kategorien gruppieren: Pflege-Nutzen / Reinigung / Styling / Special).
Erst wenn Mockup nachgezogen ist, kann man Sina/Marcel wieder etwas
zeigen.

### Priorität 2: Fantasie-Demo-Bibliothek

Zweite `wl_libraries/*.json` mit erfundenen Produktnamen (keine echten
Marken). Zweck: Compliance-sichere Demo-Grundlage für öffentliche
Kommunikation (Reels, Landing, Werbung). SAAS_BACKLOG Kapitel 2.6 Falle 1
verlangt „Bibliothek startet leer, keine markenspezifische Vorbelegung" —
die Fantasie-Bibliothek ist die Ausnahme für Demo-Zwecke.

Inhaltlich mit Sina/Desirée abstimmen: welche Fake-Marken, welche
Positionierung. Sinnvoll: 20–25 Produkte, die alle 11 Slots abdecken,
ohne konkrete Marken-Assoziation.

### Priorität 3: Whitelabel-Frontend

Route-Group `src/app/(whitelabel)/` aufsetzen (SAAS_BACKLOG Kapitel 3
Punkt 3 ff.). Fragebogen aus MONAT-Version kopieren, Vokabular-Referenzen
neutral halten, Ergebnisseite auf Bedarfsprofil + optional konkrete
Bibliothek-Empfehlung umbauen.

Mehrtägiger Bau, ~14–18 Tage laut Backlog-Schätzung. Vor dem Start:
Namensfrage MyBeautyKey final klären (SAAS_BACKLOG Kapitel 4).

### Priorität 4: HANDOVER-Erweiterung

Kommt erst dran, wenn WL für echte Kundinnen live geht. Bis dahin
bleibt der WL-Track im Session-Archiv + `SAAS_BACKLOG.md`. Bei Live-Gang:
Klon-ID, Webhook-Path, Sync-Skript-Konvention, LibraryEntry-Format
ergänzen.

## Konventionen hinzugekommen

- **Klon statt Fork.** Whitelabel-Bau läuft als eigenständiger n8n-
  Workflow-Klon, MONAT bleibt physisch unberührt und wird am Ende
  deaktiviert. Grund: strukturelle Absicherung der 0/36-Baseline
  (bereits in [[project-whitelabel-clone-strategy]]).

- **Test-Mode-Check als Regressions-Enabler.** Die 13 Test-Profile enden
  alle mit `-TEST` im `first_name`. Der IF-Node `Test-Mode-Check` fängt
  das ab und überspringt Mail-Send. Bulk-Tests haben damit nur Log-
  Nebenwirkung, keine Mail-Nebenwirkung. Konvention: Test-Profile
  **immer** mit `-TEST`-Suffix versehen, sonst würden echte Mails an
  `beratung@veradex.de` gehen.

- **11-Slot-UI ausrollen, 7-Slot verwerfen.** Iso-Session-Priorität 1
  final entschieden: die 4 Sub-Slots (`kopfhaut_taeglich`, `nacht_serum`,
  `styling_2`, `styling_3`) sind eigenständige UI-Slot-Chips. Regressions-
  Beweis: 0/76 mit 11-Slot ohne slot_typ-Passthrough.

- **`produktlinie` als LibraryEntry-System-Feld** (kein UI-Chip).
  Workflow-relevant in Nodes 08/12/14, deshalb muss der Adapter es
  transportieren — nicht mehr hardcodiert „eigen". Zukünftige UI-
  Design-Frage: soll die Beraterin das selbst wählen können (Marken-
  Kategorisierung) oder bleibt es ein System-Default? Für Sinas
  MONAT-Fixture ist es aus dem Original übernommen.

- **`kombinationen` / `kombi_optional` als workflow-tot bestätigt.**
  Grep durch alle Node-jsCodes (außer SYNC-Blöcke) zeigt 0 Referenzen.
  Damit kann der Adapter sie ignorieren, Sync-Skript setzt sie leer.
  Falls sie in Zukunft workflow-aktiv werden sollen: erst Nodes anfassen,
  dann Adapter-Feld hinzufügen.

- **Selbstreferenz vs. Fixture-Modus im Sync.** Der Sync unterstützt
  zwei Modi: Round-Trip (embedded → Reverse → Forward → embedded, zum
  Verifizieren der Adapter-Isomorphie) und `--source path/to/library.json`
  (Fixture → Forward → embedded, für echte WL-Bibliotheken). Beide
  müssen 0/76 Regressions-Drift zeigen gegen dieselbe MONAT-Baseline —
  Round-Trip beweist Adapter-Verlustfreiheit, Fixture beweist Persistenz-
  Integrität.

- **row_number ist workflow-tot** — nur Sheet-Zeilenindex, wird von
  keinem Node gelesen. Bei File-Modus-Sync als Sequenz-Nummer gesetzt
  (index+1), Δ zum embedded Original ist harmlos.
