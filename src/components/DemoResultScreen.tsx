"use client";

// =====================================================================
// DemoResultScreen — Vorschau-Ergebnisseite für die Test-Version.
//
// Zeigt zwei Ergebnis-Ansichten (Basic links: Bedarfsprofil, Pro rechts:
// konkrete Produkte) plus eine originalgetreue Vorschau der Beraterin-
// Mail. Wenn n8n via Respond-to-Webhook-Node echte Daten liefert, wird
// dynamisch gerendert. Sonst Fake-Fallback.
//
// Wasserzeichen "DEMO" liegt semi-transparent über allem.
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
// Deckt sich mit der `readable()`-Funktion in n8n Node 17, damit die
// Antworten-Tabelle in der Mail-Vorschau identisch klingt.
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
  weich_normal: "weich und normal",
  leicht_trocken: "leicht trocken",
  deutlich_trocken: "deutlich trocken / spröde",
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
  frizz_reduktion: "weniger Frizz",
  mehr_glanz: "mehr Glanz",
  glanz: "mehr Glanz",
  farb_erhalt: "Farb-Erhalt",
  volumen: "mehr Volumen",
  hitzeschutz: "Hitzeschutz",
  gesunde_kopfhaut: "gesunde Kopfhaut",
  kopfhaut_pflege: "Kopfhaut-Pflege",
  schnellere_haarwaesche: "seltener waschen",
  verdichtend: "volleres Haar",
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

// ---------------------------------------------------------------
// Slot-Typ → menschenlesbarer Slot-Label + Sortier-Reihenfolge.
// ---------------------------------------------------------------
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
// Bedarfsprofil pro Slot ableiten (für Basic-Ansicht).
// Liefert null zurück, wenn kein spezifischer Bedarf ableitbar ist —
// dann wird der Slot in der Ansicht ausgelassen.
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
    if (
      conditions.includes("stark_geschaedigt") ||
      goals.includes("reparatur")
    )
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
    if (["wellig", "lockig", "kraus"].includes(structure))
      parts.push("entwirrend");
    if (goals.includes("mehr_feuchtigkeit") || conditions.includes("trocken"))
      parts.push("tief feuchtigkeitsspendend");
    if (goals.includes("reparatur") || conditions.includes("haarbruch"))
      parts.push("stärkend");
  } else if (slotTyp === "maske") {
    if (goals.includes("reparatur") || conditions.includes("stark_geschaedigt"))
      parts.push("intensive Reparatur");
    else if (
      goals.includes("mehr_feuchtigkeit") ||
      conditions.includes("trocken")
    )
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
  } else if (
    slotTyp === "styling_1" ||
    slotTyp === "styling_2" ||
    slotTyp === "styling_3"
  ) {
    if (goals.includes("mehr_volumen") || conditions.includes("kraftlos"))
      parts.push("Volumen ohne Beschwerung");
    if (["lockig", "kraus"].includes(structure))
      parts.push("Locken-definierend");
    if (n.curl_priority === "mehr_definition") parts.push("Curl-Definition");
    if (n.heat_frequency && n.heat_frequency !== "nie_selten")
      parts.push("Hitzeschutz");
    if (conditions.includes("frizz")) parts.push("Frizz-reduzierend");
    if (
      n.styling_effort === "aufwendiges_styling" ||
      n.styling_effort === "regelmaessiges_styling"
    )
      parts.push("Halt & Formung");
  } else if (slotTyp === "scalp" || slotTyp === "nacht_serum") {
    if (scalp.includes("juckend_empfindlich"))
      parts.push("beruhigend für empfindliche Kopfhaut");
    if (scalp.includes("fettig") || scalp.includes("schnell_nachfettender_ansatz"))
      parts.push("balancierend");
    if (scalp.includes("schuppig")) parts.push("gegen Schuppen");
    if (conditions.includes("duenn"))
      parts.push("Kopfhaut-Serum für volleres Haar");
  } else if (slotTyp === "serum") {
    if (conditions.includes("spliss") || conditions.includes("haarbruch"))
      parts.push("Spitzen-Pflege gegen Spliss");
    if (conditions.includes("frizz")) parts.push("Anti-Frizz-Serum");
    if (goals.includes("mehr_glanz")) parts.push("Glanz-Serum");
  }

  if (parts.length === 0) return null;

  // Struktur/Stärke nur bei Waschprodukten anhängen (dort ist es wirklich
  // relevant für die Passung).
  if (["shampoo", "spuelung", "maske"].includes(slotTyp)) {
    const suffix: string[] = [];
    if (structure) suffix.push(`${label(structure)}es Haar`);
    if (thickness && thickness !== "mittel") {
      const t =
        thickness === "fein" ? "feinem" : thickness === "dick" ? "dickem" : label(thickness);
      suffix.push(`${t}${suffix.length ? "" : " Haar"}`);
    }
    if (suffix.length) return `${parts.join(", ")} · für ${suffix.join(", ")}`;
  }

  return parts.join(", ");
}

// ---------------------------------------------------------------
// Verkaufstipp aus hauptproblem — deckungsgleich mit Node 17.
// ---------------------------------------------------------------
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
// Fake-Fallback-Daten (wenn n8n keine Response liefert).
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
        typeof answers.hair_treatments === "string"
          ? answers.hair_treatments
          : "",
      heat_frequency:
        typeof answers.heat_frequency === "string" ? answers.heat_frequency : "",
      wash_frequency:
        typeof answers.wash_frequency === "string" ? answers.wash_frequency : "",
      care_goals: Array.isArray(answers.care_goals)
        ? (answers.care_goals as string[])
        : [],
      routine_preference:
        typeof answers.routine_preference === "string"
          ? answers.routine_preference
          : "",
      styling_effort:
        typeof answers.styling_effort === "string" ? answers.styling_effort : "",
      curl_priority:
        typeof answers.curl_priority === "string"
          ? answers.curl_priority
          : null,
      ends_condition:
        typeof answers.ends_condition === "string"
          ? answers.ends_condition
          : null,
    };

  const routine: RecommendationProduct[] = hasRealData
    ? [...(recommendation!.final_routine ?? [])].sort(
        (a, b) => (a.anwendungs_schritt ?? 99) - (b.anwendungs_schritt ?? 99),
      )
    : FAKE_ROUTINE;

  // Basic: nur Slots mit ableitbarem konkretem Bedarf. Slots ohne
  // spezifisches Profil (buildBedarf === null) werden ausgelassen.
  const basicRows: Array<{ slot: string; bedarf: string }> = Array.from(
    new Set(routine.map((p) => p.slot_typ ?? "").filter(Boolean)),
  )
    .sort((a, b) => SLOT_ORDER.indexOf(a) - SLOT_ORDER.indexOf(b))
    .map((slot) => ({ slot, bedarf: buildBedarf(slot, normalized) || "" }))
    .filter((r) => r.bedarf.length > 0)
    .map((r) => ({ slot: SLOT_LABEL[r.slot] || r.slot, bedarf: r.bedarf }));

  // Verkaufstipp aus n8n-priorities oder aus der ersten hair_condition.
  const primaryCondition =
    recommendation?.priorities?.primary_hair_condition ??
    (normalized.hair_condition && normalized.hair_condition[0]) ??
    "";
  const verkaufstipp = buildVerkaufstipp(primaryCondition);
  const pflegelevelFinal =
    recommendation?.pflegelevel?.pflegelevel_final ??
    (routine.length >= 6 ? "HIGH" : routine.length >= 4 ? "MID" : "LOW");
  const levelTipp = buildLevelTipp(pflegelevelFinal);

  const phoneDisplay = phone && phone.trim() ? phone : "keine Angabe";
  const hasPhone = Boolean(phone && phone.trim());

  return (
    <main className="relative flex flex-1 flex-col items-center px-4 py-10 md:px-8">
      {/* Diagonales DEMO-Wasserzeichen */}
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
            Varianten nebeneinander — links das schlanke <b>Basic</b>-Ergebnis,
            rechts die volle <b>Pro</b>-Empfehlung. Unten die Original-Mail,
            die deine Beraterin bekommt.
          </p>
          {!hasRealData && (
            <p className="text-xs italic text-ink-soft/70">
              Hinweis: n8n-Response-Node ist noch nicht aktiv — es werden
              Beispiel-Produkte gezeigt.
            </p>
          )}
        </div>

        {/* Zwei-Spalten: Basic + Pro */}
        <div className="grid grid-cols-1 gap-6 md:grid-cols-2">
          {/* -------- BASIC -------- */}
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
              Beraterin ordnet dir konkrete Produkte aus ihrem Sortiment zu:
            </p>
            <div className="flex flex-col gap-3">
              {basicRows.map((row) => (
                <BasicRow key={row.slot} slot={row.slot} bedarf={row.bedarf} />
              ))}
            </div>
            <div className="mt-5 rounded-xl bg-blush/40 p-4 text-xs leading-relaxed text-ink-soft">
              <b className="text-rosegold-dark">So funktioniert Basic:</b> Die
              Beraterin bekommt dieses Profil und empfiehlt dir persönlich per
              WhatsApp die passenden Produkte aus ihrer Markenwelt.
            </div>
          </div>

          {/* -------- PRO -------- */}
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
                  warum={
                    FAKE_WARUM[prod.slot_typ ?? ""] ||
                    "Ideal für deinen individuellen Bedarf."
                  }
                />
              ))}
            </div>
            <div className="mt-5 rounded-xl bg-white/70 p-4 text-xs leading-relaxed text-ink-soft ring-1 ring-rosegold/40">
              <b className="text-rosegold-dark">So funktioniert Pro:</b> Die
              Beraterin hat einmalig ihr Sortiment mit Chip-Auswahl gepflegt.
              Ab dann matcht das System bei jeder Analyse automatisch das
              richtige Produkt.
            </div>
          </div>
        </div>

        {/* ================================================== */}
        {/* Original-Mail an die Beraterin */}
        {/* ================================================== */}
        <div className="mt-10">
          <div className="mb-4 flex items-center gap-3">
            <div className="h-px flex-1 bg-blush" />
            <span className="text-xs font-semibold uppercase tracking-widest text-rosegold-dark">
              Original · Beratungsmail an die Beraterin
            </span>
            <div className="h-px flex-1 bg-blush" />
          </div>

          <div className="mx-auto max-w-2xl overflow-hidden rounded-2xl border border-blush bg-white shadow-md">
            {/* Mail-Header (Von/An/Betreff) */}
            <div className="border-b border-blush bg-[#FBF5EE] px-6 py-4 text-xs">
              <div className="flex gap-3">
                <span className="w-16 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                  Von
                </span>
                <span className="text-ink">
                  myglowmatch &lt;beratung@myglowmatch.de&gt;
                </span>
              </div>
              <div className="mt-1 flex gap-3">
                <span className="w-16 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                  An
                </span>
                <span className="text-ink">deine Beraterin</span>
              </div>
              <div className="mt-1 flex gap-3">
                <span className="w-16 shrink-0 font-bold uppercase tracking-widest text-rosegold-dark">
                  Betreff
                </span>
                <span className="font-semibold text-ink">
                  🎉 Neuer Lead via myglowmatch: {displayName}
                </span>
              </div>
            </div>

            {/* Mail-Body — nachgebaut nach Node 17 */}
            <div
              className="px-6 py-6"
              style={{ fontFamily: "Helvetica, Arial, sans-serif" }}
            >
              {/* Headline */}
              <h3
                className="text-center"
                style={{
                  fontFamily: "Georgia, serif",
                  fontSize: "22px",
                  color: "#2D2A26",
                  fontWeight: 600,
                  margin: "0 0 6px",
                }}
              >
                Neuer Lead via myglowmatch
              </h3>
              <p
                className="text-center"
                style={{
                  fontSize: "13px",
                  color: "#5C5651",
                  margin: "0 0 24px",
                  lineHeight: 1.6,
                }}
              >
                {displayName} hat soeben deinen Fragebogen ausgefüllt.
              </p>

              {/* Kontakt-Karte */}
              <div
                style={{
                  background: "#FFFFFF",
                  border: "1px solid #EFE5DC",
                  borderRadius: "14px",
                  padding: "18px 20px",
                  marginBottom: "18px",
                }}
              >
                <p
                  style={{
                    margin: "0 0 8px",
                    fontSize: "11px",
                    fontWeight: 700,
                    letterSpacing: "1.5px",
                    color: "#A07560",
                    textTransform: "uppercase",
                  }}
                >
                  Kontakt
                </p>
                <p
                  style={{
                    margin: "4px 0",
                    fontSize: "15px",
                    color: "#2D2A26",
                    fontWeight: 600,
                  }}
                >
                  {displayName}
                </p>
                <p
                  style={{ margin: "4px 0", fontSize: "14px", color: "#5C5651" }}
                >
                  Telefon: {phoneDisplay}
                  {hasPhone && (
                    <span
                      style={{
                        display: "inline-block",
                        marginLeft: "8px",
                        background: "#25D366",
                        color: "#FFF",
                        padding: "2px 10px",
                        borderRadius: "12px",
                        fontSize: "11px",
                        fontWeight: 600,
                      }}
                    >
                      → Per WhatsApp antworten
                    </span>
                  )}
                </p>
              </div>

              {/* Antworten-Tabelle */}
              <p
                style={{
                  margin: "0 0 10px",
                  fontSize: "11px",
                  fontWeight: 700,
                  letterSpacing: "1.5px",
                  color: "#A07560",
                  textTransform: "uppercase",
                }}
              >
                Ihre Antworten
              </p>
              <table className="w-full" style={{ fontSize: "13.5px" }}>
                <tbody>
                  {AnswerRow("Struktur", label(normalized.hair_structure))}
                  {AnswerRow("Stärke", label(normalized.hair_thickness))}
                  {AnswerRow(
                    "Zustand",
                    labelList(normalized.hair_condition),
                  )}
                  {AnswerRow("Kopfhaut", labelList(normalized.scalp_status))}
                  {AnswerRow(
                    "Behandlungen",
                    label(normalized.hair_treatments),
                  )}
                  {AnswerRow("Hitze-Styling", label(normalized.heat_frequency))}
                  {AnswerRow(
                    "Waschfrequenz",
                    label(normalized.wash_frequency),
                  )}
                  {AnswerRow(
                    "Styling-Aufwand",
                    label(normalized.styling_effort),
                  )}
                  {AnswerRow("Ziele", labelList(normalized.care_goals), true)}
                </tbody>
              </table>

              {/* Empfohlene Produkte */}
              <p
                style={{
                  margin: "24px 0 10px",
                  fontSize: "11px",
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
                      padding: "10px 0",
                      borderBottom:
                        i < routine.length - 1 ? "1px solid #EFE5DC" : "none",
                    }}
                  >
                    <span
                      style={{
                        background: "#F5E6DC",
                        color: "#7A5641",
                        fontSize: "10px",
                        fontWeight: 700,
                        letterSpacing: "1px",
                        padding: "3px 8px",
                        borderRadius: "12px",
                        whiteSpace: "nowrap",
                      }}
                    >
                      Schritt {prod.anwendungs_schritt ?? i + 1}
                    </span>
                    <span
                      style={{
                        fontSize: "14px",
                        color: "#2D2A26",
                        fontWeight: 600,
                      }}
                    >
                      {prod.produktname_de}
                    </span>
                  </div>
                ))}
              </div>

              {/* Profi-Tipp */}
              <div
                style={{
                  marginTop: "24px",
                  background: "#FBF5EE",
                  borderRadius: "14px",
                  padding: "20px 22px",
                }}
              >
                <p
                  style={{
                    margin: "0 0 10px",
                    fontSize: "11px",
                    fontWeight: 700,
                    letterSpacing: "1.5px",
                    color: "#A07560",
                    textTransform: "uppercase",
                  }}
                >
                  💡 Profi-Tipp für deinen Erstkontakt
                </p>
                <p
                  style={{
                    margin: "0 0 12px",
                    fontSize: "14px",
                    lineHeight: 1.6,
                    color: "#3D3935",
                  }}
                >
                  {verkaufstipp}
                </p>
                <p
                  style={{
                    margin: 0,
                    fontSize: "13px",
                    lineHeight: 1.6,
                    color: "#5C5651",
                    fontStyle: "italic",
                  }}
                >
                  {levelTipp}
                </p>
              </div>

              {/* Nächste Schritte */}
              <p
                style={{
                  margin: "24px 0 10px",
                  fontSize: "11px",
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
                  paddingLeft: "18px",
                  fontSize: "14px",
                  color: "#3D3935",
                  lineHeight: 1.7,
                  margin: 0,
                }}
              >
                <li>
                  {displayName} hat die Empfehlung gerade im Browser bekommen.
                </li>
                <li>
                  In der Ergebnisseite ist ein WhatsApp-Button zu dir — sie kann
                  sich direkt melden.
                </li>
                <li>
                  {hasPhone
                    ? `Tipp: ${displayName} hat ihre Nummer hinterlegt — du kannst sie direkt per WhatsApp kontaktieren.`
                    : `Falls sie sich nicht in 24h meldet: schreib ihr aktiv an. Das ist deine Conversion-Chance.`}
                </li>
              </ol>

              {/* Footer */}
              <p
                className="text-center"
                style={{
                  margin: "28px 0 0",
                  fontSize: "11px",
                  color: "#8C857F",
                  lineHeight: 1.7,
                }}
              >
                Diese E-Mail wurde automatisch durch myglowmatch generiert, da
                eine Kundin den Fragebogen über deinen Partner-Link ausgefüllt
                hat.
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
      <div>
        <div className="text-[10px] font-bold uppercase tracking-widest text-rosegold-dark">
          {slot}
        </div>
        <div className="mt-0.5 font-serif text-base font-semibold text-ink">
          {product}
        </div>
      </div>
      <div className="mt-2 text-xs italic leading-relaxed text-ink-soft">
        &bdquo;{warum}&ldquo;
      </div>
    </div>
  );
}

// ------------------------------------------------------------
// Ihre-Antworten-Zeile (JSX-Helper für die Mail-Tabelle)
// ------------------------------------------------------------
function AnswerRow(labelText: string, value: string, isLast = false) {
  const border = isLast ? "" : "1px solid #EFE5DC";
  return (
    <tr key={labelText}>
      <td
        style={{
          padding: "6px 0",
          borderBottom: border,
          width: "40%",
          verticalAlign: "top",
          color: "#5C5651",
          fontWeight: 600,
        }}
      >
        {labelText}
      </td>
      <td
        style={{
          padding: "6px 0",
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
