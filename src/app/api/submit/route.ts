// ===================================================================
// API-Route: /api/submit  (Etappe 8)
//
// Diese Datei läuft auf dem SERVER. Der Browser schickt das JSON
// hierher; diese Route reicht es an den n8n-Webhook weiter.
// Vorteil: Die Webhook-URL (aus .env.local) bleibt geheim, und es
// gibt keine CORS-Probleme.
// ===================================================================

import { NextResponse } from "next/server";

export async function POST(request: Request) {
  const webhookUrl = process.env.N8N_WEBHOOK_URL;

  // Sicherheitsnetz: Ist die Webhook-URL überhaupt konfiguriert?
  if (!webhookUrl) {
    return NextResponse.json(
      { error: "Server-Konfiguration fehlt: N8N_WEBHOOK_URL ist nicht gesetzt." },
      { status: 500 },
    );
  }

  // 1) Das JSON aus der Anfrage des Browsers lesen.
  let payload: unknown;
  try {
    payload = await request.json();
  } catch {
    return NextResponse.json(
      { error: "Ungültige Anfrage-Daten." },
      { status: 400 },
    );
  }

  // 2) Das JSON an n8n weiterleiten (mit 15-Sekunden-Zeitlimit).
  try {
    const n8nResponse = await fetch(webhookUrl, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(15000),
    });

    if (!n8nResponse.ok) {
      return NextResponse.json(
        { error: `n8n hat mit Status ${n8nResponse.status} geantwortet.` },
        { status: 502 },
      );
    }

    // Erfolg.
    return NextResponse.json({ ok: true });
  } catch {
    return NextResponse.json(
      { error: "n8n konnte nicht erreicht werden." },
      { status: 502 },
    );
  }
}
