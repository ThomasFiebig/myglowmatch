# HANDOVER — Stand 2026-06-10

Faktische Momentaufnahme des MONAT-Haaranalyse-Systems. Kein Verlauf, keine Diskussion.

## System-Identifikation

| Element | Wert |
|---|---|
| n8n-Instanz | `https://veradex.app.n8n.cloud` |
| Workflow | `MONAT Haarpflege-Beratungssystem v1.0`, aktiv |
| Workflow-ID | `pwSWA5NatKiLhueB` |
| Webhook-URL | `https://veradex.app.n8n.cloud/webhook/glowmatch-haaranalyse` |
| Webhook-Secret (Header `x-glowmatch-secret`) | siehe `.env` / `.env.local` als `N8N_WEBHOOK_SECRET` (rotierbar) |
| Webhook-Response-Mode | `onReceived` (Frontend bekommt sofort `{"message":"Workflow was started"}`) |
| Google-Sheet-Doc-ID | `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A` |
| Sheet-Name | `MONAT_Produktdatenbank_KOMPLETT` |
| Google-Sheets-Credential-ID (n8n) | `zf5b37nhm7NZArlz` |

## Repo & Verzeichnisse

| Pfad | Inhalt |
|---|---|
| `/Users/thomasfiebig/Projekte/myglowmatch/` | Git-Repo (Branch `main`), Next.js-Frontend + Test-Suite |
| `~/Projekte/myglowmatch/chat-archive/` | Session-Dokus |
| `~/Projekte/myglowmatch/produktdatenblaetter/` | 37 Hersteller-PDFs, benannt nach `produkt_key.pdf` + `_produktliste_uebersicht.pdf` + `produkte_index.md` |
| `~/Projekte/myglowmatch/map_*.csv` | Import-Vorlagen der bisherigen Sheet-Migrationen |
| `~/Projekte/myglowmatch/workflow_backup_*.json` | Pre-PUT-Backups |
| `/Users/thomasfiebig/Projekte/myglowmatch/.env` | `N8N_API_KEY`, `N8N_BASE_URL` (gitignored) |
| `/Users/thomasfiebig/Projekte/myglowmatch/test_suite.py` | Test-Runner über Execution-API |
| `/Users/thomasfiebig/Projekte/myglowmatch/inspect_workflow.py` | Read-only Workflow-Inspektor |

## Google-Sheet-Tabs

**Wichtig:** `MONAT_Produktdatenbank_KOMPLETT` ist der **Sheet-Dokumenten-Name** (Doc-ID `1Osmmkrtk4uu5hz6Xk65-HgVgoLMSAYhe1VXOTjLtx0A`), nicht ein Tab-Name. Tabs werden im Code per Loader-Node mit ihrem exakten Namen referenziert.

### Vom aktuellen Workflow genutzte Tabs (8)

| Tab | Spalten / Zweck | Genutzt von |
|---|---|---|
| `produktdatenbank` | 37 Produkte × 24 Spalten (produkt_key, produktname_de, produktlinie, produkttyp, slot_typ, routine_schritt, kopfhaut, haarstruktur, haarstaerke, haarzustand, hauptfunktion, nebenfunktionen, pflegelevel, ausschluss_bei, ist_hitzeschutz, ist_bonding, ist_scalp_focus, locken_geeignet, kombinationen, kombi_optional, aktiv, produkt_url, anwendung, row_number) | Node 07 |
| `map_priorities` | scalp/condition-Priorisierung (Long-Format, Spalten: regel_id, kategorie, wert, reihenfolge, aktiv, beschreibung) | Node 04a |
| `map_pflegelevel_scoring` | Punktevergabe-Regeln pro Profilfeld | Node 06a |
| `map_pflegelevel_overrides` | Floor/Cap-Regeln (PFL-OV-01 bis PFL-OV-04) | Node 06b |
| `map_max_products` | 2D-Lookup `routine_preference × pflegelevel → max_products` | Node 06c |
| `map_slot_rules` | REQ-Regeln (25 aktive Regeln, Trigger + Filter) | Node 10 |
| `map_conflict_rules` | CON-Regeln (CON-01 bis CON-12), match_typ + action | Node 13 |
| `map_pool_filter` | POOL-01 (Bonding) und POOL-03 (Locken-Styling). POOL-02 (Gewicht) bewusste Lücke. | Node 08a |
| `beratungs_log` | Run-Log (1196 Zeilen Stand 2026-06-10) | Node 19 |

### Nicht vom Workflow geladene Tabs (5) — Audit 2026-06-10

Beim Service-Account-Setup am 2026-06-10 sichtbar geworden, am selben Tag auditiert. **Alle 5 sind 0-Hit im Workflow-JSON** (Grep im neuesten Backup, Sanity-Check via Loader-Tabs 4–10 Hits). Inhalts-Status pro Tab:

| Tab | Zeilen | Header | Status | Folge-Aktion |
|---|---|---|---|---|
| `map_input_normalization` | 10 | `feld \| rohwert \| technischer_wert \| hinweis` | **verwaist (Migration entfallen)** — Tally-Pfad ist tot; Frontend liefert technische Werte direkt. Node 03 am 2026-06-10 entfernt statt migriert. | Bei nächster Bereinigung archivieren/löschen |
| `map_derived_variables` | 13 | `variable \| berechnungslogik \| erlaubte_werte \| verwendung` | **halbfertig, Format ungeeignet** — `berechnungslogik`-Spalte ist Freitext-Doku, nicht parsbar; 13 vs. 17 Bool-Flags in Node 05 | Format-Umbau (strukturierte Spalten) nötig bevor Node-05-Migration möglich |
| `map_requirement_rules` | 19 | `regel_id \| bedingung \| action \| slot_typ \| filter \| beschreibung` | **verwaist (Vorgänger)** — gleiche Struktur wie Live-`map_slot_rules` (25 Regeln), aber älter/kürzer | Bei nächster Bereinigung archivieren/löschen |
| `map_priority_resolution` | 15 | `feld \| rang \| wert \| beschreibung` | **verwaist (Vorgänger)** — 4-Spalten-Variante; Live-`map_priorities` hat 6 Spalten | Bei nächster Bereinigung archivieren/löschen |
| `map_system_dictionary` | 25 | `feld \| technischer_wert \| anzeige_text \| kategorie` | **verwaist, latent nützlich** — Reverse-Lookup technisch→deutsch (z.B. `juckend_empfindlich → "juckend / empfindlich"`) | Liegenlassen (K-05). Für Output-Lokalisierung oder Frontend-Anzeige reaktivierbar |

**Dominanter nächster Schritt**: Node 05 (17 Bool-Flag-Heuristiken) — `map_derived_variables` braucht aber erst Format-Umbau (strukturierte Spalten statt Freitext-Doku), bevor Migration möglich. `map_input_normalization`-Migration wurde am 2026-06-10 verworfen: Frontend sendet bereits technische Werte, Node 03 war im Wesentlichen ein No-Op über Tally-Legacy-Maps → komplett entfernt statt migriert.

## Workflow-Nodes (24)

Datenflussreihenfolge (Hauptpfad):

| # | Name | Typ | Funktion |
|---|---|---|---|
| 1 | Webhook | webhook | POST-Endpunkt; Response-Mode `onReceived` (Browser bekommt sofort `{"message":"Workflow was started"}`) |
| 2 | Signature prüfen | if | `x-glowmatch-secret` gegen `N8N_WEBHOOK_SECRET` validieren (Expression `={{ $json.headers['x-glowmatch-secret'] }}`); true → Hauptpfad, false → Pipeline endet still (Eindringling sieht keine Differenz im Webhook-Response) |
| 3 | 02 Felder extrahieren | code | Body in flache Felder, Defaults (`'glatt'`/`'mittel'` u.a.), Array-Dedup; Output `{ normalized, raw_input, partner_id }`. Frontend liefert bereits technische Werte. |
| 4 | 04a Prioritäten laden | googleSheets | `map_priorities` |
| 5 | 04 Prioritäten auflösen | code | scalp_primary/secondary, condition_primary/secondary, generischer Auswerter; liest aus `$node["02 Felder extrahieren"]` |
| 6 | 05 Bool-Flags berechnen | code | 17 Heuristik-Flags (needs_repair_focus, needs_lightweight_logic …), 69 LOC, **noch inline** |
| 7 | 06a Pflegelevel-Scoring laden | googleSheets | `map_pflegelevel_scoring` |
| 8 | 06b Pflegelevel-Overrides laden | googleSheets | `map_pflegelevel_overrides` |
| 9 | 06c Max-Products laden | googleSheets | `map_max_products` |
| 10 | 06 Pflegelevel berechnen | code | Phase 1+3 (Scoring), Phase 2 (Ziele-Bonus, **noch inline**), Phase 4+5+6 sheet-getrieben |
| 11 | 07 Produktdatenbank laden | googleSheets | Hauptpool 37 Produkte |
| 12 | 08a Pool-Filter laden | googleSheets | `map_pool_filter` |
| 13 | 08 Ausschluss-Filter | code | aktiv/produkt_key-Sanity, `ausschluss_bei`, `haarstaerke`, Pool-Regeln aus 08a, `pflegelevel`-Filter |
| 14 | 09 Pool validieren | code | Sanity-Check (Pool nicht leer) |
| 15 | 10 map_slot_rules | googleSheets | REQ-Regeln |
| 16 | 11 REQ-Regeln auswerten | code | Slot-Trigger-Auswertung, generisch; Z. 163-164 `minimal → optional = []` **noch inline** |
| 17 | 13 Konfliktregeln laden | googleSheets | `map_conflict_rules` |
| 18 | 14 Konflikte auflösen | code | match_typ ∈ {produkt_key, produktlinie, key_contains}; `gewicht_eq` entfernt |
| 19 | 12 Scoring & Slot-Befüllung | code | Score-Gewichte 3/2/1 **noch inline**, generischer Filter (Boolean-Flags + Substring) |
| 20 | 15 Routine sortieren | code | Finale Routine, Reihenfolge + Pflichtproduktauswahl |
| 21 | 17 Claude E-Mail formulieren | code | Templating, 517 LOC, CSS inline (mobile + desktop); liest `raw_input` aus `$node["02 Felder extrahieren"]` |
| 22 | 18 E-Mail senden | emailSend | An Kunde (`info@myglowmatch.de` in Tests) |
| 23 | 18b Partner-Mail senden | emailSend | An Partner |
| 24 | 19 Log speichern | googleSheets | Anhang an Log-Tab |

Hinweis: ehemals Node `03 Werte normieren` (160 LOC, 14 Tally-Aliase-Maps) am 2026-06-10 entfernt — Frontend liefert technische Werte direkt, Maps waren idempotent / toter Code. Logik-Reste (Defaults `'glatt'`/`'mittel'`, Array-Dedup, `{ normalized, raw_input, partner_id }`-Output) sind in Node 02 zusammengeführt.

Sticky Notes zählen nicht. Mail-Routing zwischen 18 und 18b geht aus Code-Quelle Node 17 hervor (kein eigener Router-Node).

## Migrationsstand

| Migration | Was | Sheet-Tab | Code-Status |
|---|---|---|---|
| #1 | Prioritäten (scalp/condition) | `map_priorities` | Node 04 generisch |
| #2 | Filter-Spezialfälle | (keine neue Sheet) | Node 12 generisch (Boolean-Regex-Parser); `ir_clinical_serum`-Special-Case entfernt (toter Code) |
| #3 | Pflegelevel Phase 4+5 | `map_pflegelevel_overrides` | Node 06 Phase 4+5 generisch |
| #4 | Pflegelevel Phase 6 | `map_max_products` | Node 06 Phase 6 generisch (2D-Lookup) |
| #5 | Pool-Filter | `map_pool_filter` | Node 08 generisch (Profil- + Produkt-Bedingungen); Inline-Filter Bonding/Gewicht/Locken entfernt; `gewicht_eq`-Case aus Node 14 entfernt |
| #6 | Node 03 entfernen (statt migrieren) | `map_input_normalization` verwaist | Node 03 gelöscht (Tally-Maps = toter Code); Logik-Reste in Node 02 (Defaults, Dedup, `normalized`-Output); Frontend-Edit `mehr_dichte → verdichtend` (questions.ts) fixt 🟡-Goal-Match |

Mini-Syntax in `map_pool_filter` und `map_pflegelevel_overrides`-ähnlichen Tabs:
- Bedingungen mit `;` getrennt, Liste `feld:operator[:wert]`
- Operatoren: `=`, `!=`, `is_true`, `is_false`, `in`, `not_in`
- Listenwerte bei `in`/`not_in` mit `|` getrennt
- Profil-Pfade: `flags.<feld>`, `normalized.<feld>`, `pflegelevel.<feld>`

## Audit-Konventionen (Datenblatt-Provenienz)

Etabliert im A–F-Audit am 2026-06-10. Verbindlich für künftige Sheet-Wert-Entscheidungen.

| # | Konvention | Quelle |
|---|---|---|
| K-01 | `ist_hitzeschutz = TRUE` ⟺ `hauptfunktion` enthält `hitzeschutz`. Sekundäre Hitzeschutz-Eigenschaft bleibt nur in `nebenfunktionen`. Analog ist als Default-Muster für andere Boolean-Eigenschafts-Flags (`ist_bonding`, `ist_scalp_focus` etc.) zu prüfen. | bond_iq_leave_in vs. hitzeschutzspray + smoothing_fohn_spray |
| K-02 | MONAT-Layering-Notation aus PDFs („Schritt-1-Prep" / „Schritt-2-Styling") **≠** unser `routine_schritt`. PDF-„Schritt-1-Prep" = funktional **nach Reinigung+Pflege, auf handtuchtrocknes Haar, vor Styling** → bei uns `slot_typ=leave_in` (`routine_schritt=5`). PDF-„Schritt-2-Styling" → unsere `styling_1` (7) / `styling_2` (8). | rejuvabeads-PDF, smoothing_tiefenbehandlung-PDF |
| K-03 | `haarstaerke` spiegelt die explizite **„Wer profitiert / Ideal für"-Hauptaussage** des PDFs (Bullet-Sektion oder FAQ-Q&A). **Nicht** Header-Schlagwörter, **nicht** Marketing-Description. Bei mehreren Empfehlungs-Aussagen: die mit dem konkretesten Sortiments-Signal gewinnt. | smoothing_tiefenbehandlung (`mittel,dick`) + moxie_mousse (`alle`) |
| K-04 | **PDF strikt**: Was nicht im Datenblatt belegt ist, kommt nicht ins Sheet. „Funktional besser" / „Beratungs-Praxis sagt" / „Kunden brauchen" sind **keine** legitimen Argumente, um nicht-PDF-belegte Sheet-Werte zu verteidigen. Beratungs-Heuristik gehört als **separate** Regel (REQ/CON) ins Sheet, nicht als impliziter Produktstammdaten-Wert. | essig-*.kopfhaut=schuppig nicht PDF-belegt — User-Klarstellung 2026-06-10 |
| K-05 | Sheet-Werte folgen PDF-Belegen **auch wenn aktuell kein Scoring-/Regel-Trigger darauf greift**. Scoring-Stille ist kein Grund für PDF-Verzicht — sie ist eine Folge der Migrations-Reihenfolge und ggf. ein eigener Folge-Punkt. | `staerkend` als nebenfunktion für monat_black akzeptiert, obwohl aktuell kein Profil-Goal darauf matched |
| K-06 | Eine haupt-/nebenfunktion zählt als belegt, wenn das PDF eine konkrete **Funktions-Aussage über die Wirkung am Haar** enthält — an beliebiger Stelle (Vorteils-Bullet, IDEAL-Bullet, FAQ, Test-Bullet ODER Beschreibungssatz). **NICHT** belegt: bloße Header/Taglines (Schlagwort ohne Aussage) und reine Inhaltsstoff-Mechanismus-Beschreibungen (z. B. „Lupinenprotein stabilisiert die Haarbindungen" = wie, nicht was am Haar passiert). Gilt **symmetrisch** für Hinzufügen/Behalten/Entfernen — keine historische Asymmetrie. | Negativbeispiel: `moxie_mousse.verdichtend` (nur Tagline „Volumen und Dichte" + CAPIXYL-Inhaltsstoff). Positiv-Kontrast: `monat_black.verdichtend` ist belegt (IDEAL-Bullet „Die Dichte verbessern und das Haar voller erscheinen lassen möchten"). |
| K-07 | Ein Test-Bullet zählt als Beleg **NUR** wenn die entsprechende Funktion auch im **Produktversprechen verankert** ist (WARUM / IDEAL / Beschreibung / Header — auch implizit). Test-Bullet ohne jede Produktversprechen-Verankerung = Nebenbeobachtung der Studie (35 Frauen, 14 Tage), zählt nicht als Produktfunktion. Gilt symmetrisch für Aufnahme und Entfernung. Grenzfall-Präzedenz: Inhaltsstoff-Mechanik als Verankerung zählt nicht — konsistent mit K-06 bond_iq-Entscheidung. | Negativbeispiel: `ir_clinical_spuelung.glanz` (94%-Test, aber Glanz nirgendwo im Produktversprechen). Konsistenz: K-06 schließt Inhaltsstoff-Mechanik als Verankerung aus (siehe bond_iq-Linie). |
| K-08 | Für **Filter-Spalten** (`kopfhaut`, `haarstaerke`, `haarstruktur`, `haarzustand`) zählt die strukturelle **Zielgruppen-Spezifikation im Header-Untertitel** des MONAT-PDFs (Format „Zustand / Haartyp / Haartextur / Step") als legitimer Beleg, **auch ohne** zusätzliche Verankerung in WARUM/IDEAL/Beschreibung. Begründung: Hersteller-Untertitel ist eine direkte „Für wen ist das"-Aussage, methodisch näher an K-03's „Wer profitiert"-Hauptaussage als an einer Werbe-Tagline. Abgrenzung zu K-06: Für **Funktions-Spalten** (`hauptfunktion`, `nebenfunktionen`) zählt der Header **weiter nicht** als Beleg (Werbe-Tagline ≠ Funktions-Aussage am Haar). K-03 bleibt der Konflikt-Löser: bei Widerspruch zwischen Header-Untertitel und IDEAL-Bullet gewinnt IDEAL. Gilt symmetrisch für Aufnahme/Behalten/Entfernen. | `monat_black.kopfhaut=fettig` + `.haarstaerke=fein,mittel` ausschließlich durch Header-Untertitel belegt (keine WARUM-/IDEAL-Verankerung). Abgrenzungskontrast: `essig_spuelung.kopfhaut=fettig` ist **nicht** durch K-08 belegbar — Header-Untertitel sagt nur „Kopfhautpflege", kein „Fettiges Haar". |

**bond_iq-Linie als Lehrbeispiel für K-06**: Die Bond-IQ-Produktlinie ist bewusst **nicht durchgängig bonding-klassifiziert** in `hauptfunktion`. `bond_iq_leave_in` behält `bonding` (eigener Funktions-Bullet „Stärkt die Haarstruktur und repariert Haarbindungen*"). `bond_iq_night_day_serum`, `bond_iq_shampoo`, `bond_iq_spuelung` haben `bonding` per K-06-Gegencheck verloren — bei ihnen ist Bindungs-Reparatur **nur** in der Inhaltsstoff-Beschreibung (Lupinenprotein „stabilisiert die inneren Haarbindungen") belegt, kein eigener Funktions-Bullet am Haar. Das ist PDF-Realität, kein Daten-Fehler. **Nicht "korrigieren"** in späteren Sessions.

**POOL-01-Architektur (K-06-Konsequenz)**: Das Bool-Flag `ist_bonding` hatte zwei Rollen vermischt — (a) Stammdatum „Produkt wirkt bonding am Haar" und (b) Routing-Proxy „Produkt gehört zur Reparatur-Linie". K-06 trennt sie: `ist_bonding` ist jetzt reines Wirkungs-Flag (analog `ist_hitzeschutz` per K-01). Das Routing der Bond-IQ-Linie liegt in POOL-01 jetzt explizit auf `produktlinie:=:bond_iq` statt auf `ist_bonding:is_true`. **`ist_bonding` darf in anderen Regeln nicht als Linien-Proxy verwendet werden** — wer das findet, behandelt es als Bug (Folge-Punkt: Sheet auf weitere Linien-Proxy-Misuses prüfen).

**Wichtige Beobachtung aus dem Vollrun (2026-06-10):** Sheet-Werte ohne PDF-Beleg sind nicht nur Doku-Schuld, sie produzieren aktiv falsche Empfehlungen. Beispiel: `monat_black.nebenfunktionen=volumen` (PDF-untreu, PDF spricht von „Dichte" und „Verdichtend") führte dazu, dass Maria + Julia (`scalp=normal`, `goal=volumen`) das falsche Shampoo bekamen — monat_black ist laut PDF für **fettige Kopfhaut**. Nach Fix gewinnt revive_shampoo (`hauptfunktion=volumen`), das funktionsspezifisch richtige Shampoo. K-04 hat damit direkten Output-Effekt auf die Kundenempfehlung.

## Audit-Workflow (Test-Disziplin)

Konventionen für **wie** auditiert wird, ergänzend zu den K-Datenkonventionen (K-01..K-08).

| # | Regel | Begründung |
|---|---|---|
| T-01 | **Isolations-Regel**: Edits, die potenziell dieselbe Slot-Entscheidung berühren, werden einzeln getestet (ein Edit → ein Full-Run → Drift-Analyse), nicht gekoppelt. Im Zweifel — wenn Slot-Disjunktheit nicht verifiziert ist — gilt isoliert als Default. Maskierung ist möglich, wenn zwei Edits dieselbe Slot-Entscheidung beeinflussen (Pool-Veränderung **oder** Score-Verschiebung im selben Slot). **Zwei Test-Modi unterscheiden**: (a) **strikt-isoliert** = nur der zu testende Edit ist aktiv im Sheet während des Runs; (b) **diff-isoliert** = mehrere Edits sind aktiv, der einzelne Effekt wird per Diff zum vorherigen Run extrahiert. Beide Modi sind nur bei verifizierter Slot-Disjunktheit äquivalent; bei unklarer Disjunktheit ist strikt-isoliert der Default. Mehraufwand pro Edit ~1 Run, Erkenntnis-Verlust 0. | Block-2-Stufe-1, 2026-06-13: Edit A strikt-isoliert (nur A im Sheet), Edit C diff-isoliert (A+C im Sheet, C-Effekt per Diff zum A-Run). Disjunkte Slots verifiziert → diff-isoliert war zulässig. |
| T-02 | **Mechanismus-Belegpflicht**: Aussagen in HANDOVER über das, was der Workflow tut/nicht tut (welcher Node was konsumiert, wie ein Filter/Score wirkt, welche Spalte aktiv ist) müssen **entweder** mit konkretem Code-Zitat belegt sein (Node-Name + Zeilen-Referenz aus Workflow-Backup oder file:line aus dem Repo) **oder** explizit als Hypothese markiert werden („vermutlich", „zu verifizieren"). Beobachtungs-Befunde (Run-Output, Sheet-Stand, JSON-Inspektion) sind ohne Code-Verifikation gültig, dürfen aber **nicht** zu Architektur-Schlüssen extrapoliert werden. Vor jeder Mechanismus-Aussage Stop-Frage: „Habe ich den Code dazu gelesen?" Wenn nein → kurz lesen oder als Hypothese formulieren. | Block-2-Stufe-1, 2026-06-13: erste Behauptung „kopfhaut-Spalte filtert nicht" basierte auf Beobachtungs-Extrapolation (Maria's Pool unverändert), nicht auf Code-Inspektion. Korrektur erst nach Tomi-Rückfrage: Node 12 Z. 26 zeigt Score-Bonus +2 statt Filter — die plausible „Doku-Spalte"-Erklärung wurde mit Wahrheit verwechselt. Schadensklasse: Mechanismus-Doku falsch, Routing 0/7 trotzdem korrekt — aber Audit-Vertrauen leidet. |

## Datenblatt-Provenienz-Audit (Stand 2026-06-13)

Spalten-Reihenfolge nach Scoring-Relevanz: Block 1 (scoring-kritisch: `hauptfunktion`, `nebenfunktionen`) → Block 2 (Filter: `haarstaerke`, `haarstruktur`, `haarzustand`, `kopfhaut`) → Block 3 (Bool-Flags + Level) → Block 4 (Doku). Produkt-Reihenfolge je Block in 4 Stufen nach Bug-Risiko (Multi-Funktion → seltene Tokens → A–F-Re-Verify → Singulär-Sanity).

**Block 1 Stufe 1** — 8 Produkte (Multi-Funktions-`hauptfunktion`: 4× bond_iq + 3× curl + moxie_mousse) — abgeschlossen 2026-06-11. 7 Zellen-Edits in `produktdatenbank.nebenfunktionen` (16 Token-Ergänzungen), alle K-04/K-05 strikt (eigener Vorteils-Bullet oder eigene FAQ-Aussage Pflicht; Tagline, reine Inhaltsstoff-Mechanismus-Beschreibung oder Nebensatz-Erwähnung zählen nicht):

| Produkt | nebenfunktionen ergänzt um | belegende Bullet-Kategorie |
|---|---|---|
| bond_iq_leave_in | `frizz_reduktion`, `kaemmbarkeit`, `glanz` | je eigener Vorteils-Bullet + Test 91 % für kaemmbarkeit |
| bond_iq_night_day_serum | `frizz_reduktion`, `kaemmbarkeit`, `elastizitaet` | Test 91 % für frizz_reduktion; eigener Bullet für elastizitaet |
| bond_iq_shampoo | `glanz`, `kaemmbarkeit` | je eigener Vorteils-Bullet |
| bond_iq_spuelung | `frizz_reduktion`, `glanz`, `elastizitaet` | Test 89 % für frizz_reduktion; eigener Bullet für glanz + elastizitaet |
| curl_creme | `kaemmbarkeit` | eigener Bullet + Test 91 % |
| curl_gelee | `frizz_reduktion`, `glanz` | Test 91 % für frizz_reduktion; eigener Bullet für glanz |
| curl_auffrischer | `frizz_reduktion`, `definition` | Test 91 % bzw. 94 % |

**Bewusst NICHT ergänzt** (Stand Stufe-1-Sammel-Entscheidung 2026-06-11; teilweise später per **K-06-Gegencheck** revidiert, siehe Block unten):
- `bonding` bei bond_iq_night_day_serum / bond_iq_shampoo / bond_iq_spuelung — nur via Inhaltsstoff-Beschreibung belegt, kein eigener Vorteils-Bullet. → **K-06-Gegencheck**: zusätzlich **entfernt** aus `hauptfunktion` der 3 Produkte.
- `moxie_mousse.verdichtend` — nur Header-Tagline + CAPIXYL-Inhaltsstoff → **K-06**: bleibt draußen (Negativbeispiel zu K-06).
- `moxie_mousse.definition` — vorher als „nur FAQ" abgelehnt → **K-06-Gegencheck**: nachträglich aufgenommen (FAQ-Q2 „sorgt bei Locken oder Wellen für definierte Form und Frizz-Kontrolle" ist konkrete Funktions-Aussage am Haar).

`hauptfunktion` aller 8 Produkte unverändert (Stufe 1); 3 bonding-Entfernungen erst im K-06-Gegencheck — siehe Block unten.

**Neu im Sheet-Vokabular**: `elastizitaet` (vorher nur bei `super_feuchtigkeitsmaske`, jetzt zusätzlich `bond_iq_night_day_serum`, `bond_iq_spuelung`). 0 Treffer in `map_slot_rules` / `map_conflict_rules` / `map_priorities` → kein Filter/REQ-Hard-Fail. Node 12 ohne care_goal-Match → +0 Score, kein Scoring-Effekt.

**Reihenfolge irrelevant**: Node 12 nutzt `csvToArr` + `.some()` → Set-Verhalten. Reihenfolge der Token in `nebenfunktionen` ohne funktionalen Effekt.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_010951_pre_block1_stufe1/produktdatenbank.csv` (38 Zeilen, Pre-Edit-Snapshot).

**Regression**: Full-Run 2026-06-11 — 7/7 Profile produkt_key-identisch zur 10.06.-Baseline. Erwartete Score-Drift nur für Lena (`mehr_glanz`-Goal, substring-Match auf neu-ergänztes `glanz` bei bond_iq + curl_gelee) — kein Slot-Shift, da Lenas Pool die jeweiligen Slots bereits via REQ-Routing (Renew, Hitzeschutzspray) bzw. ohne Konkurrenz (curl_gelee in styling_2) dominiert.

**Block 1 Stufe 2** — 8 Produkte (seltene/auffällige Tokens: monat_black, rejuvabeads, ir_clinical_kopfhautserum, the_champ, replenish_maske, super_feuchtigkeitsmaske, restore_leave_in, kopfhaut_peeling) — abgeschlossen 2026-06-11. 5 Zellen-Edits in `nebenfunktionen`, 7 Token-Ergänzungen, nach dem damals geltenden „eigener Vorteils-Bullet"-Kriterium (Stufe-1-Regel):

| Produkt | nebenfunktionen ergänzt um | belegender Bullet/Aussage |
|---|---|---|
| rejuvabeads | `kaemmbarkeit`, `staerkend`, `frizz_reduktion` | je eigener WARUM-/IDEAL-Bullet |
| ir_clinical_kopfhautserum | `staerkend` | Test-Bullet 82 % „zur Stärkung der Haare beiträgt" |
| replenish_maske | `kaemmbarkeit` | IDEAL „Verbesserte Haarstruktur und Kämmbarkeit wünschen" |
| super_feuchtigkeitsmaske | `kaemmbarkeit` | WARUM „Fördert die Elastizität und verbessert die Kämmbarkeit" |
| kopfhaut_peeling | `frische` | IDEAL „gereinigt und erfrischt hinterlassen möchten" |

Grenzfälle behalten (per Sammel-Entscheidung): `rejuvabeads.glanz` (Beschreibung „glatt, glänzend") + `replenish_maske.kraeftigend` (Beschreibung „stellt Glanz, Kraft und Vitalität wieder her"). Beide haben *keinen* eigenen Vorteils-Bullet, sind aber wörtliche PDF-Aussage über die Wirkung am Haar. Unter K-06 jetzt eindeutig belegt.

`hauptfunktion` aller 8 Produkte unverändert.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_015455_pre_block1_stufe2/produktdatenbank.csv`.

**Regression**: Full-Run 2026-06-11 — 7/7 produkt_key-identisch zur Pre-Stufe-2-Baseline.

### K-06-Gegencheck (2026-06-11)

Anlass: Nach Stufe 2 wurde die „Bullet-Pflicht" aus Stufe 1 zu K-06 in finaler Form ausgeweitet (Funktions-Aussage am Haar — egal an welcher Stelle — vs. Tagline/Inhaltsstoff-Mechanik). K-06 wirkt **symmetrisch** auf Hinzufügen/Behalten/Entfernen. Folge: rückwirkender Gegencheck über alle 16 Produkte aus Stufe 1+2.

**Aufnahmen** (13 Token über 7 Produkte, vorher übersehen oder per damals strenger Bullet-Pflicht ausgeschlossen):

| Produkt | Token | Beleg-Quelle |
|---|---|---|
| bond_iq_leave_in | +`staerkend` | Test 91 % „die Haarsträhnen stärkt" |
| bond_iq_night_day_serum | +`staerkend`, +`kraeftigend` | Bullets „Repariert und stärkt das Haar", „Baut Haarstruktur auf … für mehr Kraft" |
| bond_iq_shampoo | +`staerkend` | Test 89 % „das Haar fühlt sich kräftiger an" |
| bond_iq_spuelung | +`staerkend` | Test 89 % „stärkt die Haarfasern, reduziert Haarbruch" |
| curl_creme | +`elastizitaet` | Test 88 % „Locken Elastizität und Definition verleiht" |
| curl_gelee | +`elastizitaet`, +`staerkend`, +`reparatur` | Bullets „Elastizität wiederherzustellen", „Pflegt, stärkt und repariert welliges, lockiges und krauses Haar" |
| curl_auffrischer | +`elastizitaet`, +`staerkend` | Bullets „Verbessert die Haarelastizität", „Macht Locken stärker, weicher und glänzender" |
| moxie_mousse | +`definition` | FAQ-Q2 „sorgt bei Locken oder Wellen für definierte Form und Frizz-Kontrolle" |
| kopfhaut_peeling | +`feuchtigkeit` | Beschreibung „Angereichert mit REJUVENIQE® spendet es Feuchtigkeit und hinterlässt das Haar gereinigt und erfrischt" |

**Entfernungen aus `hauptfunktion`** (3 Token):
- bond_iq_night_day_serum: `reparatur,bonding` → `reparatur`
- bond_iq_shampoo: `reparatur,bonding` → `reparatur`
- bond_iq_spuelung: `reparatur,bonding` → `reparatur`

Begründung: bei diesen 3 Produkten ist Bonding **nur** über die Inhaltsstoff-Beschreibung Lupinenprotein belegt — Inhaltsstoff-Mechanik, kein Funktions-Bullet am Haar. K-06 verlangt symmetrische Konsequenz: Token raus. `bond_iq_leave_in.bonding` bleibt (eigener Bullet „repariert Haarbindungen*").

**K-01-Konsistenzkorrektur (3 Bool-Flags vorgezogen aus Block 3)**: `ist_bonding` bei bond_iq_night_day_serum, bond_iq_shampoo, bond_iq_spuelung von `TRUE` auf `FALSE` gesetzt. K-01 fordert `ist_bonding=TRUE ⟺ hauptfunktion enthält bonding` — nachdem `bonding` aus `hauptfunktion` raus ist, muss das Flag folgen. **Rest von Block 3 (übrige Bool-Flags, Pflegelevel-Audit) noch offen** — wurde nicht mit-erledigt, nur diese 3 K-01-Konsistenzfälle.

**POOL-01-Umstellung** (in `map_pool_filter`): `produkt_bedingungen` von `ist_bonding:is_true` auf `produktlinie:=:bond_iq`, `beschreibung` von „Bonding-Produkte nur bei Reparatur-Fokus zulassen" auf „Bond-IQ-Linie nur bei Reparatur-Fokus zulassen". Architektur-Hintergrund: siehe K-06-Block oben („POOL-01-Architektur"). Effekt: Routing-Verhalten bleibt funktional identisch zur Pre-K-06-Baseline, aber das Routing-Kriterium ist jetzt sauber an `produktlinie` gekoppelt statt am vermischten Stammdatum `ist_bonding`.

**Backups**:
- `~/Projekte/myglowmatch/backups/sheets_20260611_092835_pre_k06_gegencheck/produktdatenbank.csv`
- `~/Projekte/myglowmatch/backups/sheets_20260611_110432_pre_pool01_relink/map_pool_filter.csv`

**Regression**: Full-Run nach POOL-01-Umstellung — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline** (Stand nach Stufe 2). Sarah (needs_repair_focus=TRUE) bekommt weiter alle 4 Bond-IQ-Produkte; Lena/Bianca/Vivien wieder auf Renew/Feuchtigkeits-Linie wie vorher.

**Block 1 Stufe 3** — 8 Produkte (A–F-Re-Verify-Cluster + Smoothing-/Föhn-Doppelung: hitzeschutzspray, smoothing_fohn_spray, essig_shampoo, essig_spuelung, fohncreme, smoothing_shampoo, smoothing_deep_conditioner, smoothing_tiefenbehandlung) — abgeschlossen 2026-06-11. 7 Zellen-Edits in `nebenfunktionen` (16 Token-Ergänzungen über 7 Produkte + 1 K-06-konforme Entfernung; fohncreme unverändert):

| Produkt | nebenfunktionen ergänzt um (Entfernung in **fett**) | Belege |
|---|---|---|
| hitzeschutzspray | `staerkend`, `elastizitaet` | IDEAL „Stärke und Elastizität des Haares verbessern" + Test „mehr Stärke und Elastizität" + Beschreibung „stärkt und schützt das Haar" |
| smoothing_fohn_spray | `kaemmbarkeit`, `staerkend`, `elastizitaet`, `farbschutz` | Test 4x/3x Kämmbarkeit; WARUM „Stärkt das Haar"; Test „Gestärktes Haar, verbesserte Elastizität"; Test „Farbbrillanz bis zu 20 Haarwäschen erhalten" |
| essig_shampoo | `kopfhautpflege`, `frische` | WARUM „Reduziert überschüssiges Fett und stellt das Gleichgewicht der Kopfhaut wieder her"; IDEAL „Frisches, sauberes … Haar möchten" |
| essig_spuelung | `entgiftung`, `farbschutz`, `kopfhautpflege` | WARUM „Entfernt Produktrückstände" + Test 80 % „Feuchtigkeitsgehalts der Kopfhaut"; WARUM „bewahrt die Farbe für bis zu 20 Haarwäschen" + Test 83 % |
| smoothing_shampoo | `glanz`, `reparatur` | Test „24 % mehr Glanz"; WARUM „weniger Haarbruch" + Test „68 %" |
| smoothing_deep_conditioner | `glanz`, `reparatur` | Test „56 % mehr Glanz"; WIE „7x weniger Haarbruch" + Test „87 %" |
| smoothing_tiefenbehandlung | `kaemmbarkeit`, `glanz`, `reparatur`; **−`feuchtigkeit`** | Test 6x/5x Kämmbarkeit; Test „80 % mehr Glanz"; WIE „Reduziert Haarbruch um 91 %" |
| fohncreme | (keine) | hauptfunktion + Sheet-`glanz` PDF-belegt; keine weiteren Funktions-Aussagen am Haar |

**Erste K-06-konforme nebenfunktion-Entfernung**: `smoothing_tiefenbehandlung.feuchtigkeit` raus. Das Wort „Feuchtigkeit" kommt im PDF nicht vor; Wirkung nur indirekt über „Pflanzliche Buttern verwöhnen das Haar, machen es geschmeidig und weich" + Conditioner-Charakter ausgedrückt. Conditioner-Produkttyp-Rückschluss ist unter K-06 keine Funktions-Aussage am Haar. Symmetrie-Beleg für K-06: die Regel greift nicht nur bei `hauptfunktion`-Tokens (wie bei den 3 bond_iq-bondings), sondern auch bei nebenfunktion-Tokens. Auswirkung auf Routing: null (smoothing_tiefenbehandlung ist via CON-11 ohnehin aus allen 7 Profilpools).

`hauptfunktion` aller 8 Produkte unverändert.

**K-01-Konsistenz-Check** (zweite Block-3-Spot-Prüfung): `ist_hitzeschutz`-Flag bei allen 8 Produkten konsistent mit `hauptfunktion` — `hitzeschutzspray` (`hauptfunktion=hitzeschutz` → TRUE), `smoothing_fohn_spray` + `fohncreme` (enthält `hitzeschutz` → TRUE), übrige 5 (enthält nicht → FALSE). 8/8 konsistent, **keine weiteren Block-3-Vorziehungen** nötig.

**Vokabular-Beobachtung**: alle 9 verschiedenen ergänzten Tokens (`staerkend`, `elastizitaet`, `kaemmbarkeit`, `farbschutz`, `kopfhautpflege`, `frische`, `entgiftung`, `glanz`, `reparatur`) bereits im Vokabular etabliert — keine Neueinführungen. `farbschutz` war bisher nur bei `ir_clinical_shampoo` + `ir_clinical_spuelung` etabliert; Stufe 3 ist die erste Verwendung bei Styling- und Reinigungs-Produkten (`smoothing_fohn_spray`, `essig_spuelung`). Falls künftig eine Scoring-Regel `goal=farbschutz` auswertet, sind diese zwei Produkte jetzt korrekt im Pool — nur als Beobachtung, kein offener Punkt.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_210600_pre_block1_stufe3/produktdatenbank.csv`.

**Regression**: Full-Run nach den 7 Zell-Updates — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline** (Stand nach K-06-Gegencheck + POOL-01-Relink). Erwartung bestätigt: keiner der ergänzten Tokens matched ein direktes Profil-Goal, das einen Slot-Shift auslösen würde; die `feuchtigkeit`-Entfernung bei smoothing_tiefenbehandlung wirkt sich nicht aus, da CON-11 das Produkt in allen 7 Pools blockiert.

**Block 1 Stufe 4** — 13 Produkte (Singulär-Sanity: feuchtigkeits_shampoo, renew_shampoo, renew_spuelung, erweiterte_feuchtigkeit_spuelung, revive_shampoo, revitalize_spuelung, volumen_spray, rejuveniqe_oel, entwirrungsspray, scalp_comfort_behandlung, scalp_comfort_serum, ir_clinical_shampoo, ir_clinical_spuelung) — abgeschlossen 2026-06-12. **Block 1 damit vollständig**. 19 Zell-Updates in `nebenfunktionen` (26 Token-Aufnahmen über 12 Produkte + 10 Token-Entfernungen über 8 Produkte; fohncreme + scalp_comfort_serum unverändert):

| Produkt | Aufnahmen | Entfernungen | Quelle |
|---|---|---|---|
| feuchtigkeits_shampoo | `reinigung` | — | Stufe 4 |
| renew_shampoo | `reinigung`, `kaemmbarkeit` | — | Stufe 4 |
| renew_spuelung | `kaemmbarkeit` | **−`glanz`** (K-06: Glanz im PDF nicht erwähnt) | Stufe 4 |
| erweiterte_feuchtigkeit_spuelung | `kaemmbarkeit` | — | Stufe 4 |
| revive_shampoo | `staerkend`, `feuchtigkeit`, `kaemmbarkeit`, `reparatur` | — | Stufe 4 |
| revitalize_spuelung | `staerkend`, `kaemmbarkeit`, `reparatur` | — | Stufe 4 |
| volumen_spray | `verdichtend`, `staerkend` | — | Stufe 4 |
| rejuveniqe_oel | `kraeftigend`, `kaemmbarkeit` | — | Stufe 4 |
| entwirrungsspray | `glanz`, `staerkend`, `kaemmbarkeit` | — | Stufe 4 |
| scalp_comfort_behandlung | `reinigung`, `entgiftung`, `frische` | — | Stufe 4 |
| ir_clinical_shampoo | `haarwuchs`, `staerkend`, `frische` | — | Stufe 4 (4 weitere per K-07 gestrichen) |
| ir_clinical_spuelung | `haarwuchs`, `staerkend`, `kaemmbarkeit`, `frische` | — | Stufe 4 (glanz per K-07 gestrichen) |

**Erste K-06-konforme nebenfunktion-Entfernung außerhalb Stufe 3**: `renew_spuelung.glanz` — das Wort „Glanz" / „glänzend" kommt im renew_spuelung-PDF nirgendwo vor (kein WARUM, IDEAL, VORTEILE, Test oder Beschreibung). Cross-References in „FUNKTIONIERT GUT MIT" beziehen sich auf Replenish-Maske als Begleiter, nicht auf renew_spuelung selbst. Analog zu smoothing_tiefenbehandlung.feuchtigkeit-Entfernung aus Stufe 3.

**Vokabular-Beobachtung**:
- `frische` jetzt 5 Produkte: essig_shampoo, scalp_comfort_behandlung, ir_clinical_shampoo, ir_clinical_spuelung, the_champ (vorher nur the_champ; Stufe 3 ergänzte essig + kopfhaut_peeling; Stufe 4 ergänzte 3 weitere).
- `haarwuchs` jetzt **komplett bei IR-Clinical-Linie**: ir_clinical_kopfhautserum (Stufe 2) + ir_clinical_shampoo + ir_clinical_spuelung (Stufe 4). Konsistente Linien-Klassifikation.
- `verdichtend` neu als nebenfunktion bei volumen_spray — vorher nur als hauptfunktion bei IR-Clinical-Linie + monat_black. Erste Verwendung als sekundäre Funktion.
- `kraeftigend` neu bei rejuveniqe_oel — vorher nur replenish_maske + bond_iq_night_day_serum.
- Keine Neueinführungen ins Vokabular.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260611_234938_pre_stufe4_k07/produktdatenbank.csv`.

**Regression**: Full-Run nach den 19 Zell-Updates — **7/7 Profile produkt_key-identisch zur HANDOVER-Baseline**. Lena (`mehr_glanz`-Goal) trotz `renew_spuelung.glanz`-Entfernung unverändert: Score-Differenz reicht nicht für Slot-Wechsel; konkurrierende Spülungen (`erweiterte_feuchtigkeit_spuelung`, `revitalize_spuelung`) sind durch andere Kriterien dominiert.

### K-07-Gegencheck (2026-06-12)

Anlass: User-Befund zu `ir_clinical_spuelung.glanz` (Stufe-4-Vorschlag) — Glanz nur in 94%-Test, nirgendwo im Produktversprechen. K-07 als Präzisierung eingeführt (siehe Konventionen-Tabelle), rückwirkender Gegencheck über alle eingespielten Token aus Stufen 1+2+3+K-06.

**Rückwirkende Entfernungen aus eingespieltem Material** (10 Token-Entfernungen über 7 Produkte; davon 1 K-06-konform aus Stufe 4 oben + 9 K-07-konform):

| Produkt | Token | Quelle | Test-Wortlaut | Grund |
|---|---|---|---|---|
| bond_iq_spuelung | `frizz_reduktion` | Stufe 1 | „89 % … glättet die Schuppenschicht, reduziert Frizz und verbessert die Frisierbarkeit*" | Frizz nirgendwo in WARUM-Aussage-Bullets, IDEAL, Beschreibung |
| curl_creme | `elastizitaet` | K-06 | „88 % … Locken Elastizität und Definition verleiht" | Elastizität nirgendwo in WARUM, IDEAL, Beschreibung |
| smoothing_fohn_spray | `kaemmbarkeit` | Stufe 3 | „4x/3x bessere Kämmbarkeit" | Kämmbarkeit nirgendwo im Produktversprechen |
| smoothing_fohn_spray | `elastizitaet` | Stufe 3 | „Gestärktes Haar, verbesserte Elastizität …" | Elastizität nirgendwo im Produktversprechen |
| smoothing_fohn_spray | `farbschutz` | Stufe 3 | „Farbbrillanz bis zu 20 Haarwäschen erhalten" | Farbe nirgendwo im Produktversprechen |
| smoothing_shampoo | `glanz` | Stufe 3 | „24 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| smoothing_deep_conditioner | `glanz` | Stufe 3 | „56 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| smoothing_tiefenbehandlung | `glanz` | Stufe 3 | „80 % mehr Glanz" | Glanz nirgendwo im Produktversprechen |
| ir_clinical_kopfhautserum | `staerkend` | Stufe 2 | „82 % … zur Stärkung der Haare beiträgt" | Verankerung nur via CAPIXYL-Inhaltsstoff-Mechanik (K-06-Grenzfall-Präzedenz: Mechanik zählt nicht) |

**Streichungen aus Stufe-4-Vorschlag** (9 Token, gar nicht erst geschrieben):
- feuchtigkeits_shampoo: `farbschutz` (Test, keine Produktversprechen-Verankerung)
- erweiterte_feuchtigkeit_spuelung: `farbschutz` (analog)
- ir_clinical_shampoo: `kopfhautpflege`, `glanz`, `kaemmbarkeit`, `feuchtigkeit` (4 Tokens; nur in Tests, nicht im Produktversprechen) — **K-01-Cascade entfällt**: `ist_scalp_focus` bleibt FALSE (kopfhautpflege nicht aufgenommen)
- ir_clinical_spuelung: `glanz` (K-07-Negativbeispiel)
- scalp_comfort_serum: `frische` (Test sagt „erfrischt", Produktversprechen sagt nur „kühlend" — semantisch verwandt aber kein wörtlicher Beleg)

**Vokabular nach K-07-Cleanup**: `farbschutz` jetzt nur noch IR-Clinical-Linie (`ir_clinical_shampoo`, `ir_clinical_spuelung` — `smoothing_fohn_spray` rausgeflogen). `elastizitaet` nur noch bei super_feuchtigkeitsmaske + bond_iq_night_day_serum + bond_iq_spuelung + curl_gelee + curl_auffrischer (curl_creme + hitzeschutzspray + smoothing_fohn_spray rausgeflogen).

**Regression**: 7/7 produkt_key-identisch zur HANDOVER-Baseline. Vorhersage bestätigt — keiner der entfernten Tokens matched ein direktes Profil-Goal, das einen Slot-Shift auslösen würde; betroffene Smoothing-Produkte sind via CON-11 ohnehin aus den Pools blockiert.

### Block 1 — Gesamt-Bilanz nach Abschluss

Stufen 1+2+K-06+3+4+K-07 zusammen:
- **32 Produkte angefasst** (5 unverändert: ir_clinical_shampoo war kein Stufe-1-Cluster, fohncreme + scalp_comfort_serum keine Edits, 2 weitere ohne fehlt-im-Sheet)
- **Netto-Aufnahmen**: ~73 Token-Ergänzungen über alle Stufen
- **Entfernungen**: 14 Token (3 bonding aus hauptfunktion via K-06, 11 nebenfunktion via K-06/K-07)
- **3 Konventionen geschärft**: K-06 (Wirkung am Haar vs. Schlagwort/Mechanik), K-07 (Test-Verankerung im Produktversprechen), K-01-Bond-IQ-Cascade (3 ist_bonding-Flags + POOL-01-Umstellung)
- **0 Routing-Drift über alle Stufen**: HANDOVER-Sollwerte unverändert

**Offen**: Block 2 Stufe 1 in Arbeit (`kopfhaut`-Spalte, siehe unten); Block 2 Stufen 2-3 (`haarstruktur`/`haarstaerke`/`haarzustand`) + Block 3 Rest (Bool-Flags ohne die 3 bei K-06-Gegencheck vorgezogenen + `pflegelevel` + `ausschluss_bei`) + Block 4 (Doku-Spalten: `anwendung`, `produkt_url`, `locken_geeignet`).

**Block 2 Stufe 1** — `kopfhaut`-Spalte, 6 Produkte mit non-Default-Wert + Cross-Check der 31 Default-Produkte — in Arbeit 2026-06-13.

Audit-Befund pro Produkt (6 non-Default + ir_clinical_kopfhautserum als Cross-Check-Treffer):

| Produkt | Sheet-Wert | PDF-Beleg | Entscheidung |
|---|---|---|---|
| essig_shampoo | `fettig` | Header-Untertitel „Fettiges Haar und Kopfhaut" (K-08 ✓) + WARUM „Reduziert überschüssiges Fett und stellt das Gleichgewicht der Kopfhaut wieder her" (K-06 ✓) | Status Quo |
| **essig_spuelung** | `fettig` → **`-`** | Header-Untertitel sagt nur „Kopfhautpflege" (K-08 nicht einschlägig); WARUM-Bullet „Entfernt Produktrückstände, Schmutz und Öl" ist allgemeine Reinigungs-Aussage, kein Fett-spezifischer Beleg; „Talgablagerungen lösen" steht nur unter APFELESSIG-Inhaltsstoff-Erklärung → K-06 schließt Inhaltsstoff-Mechanik aus. Symmetrische K-06-Entfernung. | **Edit A** ✓ |
| kopfhaut_peeling | `fettig` | Header-Untertitel „Fettiges Haar und Kopfhaut" (K-08 ✓) + WARUM „Reduziert überschüssiges Öl und stellt das Gleichgewicht der Kopfhaut wieder her" (K-06 ✓) | Status Quo |
| monat_black | `fettig` | **Ausschließlich** Header-Untertitel „Fettiges Haar und Kopfhaut / Verdichtend / Feine bis mittlere Haartypen" (K-08 ✓). Keine weitere WARUM-/IDEAL-Verankerung — Anlass für K-08-Einführung. | Status Quo (K-08-Primärbeispiel) |
| scalp_comfort_behandlung | `juckend_empfindlich,schuppig,trocken` | Header + IDEAL „trockene, gereizte, juckende, schuppige und empfindliche Kopfhaut" + Test-Bullets 89/96/96 % — alle 3 Tokens dreifach belegt (K-06 + K-07 ✓) | Status Quo |
| scalp_comfort_serum | `juckend_empfindlich,schuppig,trocken` | analog scalp_comfort_behandlung (Header + IDEAL + Test); zusätzlich Test 87 % „schützende Feuchtigkeitsbarriere" | Status Quo |
| **ir_clinical_kopfhautserum** | `-` → **`trocken`** | Cross-Check-Fund (war auf Default trotz „Kopfhaut" im Produktnamen). IDEAL-Bullet 3 wörtlich „Trockene Kopfhaut haben" (K-06 ✓); Test 87 % „Kopfhaut mit Feuchtigkeit versorgt" mit K-07-Verankerung via IDEAL. Andere Tokens geprüft + abgelehnt: `juckend_empfindlich` (Test 77 % „weniger juckt", keine Produktversprechen-Verankerung → K-07 ausschließt), `fettig` (Test 85 % „weniger fettig", keine Verankerung → K-07), `schuppig` (nirgendwo). | **Edit C** |

**Architektur-Klärung zur `kopfhaut`-Produktspalte** (Code-verifiziert, T-02): Node 12 Z. 26 (workflow_backup_20260610_222030_pre_signature_fix.json, „12 Scoring & Slot-Befüllung"):
```javascript
if (kopfhaut.includes(p.primary_scalp_state) || kopfhaut.length === 0)
  score += (kopfhaut.includes(p.primary_scalp_state) ? 2 : 0);
```
→ `kopfhaut` wirkt als **Score-Bonus +2 bei scalp-Match**, **nicht als Pool-Filter**. Default `-` (leeres Array) lässt durch ohne Bonus. Werte ohne Match lassen ebenfalls durch ohne Bonus. Cross-Verifikation: `haarstaerke`-Spalte filtert aktiv (Maria fein → nur `fein,mittel`/`alle`-Produkte im Pool) — Block-2-Filter-Spalten haben damit **unterschiedliche Wirkmechanismen**, Cross-Check für `haarstruktur` + `haarzustand` separat nötig.

**Edit A — Drift-Analyse (strikt-isoliert, 2026-06-13)** — Sheet-Setup beim Run: nur Edit A aktiv:
- 7/7 Profile produkt_key-identisch zur Pre-Edit-A-Baseline (test_results_20260612_000047.json vs. test_results_20260613_012029.json)
- Edit A entfernt essig_spuelung's +2-Score-Bonus für scalp=fettig-Profile (Node 12 Z. 26). Aktueller Test-Suite-Stand: nur anna hat scalp=fettig (siehe 🔴-Folgepunkt zu anna), bei anna feuert CON-07 mit count=1 → essig_spuelung käme score-mäßig nicht ins Slot-Rennen.
- Zusätzlich erweitert Edit A essig_spuelung's nominelle Pool-Zugehörigkeit; **CON-12** (`exclude_product` bei `primary_scalp_state=normal|trocken|juckend_empfindlich`) fängt das für maria/julia/bianca/sarah/vivien sofort wieder ab; lena (scalp=normal) ebenfalls. Netto-Pool-Effekt null.
- K-05-Fall: Stammdaten-Korrektur ohne aktuellen Scoring-Trigger.

**Edit C — Drift-Analyse (diff-isoliert nach Edit A, 2026-06-13)** — Sheet-Setup beim Run: A+C beide aktiv, C-Effekt per Diff zum A-Run extrahiert (Slot-Disjunktheit A/C verifiziert, siehe T-01):
- 7/7 Profile produkt_key-identisch + 7/7 CON-Listen identisch zu Edit-A-Run (test_results_20260613_095740.json vs. _012029.json)
- ir_clinical_kopfhautserum bleibt im filtered_pool von maria/julia/bianca/sarah (`irck_in_pool` true→true) — konsistent mit Score-Bonus-Mechanik (kein Filter)
- Edit C fügt ir_clinical_kopfhautserum's +2-Score-Bonus für scalp=trocken neu hinzu. Keines der 7 Test-Profile hat scalp=trocken (lena hat `trocken` nur im **haarzustand**, nicht im scalp_status). Score-Effekt jetzt null, **aber für künftige Profile mit scalp=trocken hat Edit C Slot-Wirkung**.
- K-05-Fall: PDF-Provenienz-Korrektur mit potentiellem zukünftigen Score-Effekt.

**Methodische Einsicht aus essig_spuelung-Analyse**: HANDOVER-Stufen-Audit-Tabellen (Block 1 Stufen 1-4) listen **Stufen-Deltas** (Aufnahmen pro Stufe), **nicht** finale Zellwerte. Pre-Edit-Ist-Stand muss immer per Sheet-Read verifiziert werden, nie aus Delta-Tabelle abgeleitet. Während Frage-2-Audit (essig_spuelung.glanz) wurde `glanz,feuchtigkeit` als bereits etabliert übersehen → falscher Edit-B-Vorschlag. Beide Tokens sind K-06-belegt (IDEAL „glänzend macht" + WARUM/IDEAL „mit Feuchtigkeit versorgt"), kein rückwirkender Block-1-Edit nötig.

**Backup**: `~/Projekte/myglowmatch/backups/sheets_20260612_225817_pre_block2_stufe1/produktdatenbank.csv`.

**Befund zur Baseline-Tabelle**: HANDOVER-Baseline (Z. 333 ff.) listete bei julia nur CON-12, alle Test-Runs seit 27.05. zeigen aber durchgängig **CON-07 + CON-12** (CON-07 routine-neutral, weil hitzeschutzspray bei julia ohnehin nicht in finale Routine geht). Cross-Check der anderen 6 Profile gegen Run-Output: alle 6 listen tatsächlich alle gefeuerten CONs (anna: CON-07; maria: CON-09,11,12; lena: CON-09,11; bianca: CON-02,09; vivien: CON-09,11,12; sarah: CON-09,11). **Implizite Konvention: „vollständig listen"** — julia war Update-Versäumnis (vermutlich 10.06.-A-F-Audit-Lücke, als count auf 4 + CON-12 aktualisiert wurde, CON-07 übersehen). Julia-Zeile heute korrigiert auf `CON-07, CON-12`. Kein offener Klärungspunkt mehr — Konvention ist implizit klar.

## Offene Punkte (priorisiert)

| Prio | Aufgabe | Stelle |
|---|---|---|
| 🟡 (in Arbeit) | Datenblatt-Provenienz-Audit — **Block 1 vollständig abgeschlossen** 2026-06-12 (Stufen 1+2+K-06+3+4+K-07); **Block 2 Stufe 1 (`kopfhaut`) in Arbeit 2026-06-13**, K-08 eingeführt; Block 2 Stufen 2-3 + Block 3 Rest + Block 4 offen | siehe Abschnitt „Datenblatt-Provenienz-Audit" oben |
| 🟡 | Sheet auf weitere `ist_bonding`-Misuses als Linien-Proxy prüfen — `ist_bonding` ist seit K-06 reines Wirkungs-Flag, Routing-Logik gehört auf `produktlinie` | Tabs: `map_slot_rules`, `map_conflict_rules`, weitere Filter |
| 🟢 (geklärt) | `kopfhaut`-Spalte der Produktdatenbank: **Score-Bonus +2 bei scalp-Match, kein Pool-Filter** (Node 12 Z. 26, Code-Zitat im Block-2-Stufe-1-Block). Block-2-Edits wirken als Score-Faktor für künftige Profile mit passendem scalp_status, nicht als Pool-Filter. Cross-Check für `haarstruktur` + `haarzustand` separat noch offen (`haarstaerke` ist verifiziert aktiv als Filter). | Node 12 Z. 26 |
| 🔴 | **Test-Profil `anna` scalp_status-Diskrepanz**: Run-Output sagt `scalp_status=['fettig']`, HANDOVER Z. 335 dokumentiert „keine_probleme" als Eingabe. **Warum 🔴**: falsches Test-Profil macht alle Drift-Analysen über anna wertlos — und damit jede darauf gestützte Audit-Entscheidung. Heute: anna's Routine (1× monat_black) ist nur dann legitim, wenn anna wirklich scalp=fettig hat; bei scalp=keine_probleme wäre monat_black eine Fehlempfehlung (Stammdaten-Bug-Klasse, vgl. monat_black-volumen-Bug 10.06.). Die Annahme „Test-Profile sind korrekt definiert" liegt implizit jeder 0/N-Drift-Aussage zugrunde — wenn sie für ein Profil bricht, brechen alle daran gemessenen Audit-Schritte. Klären **vor Block 2 Stufe 2**: (i) mappt Node 02 „keine_probleme → fettig" (echter Normalisierungs-Bug, betrifft jede Produktiv-Kundin mit dieser Eingabe) oder (ii) weicht `test_suite.py` von HANDOVER ab (Test-Daten-Fehler, betrifft nur die Test-Baseline)? | `test_suite.py` Profil-Definition + Node 02 jsCode |
| 🟡 | Node 06 Phase 2 migrieren (Ziele-Bonus, max +2 Pkt) | Node 06 inline |
| 🟡 | Node 05 migrieren (17 Bool-Flag-Heuristiken) | Node 05 inline, 69 LOC; bei Gelegenheit `needs_lightweight_logic` mitentfernen (seit #5 ungenutzt) |
| 🟢 | Node 11 Z. 163-164: `minimal → optional = []` als REQ-Regel ins Sheet | Node 11 inline |
| 🟢 | Node 12 Score-Gewichte (6 Inline-Werte 3/2/1) optional in `map_scoring_weights` | Node 12 inline |
| 🟢 | `extract_routine_output()`-Workaround in Test-Suite aufräumen | `test_suite.py` (CONFLICT_NODE-Merge seit Pass-Through in Node 12 überflüssig) |
| 🟢 | Sheet-Spalte `gewicht` in Produktdatenbank löschen | (vermutlich bereits leer/weg — Google-Sheets-API liefert sie nicht mehr aus) |
| 🟢 | Sheet-Loader 06a/06b/06c parallelisieren | Performance-Tuning, nur falls Live-Latenz spürbar |

## Referenzprofile (Soll-Werte für Regression)

Test-Profile in `test_suite.py`, alle mit `partner_id=desiree`, `email=info@myglowmatch.de`, `consent_recommendation=true`, `consent_marketing=false`.

| Profil | Eingabe-Kurzform | Pflegelevel | Pkt | Cap | Count | CON-Regeln |
|---|---|---|---|---|---|---|
| anna   | glatt, mittel, keine_probleme, unbehandelt, Hitze gelegentlich, minimal | LOW | 0 | 3 | 1 | CON-07 |
| maria  | wellig, fein, duenn, kraftlos, gefaerbt, Hitze nie, ausgewogen | MID | 7 | 5 | 5 | CON-09, CON-11, CON-12 |
| lena   | kraus, dick, trocken, frizz, gefaerbt, Hitze sehr_haeufig, bestmoeglich | HIGH | 15 | 10 | 7 | CON-09, CON-11 |
| julia  | glatt, fein, kraftlos, unbehandelt, Hitze gelegentlich, ausgewogen | MID | 4 | 5 | 4 | CON-07, CON-12 |
| bianca | wellig, mittel, trocken, gefaerbt, Hitze gelegentlich, ausgewogen | MID | 7 | 5 | 5 | CON-02, CON-09 |
| vivien | wellig, dick, keine_probleme, gefaerbt, Hitze regelmaessig, bestmoeglich | MID | 4 | 7 | 7 | CON-09, CON-11, CON-12 |
| sarah  | lockig, fein, stark_geschaedigt+spliss+trocken, blondiert, Hitze sehr_haeufig, bestmoeglich | HIGH | 18 | 10 | 7 | CON-09, CON-11 |

Sollwerte stand 2026-06-10-Full-Run nach Node-03-Removal. Vorherige Werte (julia count=5/CON-07,12; sarah count=8) reflektierten den Pre-A-F-Audit-Stand (vor monat_black- + smoothing_fohn_spray-Korrekturen).

## Test-Suite

Aufrufe:
- `python3 test_suite.py --profile anna` — Einzelprofil
- `python3 test_suite.py` — alle 7 Profile sequenziell
- `python3 test_suite.py --save` — zusätzlich Ergebnis als `test_results_<ts>.json`
- `python3 test_suite.py --verbose` — mehr Details

Härtungsstand (seit Session 3):
- `DEFAULT_MAX_WAIT = 90` (90 s Polling-Limit pro Profil)
- `TERMINAL_STATUSES = ("success",)` — Error-Executions nicht mehr als gültig akzeptiert
- `first_name`-Verifikation in `fetch_latest_execution()` — kein Profil-Mix-Up bei Latenz

Pipeline-Latenz aktuell ~38–47 s pro Profil (5 Sheet-Loader: 04a, 06a, 06b, 06c, 08a).

## n8n REST API — Operationsregeln

PUT `/api/v1/workflows/{id}` Body-Whitelisting:
- Top-Level: nur `name`, `nodes`, `connections`, `settings`
- `settings` darf nur enthalten: `saveExecutionProgress`, `saveManualExecutions`, `saveDataErrorExecution`, `saveDataSuccessExecution`, `executionTimeout`, `errorWorkflow`, `timezone`, `executionOrder`
- Aktueller Workflow nutzt davon nur `executionOrder`
- Read-only Felder (`id`, `versionId`, `createdAt`, `updatedAt`, `active`, `tags`, `triggerCount`, `pinData`, `meta`, `shared`, `isArchived`, `staticData` etc.) müssen aus dem Body raus
- `active`-State bleibt nach PUT erhalten
- Vor jedem PUT: GET → Backup als `~/Projekte/myglowmatch/workflow_backup_<ts>_<kontext>.json`
- Eventually Consistency der Execution-Liste: Polling über `since_id > baseline_id` (nicht `since_ts`)

Neuer Sheet-Loader-Node — Pflichtfelder:
```json
{
  "id": "<uuid>",
  "name": "<Nr><Suffix> <Beschreibung>",
  "type": "n8n-nodes-base.googleSheets",
  "typeVersion": 4.7,
  "position": [x, y],
  "parameters": {
    "documentId": {"__rl": true, "value": "<doc-id>", "mode": "list", ...},
    "sheetName": {"__rl": true, "value": "<tab-name>", "mode": "name"},
    "options": {}
  },
  "credentials": {"googleSheetsOAuth2Api": {"id": "zf5b37nhm7NZArlz", "name": "Google Sheets OAuth2 API"}}
}
```

Loader-Position-Konvention: oberhalb des Hauptflusses (Hauptfluss `y=144`, Loader `y≈-176`).

Code-Node-Zugriffspattern wenn Loader zwischen Producer und Consumer liegt:
- Sheet-Daten: `$items("<loader-name>")`
- Produkt-/Profil-Daten vom Vorgänger: `$node["<name>"].json` oder `$items("<name>")` statt `$input.all()`

## Bewusste Lücken

- `POOL-02` in `map_pool_filter` fehlt absichtlich (Gewicht-Regel war Bauchgefühl ohne Datenblatt-Beleg, bei Migration #5 entfernt)
- Spalte `gewicht` in Produktdatenbank — entweder leer oder bereits gelöscht (Sheets-API liefert sie nicht aus)
- `needs_lightweight_logic` in Node 05 wird seit Migration #5 von keinem Konsumenten mehr gelesen, bleibt aber bis zur Node-05-Migration berechnet
