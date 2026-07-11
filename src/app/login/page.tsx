// /login – Placeholder-Seite. Der eigentliche Anmelde-/Login-Flow (Stripe,
// Portal, Dashboard) ist noch nicht gebaut. Bis dahin fängt diese Seite
// alle Klicks aus der Landingpage-CTA "Jetzt kostenlos starten" ab, damit
// die Nutzer:innen nicht ins 404 laufen.

import Link from "next/link";
import PageHeader from "@/components/PageHeader";
import SiteFooter from "@/components/SiteFooter";
import Reveal, { FloatBlob } from "@/components/Reveal";

const btnPrimary =
  "inline-flex items-center justify-center rounded-full bg-rosegold px-8 py-4 font-medium text-ink shadow-[0_10px_30px_-12px_rgba(224,177,168,0.55)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-rosegold-dark hover:shadow-[0_16px_40px_-14px_rgba(201,143,132,0.7)]";
const btnGhost =
  "inline-flex items-center justify-center rounded-full border border-ink/15 bg-white/70 px-8 py-4 font-medium text-ink backdrop-blur transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white hover:shadow-[0_12px_30px_-14px_rgba(50,46,45,0.25)]";

export default function LoginPage() {
  return (
    <main className="flex flex-1 flex-col overflow-hidden">
      <PageHeader />

      <section className="relative mx-auto flex w-full max-w-3xl flex-1 flex-col items-center justify-center px-6 py-16 md:py-24">
        <FloatBlob
          className="left-[-4rem] top-4 h-56 w-56 bg-rosegold/25 sm:h-[20rem] sm:w-[20rem]"
          duration={18}
        />
        <FloatBlob
          className="right-[-4rem] bottom-8 h-64 w-64 bg-blush/50 sm:h-[22rem] sm:w-[22rem]"
          duration={22}
          delay={2}
        />

        <div className="relative text-center">
          <Reveal delay={0.05}>
            <span className="mb-6 inline-flex items-center gap-2 rounded-full bg-white/70 px-4 py-1.5 text-xs font-medium tracking-widest text-ink uppercase backdrop-blur">
              <span className="h-1.5 w-1.5 rounded-full bg-rosegold-dark" />
              Anmeldung
            </span>
          </Reveal>
          <Reveal delay={0.15} y={30}>
            <h1 className="font-serif text-4xl leading-tight text-ink sm:text-5xl md:text-6xl">
              Der Anmelde­bereich geht
              <br className="hidden sm:inline" /> in den Feinschliff.
            </h1>
          </Reveal>
          <Reveal delay={0.3}>
            <p className="mx-auto mt-6 max-w-xl text-lg text-ink-soft">
              Wir bauen gerade den Portal-Zugang samt Stripe-Checkout und
              Beraterinnen-Dashboard. In wenigen Tagen kannst du hier deinen
              kostenlosen Zugang erstellen und deinen persönlichen
              Beratungs-Link generieren.
            </p>
          </Reveal>
          <Reveal delay={0.45}>
            <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link href="/demo" className={`${btnPrimary} w-full sm:w-auto`}>
                Solange Demo ausprobieren
              </Link>
              <Link href="/" className={`${btnGhost} w-full sm:w-auto`}>
                Zurück zur Startseite
              </Link>
            </div>
          </Reveal>
        </div>
      </section>

      <footer className="px-6 pb-10 pt-6">
        <SiteFooter />
      </footer>
    </main>
  );
}
