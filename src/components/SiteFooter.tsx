// =====================================================================
// SiteFooter – kleiner, dezenter Footer mit Links zu Impressum &
// Datenschutz. Wird auf der Hero-Seite und der Danke-Seite eingebunden.
// Auf den Fragebogen-Seiten bewusst NICHT, um den Mobile-Viewport
// nicht zu sprengen (Logo + Progress + Frage + Buttons müssen passen).
// =====================================================================

import Link from "next/link";

type SiteFooterProps = {
  className?: string;
};

export default function SiteFooter({ className = "" }: SiteFooterProps) {
  return (
    <nav
      aria-label="Rechtliche Hinweise"
      className={`flex justify-center gap-4 text-xs text-ink-soft ${className}`}
    >
      <Link
        href="/impressum"
        className="transition-colors hover:text-ink"
      >
        Impressum
      </Link>
      <span aria-hidden="true">·</span>
      <Link
        href="/datenschutz"
        className="transition-colors hover:text-ink"
      >
        Datenschutz
      </Link>
    </nav>
  );
}
