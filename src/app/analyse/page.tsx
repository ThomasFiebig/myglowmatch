// /analyse – Fragebogen ohne Partner-Kontext (früher unter "/").
// Laut Fragenkatalog gilt ohne Partner: partner_id = "DEFAULT".

import Questionnaire from "@/components/Questionnaire";

export default function AnalysePage() {
  return <Questionnaire partnerId="DEFAULT" />;
}
