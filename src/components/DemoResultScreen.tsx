"use client";

// =====================================================================
// DemoResultScreen — Vorschau-Ergebnisseite für die Test-Version.
//
// Erscheint nach dem Absenden des Fragebogens statt der klassischen
// Danke-Seite. Zeigt zwei Spalten (Basic links: Bedarfsprofil, Pro
// rechts: konkrete Produkte aus einer Fake-Bibliothek) plus die
// Beispiel-Mail an die Beraterin darunter.
//
// Wasserzeichen "DEMO" liegt semi-transparent über der gesamten Seite,
// damit die Ansicht nicht als echte Kundinnen-Empfehlung missbraucht
// werden kann.
//
// Alle Inhalte sind fest verdrahtete Beispiel-Daten. Sobald n8n eine
// echte Response zurückliefert, wird der Screen mit dynamischen Daten
// gefüllt.
// =====================================================================

import Link from "next/link";
import Logo from "@/components/Logo";
import SiteFooter from "@/components/SiteFooter";

type DemoResultScreenProps = {
  firstName: string;
};

export default function DemoResultScreen({ firstName }: DemoResultScreenProps) {
  const displayName = firstName || "du";

  return (
    <main className="relative flex flex-1 flex-col items-center px-4 py-10 md:px-8">
      {/* Diagonales DEMO-Wasserzeichen über der gesamten Seite */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-0 flex items-center justify-center overflow-hidden"
      >
        <div className="grid h-[200vh] w-[200vw] grid-cols-3 gap-x-40 -rotate-[24deg] opacity-[0.07]">
          {Array.from({ length: 30 }).map((_, i) => (
            <span
              key={i}
              className="whitespace-nowrap font-serif text-6xl font-bold uppercase tracking-widest text-rosegold-dark md:text-8xl"
            >
              Demo · nicht echt
            </span>
          ))}
        </div>
      </div>

      <div className="relative z-10 w-full max-w-6xl">
        {/* Kopfleiste */}
        <div className="mb-8 flex flex-col items-center gap-4 text-center">
          <Logo width={180} />
          <div className="inline-flex items-center gap-2 rounded-full bg-rosegold/20 px-4 py-1.5 text-xs font-semibold uppercase tracking-widest text-rosegold-dark">
            <span aria-hidden="true">⚠</span> Demo-Version · noch keine echte
            Empfehlung
          </div>
          <h1 className="font-serif text-3xl font-semibold text-ink md:text-4xl">
            Danke, {displayName}!
          </h1>
          <p className="max-w-2xl leading-relaxed text-ink-soft">
            So sieht deine Beraterin die Ergebnisse der Analyse gleich in zwei
            Varianten — links das schlanke <b>Basic</b>-Ergebnis, rechts die
            volle <b>Pro</b>-Empfehlung. Unten die Mail, die deine Beraterin
            als Kopie bekommt.
          </p>
        </div>

        {/* Zwei-Spalten-Layout: Basic links, Pro rechts */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* ================================================== */}
          {/* BASIC — Bedarfsprofil, keine Produktnamen */}
          {/* ================================================== */}
          <div className="rounded-2xl border border-blush bg-white/95 p-6 shadow-sm">
            <div className="mb-5 flex items-baseline justify-between">
              <h2 className="font-serif text-xl font-semibold text-ink">
                Basic-Ansicht
              </h2>
              <span className="rounded-full bg-blush/60 px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
                Bedarfsprofil
              </span>
            </div>

            <p className="mb-4 text-sm text-ink-soft">
              Für {displayName}s Haar empfehlen wir folgende Routine — die
              Beraterin ordnet dir dann konkrete Produkte aus ihrem Sortiment
              zu:
            </p>

            <div className="flex flex-col gap-3">
              <BasicRow
                slot="Shampoo"
                bedarf="feuchtigkeitsspendend, für mittleres bis dickes Haar mit Fokus Reparatur"
              />
              <BasicRow
                slot="Spülung"
                bedarf="tiefenwirksam, mit Frizz-Kontrolle und Entwirrung"
              />
              <BasicRow
                slot="Kur / Maske"
                bedarf="intensive Feuchtigkeit, 1× pro Woche"
              />
              <BasicRow
                slot="Leave-in"
                bedarf="Hitzeschutz, leicht in der Anwendung"
              />
              <BasicRow
                slot="Styling"
                bedarf="Volumen ohne Beschwerung, Frizz-reduzierend"
              />
            </div>

            <div className="mt-5 rounded-xl bg-blush/40 p-4 text-xs leading-relaxed text-ink-soft">
              <b className="text-rosegold-dark">So funktioniert Basic:</b> Die
              Beraterin bekommt dieses Profil und empfiehlt dir persönlich per
              WhatsApp die passenden Produkte aus ihrer Markenwelt.
            </div>
          </div>

          {/* ================================================== */}
          {/* PRO — konkrete Produkte aus Bibliothek */}
          {/* ================================================== */}
          <div className="rounded-2xl border-2 border-rosegold-dark/60 bg-gradient-to-b from-white to-blush/30 p-6 shadow-md">
            <div className="mb-5 flex items-baseline justify-between">
              <h2 className="font-serif text-xl font-semibold text-ink">
                Pro-Ansicht
              </h2>
              <span className="rounded-full bg-rosegold-dark px-3 py-1 text-[10px] font-bold uppercase tracking-widest text-white">
                Konkrete Empfehlung
              </span>
            </div>

            <p className="mb-4 text-sm text-ink-soft">
              Aus der Bibliothek deiner Beraterin — mit ihrer persönlichen
              Verkaufsbegründung pro Produkt:
            </p>

            <div className="flex flex-col gap-3">
              <ProRow
                slot="Shampoo"
                product="Renew Shampoo"
                warum="Speziell für coloriertes, trockenes Haar entwickelt. Schützt die Farbe und versorgt tief mit Feuchtigkeit."
              />
              <ProRow
                slot="Spülung"
                product="Erweiterte Feuchtigkeits-Spülung"
                warum="Perfekter Partner zum Renew Shampoo. Entwirrt sofort und macht das Kämmen leicht — auch bei lockigem Haar."
              />
              <ProRow
                slot="Kur / Maske"
                product="Super-Feuchtigkeitsmaske"
                warum="1× wöchentlich für die volle Regeneration. Nach 4 Wochen sichtbarer Unterschied bei geschädigtem Haar."
              />
              <ProRow
                slot="Leave-in"
                product="Bond IQ Leave-in"
                warum="Hitzeschutz + Reparatur in einem. Ich empfehle es allen, die regelmäßig föhnen oder stylen."
              />
              <ProRow
                slot="Styling"
                product="Moxie Mousse"
                warum="Volumen ohne Beschwerung, definiert die Struktur. Mein Favorit für dein Haar-Typ."
              />
            </div>

            <div className="mt-5 rounded-xl bg-white/70 p-4 text-xs leading-relaxed text-ink-soft ring-1 ring-rosegold/40">
              <b className="text-rosegold-dark">So funktioniert Pro:</b> Die
              Beraterin hat einmalig ihr Sortiment mit Chip-Auswahl gepflegt.
              Ab dann matcht das System bei jeder Analyse automatisch das
              richtige Produkt aus ihrem Sortiment — mit ihrer Handschrift bei
              der Verkaufsbegründung.
            </div>
          </div>
        </div>

        {/* ================================================== */}
        {/* Beispiel-Mail an die Beraterin */}
        {/* ================================================== */}
        <div className="mt-10">
          <div className="mb-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-blush" />
            <span className="text-xs font-semibold uppercase tracking-widest text-rosegold-dark">
              Beispiel · Beratungsmail an die Beraterin
            </span>
            <div className="h-px flex-1 bg-blush" />
          </div>

          <div className="mx-auto max-w-3xl overflow-hidden rounded-2xl border border-blush bg-white/95 shadow-sm">
            {/* Mail-Header */}
            <div className="border-b border-blush bg-blush/30 px-5 py-4 text-sm">
              <div className="flex gap-3">
                <span className="w-16 shrink-0 font-semibold uppercase text-[10px] tracking-widest text-rosegold-dark">
                  Von
                </span>
                <span className="text-ink">
                  myglowmatch &lt;no-reply@myglowmatch.de&gt;
                </span>
              </div>
              <div className="mt-1 flex gap-3">
                <span className="w-16 shrink-0 font-semibold uppercase text-[10px] tracking-widest text-rosegold-dark">
                  An
                </span>
                <span className="text-ink">sina.hildmann@example.com</span>
              </div>
              <div className="mt-1 flex gap-3">
                <span className="w-16 shrink-0 font-semibold uppercase text-[10px] tracking-widest text-rosegold-dark">
                  Betreff
                </span>
                <span className="font-semibold text-ink">
                  Neue Beratung: {displayName} hat den Fragebogen abgeschlossen
                </span>
              </div>
            </div>

            {/* Mail-Body */}
            <div className="space-y-4 px-6 py-6 text-sm leading-relaxed text-ink-soft">
              <p>Hallo Sina,</p>
              <p>
                gerade hat <b className="text-ink">{displayName}</b> deine
                Analyse durchlaufen. Hier die wichtigsten Punkte für dein
                Follow-up:
              </p>

              <div className="rounded-xl bg-blush/20 p-4 text-xs">
                <div className="mb-2 font-semibold uppercase tracking-widest text-rosegold-dark">
                  Kontakt
                </div>
                <div className="text-ink">
                  <div>{displayName}</div>
                  <div>📱 0151 234 567 89 (WhatsApp)</div>
                </div>
              </div>

              <div className="rounded-xl bg-blush/20 p-4 text-xs">
                <div className="mb-2 font-semibold uppercase tracking-widest text-rosegold-dark">
                  Analyse-Kernpunkte
                </div>
                <ul className="ml-4 list-disc space-y-1 text-ink">
                  <li>Struktur: leicht wellig, mittleres Volumen</li>
                  <li>Zustand: trocken, coloriert, glanzlos</li>
                  <li>
                    Kopfhaut: normal, keine besonderen Probleme
                  </li>
                  <li>Hitze-Nutzung: gelegentlich</li>
                  <li>Ziele: Feuchtigkeit, Farb-Erhalt, mehr Glanz</li>
                </ul>
              </div>

              <div className="rounded-xl bg-blush/20 p-4 text-xs">
                <div className="mb-2 font-semibold uppercase tracking-widest text-rosegold-dark">
                  Empfehlung aus deiner Bibliothek
                </div>
                <ol className="ml-4 list-decimal space-y-1 text-ink">
                  <li>Renew Shampoo</li>
                  <li>Erweiterte Feuchtigkeits-Spülung</li>
                  <li>Super-Feuchtigkeitsmaske (1× / Woche)</li>
                  <li>Bond IQ Leave-in</li>
                  <li>Moxie Mousse</li>
                </ol>
              </div>

              <p>
                Direktlink zur vollständigen Empfehlung im Portal:{" "}
                <span className="underline text-rosegold-dark">
                  portal.myglowmatch.de/kundinnen/{displayName.toLowerCase()}
                </span>
              </p>

              <p className="text-xs text-ink-soft/70">
                — Diese Mail wurde automatisch generiert und ist Teil deines
                myglowmatch-Zugangs.
              </p>
            </div>
          </div>
        </div>

        {/* Hinweis + zurück zur Vorschau */}
        <div className="mt-10 rounded-2xl bg-blush/30 p-6 text-center">
          <p className="text-sm leading-relaxed text-ink">
            <b className="text-rosegold-dark">Wichtig:</b> Diese Ansicht ist
            eine Demo-Vorschau mit Beispielprodukten. In der finalen Version
            entscheidet sich die Kundin nur eine der beiden Ansichten zu sehen
            — je nachdem, welchen Tarif ihre Beraterin gebucht hat.
          </p>
          <Link
            href="/team"
            className="mt-4 inline-block rounded-full bg-ink px-6 py-3 text-sm font-medium text-white transition hover:bg-ink/90"
          >
            ← Zurück zur Vorschau-Landing
          </Link>
        </div>

        <SiteFooter className="mt-10" />
      </div>
    </main>
  );
}

// ------------------------------------------------------------
// Basic-Row: Slot + Bedarfstext, keine Produktnamen
// ------------------------------------------------------------
function BasicRow({ slot, bedarf }: { slot: string; bedarf: string }) {
  return (
    <div className="rounded-xl border border-blush/60 bg-white p-4">
      <div className="text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
        {slot}
      </div>
      <div className="mt-1 text-sm text-ink">{bedarf}</div>
    </div>
  );
}

// ------------------------------------------------------------
// Pro-Row: Slot + Produktname + Verkaufsbegründung
// ------------------------------------------------------------
function ProRow({
  slot,
  product,
  warum,
}: {
  slot: string;
  product: string;
  warum: string;
}) {
  return (
    <div className="rounded-xl border border-blush/60 bg-white p-4">
      <div className="flex items-baseline justify-between gap-3">
        <div>
          <div className="text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
            {slot}
          </div>
          <div className="mt-0.5 font-serif text-base font-semibold text-ink">
            {product}
          </div>
        </div>
      </div>
      <div className="mt-2 text-xs italic leading-relaxed text-ink-soft">
        &bdquo;{warum}&ldquo;
      </div>
    </div>
  );
}
