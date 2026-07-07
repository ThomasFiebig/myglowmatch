// ===================================================================
// myglowmatch – Validierung
// Beantwortet: "Ist die aktuelle Frage gültig beantwortet?"
// ===================================================================

import type { Answers, QuestionStep } from "@/lib/types";

// -------------------------------------------------------------------
// Lockere Telefon-Prüfung: erlaubt Ziffern, +, Leerzeichen, Bindestriche.
// Leere Eingabe gilt als gültig (Pflichtfeld = NEIN).
// -------------------------------------------------------------------
export function isValidPhone(value: string): boolean {
  const trimmed = value.trim();
  if (trimmed === "") return true;
  return /^[\d+\s-]+$/.test(trimmed);
}

// -------------------------------------------------------------------
// Prüft, ob ein Frage-Schritt gültig beantwortet ist.
// Gibt true zurück, wenn man "Weiter" klicken darf.
// -------------------------------------------------------------------
export function isStepValid(step: QuestionStep, answers: Answers): boolean {
  // --- Einfachauswahl: ein nicht-leerer Wert muss gewählt sein ------
  if (step.type === "single") {
    const answer = answers[step.field];
    return typeof answer === "string" && answer !== "";
  }

  // --- Mehrfachauswahl: Anzahl muss zwischen min und max liegen -----
  if (step.type === "multi") {
    const answer = answers[step.field];
    const list = Array.isArray(answer) ? answer : [];
    return list.length >= step.minSelect && list.length <= step.maxSelect;
  }

  // --- Kontakt + Einwilligung (letzter Schritt) ---------------------
  //  Vorname nicht leer, Telefon optional (leer = ok; ungültige Zeichen
  //  sperren Absenden), Pflicht-Checkbox angehakt.
  const firstName = answers.first_name;
  const phone = answers.phone;
  const firstNameOk = typeof firstName === "string" && firstName.trim() !== "";
  const phoneOk = typeof phone !== "string" || isValidPhone(phone);
  const consentOk = answers.consent_recommendation === true;
  return firstNameOk && phoneOk && consentOk;
}
