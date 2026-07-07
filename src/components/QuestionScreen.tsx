// =====================================================================
// QuestionScreen – zeigt EINE Frage: den Fragetext + das passende
// Eingabe-Feld. Anhand von step.type wird entschieden, welches der
// vier Eingabe-Felder angezeigt wird (wie eine Weiche).
// =====================================================================

import type { Answers, AnswerValue, QuestionStep } from "@/lib/types";
import SingleChoice from "@/components/SingleChoice";
import MultiChoice from "@/components/MultiChoice";
import ContactFields from "@/components/ContactFields";

type QuestionScreenProps = {
  step: QuestionStep;
  answers: Answers;
  updateAnswer: (field: string, value: AnswerValue) => void;
};

export default function QuestionScreen({
  step,
  answers,
  updateAnswer,
}: QuestionScreenProps) {
  // Je nach Frage-Typ das passende Eingabe-Feld vorbereiten.
  let input;

  if (step.type === "single") {
    const value = answers[step.field];
    input = (
      <SingleChoice
        options={step.options}
        // Wert nur übernehmen, wenn es wirklich ein Text ist, sonst ""
        selected={typeof value === "string" ? value : ""}
        onSelect={(newValue) => updateAnswer(step.field, newValue)}
      />
    );
  } else if (step.type === "multi") {
    const value = answers[step.field];
    input = (
      <MultiChoice
        options={step.options}
        // Wert nur übernehmen, wenn es wirklich eine Liste ist, sonst []
        selected={Array.isArray(value) ? value : []}
        maxSelect={step.maxSelect}
        onChange={(newValues) => updateAnswer(step.field, newValues)}
      />
    );
  } else {
    // step.type === "contact" (letzter Schritt: Vorname, Telefon,
    // optional E-Mail-Kopie, Consent)
    input = (
      <ContactFields
        firstNameLabel={step.firstNameLabel}
        phoneLabel={step.phoneLabel}
        phoneDescription={step.phoneDescription}
        phonePlaceholder={step.phonePlaceholder}
        emailOptInLabel={step.emailOptInLabel}
        emailPlaceholder={step.emailPlaceholder}
        consentText={step.consentText}
        firstName={
          typeof answers.first_name === "string" ? answers.first_name : ""
        }
        phone={typeof answers.phone === "string" ? answers.phone : ""}
        email={typeof answers.email === "string" ? answers.email : ""}
        wantsEmailCopy={answers.wants_email_copy === true}
        consent={answers.consent_recommendation === true}
        onChange={updateAnswer}
      />
    );
  }

  return (
    <div className="w-full">
      <h2 className="font-serif text-2xl font-semibold leading-snug text-ink">
        {step.title}
      </h2>
      <div className="mt-6">{input}</div>
    </div>
  );
}
