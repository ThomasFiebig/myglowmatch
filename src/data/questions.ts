// ===================================================================
// myglowmatch – Der vollständige Fragenkatalog als Daten (Etappe 2)
// Quelle: docs/fragenkatalog.md
//
// Reihenfolge: 1 Intro-Bildschirm + 16 Fragen.
// Die 3 bedingten Fragen (curl_priority, ends_condition, heat_tools)
// haben ein "conditional"-Feld – sie erscheinen nur unter Bedingungen.
//
// WICHTIG: Die "value"-Werte (z. B. "juckend_empfindlich") müssen exakt
// so bleiben – genau diese Werte werden an den n8n-Webhook gesendet.
// ===================================================================

import type { Step } from "@/lib/types";

export const formSteps: Step[] = [
  // -----------------------------------------------------------------
  // Intro – Willkommensbildschirm (kein Eingabefeld)
  // -----------------------------------------------------------------
  {
    id: "intro",
    type: "intro",
    imageSrc: "/hero.jpg",
    imageAlt: "Frau mit gepflegtem, glänzendem Haar",
    headline: "Deine persönliche Haaranalyse",
    subHeadline: "In 2 Minuten zur Pflege, die zu dir passt.",
    points: [
      "Schnell beantwortet",
      "Persönliche Empfehlung",
      "Per E-Mail direkt zu dir",
    ],
    ctaLabel: "Jetzt starten",
    privacyNote: "Deine Daten werden DSGVO-konform verarbeitet.",
  },

  // -----------------------------------------------------------------
  // Frage 1 – Kopfhaut-Zustand (Mehrfachauswahl, max. 2)
  // -----------------------------------------------------------------
  {
    id: "scalp_status",
    type: "multi",
    field: "scalp_status",
    title: "Wie würdest du deine Kopfhaut aktuell beschreiben?",
    minSelect: 1,
    maxSelect: 2,
    options: [
      { value: "juckend_empfindlich", label: "juckend / empfindlich" },
      { value: "schuppig", label: "schuppig" },
      { value: "fettig", label: "fettig" },
      { value: "trocken", label: "trocken" },
      { value: "normal", label: "normal", exclusiveOption: true },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 2 – Haarstruktur (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "hair_structure",
    type: "single",
    field: "hair_structure",
    title: "Was ist deine natürliche Haarstruktur?",
    options: [
      { value: "glatt", label: "glatt" },
      { value: "wellig", label: "wellig" },
      { value: "lockig", label: "lockig" },
      { value: "kraus", label: "sehr lockig / kraus" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 2b – Locken / Wellen (CONDITIONAL)
  // Erscheint nur, wenn hair_structure NICHT "glatt" ist.
  // -----------------------------------------------------------------
  {
    id: "curl_priority",
    type: "single",
    field: "curl_priority",
    title: "Was ist dir bei deinen Locken / Wellen wichtiger?",
    conditional: {
      field: "hair_structure",
      operator: "notEquals",
      value: "glatt",
    },
    options: [
      { value: "mehr_definition", label: "mehr Definition" },
      { value: "mehr_volumen", label: "mehr Volumen" },
      { value: "beides", label: "Volumen & Definition" },
      { value: "glatt", label: "lieber glatt tragen" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 3 – Haarstärke (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "hair_thickness",
    type: "single",
    field: "hair_thickness",
    title: "Wie würdest du deine Haarstärke beschreiben?",
    options: [
      { value: "fein", label: "fein" },
      { value: "mittel", label: "mittel" },
      { value: "dick", label: "dick" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 4 – Haarzustand (Mehrfachauswahl, max. 3)
  // -----------------------------------------------------------------
  {
    id: "hair_condition",
    type: "multi",
    field: "hair_condition",
    title: "Welche Punkte treffen aktuell auf dein Haar zu?",
    minSelect: 1,
    maxSelect: 3,
    options: [
      { value: "stark_geschaedigt", label: "stark geschädigt" },
      { value: "haarbruch", label: "Haarbruch" },
      { value: "spliss", label: "Spliss" },
      { value: "trocken", label: "trocken" },
      { value: "frizz", label: "Frizz" },
      { value: "glanzlos", label: "glanzlos" },
      { value: "kraftlos", label: "kraftlos / wenig Volumen" },
      { value: "duenn", label: "dünner werdendes Haar" },
      {
        value: "keine_probleme",
        label: "keine besonderen Probleme",
        exclusiveOption: true,
      },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 4b – Längen / Spitzen (CONDITIONAL)
  // Erscheint nur, wenn hair_condition "trocken" ODER "frizz" enthält.
  // -----------------------------------------------------------------
  {
    id: "ends_condition",
    type: "single",
    field: "ends_condition",
    title: "Wie fühlen sich deine Längen und Spitzen an?",
    conditional: {
      field: "hair_condition",
      operator: "includesAny",
      value: ["trocken", "frizz"],
    },
    options: [
      { value: "weich_normal", label: "weich und normal" },
      { value: "leicht_trocken", label: "leicht trocken" },
      { value: "deutlich_trocken", label: "deutlich trocken / spröde" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 5 – Haarbehandlungen (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "hair_treatments",
    type: "single",
    field: "hair_treatments",
    title: "Ist dein Haar chemisch behandelt?",
    options: [
      { value: "nein", label: "nein" },
      { value: "gefaerbt", label: "gefärbt" },
      { value: "blondiert", label: "blondiert" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 6 – Hitze-Styling (Einfachauswahl)
  // Präzisiert auf Glätteisen/Lockenstab nach Migration #16
  // (2026-06-25). Föhn ist laut MONAT-PDFs keine Hitzeschäden-Quelle
  // ("Reduziere den Einsatz von Hitzestyling-Tools wie Glätteisen
  // und Lockenstäben") und wird daher nicht mehr abgefragt.
  // -----------------------------------------------------------------
  {
    id: "heat_frequency",
    type: "single",
    field: "heat_frequency",
    title: "Wie häufig nutzt du Glätteisen oder Lockenstab?",
    options: [
      { value: "nie_selten", label: "nie / sehr selten" },
      { value: "gelegentlich", label: "gelegentlich" },
      { value: "regelmaessig", label: "regelmäßig" },
      { value: "sehr_haeufig", label: "sehr häufig" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 7 – Waschverhalten (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "wash_frequency",
    type: "single",
    field: "wash_frequency",
    title: "Wie oft wäschst du deine Haare?",
    options: [
      { value: "taeglich", label: "täglich" },
      { value: "alle_2_3_tage", label: "alle 2–3 Tage" },
      { value: "1x_pro_woche", label: "1x pro Woche oder seltener" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 8 – Styling-Aufwand (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "styling_effort",
    type: "single",
    field: "styling_effort",
    title: "Wie stylst du deine Haare im Alltag?",
    options: [
      { value: "lufttrocknen", label: "lufttrocknen / minimal" },
      { value: "leichtes_styling", label: "leichtes Styling" },
      { value: "regelmaessiges_styling", label: "regelmäßiges Styling" },
      { value: "aufwendiges_styling", label: "aufwendiges Styling" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 9 – Pflegeziele (Mehrfachauswahl, max. 2)
  // -----------------------------------------------------------------
  {
    id: "care_goals",
    type: "multi",
    field: "care_goals",
    title: "Was ist dir bei deiner Haarpflege aktuell am wichtigsten?",
    minSelect: 1,
    maxSelect: 2,
    options: [
      { value: "reparatur", label: "Reparatur" },
      { value: "feuchtigkeit", label: "mehr Feuchtigkeit" },
      { value: "frizz_reduktion", label: "weniger Frizz" },
      { value: "glanz", label: "mehr Glanz" },
      { value: "volumen", label: "mehr Volumen" },
      { value: "gesunde_kopfhaut", label: "gesunde Kopfhaut" },
      { value: "verdichtend", label: "volleres Haar / mehr Dichte" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 10 – Routine-Präferenz (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "routine_preference",
    type: "single",
    field: "routine_preference",
    title: "Was passt eher zu dir?",
    options: [
      { value: "minimal", label: "so wenige Produkte wie möglich" },
      { value: "ausgewogen", label: "ausgewogene Routine" },
      { value: "bestmoeglich", label: "bestmögliches Ergebnis" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 11 – Zeitaufwand (Einfachauswahl)
  // -----------------------------------------------------------------
  {
    id: "time_commitment",
    type: "single",
    field: "time_commitment",
    title:
      "Wie viel Zeit möchtest du für deine Haarpflege + Styling investieren?",
    options: [
      { value: "sehr_wenig", label: "sehr wenig" },
      { value: "mittel", label: "mittel" },
      { value: "bewusst_regelmaessig", label: "bewusst & regelmäßig" },
    ],
  },

  // -----------------------------------------------------------------
  // Frage 12 – Kontaktdaten (Vorname + E-Mail)
  // -----------------------------------------------------------------
  {
    id: "contact",
    type: "contact",
    title: "Fast geschafft!",
    firstNameLabel: "Wie ist dein Vorname?",
    emailLabel:
      "An welche E-Mail-Adresse darf ich deine persönliche Produktempfehlung senden?",
    phoneLabel: "Telefonnummer",
    phoneDescription:
      "Optional – damit dich deine Beraterin auch per WhatsApp kontaktieren kann.",
    phonePlaceholder: "z. B. 0151 12345678",
  },

  // -----------------------------------------------------------------
  // Frage 13 – Einwilligung (DSGVO-Checkboxen + Absenden)
  // -----------------------------------------------------------------
  {
    id: "consent",
    type: "consent",
    title: "Einverständnis & Absenden",
    recommendationText:
      "Ich willige ein, dass meine Angaben zur Erstellung einer personalisierten Haarpflege-Empfehlung verarbeitet und mir per E-Mail zugesendet werden. Die Datenschutzhinweise habe ich gelesen.",
    marketingText:
      "Ich möchte zusätzlich Tipps, Angebote und Neuigkeiten per E-Mail erhalten.",
    submitLabel: "Jetzt persönliche Empfehlung erhalten →",
  },
];
