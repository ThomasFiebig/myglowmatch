"use client";

// =====================================================================
// DemoResultScreen — Vorschau-Ergebnisseite für die Test-Version.
//
// Erscheint nach dem Absenden des Fragebogens statt der klassischen
// Danke-Seite. Zeigt zwei Spalten (Basic links: Bedarfsprofil, Pro
// rechts: konkrete Produkte) plus die Beispiel-Mail an die Beraterin
// darunter.
//
// Wenn n8n die Empfehlung als Response zurückliefert (via
// „Respond to Webhook"-Node), werden echte Daten dargestellt. Sonst
// Fake-Daten als Fallback.
//
// Wasserzeichen "DEMO" liegt semi-transparent über der gesamten Seite.
// =====================================================================

import Link from "next/link";
import type {
  Answers,
  NormalizedAnswers,
  RecommendationProduct,
  RecommendationResult,
} from "@/lib/types";
import Logo from "@/components/Logo";
import SiteFooter from "@/components/SiteFooter";

type DemoResultScreenProps = {
  firstName: string;
  phone: string;
  answers: Answers;
  recommendation: RecommendationResult | null;
};

// ---------------------------------------------------------------
// Anzeige-Wörterbücher (Enum-Werte → menschenlesbare Labels)
// Werden für Beraterin-Mail und Basic-Ansicht gebraucht.
// ---------------------------------------------------------------
const HAIR_STRUCTURE_LABEL: Record<string, string> = {
  glatt: "glatt",
  wellig: "wellig",
  lockig: "lockig",
  kraus: "kraus",
};
const HAIR_THICKNESS_LABEL: Record<string, string> = {
  fein: "fein",
  mittel: "mittelstark",
  dick: "dick / kräftig",
};
const HAIR_CONDITION_LABEL: Record<string, string> = {
  keine_probleme: "keine besonderen Probleme",
  trocken: "trocken",
  frizz: "Frizz",
  glanzlos: "glanzlos",
  kraftlos: "kraftlos",
  duenn: "dünner werdend",
  spliss: "Spliss",
  haarbruch: "Haarbruch",
  stark_geschaedigt: "stark geschädigt",
};
const SCALP_LABEL: Record<string, string> = {
  keine_probleme: "unauffällig",
  normal: "normal",
  fettig: "fettig",
  schuppig: "schuppig",
  juckend_empfindlich: "juckend / empfindlich",
  schnell_nachfettender_ansatz: "schnell nachfettender Ansatz",
};
const TREATMENT_LABEL: Record<string, string> = {
  nein: "unbehandelt",
  gefaerbt: "gefärbt",
  blondiert: "blondiert",
  dauergewellt: "dauergewellt",
  geglaettet: "geglättet / gestrafft",
};
const CARE_GOAL_LABEL: Record<string, string> = {
  mehr_feuchtigkeit: "mehr Feuchtigkeit",
  mehr_glanz: "mehr Glanz",
  mehr_volumen: "mehr Volumen",
  weniger_frizz: "weniger Frizz",
  farb_erhalt: "Farb-Erhalt",
  kopfhaut_pflege: "Kopfhaut-Pflege",
  schnellere_haarwaesche: "seltener waschen",
  reparatur: "Reparatur",
  hitzeschutz: "Hitzeschutz",
};

// ---------------------------------------------------------------
// Slot-Typ → menschenlesbarer Slot-Label + Sortier-Reihenfolge.
// ---------------------------------------------------------------
const SLOT_LABEL: Record<string, string> = {
  shampoo: "Shampoo",
  spuelung: "Spülung",
  maske: "Kur / Maske",
  leave_in: "Leave-in",
  styling_1: "Styling",
  styling_2: "Styling (2)",
  styling_3: "Styling (3)",
  scalp: "Kopfhaut-Pflege",
  serum: "Serum",
};
const SLOT_ORDER = [
  "shampoo",
  "spuelung",
  "maske",
  "leave_in",
  "scalp",
  "serum",
  "styling_1",
  "styling_2",
  "styling_3",
];

// ---------------------------------------------------------------
// Bedarfsprofil pro Slot ableiten (für Basic-Ansicht).
// Nutzt die normalisierten Antworten der Kundin.
// ---------------------------------------------------------------
function buildBedarf(slotTyp: string, n: NormalizedAnswers): string {
  const parts: string[] = [];
  const goals = n.care_goals ?? [];
  const conditions = n.hair_condition ?? [];
  const structure = n.hair_structure ?? "";
  const thickness = n.hair_thickness ?? "";

  if (slotTyp === "shampoo") {
    if (
      goals.includes("mehr_feuchtigkeit") ||
      conditions.includes("trocken")
    )
      parts.push("feuchtigkeitsspendend");
    if (conditions.includes("stark_geschaedigt")) parts.push("reparierend");
    if (goals.includes("farb_erhalt") || n.hair_treatments === "gefaerbt")
      parts.push("farb-erhaltend");
    if (goals.includes("mehr_glanz") || conditions.includes("glanzlos"))
      parts.push("Glanz-fördernd");
    if (goals.includes("mehr_volumen") || conditions.includes("kraftlos"))
      parts.push("volumen-gebend");
    if (conditions.includes("fettig")) parts.push("mild-reinigend");
  } else if (slotTyp === "spuelung") {
    parts.push("tiefenwirksam");
    if (conditions.includes("frizz")) parts.push("Frizz-kontrollierend");
    if (["wellig", "lockig", "kraus"].includes(structure))
      parts.push("entwirrend");
    if (goals.includes("mehr_feuchtigkeit")) parts.push("feuchtigkeitsspendend");
  } else if (slotTyp === "maske") {
    parts.push("intensive Pflege");
    if (goals.includes("reparatur") || conditions.includes("stark_geschaedigt"))
      parts.push("Reparatur");
    if (conditions.includes("trocken"))
      parts.push("Feuchtigkeit für trockenes Haar");
  } else if (slotTyp === "leave_in") {
    if (n.heat_frequency !== "nie_selten") parts.push("Hitzeschutz");
    parts.push("leicht in der Anwendung");
    if (conditions.includes("frizz")) parts.push("Frizz-Kontrolle");
  } else if (slotTyp === "styling_1" || slotTyp === "styling_2") {
    if (goals.includes("mehr_volumen") || conditions.includes("kraftlos"))
      parts.push("Volumen ohne Beschwerung");
    if (["lockig", "kraus"].includes(structure))
      parts.push("Locken-definierend");
    if (n.heat_frequency !== "nie_selten") parts.push("Hitzeschutz");
    if (conditions.includes("frizz")) parts.push("Frizz-reduzierend");
  } else if (slotTyp === "scalp") {
    parts.push("Kopfhaut-Balance");
    if ((n.scalp_status ?? []).includes("juckend_empfindlich"))
      parts.push("beruhigend");
    if ((n.scalp_status ?? []).includes("fettig")) parts.push("balancierend");
  } else if (slotTyp === "serum") {
    parts.push("gezielte Behandlung");
    if (conditions.includes("spliss")) parts.push("Spitzen-Pflege");
  }

  if (parts.length === 0) return "abgestimmt auf deinen Bedarf";

  // Struktur/Stärke am Ende ergänzen (nur für Waschprodukte)
  if (["shampoo", "spuelung", "maske"].includes(slotTyp)) {
    const suffix: string[] = [];
    if (structure)
      suffix.push(`${HAIR_STRUCTURE_LABEL[structure] || structure}es Haar`);
    if (thickness) suffix.push(HAIR_THICKNESS_LABEL[thickness] || thickness);
    if (suffix.length > 0) {
      return `${parts.join(", ")} · für ${suffix.join(", ")}`;
    }
  }

  return parts.join(", ");
}

// ---------------------------------------------------------------
// Kompakte Antwort-Zusammenfassung für die Beraterin-Mail.
// ---------------------------------------------------------------
function buildAnalysisPoints(n: NormalizedAnswers): string[] {
  const points: string[] = [];
  const structure = n.hair_structure ?? "";
  const thickness = n.hair_thickness ?? "";
  const conditions = n.hair_condition ?? [];
  const scalp = n.scalp_status ?? [];

  const structureLabel = HAIR_STRUCTURE_LABEL[structure] || structure;
  const thicknessLabel = HAIR_THICKNESS_LABEL[thickness] || thickness;
  if (structureLabel || thicknessLabel) {
    points.push(
      `Struktur: ${[structureLabel, thicknessLabel].filter(Boolean).join(", ")}`,
    );
  }

  const condLabels = conditions
    .map((c) => HAIR_CONDITION_LABEL[c] || c)
    .filter(Boolean);
  if (condLabels.length) {
    points.push(`Zustand: ${condLabels.join(", ")}`);
  }

  const scalpLabels = scalp
    .map((s) => SCALP_LABEL[s] || s)
    .filter(Boolean);
  if (scalpLabels.length) {
    points.push(`Kopfhaut: ${scalpLabels.join(", ")}`);
  }

  if (n.hair_treatments && n.hair_treatments !== "nein") {
    points.push(
      `Behandlungen: ${TREATMENT_LABEL[n.hair_treatments] || n.hair_treatments}`,
    );
  }

  if (n.heat_frequency) {
    const heatMap: Record<string, string> = {
      nie_selten: "selten oder nie",
      gelegentlich: "gelegentlich",
      regelmaessig: "regelmäßig",
    };
    points.push(`Hitze-Styling: ${heatMap[n.heat_frequency] || n.heat_frequency}`);
  }

  const goals = (n.care_goals ?? [])
    .map((g) => CARE_GOAL_LABEL[g] || g)
    .filter(Boolean);
  if (goals.length) {
    points.push(`Ziele: ${goals.join(", ")}`);
  }

  return points;
}

// ---------------------------------------------------------------
// Fake-Fallback-Daten (wenn n8n keine Response schickt oder Format
// unerwartet ist).
// ---------------------------------------------------------------
const FAKE_ROUTINE: RecommendationProduct[] = [
  { produktname_de: "Renew Shampoo", slot_typ: "shampoo", anwendungs_schritt: 1 },
  {
    produktname_de: "Erweiterte Feuchtigkeits-Spülung",
    slot_typ: "spuelung",
    anwendungs_schritt: 2,
  },
  {
    produktname_de: "Super-Feuchtigkeitsmaske",
    slot_typ: "maske",
    anwendungs_schritt: 3,
  },
  { produktname_de: "Bond IQ Leave-in", slot_typ: "leave_in", anwendungs_schritt: 4 },
  { produktname_de: "Moxie Mousse", slot_typ: "styling_1", anwendungs_schritt: 5 },
];
const FAKE_WARUM: Record<string, string> = {
  shampoo:
    "Speziell für coloriertes, trockenes Haar. Schützt die Farbe und versorgt tief mit Feuchtigkeit.",
  spuelung:
    "Perfekter Partner zum Shampoo. Entwirrt sofort und macht das Kämmen leicht.",
  maske:
    "1× wöchentlich für die volle Regeneration. Nach 4 Wochen sichtbarer Unterschied.",
  leave_in:
    "Hitzeschutz + Reparatur in einem. Ideal wenn du regelmäßig föhnst.",
  styling_1:
    "Volumen ohne Beschwerung. Definiert die Struktur und hält den ganzen Tag.",
  styling_2: "Formung mit sanftem Halt.",
  scalp: "Beruhigt die Kopfhaut und bringt sie in Balance.",
  serum: "Gezielte Behandlung für die Spitzen.",
};

export default function DemoResultScreen({
  firstName,
  phone,
  answers,
  recommendation,
}: DemoResultScreenProps) {
  const displayName = firstName || "du";
  const hasRealData = Boolean(
    recommendation?.final_routine && recommendation.final_routine.length > 0,
  );

  // Normalisierte Antworten für Bedarfs- und Analyse-Ableitung.
  // Fallback: aus dem raw `answers`-Objekt kombinieren.
  const normalized: NormalizedAnswers =
    recommendation?.normalized ?? {
      first_name: firstName,
      phone,
      hair_structure:
        typeof answers.hair_structure === "string"
          ? answers.hair_structure
          : "",
      hair_thickness:
        typeof answers.hair_thickness === "string"
          ? answers.hair_thickness
          : "",
      hair_condition: Array.isArray(answers.hair_condition)
        ? (answers.hair_condition as string[])
        : [],
      scalp_status: Array.isArray(answers.scalp_status)
        ? (answers.scalp_status as string[])
        : [],
      hair_treatments:
        typeof answers.hair_treatments === "string"
          ? answers.hair_treatments
          : "",
      heat_frequency:
        typeof answers.heat_frequency === "string"
          ? answers.heat_frequency
          : "",
      wash_frequency:
        typeof answers.wash_frequency === "string"
          ? answers.wash_frequency
          : "",
      care_goals: Array.isArray(answers.care_goals)
        ? (answers.care_goals as string[])
        : [],
      routine_preference:
        typeof answers.routine_preference === "string"
          ? answers.routine_preference
          : "",
      styling_effort:
        typeof answers.styling_effort === "string"
          ? answers.styling_effort
          : "",
    };

  // Routine für Pro-Ansicht + Mail
  const routine: RecommendationProduct[] = hasRealData
    ? [...(recommendation!.final_routine ?? [])].sort(
        (a, b) => (a.anwendungs_schritt ?? 99) - (b.anwendungs_schritt ?? 99),
      )
    : FAKE_ROUTINE;

  // Slots, die in Basic-Ansicht angezeigt werden — abgeleitet aus der Routine
  // (nur Slots, in denen tatsächlich ein Produkt zugeordnet ist).
  const basicSlots = Array.from(
    new Set(routine.map((p) => p.slot_typ ?? "").filter(Boolean)),
  ).sort((a, b) => SLOT_ORDER.indexOf(a) - SLOT_ORDER.indexOf(b));

  const analysisPoints = buildAnalysisPoints(normalized);
  const phoneDisplay = phone && phone.trim() ? phone : "keine Angabe";

  return (
    <main className="relative flex flex-1 flex-col items-center px-4 py-10 md:px-8">
      {/* Diagonales DEMO-Wasserzeichen über der gesamten Seite */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-0 flex items-center justify-center overflow-hidden"
      >
        <div className="grid h-[220vh] w-[220vw] grid-cols-3 gap-x-40 -rotate-[24deg] opacity-[0.07]">
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
            <span aria-hidden="true">⚠</span> Demo-Version · Vorschau für
            das Test-Team
          </div>
          <h1 className="font-serif text-3xl font-semibold text-ink md:text-4xl">
            Danke, {displayName}!
          </h1>
          <p className="max-w-2xl leading-relaxed text-ink-soft">
            Deine Analyse ist durch. Zur Vorschau siehst du gleich beide
            Varianten nebeneinander — links das schlanke{" "}
            <b>Basic</b>-Ergebnis, rechts die volle <b>Pro</b>-Empfehlung.
            Unten die Mail-Kopie, die deine Beraterin bekommt.
          </p>
          {!hasRealData && (
            <p className="text-xs italic text-ink-soft/70">
              Hinweis: n8n-Response-Node ist noch nicht aktiv — es werden
              Beispiel-Produkte gezeigt.
            </p>
          )}
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
              {basicSlots.map((slot) => (
                <BasicRow
                  key={slot}
                  slot={SLOT_LABEL[slot] || slot}
                  bedarf={buildBedarf(slot, normalized)}
                />
              ))}
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
              {routine.map((prod, idx) => (
                <ProRow
                  key={`${prod.produkt_key || idx}-${prod.slot_typ}`}
                  slot={SLOT_LABEL[prod.slot_typ ?? ""] || prod.slot_typ || ""}
                  product={prod.produktname_de || "—"}
                  warum={FAKE_WARUM[prod.slot_typ ?? ""] || "Ideal für deinen Bedarf."}
                />
              ))}
            </div>

            <div className="mt-5 rounded-xl bg-white/70 p-4 text-xs leading-relaxed text-ink-soft ring-1 ring-rosegold/40">
              <b className="text-rosegold-dark">So funktioniert Pro:</b> Die
              Beraterin hat einmalig ihr Sortiment mit Chip-Auswahl gepflegt.
              Ab dann matcht das System bei jeder Analyse automatisch das
              richtige Produkt — mit ihrer Handschrift bei der
              Verkaufsbegründung.
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
                <span className="text-ink">deine.beraterin@example.com</span>
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
              <p>Hallo,</p>
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
                  <div>📱 {phoneDisplay}</div>
                </div>
              </div>

              {analysisPoints.length > 0 && (
                <div className="rounded-xl bg-blush/20 p-4 text-xs">
                  <div className="mb-2 font-semibold uppercase tracking-widest text-rosegold-dark">
                    Analyse-Kernpunkte
                  </div>
                  <ul className="ml-4 list-disc space-y-1 text-ink">
                    {analysisPoints.map((point, i) => (
                      <li key={i}>{point}</li>
                    ))}
                  </ul>
                </div>
              )}

              {routine.length > 0 && (
                <div className="rounded-xl bg-blush/20 p-4 text-xs">
                  <div className="mb-2 font-semibold uppercase tracking-widest text-rosegold-dark">
                    Empfehlung aus deiner Bibliothek
                  </div>
                  <ol className="ml-4 list-decimal space-y-1 text-ink">
                    {routine.map((prod, i) => (
                      <li key={i}>{prod.produktname_de}</li>
                    ))}
                  </ol>
                </div>
              )}

              <p>
                Direktlink zur vollständigen Empfehlung im Portal:{" "}
                <span className="underline text-rosegold-dark">
                  portal.myglowmatch.de/kundinnen/
                  {(firstName || "kundin").toLowerCase()}
                </span>
              </p>

              <p className="text-xs text-ink-soft/70">
                — Diese Mail wird automatisch generiert und ist Teil deines
                myglowmatch-Zugangs.
              </p>
            </div>
          </div>
        </div>

        {/* Hinweis + zurück zur Vorschau */}
        <div className="mt-10 rounded-2xl bg-blush/30 p-6 text-center">
          <p className="text-sm leading-relaxed text-ink">
            <b className="text-rosegold-dark">Wichtig:</b> Diese Ansicht ist
            eine Demo-Vorschau. In der finalen Version sieht die Kundin nur
            eine der beiden Ansichten — je nachdem, welchen Tarif ihre
            Beraterin gebucht hat.
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
