"use client";

// =====================================================================
// Hero – Landingpage-Kopf mit Vollflächen-Bild als Background.
// Warm getönter Champagne-Verlauf oben leicht, unten voll, damit der
// Text lesbar bleibt und das Bild sanft ins Design-Farbfeld übergeht.
// =====================================================================

import Image from "next/image";
import Link from "next/link";
import Logo from "@/components/Logo";
import Reveal from "@/components/Reveal";

const btnPrimary =
  "inline-flex items-center justify-center rounded-full bg-rosegold px-8 py-4 font-medium text-ink shadow-[0_10px_30px_-12px_rgba(224,177,168,0.55)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-rosegold-dark hover:shadow-[0_16px_40px_-14px_rgba(201,143,132,0.7)]";
const btnGhost =
  "inline-flex items-center justify-center rounded-full border border-ink/15 bg-white/80 px-8 py-4 font-medium text-ink backdrop-blur transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white hover:shadow-[0_12px_30px_-14px_rgba(50,46,45,0.25)]";

export default function Hero() {
  return (
    <section className="relative isolate overflow-hidden">
      {/* Bild als absolute Background-Ebene */}
      <div className="absolute inset-0 -z-10">
        <Image
          src="/hero.jpg"
          alt="Warmes Gegenlicht auf gepflegtem, glänzendem Haar"
          fill
          priority
          sizes="100vw"
          className="object-cover"
        />
        {/* Warm getönter Verlauf drüber: unten voll-champagne, oben transparent.
            Oben bleibt Motiv sichtbar, unten geht Bild ins Design-Farbfeld über. */}
        <div className="absolute inset-0 bg-[linear-gradient(180deg,rgba(251,245,238,0.15)_0%,rgba(251,245,238,0.55)_40%,rgba(245,230,220,0.9)_85%,rgba(245,230,220,1)_100%)]" />
      </div>

      <header className="relative z-10 mx-auto flex w-full max-w-6xl items-center justify-between px-6 pt-5 pb-2">
        <Link href="/" aria-label="Zur Startseite" className="block transition-opacity hover:opacity-70">
          <Logo width={140} />
        </Link>
        <nav className="flex items-center gap-3 text-sm">
          <Link
            href="/demo"
            className="hidden rounded-full px-4 py-2 text-ink-soft transition-colors hover:text-ink sm:inline-block"
          >
            Demo
          </Link>
          <Link
            href="/login"
            className="rounded-full border border-ink/15 bg-white/60 px-4 py-2 text-ink transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white"
          >
            Login
          </Link>
        </nav>
      </header>

      <div className="relative mx-auto w-full max-w-4xl px-6 pt-24 pb-24 text-center sm:pt-32 md:pt-40 md:pb-32">
        <Reveal delay={0.05}>
          {/* Eyebrow als weißer Chip auf warmem Bild — rosegold-dark war
              auf dem Hero-Foto praktisch unsichtbar. backdrop-blur +
              halbtransparente creme-Fläche halten die Anmutung luftig. */}
          <span className="mb-6 inline-flex items-center gap-2 rounded-full bg-white/70 px-4 py-1.5 text-xs font-medium tracking-widest text-ink uppercase backdrop-blur">
            <span className="h-1.5 w-1.5 rounded-full bg-rosegold-dark" />
            Haaranalyse als Werkzeug
          </span>
        </Reveal>
        <Reveal delay={0.15} y={30}>
          <h1 className="font-serif text-4xl leading-tight text-ink sm:text-5xl md:text-6xl">
            Persönliche Pflege­empfehlung —
            <br className="hidden sm:inline" /> aus deinem Sortiment.
          </h1>
        </Reveal>
        <Reveal delay={0.3}>
          <p className="mx-auto mt-6 max-w-2xl text-lg text-ink">
            mybeautykey ist ein Haaranalyse-System für Salons, Beauty-Vertriebspartner
            und Pflege-Marken. Deine Kundinnen beantworten ein paar kurze Fragen —
            und bekommen eine Empfehlung, die aus <em>deinen</em> Produkten kommt.
          </p>
        </Reveal>
        <Reveal delay={0.45}>
          <div className="mt-10 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link href="/demo" className={`${btnPrimary} w-full sm:w-auto`}>
              Demo ausprobieren
            </Link>
            <Link href="/login" className={`${btnGhost} w-full sm:w-auto`}>
              Zum Dashboard
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
