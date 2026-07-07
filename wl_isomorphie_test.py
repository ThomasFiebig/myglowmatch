"""
wl_isomorphie_test.py — Werkstatt-Test des wl_adapter.

Liest die 37 MONAT-Produkte aus einem beliebigen test_results-JSON,
schickt jede Zeile durch Reverse→Forward und misst pro Spalte, wie oft
das Ergebnis von der Original-Zeile abweicht.

Rein lokal, schreibt NUR isomorphie_report.md. Keine Sheet-Writes,
keine n8n-Aufrufe. Testdaten werden nach dem Lauf verworfen.

Aufruf:
    python3 wl_isomorphie_test.py                # Default-JSON
    python3 wl_isomorphie_test.py path/to/x.json
"""

from __future__ import annotations
import json
import sys
from collections import defaultdict
from pathlib import Path

from wl_adapter import (
    DB_COLUMNS,
    from_produktdatenbank_row,
    to_produktdatenbank_row,
)


DEFAULT_INPUT = "test_results_20260701_115939.json"
REPORT_OUT = "isomorphie_report.md"

# Erwartete, bewusste Δ (dokumentiert im wl_adapter.py-Header).
# Diese Spalten werden im Report ausgewiesen aber nicht als „echte" Δ
# gewertet — sie sind Design-Entscheidungen, keine Adapter-Bugs.
DESIGN_LOSS_COLS = {"produktlinie", "kombinationen", "kombi_optional"}


def load_all_products(path: str) -> list[dict]:
    with open(path) as f:
        blob = json.load(f)
    seen: set[str] = set()
    prods: list[dict] = []

    def walk(o, depth=0):
        if depth > 8:
            return
        if isinstance(o, dict):
            if "produktname_de" in o and "slot_typ" in o and "produkt_key" in o:
                key = o["produkt_key"]
                if key and key not in seen:
                    seen.add(key)
                    prods.append(o)
            for v in o.values():
                walk(v, depth + 1)
        elif isinstance(o, list):
            for v in o:
                walk(v, depth + 1)

    walk(blob)
    return prods


def normalize(v):
    """Vergleichs-Normalisierung: Booleans case-insensitiv (Original hat
    mal 'FALSE', mal 'False'), Whitespace strip."""
    if v is None:
        return ""
    s = str(v).strip()
    if s.upper() in {"TRUE", "FALSE"}:
        return s.upper()
    return s


def diff_row(original: dict, reproduced: dict) -> list[tuple[str, str, str]]:
    out: list[tuple[str, str, str]] = []
    for col in DB_COLUMNS:
        a = normalize(original.get(col))
        b = normalize(reproduced.get(col))
        if a != b:
            out.append((col, a, b))
    return out


def main(input_path: str) -> None:
    prods = load_all_products(input_path)
    print(f"Geladen: {len(prods)} unikate Produkte aus {input_path}")

    col_diff_count: dict[str, int] = defaultdict(int)
    col_examples: dict[str, list[tuple[str, str, str]]] = defaultdict(list)
    warnings_by_type: dict[str, int] = defaultdict(int)
    warnings_examples: dict[str, list[tuple[str, str]]] = defaultdict(list)
    per_product: list[tuple[str, int, int]] = []  # (name, diff_count, warn_count)

    for p in prods:
        entry, warns = from_produktdatenbank_row(p)
        reproduced = to_produktdatenbank_row(
            entry,
            row_number=p.get("row_number", 0),
            produktlinie=p.get("produktlinie", "eigen"),  # bewusste Konzession
        )
        diffs = diff_row(p, reproduced)
        per_product.append((p["produkt_key"], len(diffs), len(warns)))

        for col, orig, repr_ in diffs:
            col_diff_count[col] += 1
            if len(col_examples[col]) < 3:
                col_examples[col].append((p["produkt_key"], orig, repr_))

        for w in warns:
            # Kategorie aus Warnung ableiten
            kind = w.split(" ", 1)[0]
            warnings_by_type[kind] += 1
            if len(warnings_examples[kind]) < 3:
                warnings_examples[kind].append((p["produkt_key"], w))

    write_report(prods, col_diff_count, col_examples, warnings_by_type,
                 warnings_examples, per_product, input_path)

    # Konsolen-Summary
    print("\n--- Δ pro Spalte (Anzahl abweichender Produkte / 37) ---")
    hard_diffs = 0
    for col in DB_COLUMNS:
        n = col_diff_count.get(col, 0)
        if n == 0:
            continue
        marker = "(design)" if col in DESIGN_LOSS_COLS else ""
        if col not in DESIGN_LOSS_COLS:
            hard_diffs += n
        print(f"  {col:20s} {n:2d}/37 {marker}")
    print(f"\nHarte Δ (ohne Design-Verlust): {hard_diffs}")
    print(f"Report geschrieben: {REPORT_OUT}")


def write_report(prods, col_diff_count, col_examples, warnings_by_type,
                 warnings_examples, per_product, input_path):
    lines = []
    lines.append("# Isomorphie-Report — wl_adapter gegen MONAT-produktdatenbank\n")
    lines.append(f"**Datenquelle:** `{input_path}`  \n")
    lines.append(f"**Produkte getestet:** {len(prods)}  \n")
    lines.append(
        "**Methode:** jede Original-Zeile durch `from_produktdatenbank_row` "
        "(Reverse) → `to_produktdatenbank_row` (Forward); Δ pro Spalte.\n"
    )
    lines.append("\n## Δ pro Spalte\n")
    lines.append("| Spalte | Δ-Anzahl | Kategorie | Beispiele |\n")
    lines.append("|---|---|---|---|\n")
    for col in DB_COLUMNS:
        n = col_diff_count.get(col, 0)
        if n == 0:
            continue
        cat = "**Design (erwartet)**" if col in DESIGN_LOSS_COLS else "Adapter-Δ"
        examples = "; ".join(
            f"`{k}`: `{o}` → `{r}`"
            for k, o, r in col_examples[col]
        )
        lines.append(f"| `{col}` | {n} / {len(prods)} | {cat} | {examples} |\n")

    lines.append("\n## Reverse-Warnungen (aggregiert)\n")
    lines.append("| Warnungs-Kategorie | Vorkommen | Beispiel |\n")
    lines.append("|---|---|---|\n")
    for kind, n in sorted(warnings_by_type.items(), key=lambda x: -x[1]):
        ex = warnings_examples[kind][0] if warnings_examples[kind] else ("", "")
        lines.append(f"| {kind} | {n} | `{ex[0]}`: {ex[1]} |\n")

    lines.append("\n## Pro-Produkt Δ-Verteilung\n")
    lines.append("| Produkt | Δ-Spalten | Warnungen |\n")
    lines.append("|---|---|---|\n")
    for name, d, w in sorted(per_product, key=lambda x: -x[1]):
        lines.append(f"| `{name}` | {d} | {w} |\n")

    Path(REPORT_OUT).write_text("".join(lines))


if __name__ == "__main__":
    inp = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_INPUT
    main(inp)
