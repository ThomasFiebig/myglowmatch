#!/usr/bin/env python3
"""
Diff zweier test_results_*.json-Dateien.
=========================================
Vergleicht pro Profil das Set der `final_routine.produkt_key` und
gibt eine Markdown-Tabelle der Drift aus.

Aufruf:
  python3 diff_test_results.py <baseline.json> <post.json>
"""

import json
import sys
from pathlib import Path


def load_results(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Format aus test_suite.py: { profile_name: {output: {...}, anomalies: [...], execution_id: int}, ... }
    profiles = {}
    for name, entry in data.items():
        if not isinstance(entry, dict):
            continue
        output = entry.get("output") or {}
        routine = output.get("final_routine") or []
        keys = sorted({p.get("produkt_key", "") for p in routine if p.get("produkt_key")})
        profiles[name] = {
            "keys": keys,
            "exec_id": entry.get("execution_id"),
            "anomalies": entry.get("anomalies", []),
        }
    return profiles


def main() -> int:
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <baseline.json> <post.json>", file=sys.stderr)
        return 1

    base_path = Path(sys.argv[1])
    post_path = Path(sys.argv[2])
    base = load_results(base_path)
    post = load_results(post_path)

    all_profiles = sorted(set(base) | set(post))

    print(f"# Drift-Diff: {base_path.name} → {post_path.name}\n")
    print("| Profil | Pre-Exec | Post-Exec | +Added | -Removed | Status |")
    print("|---|---|---|---|---|---|")

    drift_count = 0
    for name in all_profiles:
        b = base.get(name)
        p = post.get(name)
        if not b or not p:
            print(f"| {name} | {b['exec_id'] if b else '—'} | {p['exec_id'] if p else '—'} | — | — | ⚠ fehlt in einem Lauf |")
            continue
        b_set = set(b["keys"])
        p_set = set(p["keys"])
        added = sorted(p_set - b_set)
        removed = sorted(b_set - p_set)
        if not added and not removed:
            status = "🟢 identisch"
        else:
            status = "🔴 Drift"
            drift_count += 1
        added_s = ", ".join(added) or "—"
        removed_s = ", ".join(removed) or "—"
        print(f"| {name} | {b['exec_id']} | {p['exec_id']} | {added_s} | {removed_s} | {status} |")

    print(f"\n**Drift: {drift_count}/{len(all_profiles)} Profile**")
    return 0


if __name__ == "__main__":
    sys.exit(main())
