import type { Metadata } from "next";
import { Geist, Fraunces } from "next/font/google";
import { MotionConfig } from "framer-motion";
import "./globals.css";

// Sans-Serif für UI & Fließtext
const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

// Serif (Fraunces) für Headlines – edler Premium-Kontrast
const fraunces = Fraunces({
  variable: "--font-fraunces",
  subsets: ["latin"],
});

// Titel & Beschreibung – erscheinen im Browser-Tab und bei Google.
// openGraph + twitter sorgen für hübsche Vorschau-Karten, wenn der Link
// auf Instagram, WhatsApp, Facebook, X, LinkedIn etc. geteilt wird.
export const metadata: Metadata = {
  metadataBase: new URL("https://myglowmatch.de"),
  title: "MyBeautyKey – Deine persönliche Haaranalyse",
  description:
    "Beantworte ein paar kurze Fragen und erhalte deine persönliche Haarpflege-Empfehlung – abgestimmt auf dein Haar und deine Kopfhaut.",
  icons: {
    icon: [{ url: "/favicon.svg", type: "image/svg+xml" }],
  },
  openGraph: {
    type: "website",
    locale: "de_DE",
    url: "https://myglowmatch.de",
    siteName: "MyBeautyKey",
    title: "MyBeautyKey – Deine persönliche Haaranalyse",
    description:
      "Beantworte ein paar kurze Fragen und erhalte deine persönliche Haarpflege-Empfehlung.",
    images: [
      {
        url: "/og-image.jpg",
        width: 1200,
        height: 630,
        alt: "MyBeautyKey – Deine persönliche Haaranalyse",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "MyBeautyKey – Deine persönliche Haaranalyse",
    description:
      "Beantworte ein paar kurze Fragen und erhalte deine persönliche Haarpflege-Empfehlung.",
    images: ["/og-image.jpg"],
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="de"
      className={`${geistSans.variable} ${fraunces.variable} h-full antialiased`}
    >
      <body className="flex min-h-full flex-col">
        {/* Globaler Hintergrund-Verlauf creme -> leicht rosé.
            position:fixed sorgt dafür, dass der Verlauf immer den
            Viewport ausfüllt und beim Scrollen ruhig stehen bleibt –
            keine Stretch-Artefakte auf langen Seiten. */}
        <div
          aria-hidden="true"
          className="pointer-events-none fixed inset-0 -z-10 bg-[linear-gradient(to_bottom,#fbf5ee,#f5e6dc)]"
        />

        {/* reducedMotion="user": Hat ein Nutzer in seinen System-
            Einstellungen "Bewegung reduzieren" aktiviert, schaltet
            framer-motion automatisch alle Bewegungs-Animationen ab
            (nur dezentes Ein-/Ausblenden bleibt). */}
        <MotionConfig reducedMotion="user">{children}</MotionConfig>
      </body>
    </html>
  );
}
