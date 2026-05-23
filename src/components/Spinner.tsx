// =====================================================================
// Spinner – kleiner Lade-Kreisel.
// Reine CSS-Animation (Tailwinds animate-spin) – sehr performant.
// =====================================================================

export default function Spinner() {
  return (
    <span
      aria-hidden="true"
      className="h-4 w-4 animate-spin rounded-full border-2 border-ink/30 border-t-ink"
    />
  );
}
