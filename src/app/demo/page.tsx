"use client";

// /demo – kompakter 3-Screen-Walkthrough für Marketing-Zwecke.
// Bewusst kein bedienbarer Fragebogen — Antworten sind vorausgefüllt,
// damit klar unterschieden bleibt: /demo = Preview, /[partner] = echte
// Beratung mit Tarif-Zählung. Vermeidet, dass der Free-Tarif (2 Analysen
// pro Monat) durch die öffentliche Demo entwertet wird.

import { useState } from "react";
import Link from "next/link";
import { AnimatePresence, motion } from "framer-motion";
import Logo from "@/components/Logo";
import SiteFooter from "@/components/SiteFooter";
import Reveal, { FloatBlob } from "@/components/Reveal";

const btnPrimary =
  "inline-flex items-center justify-center rounded-full bg-rosegold px-8 py-4 font-medium text-ink shadow-[0_10px_30px_-12px_rgba(224,177,168,0.55)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-rosegold-dark hover:shadow-[0_16px_40px_-14px_rgba(201,143,132,0.7)]";
const btnGhost =
  "inline-flex items-center justify-center rounded-full border border-ink/15 bg-white/70 px-6 py-3 font-medium text-ink backdrop-blur transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white hover:shadow-[0_12px_30px_-14px_rgba(50,46,45,0.25)]";

// Beispiel-Antworten der Beispiel-Kundin – bewusst konsistent gewählt
// (trocken + Frizz + glanzlos passt zu Feuchtigkeit + Glanz als Ziel).
const exampleQuestions = [
  {
    label: "Frage 1 · Einfachauswahl",
    title: "Was ist deine natürliche Haarstruktur?",
    options: ["glatt", "wellig", "lockig", "sehr lockig / kraus"],
    selected: ["wellig"],
  },
  {
    label: "Frage 2 · bis zu 3 Antworten",
    title: "Welche Punkte treffen aktuell auf dein Haar zu?",
    options: [
      "stark geschädigt",
      "Haarbruch",
      "Spliss",
      "trocken",
      "Frizz",
      "glanzlos",
      "kraftlos",
      "dünner werdendes Haar",
    ],
    selected: ["trocken", "Frizz", "glanzlos"],
  },
  {
    label: "Frage 3 · bis zu 2 Antworten",
    title: "Was ist dir bei deiner Haarpflege aktuell am wichtigsten?",
    options: [
      "Reparatur",
      "mehr Feuchtigkeit",
      "weniger Frizz",
      "mehr Glanz",
      "mehr Volumen",
      "gesunde Kopfhaut",
      "volleres Haar",
    ],
    selected: ["mehr Feuchtigkeit", "mehr Glanz"],
  },
];

const detectedNeeds = [
  {
    title: "Feuchtigkeit",
    reason: `„trocken" markiert + „mehr Feuchtigkeit" als Ziel — Haarfaser braucht Feuchtigkeitszufuhr.`,
    icon: (
      <path d="M12 3s-6 7-6 11a6 6 0 0 0 12 0c0-4-6-11-6-11z" />
    ),
  },
  {
    title: "Frizz-Kontrolle",
    reason: `„Frizz" markiert — Haarstruktur wellig, offene Schuppenschicht braucht Glättung.`,
    icon: (
      <path d="M4 8c2-2 4 2 6 0s4 2 6 0 4 2 6 0M4 14c2-2 4 2 6 0s4 2 6 0 4 2 6 0" />
    ),
  },
  {
    title: "Glanz",
    reason: `„glanzlos" markiert + „mehr Glanz" als Ziel — Oberfläche versiegeln, Licht reflektieren.`,
    icon: (
      <path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2z" />
    ),
  },
];

const recommendations = [
  {
    kind: "Shampoo",
    name: "Feuchtigkeits-Shampoo",
    why: "Reinigt mild, ohne die Kopfhaut auszutrocknen. Bringt Feuchtigkeit direkt beim Waschen ins Haar.",
  },
  {
    kind: "Leave-in",
    name: "Leave-in-Pflege mit Hitzeschutz",
    why: "Legt sich um die Haarfaser, reduziert Frizz spürbar und schützt beim Styling bis 220 °C.",
  },
  {
    kind: "Finish",
    name: "Glanz-Serum",
    why: "Ein bis zwei Tropfen in die Längen — versiegelt die Oberfläche, das Haar reflektiert Licht sichtbar mehr.",
  },
];

function DemoNav() {
  return (
    <header className="relative z-10 mx-auto flex w-full max-w-6xl items-center justify-between px-6 pt-5 pb-2">
      <Link href="/" aria-label="Zur Startseite" className="block transition-opacity hover:opacity-70">
        <Logo width={120} />
      </Link>
      <nav className="flex items-center gap-3 text-sm">
        <Link
          href="/login"
          className="rounded-full border border-ink/15 bg-white/60 px-4 py-2 text-ink transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white"
        >
          Jetzt starten
        </Link>
      </nav>
    </header>
  );
}

function ProgressDots({ step, total }: { step: number; total: number }) {
  return (
    <div className="flex justify-center gap-2 py-6">
      {Array.from({ length: total }).map((_, i) => (
        <span
          key={i}
          className={`h-1.5 rounded-full transition-all duration-500 ${
            i + 1 === step
              ? "w-10 bg-rosegold-dark"
              : i + 1 < step
                ? "w-6 bg-rosegold/60"
                : "w-6 bg-ink/10"
          }`}
        />
      ))}
    </div>
  );
}

const stepMotion = {
  initial: { opacity: 0, y: 20 },
  animate: { opacity: 1, y: 0 },
  exit: { opacity: 0, y: -20 },
  transition: { duration: 0.4, ease: [0.22, 1, 0.36, 1] as const },
};

// ---------------------------------------------------------------------
// Screen 1: Fragebogen-Vorschau mit den 3 Beispielfragen + Antworten
// ---------------------------------------------------------------------
function StepQuestions() {
  return (
    <motion.div key="questions" {...stepMotion}>
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-3 text-sm font-medium tracking-widest text-rosegold-dark uppercase">
          Schritt 1 von 3
        </p>
        <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
          So beantwortet deine Kundin die Fragen
        </h2>
        <p className="mt-4 text-ink-soft">
          Der echte Fragebogen hat 16 Fragen. Hier drei Beispiele — mit den
          Antworten unserer Beispiel-Kundin.
        </p>
      </div>

      <div className="mt-10 space-y-5">
        {exampleQuestions.map((q) => (
          <div
            key={q.title}
            className="rounded-2xl border border-ink/5 bg-white/70 p-6 md:p-7"
          >
            <p className="mb-1 text-xs font-medium tracking-widest text-rosegold-dark uppercase">
              {q.label}
            </p>
            <p className="font-serif text-lg text-ink md:text-xl">{q.title}</p>
            <div className="mt-4 flex flex-wrap gap-2">
              {q.options.map((opt) => {
                const isSelected = q.selected.includes(opt);
                return (
                  <span
                    key={opt}
                    className={`rounded-full border px-3 py-1.5 text-sm transition-colors ${
                      isSelected
                        ? "border-rosegold-dark bg-rosegold/25 font-medium text-ink"
                        : "border-ink/10 bg-white/40 text-ink-soft"
                    }`}
                  >
                    {isSelected && "✓ "}
                    {opt}
                  </span>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------
// Screen 2: Bedarfsanalyse — abgeleitete Bedarfe mit Begründung
// ---------------------------------------------------------------------
function StepAnalysis() {
  return (
    <motion.div key="analysis" {...stepMotion}>
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-3 text-sm font-medium tracking-widest text-rosegold-dark uppercase">
          Schritt 2 von 3
        </p>
        <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
          Diese Bedarfe wurden erkannt
        </h2>
        <p className="mt-4 text-ink-soft">
          Das System übersetzt die Antworten in konkrete Pflege-Bedarfe —
          mit einer Begründung, die die Kundin nachvollziehen kann.
        </p>
      </div>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {detectedNeeds.map((n) => (
          <div
            key={n.title}
            className="rounded-2xl border border-ink/5 bg-white/70 p-6"
          >
            <div className="flex h-12 w-12 items-center justify-center rounded-full bg-rosegold/20 text-rosegold-dark">
              <svg
                viewBox="0 0 24 24"
                className="h-6 w-6"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              >
                {n.icon}
              </svg>
            </div>
            <h3 className="mt-4 font-serif text-xl text-ink">{n.title}</h3>
            <p className="mt-2 text-sm text-ink-soft">{n.reason}</p>
          </div>
        ))}
      </div>
    </motion.div>
  );
}

// ---------------------------------------------------------------------
// Screen 3: Empfehlung — 3 markenneutrale Beispielprodukte
// ---------------------------------------------------------------------
function StepRecommendation() {
  return (
    <motion.div key="recommendation" {...stepMotion}>
      <div className="mx-auto max-w-2xl text-center">
        <p className="mb-3 text-sm font-medium tracking-widest text-rosegold-dark uppercase">
          Schritt 3 von 3
        </p>
        <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
          Diese Produkte passen dazu
        </h2>
        <p className="mt-4 text-ink-soft">
          Im Pro-Tarif kommen hier deine eigenen Produkte rein — mit deiner
          Begründung, deinem Ton. In dieser Demo zeigen wir neutrale
          Beispiele.
        </p>
      </div>

      <div className="mt-10 grid gap-5 md:grid-cols-3">
        {recommendations.map((r, i) => (
          <div
            key={r.name}
            className="relative overflow-hidden rounded-2xl border border-ink/5 bg-white/70 p-6 pt-8"
          >
            <span
              aria-hidden="true"
              className="pointer-events-none absolute -top-2 -right-2 select-none font-serif text-[6rem] leading-none text-rosegold/15"
            >
              {String(i + 1).padStart(2, "0")}
            </span>
            <div className="relative">
              <p className="text-xs font-medium tracking-widest text-rosegold-dark uppercase">
                {r.kind}
              </p>
              <h3 className="mt-1 font-serif text-xl text-ink">{r.name}</h3>
              <p className="mt-3 text-sm text-ink-soft">{r.why}</p>
            </div>
          </div>
        ))}
      </div>

      <Reveal delay={0.2}>
        <div className="mt-12 rounded-3xl bg-rosegold/20 p-8 text-center md:p-12">
          <h3 className="font-serif text-2xl text-ink sm:text-3xl">
            So sieht das für deine Kundin aus.
          </h3>
          <p className="mx-auto mt-3 max-w-xl text-ink-soft">
            Deine echte Beratung nutzt deine Produkte, deinen Ton — und deinen
            persönlichen Beratungs-Link. Der Free-Tarif erlaubt dir zwei echte
            Beratungen pro Monat.
          </p>
          <div className="mt-6 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link href="/login" className={`${btnPrimary} w-full sm:w-auto`}>
              Jetzt kostenlos starten
            </Link>
            <Link href="/" className={`${btnGhost} w-full sm:w-auto`}>
              Zurück zur Übersicht
            </Link>
          </div>
        </div>
      </Reveal>
    </motion.div>
  );
}

export default function DemoPage() {
  const total = 3;
  const [step, setStep] = useState(1);

  return (
    <main className="flex flex-1 flex-col overflow-hidden">
      <DemoNav />

      {/* Dezente Farbwolken im Hintergrund für Konsistenz zum Rest */}
      <div className="pointer-events-none absolute inset-0 -z-0 overflow-hidden">
        <FloatBlob
          className="left-[-6rem] top-16 h-64 w-64 bg-rosegold/20 sm:h-[20rem] sm:w-[20rem]"
          duration={22}
        />
        <FloatBlob
          className="right-[-4rem] bottom-24 h-64 w-64 bg-blush/40 sm:h-[22rem] sm:w-[22rem]"
          duration={26}
          delay={2}
        />
      </div>

      <section className="relative mx-auto w-full max-w-4xl flex-1 px-6 pb-16">
        <ProgressDots step={step} total={total} />

        <AnimatePresence mode="wait">
          {step === 1 && <StepQuestions />}
          {step === 2 && <StepAnalysis />}
          {step === 3 && <StepRecommendation />}
        </AnimatePresence>

        {/* Navigation zwischen den Schritten. Auf dem letzten Schritt gibt
            es keinen "Weiter"-Button mehr — der CTA im Screen selbst führt
            weiter. */}
        {step < total && (
          <div className="mt-12 flex items-center justify-between">
            {step > 1 ? (
              <button
                onClick={() => setStep((s) => s - 1)}
                className="text-sm text-ink-soft transition-colors hover:text-ink"
              >
                ← Zurück
              </button>
            ) : (
              <span />
            )}
            <button
              onClick={() => setStep((s) => s + 1)}
              className={btnPrimary}
            >
              Weiter →
            </button>
          </div>
        )}
        {step === total && (
          <div className="mt-8 text-center">
            <button
              onClick={() => setStep(1)}
              className="text-sm text-ink-soft transition-colors hover:text-ink"
            >
              ← Demo nochmal ansehen
            </button>
          </div>
        )}
      </section>

      <footer className="px-6 pb-10 pt-6">
        <SiteFooter />
      </footer>
    </main>
  );
}
