// =====================================================================
// Dynamische Route für Partner-URLs: /maria, /peter, /martina ...
//
// Der Ordnername [partner] (mit eckigen Klammern) macht aus diesem
// URL-Teil eine Variable. Diese EINE Datei bedient also alle Partner.
// =====================================================================

import Questionnaire from "@/components/Questionnaire";

type PartnerPageProps = {
  // In Next.js 16 kommen die Routen-Parameter als "Promise" (Versprechen)
  // an – wir müssen sie mit await auspacken.
  params: Promise<{ partner: string }>;
};

export default async function PartnerPage({ params }: PartnerPageProps) {
  const { partner } = await params;

  // Partner-ID vereinheitlichen: Groß-/Kleinschreibung soll egal sein,
  // also immer klein speichern (/Maria und /maria => "maria").
  const partnerId = partner.toLowerCase();

  return <Questionnaire partnerId={partnerId} />;
}
