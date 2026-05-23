"use client";

// =====================================================================
// MotionButton – ein Knopf mit sanftem Hover-Anheben und Press-Effekt.
// Wird im ganzen Projekt für alle Knöpfe verwendet, damit sie sich
// einheitlich "premium" anfühlen.
// Bei disabled=true gibt es bewusst keine Hover-/Press-Effekte.
// =====================================================================

import type { ReactNode } from "react";
import { motion } from "framer-motion";
import { spring } from "@/lib/animations";

type MotionButtonProps = {
  children: ReactNode;
  onClick?: () => void;
  disabled?: boolean;
  type?: "button" | "submit";
  className?: string;
};

export default function MotionButton({
  children,
  onClick,
  disabled = false,
  type = "button",
  className = "",
}: MotionButtonProps) {
  return (
    <motion.button
      type={type}
      onClick={onClick}
      disabled={disabled}
      // sanftes Anheben beim Hover, Press-Effekt beim Klick
      whileHover={disabled ? undefined : { y: -2 }}
      whileTap={disabled ? undefined : { scale: 0.97 }}
      transition={spring}
      className={className}
    >
      {children}
    </motion.button>
  );
}
