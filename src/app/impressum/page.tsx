// =====================================================================
// Impressum – Pflicht-Angaben nach § 5 DDG + Haftungsausschluss.
// Daten: Thomas Fiebig / Veradex (Einzelunternehmen).
// =====================================================================

import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/PageHeader";

export const metadata: Metadata = {
  title: "Impressum – myglowmatch",
};

export default function ImpressumPage() {
  return (
    <main className="flex flex-1 flex-col items-center">
      <div className="flex w-full max-w-md flex-col px-6 pb-12">
        <PageHeader />

        {/* Zurück-Link oben */}
        <Link
          href="/"
          className="mt-2 inline-flex w-fit items-center gap-1 text-sm text-ink-soft underline underline-offset-4 hover:text-ink"
        >
          ← Zurück zur Startseite
        </Link>

        <h1 className="mt-6 font-serif text-3xl font-semibold leading-tight text-ink">
          Impressum
        </h1>

        <div className="mt-6 space-y-8 leading-relaxed text-ink">
          {/* --- Angaben gemäß § 5 DDG ------------------------------ */}
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

          {/* --- Kontakt -------------------------------------------- */}
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

          {/* --- USt-IdNr. ------------------------------------------ */}
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

          {/* --- Verantwortlich nach MStV --------------------------- */}
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

          {/* --- Haftungsausschluss --------------------------------- */}
          <section>
            <h2 className="font-serif text-lg font-semibold">
              Haftungsausschluss
            </h2>

            <h3 className="mt-4 font-serif font-semibold">
              Haftung für Inhalte
            </h3>
            <p className="mt-2">
              Die Inhalte unserer Seiten wurden mit größter Sorgfalt
              erstellt. Für die Richtigkeit, Vollständigkeit und
              Aktualität der Inhalte können wir jedoch keine Gewähr
              übernehmen. Als Diensteanbieter sind wir gemäß § 7 Abs. 1
              DDG für eigene Inhalte auf diesen Seiten nach den
              allgemeinen Gesetzen verantwortlich. Nach §§ 8 bis 10 DDG
              sind wir als Diensteanbieter jedoch nicht verpflichtet,
              übermittelte oder gespeicherte fremde Informationen zu
              überwachen oder nach Umständen zu forschen, die auf eine
              rechtswidrige Tätigkeit hinweisen. Verpflichtungen zur
              Entfernung oder Sperrung der Nutzung von Informationen
              nach den allgemeinen Gesetzen bleiben hiervon unberührt.
              Eine diesbezügliche Haftung ist jedoch erst ab dem
              Zeitpunkt der Kenntnis einer konkreten Rechtsverletzung
              möglich. Bei Bekanntwerden von entsprechenden
              Rechtsverletzungen werden wir diese Inhalte umgehend
              entfernen.
            </p>

            <h3 className="mt-6 font-serif font-semibold">
              Haftung für Links
            </h3>
            <p className="mt-2">
              Unser Angebot enthält gegebenenfalls Links zu externen
              Websites Dritter, auf deren Inhalte wir keinen Einfluss
              haben. Deshalb können wir für diese fremden Inhalte auch
              keine Gewähr übernehmen. Für die Inhalte der verlinkten
              Seiten ist stets der jeweilige Anbieter oder Betreiber
              der Seiten verantwortlich. Die verlinkten Seiten wurden
              zum Zeitpunkt der Verlinkung auf mögliche Rechtsverstöße
              überprüft. Rechtswidrige Inhalte waren zum Zeitpunkt der
              Verlinkung nicht erkennbar. Eine permanente inhaltliche
              Kontrolle der verlinkten Seiten ist jedoch ohne konkrete
              Anhaltspunkte einer Rechtsverletzung nicht zumutbar. Bei
              Bekanntwerden von Rechtsverletzungen werden wir derartige
              Links umgehend entfernen.
            </p>

            <h3 className="mt-6 font-serif font-semibold">Urheberrecht</h3>
            <p className="mt-2">
              Die durch den Seitenbetreiber erstellten Inhalte und Werke
              auf diesen Seiten unterliegen dem deutschen Urheberrecht.
              Die Vervielfältigung, Bearbeitung, Verbreitung und jede
              Art der Verwertung außerhalb der Grenzen des
              Urheberrechtes bedürfen der schriftlichen Zustimmung des
              jeweiligen Autors bzw. Erstellers. Downloads und Kopien
              dieser Seite sind nur für den privaten, nicht
              kommerziellen Gebrauch gestattet. Soweit die Inhalte auf
              dieser Seite nicht vom Betreiber erstellt wurden, werden
              die Urheberrechte Dritter beachtet. Insbesondere werden
              Inhalte Dritter als solche gekennzeichnet. Sollten Sie
              trotzdem auf eine Urheberrechtsverletzung aufmerksam
              werden, bitten wir um einen entsprechenden Hinweis. Bei
              Bekanntwerden von Rechtsverletzungen werden wir derartige
              Inhalte umgehend entfernen.
            </p>
          </section>

          {/* --- Querverweise --------------------------------------- */}
          <section className="flex flex-col gap-3 pt-2 text-sm">
            <Link
              href="/datenschutz"
              className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
            >
              Zur Datenschutzerklärung
            </Link>
            <Link
              href="/"
              className="text-ink-soft underline underline-offset-4 hover:text-ink"
            >
              ← Zurück zur Startseite
            </Link>
          </section>
        </div>
      </div>
    </main>
  );
}
