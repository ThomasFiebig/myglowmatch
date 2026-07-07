"use client";

// =====================================================================
// Questionnaire – das "Gehirn" des Fragebogens.
//
// Führt durch die Schritte, sammelt Antworten, überspringt bedingte
// Fragen, prüft Pflichtfelder und sendet das Ergebnis an n8n.
// Der Frage-Wechsel ist animiert: alte Frage gleitet raus, neue rein –
// in Richtung der Navigation (vorwärts/zurück).
// =====================================================================

import { useState } from "react";
import { AnimatePresence, motion, type Variants } from "framer-motion";
import type { Answers, AnswerValue, Step } from "@/lib/types";
import { formSteps } from "@/data/questions";
import { isStepVisible } from "@/lib/conditional";
import { isStepValid } from "@/lib/validation";
import { buildSubmission } from "@/lib/submission";
import { fade, spring } from "@/lib/animations";
import ProgressBar from "@/components/ProgressBar";
import IntroScreen from "@/components/IntroScreen";
import QuestionScreen from "@/components/QuestionScreen";
import DemoResultScreen from "@/components/DemoResultScreen";
import MotionButton from "@/components/MotionButton";
import Spinner from "@/components/Spinner";
import Logo from "@/components/Logo";

type QuestionnaireProps = {
  partnerId: string;
};

type SubmitState = "idle" | "sending" | "success" | "error";

// Animation für den Frage-Wechsel. direction: 1 = vorwärts, -1 = zurück.
// Neue Frage kommt von einer Seite herein, alte gleitet zur anderen raus.
const questionVariants: Variants = {
  enter: (direction: number) => ({ x: direction * 32, opacity: 0 }),
  center: { x: 0, opacity: 1 },
  exit: (direction: number) => ({
    x: direction * -32,
    opacity: 0,
    transition: { duration: 0.22, ease: "easeIn" },
  }),
};

export default function Questionnaire({ partnerId }: QuestionnaireProps) {
  // State 1: Auf welchem Schritt sind wir? (0 = Intro)
  const [currentIndex, setCurrentIndex] = useState(0);

  // State 2: Alle bisher gegebenen Antworten.
  const [answers, setAnswers] = useState<Answers>({});

  // State 3: Stand des Absende-Vorgangs.
  const [submitState, setSubmitState] = useState<SubmitState>("idle");

  // State 4: Richtung der letzten Navigation (für die Animation).
  const [direction, setDirection] = useState(1);

  const totalSteps = formSteps.length;

  function isVisible(step: Step) {
    return isStepVisible(step, answers);
  }

  function updateAnswer(field: string, value: AnswerValue) {
    setAnswers((previous) => ({ ...previous, [field]: value }));
  }

  // --- Navigation: überspringt unsichtbare (bedingte) Schritte ------
  function goNext() {
    setDirection(1);
    setCurrentIndex((index) => {
      let next = index + 1;
      while (next < totalSteps && !isVisible(formSteps[next])) {
        next += 1;
      }
      return next;
    });
  }
  function goBack() {
    setDirection(-1);
    setCurrentIndex((index) => {
      let prev = index - 1;
      while (prev > 0 && !isVisible(formSteps[prev])) {
        prev -= 1;
      }
      return Math.max(prev, 0);
    });
  }
  // Klick aufs Logo im Header -> zurück zur Hero-Seite (Antworten bleiben).
  function goToIntro() {
    setDirection(-1);
    setCurrentIndex(0);
  }

  // --- Absenden: JSON bauen und an /api/submit schicken -------------
  async function handleSubmit() {
    setSubmitState("sending");
    try {
      const payload = buildSubmission(answers, partnerId);
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
      if (!response.ok) {
        throw new Error("Antwort war nicht ok");
      }
      setSubmitState("success");
    } catch {
      setSubmitState("error");
    }
  }

  // --- Fall A: erfolgreich abgesendet -> Demo-Ergebnisseite ---------
  //  Zeigt Basic-Ansicht + Pro-Ansicht + Beispielmail für die Beraterin,
  //  überlagert mit DEMO-Wasserzeichen.
  if (submitState === "success") {
    const firstName =
      typeof answers.first_name === "string" ? answers.first_name : "";
    return <DemoResultScreen firstName={firstName} />;
  }

  const currentStep = formSteps[currentIndex];

  // --- Fall B: Intro-Bildschirm -------------------------------------
  if (currentStep.type === "intro") {
    return <IntroScreen step={currentStep} onStart={goNext} />;
  }

  // --- Fall C: eine Frage anzeigen ----------------------------------
  const visibleQuestions = formSteps.filter(
    (step, index) => index > 0 && isVisible(step),
  );
  const currentNumber = visibleQuestions.indexOf(currentStep) + 1;
  const isLastStep = currentIndex === totalSteps - 1;
  const stepValid = isStepValid(currentStep, answers);

  let primaryLabel = "Weiter";
  if (isLastStep) {
    if (submitState === "sending") primaryLabel = "Wird gesendet …";
    else if (submitState === "error") primaryLabel = "Erneut senden";
    else if (currentStep.type === "contact")
      primaryLabel = currentStep.submitLabel;
    else primaryLabel = "Abschließen";
  }

  const primaryDisabled = !stepValid || submitState === "sending";

  function handlePrimaryClick() {
    if (isLastStep) {
      void handleSubmit();
    } else {
      goNext();
    }
  }

  return (
    <main data-partner={partnerId} className="flex flex-1 justify-center">
      <div className="flex w-full max-w-md flex-1 flex-col px-6 pt-4 pb-0 md:pb-6">
        {/* Kompakter Header: kleines Logo dicht über der Progress-Bar */}
        <header className="mb-3 flex justify-center">
          <button
            type="button"
            onClick={goToIntro}
            aria-label="Zur Startseite"
            className="block transition-opacity hover:opacity-70"
          >
            <Logo width={90} />
          </button>
        </header>

        {/* Fortschrittsbalken – zählt nur sichtbare Fragen */}
        <ProgressBar current={currentNumber} total={visibleQuestions.length} />

        {/* die aktuelle Frage – animierter Wechsel beim Blättern */}
        <div className="flex-1 py-5">
          <AnimatePresence mode="wait" custom={direction}>
            <motion.div
              key={currentIndex}
              custom={direction}
              variants={questionVariants}
              initial="enter"
              animate="center"
              exit="exit"
              transition={{ x: spring, opacity: fade }}
            >
              <QuestionScreen
                step={currentStep}
                answers={answers}
                updateAnswer={updateAnswer}
              />
            </motion.div>
          </AnimatePresence>
        </div>

        {/* Sticky Nav-Bar auf Mobile, klassisch im Fluss auf Desktop.
            Löst zwei Probleme bei langen Fragen:
            – Mobile-Safari-URL-Bar-Verhalten (erster Tap nicht erfasst,
              weil Scrollen ausgelöst wird).
            – User muss nicht erst scrollen, um den Weiter-Knopf zu
              finden. Die Fehlermeldung sitzt mit drin, damit sie nie
              "vergessen" werden kann, wenn man hochgescrollt hat. */}
        <div className="sticky bottom-0 z-10 -mx-6 bg-[#fbf5ee]/90 px-6 pt-3 pb-4 backdrop-blur-md md:static md:mx-0 md:bg-transparent md:p-0 md:backdrop-blur-none">
          {submitState === "error" && (
            <p className="mb-3 rounded-2xl bg-blush px-4 py-3 text-sm text-rosegold-dark">
              Das Absenden hat leider nicht geklappt. Bitte prüfe deine
              Internetverbindung und versuche es noch einmal.
            </p>
          )}

          <div className="flex gap-3">
            <MotionButton
              onClick={goBack}
              className="rounded-full border border-rosegold px-6 py-3 font-medium text-ink transition-colors hover:bg-blush"
            >
              Zurück
            </MotionButton>
            <MotionButton
              onClick={handlePrimaryClick}
              disabled={primaryDisabled}
              className={`flex flex-1 items-center justify-center gap-2 rounded-full px-6 py-3 font-medium transition-colors ${
                primaryDisabled
                  ? "cursor-not-allowed bg-blush text-ink-soft"
                  : "bg-rosegold text-ink hover:bg-rosegold-dark"
              }`}
            >
              {submitState === "sending" && <Spinner />}
              {primaryLabel}
            </MotionButton>
          </div>
        </div>
      </div>
    </main>
  );
}
