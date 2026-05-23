// ===================================================================
// myglowmatch – Validierung (Etappe 7)
// Beantwortet: "Ist die aktuelle Frage gültig beantwortet?"
// Die Regeln stammen aus docs/fragenkatalog.md.
// ===================================================================

import type { Answers, QuestionStep } from "@/lib/types";

// -------------------------------------------------------------------
// Einfache E-Mail-Prüfung: etwas@etwas.endung
//  [^\s@]+  = ein oder mehr Zeichen, die kein Leerzeichen / kein @ sind
// -------------------------------------------------------------------
export function isValidEmail(value: string): boolean {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

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

  // --- Kontaktdaten: Vorname nicht leer, E-Mail gültig,
  //     Telefon optional (leer = ok; ungültige Zeichen sperren Weiter)
  if (step.type === "contact") {
    const firstName = answers.first_name;
    const email = answers.email;
    const phone = answers.phone;
    const firstNameOk =
      typeof firstName === "string" && firstName.trim() !== "";
    const emailOk = typeof email === "string" && isValidEmail(email);
    const phoneOk = typeof phone !== "string" || isValidPhone(phone);
    return firstNameOk && emailOk && phoneOk;
  }

  // --- Einwilligung: die Pflicht-Checkbox muss angehakt sein --------
  // (consent_marketing ist optional und wird nicht geprüft)
  return answers.consent_recommendation === true;
}
