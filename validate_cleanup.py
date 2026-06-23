#!/usr/bin/env python3
"""
Direct-API-Validation für Node-05-Cleanup (2026-06-23).

Vergleicht final_routine.produkt_key Position-für-Position zwischen
Pre-Cleanup-Baseline (Executions 472-478 vom 2026-06-23 post Migration #9)
und Post-Cleanup-Lauf (frische Trigger).

Modi:
  --baseline       Pull Baseline 472-478 und schreibe baseline.json
  --trigger        Trigger 7 Profile gegen Webhook
  --post-pull      Pull letzte 7 success-Executions und schreibe post.json
  --diff           Vergleiche baseline.json vs post.json
"""

import argparse
import json
import sys
import time
import urllib.request
import urllib.error
from datetime import datetime
from pathlib import Path

from test_suite import PROFILES, WEBHOOK_URL

BASE_URL = "https://veradex.app.n8n.cloud"
WF_ID = "pwSWA5NatKiLhueB"
BASELINE_PATH = Path("baseline_pre_cleanup.json")
POST_PATH = Path("post_cleanup.json")


def load_env(path: Path) -> dict:
    env = {}
    if not path.exists():
        return env
    for line in path.read_text().splitlines():
        if "=" in line and not line.strip().startswith("#"):
            k, _, v = line.partition("=")
            env[k.strip()] = v.strip()
    return env


def api_get(url: str, api_key: str):
    req = urllib.request.Request(url, headers={"X-N8N-API-KEY": api_key, "Accept": "application/json"})
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def fetch_execution(api_key: str, exec_id: int) -> dict:
    return api_get(f"{BASE_URL}/api/v1/executions/{exec_id}?includeData=true", api_key)


def extract_routine(execution: dict) -> dict:
    """Aus Execution-Run-Data: final_routine + first_name extrahieren."""
    rd = execution.get("data", {}).get("resultData", {}).get("runData", {})
    # Node 15 heißt typischerweise so etwas wie '15 ...' — finde Node mit final_routine
    for node_name, runs in rd.items():
        for run in runs:
            data = run.get("data", {}).get("main", [])
            for output in data:
                for item in output or []:
                    j = item.get("json", {})
                    if "final_routine" in j:
                        produkt_keys = [s.get("produkt_key") for s in j["final_routine"]]
                        first_name = j.get("first_name") or j.get("normalized", {}).get("first_name")
                        return {
                            "exec_id": execution.get("id"),
                            "node": node_name,
                            "first_name": first_name,
                            "produkt_keys": produkt_keys,
                        }
    return {"exec_id": execution.get("id"), "produkt_keys": None}


def cmd_baseline(api_key: str):
    print("Pull Baseline-Executions 472-478…")
    rows = []
    for exec_id in range(472, 479):
        try:
            ex = fetch_execution(api_key, exec_id)
        except urllib.error.HTTPError as e:
            print(f"  {exec_id}: HTTP {e.code} {e.reason}", file=sys.stderr)
            continue
        r = extract_routine(ex)
        r["started_at"] = ex.get("startedAt")
        r["status"] = ex.get("status")
        rows.append(r)
        fn = r.get("first_name") or "?"
        keys = r.get("produkt_keys") or []
        print(f"  {exec_id} {ex.get('status'):8s} fn={fn!r:18s} keys={keys}")
    BASELINE_PATH.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"\nGeschrieben: {BASELINE_PATH} ({len(rows)} Executions)")


def cmd_trigger(secret: str, gap: float = 90.0):
    """Sequenziell triggern mit Pause, damit Google-Sheets-API nicht ratelimit-hit."""
    print(f"Trigger 7 Profile sequenziell (Gap {gap}s pro Profil)…")
    names = list(PROFILES.keys())
    for i, name in enumerate(names):
        profile = PROFILES[name]
        body = json.dumps(profile).encode("utf-8")
        req = urllib.request.Request(
            WEBHOOK_URL, data=body,
            headers={
                "Content-Type": "application/json",
                "x-glowmatch-secret": secret,
            }, method="POST",
        )
        t0 = time.time()
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8", "replace")[:80]
            elapsed = time.time() - t0
            print(f"  [{i+1}/7] {name:8s} → HTTP 200 ({elapsed:.1f}s): {txt}")
        except Exception as e:
            print(f"  [{i+1}/7] {name:8s} → FAIL: {e}", file=sys.stderr)
        if i < len(names) - 1:
            time.sleep(gap)
    print("\nAlle 7 getriggert. Warte 5 Min bis alle Executions fertig sind, dann --post-pull.")


def cmd_post_pull(api_key: str):
    """Pull die letzten 14 Executions, filtere auf success, nimm die letzten 7."""
    print("Pull letzte Executions…")
    url = f"{BASE_URL}/api/v1/executions?workflowId={WF_ID}&limit=20&status=success&includeData=true"
    resp = api_get(url, api_key)
    items = resp.get("data", [])
    items.sort(key=lambda e: e.get("startedAt", ""))
    last_7 = items[-7:]
    print(f"  Got {len(items)} success-Executions, nehme letzte 7:")
    rows = []
    for ex in last_7:
        r = extract_routine(ex)
        r["started_at"] = ex.get("startedAt")
        r["status"] = ex.get("status")
        rows.append(r)
        fn = r.get("first_name") or "?"
        keys = r.get("produkt_keys") or []
        print(f"  {ex.get('id'):5} {ex.get('status'):8s} started={ex.get('startedAt')} fn={fn!r:18s} keys={keys}")
    POST_PATH.write_text(json.dumps(rows, indent=2, ensure_ascii=False))
    print(f"\nGeschrieben: {POST_PATH}")


def cmd_diff():
    if not BASELINE_PATH.exists() or not POST_PATH.exists():
        print(f"FEHLER: {BASELINE_PATH} oder {POST_PATH} fehlt.", file=sys.stderr)
        return 1
    base = {b.get("first_name", "?"): b.get("produkt_keys") for b in json.loads(BASELINE_PATH.read_text())}
    post = {p.get("first_name", "?"): p.get("produkt_keys") for p in json.loads(POST_PATH.read_text())}

    total_slots = 0
    drifted_slots = 0
    print(f"{'first_name':18s} {'slot':>4s} {'baseline':35s} {'post':35s}")
    for fn in sorted(set(base) | set(post)):
        b_keys = base.get(fn) or []
        p_keys = post.get(fn) or []
        n = max(len(b_keys), len(p_keys))
        for i in range(n):
            total_slots += 1
            bv = b_keys[i] if i < len(b_keys) else "(none)"
            pv = p_keys[i] if i < len(p_keys) else "(none)"
            marker = " " if bv == pv else "✗"
            if bv != pv:
                drifted_slots += 1
                print(f"{fn:18s} {i+1:>4d} {bv!s:35s} {pv!s:35s} {marker}")
    print(f"\n=== Ergebnis: {drifted_slots}/{total_slots} Slot-Drift ===")
    return 0 if drifted_slots == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--baseline", action="store_true")
    ap.add_argument("--trigger", action="store_true")
    ap.add_argument("--post-pull", action="store_true")
    ap.add_argument("--diff", action="store_true")
    args = ap.parse_args()

    env = load_env(Path(".env"))
    api_key = env.get("N8N_API_KEY")

    secret = env.get("N8N_WEBHOOK_SECRET")
    if args.baseline:
        cmd_baseline(api_key)
    elif args.trigger:
        cmd_trigger(secret)
    elif args.post_pull:
        cmd_post_pull(api_key)
    elif args.diff:
        return cmd_diff()
    else:
        ap.print_help()


if __name__ == "__main__":
    sys.exit(main() or 0)
