import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  // Erlaubt dem Dev-Server, JS-/HMR-Ressourcen auch an Anfragen aus dem
  // lokalen Netzwerk auszuliefern (z. B. iPhone-Test über die Mac-IP).
  // Ohne diesen Eintrag blockiert Next.js 16 alles außer "localhost" –
  // Symptom: HTML & CSS laden, aber JS nicht -> Seite bleibt leer.
  allowedDevOrigins: ["192.168.2.79"],
};

export default nextConfig;
