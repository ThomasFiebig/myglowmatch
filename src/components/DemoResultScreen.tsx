"use client";

// =====================================================================
// DemoResultScreen — Ergebnisseite für die Demo-Version.
//
// Aufbau wie eine Kundinnen-Mail:
//   1) Persönliche Begrüßung ("Danke, [Name]!") + Body-Text
//   2) Basic + Pro Split-Ansicht mit den echten Empfehlungen
//   3) Beraterinnen-Karte mit Foto + WhatsApp-Button
//   4) Beispielmail an die Beraterin (Vollständiges Layout wie Node 17)
//
// Produkt-Texte kommen echt aus der Produktdatenbank (Feld `anwendung`).
// DEMO-Wasserzeichen als Overlay.
// =====================================================================

import Link from "next/link";
import type {
  Answers,
  NormalizedAnswers,
  RecommendationProduct,
  RecommendationResult,
} from "@/lib/types";

type DemoResultScreenProps = {
  firstName: string;
  phone: string;
  answers: Answers;
  recommendation: RecommendationResult | null;
};

// ---------------------------------------------------------------
// Partner-Datenbank (nachgebildet aus n8n Node 17)
// ---------------------------------------------------------------
type Partner = {
  name: string;
  first_name: string;
  email: string;
  phone: string;
  whatsapp: string;
  title: string;
  initials: string;
  photo_url?: string;
};

const PARTNERS: Record<string, Partner> = {
  desiree: {
    name: "Desirée Fiebig",
    first_name: "Desirée",
    email: "beratung@veradex.de",
    phone: "0175 / 3742698",
    whatsapp: "491753742698",
    title: "Deine MONAT Markenpartnerin",
    initials: "DF",
    photo_url: "/partners/desiree.jpg",
  },
  DEFAULT: {
    name: "Deine Beraterin",
    first_name: "Deine Beraterin",
    email: "info@mybeautykey.de",
    phone: "",
    whatsapp: "",
    title: "MyBeautyKey Beratung",
    initials: "MK",
  },
};

// ---------------------------------------------------------------
// Enum-Labels — deckungsgleich mit n8n Node 17.
// ---------------------------------------------------------------
const LABELS: Record<string, string> = {
  juckend_empfindlich: "juckend / empfindlich",
  schuppig: "schuppig",
  fettig: "fettig",
  trocken: "trocken",
  normal: "normal",
  keine_probleme: "keine besonderen Probleme",
  glatt: "glatt",
  wellig: "wellig",
  lockig: "lockig",
  kraus: "sehr lockig / kraus",
  fein: "fein",
  mittel: "mittel",
  dick: "dick",
  stark_geschaedigt: "stark geschädigt",
  haarbruch: "Haarbruch",
  spliss: "Spliss",
  frizz: "Frizz",
  glanzlos: "glanzlos",
  kraftlos: "kraftlos / wenig Volumen",
  duenn: "dünner werdendes Haar",
  nein: "unbehandelt",
  gefaerbt: "gefärbt",
  blondiert: "blondiert",
  dauergewellt: "dauergewellt",
  geglaettet: "geglättet",
  nie_selten: "nie / sehr selten",
  gelegentlich: "gelegentlich",
  regelmaessig: "regelmäßig",
  taeglich: "täglich",
  nicht_taeglich: "nicht täglich",
  lufttrocknen: "lufttrocknen / minimal",
  leichtes_styling: "leichtes Styling",
  regelmaessiges_styling: "regelmäßiges Styling",
  aufwendiges_styling: "aufwendiges Styling",
  mehr_definition: "mehr Definition",
  mehr_volumen: "mehr Volumen",
  beides: "beides",
  reparatur: "Reparatur",
  mehr_feuchtigkeit: "mehr Feuchtigkeit",
  feuchtigkeit: "mehr Feuchtigkeit",
  weniger_frizz: "weniger Frizz",
  mehr_glanz: "mehr Glanz",
  glanz: "mehr Glanz",
  farb_erhalt: "Farb-Erhalt",
  volumen: "mehr Volumen",
  hitzeschutz: "Hitzeschutz",
  gesunde_kopfhaut: "gesunde Kopfhaut",
  kopfhaut_pflege: "Kopfhaut-Pflege",
  schnellere_haarwaesche: "seltener waschen",
  minimal: "so wenige Produkte wie möglich",
  ausgewogen: "ausgewogene Routine",
  bestmoeglich: "bestmögliches Ergebnis",
  sehr_wenig: "sehr wenig",
  bewusst_regelmaessig: "bewusst & regelmäßig",
};

function label(value: string | undefined | null): string {
  if (!value) return "–";
  return LABELS[value] || value;
}
function labelList(arr: string[] | undefined): string {
  if (!arr || arr.length === 0) return "–";
  return arr.map((v) => label(v)).join(", ");
}

const SLOT_LABEL: Record<string, string> = {
  shampoo: "Shampoo",
  spuelung: "Spülung",
  maske: "Kur / Maske",
  leave_in: "Leave-in",
  styling_1: "Styling",
  styling_2: "Styling (zusätzlich)",
  styling_3: "Styling (zusätzlich)",
  scalp: "Kopfhaut-Pflege",
  serum: "Serum",
  nacht_serum: "Nacht-Serum",
};
const SLOT_ORDER = [
  "shampoo",
  "spuelung",
  "maske",
  "leave_in",
  "scalp",
  "serum",
  "nacht_serum",
  "styling_1",
  "styling_2",
  "styling_3",
];

// ---------------------------------------------------------------
// Body-Textbausteine (deckungsgleich mit Node 17 Kundinnen-Mail)
// ---------------------------------------------------------------
function buildProblemSatz(primary: string | undefined): string {
  switch (primary) {
    case "stark_geschaedigt":
      return "Dein Haar braucht gerade besonders viel Liebe und intensive Pflege – wir haben genau das Richtige für dich zusammengestellt.";
    case "trocken":
      return "Trockenes Haar kennt man – und wie schön, dass du dir jetzt die Zeit nimmst, es wirklich gut zu versorgen.";
    case "haarbruch":
      return "Haarbruch ist oft ein Zeichen, dass das Haar etwas mehr Unterstützung braucht – und genau dabei möchten wir dir helfen.";
    case "frizz":
      return "Frizz kann so nervig sein – aber keine Sorge, wir haben eine Routine für dich, die genau das in den Griff bekommt.";
    case "kraftlos":
      return "Mehr Volumen und Lebendigkeit für dein Haar – das klingt gut, oder? Genau darauf ist deine Routine ausgerichtet.";
    case "duenn":
      return "Dein Haar soll sich wieder voll und kräftig anfühlen – mit der richtigen Pflege ist das absolut möglich.";
    default:
      return "Wir haben uns deine Antworten genau angeschaut und eine Routine zusammengestellt, die wirklich zu dir und deinem Haar passt.";
  }
}
function buildLevelSatz(level: string | undefined): string {
  if (level === "LOW")
    return "Deine Routine ist schön unkompliziert – wenige, dafür wirkungsvolle Produkte, die du schnell in deinen Alltag integrieren kannst.";
  if (level === "HIGH")
    return "Deine Routine ist etwas umfangreicher – aber dein Haar verdient diese intensive Zuwendung, und du wirst den Unterschied sehen und fühlen.";
  return "Deine Routine ist ausgewogen – nicht zu viel, nicht zu wenig. Genau richtig für sichtbare Ergebnisse ohne großen Aufwand.";
}
function buildStrukturSatz(structure: string | undefined): string | null {
  if (structure === "lockig" || structure === "kraus")
    return "Für deine wunderschönen Locken haben wir besonders darauf geachtet, dass jedes Produkt Feuchtigkeit spendet und die Struktur unterstützt.";
  if (structure === "wellig")
    return "Für deine welligen Strähnen haben wir Produkte gewählt, die deine natürliche Textur betonen und gleichzeitig pflegen.";
  if (structure === "glatt")
    return "Für dein glattes Haar haben wir Produkte ausgewählt, die Glanz und Geschmeidigkeit fördern, ohne zu beschweren.";
  return null;
}

// ---------------------------------------------------------------
// Bedarfsprofil pro Slot (für Basic-Ansicht). null = Slot auslassen.
// ---------------------------------------------------------------
function buildBedarf(slotTyp: string, n: NormalizedAnswers): string | null {
  const parts: string[] = [];
  const goals = n.care_goals ?? [];
  const conditions = n.hair_condition ?? [];
  const scalp = n.scalp_status ?? [];
  const structure = n.hair_structure ?? "";
  const thickness = n.hair_thickness ?? "";

  if (slotTyp === "shampoo") {
    if (goals.includes("mehr_feuchtigkeit") || conditions.includes("trocken"))
      parts.push("feuchtigkeitsspendend");
    if (conditions.includes("stark_geschaedigt") || goals.includes("reparatur"))
      parts.push("reparierend");
    if (goals.includes("farb_erhalt") || n.hair_treatments === "gefaerbt")
      parts.push("farb-erhaltend");
    if (goals.includes("mehr_glanz") || conditions.includes("glanzlos"))
      parts.push("Glanz-fördernd");
    if (goals.includes("mehr_volumen") || conditions.includes("kraftlos"))
      parts.push("volumen-gebend");
    if (scalp.includes("fettig")) parts.push("mild-reinigend");
    if (scalp.includes("juckend_empfindlich")) parts.push("kopfhaut-beruhigend");
  } else if (slotTyp === "spuelung") {
    if (conditions.includes("frizz")) parts.push("Frizz-kontrollierend");
    if (["wellig", "lockig", "kraus"].includes(structure)) parts.push("entwirrend");
    if (goals.includes("mehr_feuchtigkeit") || conditions.includes("trocken"))
      parts.push("tief feuchtigkeitsspendend");
    if (goals.includes("reparatur") || conditions.includes("haarbruch"))
      parts.push("stärkend");
  } else if (slotTyp === "maske") {
    if (goals.includes("reparatur") || conditions.includes("stark_geschaedigt"))
      parts.push("intensive Reparatur");
    else if (goals.includes("mehr_feuchtigkeit") || conditions.includes("trocken"))
      parts.push("tiefe Feuchtigkeitskur");
    if (n.hair_treatments === "gefaerbt" || n.hair_treatments === "blondiert")
      parts.push("Coloriertes-Haar-Pflege");
  } else if (slotTyp === "leave_in") {
    if (n.heat_frequency && n.heat_frequency !== "nie_selten")
      parts.push("Hitzeschutz");
    if (conditions.includes("frizz")) parts.push("Frizz-Kontrolle");
    if (goals.includes("mehr_feuchtigkeit") || conditions.includes("trocken"))
      parts.push("Feuchtigkeits-Boost für den Tag");
    if (goals.includes("reparatur") || conditions.includes("haarbruch"))
      parts.push("Bonding-Stärkung");
  } else if (slotTyp === "styling_1" || slotTyp === "styling_2" || slotTyp === "styling_3") {
    if (goals.includes("mehr_volumen") || conditions.includes("kraftlos"))
      parts.push("Volumen ohne Beschwerung");
    if (["lockig", "kraus"].includes(structure)) parts.push("Locken-definierend");
    if (n.curl_priority === "mehr_definition") parts.push("Curl-Definition");
    if (n.heat_frequency && n.heat_frequency !== "nie_selten") parts.push("Hitzeschutz");
    if (conditions.includes("frizz")) parts.push("Frizz-reduzierend");
    if (n.styling_effort === "aufwendiges_styling" || n.styling_effort === "regelmaessiges_styling")
      parts.push("Halt & Formung");
  } else if (slotTyp === "scalp" || slotTyp === "nacht_serum") {
    if (scalp.includes("juckend_empfindlich"))
      parts.push("beruhigend für empfindliche Kopfhaut");
    if (scalp.includes("fettig") || scalp.includes("schnell_nachfettender_ansatz"))
      parts.push("balancierend");
    if (scalp.includes("schuppig")) parts.push("gegen Schuppen");
    if (conditions.includes("duenn")) parts.push("Kopfhaut-Serum für volleres Haar");
  } else if (slotTyp === "serum") {
    if (conditions.includes("spliss") || conditions.includes("haarbruch"))
      parts.push("Spitzen-Pflege gegen Spliss");
    if (conditions.includes("frizz")) parts.push("Anti-Frizz-Serum");
    if (goals.includes("mehr_glanz")) parts.push("Glanz-Serum");
  }

  if (parts.length === 0) return null;

  if (["shampoo", "spuelung", "maske"].includes(slotTyp)) {
    // "für <adjektiv> Haar" grammatikalisch korrekt zusammenbauen.
    // Struktur + Stärke werden zu einem einzigen Adjektiv-Compound:
    //   glatt + fein  → "feines, glattes Haar"
    //   wellig + dick → "dickes, welliges Haar"
    const adjektive: string[] = [];
    if (thickness && thickness !== "mittel") {
      const t = thickness === "fein" ? "feines" : thickness === "dick" ? "dickes" : label(thickness);
      adjektive.push(t);
    }
    if (structure) {
      const s =
        structure === "glatt"
          ? "glattes"
          : structure === "wellig"
            ? "welliges"
            : structure === "lockig"
              ? "lockiges"
              : structure === "kraus"
                ? "krauses"
                : label(structure);
      adjektive.push(s);
    }
    if (adjektive.length) return `${parts.join(", ")} · für ${adjektive.join(", ")} Haar`;
  }
  return parts.join(", ");
}

function buildVerkaufstipp(primary: string | undefined): string {
  switch (primary) {
    case "stark_geschaedigt":
      return 'Sprich konkret das geschädigte Haar an. Beispiel: „Ich habe gesehen, dass dein Haar gerade etwas Unterstützung braucht – mit dem IR Clinical werden wir das Schritt für Schritt aufbauen."';
    case "trocken":
      return 'Beziehe dich auf das trockene Haar. Beispiel: „Trockenes Haar ist so frustrierend – die gute Nachricht ist: Mit der richtigen Feuchtigkeitspflege siehst du schon nach wenigen Wochen einen Unterschied."';
    case "haarbruch":
      return 'Geh auf das Thema Haarbruch ein und vermittle Sicherheit. Beispiel: „Haarbruch kann viele Ursachen haben – wichtig ist eine Routine, die das Haar von innen stärkt."';
    case "frizz":
      return 'Sprich Frizz als Thema an. Beispiel: „Frizz nervt unglaublich – die empfohlene Routine glättet und definiert gleichzeitig."';
    case "kraftlos":
      return 'Beziehe dich auf Volumen. Beispiel: „Volumen ist eine Frage der richtigen Produkte – mit dem verdickenden Shampoo wirst du den Unterschied sofort fühlen."';
    case "duenn":
      return 'Sprich behutsam über Haardichte. Beispiel: „Das Gefühl von dünner werdendem Haar ist sehr persönlich – die empfohlenen Produkte unterstützen die Kopfhaut und sorgen für volleres Haar."';
    default:
      return 'Bedanke dich für ihr Interesse und biete eine persönliche Beratung an. Beispiel: „Schön, dass du die Analyse gemacht hast – wenn du Fragen zu den Produkten hast, melde dich gerne."';
  }
}
function buildLevelTipp(level: string | undefined): string {
  if (level === "LOW")
    return "Sie möchte eine schlanke Routine. Konzentriere dich auf die Hauptprodukte, biete keine Zusatzartikel beim Erstkontakt an.";
  if (level === "HIGH")
    return "Sie ist bereit, in eine umfangreiche Routine zu investieren – ein starkes Kaufsignal. Zeig ihr den vollen Ablauf.";
  return "Eine ausgewogene Routine wurde gewünscht. Du kannst gerne ergänzende Produkte vorschlagen, ohne zu überfordern.";
}

// ---------------------------------------------------------------
// Fake-Fallback-Daten (nur wenn n8n keine Response schickt).
// ---------------------------------------------------------------
const FAKE_ROUTINE: RecommendationProduct[] = [
  {
    produktname_de: "Renew™ Hydrating Shampoo",
    slot_typ: "shampoo",
    anwendungs_schritt: 1,
    anwendung:
      "In den Händen aufemulgieren und auf das nasse Haar und die Kopfhaut auftragen. 2–3 Minuten einwirken lassen.",
  },
  {
    produktname_de: "Erweiterte Feuchtigkeits-Spülung",
    slot_typ: "spuelung",
    anwendungs_schritt: 2,
    anwendung: "Nach dem Shampoo in Längen und Spitzen einarbeiten, kurz einwirken und ausspülen.",
  },
  {
    produktname_de: "Super-Feuchtigkeitsmaske",
    slot_typ: "maske",
    anwendungs_schritt: 3,
    anwendung: "1× wöchentlich statt der Spülung, 5–10 Minuten einwirken lassen.",
  },
  {
    produktname_de: "Bond IQ Leave-in",
    slot_typ: "leave_in",
    anwendungs_schritt: 4,
    anwendung: "Auf handtuchtrockenes Haar sprühen, nicht ausspülen. Föhnen oder lufttrocknen.",
  },
  {
    produktname_de: "Moxie Mousse",
    slot_typ: "styling_1",
    anwendungs_schritt: 5,
    anwendung: "Golfballgroße Menge auf feuchtem Haar verteilen, ansetzen und stylen.",
  },
];

// =====================================================================
// Haupt-Komponente
// =====================================================================
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

  const normalized: NormalizedAnswers =
    recommendation?.normalized ?? {
      first_name: firstName,
      phone,
      hair_structure:
        typeof answers.hair_structure === "string" ? answers.hair_structure : "",
      hair_thickness:
        typeof answers.hair_thickness === "string" ? answers.hair_thickness : "",
      hair_condition: Array.isArray(answers.hair_condition)
        ? (answers.hair_condition as string[])
        : [],
      scalp_status: Array.isArray(answers.scalp_status)
        ? (answers.scalp_status as string[])
        : [],
      hair_treatments:
        typeof answers.hair_treatments === "string" ? answers.hair_treatments : "",
      heat_frequency:
        typeof answers.heat_frequency === "string" ? answers.heat_frequency : "",
      wash_frequency:
        typeof answers.wash_frequency === "string" ? answers.wash_frequency : "",
      care_goals: Array.isArray(answers.care_goals) ? (answers.care_goals as string[]) : [],
      routine_preference:
        typeof answers.routine_preference === "string" ? answers.routine_preference : "",
      styling_effort:
        typeof answers.styling_effort === "string" ? answers.styling_effort : "",
      curl_priority:
        typeof answers.curl_priority === "string" ? answers.curl_priority : null,
      ends_condition:
        typeof answers.ends_condition === "string" ? answers.ends_condition : null,
    };

  const routine: RecommendationProduct[] = hasRealData
    ? [...(recommendation!.final_routine ?? [])].sort(
        (a, b) => (a.anwendungs_schritt ?? 99) - (b.anwendungs_schritt ?? 99),
      )
    : FAKE_ROUTINE;

  const basicRows: Array<{ slot: string; bedarf: string }> = Array.from(
    new Set(routine.map((p) => p.slot_typ ?? "").filter(Boolean)),
  )
    .sort((a, b) => SLOT_ORDER.indexOf(a) - SLOT_ORDER.indexOf(b))
    .map((slot) => ({ slot, bedarf: buildBedarf(slot, normalized) || "" }))
    .filter((r) => r.bedarf.length > 0)
    .map((r) => ({ slot: SLOT_LABEL[r.slot] || r.slot, bedarf: r.bedarf }));

  const primaryCondition =
    recommendation?.priorities?.primary_hair_condition ??
    (normalized.hair_condition && normalized.hair_condition[0]) ??
    "";
  const pflegelevelFinal =
    recommendation?.pflegelevel?.pflegelevel_final ??
    (routine.length >= 6 ? "HIGH" : routine.length >= 4 ? "MID" : "LOW");
  const verkaufstipp = buildVerkaufstipp(primaryCondition);
  const levelTipp = buildLevelTipp(pflegelevelFinal);
  const problemSatz = buildProblemSatz(primaryCondition);
  const levelSatz = buildLevelSatz(pflegelevelFinal);
  const strukturSatz = buildStrukturSatz(normalized.hair_structure);

  const partnerId = recommendation?.partner_id || "DEFAULT";
  const partner = PARTNERS[partnerId] || PARTNERS.DEFAULT;
  const waText = encodeURIComponent(
    `Hallo ${partner.first_name}, ich habe gerade meine Haaranalyse bei MyBeautyKey gemacht und würde gerne mehr zu meinen Produkten erfahren.`,
  );
  const waHref = partner.whatsapp
    ? `https://wa.me/${partner.whatsapp}?text=${waText}`
    : `mailto:${partner.email}`;

  const phoneDisplay = phone && phone.trim() ? phone : "keine Angabe";
  const hasPhone = Boolean(phone && phone.trim());

  return (
    <main className="relative flex flex-1 flex-col items-center px-3 py-6 md:px-8 md:py-10">
      {/* Diagonales DEMO-Wasserzeichen — als Rautenmuster ohne Überlappung */}
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-0 z-0 overflow-hidden"
        style={{
          backgroundImage:
            "repeating-linear-gradient(-24deg, transparent 0 220px, transparent 220px 240px)",
        }}
      >
        <div
          className="absolute inset-0"
          style={{
            transform: "rotate(-24deg) scale(1.4)",
            transformOrigin: "center",
            display: "grid",
            gridTemplateColumns: "repeat(6, 1fr)",
            gap: "80px 100px",
            padding: "40px",
            opacity: 0.09,
            fontFamily: "Georgia, serif",
            fontSize: "56px",
            fontWeight: 700,
            letterSpacing: "0.3em",
            color: "#c98f84",
            textTransform: "uppercase",
            whiteSpace: "nowrap",
            userSelect: "none",
          }}
        >
          {Array.from({ length: 48 }).map((_, i) => (
            <span key={i}>DEMO</span>
          ))}
        </div>
      </div>

      <div className="relative z-10 w-full max-w-3xl">
        {/* Kopfleiste + Demo-Chip */}
        <div className="mb-6 flex flex-col items-center gap-3 text-center">
          <div className="font-serif text-2xl text-ink">MyBeautyKey</div>
          <div className="inline-flex items-center gap-2 rounded-full bg-rosegold/20 px-3 py-1.5 text-[10px] font-semibold uppercase tracking-widest text-rosegold-dark">
            <span aria-hidden="true">⚠</span> Demo · nicht das Endergebnis
          </div>
        </div>

        {/* Persönliche Begrüßung + Body wie in der Kundinnen-Mail */}
        <section className="mb-6 rounded-2xl border border-blush bg-white/95 px-5 py-6 shadow-sm md:px-8">
          <h1 className="mb-4 font-serif text-2xl font-semibold text-ink md:text-3xl">
            Deine persönliche Haaranalyse ist da, {displayName} ✨
          </h1>
          <div className="space-y-3 text-[15px] leading-relaxed text-ink-soft">
            <p>Hallo {displayName},</p>
            <p>wie schön, dass du dir die Zeit genommen hast – jetzt kommt das Ergebnis!</p>
            <p>{problemSatz}</p>
            <p>{levelSatz}</p>
            {strukturSatz && <p>{strukturSatz}</p>}
          </div>
        </section>

        {/* Basic + Pro Split */}
        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-2">
          {/* Basic */}
          <div className="rounded-2xl border border-blush bg-white/95 p-5 shadow-sm">
            <div className="mb-4 flex items-baseline justify-between">
              <h2 className="font-serif text-lg font-semibold text-ink">Basic-Ansicht</h2>
              <span className="rounded-full bg-blush/60 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
                Bedarfsprofil
              </span>
            </div>
            <p className="mb-3 text-xs text-ink-soft">
              Die Beraterin bekommt dieses Profil und empfiehlt dir persönlich
              die passenden Produkte aus ihrer Markenwelt.
            </p>
            <div className="flex flex-col gap-2">
              {basicRows.map((row) => (
                <div
                  key={row.slot}
                  className="rounded-xl border border-blush/60 bg-white p-3"
                >
                  <div className="text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
                    {row.slot}
                  </div>
                  <div className="mt-1 text-[13px] text-ink">{row.bedarf}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Pro */}
          <div className="rounded-2xl border-2 border-rosegold-dark/60 bg-gradient-to-b from-white to-blush/30 p-5 shadow-md">
            <div className="mb-4 flex items-baseline justify-between">
              <h2 className="font-serif text-lg font-semibold text-ink">Pro-Ansicht</h2>
              <span className="rounded-full bg-rosegold-dark px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-white">
                Deine Routine
              </span>
            </div>
            <p className="mb-3 text-xs text-ink-soft">
              Aus dem Sortiment deiner Beraterin — Schritt für Schritt.
            </p>
            <div className="flex flex-col gap-3">
              {routine.map((prod, i) => (
                <div
                  key={`${prod.produkt_key || i}`}
                  className="rounded-xl border border-blush/60 bg-white p-3"
                >
                  <div className="flex items-baseline justify-between gap-2">
                    <span className="rounded-full bg-blush px-2.5 py-0.5 text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
                      Schritt {prod.anwendungs_schritt ?? i + 1}
                    </span>
                    <span className="text-[10px] uppercase tracking-widest text-ink-soft/60">
                      {SLOT_LABEL[prod.slot_typ ?? ""] || prod.slot_typ}
                    </span>
                  </div>
                  <div className="mt-1.5 font-serif text-[15px] font-semibold text-ink">
                    {prod.produktname_de}
                  </div>
                  {prod.anwendung && (
                    <div className="mt-1.5 text-[12.5px] leading-relaxed text-ink-soft">
                      {prod.anwendung}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Beraterinnen-Karte */}
        <section className="mb-6 rounded-2xl border border-blush bg-white px-5 py-5 shadow-sm md:px-8 md:py-6">
          <div className="flex flex-col items-center gap-4 text-center md:flex-row md:items-center md:text-left">
            {partner.photo_url ? (
              // eslint-disable-next-line @next/next/no-img-element
              <img
                src={partner.photo_url}
                alt={partner.name}
                className="h-20 w-20 shrink-0 rounded-full object-cover"
                style={{
                  border: "3px solid #FFFFFF",
                  boxShadow: "0 4px 12px rgba(160, 117, 96, 0.2)",
                }}
              />
            ) : (
              <div
                className="flex h-20 w-20 shrink-0 items-center justify-center rounded-full font-serif text-2xl font-medium text-white"
                style={{
                  background: "linear-gradient(135deg, #D4A593, #A07560)",
                  border: "3px solid #FFFFFF",
                  boxShadow: "0 4px 12px rgba(160, 117, 96, 0.2)",
                }}
              >
                {partner.initials}
              </div>
            )}
            <div className="flex-1">
              <p className="text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
                {partner.title}
              </p>
              <p className="mt-1 font-serif text-xl text-ink">{partner.name}</p>
              {partner.email && (
                <p className="mt-1 text-sm text-ink-soft break-all">
                  {partner.email}
                </p>
              )}
              {partner.phone && (
                <p className="mt-0.5 text-sm text-ink-soft">{partner.phone}</p>
              )}
            </div>
          </div>
          <div className="mt-5 text-center">
            <a
              href={waHref}
              target={partner.whatsapp ? "_blank" : undefined}
              rel="noreferrer"
              className="inline-flex items-center gap-2 rounded-full bg-[#25D366] px-6 py-3 text-sm font-semibold text-white shadow-md transition hover:bg-[#22b459]"
            >
              💬 &nbsp; Per WhatsApp anschreiben
            </a>
          </div>
        </section>

        {/* Zwischen-Info: das war der Kundinnen-Blick */}
        <div className="mb-6 rounded-xl border border-dashed border-rosegold-dark/40 bg-white/70 p-4 text-center text-xs italic text-ink-soft">
          ↑ So sieht deine Kundin ihre Empfehlung im Browser. ↓ Zusätzlich
          bekommst du als Beraterin diese Mail:
        </div>

        {/* Original Beraterinnen-Mail-Preview */}
        <section className="mb-6 overflow-hidden rounded-2xl border border-blush bg-white shadow-md">
          <div className="border-b border-blush bg-[#FBF5EE] px-4 py-3 text-[11px] md:px-6">
            <div className="flex gap-2">
              <span className="w-14 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                Von
              </span>
              <span className="text-ink">MyBeautyKey &lt;beratung@mybeautykey.de&gt;</span>
            </div>
            <div className="mt-0.5 flex gap-2">
              <span className="w-14 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                An
              </span>
              <span className="text-ink break-all">{partner.email}</span>
            </div>
            <div className="mt-0.5 flex gap-2">
              <span className="w-14 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                Betreff
              </span>
              <span className="font-semibold text-ink">
                🎉 Neuer Lead via MyBeautyKey: {displayName}
              </span>
            </div>
          </div>
          <div
            className="px-4 py-5 md:px-6"
            style={{ fontFamily: "Helvetica, Arial, sans-serif" }}
          >
            <h3
              className="text-center"
              style={{
                fontFamily: "Georgia, serif",
                fontSize: "20px",
                color: "#2D2A26",
                fontWeight: 600,
                margin: "0 0 6px",
              }}
            >
              Neuer Lead via MyBeautyKey
            </h3>
            <p
              className="text-center"
              style={{
                fontSize: "13px",
                color: "#5C5651",
                margin: "0 0 20px",
                lineHeight: 1.6,
              }}
            >
              {displayName} hat soeben deinen Fragebogen ausgefüllt.
            </p>

            <div
              style={{
                background: "#FFFFFF",
                border: "1px solid #EFE5DC",
                borderRadius: "14px",
                padding: "16px 18px",
                marginBottom: "16px",
              }}
            >
              <p
                style={{
                  margin: "0 0 6px",
                  fontSize: "10px",
                  fontWeight: 700,
                  letterSpacing: "1.5px",
                  color: "#A07560",
                  textTransform: "uppercase",
                }}
              >
                Kontakt
              </p>
              <p style={{ margin: "3px 0", fontSize: "14px", color: "#2D2A26", fontWeight: 600 }}>
                {displayName}
              </p>
              <p style={{ margin: "3px 0", fontSize: "13px", color: "#5C5651" }}>
                Telefon: {phoneDisplay}
                {hasPhone && (
                  <span
                    style={{
                      display: "inline-block",
                      marginLeft: "8px",
                      background: "#25D366",
                      color: "#FFF",
                      padding: "2px 9px",
                      borderRadius: "12px",
                      fontSize: "10.5px",
                      fontWeight: 600,
                    }}
                  >
                    → WhatsApp
                  </span>
                )}
              </p>
            </div>

            <p
              style={{
                margin: "0 0 8px",
                fontSize: "10px",
                fontWeight: 700,
                letterSpacing: "1.5px",
                color: "#A07560",
                textTransform: "uppercase",
              }}
            >
              Ihre Antworten
            </p>
            <table className="w-full" style={{ fontSize: "12.5px" }}>
              <tbody>
                {AnswerRow("Struktur", label(normalized.hair_structure))}
                {AnswerRow("Stärke", label(normalized.hair_thickness))}
                {AnswerRow("Zustand", labelList(normalized.hair_condition))}
                {AnswerRow("Kopfhaut", labelList(normalized.scalp_status))}
                {AnswerRow("Behandlungen", label(normalized.hair_treatments))}
                {AnswerRow("Hitze-Styling", label(normalized.heat_frequency))}
                {AnswerRow("Waschfrequenz", label(normalized.wash_frequency))}
                {AnswerRow("Styling-Aufwand", label(normalized.styling_effort))}
                {AnswerRow("Ziele", labelList(normalized.care_goals), true)}
              </tbody>
            </table>

            <p
              style={{
                margin: "20px 0 8px",
                fontSize: "10px",
                fontWeight: 700,
                letterSpacing: "1.5px",
                color: "#A07560",
                textTransform: "uppercase",
              }}
            >
              Empfohlene Produkte
            </p>
            <div>
              {routine.map((prod, i) => (
                <div
                  key={`m-${i}`}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "10px",
                    padding: "9px 0",
                    borderBottom: i < routine.length - 1 ? "1px solid #EFE5DC" : "none",
                  }}
                >
                  <span
                    style={{
                      background: "#F5E6DC",
                      color: "#7A5641",
                      fontSize: "9.5px",
                      fontWeight: 700,
                      letterSpacing: "1px",
                      padding: "3px 8px",
                      borderRadius: "12px",
                      whiteSpace: "nowrap",
                    }}
                  >
                    Schritt {prod.anwendungs_schritt ?? i + 1}
                  </span>
                  <span style={{ fontSize: "13px", color: "#2D2A26", fontWeight: 600 }}>
                    {prod.produktname_de}
                  </span>
                </div>
              ))}
            </div>

            <div
              style={{
                marginTop: "20px",
                background: "#FBF5EE",
                borderRadius: "14px",
                padding: "18px 20px",
              }}
            >
              <p
                style={{
                  margin: "0 0 8px",
                  fontSize: "10px",
                  fontWeight: 700,
                  letterSpacing: "1.5px",
                  color: "#A07560",
                  textTransform: "uppercase",
                }}
              >
                💡 Profi-Tipp für deinen Erstkontakt
              </p>
              <p style={{ margin: "0 0 10px", fontSize: "13px", lineHeight: 1.6, color: "#3D3935" }}>
                {verkaufstipp}
              </p>
              <p
                style={{
                  margin: 0,
                  fontSize: "12.5px",
                  lineHeight: 1.6,
                  color: "#5C5651",
                  fontStyle: "italic",
                }}
              >
                {levelTipp}
              </p>
            </div>

            <p
              style={{
                margin: "20px 0 8px",
                fontSize: "10px",
                fontWeight: 700,
                letterSpacing: "1.5px",
                color: "#A07560",
                textTransform: "uppercase",
              }}
            >
              Nächste Schritte
            </p>
            <ol
              style={{
                paddingLeft: "22px",
                fontSize: "13px",
                color: "#3D3935",
                lineHeight: 1.7,
                margin: 0,
                listStyleType: "decimal",
                listStylePosition: "outside",
              }}
            >
              <li style={{ paddingLeft: "4px" }}>
                {displayName} hat die Empfehlung gerade im Browser bekommen.
              </li>
              <li style={{ paddingLeft: "4px" }}>
                In der Ergebnisseite ist ein WhatsApp-Button zu dir — sie kann sich
                direkt melden.
              </li>
              <li style={{ paddingLeft: "4px" }}>
                {hasPhone
                  ? `Tipp: ${displayName} hat ihre Nummer hinterlegt — du kannst sie direkt per WhatsApp kontaktieren.`
                  : `Falls sie sich nicht in 24h meldet: schreib ihr aktiv an. Das ist deine Conversion-Chance.`}
              </li>
            </ol>
          </div>
        </section>

        <div className="rounded-xl bg-blush/30 p-4 text-center text-xs italic text-ink-soft">
          Diese Ansicht ist eine Demo-Vorschau. Produktdaten kommen aus der
          echten Produktdatenbank, Layout ist im Aufbau.{" "}
          <Link href="/team" className="underline underline-offset-2">
            Zurück zur Vorschau-Landing
          </Link>
        </div>
      </div>
    </main>
  );
}

function AnswerRow(labelText: string, value: string, isLast = false) {
  const border = isLast ? "" : "1px solid #EFE5DC";
  return (
    <tr key={labelText}>
      <td
        style={{
          padding: "5px 0",
          borderBottom: border,
          width: "42%",
          verticalAlign: "top",
          color: "#5C5651",
          fontWeight: 600,
        }}
      >
        {labelText}
      </td>
      <td
        style={{
          padding: "5px 0",
          borderBottom: border,
          verticalAlign: "top",
          color: "#3D3935",
        }}
      >
        {value}
      </td>
    </tr>
  );
}
