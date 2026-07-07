// ===================================================================
// myglowmatch – Validierung
// Beantwortet: "Ist die aktuelle Frage gültig beantwortet?"
// ===================================================================

import type { Answers, QuestionStep } from "@/lib/types";

// -------------------------------------------------------------------
// Einfache E-Mail-Prüfung: etwas@etwas.endung
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
// -------------------------------------------------------------------
export function isStepValid(step: QuestionStep, answers: Answers): boolean {
  if (step.type === "single") {
    const answer = answers[step.field];
    return typeof answer === "string" && answer !== "";
  }

  if (step.type === "multi") {
    const answer = answers[step.field];
    const list = Array.isArray(answer) ? answer : [];
    return list.length >= step.minSelect && list.length <= step.maxSelect;
  }

  // Kontakt + Einwilligung (letzter Schritt):
  //  Vorname Pflicht, Telefon optional (leer = ok; falsche Zeichen sperren),
  //  E-Mail Pflicht wenn Opt-in aktiv, Consent-Checkbox angehakt.
  const firstName = answers.first_name;
  const phone = answers.phone;
  const email = answers.email;
  const firstNameOk = typeof firstName === "string" && firstName.trim() !== "";
  const phoneOk = typeof phone !== "string" || isValidPhone(phone);
  const consentOk = answers.consent_recommendation === true;
  const wantsEmail = answers.wants_email_copy === true;
  const emailOk =
    !wantsEmail || (typeof email === "string" && isValidEmail(email));
  return firstNameOk && phoneOk && emailOk && consentOk;
}
