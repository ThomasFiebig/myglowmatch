"use client";

// =====================================================================
// ProgressBar – der Fortschrittsbalken oben im Fragebogen.
// Der gefüllte Teil gleitet jetzt flüssig (ease-out) auf den neuen Wert.
// =====================================================================

import { motion } from "framer-motion";

type ProgressBarProps = {
  current: number; // aktuelle Frage, z. B. 3
  total: number; // Gesamtzahl der Fragen, z. B. 16
};

export default function ProgressBar({ current, total }: ProgressBarProps) {
  const percent = Math.round((current / total) * 100);

  return (
    <div>
      {/* Beschriftung über dem Balken */}
      <div className="flex justify-between text-xs font-medium text-ink-soft">
        <span>
          Frage {current} von {total}
        </span>
        <span>{percent}%</span>
      </div>

      {/* Der Balken: heller Hintergrund + gefüllter Teil */}
      <div className="mt-2 h-2 w-full overflow-hidden rounded-full bg-blush">
        <motion.div
          className="h-full rounded-full bg-rosegold"
          initial={false}
          animate={{ width: `${percent}%` }}
          transition={{ duration: 0.6, ease: "easeOut" }}
        />
      </div>
    </div>
  );
}
