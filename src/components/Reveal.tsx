"use client";

// =====================================================================
// Reveal + FloatBlob – Landingpage-Animationsbausteine.
// - Reveal: sanftes Ein-Blenden mit leichtem Hochsteigen, sobald das
//   Element in den Viewport kommt. Nutzt whileInView (einmalig).
// - FloatBlob: dezente, endlos schwebende Farbwolke im Hintergrund –
//   für die "atmende" Anmutung ohne aufdringliche Bewegung.
// =====================================================================

import { motion } from "framer-motion";
import type { ReactNode } from "react";

type RevealProps = {
  children: ReactNode;
  /** Verzögerung in Sekunden – für Stagger in Grids. */
  delay?: number;
  /** Hochstieg-Weite in Pixel. Default 24. */
  y?: number;
  /** Horizontale Start-Position in Pixel. Positiv = kommt von rechts,
   *  negativ = von links. Nützlich für "auseinander fahren" Effekte,
   *  bei denen Elemente aus der Mitte an ihre Zielpositionen driften. */
  x?: number;
  className?: string;
};

export default function Reveal({
  children,
  delay = 0,
  y = 24,
  x = 0,
  className,
}: RevealProps) {
  return (
    <motion.div
      className={className}
      initial={{ opacity: 0, y, x }}
      whileInView={{ opacity: 1, y: 0, x: 0 }}
      viewport={{ once: true, margin: "-80px" }}
      transition={{
        duration: 0.7,
        delay,
        ease: [0.22, 1, 0.36, 1], // sanftes ease-out mit weichem Auslauf
      }}
    >
      {children}
    </motion.div>
  );
}

type FloatBlobProps = {
  className?: string;
  /** Dauer eines Atemzugs in Sekunden. Default 14. */
  duration?: number;
  /** Startverzögerung – damit mehrere Blobs versetzt schweben. */
  delay?: number;
  /** Horizontale Drift in Pixel. Default 16. */
  xDrift?: number;
  /** Vertikale Drift in Pixel. Default 22. */
  yDrift?: number;
};

export function FloatBlob({
  className = "",
  duration = 14,
  delay = 0,
  xDrift = 16,
  yDrift = 22,
}: FloatBlobProps) {
  return (
    <motion.div
      aria-hidden="true"
      className={`pointer-events-none absolute rounded-full blur-3xl ${className}`}
      animate={{
        x: [0, xDrift, 0, -xDrift * 0.6, 0],
        y: [0, -yDrift, 0, yDrift * 0.5, 0],
        scale: [1, 1.05, 1, 0.98, 1],
      }}
      transition={{
        duration,
        delay,
        ease: "easeInOut",
        repeat: Infinity,
      }}
    />
  );
}
