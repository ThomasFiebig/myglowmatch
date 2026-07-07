"use client";

// =====================================================================
// ThankYouScreen – die Bestätigungs-Seite nach erfolgreichem Absenden.
// Der Inhalt blendet sanft ein; das Häkchen "ploppt" federnd hinein.
// =====================================================================

import { motion } from "framer-motion";
import { fade, spring } from "@/lib/animations";
import Logo from "@/components/Logo";
import SiteFooter from "@/components/SiteFooter";

type ThankYouScreenProps = {
  firstName: string;
};

export default function ThankYouScreen({ firstName }: ThankYouScreenProps) {
  return (
    <main className="flex flex-1 items-center justify-center px-6 py-16">
      <motion.div
        className="w-full max-w-md text-center"
        initial={{ opacity: 0, y: 12 }}
        animate={{ opacity: 1, y: 0 }}
        transition={fade}
      >
        {/* Logo oben */}
        <div className="mb-8 flex justify-center">
          <Logo width={200} />
        </div>

        {/* Häkchen-Kreis – ploppt mit Feder-Effekt hinein */}
        <motion.div
          className="mx-auto flex h-16 w-16 items-center justify-center rounded-full bg-rosegold text-3xl text-ink"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ ...spring, delay: 0.15 }}
        >
          ✓
        </motion.div>

        <h1 className="mt-6 font-serif text-3xl font-semibold text-ink">
          Danke{firstName ? `, ${firstName}` : ""}!
        </h1>

        <p className="mt-4 leading-relaxed text-ink-soft">
          Deine Angaben sind bei deiner Beraterin. Sie meldet sich in Kürze
          persönlich bei dir — mit deiner individuellen Produktempfehlung.
        </p>

        <SiteFooter className="mt-10" />
      </motion.div>
    </main>
  );
}
