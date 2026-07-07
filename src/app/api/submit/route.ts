// ===================================================================
// API-Route: /api/submit  (Etappe 8)
//
// Diese Datei läuft auf dem SERVER. Der Browser schickt das JSON
// hierher; diese Route reicht es an den n8n-Webhook weiter.
// Vorteil: Die Webhook-URL (aus .env.local) bleibt geheim, und es
// gibt keine CORS-Probleme.
// ===================================================================

import { NextResponse } from "next/server";

// Defensiv: wenn jemand die ganze .env-Zeile (`NAME=value`) ins
// Value-Feld der Deployment-ENV kopiert hat, automatisch das Präfix
// entfernen. 2026-06-24: genau dieser Bug hat alle Webhook-Calls
// stumm im n8n-Signature-IF-Branch enden lassen (Execution 550).
function sanitizeEnv(name: string, raw: string | undefined): string | undefined {
  if (!raw) return raw;
  const prefix = `${name}=`;
  if (raw.startsWith(prefix)) {
    console.warn(
      `[env] ${name} ist falsch gesetzt: Wert beginnt mit ${prefix} — ` +
      `vermutlich wurde die ganze .env-Zeile ins Value-Feld kopiert. ` +
      `Trimme automatisch, aber bitte ENV-Variable im Deployment-Dashboard korrigieren.`,
    );
    return raw.slice(prefix.length);
  }
  return raw;
}

export async function POST(request: Request) {
  const webhookUrl = sanitizeEnv("N8N_WEBHOOK_URL", process.env.N8N_WEBHOOK_URL);
  const webhookSecret = sanitizeEnv("N8N_WEBHOOK_SECRET", process.env.N8N_WEBHOOK_SECRET);

  // Sicherheitsnetz: Sind URL und Secret konfiguriert?
  if (!webhookUrl || !webhookSecret) {
    return NextResponse.json(
      { error: "Server-Konfiguration fehlt: N8N_WEBHOOK_URL / N8N_WEBHOOK_SECRET." },
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
      headers: {
        "Content-Type": "application/json",
        "x-glowmatch-secret": webhookSecret,
      },
      body: JSON.stringify(payload),
      signal: AbortSignal.timeout(15000),
    });

    if (!n8nResponse.ok) {
      return NextResponse.json(
        { error: `n8n hat mit Status ${n8nResponse.status} geantwortet.` },
        { status: 502 },
      );
    }

    // n8n-Response (falls „Respond to Webhook"-Node im Workflow steckt)
    // durchreichen, damit das Frontend die tatsächliche Empfehlung
    // rendern kann. Falls n8n nur `{ ok: true }` oder gar nichts schickt,
    // zeigt das Frontend Fake-Daten als Fallback.
    let recommendation: unknown = null;
    try {
      const text = await n8nResponse.text();
      if (text) {
        recommendation = JSON.parse(text);
      }
    } catch {
      // Body kein gültiges JSON — Fallback zu Fake-Daten im Frontend.
      recommendation = null;
    }

    return NextResponse.json({ ok: true, recommendation });
  } catch {
    return NextResponse.json(
      { error: "n8n konnte nicht erreicht werden." },
      { status: 502 },
    );
  }
}
