"use client";

// =====================================================================
// SingleChoice – Einfachauswahl: genau eine Option ist wählbar.
// Dezenter Premium-Look: ausgewählte Karte bleibt weiß mit Rosé-Rand
// und einem Häkchen rechts (nicht rosa-flächig).
// =====================================================================

import { motion } from "framer-motion";
import type { Option } from "@/lib/types";
import { cardListVariants, cardVariants, spring } from "@/lib/animations";

type SingleChoiceProps = {
  options: Option[];
  selected: string;
  onSelect: (value: string) => void;
};

export default function SingleChoice({
  options,
  selected,
  onSelect,
}: SingleChoiceProps) {
  return (
    <motion.div
      className="flex flex-col gap-3"
      variants={cardListVariants}
      initial="hidden"
      animate="visible"
    >
      {options.map((option) => {
        const isSelected = option.value === selected;

        return (
          <motion.button
            key={option.value}
            type="button"
            variants={cardVariants}
            whileHover={{ y: -2 }}
            whileTap={{ scale: 0.97 }}
            transition={spring}
            onClick={() => onSelect(option.value)}
            className={`flex w-full items-center gap-3 rounded-2xl border px-5 py-4 text-left transition-[background-color,border-color,box-shadow] duration-300 ${
              isSelected
                ? "border-rose-line bg-white ring-1 ring-rose-line shadow-[0_6px_18px_-6px_rgba(212,165,147,0.5)]"
                : "border-card-line bg-[linear-gradient(to_bottom,#ffffff,#fefbf8)] shadow-sm hover:border-rose-line/40 hover:shadow-md"
            }`}
          >
            {/* runder Radio-Indikator links – bei Auswahl rosé gefüllt */}
            <span
              className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-full border-2 ${
                isSelected ? "border-rose-line" : "border-ink-soft"
              }`}
            >
              {isSelected && (
                <span className="h-2.5 w-2.5 rounded-full bg-rose-line" />
              )}
            </span>

            {/* Label */}
            <span className="flex-1 text-ink">{option.label}</span>

            {/* Häkchen rechts – erscheint bei Auswahl */}
            {isSelected && (
              <svg
                className="h-5 w-5 shrink-0 text-rose-line"
                viewBox="0 0 20 20"
                fill="none"
                stroke="currentColor"
                strokeWidth="2.5"
                strokeLinecap="round"
                strokeLinejoin="round"
                aria-hidden="true"
              >
                <path d="M4 10.5l4 4 8-9" />
              </svg>
            )}
          </motion.button>
        );
      })}
    </motion.div>
  );
}
