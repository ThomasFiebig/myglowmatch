#!/usr/bin/env python3
"""
n8n-Workflow-Inspektor
======================
Holt per n8n-API die Workflow-Definition und zeigt:
  - Liste aller Workflows
  - Webhook-Node-Konfiguration (Response Mode)
  - Ob ein "Respond to Webhook"-Node existiert
  - Den letzten Node der Hauptkette
"""

import json
import os
import sys
import urllib.request
import urllib.error
from pathlib import Path


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, _, v = line.partition("=")
        env[k.strip()] = v.strip()
    return env


def api_get(base_url: str, path: str, api_key: str):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    req = urllib.request.Request(
        url,
        headers={
            "X-N8N-API-KEY": api_key,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main():
    env = load_env(Path(__file__).parent / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")

    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY oder N8N_BASE_URL fehlt in .env", file=sys.stderr)
        sys.exit(1)

    print(f"Base URL: {base_url}")
    print(f"API-Key:  {api_key[:20]}…{api_key[-6:]} (gekürzt)")
    print()

    # 1) Liste aller Workflows
    print("=== Schritt 1: Workflow-Liste ===")
    try:
        wf_list = api_get(base_url, "/workflows", api_key)
    except urllib.error.HTTPError as e:
        print(f"HTTP-Fehler: {e.code} {e.reason}")
        print(e.read().decode("utf-8", errors="replace"))
        sys.exit(1)

    workflows = wf_list.get("data", wf_list) if isinstance(wf_list, dict) else wf_list
    glowmatch_wf = None
    for wf in workflows:
        name = wf.get("name", "?")
        wid = wf.get("id", "?")
        active = "✓ aktiv" if wf.get("active") else "✗ inaktiv"
        marker = ""
        # Priorität: aktiver MONAT/Haar/glowmatch-Workflow
        name_lower = name.lower()
        matches = any(k in name_lower for k in ("glowmatch", "haaranalyse", "haarpflege", "haarberatung"))
        if matches:
            marker = "  ← Kandidat"
            if glowmatch_wf is None or (wf.get("active") and not glowmatch_wf.get("active")):
                glowmatch_wf = wf
                marker += " (gewählt)"
        print(f"  [{wid}] {active}  {name}{marker}")

    if not glowmatch_wf:
        print("\nKein Workflow mit 'glowmatch' oder 'haaranalyse' im Namen gefunden.")
        sys.exit(0)

    # 2) Details des Glowmatch-Workflows
    wid = glowmatch_wf["id"]
    print(f"\n=== Schritt 2: Workflow-Details '{glowmatch_wf['name']}' (ID {wid}) ===")
    detail = api_get(base_url, f"/workflows/{wid}", api_key)

    nodes = detail.get("nodes", [])
    print(f"Anzahl Nodes: {len(nodes)}")
    print()

    # Webhook-Nodes finden
    webhook_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.webhook"]
    respond_nodes = [n for n in nodes if n.get("type") == "n8n-nodes-base.respondToWebhook"]

    print(f"Webhook-Nodes:           {len(webhook_nodes)}")
    print(f"Respond-to-Webhook-Nodes: {len(respond_nodes)}")
    print()

    for wn in webhook_nodes:
        print(f"--- Webhook-Node: '{wn.get('name')}' ---")
        params = wn.get("parameters", {})
        print(f"  Path:           {params.get('path', '(default)')}")
        print(f"  HTTP-Methode:   {params.get('httpMethod', 'GET')}")
        response_mode = params.get("responseMode", "onReceived")
        print(f"  Response-Mode:  {response_mode}")
        if response_mode == "onReceived":
            print("  ⚠ PROBLEM: 'onReceived' = Webhook antwortet SOFORT mit 'Workflow was started'")
            print("    → muss auf 'responseNode' (= 'Using Respond to Webhook Node') geändert werden")
        elif response_mode == "lastNode":
            print("  ✓ 'lastNode' = Antwort kommt vom letzten Node der Kette")
        elif response_mode == "responseNode":
            print("  ✓ 'responseNode' = Antwort kommt vom 'Respond to Webhook'-Node")
        print(f"  Response-Data:  {params.get('responseData', '(default)')}")
        print()

    if respond_nodes:
        for rn in respond_nodes:
            print(f"--- Respond-to-Webhook-Node: '{rn.get('name')}' ---")
            params = rn.get("parameters", {})
            print(f"  Respond-With:   {params.get('respondWith', '(default)')}")
            if "responseBody" in params:
                body = params["responseBody"]
                print(f"  Response-Body:  {body[:200]}{'…' if len(str(body)) > 200 else ''}")
            print()
    else:
        print("⚠ Es gibt KEINEN 'Respond to Webhook'-Node im Workflow.")
        print("  Bei Response-Mode='responseNode' wäre das ein Fehler.")
        print()

    # Alle Node-Namen + Typen kurz auflisten (Übersicht)
    print("--- Alle Nodes im Workflow ---")
    for n in nodes:
        ntype = n.get("type", "?").replace("n8n-nodes-base.", "")
        disabled = " (DEAKTIVIERT)" if n.get("disabled") else ""
        print(f"  • {n.get('name', '?'):<40s} [{ntype}]{disabled}")


if __name__ == "__main__":
    main()
