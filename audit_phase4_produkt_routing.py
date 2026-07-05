#!/usr/bin/env python3
"""
Phase-4-Inventar — Routing-Aussage pro Produkt
================================================
Aus den Routing-Tabs (map_slot_rules, map_conflict_rules,
map_pool_filter) und den Stammdaten (produktdatenbank) sammeln wir
pro Produkt alle Aussagen, die das System über dieses Produkt trifft.
Output: `audit_phase4_inventar.md` als Briefing für die PDF-Welle.

Bereits in Phase 3 geprüft (ausgeblendet): 8 Produkte um Bond-IQ +
moxie_mousse + volumen_spray + curl_creme + entwirrungsspray.
"""

from __future__ import annotations

import csv
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).parent
sys.path.insert(0, str(REPO))

from sheets_writer import DOC_ID, load_env, open_sheet, resolve_sa_path

ALREADY_AUDITED = {
    "bond_iq_leave_in",
    "bond_iq_night_day_serum",
    "bond_iq_shampoo",
    "bond_iq_spuelung",
    "curl_creme",
    "entwirrungsspray",
    "moxie_mousse",
    "volumen_spray",
}

OUT_MD = REPO / "audit_phase4_inventar.md"


def load_tab(ws) -> list[dict]:
    values = ws.get_all_values()
    if not values:
        return []
    headers = values[0]
    return [dict(zip(headers, row + [""] * (len(headers) - len(row)))) for row in values[1:]]


def parse_filter(filter_str: str) -> tuple[str, list[str]]:
    """Klassifiziert einen REQ-filter-Wert.

    Return: (kategorie, werte)
      - "exakt_key": filter ist eine `produkt_key`- oder `produktlinie`-Liste (pipe-getrennt)
      - "bool_attribut": filter ist eine Bedingung wie `ist_hitzeschutz=TRUE`
      - "leer": keine Einschränkung
    """
    s = (filter_str or "").strip()
    if not s:
        return "leer", []
    if "=" in s and not s.startswith("|"):
        return "bool_attribut", [s]
    parts = [p.strip() for p in s.split("|") if p.strip()]
    return "exakt_key", parts


def main() -> int:
    env = load_env(REPO / ".env")
    sa_path = resolve_sa_path(env, REPO)
    sheet = open_sheet(sa_path, DOC_ID)

    pdb = load_tab(sheet.worksheet("produktdatenbank"))
    sr = load_tab(sheet.worksheet("map_slot_rules"))
    cr = load_tab(sheet.worksheet("map_conflict_rules"))
    pf = load_tab(sheet.worksheet("map_pool_filter"))

    # Nur aktive Produkte + Regeln
    pdb_active = [p for p in pdb if (p.get("aktiv", "TRUE").upper() == "TRUE")]
    sr_active = [r for r in sr if (r.get("aktiv", "TRUE").upper() == "TRUE")]
    cr_active = [r for r in cr if (r.get("aktiv", "TRUE").upper() == "TRUE")]
    pf_active = [r for r in pf if (r.get("aktiv", "TRUE").upper() == "TRUE")]

    print(f"produktdatenbank: {len(pdb_active)} aktive Produkte")
    print(f"map_slot_rules: {len(sr_active)} aktive Regeln")
    print(f"map_conflict_rules: {len(cr_active)} aktive Regeln")
    print(f"map_pool_filter: {len(pf_active)} aktive Regeln")

    # Index: produktlinie → Produkte
    line_to_keys = {}
    for p in pdb_active:
        line = p.get("produktlinie", "").strip()
        if line:
            line_to_keys.setdefault(line, []).append(p["produkt_key"])

    # Produkte zum Audit: alle aktiven, minus already_audited
    to_audit = [p for p in pdb_active if p["produkt_key"] not in ALREADY_AUDITED]
    print(f"\nZu auditieren: {len(to_audit)} Produkte (8 bereits in Phase 3 geprüft)")

    md = [
        f"# Phase-4-Inventar — Routing-Aussage pro Produkt",
        "",
        f"Stand {datetime.now().strftime('%Y-%m-%d %H:%M')}.",
        f"Quelle: Live-Read von produktdatenbank + map_slot_rules + "
        f"map_conflict_rules + map_pool_filter.",
        "",
        f"Pro Produkt zusammengefasst, was das Routing-System über das "
        f"Produkt aussagt — als Briefing für die PDF-Verifikation in "
        f"Phase 4. Aussagen sind hierarchisch:",
        "",
        "1. **Direkt-REQ**: REQ-Regeln, die das Produkt namentlich im "
        "`filter` referenzieren — triggert das Produkt aktiv.",
        "2. **Linien-REQ**: REQ-Regeln, die die Produktlinie als filter "
        "haben — Produkt kann gewinnen, wenn es die Linie repräsentiert.",
        "3. **Bool-Attribut-REQ**: REQ-Regeln mit Bool-Filter "
        "(`ist_hitzeschutz=TRUE` etc.) — Produkt qualifiziert sich, "
        "wenn das Bool-Flag in Stammdaten gesetzt ist.",
        "4. **CON-Regeln**: schließen das Produkt aus.",
        "5. **Stammdaten-Filter**: kopfhaut/haarstaerke/haarstruktur/"
        "haarzustand + ausschluss_bei + pflegelevel + slot_typ.",
        "",
        "**Bereits in Phase 3 geprüft** (nicht hier): bond_iq_leave_in, "
        "bond_iq_night_day_serum, bond_iq_shampoo, bond_iq_spuelung, "
        "curl_creme, entwirrungsspray, moxie_mousse, volumen_spray.",
        "",
        "---",
        "",
    ]

    for p in sorted(to_audit, key=lambda x: x["produkt_key"]):
        key = p["produkt_key"]
        line = p.get("produktlinie", "")
        name = p.get("produktname_de", "")
        slot = p.get("slot_typ", "")
        haupt = p.get("hauptfunktion", "")
        neben = p.get("nebenfunktionen", "")
        kopfhaut = p.get("kopfhaut", "")
        haarstruktur = p.get("haarstruktur", "")
        haarstaerke = p.get("haarstaerke", "")
        haarzustand = p.get("haarzustand", "")
        ausschluss = p.get("ausschluss_bei", "")
        pflegelevel = p.get("pflegelevel", "")
        intensitaet = p.get("intensitaet", "")
        ist_hitzeschutz = p.get("ist_hitzeschutz", "")
        ist_bonding = p.get("ist_bonding", "")
        ist_scalp_focus = p.get("ist_scalp_focus", "")
        locken_geeignet = p.get("locken_geeignet", "")

        md.append(f"## {key} — {name}")
        md.append("")
        md.append(f"**Linie**: `{line}` · **Slot**: `{slot}` · **Pflegelevel**: `{pflegelevel}` · **Intensität**: `{intensitaet}`")
        md.append("")
        md.append(f"**Stammdaten-Funktion** (für PDF-Verifikation):")
        md.append(f"- hauptfunktion: `{haupt}`")
        md.append(f"- nebenfunktionen: `{neben}`")
        md.append("")
        md.append(f"**Stammdaten-Filter** (Zielgruppe laut Sheet):")
        md.append(f"- kopfhaut: `{kopfhaut}` · haarstruktur: `{haarstruktur}` · haarstaerke: `{haarstaerke}` · haarzustand: `{haarzustand}`")
        bool_flags = []
        if ist_hitzeschutz == "TRUE":
            bool_flags.append("ist_hitzeschutz")
        if ist_bonding == "TRUE":
            bool_flags.append("ist_bonding")
        if ist_scalp_focus == "TRUE":
            bool_flags.append("ist_scalp_focus")
        if locken_geeignet == "TRUE":
            bool_flags.append("locken_geeignet")
        if bool_flags:
            md.append(f"- bool-Flags: `{', '.join(bool_flags)}`")
        if ausschluss:
            md.append(f"- ausschluss_bei: `{ausschluss}`")
        md.append("")

        # Direkt-REQ + Linien-REQ + Bool-Attribut-REQ
        direct_req = []
        line_req = []
        bool_req = []
        for r in sr_active:
            kind, vals = parse_filter(r.get("filter", ""))
            if kind == "exakt_key":
                if key in vals:
                    direct_req.append(r)
                elif line and line in vals:
                    line_req.append(r)
            elif kind == "bool_attribut":
                # Prüfen, ob das Produkt das Bool erfüllt
                # (filter wie "ist_hitzeschutz=TRUE")
                cond = vals[0]
                if "=" in cond:
                    flag, val = cond.split("=", 1)
                    flag = flag.strip()
                    val = val.strip()
                    if p.get(flag, "").upper() == val.upper():
                        bool_req.append((r, cond))

        if direct_req:
            md.append("**Direkt-REQ-Routing** (Produkt namentlich im filter):")
            for r in direct_req:
                trigger = format_trigger(r)
                md.append(f"- `{r['regel_id']}` ({r.get('prioritaet','')}): WENN {trigger} → slot `{r.get('slot_typ','')}` (filter: `{r.get('filter','')}`)")
            md.append("")

        if line_req:
            md.append(f"**Linien-REQ-Routing** (filter referenziert produktlinie `{line}`):")
            for r in line_req:
                trigger = format_trigger(r)
                md.append(f"- `{r['regel_id']}` ({r.get('prioritaet','')}): WENN {trigger} → slot `{r.get('slot_typ','')}` (filter: `{r.get('filter','')}`)")
            md.append("")

        if bool_req:
            md.append("**Bool-Attribut-REQ-Routing** (Produkt erfüllt Bool-Bedingung):")
            for r, cond in bool_req:
                trigger = format_trigger(r)
                md.append(f"- `{r['regel_id']}` ({r.get('prioritaet','')}): WENN {trigger} → slot `{r.get('slot_typ','')}` (filter: `{cond}`)")
            md.append("")

        # CON-Regeln
        cons = []
        for c in cr_active:
            match_typ = c.get("match_typ", "")
            match_wert = c.get("match_wert", "")
            wert_list = [w.strip() for w in match_wert.split(",") if w.strip()]
            if match_typ == "produkt_key" and key in wert_list:
                cons.append(c)
            elif match_typ == "produktlinie" and line in wert_list:
                cons.append(c)
            elif match_typ == "key_contains":
                for w in wert_list:
                    if w in key:
                        cons.append(c)
                        break
        if cons:
            md.append("**CON-Regeln** (Produkt wird ausgeschlossen):")
            for c in cons:
                trigger = format_trigger(c)
                md.append(f"- `{c.get('konflikt_id','?')}`: WENN {trigger} → {c.get('action','')} (match: {c.get('match_typ','')}={c.get('match_wert','')})")
            md.append("")

        # Pool-Filter (selten produktspezifisch, aber sammeln)
        pfs = []
        for r in pf_active:
            cond = r.get("bedingung", "") + " " + r.get("filter", "")
            if key in cond or (line and line in cond):
                pfs.append(r)
        if pfs:
            md.append("**Pool-Filter-Referenzen** (kontextueller Pool-Ein-/Ausschluss):")
            for r in pfs:
                md.append(f"- `{r.get('regel_id','?')}`: {r.get('beschreibung', r.get('bedingung', ''))}")
            md.append("")

        if not (direct_req or line_req or bool_req or cons or pfs):
            md.append("_Keine direkten Routing-Referenzen — Produkt landet ausschließlich über Pool-Scoring (Node 12) im Slot. Audit-Fokus: Stammdaten oben passen zu PDF-Zielgruppe?_")
            md.append("")

        md.append("---")
        md.append("")

    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print(f"\nInventar geschrieben: {OUT_MD.relative_to(REPO)}")
    print(f"Produkte im Inventar: {len(to_audit)}")
    return 0


def format_trigger(r: dict) -> str:
    parts = []
    for f_key, v_key in [
        ("trigger_flag", "trigger_wert"),
        ("trigger_flag2", "trigger_wert2"),
    ]:
        f = r.get(f_key, "")
        v = r.get(v_key, "")
        if f:
            parts.append(f"`{f}={v}`" if v else f"`{f}`")
    return " AND ".join(parts) if parts else "(immer)"


if __name__ == "__main__":
    sys.exit(main())
