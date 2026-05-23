// =====================================================================
// Datenschutzerklärung
// Grundtext: e-recht24-Generator (Quelle am Ende verlinkt).
// Eigentexte zu Online-Fragebogen + n8n, KI und WhatsApp eingefügt
// zwischen "Server-Log-Dateien" und "Anfrage per E-Mail".
// =====================================================================

import type { Metadata } from "next";
import Link from "next/link";
import PageHeader from "@/components/PageHeader";

export const metadata: Metadata = {
  title: "Datenschutz – myglowmatch",
};

export default function DatenschutzPage() {
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
          Datenschutzerklärung
        </h1>

        {/* === 1. Datenschutz auf einen Blick ====================== */}
        <h2 className="mt-10 font-serif text-2xl font-semibold leading-snug text-ink">
          1. Datenschutz auf einen Blick
        </h2>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Allgemeine Hinweise
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Die folgenden Hinweise geben einen einfachen Überblick darüber,
          was mit Ihren personenbezogenen Daten passiert, wenn Sie diese
          Website besuchen. Personenbezogene Daten sind alle Daten, mit
          denen Sie persönlich identifiziert werden können. Ausführliche
          Informationen zum Thema Datenschutz entnehmen Sie unserer unter
          diesem Text aufgeführten Datenschutzerklärung.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Datenerfassung auf dieser Website
        </h3>

        <p className="mt-3 font-semibold leading-relaxed text-ink">
          Wer ist verantwortlich für die Datenerfassung auf dieser
          Website?
        </p>
        <p className="mt-2 leading-relaxed text-ink">
          Die Datenverarbeitung auf dieser Website erfolgt durch den
          Websitebetreiber. Dessen Kontaktdaten können Sie dem Abschnitt
          „Hinweis zur Verantwortlichen Stelle&ldquo; in dieser
          Datenschutzerklärung entnehmen.
        </p>

        <p className="mt-4 font-semibold leading-relaxed text-ink">
          Wie erfassen wir Ihre Daten?
        </p>
        <p className="mt-2 leading-relaxed text-ink">
          Ihre Daten werden zum einen dadurch erhoben, dass Sie uns diese
          mitteilen. Hierbei kann es sich z. B. um Daten handeln, die Sie
          in ein Kontaktformular eingeben.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Andere Daten werden automatisch oder nach Ihrer Einwilligung
          beim Besuch der Website durch unsere IT-Systeme erfasst. Das
          sind vor allem technische Daten (z. B. Internetbrowser,
          Betriebssystem oder Uhrzeit des Seitenaufrufs). Die Erfassung
          dieser Daten erfolgt automatisch, sobald Sie diese Website
          betreten.
        </p>

        <p className="mt-4 font-semibold leading-relaxed text-ink">
          Wofür nutzen wir Ihre Daten?
        </p>
        <p className="mt-2 leading-relaxed text-ink">
          Ein Teil der Daten wird erhoben, um eine fehlerfreie
          Bereitstellung der Website zu gewährleisten. Andere Daten
          können zur Analyse Ihres Nutzerverhaltens verwendet werden.
          Sofern über die Website Verträge geschlossen oder angebahnt
          werden können, werden die übermittelten Daten auch für
          Vertragsangebote, Bestellungen oder sonstige Auftragsanfragen
          verarbeitet.
        </p>

        <p className="mt-4 font-semibold leading-relaxed text-ink">
          Welche Rechte haben Sie bezüglich Ihrer Daten?
        </p>
        <p className="mt-2 leading-relaxed text-ink">
          Sie haben jederzeit das Recht, unentgeltlich Auskunft über
          Herkunft, Empfänger und Zweck Ihrer gespeicherten
          personenbezogenen Daten zu erhalten. Sie haben außerdem ein
          Recht, die Berichtigung oder Löschung dieser Daten zu
          verlangen. Wenn Sie eine Einwilligung zur Datenverarbeitung
          erteilt haben, können Sie diese Einwilligung jederzeit für die
          Zukunft widerrufen. Außerdem haben Sie das Recht, unter
          bestimmten Umständen die Einschränkung der Verarbeitung Ihrer
          personenbezogenen Daten zu verlangen. Des Weiteren steht Ihnen
          ein Beschwerderecht bei der zuständigen Aufsichtsbehörde zu.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Hierzu sowie zu weiteren Fragen zum Thema Datenschutz können
          Sie sich jederzeit an uns wenden.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Analyse-Tools und Tools von Drittanbietern
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Beim Besuch dieser Website kann Ihr Surf-Verhalten statistisch
          ausgewertet werden. Das geschieht vor allem mit sogenannten
          Analyseprogrammen.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Detaillierte Informationen zu diesen Analyseprogrammen finden
          Sie in der folgenden Datenschutzerklärung.
        </p>

        {/* === 2. Hosting ========================================== */}
        <h2 className="mt-12 font-serif text-2xl font-semibold leading-snug text-ink">
          2. Hosting
        </h2>
        <p className="mt-3 leading-relaxed text-ink">
          Wir hosten die Inhalte unserer Website bei folgendem Anbieter:
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Externes Hosting
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Diese Website wird extern gehostet. Die personenbezogenen
          Daten, die auf dieser Website erfasst werden, werden auf den
          Servern des Hosters / der Hoster gespeichert. Hierbei kann es
          sich v. a. um IP-Adressen, Kontaktanfragen, Meta- und
          Kommunikationsdaten, Vertragsdaten, Kontaktdaten, Namen,
          Websitezugriffe und sonstige Daten, die über eine Website
          generiert werden, handeln.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Das externe Hosting erfolgt zum Zwecke der Vertragserfüllung
          gegenüber unseren potenziellen und bestehenden Kunden (Art. 6
          Abs. 1 lit. b DSGVO) und im Interesse einer sicheren, schnellen
          und effizienten Bereitstellung unseres Online-Angebots durch
          einen professionellen Anbieter (Art. 6 Abs. 1 lit. f DSGVO).
          Sofern eine entsprechende Einwilligung abgefragt wurde, erfolgt
          die Verarbeitung ausschließlich auf Grundlage von Art. 6 Abs. 1
          lit. a DSGVO und § 25 Abs. 1 TDDDG, soweit die Einwilligung die
          Speicherung von Cookies oder den Zugriff auf Informationen im
          Endgerät des Nutzers (z. B. Device-Fingerprinting) im Sinne des
          TDDDG umfasst. Die Einwilligung ist jederzeit widerrufbar.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Unser(e) Hoster wird bzw. werden Ihre Daten nur insoweit
          verarbeiten, wie dies zur Erfüllung seiner Leistungspflichten
          erforderlich ist und unsere Weisungen in Bezug auf diese Daten
          befolgen.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Wir setzen folgende(n) Hoster ein:
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Vercel Inc., 340 S Lemon Ave #4133, Walnut, CA 91789, USA
          <br />
          Datenschutzerklärung:{" "}
          <a
            href="https://vercel.com/legal/privacy-policy"
            target="_blank"
            rel="noreferrer"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            https://vercel.com/legal/privacy-policy
          </a>
        </p>

        {/* === 3. Allgemeine Hinweise und Pflichtinformationen ===== */}
        <h2 className="mt-12 font-serif text-2xl font-semibold leading-snug text-ink">
          3. Allgemeine Hinweise und Pflichtinformationen
        </h2>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Datenschutz
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Die Betreiber dieser Seiten nehmen den Schutz Ihrer
          persönlichen Daten sehr ernst. Wir behandeln Ihre
          personenbezogenen Daten vertraulich und entsprechend den
          gesetzlichen Datenschutzvorschriften sowie dieser
          Datenschutzerklärung.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Wenn Sie diese Website benutzen, werden verschiedene
          personenbezogene Daten erhoben. Personenbezogene Daten sind
          Daten, mit denen Sie persönlich identifiziert werden können.
          Die vorliegende Datenschutzerklärung erläutert, welche Daten
          wir erheben und wofür wir sie nutzen. Sie erläutert auch, wie
          und zu welchem Zweck das geschieht.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Wir weisen darauf hin, dass die Datenübertragung im Internet
          (z. B. bei der Kommunikation per E-Mail) Sicherheitslücken
          aufweisen kann. Ein lückenloser Schutz der Daten vor dem
          Zugriff durch Dritte ist nicht möglich.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Hinweis zur verantwortlichen Stelle
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Die verantwortliche Stelle für die Datenverarbeitung auf dieser
          Website ist:
        </p>
        <p className="mt-3 leading-relaxed text-ink">
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
        <p className="mt-3 leading-relaxed text-ink">
          Telefon:{" "}
          <a
            href="tel:+4915150225230"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            +49 151 50225230
          </a>
          <br />
          E-Mail:{" "}
          <a
            href="mailto:info@veradex.de"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            info@veradex.de
          </a>
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Verantwortliche Stelle ist die natürliche oder juristische
          Person, die allein oder gemeinsam mit anderen über die Zwecke
          und Mittel der Verarbeitung von personenbezogenen Daten (z. B.
          Namen, E-Mail-Adressen o. Ä.) entscheidet.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Speicherdauer
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Soweit innerhalb dieser Datenschutzerklärung keine speziellere
          Speicherdauer genannt wurde, verbleiben Ihre personenbezogenen
          Daten bei uns, bis der Zweck für die Datenverarbeitung
          entfällt. Wenn Sie ein berechtigtes Löschersuchen geltend
          machen oder eine Einwilligung zur Datenverarbeitung
          widerrufen, werden Ihre Daten gelöscht, sofern wir keine
          anderen rechtlich zulässigen Gründe für die Speicherung Ihrer
          personenbezogenen Daten haben (z. B. steuer- oder
          handelsrechtliche Aufbewahrungsfristen); im letztgenannten Fall
          erfolgt die Löschung nach Fortfall dieser Gründe.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Allgemeine Hinweise zu den Rechtsgrundlagen der
          Datenverarbeitung auf dieser Website
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Sofern Sie in die Datenverarbeitung eingewilligt haben,
          verarbeiten wir Ihre personenbezogenen Daten auf Grundlage von
          Art. 6 Abs. 1 lit. a DSGVO bzw. Art. 9 Abs. 2 lit. a DSGVO,
          sofern besondere Datenkategorien nach Art. 9 Abs. 1 DSGVO
          verarbeitet werden. Im Falle einer ausdrücklichen Einwilligung
          in die Übertragung personenbezogener Daten in Drittstaaten
          erfolgt die Datenverarbeitung außerdem auf Grundlage von
          Art. 49 Abs. 1 lit. a DSGVO. Sofern Sie in die Speicherung von
          Cookies oder in den Zugriff auf Informationen in Ihr Endgerät
          (z. B. via Device-Fingerprinting) eingewilligt haben, erfolgt
          die Datenverarbeitung zusätzlich auf Grundlage von § 25 Abs. 1
          TDDDG. Die Einwilligung ist jederzeit widerrufbar. Sind Ihre
          Daten zur Vertragserfüllung oder zur Durchführung
          vorvertraglicher Maßnahmen erforderlich, verarbeiten wir Ihre
          Daten auf Grundlage des Art. 6 Abs. 1 lit. b DSGVO. Des
          Weiteren verarbeiten wir Ihre Daten, sofern diese zur Erfüllung
          einer rechtlichen Verpflichtung erforderlich sind auf Grundlage
          von Art. 6 Abs. 1 lit. c DSGVO. Die Datenverarbeitung kann
          ferner auf Grundlage unseres berechtigten Interesses nach
          Art. 6 Abs. 1 lit. f DSGVO erfolgen. Über die jeweils im
          Einzelfall einschlägigen Rechtsgrundlagen wird in den folgenden
          Absätzen dieser Datenschutzerklärung informiert.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Empfänger von personenbezogenen Daten
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Im Rahmen unserer Geschäftstätigkeit arbeiten wir mit
          verschiedenen externen Stellen zusammen. Dabei ist teilweise
          auch eine Übermittlung von personenbezogenen Daten an diese
          externen Stellen erforderlich. Wir geben personenbezogene Daten
          nur dann an externe Stellen weiter, wenn dies im Rahmen einer
          Vertragserfüllung erforderlich ist, wenn wir gesetzlich hierzu
          verpflichtet sind (z. B. Weitergabe von Daten an
          Steuerbehörden), wenn wir ein berechtigtes Interesse nach
          Art. 6 Abs. 1 lit. f DSGVO an der Weitergabe haben oder wenn
          eine sonstige Rechtsgrundlage die Datenweitergabe erlaubt. Beim
          Einsatz von Auftragsverarbeitern geben wir personenbezogene
          Daten unserer Kunden nur auf Grundlage eines gültigen Vertrags
          über Auftragsverarbeitung weiter. Im Falle einer gemeinsamen
          Verarbeitung wird ein Vertrag über gemeinsame Verarbeitung
          geschlossen.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Widerruf Ihrer Einwilligung zur Datenverarbeitung
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Viele Datenverarbeitungsvorgänge sind nur mit Ihrer
          ausdrücklichen Einwilligung möglich. Sie können eine bereits
          erteilte Einwilligung jederzeit widerrufen. Die Rechtmäßigkeit
          der bis zum Widerruf erfolgten Datenverarbeitung bleibt vom
          Widerruf unberührt.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Widerspruchsrecht gegen die Datenerhebung in besonderen Fällen
          sowie gegen Direktwerbung (Art. 21 DSGVO)
        </h3>
        <div className="mt-3 rounded-2xl bg-blush p-5 text-sm leading-relaxed tracking-wide text-ink">
          <p>
            WENN DIE DATENVERARBEITUNG AUF GRUNDLAGE VON ART. 6 ABS. 1
            LIT. E ODER F DSGVO ERFOLGT, HABEN SIE JEDERZEIT DAS RECHT,
            AUS GRÜNDEN, DIE SICH AUS IHRER BESONDEREN SITUATION ERGEBEN,
            GEGEN DIE VERARBEITUNG IHRER PERSONENBEZOGENEN DATEN
            WIDERSPRUCH EINZULEGEN; DIES GILT AUCH FÜR EIN AUF DIESE
            BESTIMMUNGEN GESTÜTZTES PROFILING. DIE JEWEILIGE
            RECHTSGRUNDLAGE, AUF DENEN EINE VERARBEITUNG BERUHT,
            ENTNEHMEN SIE DIESER DATENSCHUTZERKLÄRUNG. WENN SIE
            WIDERSPRUCH EINLEGEN, WERDEN WIR IHRE BETROFFENEN
            PERSONENBEZOGENEN DATEN NICHT MEHR VERARBEITEN, ES SEI DENN,
            WIR KÖNNEN ZWINGENDE SCHUTZWÜRDIGE GRÜNDE FÜR DIE
            VERARBEITUNG NACHWEISEN, DIE IHRE INTERESSEN, RECHTE UND
            FREIHEITEN ÜBERWIEGEN ODER DIE VERARBEITUNG DIENT DER
            GELTENDMACHUNG, AUSÜBUNG ODER VERTEIDIGUNG VON
            RECHTSANSPRÜCHEN (WIDERSPRUCH NACH ART. 21 ABS. 1 DSGVO).
          </p>
          <p className="mt-4">
            WERDEN IHRE PERSONENBEZOGENEN DATEN VERARBEITET, UM
            DIREKTWERBUNG ZU BETREIBEN, SO HABEN SIE DAS RECHT, JEDERZEIT
            WIDERSPRUCH GEGEN DIE VERARBEITUNG SIE BETREFFENDER
            PERSONENBEZOGENER DATEN ZUM ZWECKE DERARTIGER WERBUNG
            EINZULEGEN; DIES GILT AUCH FÜR DAS PROFILING, SOWEIT ES MIT
            SOLCHER DIREKTWERBUNG IN VERBINDUNG STEHT. WENN SIE
            WIDERSPRECHEN, WERDEN IHRE PERSONENBEZOGENEN DATEN
            ANSCHLIESSEND NICHT MEHR ZUM ZWECKE DER DIREKTWERBUNG
            VERWENDET (WIDERSPRUCH NACH ART. 21 ABS. 2 DSGVO).
          </p>
        </div>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Beschwerderecht bei der zuständigen Aufsichtsbehörde
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Im Falle von Verstößen gegen die DSGVO steht den Betroffenen
          ein Beschwerderecht bei einer Aufsichtsbehörde, insbesondere in
          dem Mitgliedstaat ihres gewöhnlichen Aufenthalts, ihres
          Arbeitsplatzes oder des Orts des mutmaßlichen Verstoßes zu. Das
          Beschwerderecht besteht unbeschadet anderweitiger
          verwaltungsrechtlicher oder gerichtlicher Rechtsbehelfe.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Recht auf Datenübertragbarkeit
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Sie haben das Recht, Daten, die wir auf Grundlage Ihrer
          Einwilligung oder in Erfüllung eines Vertrags automatisiert
          verarbeiten, an sich oder an einen Dritten in einem gängigen,
          maschinenlesbaren Format aushändigen zu lassen. Sofern Sie die
          direkte Übertragung der Daten an einen anderen Verantwortlichen
          verlangen, erfolgt dies nur, soweit es technisch machbar ist.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Auskunft, Berichtigung und Löschung
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Sie haben im Rahmen der geltenden gesetzlichen Bestimmungen
          jederzeit das Recht auf unentgeltliche Auskunft über Ihre
          gespeicherten personenbezogenen Daten, deren Herkunft und
          Empfänger und den Zweck der Datenverarbeitung und ggf. ein
          Recht auf Berichtigung oder Löschung dieser Daten. Hierzu sowie
          zu weiteren Fragen zum Thema personenbezogene Daten können Sie
          sich jederzeit an uns wenden.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Recht auf Einschränkung der Verarbeitung
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Sie haben das Recht, die Einschränkung der Verarbeitung Ihrer
          personenbezogenen Daten zu verlangen. Hierzu können Sie sich
          jederzeit an uns wenden. Das Recht auf Einschränkung der
          Verarbeitung besteht in folgenden Fällen:
        </p>
        <ul className="mt-3 list-disc space-y-2 pl-5 leading-relaxed text-ink">
          <li>
            Wenn Sie die Richtigkeit Ihrer bei uns gespeicherten
            personenbezogenen Daten bestreiten, benötigen wir in der
            Regel Zeit, um dies zu überprüfen. Für die Dauer der Prüfung
            haben Sie das Recht, die Einschränkung der Verarbeitung Ihrer
            personenbezogenen Daten zu verlangen.
          </li>
          <li>
            Wenn die Verarbeitung Ihrer personenbezogenen Daten
            unrechtmäßig geschah/geschieht, können Sie statt der Löschung
            die Einschränkung der Datenverarbeitung verlangen.
          </li>
          <li>
            Wenn wir Ihre personenbezogenen Daten nicht mehr benötigen,
            Sie sie jedoch zur Ausübung, Verteidigung oder
            Geltendmachung von Rechtsansprüchen benötigen, haben Sie das
            Recht, statt der Löschung die Einschränkung der Verarbeitung
            Ihrer personenbezogenen Daten zu verlangen.
          </li>
          <li>
            Wenn Sie einen Widerspruch nach Art. 21 Abs. 1 DSGVO
            eingelegt haben, muss eine Abwägung zwischen Ihren und
            unseren Interessen vorgenommen werden. Solange noch nicht
            feststeht, wessen Interessen überwiegen, haben Sie das Recht,
            die Einschränkung der Verarbeitung Ihrer personenbezogenen
            Daten zu verlangen.
          </li>
        </ul>
        <p className="mt-3 leading-relaxed text-ink">
          Wenn Sie die Verarbeitung Ihrer personenbezogenen Daten
          eingeschränkt haben, dürfen diese Daten – von ihrer Speicherung
          abgesehen – nur mit Ihrer Einwilligung oder zur Geltendmachung,
          Ausübung oder Verteidigung von Rechtsansprüchen oder zum Schutz
          der Rechte einer anderen natürlichen oder juristischen Person
          oder aus Gründen eines wichtigen öffentlichen Interesses der
          Europäischen Union oder eines Mitgliedstaats verarbeitet
          werden.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          SSL- bzw. TLS-Verschlüsselung
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Diese Seite nutzt aus Sicherheitsgründen und zum Schutz der
          Übertragung vertraulicher Inhalte, wie zum Beispiel
          Bestellungen oder Anfragen, die Sie an uns als Seitenbetreiber
          senden, eine SSL- bzw. TLS-Verschlüsselung. Eine verschlüsselte
          Verbindung erkennen Sie daran, dass die Adresszeile des
          Browsers von „http://&ldquo; auf „https://&ldquo; wechselt und an dem
          Schloss-Symbol in Ihrer Browserzeile.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Wenn die SSL- bzw. TLS-Verschlüsselung aktiviert ist, können
          die Daten, die Sie an uns übermitteln, nicht von Dritten
          mitgelesen werden.
        </p>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Widerspruch gegen Werbe-E-Mails
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Der Nutzung von im Rahmen der Impressumspflicht
          veröffentlichten Kontaktdaten zur Übersendung von nicht
          ausdrücklich angeforderter Werbung und Informationsmaterialien
          wird hiermit widersprochen. Die Betreiber der Seiten behalten
          sich ausdrücklich rechtliche Schritte im Falle der unverlangten
          Zusendung von Werbeinformationen, etwa durch Spam-E-Mails, vor.
        </p>

        {/* === 4. Datenerfassung auf dieser Website ================ */}
        <h2 className="mt-12 font-serif text-2xl font-semibold leading-snug text-ink">
          4. Datenerfassung auf dieser Website
        </h2>

        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Server-Log-Dateien
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Der Provider der Seiten erhebt und speichert automatisch
          Informationen in so genannten Server-Log-Dateien, die Ihr
          Browser automatisch an uns übermittelt. Dies sind:
        </p>
        <ul className="mt-3 list-disc space-y-1 pl-5 leading-relaxed text-ink">
          <li>Browsertyp und Browserversion</li>
          <li>verwendetes Betriebssystem</li>
          <li>Referrer URL</li>
          <li>Hostname des zugreifenden Rechners</li>
          <li>Uhrzeit der Serveranfrage</li>
          <li>IP-Adresse</li>
        </ul>
        <p className="mt-3 leading-relaxed text-ink">
          Eine Zusammenführung dieser Daten mit anderen Datenquellen wird
          nicht vorgenommen.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Die Erfassung dieser Daten erfolgt auf Grundlage von Art. 6
          Abs. 1 lit. f DSGVO. Der Websitebetreiber hat ein berechtigtes
          Interesse an der technisch fehlerfreien Darstellung und der
          Optimierung seiner Website – hierzu müssen die Server-Log-Files
          erfasst werden.
        </p>

        {/* --- Eigentext 1: Online-Fragebogen ------------------- */}
        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Online-Fragebogen zur Haaranalyse
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Auf dieser Website bieten wir einen Online-Fragebogen zur
          Erstellung einer personalisierten Haarpflege-Empfehlung an. Im
          Rahmen dieses Fragebogens erheben wir folgende Daten:
        </p>
        <ul className="mt-3 list-disc space-y-1 pl-5 leading-relaxed text-ink">
          <li>Vorname</li>
          <li>E-Mail-Adresse</li>
          <li>
            Antworten zu Haar- und Kopfhautmerkmalen (Haartyp,
            Pflegebedürfnisse etc.)
          </li>
          <li>
            Optional: Einwilligung zum Erhalt weiterer Informationen
          </li>
        </ul>
        <p className="mt-3 leading-relaxed text-ink">
          Die Verarbeitung erfolgt ausschließlich zum Zweck der
          Erstellung einer individuellen Produktempfehlung und deren
          Versand an die angegebene E-Mail-Adresse. Rechtsgrundlage ist
          Ihre Einwilligung gemäß Art. 6 Abs. 1 lit. a DSGVO. Sie können
          diese Einwilligung jederzeit widerrufen, indem Sie uns eine
          formlose Mitteilung per E-Mail zukommen lassen.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Zur technischen Verarbeitung der Fragebogen-Daten und Auswahl
          passender Produktempfehlungen nutzen wir den Dienst n8n Cloud
          (n8n GmbH, Krausenstraße 38, 10117 Berlin, Deutschland). Die
          Daten werden auf Servern innerhalb der Europäischen Union
          verarbeitet. Weitere Informationen zum Datenschutz bei n8n
          finden Sie unter:{" "}
          <a
            href="https://n8n.io/legal/privacy"
            target="_blank"
            rel="noreferrer"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            https://n8n.io/legal/privacy
          </a>
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Die Empfehlungs-E-Mail wird über einen externen
          E-Mail-Versanddienst (SMTP) zugestellt. Hierbei werden Ihre
          E-Mail-Adresse und der Inhalt der Empfehlung verarbeitet.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Ihre Daten verbleiben bei uns, bis Sie der Speicherung
          widersprechen oder der Zweck für die Speicherung entfällt.
        </p>

        {/* --- Eigentext 2: KI --------------------------------- */}
        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Einsatz von Künstlicher Intelligenz (KI)
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Zur Erstellung Ihrer personalisierten Produktempfehlung setzen
          wir KI-gestützte Verfahren ein. Konkret werden Ihre Antworten
          aus dem Fragebogen mithilfe regelbasierter Algorithmen
          ausgewertet, um die für Ihren Haartyp passenden Produkte aus
          unserer Datenbank zu identifizieren.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Ihre Daten werden dabei ausschließlich zur Erstellung Ihrer
          persönlichen Empfehlung verwendet. Eine Nutzung Ihrer Daten zu
          Trainingszwecken durch KI-Anbieter findet nicht statt.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Rechtsgrundlage für diese Verarbeitung ist Ihre Einwilligung
          (Art. 6 Abs. 1 lit. a DSGVO).
        </p>

        {/* --- Eigentext 3: WhatsApp --------------------------- */}
        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Kommunikation via WhatsApp
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          In unserer Empfehlungs-E-Mail finden Sie die Möglichkeit, über
          einen Button direkt eine Nachricht via WhatsApp an Ihre
          persönliche Beraterin zu senden. Wenn Sie diesen Button
          anklicken, werden Sie zur WhatsApp-Anwendung weitergeleitet.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          WhatsApp wird betrieben von der WhatsApp Ireland Limited, 4
          Grand Canal Square, Grand Canal Harbour, Dublin 2, Irland. Bei
          der Kommunikation über WhatsApp verarbeitet WhatsApp Ihre Daten
          (insbesondere Telefonnummer, Nachrichteninhalt, Metadaten)
          gemäß den Datenschutzbestimmungen von WhatsApp.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Weitere Informationen:{" "}
          <a
            href="https://www.whatsapp.com/legal/privacy-policy-eea"
            target="_blank"
            rel="noreferrer"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            https://www.whatsapp.com/legal/privacy-policy-eea
          </a>
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Die Nutzung des WhatsApp-Buttons ist freiwillig.
          Rechtsgrundlage ist Ihre Einwilligung gemäß Art. 6 Abs. 1 lit.
          a DSGVO, die Sie durch Anklicken des Buttons erteilen.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Bitte beachten Sie: Da WhatsApp auch außerhalb der EU Daten
          verarbeiten kann, können wir nicht garantieren, dass das
          Datenschutzniveau dem der EU entspricht.
        </p>

        {/* --- Continued e-recht24: Anfrage per E-Mail ---------- */}
        <h3 className="mt-6 font-serif text-lg font-semibold text-ink">
          Anfrage per E-Mail, Telefon oder Telefax
        </h3>
        <p className="mt-3 leading-relaxed text-ink">
          Wenn Sie uns per E-Mail, Telefon oder Telefax kontaktieren,
          wird Ihre Anfrage inklusive aller daraus hervorgehenden
          personenbezogenen Daten (Name, Anfrage) zum Zwecke der
          Bearbeitung Ihres Anliegens bei uns gespeichert und
          verarbeitet. Diese Daten geben wir nicht ohne Ihre Einwilligung
          weiter.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Die Verarbeitung dieser Daten erfolgt auf Grundlage von Art. 6
          Abs. 1 lit. b DSGVO, sofern Ihre Anfrage mit der Erfüllung
          eines Vertrags zusammenhängt oder zur Durchführung
          vorvertraglicher Maßnahmen erforderlich ist. In allen übrigen
          Fällen beruht die Verarbeitung auf unserem berechtigten
          Interesse an der effektiven Bearbeitung der an uns gerichteten
          Anfragen (Art. 6 Abs. 1 lit. f DSGVO) oder auf Ihrer
          Einwilligung (Art. 6 Abs. 1 lit. a DSGVO) sofern diese
          abgefragt wurde; die Einwilligung ist jederzeit widerrufbar.
        </p>
        <p className="mt-3 leading-relaxed text-ink">
          Die von Ihnen an uns per Kontaktanfragen übersandten Daten
          verbleiben bei uns, bis Sie uns zur Löschung auffordern, Ihre
          Einwilligung zur Speicherung widerrufen oder der Zweck für die
          Datenspeicherung entfällt (z. B. nach abgeschlossener
          Bearbeitung Ihres Anliegens). Zwingende gesetzliche
          Bestimmungen – insbesondere gesetzliche Aufbewahrungsfristen –
          bleiben unberührt.
        </p>

        {/* Stand & Quelle */}
        <p className="mt-12 text-sm text-ink-soft">Stand: Mai 2026</p>
        <p className="mt-2 text-sm text-ink-soft">
          Quelle:{" "}
          <a
            href="https://www.e-recht24.de"
            target="_blank"
            rel="noreferrer"
            className="underline underline-offset-4 hover:text-ink"
          >
            https://www.e-recht24.de
          </a>
        </p>

        {/* Querverweise unten */}
        <section className="mt-12 flex flex-col gap-3 text-sm">
          <Link
            href="/impressum"
            className="text-rose-line underline underline-offset-4 hover:text-rosegold-dark"
          >
            Zum Impressum
          </Link>
          <Link
            href="/"
            className="text-ink-soft underline underline-offset-4 hover:text-ink"
          >
            ← Zurück zur Startseite
          </Link>
        </section>
      </div>
    </main>
  );
}
