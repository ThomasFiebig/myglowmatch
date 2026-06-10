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
SIGNATURE = "acf86723-a18d-4418-8788-cf5c5a4eaf54"
TARGET_NODE = "15 Routine sortieren"
CONFLICT_NODE = "14 Konflikte auflösen"  # propagiert applied_conflict_rules
TIMEOUT = 30
DEFAULT_MAX_WAIT = 90
POLL_INTERVAL = 0.8
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
        "heat_frequency": "gelegentlich",
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
        "heat_tools": ["fohn", "lockenstab"],
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
        "heat_frequency": "gelegentlich",
        "heat_tools": ["fohn"],
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
        "heat_frequency": "gelegentlich",
        "heat_tools": ["fohn"],
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
        "heat_tools": ["fohn"],
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
        "heat_tools": ["fohn", "glaetteisen"],
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
            "x-tally-signature": SIGNATURE,
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
                            max_wait: float = DEFAULT_MAX_WAIT,
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
        time.sleep(POLL_INTERVAL)
    return None


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
    """Holt Routine-Output aus Node 15. Mergt `applied_conflict_rules` aus
    Node 14 ein, weil Node 15 das Feld nicht propagiert (Workflow-Bug)."""
    output = dict(extract_node_json(detail, TARGET_NODE))
    if not output:
        return output

    rules_from_14 = extract_node_json(detail, CONFLICT_NODE).get("applied_conflict_rules", [])
    if rules_from_14 and not output.get("applied_conflict_rules"):
        output["applied_conflict_rules"] = rules_from_14
        output["_conflict_source"] = CONFLICT_NODE
    return output


# ─── Anomalie-Heuristik ─────────────────────────────────────────
def check_anomalies(profile: dict, output: dict) -> list:
    warnings = []
    routine = output.get("final_routine", [])
    product_keys = [p.get("produkt_key", "") for p in routine]

    if profile["hair_structure"] in ("wellig", "lockig", "kraus"):
        if "fohncreme" in product_keys:
            warnings.append("Föhncreme empfohlen trotz Locken/Wellen (glättet aktiv)")

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


# ─── Main ──────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="MONAT System Test-Suite v2")
    parser.add_argument("--profile", "-p",
        choices=list(PROFILES.keys()) + ["all"], default="all",
        help="Welches Profil testen")
    parser.add_argument("--verbose", "-v", action="store_true",
        help="Zeige vollen JSON-Output statt Summary")
    parser.add_argument("--save", action="store_true",
        help="Speichere Ergebnisse in test_results_<ts>.json")
    parser.add_argument("--wait", type=float, default=DEFAULT_MAX_WAIT,
        help=f"Max. Wartezeit (Sek.) auf neue Execution nach Trigger (default: {DEFAULT_MAX_WAIT})")
    args = parser.parse_args()

    env = load_env(Path(__file__).parent / ".env")
    api_key = env.get("N8N_API_KEY") or os.environ.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL") or os.environ.get("N8N_BASE_URL")

    if not api_key or not base_url:
        print(f"{C.RED}FEHLER: N8N_API_KEY oder N8N_BASE_URL fehlt in .env{C.R}", file=sys.stderr)
        sys.exit(1)

    to_test = list(PROFILES.keys()) if args.profile == "all" else [args.profile]

    print(f"{C.BOLD}{C.BLUE}MONAT Test-Suite v2 (Execution-API){C.R}")
    print(f"{C.DIM}Webhook:    {WEBHOOK_URL}{C.R}")
    print(f"{C.DIM}n8n Base:   {base_url}{C.R}")
    print(f"{C.DIM}Workflow:   {WORKFLOW_ID}{C.R}")
    print(f"{C.DIM}Target:     {TARGET_NODE}{C.R}")
    print(f"{C.DIM}Zeit:       {datetime.now().isoformat()}{C.R}")
    print(f"{C.DIM}Profile:    {', '.join(to_test)} (Max-Wait: {args.wait}s, Poll: {POLL_INTERVAL}s){C.R}")

    results = {}
    for name in to_test:
        profile = PROFILES[name]
        try:
            baseline_id = get_current_max_execution_id(base_url, api_key)
            print(f"\n{C.DIM}→ Trigger Webhook für '{name}' (Baseline-ID: {baseline_id})…{C.R}")
            trigger_resp = trigger_webhook(profile)
            print(f"{C.DIM}  Webhook-Response: {trigger_resp}{C.R}")

            expected_fn = profile.get("first_name")
            print(f"{C.DIM}  Polle auf Execution > {baseline_id} mit first_name={expected_fn} (max {args.wait}s)…{C.R}")
            execution = fetch_latest_execution(
                base_url, api_key,
                baseline_id=baseline_id,
                max_wait=args.wait,
                expected_first_name=expected_fn,
            )
            if not execution:
                raise RuntimeError(
                    f"Keine passende Execution > {baseline_id} (first_name={expected_fn}) innerhalb {args.wait}s"
                )

            exec_id = execution.get("id")
            polls = execution.get("_polls", "?")
            print(f"{C.DIM}  Execution-ID: {exec_id}, status: {execution.get('status', '?')} (nach {polls} Poll(s)){C.R}")

            detail = fetch_execution_details(base_url, api_key, exec_id)
            output = extract_routine_output(detail)

            if not output:
                print(f"{C.YELLOW}  ⚠ Konnte Output von '{TARGET_NODE}' nicht extrahieren{C.R}")

            anomalies = check_anomalies(profile, output)
            results[name] = {"output": output, "anomalies": anomalies, "execution_id": exec_id}

            if args.verbose:
                print(json.dumps(output, indent=2, ensure_ascii=False))
            else:
                print_profile_report(name, profile, output, anomalies)

        except urllib.error.HTTPError as e:
            print(f"{C.RED}✗ HTTP-Fehler bei {name}: {e.code} {e.reason}{C.R}")
            try:
                print(f"{C.DIM}  Body: {e.read().decode('utf-8', errors='replace')[:300]}{C.R}")
            except Exception:
                pass
            results[name] = {"output": None, "anomalies": [f"HTTP {e.code}"], "execution_id": None}
        except Exception as e:
            print(f"{C.RED}✗ Fehler bei {name}: {e}{C.R}")
            results[name] = {"output": None, "anomalies": [str(e)], "execution_id": None}

    if len(to_test) > 1:
        print_overview(results)

    if args.save:
        fname = f"test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(fname, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        print(f"\n{C.GREEN}✓ Gespeichert: {fname}{C.R}")


if __name__ == "__main__":
    main()
