// =====================================================================
// ContactFields – Eingabefelder für Frage 12: Vorname, E-Mail, Telefon.
//
// Vorname + E-Mail = Pflicht.
// Telefon = optional (leer = ok; ungültige Zeichen sperren "Weiter").
// =====================================================================

import { isValidEmail, isValidPhone } from "@/lib/validation";

type ContactFieldsProps = {
  // Texte (kommen aus questions.ts -> ContactStep)
  firstNameLabel: string;
  emailLabel: string;
  phoneLabel: string;
  phoneDescription: string;
  phonePlaceholder: string;
  // aktuelle Werte
  firstName: string;
  email: string;
  phone: string;
  // setzt einen Wert in answers (Field, String)
  onChange: (field: string, value: string) => void;
};

export default function ContactFields({
  firstNameLabel,
  emailLabel,
  phoneLabel,
  phoneDescription,
  phonePlaceholder,
  firstName,
  email,
  phone,
  onChange,
}: ContactFieldsProps) {
  // gemeinsame Stil-Klassen für alle Eingabefelder
  const inputClass =
    "mt-2 w-full rounded-2xl border border-blush bg-white px-4 py-3 text-ink outline-none transition focus:border-rosegold";

  // Inline-Fehler nur zeigen, wenn etwas eingegeben wurde, das ungültig ist.
  const showEmailError = email !== "" && !isValidEmail(email);
  const showPhoneError = phone !== "" && !isValidPhone(phone);

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

      {/* E-Mail */}
      <div>
        <label htmlFor="email" className="block text-sm font-medium text-ink">
          {emailLabel}
        </label>
        <input
          id="email"
          type="email"
          autoComplete="email"
          value={email}
          onChange={(event) => onChange("email", event.target.value)}
          className={inputClass}
        />
        {showEmailError && (
          <p className="mt-2 text-sm text-rosegold-dark">
            Bitte gib eine gültige E-Mail-Adresse ein.
          </p>
        )}
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
    </div>
  );
}
