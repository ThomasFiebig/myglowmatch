// ===================================================================
// mybeautykey – Absende-Daten zusammenbauen (Etappe 8)
// Macht aus dem gesammelten "answers"-Objekt das finale JSON für n8n.
// Format: siehe docs/fragenkatalog.md.
// ===================================================================

import type { Answers, SubmissionData } from "@/lib/types";
import { formSteps } from "@/data/questions";
import { isStepVisible } from "@/lib/conditional";

// --- kleine Helfer: einen Wert sicher im richtigen Typ holen ---------
function getText(answers: Answers, field: string): string {
  const value = answers[field];
  return typeof value === "string" ? value : "";
}
function getList(answers: Answers, field: string): string[] {
  const value = answers[field];
  return Array.isArray(value) ? value : [];
}
function getBool(answers: Answers, field: string): boolean {
  return answers[field] === true;
}

// Ist der bedingte Schritt mit dieser id aktuell sichtbar?
// Wird gebraucht, um übersprungene Fragen als null zu senden.
function isVisibleById(id: string, answers: Answers): boolean {
  const step = formSteps.find((entry) => entry.id === id);
  return step ? isStepVisible(step, answers) : false;
}

// -------------------------------------------------------------------
// Baut das finale JSON, das an den n8n-Webhook geschickt wird.
// -------------------------------------------------------------------
export function buildSubmission(
  answers: Answers,
  partnerId: string,
): SubmissionData {
  // bedingte Fragen: nur den Wert senden, wenn die Frage sichtbar war –
  // sonst null (bzw. leere Liste). So erwartet es der n8n-Code.
  const curlVisible = isVisibleById("curl_priority", answers);
  const endsVisible = isVisibleById("ends_condition", answers);
  const heatToolsVisible = isVisibleById("heat_tools", answers);

  return {
    partner_id: partnerId,
    first_name: getText(answers, "first_name"),
    // E-Mail nur mitschicken, wenn die Kundin aktiv „Analyse per Mail"
    // angeklickt hat. Sonst leer (n8n-Send-Node an die Kundin ist
    // ohnehin deaktiviert, siehe n8n-UI).
    email: getBool(answers, "wants_email_copy") ? getText(answers, "email") : "",
    phone: getText(answers, "phone"),
    consent_recommendation: getBool(answers, "consent_recommendation"),
    // Marketing-Checkbox entfällt — konstant false, damit das n8n-Schema
    // unverändert bleibt.
    consent_marketing: false,
    scalp_status: getList(answers, "scalp_status"),
    hair_structure: getText(answers, "hair_structure"),
    hair_thickness: getText(answers, "hair_thickness"),
    hair_condition: getList(answers, "hair_condition"),
    ends_condition: endsVisible
      ? getText(answers, "ends_condition") || null
      : null,
    hair_treatments: getText(answers, "hair_treatments"),
    heat_frequency: getText(answers, "heat_frequency"),
    heat_tools: heatToolsVisible ? getList(answers, "heat_tools") : [],
    wash_frequency: getText(answers, "wash_frequency"),
    styling_effort: getText(answers, "styling_effort"),
    curl_priority: curlVisible
      ? getText(answers, "curl_priority") || null
      : null,
    care_goals: getList(answers, "care_goals"),
    routine_preference: getText(answers, "routine_preference"),
    time_commitment: getText(answers, "time_commitment"),
  };
}
