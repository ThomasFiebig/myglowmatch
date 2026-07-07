// =====================================================================
// ContactFields – Eingabefelder für den letzten Schritt:
// Vorname (Pflicht), Telefon (optional), E-Mail-Opt-in (optional) +
// DSGVO-Einwilligung (Pflicht).
//
// Wenn die E-Mail-Opt-in-Checkbox aktiv ist, erscheint das E-Mail-Feld
// darunter und wird zur Pflicht (muss gültig sein).
// =====================================================================

import Link from "next/link";
import { isValidEmail, isValidPhone } from "@/lib/validation";

// Wandelt das Wort "Datenschutzhinweise" im Einwilligungstext in einen
// klickbaren Link auf /datenschutz um.
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

type ContactFieldsProps = {
  firstNameLabel: string;
  phoneLabel: string;
  phoneDescription: string;
  phonePlaceholder: string;
  emailOptInLabel: string;
  emailPlaceholder: string;
  consentText: string;
  firstName: string;
  phone: string;
  email: string;
  wantsEmailCopy: boolean;
  consent: boolean;
  onChange: (field: string, value: string | boolean) => void;
};

export default function ContactFields({
  firstNameLabel,
  phoneLabel,
  phoneDescription,
  phonePlaceholder,
  emailOptInLabel,
  emailPlaceholder,
  consentText,
  firstName,
  phone,
  email,
  wantsEmailCopy,
  consent,
  onChange,
}: ContactFieldsProps) {
  const inputClass =
    "mt-2 w-full rounded-2xl border border-blush bg-white px-4 py-3 text-ink outline-none transition focus:border-rosegold";

  const showPhoneError = phone !== "" && !isValidPhone(phone);
  const showEmailError = wantsEmailCopy && email !== "" && !isValidEmail(email);

  return (
    <div className="flex flex-col gap-5">
      {/* Vorname */}
      <div>
        <label
          htmlFor="first_name"
          className="block text-sm font-medium text-ink"
        >
          {firstNameLabel}
        </label>
        <input
          id="first_name"
          type="text"
          autoComplete="given-name"
          value={firstName}
          onChange={(event) => onChange("first_name", event.target.value)}
          className={inputClass}
        />
      </div>

      {/* Telefon (optional) */}
      <div>
        <label htmlFor="phone" className="block text-sm font-medium text-ink">
          {phoneLabel}
        </label>
        <p className="mt-1 text-xs leading-relaxed text-ink-soft">
          {phoneDescription}
        </p>
        <input
          id="phone"
          type="tel"
          inputMode="tel"
          autoComplete="tel"
          value={phone}
          placeholder={phonePlaceholder}
          onChange={(event) => onChange("phone", event.target.value)}
          className={inputClass}
        />
        {showPhoneError && (
          <p className="mt-2 text-sm text-rosegold-dark">
            Bitte nur Ziffern, +, Leerzeichen oder Bindestriche verwenden.
          </p>
        )}
      </div>

      {/* E-Mail-Opt-in (optional) */}
      <div>
        <label className="flex cursor-pointer gap-3 rounded-2xl bg-white p-4 ring-1 ring-blush">
          <input
            type="checkbox"
            checked={wantsEmailCopy}
            onChange={(event) =>
              onChange("wants_email_copy", event.target.checked)
            }
            className="mt-0.5 h-5 w-5 shrink-0 accent-rosegold"
          />
          <span className="text-sm leading-relaxed text-ink">
            {emailOptInLabel}
          </span>
        </label>
        {wantsEmailCopy && (
          <div className="mt-3">
            <label
              htmlFor="email"
              className="block text-sm font-medium text-ink"
            >
              Deine E-Mail-Adresse
            </label>
            <input
              id="email"
              type="email"
              autoComplete="email"
              value={email}
              placeholder={emailPlaceholder}
              onChange={(event) => onChange("email", event.target.value)}
              className={inputClass}
            />
            {showEmailError && (
              <p className="mt-2 text-sm text-rosegold-dark">
                Bitte gib eine gültige E-Mail-Adresse ein.
              </p>
            )}
          </div>
        )}
      </div>

      {/* Pflicht-Einwilligung DSGVO */}
      <label className="flex cursor-pointer gap-3 rounded-2xl bg-white p-4 ring-1 ring-blush">
        <input
          type="checkbox"
          checked={consent}
          onChange={(event) =>
            onChange("consent_recommendation", event.target.checked)
          }
          className="mt-0.5 h-5 w-5 shrink-0 accent-rosegold"
        />
        <span className="text-sm leading-relaxed text-ink">
          {withDatenschutzLink(consentText)}
        </span>
      </label>
    </div>
  );
}
