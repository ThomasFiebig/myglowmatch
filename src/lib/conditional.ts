// ===================================================================
// mybeautykey – Conditional Logic (Etappe 6)
// Hier wird ausgewertet, OB ein Schritt angezeigt werden soll.
// Die Bedingungen selbst stehen als Daten in src/data/questions.ts.
// ===================================================================

import type { Answers, Condition, Step } from "@/lib/types";

// -------------------------------------------------------------------
// Prüft EINE Bedingung anhand der bisher gegebenen Antworten.
// Gibt true zurück, wenn die Bedingung erfüllt ist.
// -------------------------------------------------------------------
export function isConditionMet(
  condition: Condition,
  answers: Answers,
): boolean {
  // Die bisherige Antwort auf das geprüfte Feld holen.
  const answer = answers[condition.field];

  switch (condition.operator) {
    // Antwort ist GENAU dieser Wert
    case "equals":
      return answer === condition.value;

    // Antwort ist NICHT dieser Wert
    // (gilt auch als erfüllt, solange noch nichts geantwortet wurde)
    case "notEquals":
      return answer !== condition.value;

    // Antwort (ein Einzelwert) ist einer der Werte aus der Liste
    case "in":
      if (typeof answer !== "string" || !Array.isArray(condition.value)) {
        return false;
      }
      return condition.value.includes(answer);

    // Antwort (eine Mehrfach-Liste) enthält mindestens einen der Werte
    case "includesAny":
      if (!Array.isArray(answer) || !Array.isArray(condition.value)) {
        return false;
      }
      return answer.some((entry) => condition.value.includes(entry));

    default:
      return false;
  }
}

// -------------------------------------------------------------------
// Prüft, ob ein Schritt aktuell sichtbar ist.
//  - ohne "conditional"-Feld -> immer sichtbar
//  - mit "conditional"-Feld  -> nur sichtbar, wenn die Bedingung passt
// -------------------------------------------------------------------
export function isStepVisible(step: Step, answers: Answers): boolean {
  if (!step.conditional) {
    return true;
  }
  return isConditionMet(step.conditional, answers);
}
