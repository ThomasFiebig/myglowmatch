// ===================================================================
// mybeautykey – Datenmodell (Etappe 2)
// Diese Datei beschreibt die "Baupläne": Wie darf eine Frage aussehen?
// Hier stehen KEINE echten Fragen – die kommen in src/data/questions.ts.
// ===================================================================

// -------------------------------------------------------------------
// Eine einzelne Antwortoption (bei Einfach- und Mehrfachauswahl).
// "value" ist der technische Wert, der ins JSON an n8n geht.
// "label" ist der Text, den der Nutzer auf dem Bildschirm sieht.
// -------------------------------------------------------------------
export type Option = {
  value: string;
  label: string;
  // Wenn true: diese Option schließt alle anderen aus (z. B. "keine
  // besonderen Probleme"). Wird von der MultiChoice-Komponente
  // ausgewertet – siehe dort.
  exclusiveOption?: boolean;
};

// -------------------------------------------------------------------
// Eine Bedingung steuert, OB eine Frage angezeigt wird.
// Beispiel: Frage 2b erscheint nur, wenn hair_structure NICHT "glatt" ist.
//
//  field    = welches frühere Antwortfeld wird geprüft
//  operator = wie wird verglichen:
//             "equals"      -> Antwort ist genau dieser Wert
//             "notEquals"   -> Antwort ist NICHT dieser Wert
//             "in"          -> Antwort ist einer der Werte in der Liste
//             "includesAny" -> Mehrfach-Antwort enthält einen der Werte
//  value    = der Vergleichswert (einzeln oder als Liste)
// -------------------------------------------------------------------
export type Condition = {
  field: string;
  operator: "equals" | "notEquals" | "in" | "includesAny";
  value: string | string[];
};

// -------------------------------------------------------------------
// Felder, die JEDER Schritt hat.
// "conditional" ist optional (das "?" bedeutet: darf fehlen).
// Fehlt es, wird der Schritt immer angezeigt.
// -------------------------------------------------------------------
type StepBase = {
  id: string;
  conditional?: Condition;
};

// -------------------------------------------------------------------
// Schritt-Typ 1: Intro-/Hero-Bildschirm (Bild, Texte, Start-Button)
// -------------------------------------------------------------------
export type IntroStep = StepBase & {
  type: "intro";
  imageSrc: string; // Pfad zum Hero-Bild (z. B. /hero.jpg)
  imageAlt: string; // Alternativtext für das Bild
  headline: string;
  subHeadline: string;
  points: string[]; // genau 3 kurze Mini-Punkte
  ctaLabel: string; // Beschriftung des Start-Buttons
  privacyNote: string; // DSGVO-Hinweis unter dem Button
};

// -------------------------------------------------------------------
// Schritt-Typ 2: Einfachauswahl (genau eine Option wählbar)
// -------------------------------------------------------------------
export type SingleStep = StepBase & {
  type: "single";
  field: string; // Feldname im JSON, z. B. "hair_structure"
  title: string; // die Frage als Anzeigetext
  options: Option[];
};

// -------------------------------------------------------------------
// Schritt-Typ 3: Mehrfachauswahl (mehrere Optionen, mit Min/Max-Grenze)
// -------------------------------------------------------------------
export type MultiStep = StepBase & {
  type: "multi";
  field: string;
  title: string;
  options: Option[];
  minSelect: number; // mindestens so viele müssen gewählt werden
  maxSelect: number; // höchstens so viele dürfen gewählt werden
};

// -------------------------------------------------------------------
// Schritt-Typ 4: Kontaktdaten + DSGVO-Einwilligung + Absenden
// (letzter Schritt vor der Analyse — E-Mail entfällt, weil das
// Ergebnis direkt im Browser erscheint und kein Versand mehr nötig ist.)
// -------------------------------------------------------------------
export type ContactStep = StepBase & {
  type: "contact";
  title: string;
  firstNameLabel: string;
  // Telefonnummer: optionales Feld für WhatsApp-Kontakt zur Beraterin.
  phoneLabel: string;
  phoneDescription: string;
  phonePlaceholder: string;
  // Optionales E-Mail-Opt-in — Kundin kann Analyse zusätzlich als Mail erhalten.
  emailOptInLabel: string;
  emailPlaceholder: string;
  // Pflicht-Einwilligung — jetzt auf derselben Seite wie Kontakt.
  consentText: string;
  // CTA-Label des Absende-Buttons („Zu deiner Haaranalyse →").
  submitLabel: string;
};

// -------------------------------------------------------------------
// "Step" fasst alle Schritttypen zusammen.
// -------------------------------------------------------------------
export type Step = IntroStep | SingleStep | MultiStep | ContactStep;

// -------------------------------------------------------------------
// "QuestionStep" = alle Schritte AUSSER dem Intro, also die echten
// Fragen. Sie haben alle ein "title"-Feld. Praktisch für Komponenten,
// die nur Fragen anzeigen (nie das Intro).
// -------------------------------------------------------------------
export type QuestionStep = SingleStep | MultiStep | ContactStep;

// -------------------------------------------------------------------
// Das finale JSON, das beim Absenden an den n8n-Webhook geht.
// Diese Struktur ist 1:1 das Format aus docs/fragenkatalog.md.
// Übersprungene Conditional-Fragen werden als null gesendet.
// -------------------------------------------------------------------
export type SubmissionData = {
  partner_id: string;
  first_name: string;
  email: string;
  phone: string; // optional – leer, wenn nicht angegeben
  consent_recommendation: boolean;
  consent_marketing: boolean;
  scalp_status: string[];
  hair_structure: string;
  hair_thickness: string;
  hair_condition: string[];
  ends_condition: string | null;
  hair_treatments: string;
  heat_frequency: string;
  heat_tools: string[];
  wash_frequency: string;
  styling_effort: string;
  curl_priority: string | null;
  care_goals: string[];
  routine_preference: string;
  time_commitment: string;
};

// -------------------------------------------------------------------
// Ein einzelner Antwortwert kann dreierlei sein:
//  - ein Text        -> Einfachauswahl, Vorname, E-Mail
//  - eine Text-Liste -> Mehrfachauswahl
//  - ein Ja/Nein     -> die Einwilligungs-Checkboxen
// -------------------------------------------------------------------
export type AnswerValue = string | string[] | boolean;

// -------------------------------------------------------------------
// "Answers" sammelt alle bisher gegebenen Antworten – abgelegt unter
// ihrem Feldnamen (z. B. answers["hair_structure"] = "wellig").
// Noch nicht beantwortete Felder fehlen einfach.
// -------------------------------------------------------------------
export type Answers = Record<string, AnswerValue>;

// -------------------------------------------------------------------
// Antwort-Format des n8n-Workflows (via Respond-to-Webhook-Node).
// Nur die Felder, die das Frontend zum Rendern der Ergebnisseite braucht.
// Alle Felder optional, damit graceful degradation möglich ist, falls
// n8n noch kein Response-Node hat oder Antwort-Format fehlerhaft.
// -------------------------------------------------------------------
export type RecommendationProduct = {
  produkt_key?: string;
  produktname_de?: string;
  slot_typ?: string;
  routine_schritt?: number;
  anwendungs_schritt?: number;
  priority?: string;
  hauptfunktion?: string;
  produktlinie?: string;
  anwendung?: string;
};

export type NormalizedAnswers = {
  first_name?: string;
  phone?: string;
  hair_structure?: string;
  hair_thickness?: string;
  hair_condition?: string[];
  scalp_status?: string[];
  hair_treatments?: string;
  heat_frequency?: string;
  wash_frequency?: string;
  care_goals?: string[];
  routine_preference?: string;
  time_commitment?: string;
  styling_effort?: string;
  ends_condition?: string | null;
  curl_priority?: string | null;
};

export type PflegelevelInfo = {
  pflegelevel_final?: string; // "LOW" | "MID" | "HIGH"
  max_products?: number;
};

export type PrioritiesInfo = {
  primary_hair_condition?: string;
  primary_scalp_state?: string;
  hair_condition_cleaned?: string[];
};

export type RecommendationResult = {
  final_routine?: RecommendationProduct[];
  routine_count?: number;
  normalized?: NormalizedAnswers;
  partner_id?: string;
  pflegelevel?: PflegelevelInfo;
  priorities?: PrioritiesInfo;
};
