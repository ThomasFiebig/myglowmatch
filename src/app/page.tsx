// Startseite "/" – Landingpage für mybeautykey (SaaS-Frontpage).
// Kein Fragebogen mehr hier: der wohnt jetzt unter /analyse.
// Hero: Variante A (Vollflächen-Bild als Background) — siehe HeroVariants.

import Image from "next/image";
import Link from "next/link";
import SiteFooter from "@/components/SiteFooter";
import Reveal, { FloatBlob } from "@/components/Reveal";
import Hero from "@/components/Hero";

// Zwei Button-Basisklassen einmal zentral, damit hover-States (leichter
// Lift + Schatten) überall gleich wirken.
const btnPrimary =
  "inline-flex items-center justify-center rounded-full bg-rosegold px-8 py-4 font-medium text-ink shadow-[0_10px_30px_-12px_rgba(224,177,168,0.55)] transition-all duration-300 hover:-translate-y-0.5 hover:bg-rosegold-dark hover:shadow-[0_16px_40px_-14px_rgba(201,143,132,0.7)]";
const btnGhost =
  "inline-flex items-center justify-center rounded-full border border-ink/15 bg-white/70 px-8 py-4 font-medium text-ink backdrop-blur transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white hover:shadow-[0_12px_30px_-14px_rgba(50,46,45,0.25)]";

export default function Home() {
  return (
    <main className="flex flex-1 flex-col overflow-hidden">
      <Hero />
      <HowItWorks />
      <ForWhom />
      <VideoPlaceholder />
      <Pricing />
      <ClosingCta />
      <footer className="px-6 pb-10 pt-6">
        <SiteFooter />
      </footer>
    </main>
  );
}

function HowItWorks() {
  const steps = [
    {
      n: "01",
      title: "Analyse",
      body:
        "Deine Kundin beantwortet Fragen zu Haar, Kopfhaut, Alltag und Zielen — mobiloptimiert, in unter drei Minuten.",
    },
    {
      n: "02",
      title: "Bedarf",
      body:
        "Das System übersetzt die Antworten in konkrete Pflege-Bedarfe: Feuchtigkeit, Hitzeschutz, Volumen, Kopfhaut-Balance.",
    },
    {
      n: "03",
      title: "Empfehlung",
      body:
        "Aus deiner hinterlegten Produkt-Bibliothek kommt die passgenaue Empfehlung — mit deiner Begründung, deinem Ton.",
    },
  ];

  return (
    <section className="relative border-y border-ink/5 bg-white/40 py-16 md:py-20">
      <div className="mx-auto w-full max-w-6xl px-6">
        <Reveal>
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
              So funktioniert&#39;s
            </h2>
            <p className="mt-4 text-ink-soft">
              Drei Schritte von der Kundin zur Empfehlung — automatisiert und markenneutral.
            </p>
          </div>
        </Reveal>
        <div className="mt-16 grid gap-10 md:grid-cols-3 md:gap-6">
          {steps.map((s, i) => {
            // Nummer 1 startet weiter rechts (driftet nach links),
            // Nummer 3 startet weiter links (driftet nach rechts),
            // Nummer 2 bleibt in ihrer Achse — klassisches "aus der Mitte
            // auseinander fahren". Auf Mobile weniger dramatisch (Werte
            // sind Pixel, ~120 px reichen für den Effekt ohne Overshoot).
            const numberX = i === 0 ? 120 : i === 2 ? -120 : 0;
            return (
              <div key={s.n} className="flex flex-col items-center">
                {/* Nummer sitzt jetzt ÜBER der Karte, groß und in
                    Rosegold-Dark statt blasser Watermark. Verbindungs-
                    Strich von der Nummer zur Karte gibt visuelle Anker-
                    Wirkung. */}
                <Reveal delay={i * 0.15} x={numberX} y={0}>
                  <div className="flex flex-col items-center">
                    <span
                      aria-hidden="true"
                      className="select-none font-serif text-6xl leading-none text-rosegold-dark md:text-7xl"
                    >
                      {s.n}
                    </span>
                    <span
                      aria-hidden="true"
                      className="mt-3 h-6 w-px bg-gradient-to-b from-rosegold-dark/60 to-transparent"
                    />
                  </div>
                </Reveal>

                <Reveal delay={i * 0.15 + 0.15} className="mt-2 w-full">
                  <div className="h-full rounded-2xl border border-ink/5 bg-white/70 p-7 transition-all duration-500 hover:-translate-y-1 hover:border-rosegold/40 hover:shadow-[0_20px_50px_-24px_rgba(224,177,168,0.5)]">
                    <h3 className="font-serif text-2xl text-ink">{s.title}</h3>
                    <p className="mt-3 text-ink-soft">{s.body}</p>
                  </div>
                </Reveal>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}

function ForWhom() {
  const groups = [
    {
      title: "Salons",
      body:
        "Analyse als Beratungs-Werkzeug am Waschbecken. Empfehlung landet direkt bei den Produkten, die im Regal stehen.",
      image: "/for-salons.png",
      alt: "Elegantes Salon-Waschbecken mit gefaltetem Handtuch und Pampasgras im warmen Morgenlicht",
    },
    {
      title: "Vertriebspartner",
      body:
        "Für Beraterinnen im Direktvertrieb — jede pflegt ihr eigenes Sortiment im Portal und empfiehlt daraus.",
      image: "/for-partners.png",
      alt: "Hand hält eine schlichte cremeweiße Pflege-Flasche auf einem Holztisch im Tageslicht",
    },
    {
      title: "Pflege-Marken",
      body:
        "Whitelabel-Analyse für den eigenen Shop — mit deinem Logo, deinem Katalog, deinem Ton.",
      image: "/for-brands.png",
      alt: "Minimalistisches Holzregal mit drei schlichten Pflege-Flaschen im Gegenlicht",
    },
  ];

  return (
    <section className="relative mx-auto w-full max-w-6xl px-6 py-16 md:py-20">
      <FloatBlob
        className="left-1/2 top-4 h-56 w-56 -translate-x-1/2 bg-blush/40 sm:top-8 sm:h-[18rem] sm:w-[18rem]"
        duration={22}
        delay={1}
      />
      <div className="relative">
        <Reveal>
          <div className="mx-auto max-w-2xl text-center">
            <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
              Für wen mybeautykey gemacht ist
            </h2>
            <p className="mt-4 text-ink-soft">
              Ein System, drei Anwendungsfälle — jeweils mit deinem eigenen Katalog.
            </p>
          </div>
        </Reveal>
        <div className="mt-12 grid gap-6 md:grid-cols-3">
          {groups.map((g, i) => (
            <Reveal key={g.title} delay={i * 0.12}>
              <div className="group h-full overflow-hidden rounded-2xl bg-white/70 backdrop-blur-sm transition-all duration-500 hover:-translate-y-1 hover:bg-white/85 hover:shadow-[0_20px_50px_-24px_rgba(224,177,168,0.5)]">
                <div className="relative aspect-[4/3] w-full overflow-hidden">
                  <Image
                    src={g.image}
                    alt={g.alt}
                    fill
                    sizes="(max-width: 768px) 100vw, (max-width: 1024px) 50vw, 33vw"
                    className="object-cover transition-transform duration-700 group-hover:scale-[1.04]"
                  />
                </div>
                <div className="p-7">
                  <h3 className="font-serif text-2xl text-ink">{g.title}</h3>
                  <p className="mt-3 text-ink-soft">{g.body}</p>
                </div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}

function VideoPlaceholder() {
  return (
    <section className="mx-auto w-full max-w-4xl px-6 pb-16 md:pb-24">
      <Reveal>
        <div className="mx-auto max-w-2xl text-center">
          <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
            In 90 Sekunden erklärt
          </h2>
          <p className="mt-4 text-ink-soft">
            Das Erklär-Video ist in Produktion. Bis dahin: einfach die Demo starten.
          </p>
        </div>
      </Reveal>
      <Reveal delay={0.1}>
        <div className="mt-10 aspect-video overflow-hidden rounded-2xl border border-ink/5 bg-white/40 transition-shadow duration-500 hover:shadow-[0_30px_60px_-30px_rgba(224,177,168,0.5)]">
          <div className="flex h-full w-full items-center justify-center">
            <div className="flex flex-col items-center gap-3 text-ink-soft">
              <div className="flex h-16 w-16 items-center justify-center rounded-full border border-ink/15 bg-white/70 transition-transform duration-500 hover:scale-110">
                <svg
                  viewBox="0 0 24 24"
                  className="ml-1 h-6 w-6"
                  fill="currentColor"
                >
                  <path d="M8 5v14l11-7z" />
                </svg>
              </div>
              <span className="text-sm">Video folgt</span>
            </div>
          </div>
        </div>
      </Reveal>
    </section>
  );
}

function Pricing() {
  const plans = [
    {
      name: "Free",
      tagline: "Zum Reinkommen",
      price: "0 €",
      cycle: "für immer",
      alt: "Kein Login, keine Kreditkarte. Persönlicher Beratungs-Link entsteht beim ersten Aufruf.",
      setup: "Kein Setup — sofort startbereit.",
      features: [
        "Analyse-Modus mit Bedarfsprofil",
        "Limit: 2 Beratungen pro Monat",
        "Upgrade-Prompt beim Erreichen",
      ],
      cta: "Kostenlos starten",
      href: "/login",
      highlighted: false,
    },
    {
      name: "Basic",
      tagline: "Das System zur Beratung",
      price: "9,90 €",
      cycle: "pro Monat",
      alt: "Oder 119 € / Jahr — Setup entfällt.",
      setup: "Setup einmalig 29,90 € — entfällt bei Jahresabo.",
      features: [
        "Portal mit Stammdaten",
        "Beratungs-Mail an die Beraterin",
        "WhatsApp-Kontakt-Button für die Kundin",
        "Übersicht der letzten 10 Analysen",
      ],
      cta: "Basic wählen",
      href: "/login",
      highlighted: false,
    },
    {
      name: "Pro",
      tagline: "Beratung mit Bibliothek",
      price: "19,90 €",
      cycle: "pro Monat",
      alt: "Oder 229 € / Jahr — Setup entfällt.",
      setup: "Setup einmalig 29,90 € — entfällt bei Jahresabo.",
      features: [
        "Eigene Produkt-Bibliothek + Team-Sharing",
        "Kundinnen sehen konkrete Produktnamen",
        "Freitext-Begründung pro Produkt",
        "Vollständiges Dashboard + Branding",
        "PWA-Installation, Push-Nachrichten",
      ],
      cta: "Pro wählen",
      href: "/login",
      highlighted: true,
    },
  ];

  return (
    <section className="relative border-t border-ink/5 bg-white/40 py-16 md:py-24">
      <div className="mx-auto w-full max-w-6xl px-6">
        <Reveal>
          <div className="mx-auto max-w-2xl text-center">
            <p className="mb-4 text-sm font-medium tracking-widest text-rosegold-dark uppercase">
              Preise
            </p>
            <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl md:text-5xl">
              Free, Basic, Pro.
            </h2>
            <p className="mt-4 text-ink-soft">
              Drei Tarife, klare Grenzen, jederzeit wechselbar. Kein Kleingedrucktes,
              keine Setup-Falle.
            </p>
          </div>
        </Reveal>

        <div className="mt-14 grid gap-6 md:grid-cols-3">
          {plans.map((p, i) => (
            <Reveal key={p.name} delay={i * 0.12}>
              <div
                className={`relative flex h-full flex-col rounded-2xl p-7 transition-all duration-500 hover:-translate-y-1 ${
                  p.highlighted
                    ? "border-2 border-rosegold bg-gradient-to-b from-white to-blush/40 shadow-[0_30px_60px_-30px_rgba(224,177,168,0.55)]"
                    : "border border-ink/5 bg-white/70 hover:shadow-[0_20px_50px_-24px_rgba(224,177,168,0.4)]"
                }`}
              >
                {p.highlighted && (
                  <span className="absolute -top-3 left-1/2 -translate-x-1/2 rounded-full bg-rosegold-dark px-4 py-1 text-[10px] font-semibold tracking-widest text-white uppercase">
                    Empfohlen
                  </span>
                )}

                <p className="text-xs font-semibold tracking-widest text-rosegold-dark uppercase">
                  {p.name}
                </p>
                <h3 className="mt-1 font-serif text-xl text-ink">{p.tagline}</h3>

                <div className="mt-6">
                  <span className="font-serif text-4xl text-ink">{p.price}</span>
                  <span className="ml-2 text-sm tracking-wide text-ink-soft uppercase">
                    {p.cycle}
                  </span>
                </div>

                <p className="mt-4 border-y border-dashed border-ink/10 py-3 text-sm text-ink-soft">
                  {p.alt}
                </p>
                <p className="mt-3 text-sm text-ink-soft">{p.setup}</p>

                <ul className="mt-6 space-y-2 text-sm text-ink">
                  {p.features.map((f) => (
                    <li key={f} className="flex items-start gap-2">
                      <svg
                        aria-hidden="true"
                        viewBox="0 0 20 20"
                        className="mt-0.5 h-4 w-4 shrink-0 text-rosegold-dark"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                      >
                        <path d="M4 10.5l4 4 8-9" />
                      </svg>
                      <span>{f}</span>
                    </li>
                  ))}
                </ul>

                <div className="mt-8 flex-1" />
                <Link
                  href={p.href}
                  className={
                    p.highlighted
                      ? `${btnPrimary} w-full`
                      : "inline-flex w-full items-center justify-center rounded-full border border-ink/15 bg-white/80 px-6 py-3 font-medium text-ink transition-all duration-300 hover:-translate-y-0.5 hover:border-ink/30 hover:bg-white"
                  }
                >
                  {p.cta}
                </Link>
              </div>
            </Reveal>
          ))}
        </div>

        <Reveal delay={0.3}>
          <p className="mx-auto mt-10 max-w-2xl text-center text-xs text-ink-soft">
            Alle Preise brutto inkl. 19 % USt. Wechsel jederzeit möglich, Kündigung
            formlos per Mail. Rechnungsstellung über VERADEX via Stripe.
          </p>
        </Reveal>
      </div>
    </section>
  );
}

function ClosingCta() {
  return (
    <section className="mx-auto w-full max-w-4xl px-6 pb-20">
      <Reveal y={40}>
        <div className="relative overflow-hidden rounded-3xl bg-rosegold/25 p-10 text-center md:p-14">
          <FloatBlob
            className="left-[-3rem] top-[-3rem] h-40 w-40 bg-white/50 sm:left-[-4rem] sm:top-[-4rem] sm:h-64 sm:w-64"
            duration={18}
          />
          <FloatBlob
            className="right-[-3rem] bottom-[-3rem] h-40 w-40 bg-rosegold/40 sm:right-[-4rem] sm:bottom-[-4rem] sm:h-64 sm:w-64"
            duration={22}
            delay={3}
          />
          <div className="relative">
            <h2 className="font-serif text-3xl leading-tight text-ink sm:text-4xl">
              Sieh selbst, wie sich das anfühlt.
            </h2>
            <p className="mx-auto mt-4 max-w-xl text-ink-soft">
              Klick durch die Demo — in unter drei Minuten hast du das komplette
              Erlebnis, das deine Kundinnen bekommen.
            </p>
            <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
              <Link href="/login" className={`${btnPrimary} w-full sm:w-auto`}>
                Jetzt kostenlos starten
              </Link>
              <Link href="/demo" className={`${btnGhost} w-full sm:w-auto`}>
                Demo ausprobieren
              </Link>
            </div>
          </div>
        </div>
      </Reveal>
    </section>
  );
}
