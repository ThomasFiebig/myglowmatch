// =====================================================================
// PageHeader – wiederverwendbarer Header für statische Seiten
// (Impressum, Datenschutz, später ggf. weitere). Zeigt das kleine
// Logo zentriert; Klick führt zur Startseite "/".
// =====================================================================

import Link from "next/link";
import Logo from "@/components/Logo";

export default function PageHeader() {
  return (
    <header className="flex justify-center pt-4 pb-3">
      <Link
        href="/"
        aria-label="Zur Startseite"
        className="block transition-opacity hover:opacity-70"
      >
        <Logo width={90} />
      </Link>
    </header>
  );
}
