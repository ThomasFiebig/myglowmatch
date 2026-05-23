// Startseite "/" – wird OHNE Partner in der URL aufgerufen.
// Laut Fragenkatalog gilt dann partner_id = "DEFAULT".

import Questionnaire from "@/components/Questionnaire";

export default function Home() {
  return <Questionnaire partnerId="DEFAULT" />;
}
