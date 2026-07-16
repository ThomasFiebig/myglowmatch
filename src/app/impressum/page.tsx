import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "Impressum – myglowmatch",
};

export default function ImpressumPage() {
  return (
    <main className="flex flex-1 flex-col items-center px-6 py-12">
      <div className="w-full max-w-xl">
        <Link
          href="/"
          className="inline-flex w-fit items-center gap-1 text-sm text-ink-soft underline underline-offset-4 hover:text-ink"
        >
          ← Zurück
        </Link>

        <h1 className="mt-8 font-serif text-4xl leading-tight text-ink">
          Impressum
        </h1>

        <div className="mt-8 space-y-8 leading-relaxed text-ink">
          <section>
            <h2 className="font-serif text-lg font-semibold">
              Angaben gemäß § 5 DDG
            </h2>
            <p className="mt-2">
              Thomas Fiebig
              <br />
              handelnd als: Veradex (Einzelunternehmen)
              <br />
              Bürgermeister-Benz-Str. 13
              <br />
              77787 Nordrach
              <br />
              Deutschland
            </p>
          </section>

          <section>
            <h2 className="font-serif text-lg font-semibold">Kontakt</h2>
            <p className="mt-2">
              Telefon:{" "}
              <a
                href="tel:+4915150225230"
                className="underline underline-offset-4 hover:text-rosegold-dark"
              >
                +49 151 50225230
              </a>
              <br />
              E-Mail:{" "}
              <a
                href="mailto:info@veradex.de"
                className="underline underline-offset-4 hover:text-rosegold-dark"
              >
                info@veradex.de
              </a>
            </p>
          </section>

          <section>
            <h2 className="font-serif text-lg font-semibold">
              Umsatzsteuer-Identifikationsnummer
            </h2>
            <p className="mt-2">
              Umsatzsteuer-Identifikationsnummer gemäß § 27 a
              Umsatzsteuergesetz:
              <br />
              DE459689533
            </p>
          </section>

          <section>
            <h2 className="font-serif text-lg font-semibold">
              Verantwortlich für den Inhalt nach § 18 Abs. 2 MStV
            </h2>
            <p className="mt-2">
              Thomas Fiebig
              <br />
              Anschrift wie oben
            </p>
          </section>

          <section>
            <h2 className="font-serif text-lg font-semibold">
              Haftungsausschluss
            </h2>
            <p className="mt-2">
              Diese Website wird gerade überarbeitet. Zurzeit werden keine
              Inhalte oder Angebote bereitgestellt. Für die Richtigkeit,
              Vollständigkeit und Aktualität der Inhalte kann keine Gewähr
              übernommen werden. Als Diensteanbieter sind wir gemäß § 7
              Abs. 1 DDG für eigene Inhalte auf diesen Seiten nach den
              allgemeinen Gesetzen verantwortlich.
            </p>
          </section>
        </div>

        <div className="mt-12">
          <Link
            href="/"
            className="text-sm text-ink-soft underline underline-offset-4 hover:text-ink"
          >
            ← Zurück zur Startseite
          </Link>
        </div>
      </div>
    </main>
  );
}
