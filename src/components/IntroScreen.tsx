"use client";

// =====================================================================
// IntroScreen – die Hero-/Willkommensseite vor Frage 1.
// Beim ersten Laden erscheinen die Elemente gestaffelt nacheinander
// (Bild -> Headline -> Subline -> Icons -> Button -> Hinweis) – das
// gibt den "wow"-Moment beim Aufruf.
// =====================================================================

import Image from "next/image";
import { motion, type Variants } from "framer-motion";
import type { IntroStep } from "@/lib/types";
import { fade } from "@/lib/animations";
import MotionButton from "@/components/MotionButton";
import Logo from "@/components/Logo";
import SiteFooter from "@/components/SiteFooter";

type IntroScreenProps = {
  step: IntroStep;
  onStart: () => void;
};

// Drei kleine Icons – passend zu den drei Mini-Punkten (gleiche Reihenfolge).
const heroIcons = [
  // Uhr – "Schnell beantwortet"
  <svg
    key="clock"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="h-4 w-4"
  >
    <circle cx="12" cy="12" r="9" />
    <path d="M12 7v5l3.5 2" />
  </svg>,
  // Funkeln – "Persönliche Empfehlung"
  <svg
    key="sparkle"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="h-4 w-4"
  >
    <path d="M12 3l2.2 6.8L21 12l-6.8 2.2L12 21l-2.2-6.8L3 12l6.8-2.2z" />
  </svg>,
  // Auge – "Ergebnis sofort sichtbar"
  <svg
    key="eye"
    viewBox="0 0 24 24"
    fill="none"
    stroke="currentColor"
    strokeWidth="2"
    strokeLinecap="round"
    strokeLinejoin="round"
    className="h-4 w-4"
  >
    <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z" />
    <circle cx="12" cy="12" r="3" />
  </svg>,
];

// Sanfter Fade-Mask für das Hero-Bild: oben ganz leicht, unten kräftig.
// Dadurch geht das Bild weich in den Hintergrund über, statt einen
// harten Rahmen zu zeigen.
const heroFadeMask =
  "linear-gradient(to bottom, transparent 0%, black 6%, black 65%, transparent 100%)";

// --- Stagger-Variants für den Hero-Auftritt --------------------------
// Äußerer Container: staffelt Bild -> Inhaltsblock.
const heroOuter: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.12 } },
};
// Inhaltsblock: staffelt seine Kinder (Headline, Subline, Icons, ...).
const heroContent: Variants = {
  hidden: {},
  visible: { transition: { staggerChildren: 0.1 } },
};
// Das Bild blendet nur sanft ein.
const heroImage: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: fade },
};
// Text-Elemente: einblenden und leicht aufsteigen.
const heroItem: Variants = {
  hidden: { opacity: 0, y: 14 },
  visible: { opacity: 1, y: 0, transition: fade },
};

export default function IntroScreen({ step, onStart }: IntroScreenProps) {
  return (
    <main className="flex flex-1 flex-col items-center">
      <motion.div
        className="flex w-full max-w-md flex-col md:max-w-3xl"
        variants={heroOuter}
        initial="hidden"
        animate="visible"
      >
        {/* Logo ganz oben – dezent, leitet den Auftritt ein */}
        <motion.div
          variants={heroItem}
          className="flex justify-center pt-5 pb-2"
        >
          <Logo width={200} />
        </motion.div>

        {/* Hero-Bild – priority (kein lazy), da erstes sichtbares Element.
            Atmosphärischer Look: kein Rahmen, kein Schatten – stattdessen
            ein weicher Fade unten (und ganz leicht oben) per mask-image,
            damit das Bild sanft in den Champagne-Hintergrund übergeht.
            Die Headline darunter wird so der visuelle Anker. */}
        <motion.div
          variants={heroImage}
          className="relative h-60 w-full sm:h-72 md:h-auto md:aspect-video"
          style={{
            maskImage: heroFadeMask,
            WebkitMaskImage: heroFadeMask,
          }}
        >
          <Image
            src={step.imageSrc}
            alt={step.imageAlt}
            fill
            priority
            sizes="(max-width: 448px) 100vw, (max-width: 768px) 448px, 768px"
            className="object-cover"
          />
        </motion.div>

        {/* Inhalt – staffelt seine eigenen Kinder */}
        <motion.div
          variants={heroContent}
          className="px-6 pb-12 pt-3 text-center"
        >
          <motion.h1
            variants={heroItem}
            className="font-serif text-3xl font-semibold leading-tight text-ink"
          >
            {step.headline}
          </motion.h1>

          <motion.p variants={heroItem} className="mt-3 text-ink-soft">
            {step.subHeadline}
          </motion.p>

          {/* drei Mini-Punkte mit Icons */}
          <motion.ul
            variants={heroItem}
            className="mx-auto mt-10 flex max-w-xs flex-col gap-3 text-left"
          >
            {step.points.map((point, index) => (
              <li key={point} className="flex items-center gap-3">
                <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-rosegold/20 text-rosegold-dark">
                  {heroIcons[index]}
                </span>
                <span className="text-ink">{point}</span>
              </li>
            ))}
          </motion.ul>

          <motion.div
            variants={heroItem}
            className="mt-8 md:mx-auto md:max-w-sm"
          >
            <MotionButton
              onClick={onStart}
              className="w-full rounded-full bg-rosegold px-6 py-4 font-medium text-ink transition-colors hover:bg-rosegold-dark"
            >
              {step.ctaLabel}
            </MotionButton>
          </motion.div>

          <motion.p
            variants={heroItem}
            className="mt-4 text-xs text-ink-soft"
          >
            {step.privacyNote}
          </motion.p>

          {/* Footer mit Impressum & Datenschutz */}
          <motion.div variants={heroItem} className="mt-10">
            <SiteFooter />
          </motion.div>
        </motion.div>
      </motion.div>
    </main>
  );
}
