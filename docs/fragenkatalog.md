# myglowmatch.de – Vollständiger Fragenkatalog
## Technische Implementierungsreferenz für HTML-Fragebogen

---

## Übersicht

- **16 Fragen** (11 Pflicht + 5 Conditional)
- **Webhook-Ziel:** n8n Production URL (wird separat mitgeteilt)
- **Partner-ID:** wird als URL-Parameter übergeben: `myglowmatch.de/martina` → `partner_id=martina`
- **Submit:** JSON per POST an n8n Webhook

---

## JSON-Format beim Submit

Das Formular sendet beim Absenden folgendes JSON an n8n:

```json
{
  "partner_id": "martina",
  "first_name": "Desiree",
  "email": "desiree@example.de",
  "consent_recommendation": true,
  "consent_marketing": false,
  "scalp_status": ["normal"],
  "hair_structure": "wellig",
  "hair_thickness": "mittel",
  "hair_condition": ["trocken", "frizz"],
  "ends_condition": "leicht_trocken",
  "hair_treatments": "nein",
  "heat_frequency": "gelegentlich",
  "heat_tools": ["fohn"],
  "wash_frequency": "alle_2_3_tage",
  "styling_effort": "leichtes_styling",
  "curl_priority": "mehr_definition",
  "care_goals": ["feuchtigkeit", "glanz"],
  "routine_preference": "ausgewogen",
  "time_commitment": "mittel"
}
```

**Wichtig:** Alle Werte müssen exakt so gesendet werden wie in den Antwortoptionen angegeben (technische Werte, keine Anzeigetexte).

---

## Alle Fragen im Detail

---

### Seite 1 – Intro
**Kein Feld** – nur Willkommenstext und Start-Button.

> „Beantworte ein paar kurze Fragen und erhalte deine persönliche Produktempfehlung, abgestimmt auf dein Haar und deine Kopfhaut."
> Dauer: ca. 2–3 Minuten

---

### Frage 1 – Kopfhaut-Zustand
**Field Name:** `scalp_status`
**Typ:** Mehrfachauswahl (max. 2 auswählbar)
**Pflicht:** Ja

**Anzeigetext:** „Wie würdest du deine Kopfhaut aktuell beschreiben? (max. 2 auswählen)"

| Anzeigetext | Technischer Wert |
|---|---|
| juckend / empfindlich | `juckend_empfindlich` |
| schuppig | `schuppig` |
| fettig | `fettig` |
| trocken | `trocken` |
| normal | `normal` |

---

### Frage 2 – Haarstruktur
**Field Name:** `hair_structure`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Was ist deine natürliche Haarstruktur?"

| Anzeigetext | Technischer Wert |
|---|---|
| glatt | `glatt` |
| wellig | `wellig` |
| lockig | `lockig` |
| sehr lockig / kraus | `kraus` |

**Conditional Logic:**
- Wenn `glatt` gewählt → Frage 2b (curl_priority) überspringen → weiter zu Frage 3

---

### Frage 2b – Locken / Wellen (CONDITIONAL)
**Field Name:** `curl_priority`
**Typ:** Einfachauswahl
**Pflicht:** Ja (nur wenn hair_structure = wellig, lockig oder kraus)
**Anzeigen wenn:** `hair_structure` ist NICHT `glatt`

**Anzeigetext:** „Was ist dir bei deinen Locken / Wellen wichtiger?"

| Anzeigetext | Technischer Wert |
|---|---|
| mehr Definition | `mehr_definition` |
| mehr Volumen | `mehr_volumen` |
| beides | `beides` |

---

### Frage 3 – Haarstärke
**Field Name:** `hair_thickness`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Wie würdest du deine Haarstärke beschreiben?"

| Anzeigetext | Technischer Wert |
|---|---|
| fein | `fein` |
| mittel | `mittel` |
| dick | `dick` |

---

### Frage 4 – Haarzustand
**Field Name:** `hair_condition`
**Typ:** Mehrfachauswahl (max. 3 auswählbar)
**Pflicht:** Ja

**Anzeigetext:** „Welche Punkte treffen aktuell auf dein Haar zu? (max. 3 auswählen – wenn nichts zutrifft: ‚keine besonderen Probleme' wählen)"

| Anzeigetext | Technischer Wert |
|---|---|
| stark geschädigt | `stark_geschaedigt` |
| Haarbruch | `haarbruch` |
| Spliss | `spliss` |
| trocken | `trocken` |
| Frizz | `frizz` |
| glanzlos | `glanzlos` |
| kraftlos / wenig Volumen | `kraftlos` |
| dünner werdendes Haar | `duenn` |
| keine besonderen Probleme | `keine_probleme` |

**Conditional Logic:**
- Wenn `trocken` ODER `frizz` gewählt → Frage 4b (ends_condition) anzeigen
- Sonst → Frage 4b überspringen

---

### Frage 4b – Längen / Spitzen (CONDITIONAL)
**Field Name:** `ends_condition`
**Typ:** Einfachauswahl
**Pflicht:** Ja (nur wenn angezeigt)
**Anzeigen wenn:** `hair_condition` enthält `trocken` ODER `frizz`

**Anzeigetext:** „Wie fühlen sich deine Längen und Spitzen an?"

| Anzeigetext | Technischer Wert |
|---|---|
| weich und normal | `weich_normal` |
| leicht trocken | `leicht_trocken` |
| deutlich trocken / spröde | `deutlich_trocken` |

---

### Frage 5 – Haarbehandlungen
**Field Name:** `hair_treatments`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Ist dein Haar chemisch behandelt?"

| Anzeigetext | Technischer Wert |
|---|---|
| nein | `nein` |
| gefärbt | `gefaerbt` |
| blondiert | `blondiert` |

---

### Frage 6 – Hitze-Styling
**Field Name:** `heat_frequency`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Wie häufig nutzt du Hitze-Styling?"

| Anzeigetext | Technischer Wert |
|---|---|
| nie / sehr selten | `nie_selten` |
| gelegentlich | `gelegentlich` |
| regelmäßig | `regelmaessig` |
| sehr häufig | `sehr_haeufig` |

**Conditional Logic:**
- Wenn `nie_selten` gewählt → Frage 6b (heat_tools) überspringen
- Wenn `gelegentlich`, `regelmaessig` ODER `sehr_haeufig` → Frage 6b anzeigen

---

### Frage 6b – Hitze-Tools (CONDITIONAL)
**Field Name:** `heat_tools`
**Typ:** Mehrfachauswahl
**Pflicht:** Ja (nur wenn angezeigt)
**Anzeigen wenn:** `heat_frequency` ist `gelegentlich`, `regelmaessig` ODER `sehr_haeufig` (also alles außer `nie_selten`)

**Anzeigetext:** „Welche Hitze-Tools nutzt du?"

| Anzeigetext | Technischer Wert |
|---|---|
| Föhn | `fohn` |
| Glätteisen | `glaetteisen` |
| Lockenstab | `lockenstab` |

---

### Frage 7 – Waschverhalten
**Field Name:** `wash_frequency`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Wie oft wäschst du deine Haare?"

| Anzeigetext | Technischer Wert |
|---|---|
| täglich | `taeglich` |
| alle 2–3 Tage | `alle_2_3_tage` |
| 1x pro Woche oder seltener | `1x_pro_woche` |

---

### Frage 8 – Styling-Aufwand
**Field Name:** `styling_effort`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Wie stylst du deine Haare im Alltag?"

| Anzeigetext | Technischer Wert |
|---|---|
| lufttrocknen / minimal | `lufttrocknen` |
| leichtes Styling | `leichtes_styling` |
| regelmäßiges Styling | `regelmaessiges_styling` |
| aufwendiges Styling | `aufwendiges_styling` |

---

### Frage 9 – Pflegeziele
**Field Name:** `care_goals`
**Typ:** Mehrfachauswahl (max. 2 auswählbar)
**Pflicht:** Ja

**Anzeigetext:** „Was ist dir bei deiner Haarpflege aktuell am wichtigsten? (max. 2 auswählen)"

| Anzeigetext | Technischer Wert |
|---|---|
| Reparatur | `reparatur` |
| mehr Feuchtigkeit | `feuchtigkeit` |
| weniger Frizz | `frizz_reduktion` |
| mehr Glanz | `glanz` |
| mehr Volumen | `volumen` |
| gesunde Kopfhaut | `gesunde_kopfhaut` |
| volleres Haar / mehr Dichte | `mehr_dichte` |

---

### Frage 10 – Routine-Präferenz
**Field Name:** `routine_preference`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Was passt eher zu dir?"

| Anzeigetext | Technischer Wert |
|---|---|
| so wenige Produkte wie möglich | `minimal` |
| ausgewogene Routine | `ausgewogen` |
| bestmögliches Ergebnis | `bestmoeglich` |

---

### Frage 11 – Zeitaufwand
**Field Name:** `time_commitment`
**Typ:** Einfachauswahl
**Pflicht:** Ja

**Anzeigetext:** „Wie viel Zeit möchtest du für deine Haarpflege + Styling investieren?"

| Anzeigetext | Technischer Wert |
|---|---|
| sehr wenig | `sehr_wenig` |
| mittel | `mittel` |
| bewusst & regelmäßig | `bewusst_regelmaessig` |

---

### Frage 12 – Kontaktdaten
**Field Name:** `first_name` + `email`
**Typ:** Texteingabe + E-Mail-Eingabe
**Pflicht:** Ja

**Anzeigetext Vorname:** „Wie ist dein Vorname?"
**Anzeigetext E-Mail:** „An welche E-Mail-Adresse darf ich deine persönliche Produktempfehlung senden?"

---

### Frage 13 – Einwilligung (DSGVO)
**Field Name:** `consent_recommendation` + `consent_marketing`
**Typ:** Checkboxen
**Pflicht:** `consent_recommendation` = Pflicht, `consent_marketing` = optional

**consent_recommendation Text:**
„Ich willige ein, dass meine Angaben zur Erstellung einer personalisierten Haarpflege-Empfehlung verarbeitet und mir per E-Mail zugesendet werden. Die Datenschutzhinweise habe ich gelesen."

**consent_marketing Text:**
„Ich möchte zusätzlich Tipps, Angebote und Neuigkeiten per E-Mail erhalten."

**Submit-Button Text:** „Jetzt persönliche Empfehlung erhalten →"

---

## Wichtige Hinweise für die Implementierung

### Partner-ID aus URL lesen
```javascript
const urlParams = new URLSearchParams(window.location.search);
const partnerId = urlParams.get('partner_id') || 
                  window.location.pathname.split('/').pop() || 
                  'DEFAULT';
```

### Validierungsregeln
- `scalp_status`: min. 1, max. 2 Auswahlen
- `hair_condition`: min. 1, max. 3 Auswahlen
- `care_goals`: min. 1, max. 2 Auswahlen
- `heat_tools`: min. 1 Auswahl (nur wenn angezeigt)
- `email`: muss gültiges E-Mail-Format haben
- `consent_recommendation`: muss angehakt sein (Pflicht)

### Conditional Logic Zusammenfassung
| Frage | Bedingung | Aktion |
|---|---|---|
| curl_priority (2b) | hair_structure ≠ glatt | anzeigen |
| ends_condition (4b) | hair_condition enthält trocken ODER frizz | anzeigen |
| heat_tools (6b) | heat_frequency = gelegentlich, regelmaessig ODER sehr_haeufig | anzeigen |

### n8n Webhook
- **Methode:** POST
- **Content-Type:** application/json
- **URL:** wird separat mitgeteilt (n8n Production URL)

---

## Node 02 in n8n – neuer Code nach Umstieg von Tally

Node 02 muss nach dem Umstieg angepasst werden damit er das neue JSON-Format liest:

```javascript
// NODE 02: Felder aus eigenem Fragebogen lesen
const body = $input.item.json.body || $input.item.json;

const raw = {
  partner_id:             body.partner_id || 'DEFAULT',
  first_name:             body.first_name || '',
  email:                  body.email || '',
  scalp_status:           Array.isArray(body.scalp_status) ? body.scalp_status : [body.scalp_status].filter(Boolean),
  hair_structure:         body.hair_structure || '',
  hair_thickness:         body.hair_thickness || '',
  hair_condition:         Array.isArray(body.hair_condition) ? body.hair_condition : [body.hair_condition].filter(Boolean),
  ends_condition:         body.ends_condition || null,
  hair_treatments:        body.hair_treatments || 'nein',
  heat_frequency:         body.heat_frequency || 'nie_selten',
  heat_tools:             Array.isArray(body.heat_tools) ? body.heat_tools : [body.heat_tools].filter(Boolean),
  wash_frequency:         body.wash_frequency || 'alle_2_3_tage',
  styling_effort:         body.styling_effort || 'leichtes_styling',
  curl_priority:          body.curl_priority || null,
  care_goals:             Array.isArray(body.care_goals) ? body.care_goals : [body.care_goals].filter(Boolean),
  routine_preference:     body.routine_preference || 'ausgewogen',
  time_commitment:        body.time_commitment || 'mittel',
  consent_recommendation: body.consent_recommendation === true || body.consent_recommendation === 'true',
  consent_marketing:      body.consent_marketing === true || body.consent_marketing === 'true',
};

return [{ json: { raw_input: raw, partner_id: raw.partner_id } }];
```

**Wichtig:** Node 03 bleibt unverändert – die technischen Werte kommen jetzt bereits normiert aus dem Fragebogen, aber Node 03 schadet nicht als zusätzliche Sicherheitsschicht.
