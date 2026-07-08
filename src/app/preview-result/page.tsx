// Preview-Route für DemoResultScreen — nur lokal, nicht öffentlich verlinkt.
// Rendert die Ergebnisseite mit realistischen Fake-Answers ohne den Fragebogen
// durchklicken zu müssen. `recommendation=null` lässt die eingebauten
// FAKE_ROUTINE/FAKE_WARUM-Fallbacks in DemoResultScreen greifen.

import type { Metadata } from "next";
import DemoResultScreen from "@/components/DemoResultScreen";
import type { Answers } from "@/lib/types";

export const metadata: Metadata = {
  title: "Preview · Ergebnisseite",
  robots: { index: false, follow: false },
};

const FAKE_ANSWERS: Answers = {
  first_name: "Sarah",
  phone: "0151 12345678",
  partner_id: "desiree",
  scalp_status: ["trocken"],
  hair_structure: "wellig",
  hair_thickness: "mittel",
  hair_condition: ["trocken", "gefaerbt"],
  hair_treatments: "gefaerbt",
  heat_frequency: "regelmaessig",
  wash_frequency: "nicht_taeglich",
  styling_effort: "ausgewogen",
  curl_priority: "mehr_definition",
  ends_condition: "leicht_trocken",
  care_goals: ["mehr_feuchtigkeit", "mehr_glanz"],
  routine_preference: "ausgewogen",
  time_commitment: "5_10_min",
  wants_email_copy: false,
  email: "",
  consent_recommendation: true,
  consent_marketing: false,
};

export default function PreviewResultPage() {
  return (
    <DemoResultScreen
      firstName="Sarah"
      phone="0151 12345678"
      answers={FAKE_ANSWERS}
      recommendation={null}
    />
  );
}
