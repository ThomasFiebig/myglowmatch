"use client";

// =====================================================================
// MultiChoice – Mehrfachauswahl: mehrere Optionen wählbar, bis maxSelect.
//
// Unterstützt "exklusive" Optionen (option.exclusiveOption === true):
// Eine exklusive Option und die übrigen Optionen schließen sich
// gegenseitig aus – die jeweils andere Seite wird gesperrt.
//
// Dezenter Premium-Look: ausgewählte Karte bleibt weiß mit Rosé-Rand
// und Häkchen rechts; gesperrte Karten hellgrau mit abgedunkeltem Text.
// =====================================================================

import { motion } from "framer-motion";
import type { Option } from "@/lib/types";
import { cardListVariants, cardVariants, spring } from "@/lib/animations";

type MultiChoiceProps = {
  options: Option[];
  selected: string[];
  maxSelect: number;
  onChange: (values: string[]) => void;
};

export default function MultiChoice({
  options,
  selected,
  maxSelect,
  onChange,
}: MultiChoiceProps) {
  const limitReached = selected.length >= maxSelect;

  const exclusiveSelected = options.some(
    (option) => option.exclusiveOption && selected.includes(option.value),
  );
  const normalSelected = options.some(
    (option) => !option.exclusiveOption && selected.includes(option.value),
  );

  function toggle(option: Option) {
    const isSelected = selected.includes(option.value);

    // Exklusive Option: anwählen = NUR sie; abwählen = leere Auswahl.
    if (option.exclusiveOption) {
      onChange(isSelected ? [] : [option.value]);
      return;
    }

    // Normale Option: an-/abwählen wie gewohnt (Limit beachten).
    if (isSelected) {
      onChange(selected.filter((entry) => entry !== option.value));
    } else {
      if (limitReached) return;
      onChange([...selected, option.value]);
    }
  }

  return (
    <div>
      <motion.div
        className="flex flex-col gap-3"
        variants={cardListVariants}
        initial="hidden"
        animate="visible"
      >
        {options.map((option) => {
          const isSelected = selected.includes(option.value);

          // Wann ist diese Option gesperrt? Gewählte Optionen nie.
          let isDisabled = false;
          if (!isSelected) {
            if (option.exclusiveOption) {
              isDisabled = normalSelected;
            } else {
              isDisabled = exclusiveSelected || limitReached;
            }
          }

          return (
            <motion.button
              key={option.value}
              type="button"
              variants={cardVariants}
              disabled={isDisabled}
              whileHover={isDisabled ? undefined : { y: -2 }}
              whileTap={isDisabled ? undefined : { scale: 0.97 }}
              transition={spring}
              onClick={() => toggle(option)}
              className={`flex w-full items-center gap-3 rounded-2xl border px-5 py-4 text-left transition-[background-color,border-color,box-shadow] duration-300 ${
                isSelected
                  ? "border-rose-line bg-white ring-1 ring-rose-line shadow-[0_6px_18px_-6px_rgba(212,165,147,0.5)]"
                  : isDisabled
                    ? "cursor-not-allowed border-transparent bg-card-muted"
                    : "border-card-line bg-[linear-gradient(to_bottom,#ffffff,#fefbf8)] shadow-sm hover:border-rose-line/40 hover:shadow-md"
              }`}
            >
              {/* eckiger Checkbox-Indikator links – bei Auswahl rosé gefüllt */}
              <span
                className={`flex h-5 w-5 shrink-0 items-center justify-center rounded-md border-2 text-xs transition-opacity duration-300 ${
                  isSelected
                    ? "border-rose-line bg-rose-line text-white"
                    : isDisabled
                      ? "border-ink-soft opacity-40"
                      : "border-ink-soft"
                }`}
              >
                {isSelected && "✓"}
              </span>

              {/* Label */}
              <span
                className={`flex-1 text-ink transition-opacity duration-300 ${
                  isDisabled ? "opacity-40" : ""
                }`}
              >
                {option.label}
              </span>

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

      {/* Zähler */}
      <p className="mt-3 text-xs text-ink-soft">
        {selected.length} von max. {maxSelect} gewählt
      </p>
    </div>
  );
}
