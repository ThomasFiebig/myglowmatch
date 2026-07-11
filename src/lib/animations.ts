// ===================================================================
// mybeautykey – zentrale Animations-Einstellungen
// Alle Animationen im Projekt greifen auf diese Werte zu, damit alles
// einheitlich wirkt. Hier zentral anpassbar.
// ===================================================================

import type { Transition, Variants } from "framer-motion";

// Feder-Animation – sorgt für den federnden "Premium"-Effekt.
// Höhere stiffness = schneller, höhere damping = weniger Nachwippen.
export const spring: Transition = {
  type: "spring",
  stiffness: 300,
  damping: 30,
};

// Sanftes Ein-/Ausblenden: 400 ms, ease-out (am Ende abbremsend).
export const fade: Transition = {
  duration: 0.4,
  ease: "easeOut",
};

// Zeit-Versatz zwischen den Antwort-Karten beim Nacheinander-Erscheinen.
export const staggerStep = 0.06; // 60 ms

// -------------------------------------------------------------------
// Variants = benannte Animations-Zustände.
// Der Container der Antwort-Karten: lässt seine Kinder gestaffelt
// (eines nach dem anderen) erscheinen.
// -------------------------------------------------------------------
export const cardListVariants: Variants = {
  hidden: {},
  visible: {
    transition: { staggerChildren: staggerStep },
  },
};

// Eine einzelne Antwort-Karte: aus 0.95 leicht hochskalieren + einblenden.
export const cardVariants: Variants = {
  hidden: { opacity: 0, scale: 0.96 },
  visible: { opacity: 1, scale: 1, transition: fade },
};
