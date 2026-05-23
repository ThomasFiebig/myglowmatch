// =====================================================================
// ConsentFields – die zwei DSGVO-Checkboxen für Frage 13.
//
// props:
//  recommendationText / marketingText = die Einwilligungs-Texte
//  recommendation / marketing         = ob die Checkbox angehakt ist
//  onChange                           = wird mit (Feldname, true/false) aufgerufen
// =====================================================================

import Link from "next/link";

// Wandelt das Wort "Datenschutzhinweise" im Einwilligungstext in einen
// klickbaren Link auf /datenschutz um. stopPropagation verhindert,
// dass der Klick aufs Wort das umgebende Label (Checkbox) toggelt.
function withDatenschutzLink(text: string) {
  const word = "Datenschutzhinweise";
  const index = text.indexOf(word);
  if (index === -1) return text;
  return (
    <>
      {text.slice(0, index)}
      <Link
        href="/datenschutz"
        onClick={(event) => event.stopPropagation()}
        className="underline underline-offset-2 hover:text-rosegold-dark"
      >
        {word}
      </Link>
      {text.slice(index + word.length)}
    </>
  );
}

type ConsentFieldsProps = {
  recommendationText: string;
  marketingText: string;
  recommendation: boolean;
  marketing: boolean;
  onChange: (field: string, value: boolean) => void;
};

export default function ConsentFields({
  recommendationText,
  marketingText,
  recommendation,
  marketing,
  onChange,
}: ConsentFieldsProps) {
  return (
    <div className="flex flex-col gap-4">
      {/* Pflicht-Einwilligung */}
      <label className="flex cursor-pointer gap-3 rounded-2xl bg-white p-4 ring-1 ring-blush">
        <input
          type="checkbox"
          checked={recommendation}
          onChange={(event) =>
            onChange("consent_recommendation", event.target.checked)
          }
          className="mt-0.5 h-5 w-5 shrink-0 accent-rosegold"
        />
        <span className="text-sm leading-relaxed text-ink">
          {withDatenschutzLink(recommendationText)}
        </span>
      </label>

      {/* optionale Einwilligung */}
      <label className="flex cursor-pointer gap-3 rounded-2xl bg-white p-4 ring-1 ring-blush">
        <input
          type="checkbox"
          checked={marketing}
          onChange={(event) =>
            onChange("consent_marketing", event.target.checked)
          }
          className="mt-0.5 h-5 w-5 shrink-0 accent-rosegold"
        />
        <span className="text-sm leading-relaxed text-ink">
          {marketingText}
        </span>
      </label>
    </div>
  );
}
