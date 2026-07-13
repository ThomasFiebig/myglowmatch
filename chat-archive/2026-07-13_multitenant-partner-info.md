# Session 2026-07-13 — Multi-Tenant-Baustein „Partner-Info dynamisch" live + Bibliothek-Design abgeschlossen

**Kern-Session:** Zwei Meilensteine an einem Tag. (1) Bibliothek-UI konzeptionell finalisiert und persistiert (`bibliothek.html` + `bibliothek-live.html` + Ableitungs-Regeln komplett dokumentiert, Commit `a9a0139` gepusht). (2) Erster echter Multi-Tenant-Baustein im n8n-Workflow live: Partner-Info kommt dynamisch aus neuem Sheet-Tab `beraterinnen`, Node 17 refactort, DEFAULT-Fallback markenneutral. Verifiziert durch Execution 1353 (alle 17 Nodes success, Anna-Empfehlung unverändert).

## Wiedereinstieg-Prompt für nächste Session

> Lies `chat-archive/2026-07-13_multitenant-partner-info.md`.
> Multi-Tenant-Sprint hat begonnen. Partner-Info-Baustein ist live
> (siehe [[project-multitenant-partner-info-live]]). Bibliothek-Design
> ist finalisiert (siehe [[project-bibliothek-design-locked]]).
> **Ein zweiter Chat-Tab arbeitet parallel** an Supabase-Auth + DB-Schema +
> Dashboard-KPIs (Commit `a9a0139` letzter gemeinsamer Stand, hier bewusst
> nichts committet nach diesem Punkt). API-Kontrakt zwischen den Tabs:
> `docs/api-kontrakt-n8n-supabase.md`.
>
> Offene Blocker für Multi-Tenant-Launch:
> (a) Node 07 (Bibliothek-Loader) auf HTTP-DB-Query umstellen — braucht
>     Supabase-API-Endpunkte vom anderen Tab
> (b) Sinas Zeile im `beraterinnen`-Sheet anlegen (echte Daten)
> (c) Beraterin-Registrierung + Stripe-Abo
>
> **Vor Commit hier: erst prüfen ob der andere Tab gepusht hat, dann
> git pull, dann uncommitete Skripte + docs zusammen mit dessen Kram
> als getrennter Commit.**

## Was heute passiert ist

### Vormittag — Bibliothek-Design finalisiert (Commit `a9a0139`)

Fortsetzung der Design-Arbeit vom 07-12. Konkrete Änderungen:
- Layer-2-Analyse abgeschlossen: PFL-OV-01…04 waren bereits markenneutral, kein Umbau nötig
- 5 UI-Änderungen im Bibliothek-Mockup: conditional 2-in-1-Feld bei Shampoo, Nutzen-Tabelle Default-„—" sichtbar, Sub-Serien als skalierbarer Multi-Chip (statt Ja/Nein), Wirkstärke-Beschreibung als Radio-Chip (Default „vielseitig"), Info-Toggles (`<details class="info-toggle">`) für alle Erklär-Texte
- Bezugsquelle-Link entfernt (produkt_url ungenutzt, siehe [[project_produkt_url_aufgegeben]])
- Zwei Dateien getrennt: `demo/bibliothek.html` (Konzept-Mockup mit Hero/Erklär-Cards) und `demo/bibliothek-live.html` (Design-Referenz für React-Component im Dashboard, nur Formular)
- `public/konzept/bibliothek.html` gesynct, alte Sina-Version umbenannt zu `bibliothek-v1-original.html` mit Deprecation-Banner
- HANDOVER-Abschnitt „Bibliothek-UI" mit 9 Feldern + Ableitungs-Regeln + UX-Prinzipien
- Memory: [[project-bibliothek-design-locked]] neu, `MEMORY.md`-Index erweitert

### Nachmittag — Multi-Tenant-Check des Workflows

Systematischer Health-Check: welche Marken-Bindungen hat der aktuelle Workflow?
- **Engine-Nodes (04-15)**: markenneutral, alle inline-„Marken"-Referenzen sind Sync-Daten oder Kommentare
- **Sheet-Loader**: alle 11 googleSheets-Nodes zeigen fix auf MONAT-Sheet-Doc-ID (blocker)
- **Node 17 „Mail formulieren"**: statisches Partner-Objekt-Lookup mit nur 2 Einträgen (Desiree, DEFAULT)
- **`partner_id`**: läuft schon durch den ganzen Workflow (Node 02 → 15 → 17), gute Grundlage

User-Entscheidung: **Weg B — Multi-Tenant vollständig statt Kosmetik-Fix**. Nächster Kontakt mit Sina erst wenn System launch-ready ist.

### Sprint-Planung → Kollision mit parallelem Tab bemerkt

Ich fing an Supabase zu planen und wollte gerade `npm install @supabase/supabase-js` triggern, da meldete User: **ein zweiter Chat-Tab arbeitet parallel** an Supabase, Dashboard, RLS, Server Actions, Follow-up-Chips. Sein anderer Tab hatte bereits gemeldet: „Live-Dashboard läuft, Kundinnen-Tabelle mit Chips klickbar, Sandbox-Modus". Ich habe sofort gestoppt.

Klarheit: git-lokal ist noch nichts vom anderen Tab da (commited aber nicht gepusht oder in anderem Verzeichnis). Vereinbarung: hier keinen Commit machen, bis der andere Tab gepusht hat.

### Was ohne Konflikt geht: n8n-Workflow-Arbeit

n8n liegt außerhalb des Git-Repos. Wir haben zwei parallele Arbeitsstränge festgelegt:
- **A**: Node 17 Partner-Info entkoppeln (Sheet-Tab + Loader-Node + Node-Refactor)
- **B**: API-Kontrakt-Dokument als Grenzlinie zum anderen Tab

Beide grünes Licht bekommen, parallel bearbeitet.

### Task 5: API-Kontrakt-Dokument (`docs/api-kontrakt-n8n-supabase.md`)

Spezifiziert:
- Zwei Endpunkte: `GET /api/v1/beraterinnen/:partner_id` + `GET /api/v1/beraterinnen/:partner_id/bibliothek`
- Auth via `x-n8n-service-key`-Header (rotierbar, analog `N8N_WEBHOOK_SECRET`)
- Response-Schemas kompatibel zum bestehenden `produktdatenbank`-Sheet-Schema (damit Nodes 08/12/14/15 unverändert bleiben)
- Fallback-Verhalten: n8n hat DEFAULT-Partner + leere-Bibliothek-Behandlung
- Cache-Headers, Rate-Limits, offene Diskussionspunkte zwischen den Tabs

### Task 1: Sheet-Tab `beraterinnen` angelegt

Skript `create_beraterinnen_tab.py`, idempotent. Header + 1 Zeile (Desiree, 1:1 aus altem Node-17-Hardcode). 10 Spalten: `partner_id, name, first_name, email, phone, whatsapp, photo_url, title, brand_partner_of, aktiv`. Verifiziert per Re-Read.

### Task 2: Loader-Node im Workflow

Skript `patch_add_beraterinnen_loader.py`. Neuer googleSheets-Reader zwischen Node 15 („Routine sortieren") und Node 17 („Mail formulieren"). Verkabelung: `15 → 16z → 17`. Erster Deploy-Versuch scheiterte an falschem Credential-Type (`googleApi` statt `googleSheetsOAuth2Api`) — n8n hatte den Node trotzdem in die Struktur übernommen. Reparatur per `fix_beraterinnen_loader_credentials.py` (in-place typeVersion 4.5→4, credentials-Key korrigiert). Zweite Verifikation grün.

### Task 3: Node 17 refactoren

Skript `patch_node17_partner_loader.py`. Statisches `partners`-Objekt durch dynamischen Lookup ersetzt:
```javascript
let partner = DEFAULT_PARTNER;
try {
  const partnerRows = $items("16z Partner-Info laden") || [];
  const found = partnerRows.find(item => String(item.json.partner_id) === String(partnerId));
  if (found && String(found.json.aktiv).toUpperCase() === 'TRUE') partner = found.json;
} catch (e) { /* Loader down → DEFAULT_PARTNER */ }
```
DEFAULT-Fallback bleibt inline (Business-Continuity bei Sheet-Ausfall), Titel markenneutral: „Deine persönliche Beauty-Beraterin".

### Task 4: MONAT-Baseline-Test — Regression + Fix

Erster Test-Lauf (Execution 1352): 
- ✅ Node 16z + Node 17 success
- 🔴 Node 18 „No recipients defined" — Kunden-Mail fehlgeschlagen
- Ursache: `to_email = ''` in Node-17-Output, weil `data.normalized` undefined

**Erkenntnis (Lektion für zukünftige Node-Insertions)**: Verkabelung `15 → 16z → 17` machte Node 16z's Sheet-Row zum `$input.item.json` von Node 17. Der bisherige Code `const data = $input.item.json` griff auf die Sheet-Row zu statt auf Node-15-Output. **Fix** (`fix_node17_data_source.py`): `const data = $node["15 Routine sortieren"].json`. Damit greift Node 17 explizit auf Node 15 zu (Kundenprofil), und `$items("16z ...")` bleibt für Partner-Info verfügbar.

Zweiter Test-Lauf (Execution 1353):
- ✅ Alle 17 Nodes success
- ✅ Anna-Empfehlung unverändert: `monat_black` (Baseline-konform)
- ✅ Node 17 Output vollständig: `to_email='info@myglowmatch.de'`, `first_name='Anna-TEST'`, `partner_name='Desirée Fiebig'` (aus Sheet), `partner_to_email='beratung@veradex.de'` (aus Sheet)

## Multi-Tenant-Fortschritt (Ende des Tages)

| Baustein | Status |
|---|---|
| `partner_id` durch Workflow | ✅ war schon da |
| **Partner-Info dynamisch aus DB/Sheet** | ✅ **heute erledigt** — Zwischenschritt Sheet, später HTTP-API |
| Bibliothek-UI-Design | ✅ heute morgen persistiert |
| Beraterin-Registrierung (Frontend) | 🟡 andere Tab arbeitet dran |
| DB-Schema + Auth | 🟡 anderer Tab arbeitet dran |
| Dashboard mit KPIs + Kundinnen-Tabelle | 🟡 anderer Tab hat's live laut Meldung |
| Node 07 (Bibliothek-Loader) auf DB-API | 🔴 wartet auf Supabase-API-Endpunkte |
| Stripe-Abo | 🔴 offen |
| Sinas Zeile im Sheet | 🔴 offen (Daten fehlen) |

## Persistenz am Session-Ende

- **Memory (neu)**: `project-multitenant-partner-info-live.md` — was live ist, was noch offen, Skript-Liste, Sync-Hinweis
- **Memory-Update**: `MEMORY.md`-Index erweitert
- **Session-Doku**: diese Datei
- **Sheet + Workflow**: alle Änderungen live auf n8n-Cloud + Google Sheet — kein Commit nötig für Persistenz
- **Lokale Skripte + Doku uncommitted** (bewusst): `check_sheet_tabs.py`, `create_beraterinnen_tab.py`, `patch_add_beraterinnen_loader.py`, `fix_beraterinnen_loader_credentials.py`, `patch_node17_partner_loader.py`, `fix_node17_data_source.py`, `docs/api-kontrakt-n8n-supabase.md`. Nächster Chat: **erst prüfen ob der andere Tab gepusht hat, dann `git pull`, dann bewusst committen.**

## Bewusst NICHT gemacht in dieser Session

- **Kein `git commit` nach `a9a0139`** — Koordination mit dem anderen Tab
- **Kein Supabase-Setup hier** — läuft im anderen Tab
- **Node 07 nicht angefasst** — braucht die API vom anderen Tab
- **Sinas Zeile nicht angelegt** — echte Daten fehlen (Name, Foto, WhatsApp)
- **HANDOVER-Update für Node 16z/17-Refactor** — hätte dazwischen synchronisieren müssen, im nächsten Chat nachziehen

## Offene Punkte für nächste Session(s)

1. **Sync mit anderem Tab**: prüfen was er gepusht hat, mit `git pull` einholen, dann diesen Kram sauber commiten
2. **HANDOVER-Update** für den heutigen Multi-Tenant-Fortschritt (Node 16z, Node-17-Refactor, `beraterinnen`-Tab)
3. **Node 07 auf HTTP-Loader umbauen** — sobald Supabase-API-Endpunkte für die Bibliothek fertig sind (API-Kontrakt liegt vor)
4. **Stripe-Integration** in Zusammenarbeit mit dem anderen Tab
5. **Sinas Zeile** im Sheet ergänzen (nach echten Daten fragen)
