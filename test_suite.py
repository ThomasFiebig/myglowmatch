#!/usr/bin/env python3
"""
MONAT Haarpflege-System Test-Suite v2
========================================
Testet 7 strategische Profile gegen den n8n-Webhook und holt die echten
Execution-Daten nachträglich via n8n REST API. Funktioniert auch bei
onReceived-Response (Webhook-Konfiguration bleibt unverändert).

Verwendung:
    python3 test_suite.py                    # alle 7 Profile
    python3 test_suite.py --profile sarah    # nur eines
    python3 test_suite.py --verbose          # voller JSON-Output
    python3 test_suite.py --save             # speichert Ergebnisse
    python3 test_suite.py --wait 6           # Wartezeit anpassen

Voraussetzungen:
    - Python 3.8+
    - .env mit N8N_API_KEY und N8N_BASE_URL
    - Nur Standard-Library
"""

import argparse
import json
import os
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

# ─── Konfiguration ──────────────────────────────────────────────
WEBHOOK_URL = "https://veradex.app.n8n.cloud/webhook/glowmatch-haaranalyse"
WORKFLOW_ID = "pwSWA5NatKiLhueB"
SIGNATURE = None  # gefüllt aus .env (N8N_WEBHOOK_SECRET) in main()
TARGET_NODE = "15 Routine sortieren"
TIMEOUT = 30
SINGLE_PROFILE_WAIT = 360       # 6 Min — reale Pipeline-Latenz (6 Sheet-Loader + Cold-Start)
BULK_TOTAL_WAIT = 900           # 15 Min — Trigger-Phase (7×90s) + letzte Pipeline (4 Min)
BULK_TRIGGER_GAP = 90           # 90 s — Pause zwischen sequenziellen Webhook-POSTs, vermeidet Google-Sheets-Rate-Limit
POLL_INTERVAL_SINGLE = 0.8      # schneller Poll für Single-Profile (lokale Sicht auf 1 ID)
POLL_INTERVAL_BULK = 15.0       # bulk-Polling alle 15 s — schont API, reicht für 3-5 Min-Pipelines
TERMINAL_STATUSES = ("success",)

# ─── ANSI-Farben ────────────────────────────────────────────────
class C:
    R = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    CYAN = "\033[96m"


# ─── Test-Profile (7 strategische Klassen) ─────────────────────
PROFILES = {
    "anna": {
        "partner_id": "desiree",
        "first_name": "Anna-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000001",
        "scalp_status": ["fettig"],
        "hair_structure": "glatt",
        "hair_thickness": "mittel",
        "hair_condition": ["keine_probleme"],
        "hair_treatments": "unbehandelt",
        "heat_frequency": "nie_selten",
        "heat_tools": [],
        "wash_frequency": "taeglich",
        "styling_effort": "lufttrocknen",
        "curl_priority": None,
        "ends_condition": None,
        "care_goals": ["gesunde_kopfhaut"],
        "routine_preference": "minimal",
        "time_commitment": "sehr_wenig",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "maria": {
        "partner_id": "desiree",
        "first_name": "Maria-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000002",
        "scalp_status": ["normal"],
        "hair_structure": "wellig",
        "hair_thickness": "fein",
        "hair_condition": ["duenn", "kraftlos"],
        "hair_treatments": "gefaerbt",
        "heat_frequency": "nie",
        "heat_tools": [],
        "wash_frequency": "alle_2_3_tage",
        "styling_effort": "lufttrocknen",
        "curl_priority": "mehr_definition",
        "ends_condition": None,
        "care_goals": ["volumen", "gesunde_kopfhaut"],
        "routine_preference": "ausgewogen",
        "time_commitment": "mittel",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "lena": {
        "partner_id": "desiree",
        "first_name": "Lena-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000003",
        "scalp_status": ["normal"],
        "hair_structure": "kraus",
        "hair_thickness": "dick",
        "hair_condition": ["trocken", "frizz"],
        "hair_treatments": "gefaerbt",
        "heat_frequency": "sehr_haeufig",
        "heat_tools": ["lockenstab"],
        "wash_frequency": "1x_pro_woche",
        "styling_effort": "aufwendiges_styling",
        "curl_priority": "mehr_definition",
        "ends_condition": "leicht_trocken",
        "care_goals": ["feuchtigkeit", "mehr_glanz"],
        "routine_preference": "bestmoeglich",
        "time_commitment": "bewusst_regelmaessig",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "julia": {
        "partner_id": "desiree",
        "first_name": "Julia-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000004",
        "scalp_status": ["normal"],
        "hair_structure": "glatt",
        "hair_thickness": "fein",
        "hair_condition": ["kraftlos"],
        "hair_treatments": "unbehandelt",
        "heat_frequency": "nie_selten",
        "heat_tools": [],
        "wash_frequency": "alle_2_3_tage",
        "styling_effort": "leichtes_styling",
        "curl_priority": None,
        "ends_condition": None,
        "care_goals": ["volumen"],
        "routine_preference": "ausgewogen",
        "time_commitment": "mittel",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "bianca": {
        "partner_id": "desiree",
        "first_name": "Bianca-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000005",
        "scalp_status": ["juckend_empfindlich"],
        "hair_structure": "wellig",
        "hair_thickness": "mittel",
        "hair_condition": ["trocken"],
        "hair_treatments": "gefaerbt",
        "heat_frequency": "nie_selten",
        "heat_tools": [],
        "wash_frequency": "alle_2_3_tage",
        "styling_effort": "leichtes_styling",
        "curl_priority": None,
        "ends_condition": None,
        "care_goals": ["gesunde_kopfhaut", "feuchtigkeit"],
        "routine_preference": "ausgewogen",
        "time_commitment": "mittel",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "vivien": {
        "partner_id": "desiree",
        "first_name": "Vivien-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000006",
        "scalp_status": ["normal"],
        "hair_structure": "wellig",
        "hair_thickness": "dick",
        "hair_condition": ["keine_probleme"],
        "hair_treatments": "gefaerbt",
        "heat_frequency": "regelmaessig",
        "heat_tools": ["lockenstab"],
        "wash_frequency": "taeglich",
        "styling_effort": "lufttrocknen",
        "curl_priority": "mehr_definition",
        "ends_condition": None,
        "care_goals": ["gesunde_kopfhaut"],
        "routine_preference": "bestmoeglich",
        "time_commitment": "sehr_wenig",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    "sarah": {
        "partner_id": "desiree",
        "first_name": "Sarah-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000007",
        "scalp_status": ["normal"],
        "hair_structure": "lockig",
        "hair_thickness": "fein",
        "hair_condition": ["stark_geschaedigt", "spliss", "trocken"],
        "hair_treatments": "blondiert",
        "heat_frequency": "sehr_haeufig",
        "heat_tools": ["glaetteisen"],
        "wash_frequency": "alle_2_3_tage",
        "styling_effort": "aufwendiges_styling",
        "curl_priority": "mehr_definition",
        "ends_condition": "spliss",
        "care_goals": ["reparatur", "feuchtigkeit"],
        "routine_preference": "bestmoeglich",
        "time_commitment": "bewusst_regelmaessig",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    # Silvia — Locken-Profil das glatt getragen wird (Migration #16 Test).
    # Erwartung: smoothing_fohn_spray (REQ-04b) statt curl_creme/hitzeschutzspray,
    # keine Curl-Produkte, Hitzeschutz greift.
    "silvia": {
        "partner_id": "desiree",
        "first_name": "Silvia-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000009",
        "scalp_status": ["normal"],
        "hair_structure": "wellig",
        "hair_thickness": "mittel",
        "hair_condition": ["trocken", "frizz"],
        "hair_treatments": "gefaerbt",
        "heat_frequency": "regelmaessig",
        "heat_tools": ["glaetteisen"],
        "wash_frequency": "alle_2_3_tage",
        "styling_effort": "regelmaessiges_styling",
        "curl_priority": "glatt",
        "ends_condition": "leicht_trocken",
        "care_goals": ["glanz", "feuchtigkeit"],
        "routine_preference": "ausgewogen",
        "time_commitment": "mittel",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
    # Sina — Locken-Vollprofil mit curl_priority='beides' (Migration #15 Test).
    # Erwartung: curl_creme (styling_1) + curl_gelee (styling_2) +
    # curl_auffrischer (styling_3), kein smoothing_fohn_spray (Frizz+Locken),
    # kein hitzeschutzspray (durch wants_full_curl_line), nur ein Scalp-Comfort-Produkt.
    "sina": {
        "partner_id": "desiree",
        "first_name": "Sina-TEST",
        "email": "info@myglowmatch.de",
        "phone": "01500000008",
        "scalp_status": ["juckend_empfindlich", "schuppig"],
        "hair_structure": "kraus",
        "hair_thickness": "dick",
        "hair_condition": ["trocken", "frizz"],
        "hair_treatments": "blondiert",
        "heat_frequency": "nie_selten",
        "heat_tools": [],
        "wash_frequency": "1x_pro_woche",
        "styling_effort": "aufwendiges_styling",
        "curl_priority": "beides",
        "ends_condition": "deutlich_trocken",
        "care_goals": ["feuchtigkeit", "reparatur"],
        "routine_preference": "bestmoeglich",
        "time_commitment": "bewusst_regelmaessig",
        "consent_recommendation": True,
        "consent_marketing": False,
    },
}


# ─── .env-Loader ────────────────────────────────────────────────
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


# ─── Webhook + n8n_api Calls ────────────────────────────────────
def trigger_webhook(profile_data: dict) -> dict:
    """Schickt Profil-Daten an n8n-Webhook (Response = 'Workflow was started')."""
    body = json.dumps(profile_data).encode("utf-8")
    req = urllib.request.Request(
        WEBHOOK_URL,
        data=body,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-glowmatch-secret": SIGNATURE,
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def n8n_api_get(base_url: str, path: str, api_key: str):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    req = urllib.request.Request(
        url,
        headers={
            "X-N8N-API-KEY": api_key,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _as_int_id(val) -> int:
    try:
        return int(val)
    except (TypeError, ValueError):
        return 0


def get_current_max_execution_id(base_url: str, api_key: str) -> int:
    """Höchste vorhandene Execution-ID für den Workflow (Baseline vor Trigger)."""
    data = n8n_api_get(
        base_url,
        f"/executions?workflowId={WORKFLOW_ID}&limit=1",
        api_key,
    )
    items = data.get("data", data) if isinstance(data, dict) else data
    if not items:
        return 0
    return _as_int_id(items[0].get("id"))


def _extract_first_name_from_detail(detail: dict):
    """Holt first_name aus einer Execution (für Profil-Verifikation)."""
    try:
        rd = detail.get("data", {}).get("resultData", {}).get("runData", {}) or {}
        for node_name in ("15 Routine sortieren", "02 Felder extrahieren"):
            node_runs = rd.get(node_name, [])
            if not node_runs:
                continue
            items = (node_runs[0].get("data", {}) or {}).get("main", [[]])
            items = items[0] if items else []
            if not items:
                continue
            j = items[0].get("json", {}) or {}
            n = j.get("normalized") or j
            if isinstance(n, dict) and n.get("first_name"):
                return n["first_name"]
    except Exception:
        pass
    return None


def fetch_latest_execution(base_url: str, api_key: str, baseline_id: int = 0,
                            max_wait: float = SINGLE_PROFILE_WAIT,
                            expected_first_name: str = None):
    """Polling: wartet, bis eine Execution mit ID > baseline_id existiert, success
    ist UND optional zum erwarteten first_name passt.

    expected_first_name verhindert Profil-Verwechslung bei Latenz-Spikes:
    wenn eine Execution success ist aber zu einem anderen Profil gehört,
    wird sie ignoriert (kein false-positive).
    """
    deadline = time.time() + max_wait
    polls = 0
    rejected_ids = set()  # bereits geprüft + verworfen (anderes Profil)
    while time.time() < deadline:
        polls += 1
        data = n8n_api_get(
            base_url,
            f"/executions?workflowId={WORKFLOW_ID}&limit=10",
            api_key,
        )
        items = data.get("data", data) if isinstance(data, dict) else data
        for ex in items:
            eid = _as_int_id(ex.get("id"))
            if eid <= baseline_id:
                continue
            if eid in rejected_ids:
                continue
            status = ex.get("status", "")
            if status not in TERMINAL_STATUSES:
                continue
            # Profil-Verifikation (falls gewünscht)
            if expected_first_name:
                try:
                    detail = n8n_api_get(base_url, f"/executions/{eid}?includeData=true", api_key)
                    fn = _extract_first_name_from_detail(detail)
                    if fn and fn != expected_first_name:
                        rejected_ids.add(eid)
                        continue
                except Exception:
                    # Wenn Detail-Fetch fehlschlägt, lieber überspringen als falsch zuordnen
                    rejected_ids.add(eid)
                    continue
            ex["_polls"] = polls
            return ex
        time.sleep(POLL_INTERVAL_SINGLE)
    return None


def fetch_new_success_executions(base_url: str, api_key: str, baseline_id: int,
                                  expected_count: int, max_wait: float):
    """Bulk-Polling: wartet, bis `expected_count` neue success-Executions
    (ID > baseline_id) für den Workflow existieren. Pollt mit
    POLL_INTERVAL_BULK. Return: Liste der Executions, aufsteigend nach ID.
    Bei Timeout: was bis dahin da war (partial).
    """
    deadline = time.time() + max_wait
    last_found = -1
    while time.time() < deadline:
        data = n8n_api_get(
            base_url,
            f"/executions?workflowId={WORKFLOW_ID}&status=success&limit=20",
            api_key,
        )
        items = data.get("data", data) if isinstance(data, dict) else data
        new = [e for e in items if _as_int_id(e.get("id")) > baseline_id]
        new.sort(key=lambda e: _as_int_id(e.get("id")))
        if len(new) != last_found:
            elapsed = int(time.time() - (deadline - max_wait))
            print(f"{C.DIM}  t+{elapsed:3d}s: {len(new)}/{expected_count} success-Executions seit Baseline {baseline_id}{C.R}")
            last_found = len(new)
        if len(new) >= expected_count:
            return new[:expected_count] if len(new) > expected_count else new
        time.sleep(POLL_INTERVAL_BULK)
    # Timeout: was bis dahin da ist
    data = n8n_api_get(
        base_url,
        f"/executions?workflowId={WORKFLOW_ID}&status=success&limit=20",
        api_key,
    )
    items = data.get("data", data) if isinstance(data, dict) else data
    new = [e for e in items if _as_int_id(e.get("id")) > baseline_id]
    new.sort(key=lambda e: _as_int_id(e.get("id")))
    return new


def fetch_execution_details(base_url: str, api_key: str, exec_id) -> dict:
    return n8n_api_get(base_url, f"/executions/{exec_id}?includeData=true", api_key)


def extract_node_json(detail: dict, node_name: str) -> dict:
    """Holt den JSON-Output eines beliebigen Nodes aus der Execution."""
    try:
        run_data = detail.get("data", {}).get("resultData", {}).get("runData", {})
        node_runs = run_data.get(node_name, [])
        if not node_runs:
            return {}
        main = node_runs[0].get("data", {}).get("main", [])
        if not main or not main[0]:
            return {}
        return main[0][0].get("json", {})
    except (KeyError, IndexError, TypeError, AttributeError):
        return {}


def extract_routine_output(detail: dict) -> dict:
    """Holt Routine-Output aus Node 15. Seit Node-12-Pass-Through (siehe
    Workflow) propagiert Node 15 `applied_conflict_rules` automatisch via
    `...data`-Spread aus Node 14 — kein Merge mehr nötig."""
    return dict(extract_node_json(detail, TARGET_NODE))


# ─── Anomalie-Heuristik ─────────────────────────────────────────
def check_anomalies(profile: dict, output: dict) -> list:
    warnings = []
    routine = output.get("final_routine", [])
    product_keys = [p.get("produkt_key", "") for p in routine]

    if profile["hair_structure"] in ("wellig", "lockig", "kraus"):
        if "fohncreme" in product_keys:
            warnings.append("Föhncreme empfohlen trotz Locken/Wellen (glättet aktiv)")
        # Migration #15 — Locken-Profile sollten mind. 1 Curl-Produkt erhalten,
        # AUSSER curl_priority='glatt' (User trägt Locken bewusst geglättet).
        if profile.get("curl_priority") != "glatt":
            curl_products = {"curl_creme", "curl_gelee", "curl_auffrischer"}
            if not (set(product_keys) & curl_products):
                warnings.append("Locken-Profil ohne einziges Curl-Produkt")
        # Smoothing-Föhn-Spray darf bei Locken + Frizz nicht im Slot landen
        # (CON-13, Migration #14): Curl-Creme behandelt Frizz besser.
        # AUSNAHME: curl_priority='glatt' → smoothing_fohn_spray ist explizit gewollt (REQ-04b, Migration #16)
        if "frizz" in profile.get("hair_condition", []) and profile.get("curl_priority") != "glatt":
            if "smoothing_fohn_spray" in product_keys:
                warnings.append("Smoothing Föhn-Spray empfohlen trotz Locken+Frizz (CON-13 hätte greifen müssen)")
    # Migration #16 — bei curl_priority='glatt' (prefers_straight): kein Curl-Produkt,
    # aber Hitzeschutz bei heat_use=yes muss da sein
    if profile.get("curl_priority") == "glatt":
        curl_products = {"curl_creme", "curl_gelee", "curl_auffrischer"}
        leaked = set(product_keys) & curl_products
        if leaked:
            warnings.append(f"Curl-Produkt(e) trotz 'glatt'-Wunsch empfohlen: {sorted(leaked)}")
        if profile.get("heat_frequency") in ("regelmaessig", "sehr_haeufig"):
            hitze_produkte = {"hitzeschutzspray", "smoothing_fohn_spray", "fohncreme"}
            if not (set(product_keys) & hitze_produkte):
                warnings.append("'glatt' + Hitzestyling, aber kein Hitzeschutz-Produkt empfohlen")

    has_fettig = "fettig" in profile.get("scalp_status", [])
    if not has_fettig:
        if "essig_shampoo" in product_keys or "essig_spuelung" in product_keys:
            warnings.append("Essig-Linie empfohlen ohne fettige Kopfhaut")

    if profile.get("curl_priority") == "mehr_definition":
        for k in ("smoothing_shampoo", "smoothing_deep_conditioner", "smoothing_fohn_spray"):
            if k in product_keys:
                warnings.append(f"{k} empfohlen trotz Definitions-Wunsch")

    if profile["hair_thickness"] == "dick":
        for k in ("ir_clinical_shampoo", "ir_clinical_spuelung", "ir_clinical_kopfhautserum"):
            if k in product_keys:
                warnings.append(f"{k} bei dickem Haar (Datenblatt: 'Feines bis mittleres Haar')")

    has_shampoo = any(p.get("slot_typ") == "shampoo" for p in routine)
    has_spuelung = any(p.get("slot_typ") == "spuelung" for p in routine)
    if not has_shampoo:
        warnings.append("KEIN Shampoo in der Routine!")
    if not has_spuelung and profile.get("routine_preference") != "minimal":
        warnings.append("KEINE Spülung in der Routine!")

    if not routine:
        warnings.append("Routine ist KOMPLETT LEER!")

    return warnings


# ─── Output-Formatierung ────────────────────────────────────────
def print_profile_report(name: str, profile: dict, output: dict, anomalies: list):
    pl = output.get("pflegelevel", {})
    applied = output.get("applied_conflict_rules", [])
    routine = output.get("final_routine", [])
    count = output.get("routine_count", 0)

    print(f"\n{C.BOLD}{C.CYAN}━━━ {name.upper()} ━━━{C.R}")

    print(
        f"{C.DIM}Eingabe: "
        f"{profile['hair_structure']}, {profile['hair_thickness']}, "
        f"{', '.join(profile['hair_condition'])}, "
        f"{profile['hair_treatments']}, Hitze: {profile['heat_frequency']}, "
        f"Pref: {profile['routine_preference']}{C.R}"
    )

    print(
        f"{C.BOLD}Pflegelevel:{C.R} {pl.get('pflegelevel_final', '?')} "
        f"({pl.get('pflegelevel_raw', '?')} Pkt) • "
        f"max={pl.get('max_products', '?')} • "
        f"count={count}"
    )

    if applied:
        print(f"{C.BOLD}Konflikt-Regeln gefeuert:{C.R}")
        for r in applied:
            removed = r.get("removed_products", [])
            print(
                f"  {C.YELLOW}{r.get('konflikt_id', '?')}{C.R}: "
                f"-{r.get('removed_count', len(removed))} ({', '.join(removed)})"
            )
    else:
        print(f"{C.DIM}Keine Konflikt-Regeln gefeuert{C.R}")

    print(f"{C.BOLD}Routine:{C.R}")
    if not routine:
        print(f"  {C.DIM}(keine){C.R}")
    for p in routine:
        slot = p.get("slot_typ", "?")
        prio = p.get("priority", "?")
        prio_short = {
            "required_always": "REQ",
            "required_conditional": "req",
            "optional": "opt",
        }.get(prio, prio)
        nm = p.get("produktname_de", "?")
        linie = p.get("produktlinie", "")
        reason = p.get("reason", "")
        reason_short = reason.split(":")[0] if ":" in reason else reason
        print(
            f"  {p.get('anwendungs_schritt', '?'):>2}. "
            f"[{slot:<18s} {prio_short:>3s}] "
            f"{nm[:55]:<55s} "
            f"{C.DIM}({linie}, {reason_short}){C.R}"
        )

    if anomalies:
        print(f"{C.RED}⚠ Möglicherweise problematisch:{C.R}")
        for w in anomalies:
            print(f"   {C.RED}• {w}{C.R}")


def print_overview(results: dict):
    print(f"\n{C.BOLD}{C.BLUE}═══ GESAMT-ÜBERSICHT ═══{C.R}\n")
    print(f"{'Profil':<10}{'Level':<8}{'Pkt':<6}{'Cap':<6}{'Anzahl':<9}{'Status':<30}")
    print("─" * 70)
    for name, data in results.items():
        out = data["output"]
        pl = out.get("pflegelevel", {}) if out else {}
        anomalies = data["anomalies"]
        if not out:
            status = f"{C.RED}✗ FEHLER{C.R}"
        elif not anomalies:
            status = f"{C.GREEN}✓ OK{C.R}"
        else:
            status = f"{C.RED}⚠ {len(anomalies)} Auffälligkeit(en){C.R}"
        count_val = out.get("routine_count", "?") if out else "?"
        print(
            f"{name:<10}"
            f"{str(pl.get('pflegelevel_final', '?')):<8}"
            f"{str(pl.get('pflegelevel_raw', '?')):<6}"
            f"{str(pl.get('max_products', '?')):<6}"
            f"{str(count_val):<9}"
            f"{status:<30}"
        )


# ─── Run-Modi ──────────────────────────────────────────────────
def run_single(base_url: str, api_key: str, name: str, profile: dict,
                max_wait: float, verbose: bool) -> dict:
    """Single-Profile-Run: Trigger + Polling auf 1 success-Execution."""
    try:
        baseline_id = get_current_max_execution_id(base_url, api_key)
        print(f"\n{C.DIM}→ Trigger Webhook für '{name}' (Baseline-ID: {baseline_id})…{C.R}")
        trigger_resp = trigger_webhook(profile)
        print(f"{C.DIM}  Webhook-Response: {trigger_resp}{C.R}")

        expected_fn = profile.get("first_name")
        print(f"{C.DIM}  Polle auf Execution > {baseline_id} mit first_name={expected_fn} (max {max_wait:.0f}s)…{C.R}")
        execution = fetch_latest_execution(
            base_url, api_key,
            baseline_id=baseline_id,
            max_wait=max_wait,
            expected_first_name=expected_fn,
        )
        if not execution:
            raise RuntimeError(
                f"Keine passende Execution > {baseline_id} (first_name={expected_fn}) innerhalb {max_wait:.0f}s"
            )

        exec_id = execution.get("id")
        polls = execution.get("_polls", "?")
        print(f"{C.DIM}  Execution-ID: {exec_id}, status: {execution.get('status', '?')} (nach {polls} Poll(s)){C.R}")

        detail = fetch_execution_details(base_url, api_key, exec_id)
        output = extract_routine_output(detail)
        if not output:
            print(f"{C.YELLOW}  ⚠ Konnte Output von '{TARGET_NODE}' nicht extrahieren{C.R}")

        anomalies = check_anomalies(profile, output)
        result = {"output": output, "anomalies": anomalies, "execution_id": exec_id}

        if verbose:
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print_profile_report(name, profile, output, anomalies)
        return result
    except urllib.error.HTTPError as e:
        print(f"{C.RED}✗ HTTP-Fehler bei {name}: {e.code} {e.reason}{C.R}")
        try:
            print(f"{C.DIM}  Body: {e.read().decode('utf-8', errors='replace')[:300]}{C.R}")
        except Exception:
            pass
        return {"output": None, "anomalies": [f"HTTP {e.code}"], "execution_id": None}
    except Exception as e:
        print(f"{C.RED}✗ Fehler bei {name}: {e}{C.R}")
        return {"output": None, "anomalies": [str(e)], "execution_id": None}


def run_bulk(base_url: str, api_key: str, to_test: list, gap: float,
              max_wait: float, verbose: bool) -> dict:
    """Bulk-Modus: alle Profile sequenziell triggern (Gap dazwischen), dann
    auf alle Executions warten und in einem Rutsch auswerten. Behebt T-03:
    Per-Profile-Polling timed bei 90s out — hier wartet die Suite einmal
    auf alle Executions gleichzeitig, statt nach jedem Trigger.

    Profile-Zuordnung erfolgt nachträglich per `first_name` aus dem Node
    `15 Routine sortieren`. Wer keine Execution bekommt (Timeout oder
    fehlgeschlagene Pipeline), landet mit output=None im Result.
    """
    baseline_id = get_current_max_execution_id(base_url, api_key)
    print(f"\n{C.DIM}Bulk-Modus: Baseline-ID {baseline_id}, Trigger-Gap {gap:.0f}s, Wait-Limit {max_wait:.0f}s{C.R}")

    # ── Phase 1: sequenziell triggern ─────────────────────────
    for i, name in enumerate(to_test):
        profile = PROFILES[name]
        try:
            t0 = time.time()
            resp = trigger_webhook(profile)
            elapsed = time.time() - t0
            print(f"{C.DIM}  [{i+1}/{len(to_test)}] {name:8s} → {resp.get('message', resp)} ({elapsed:.1f}s){C.R}")
        except Exception as e:
            print(f"{C.RED}  [{i+1}/{len(to_test)}] {name:8s} → FAIL: {e}{C.R}", file=sys.stderr)
        if i < len(to_test) - 1:
            time.sleep(gap)

    # ── Phase 2: warten bis alle Executions success ───────────
    print(f"\n{C.DIM}Warte auf {len(to_test)} neue success-Executions…{C.R}")
    new_executions = fetch_new_success_executions(
        base_url, api_key, baseline_id, len(to_test), max_wait
    )
    if len(new_executions) < len(to_test):
        print(f"{C.YELLOW}⚠ Nur {len(new_executions)}/{len(to_test)} Executions success innerhalb {max_wait:.0f}s — Rest mit output=None{C.R}")

    # ── Phase 3: per first_name den Profilen zuordnen ─────────
    fn_to_exec = {}
    for ex in new_executions:
        exec_id = ex.get("id")
        try:
            detail = fetch_execution_details(base_url, api_key, exec_id)
        except Exception as e:
            print(f"{C.YELLOW}  ⚠ Detail-Fetch Execution {exec_id} failed: {e}{C.R}")
            continue
        fn = _extract_first_name_from_detail(detail)
        if not fn:
            print(f"{C.YELLOW}  ⚠ Execution {exec_id}: kein first_name extrahiert{C.R}")
            continue
        fn_to_exec[fn] = (ex, detail)

    # ── Phase 4: Reports pro Profil ──────────────────────────
    results = {}
    for name in to_test:
        profile = PROFILES[name]
        expected_fn = profile.get("first_name")
        match = fn_to_exec.get(expected_fn)
        if not match:
            print(f"{C.RED}\n✗ {name}: keine passende Execution (first_name={expected_fn}) gefunden{C.R}")
            results[name] = {"output": None, "anomalies": ["keine passende Execution"], "execution_id": None}
            continue
        ex, detail = match
        exec_id = ex.get("id")
        output = extract_routine_output(detail)
        anomalies = check_anomalies(profile, output)
        results[name] = {"output": output, "anomalies": anomalies, "execution_id": exec_id}
        if verbose:
            print(f"\n{C.BOLD}{name}: Execution {exec_id}{C.R}")
            print(json.dumps(output, indent=2, ensure_ascii=False))
        else:
            print_profile_report(name, profile, output, anomalies)
    return results


# ─── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="MONAT System Test-Suite v3 (T-03)")
    parser.add_argument("--profile", "-p",
        choices=list(PROFILES.keys()) + ["all"], default="all",
        help="Welches Profil testen")
    parser.add_argument("--verbose", "-v", action="store_true",
        help="Zeige vollen JSON-Output statt Summary")
    parser.add_argument("--save", action="store_true",
        help="Speichere Ergebnisse in test_results_<ts>.json")
    parser.add_argument("--wait", type=float, default=None,
        help=f"Max. Wartezeit (Sek.). Single-Profile-Default {SINGLE_PROFILE_WAIT}s, Bulk-Default {BULK_TOTAL_WAIT}s.")
    parser.add_argument("--gap", type=float, default=BULK_TRIGGER_GAP,
        help=f"Gap (Sek.) zwischen Bulk-Triggern (default: {BULK_TRIGGER_GAP}s). Schützt vor Google-Sheets-Rate-Limit.")
    args = parser.parse_args()

    env = load_env(Path(__file__).parent / ".env")
    api_key = env.get("N8N_API_KEY") or os.environ.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL") or os.environ.get("N8N_BASE_URL")
    secret = env.get("N8N_WEBHOOK_SECRET") or os.environ.get("N8N_WEBHOOK_SECRET")

    if not api_key or not base_url:
        print(f"{C.RED}FEHLER: N8N_API_KEY oder N8N_BASE_URL fehlt in .env{C.R}", file=sys.stderr)
        sys.exit(1)
    if not secret:
        print(f"{C.RED}FEHLER: N8N_WEBHOOK_SECRET fehlt in .env{C.R}", file=sys.stderr)
        sys.exit(1)

    global SIGNATURE
    SIGNATURE = secret

    to_test = list(PROFILES.keys()) if args.profile == "all" else [args.profile]
    bulk_mode = len(to_test) > 1
    max_wait = args.wait if args.wait is not None else (BULK_TOTAL_WAIT if bulk_mode else SINGLE_PROFILE_WAIT)

    print(f"{C.BOLD}{C.BLUE}MONAT Test-Suite v3 (T-03 Direct-API){C.R}")
    print(f"{C.DIM}Webhook:    {WEBHOOK_URL}{C.R}")
    print(f"{C.DIM}n8n Base:   {base_url}{C.R}")
    print(f"{C.DIM}Workflow:   {WORKFLOW_ID}{C.R}")
    print(f"{C.DIM}Target:     {TARGET_NODE}{C.R}")
    print(f"{C.DIM}Zeit:       {datetime.now().isoformat()}{C.R}")
    print(f"{C.DIM}Mode:       {'bulk' if bulk_mode else 'single'} ({', '.join(to_test)}), Wait {max_wait:.0f}s{C.R}")

    if bulk_mode:
        results = run_bulk(base_url, api_key, to_test, args.gap, max_wait, args.verbose)
        print_overview(results)
    else:
        name = to_test[0]
        results = {name: run_single(base_url, api_key, name, PROFILES[name], max_wait, args.verbose)}

    if args.save:
        fname = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n{C.GREEN}✓ Gespeichert: {fname}{C.R}")


if __name__ == "__main__":
    main()
