# API-Kontrakt n8n ↔ Supabase

**Zweck**: Definiert die Endpunkte, die die Supabase-Instanz (bzw. das Next.js-Backend) für den n8n-Workflow bereitstellen muss, damit Multi-Tenant funktioniert. Der n8n-Workflow lädt pro Anfrage die Beraterin-Info und die Bibliothek anhand von `partner_id`.

**Status**: Draft, 2026-07-13, geschrieben zur Abstimmung zwischen n8n-Tab und Dashboard-Tab. Noch nicht implementiert.

**Kontext**: Der andere Tab baut aktuell das Dashboard + Supabase-Auth + DB-Schema (siehe Commit-Historie ab `a9a0139`). Dieses Dokument spezifiziert die Grenze, damit beide Seiten kompatibel entwickelt werden können.

---

## Base-URL

Empfohlen: `https://mybeautykey.de/api/v1/` — bedient von Next.js API-Routes, die serverseitig gegen Supabase queryen (nicht Supabase-URL direkt, damit wir Auth + Rate-Limiting + Response-Shaping kontrollieren).

Alternative: direkt gegen Supabase REST/PostgREST — nicht empfohlen, weil (a) n8n müsste Row-Level-Security umgehen (service_role_key exponiert), (b) Response-Shape bindet zu stark an DB-Schema.

## Auth

**Empfehlung**: statischer API-Key im Request-Header.

- Header: `x-n8n-service-key: <SERVICE_KEY>`
- Wird beim Deploy als Env-Var auf n8n-Cloud gesetzt (`N8N_SERVICE_KEY`) und in Next.js-API-Routes gegen `process.env.N8N_SERVICE_KEY` verifiziert
- Rotierbar (analog `N8N_WEBHOOK_SECRET`, siehe HANDOVER)
- Nur der n8n-Workflow kennt den Key — kein Client-Access

Alternative: JWT mit Beraterin-Kontext — überflüssig, weil der Workflow im Namen der Plattform arbeitet, nicht im Namen der Beraterin.

## Endpunkt 1: Partner-Info

**Zweck**: Node 17 lädt Beraterin-Kontaktdaten, Titel, Foto-URL für die Kundinnen-Mail.

### Request

```
GET /api/v1/beraterinnen/:partner_id
Headers:
  x-n8n-service-key: <SERVICE_KEY>
```

### Response 200

```json
{
  "partner_id": "sina",
  "name": "Sina Müller",
  "first_name": "Sina",
  "email": "sina@example.com",
  "phone": "0170 1234567",
  "whatsapp": "491701234567",
  "photo_url": "https://mybeautykey.de/uploads/beraterinnen/sina.jpg",
  "title": "Deine MONAT Markenpartnerin",
  "brand_partner_of": "MONAT",
  "aktiv": true
}
```

Feld-Beschreibungen:
- **`partner_id`** (string, required) — Slug, URL-safe, wird als externer Identifier vom Frontend an n8n gegeben
- **`name`** (string, required) — Vollname für Mail-Signatur
- **`first_name`** (string, required) — Vorname für Anrede (WhatsApp-Preview, „Hallo, ich bin {first_name}")
- **`email`** (string, required) — Reply-To, kann kurzfristig auch nur zur Info sein (Absender bleibt System-Mail)
- **`phone`** (string, optional) — Telefon-Kontakt
- **`whatsapp`** (string, optional) — internationale Nummer ohne + oder Leerzeichen (z.B. `491701234567`), für `wa.me/`-Link
- **`photo_url`** (string, optional) — absolute URL zum Foto (JPG/PNG), quadratisch, mind. 200×200px
- **`title`** (string, required) — Rolle unter dem Foto in der Mail (z.B. „Deine MONAT Markenpartnerin", „Deine Frisörin", „Deine Beauty-Beraterin")
- **`brand_partner_of`** (string, optional) — Marken-Bezug für Legal + Filterlogik (z.B. `MONAT`, `Redken`, `null` = unabhängig)
- **`aktiv`** (boolean, required) — false = Abo pausiert/gekündigt, n8n antwortet Kundin mit generischem Fallback

### Response 404

Partner nicht gefunden. n8n fällt auf DEFAULT-Partner zurück (siehe unten).

```json
{ "error": "partner_not_found", "partner_id": "<angefragte-id>" }
```

### Response 401

API-Key fehlt oder ungültig. n8n bricht sofort ab.

```json
{ "error": "unauthorized" }
```

### Fallback-Verhalten in n8n

Wenn Endpunkt nicht erreichbar (Timeout, 5xx) **oder** Partner nicht gefunden:
- n8n nutzt intern definierten DEFAULT-Partner (`{ name: "Beauty-Beraterin", title: "Deine persönliche Beraterin", … }`)
- Log-Eintrag in `beratungs_log` mit `partner_lookup_failed: true`
- Kundin bekommt trotzdem eine Mail (Business-Continuity)

## Endpunkt 2: Bibliothek

**Zweck**: Node 07 lädt die Produkt-Bibliothek der Beraterin.

### Request

```
GET /api/v1/beraterinnen/:partner_id/bibliothek
Headers:
  x-n8n-service-key: <SERVICE_KEY>
```

### Response 200

Array von Produkt-Objekten. **Kompatibel zum bestehenden `produktdatenbank`-Sheet-Schema** (siehe HANDOVER Zeile 41), damit Node 08/12/14/15 unverändert weiterlaufen können.

```json
{
  "partner_id": "sina",
  "aktualisiert_am": "2026-07-13T14:22:11Z",
  "produkte": [
    {
      "produkt_key": "sinas_bond_shampoo",
      "produktname_de": "Sinas Bond-Shampoo",
      "produktlinie": "bond_line",
      "produkttyp": "shampoo",
      "slot_typ": "shampoo",
      "routine_schritt": 1,
      "kopfhaut": "",
      "haarstruktur": "glatt,wellig,lockig,kraus",
      "haarstaerke": "fein,mittel,dick",
      "haarzustand": "trocken,glanzlos,haarbruch,spliss,stark_geschaedigt",
      "hauptfunktion": "reparatur",
      "nebenfunktionen": "feuchtigkeit",
      "pflegelevel": "MID,HIGH",
      "intensitaet": "intensiv",
      "ausschluss_bei": "",
      "ist_hitzeschutz": "FALSE",
      "ist_bonding": "TRUE",
      "ist_scalp_focus": "FALSE",
      "ist_bonding_line": "TRUE",
      "ist_hitzeschutz_solo": "FALSE",
      "ist_smoothing": "FALSE",
      "ist_trockenshampoo": "FALSE",
      "ist_zwei_in_eins": "FALSE",
      "ist_oel": "FALSE",
      "ist_peeling": "FALSE",
      "ist_haarwuchs": "FALSE",
      "ist_curl_volumen_booster": "FALSE",
      "locken_geeignet": "TRUE",
      "anwendung": "Auf nasses Haar auftragen, einmassieren, ausspülen.",
      "kombinationen": "sinas_bond_spuelung",
      "kombi_optional": "sinas_bond_leave_in",
      "aktiv": "TRUE"
    },
    { "produkt_key": "sinas_bond_spuelung", ... },
    ...
  ]
}
```

### Feld-Semantik: siehe [[project-bibliothek-design-locked]] und HANDOVER-Abschnitt „Bibliothek-UI"

Ableitungs-Regeln (Bibliothek-UI-Felder → Sheet-Spalten) müssen im API-Layer angewendet werden — das Frontend erfasst 9 Felder, die API-Response enthält die 33 Sheet-kompatiblen Spalten. Migration-Logik siehe HANDOVER.

### Response 200 mit leerer Bibliothek

```json
{
  "partner_id": "sina",
  "aktualisiert_am": "2026-07-13T14:22:11Z",
  "produkte": []
}
```

n8n prüft `produkte.length > 0` in Node 09 (Pool validieren) und bricht mit definiertem Fehler ab („Bibliothek leer, bitte Produkte hinzufügen"). Kundin bekommt Mail mit Hinweis „Beraterin baut Bibliothek gerade auf".

### Response 404

Wie Endpunkt 1 — Partner nicht gefunden.

### Response 402

Abo abgelaufen / nicht bezahlt. n8n bricht ab, System sendet Beraterin eine Erinnerungs-Mail.

```json
{ "error": "subscription_expired", "partner_id": "sina" }
```

### Cache-Header

Response sollte `Cache-Control: private, max-age=300` (5 Min) enthalten. n8n selbst kann pro Execution einen Fresh-Load machen (kurz genug, damit Änderungen in der Bibliothek nach spätestens 5 Min live sind).

## Rate-Limits (Empfehlung)

- 60 req/Min pro Partner-ID (n8n macht 2 Requests pro Kundinnen-Anfrage, das erlaubt ~30 gleichzeitige Kundinnen)
- 429 bei Überschreitung, n8n retryt mit exponential backoff (analog Migration #25)

## Auth-Level-Vergleich

| Wer ruft | Endpunkt | Auth |
|---|---|---|
| **n8n Workflow** | GET /api/v1/beraterinnen/:id, GET /api/v1/beraterinnen/:id/bibliothek | `x-n8n-service-key` |
| **Dashboard (Beraterin)** | POST /api/dashboard/products, GET /api/dashboard/analysen | Supabase-Auth-Session (RLS) |
| **Analyse-Frontend (Kundin)** | POST /webhook/glowmatch-haaranalyse (auf n8n direkt) | `x-glowmatch-secret` |

## Offene Punkte für Diskussion mit Dashboard-Tab

1. **Endpunkt-Location**: Next.js API-Routes unter `mybeautykey.de/api/v1/` oder auf separatem Sub-Domain (`api.mybeautykey.de`)?
2. **Response-Shape für Bibliothek**: Ableitung im API-Layer (Frontend liefert 9 Felder, API liefert 33 Sheet-Spalten) — wo genau lebt die Ableitungs-Logik? Vorschlag: als Postgres-View oder Supabase Edge Function, damit sowohl API als auch Direct-Query denselben Blickwinkel haben.
3. **DEFAULT-Partner-Handling**: soll der DEFAULT-Fall aus DB kommen (Zeile `partner_id='DEFAULT'` in der Beraterinnen-Tabelle) oder statisch im n8n-Code bleiben? Vorschlag: statisch im n8n-Code, damit auch bei kompletter DB-Down-Zeit Kundinnen antworten kommen.
4. **`aktualisiert_am` als Cache-Key**: kann Frontend `If-Modified-Since` senden und 304 zurückbekommen? Nice-to-have, nicht Blocker.
5. **Bulk-Endpunkt für Test-Suite**: `GET /api/v1/beraterinnen/:id/bibliothek?full=true` mit allen abgeleiteten Feldern für Debugging?

## Nicht-Ziele

- **Kein Schreib-Endpunkt für n8n** — n8n liest nur, das Dashboard schreibt (RLS-geschützt)
- **Keine Real-Time-Subscription** — 5-Min-Cache reicht
- **Keine Sub-Ressourcen wie Kombinations-Sets** — sind in `kombinationen`/`kombi_optional` als CSV eingebettet

---

Verwandt:
- [[project-bibliothek-design-locked]] — die 9 Bibliothek-Felder + Ableitungs-Regeln
- [[project-multi-tenant-architecture]] — Zielarchitektur
- HANDOVER-Abschnitt „Bibliothek-UI" — Feld-Übersicht
- HANDOVER-Abschnitt „System-Identifikation" — bestehender `x-glowmatch-secret`-Header, gleiches Muster
