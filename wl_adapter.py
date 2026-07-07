"""
wl_adapter.py — Whitelabel-Bibliothek → produktdatenbank

Übersetzt die 11 UI-Felder aus demo/bibliothek.html-Mockup in die 25 Spalten
der laufenden produktdatenbank, kompatibel mit dem n8n-Workflow (Node 07
liefert diese 25 Spalten an Nodes 08/11/12/14).

Referenz-Beispielzeile aus test_results_20260701 (entwirrungsspray):
    {'produkt_key': 'entwirrungsspray', 'slot_typ': 'leave_in',
     'haarzustand': 'haarbruch,spliss', 'pflegelevel': 'MID,HIGH',
     'ist_hitzeschutz': 'FALSE', 'intensitaet': 'leicht', ...}

Format-Konventionen:
    - CSV-Separator: KOMMA
    - Booleans: Strings "TRUE" / "FALSE"
    - Sonderwerte: "alle" = alle Ausprägungen, "-" = irrelevant
    - Enums: kleinbuchstaben mit underscore
    - pflegelevel: SET aus {LOW, MID, HIGH}, in aufsteigender Reihenfolge

Bekannte Limits gegenüber MONAT-produktdatenbank (Isomorphie-Δ):
    - Mockup-UI kennt 11 Funktions-Tokens; real sind ~25 im Umlauf
    - Mockup-UI kennt 7 Slots; real gibt es 11 (kopfhaut_taeglich, nacht_serum,
      styling_3 nicht abbildbar)
    - produktlinie hardcodiert auf "eigen" (real 12 MONAT-Linien)
    - kombinationen / kombi_optional werden nicht gepflegt (V1)
    - hauptfunktion im Mockup ein primary + Sekundär-Liste; real kann
      hauptfunktion selbst mehrwertig sein (z.B. "reparatur,bonding")
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Iterable
import re
import unicodedata


# ---------------------------------------------------------------------------
# Vokabular — UI-Slug → DB-Token
# ---------------------------------------------------------------------------

# Slot-Wahl im Mockup → (slot_typ, produkttyp_default, routine_schritt)
SLOT_MAP: dict[str, tuple[str, str, int]] = {
    "shampoo":         ("shampoo",   "shampoo",   1),
    "spuelung":        ("spuelung",  "spuelung",  2),
    "maske":           ("maske",     "maske",     3),
    "kopfhaut":        ("kopfhaut",  "kopfhaut_treatment", 4),
    "leave_in":        ("leave_in",  "leave_in",  5),
    "styling":         ("styling_1", "styling",   6),
    "serum":           ("finish",    "serum",     8),
}

# Chip: Haupt-Nutzen — UI-Slug = DB-Token (1:1), damit Reverse eindeutig ist.
# Der Mockup zeigt freundliche Labels (z.B. "Anti-Frizz" für frizz_reduktion),
# die internen Enum-Werte sind identisch mit den DB-Tokens.
# Erweitert nach Isomorphie-Test 2026-07-07 um alle real vorkommenden Tokens.
UI_HAUPTNUTZEN: dict[str, str] = {t: t for t in [
    # Mockup-Chips (11)
    "feuchtigkeit", "reparatur", "glanz", "volumen", "bonding",
    "frizz_reduktion", "locken", "hitzeschutz", "kopfhautpflege",
    "entwirren", "halt",
    # Ergänzt nach Isomorphie-Report (mockup muss diese als Chips zeigen)
    "verdichtend", "staerkend", "kaemmbarkeit", "definition",
    "elastizitaet", "entgiftung", "farbschutz", "frische",
    "haarwuchs", "kraeftigend", "reinigung", "textur",
    "versiegelung", "wash_alternative", "auffrischung", "ausgleichend",
]}

UI_HAARSTRUKTUR = {"glatt": "glatt", "wellig": "wellig",
                   "lockig": "lockig", "kraus": "kraus"}
UI_HAARSTAERKE = {"fein": "fein", "mittel": "mittel", "dick": "dick"}
UI_HAARZUSTAND = {
    "normal": "normal", "trocken": "trocken", "glanzlos": "glanzlos",
    "gefaerbt": "gefaerbt", "blondiert": "blondiert",
    "kraftlos": "kraftlos", "duenn": "duenn", "frizz": "frizz",
    "spliss": "spliss", "haarbruch": "haarbruch",
    "stark_geschaedigt": "stark_geschaedigt",
}
UI_KOPFHAUT = {t: t for t in [
    "normal", "fettig", "schuppig", "juckend_empfindlich",
    "schnell_nachfettender_ansatz", "trocken",
]}
# 'alle' als Sonderwert für Produkte, die intensitäts-neutral wirken
UI_INTENSITAET = {t: t for t in ["leicht", "mittel", "intensiv", "alle"]}
# ausschluss_bei akzeptiert Union aller Struktur/Kopfhaut/Zustand-Tokens
UI_AUSSCHLUSS = {t: t for t in [
    "glatt", "wellig", "lockig", "kraus",
    "fein", "mittel", "dick",
    "normal", "fettig", "schuppig", "juckend_empfindlich",
    "trocken", "blondiert", "gefaerbt",
]}

# Reihenfolge der 25 Spalten wie in der Live-produktdatenbank
DB_COLUMNS = (
    "produkt_key", "produktname_de", "produktlinie", "produkttyp",
    "slot_typ", "routine_schritt", "kopfhaut", "haarstruktur",
    "haarstaerke", "haarzustand", "hauptfunktion", "nebenfunktionen",
    "pflegelevel", "ausschluss_bei", "ist_hitzeschutz", "ist_bonding",
    "ist_scalp_focus", "locken_geeignet", "kombinationen",
    "kombi_optional", "aktiv", "produkt_url", "anwendung",
    "intensitaet", "row_number",
)


# ---------------------------------------------------------------------------
# Datenklasse — was die Beraterin im UI eintippt/anklickt
# ---------------------------------------------------------------------------

@dataclass
class LibraryEntry:
    """
    Die 11 UI-Felder aus demo/bibliothek.html-Mockup plus 3 System-Felder,
    die nicht im UI erscheinen aber persistiert werden (produkt_key als
    stabiler Slug beim Speichern generiert, routine_schritt und produkttyp
    aus dem Original-Sheet durchgereicht wenn vorhanden).

    hauptnutzen_primary ist Liste — reale hauptfunktion kann mehrwertig
    sein ('reparatur,bonding'). Der Mockup zeigt heute einen Haupt-Chip;
    die Datenklasse hält 1..n aus.
    """
    produktname: str
    slot: str                                                     # SLOT_MAP-key
    hauptnutzen_primary: list[str] = field(default_factory=list)  # UI_HAUPTNUTZEN-keys
    hauptnutzen_secondary: list[str] = field(default_factory=list)
    haarstruktur: list[str] = field(default_factory=list)
    haarstaerke: list[str] = field(default_factory=list)
    haarzustand: list[str] = field(default_factory=list)
    kopfhaut: list[str] = field(default_factory=list)
    intensitaet: str = "mittel"                                   # UI_INTENSITAET-key
    ausschluss_bei: list[str] = field(default_factory=list)
    bezugsquelle: str = ""
    warum_sinnvoll: str = ""
    # System-Felder (kein UI, aber persistiert):
    produkt_key: str = ""       # leer → aus produktname slugifiziert
    routine_schritt: int = 0    # 0 → Default aus SLOT_MAP
    produkttyp: str = ""        # leer → Default aus SLOT_MAP
    # 12. UI-Feld (nach Isomorphie-Test 2026-07-07 als Chip-Multi ergänzt):
    pflegelevel: list[str] = field(default_factory=list)  # ["LOW","MID","HIGH"]-Untermenge


# ---------------------------------------------------------------------------
# Adapter forward
# ---------------------------------------------------------------------------

def to_produktdatenbank_row(
    e: LibraryEntry,
    row_number: int,
    produktlinie: str = "eigen",
) -> dict:
    """Erzeugt eine 25-Spalten-Zeile, kompatibel zu Node 07-Output."""
    slot_db, produkttyp_default, routine_schritt_default = SLOT_MAP[e.slot]

    hauptfunktion = _csv([UI_HAUPTNUTZEN[t] for t in e.hauptnutzen_primary])
    nebenfunktionen = _csv([UI_HAUPTNUTZEN[t] for t in e.hauptnutzen_secondary])

    # Bool-Flags NUR aus Haupt-Nutzen ableiten (Neben-Nutzen ist zu breit —
    # essig_shampoo hat kopfhautpflege sekundär, ist aber kein scalp_focus)
    primary_set = set(e.hauptnutzen_primary)

    return {
        "produkt_key":       e.produkt_key or _slugify(e.produktname),
        "produktname_de":    e.produktname,
        "produktlinie":      produktlinie,
        "produkttyp":        e.produkttyp or produkttyp_default,
        "slot_typ":          slot_db,
        "routine_schritt":   e.routine_schritt or routine_schritt_default,
        "kopfhaut":          _kopfhaut(e),
        "haarstruktur":      _multi_or_alle(e.haarstruktur, UI_HAARSTRUKTUR),
        "haarstaerke":       _multi_or_alle(e.haarstaerke, UI_HAARSTAERKE),
        "haarzustand":       _multi(e.haarzustand, UI_HAARZUSTAND) or "-",
        "hauptfunktion":     hauptfunktion,
        "nebenfunktionen":   nebenfunktionen,
        "pflegelevel":       _csv(e.pflegelevel) if e.pflegelevel else _pflegelevel(e.intensitaet, e.haarzustand),
        "ausschluss_bei":    _multi(e.ausschluss_bei, UI_AUSSCHLUSS),
        "ist_hitzeschutz":   _bool("hitzeschutz" in primary_set),
        "ist_bonding":       _bool("bonding" in primary_set),
        "ist_scalp_focus":   _bool("kopfhautpflege" in primary_set or e.slot == "kopfhaut"),
        "locken_geeignet":   _bool(bool({"lockig", "kraus"} & set(e.haarstruktur))),
        "kombinationen":     "",
        "kombi_optional":    "",
        "aktiv":             "TRUE",
        "produkt_url":       e.bezugsquelle,
        "anwendung":         e.warum_sinnvoll,
        "intensitaet":       UI_INTENSITAET.get(e.intensitaet, e.intensitaet),
        "row_number":        row_number,
    }


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def _csv(tokens: Iterable[str]) -> str:
    return ",".join(t for t in tokens if t)


def _multi(values: list[str], vocab: dict[str, str]) -> str:
    return _csv(vocab[v] for v in values if v in vocab)


def _multi_or_alle(values: list[str], vocab: dict[str, str]) -> str:
    """Wenn alle Ausprägungen gewählt sind, kompaktes 'alle' schreiben."""
    if len(values) == len(vocab):
        return "alle"
    return _multi(values, vocab)


def _kopfhaut(e: LibraryEntry) -> str:
    """Slot != kopfhaut UND keine Auswahl → '-' (irrelevant)."""
    if not e.kopfhaut and e.slot != "kopfhaut":
        return "-"
    return _multi_or_alle(e.kopfhaut, UI_KOPFHAUT)


def _bool(b: bool) -> str:
    return "TRUE" if b else "FALSE"


# haarzustand-Tokens, die HIGH-Bedarf signalisieren
_HIGH_MARKER = {"stark_geschaedigt", "spliss", "haarbruch", "blondiert"}
# haarzustand-Tokens, die MID-Bedarf signalisieren
_MID_MARKER = {"trocken", "glanzlos", "gefaerbt", "kraftlos", "frizz", "duenn"}


def _pflegelevel(intensitaet: str, haarzustand: list[str]) -> str:
    """
    Ableitung: welche Pflegelevel-Bedürfnisse deckt das Produkt ab.

    Semantik (abwärtskompatibel, nach Isomorphie-Test 2026-07-07):
    ein Produkt für HIGH-Bedarf ist auch für MID-Profile geeignet;
    ein Produkt für MID-Bedarf auch für LOW.

    Marker aus haarzustand setzen die Obergrenze:
      - stark_geschaedigt/spliss/haarbruch/blondiert → HIGH
      - trocken/glanzlos/gefaerbt/kraftlos/frizz/duenn → MID
      - sonst (leer/normal) → LOW

    intensitaet setzt zusätzlich das Mindestmaß:
      - "intensiv" → mindestens HIGH (LOW raus)
      - "mittel"   → mindestens MID
      - "leicht"   → keine Erhöhung
      - "alle"     → alle drei Levels
    """
    if intensitaet == "alle":
        return "LOW,MID,HIGH"

    hz = set(haarzustand)
    if hz & _HIGH_MARKER:
        top = "HIGH"
    elif hz & _MID_MARKER:
        top = "MID"
    else:
        top = "LOW"

    if intensitaet == "intensiv" and top != "HIGH":
        top = "HIGH"
    elif intensitaet == "mittel" and top == "LOW":
        top = "MID"

    # abwärts-kompatible Expansion
    if top == "HIGH":
        levels = ["MID", "HIGH"] if intensitaet == "intensiv" else ["LOW", "MID", "HIGH"]
    elif top == "MID":
        levels = ["LOW", "MID"]
    else:
        levels = ["LOW"]

    # intensiv schließt LOW aus
    if intensitaet == "intensiv":
        levels = [l for l in levels if l != "LOW"]

    return _csv(levels)


def _slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s.lower()).strip("_")
    return s


# ---------------------------------------------------------------------------
# Adapter reverse — 25 DB-Spalten → 11 UI-Felder
# ---------------------------------------------------------------------------
#
# Für den Isomorphie-Test: nimmt eine DB-Zeile (z.B. aus MONAT-Sheet),
# projiziert sie in ein LibraryEntry, und die anschließende Forward-Runde
# muss möglichst wieder dieselbe DB-Zeile ergeben. Δ misst den Info-Verlust
# des UI-Vokabulars.
#
# Bekannter, unvermeidbarer Info-Verlust (im Reverse verworfen, wird beim
# Forward NICHT rekonstruiert; erwarteter Δ-Beitrag):
#   - produktlinie (12 MONAT-Linien → Forward hardcodiert "eigen")
#   - kombinationen / kombi_optional (Produkt-zu-Produkt-Referenzen)
#   - produkttyp-Feinheiten (finish_oel vs finish_treatment vs serum werden
#     alle im UI zu "Serum"→"finish")
#   - Slots kopfhaut_taeglich, nacht_serum, styling_2, styling_3 (nicht im UI)
#   - Funktions-Tokens jenseits der 11 Mockup-Chips (auffrischung, definition,
#     elastizitaet, entgiftung, farbschutz, frische, haarwuchs, kaemmbarkeit,
#     kraeftigend, reinigung, staerkend, textur, verdichtend, versiegelung,
#     wash_alternative)
#   - pflegelevel-Set wird beim Forward neu abgeleitet — kann vom gespeicherten
#     Set abweichen

REVERSE_HAUPTNUTZEN = {v: k for k, v in UI_HAUPTNUTZEN.items()}
REVERSE_HAARSTRUKTUR = {v: k for k, v in UI_HAARSTRUKTUR.items()}
REVERSE_HAARSTAERKE = {v: k for k, v in UI_HAARSTAERKE.items()}
REVERSE_HAARZUSTAND = {v: k for k, v in UI_HAARZUSTAND.items()}
REVERSE_KOPFHAUT = {v: k for k, v in UI_KOPFHAUT.items()}
REVERSE_AUSSCHLUSS = {v: k for k, v in UI_AUSSCHLUSS.items()}

# slot_typ → UI-Slot (mit Fallback-Zuordnung für Slots ohne UI-Repräsentation)
REVERSE_SLOT = {
    "shampoo":           "shampoo",
    "spuelung":          "spuelung",
    "maske":             "maske",
    "kopfhaut":          "kopfhaut",
    "kopfhaut_taeglich": "kopfhaut",   # Δ: kein Sub-Slot im UI
    "leave_in":          "leave_in",
    "styling_1":         "styling",
    "styling_2":         "styling",    # Δ: kein Sub-Slot im UI
    "styling_3":         "styling",    # Δ: kein Sub-Slot im UI
    "finish":            "serum",
    "nacht_serum":       "serum",      # Δ: kein Sub-Slot im UI
}


def from_produktdatenbank_row(row: dict) -> tuple["LibraryEntry", list[str]]:
    """
    Reverse: DB-Zeile → LibraryEntry. Zusätzlich Liste von Δ-Warnungen
    für den Isomorphie-Report (z.B. "hauptfunktion-Token 'verdichtend'
    nicht im UI-Vokabular").
    """
    warnings: list[str] = []

    slot = REVERSE_SLOT.get(row["slot_typ"])
    if slot is None:
        warnings.append(f"unbekannter slot_typ '{row['slot_typ']}' → 'shampoo'")
        slot = "shampoo"
    elif row["slot_typ"] in {"kopfhaut_taeglich", "styling_2", "styling_3", "nacht_serum"}:
        warnings.append(f"slot_typ '{row['slot_typ']}' auf UI-Slot '{slot}' verschmolzen")

    haupt_tokens = _split(row.get("hauptfunktion", ""))
    neben_tokens = _split(row.get("nebenfunktionen", ""))

    hauptnutzen_primary, unmapped_h = _map_reverse(haupt_tokens, REVERSE_HAUPTNUTZEN)
    hauptnutzen_secondary, unmapped_n = _map_reverse(neben_tokens, REVERSE_HAUPTNUTZEN)
    for tok in unmapped_h:
        warnings.append(f"hauptfunktion-Token '{tok}' nicht im UI-Vokabular")
    for tok in unmapped_n:
        warnings.append(f"nebenfunktionen-Token '{tok}' nicht im UI-Vokabular")

    haarstruktur = _reverse_multi(row.get("haarstruktur", ""), REVERSE_HAARSTRUKTUR, UI_HAARSTRUKTUR)
    haarstaerke = _reverse_multi(row.get("haarstaerke", ""), REVERSE_HAARSTAERKE, UI_HAARSTAERKE)
    # haarzustand='-' bedeutet leer, kein Token
    hz_raw_str = row.get("haarzustand", "")
    haarzustand_raw = [] if hz_raw_str == "-" else _split(hz_raw_str)
    haarzustand, unmapped_hz = _map_reverse(haarzustand_raw, REVERSE_HAARZUSTAND)
    for tok in unmapped_hz:
        warnings.append(f"haarzustand-Token '{tok}' nicht im UI-Vokabular")

    kopfhaut_raw = row.get("kopfhaut", "")
    if kopfhaut_raw == "-":
        kopfhaut: list[str] = []
    else:
        kopfhaut_tokens = _split(kopfhaut_raw)
        kopfhaut, unmapped_k = _map_reverse(kopfhaut_tokens, REVERSE_KOPFHAUT)
        for tok in unmapped_k:
            warnings.append(f"kopfhaut-Token '{tok}' nicht im UI-Vokabular")

    intensitaet = row.get("intensitaet", "mittel")
    # 'alle' ist im UI seit Isomorphie-Test 2026-07-07 zugelassen

    ausschluss = _reverse_ausschluss(row.get("ausschluss_bei", ""), warnings)

    if row.get("produktlinie", "") not in ("", "eigen"):
        warnings.append(f"produktlinie='{row['produktlinie']}' geht beim Reverse verloren")
    if row.get("kombinationen", "") or row.get("kombi_optional", ""):
        warnings.append("kombinationen/kombi_optional gehen beim Reverse verloren")

    entry = LibraryEntry(
        produktname=row.get("produktname_de", ""),
        slot=slot,
        hauptnutzen_primary=hauptnutzen_primary,
        hauptnutzen_secondary=hauptnutzen_secondary,
        haarstruktur=haarstruktur,
        haarstaerke=haarstaerke,
        haarzustand=haarzustand,
        kopfhaut=kopfhaut,
        intensitaet=intensitaet,
        ausschluss_bei=ausschluss,
        bezugsquelle=row.get("produkt_url", ""),
        warum_sinnvoll=row.get("anwendung", ""),
        # System-Felder durchreichen (siehe LibraryEntry-Doku)
        produkt_key=row.get("produkt_key", ""),
        routine_schritt=int(row.get("routine_schritt", 0) or 0),
        produkttyp=row.get("produkttyp", ""),
        pflegelevel=_split(row.get("pflegelevel", "")),
    )
    return entry, warnings


def _split(csv: str) -> list[str]:
    return [t.strip() for t in csv.split(",") if t.strip()]


def _map_reverse(tokens: list[str], vocab: dict[str, str]) -> tuple[list[str], list[str]]:
    mapped: list[str] = []
    unmapped: list[str] = []
    for t in tokens:
        if t in vocab:
            mapped.append(vocab[t])
        else:
            unmapped.append(t)
    return mapped, unmapped


def _reverse_multi(value: str, reverse_vocab: dict[str, str],
                   forward_vocab: dict[str, str]) -> list[str]:
    """Sonderwert 'alle' expandiert zurück auf komplette Auswahl."""
    if value == "alle":
        return list(forward_vocab.keys())
    tokens = _split(value)
    return [reverse_vocab[t] for t in tokens if t in reverse_vocab]


def _reverse_ausschluss(value: str, warnings: list[str]) -> list[str]:
    """ausschluss_bei mischt Struktur/Kopfhaut/Zustand-Tokens — Reverse via
    Union aller UI-Ausschluss-Vokabulare, unbekannte Tokens als Warnung."""
    if not value:
        return []
    tokens = _split(value)
    out: list[str] = []
    for t in tokens:
        if t in REVERSE_AUSSCHLUSS:
            out.append(REVERSE_AUSSCHLUSS[t])
        else:
            warnings.append(f"ausschluss_bei-Token '{t}' nicht im UI-Vokabular")
    return out


# ---------------------------------------------------------------------------
# Selbst-Test (`python3 wl_adapter.py`)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Renew-Shampoo-Beispiel aus dem Mockup (bibliothek.html Zeile 431-549)
    renew = LibraryEntry(
        produktname="Renew Shampoo",
        slot="shampoo",
        hauptnutzen_primary=["feuchtigkeit"],
        hauptnutzen_secondary=["reparatur", "glanz"],
        haarstruktur=["glatt", "wellig", "lockig"],
        haarstaerke=["fein", "mittel"],
        haarzustand=["trocken", "glanzlos", "gefaerbt"],
        kopfhaut=["normal"],
        intensitaet="mittel",
        ausschluss_bei=[],
        bezugsquelle="https://mymonat.com/de/…",
        warum_sinnvoll=(
            "Weil dieses Shampoo speziell für coloriertes Haar entwickelt "
            "wurde und die Farbe schützt, während es tief mit Feuchtigkeit "
            "versorgt."
        ),
    )
    row = to_produktdatenbank_row(renew, row_number=1)

    from pprint import pprint
    pprint(row, sort_dicts=False)

    # Sanity: alle 25 Spalten produziert, keine Auslassungen
    missing = set(DB_COLUMNS) - set(row.keys())
    extra = set(row.keys()) - set(DB_COLUMNS)
    assert not missing, f"fehlende Spalten: {missing}"
    assert not extra, f"unbekannte Spalten: {extra}"
    print("\nOK — 25 Spalten vollständig, Reihenfolge kompatibel.")

    # Round-Trip: forward → reverse → forward, sollte identisch sein
    print("\n--- Round-Trip-Test ---")
    entry2, warns = from_produktdatenbank_row(row)
    row2 = to_produktdatenbank_row(entry2, row_number=1)
    diffs = [c for c in DB_COLUMNS if row.get(c) != row2.get(c)]
    if diffs:
        print(f"Δ in Spalten: {diffs}")
        for c in diffs:
            print(f"  {c}: {row.get(c)!r} → {row2.get(c)!r}")
    else:
        print("OK — Round-Trip identisch.")
    if warns:
        print(f"Warnungen: {warns}")

    # Reverse-Test mit realer MONAT-Zeile (Entwirrungsspray aus test_results)
    print("\n--- Reverse-Test mit realer MONAT-Zeile ---")
    real = {
        "produkt_key": "entwirrungsspray",
        "produktname_de": "Entwirrungs-Spray",
        "produktlinie": "basis",
        "produkttyp": "leave_in",
        "slot_typ": "leave_in",
        "routine_schritt": 5,
        "kopfhaut": "-",
        "haarstruktur": "alle",
        "haarstaerke": "alle",
        "haarzustand": "haarbruch,spliss",
        "hauptfunktion": "entwirren",
        "nebenfunktionen": "feuchtigkeit,frizz_reduktion,glanz,staerkend,kaemmbarkeit",
        "pflegelevel": "MID,HIGH",
        "ausschluss_bei": "",
        "ist_hitzeschutz": "FALSE",
        "ist_bonding": "FALSE",
        "ist_scalp_focus": "FALSE",
        "locken_geeignet": "TRUE",
        "kombinationen": "",
        "kombi_optional": "rejuvabeads",
        "aktiv": "TRUE",
        "produkt_url": "",
        "anwendung": "Auf das handtuchtrockene Haar sprühen …",
        "intensitaet": "leicht",
        "row_number": 9,
    }
    entry_real, warns_real = from_produktdatenbank_row(real)
    row_back = to_produktdatenbank_row(entry_real, row_number=9)
    diffs2 = [c for c in DB_COLUMNS if real.get(c) != row_back.get(c)]
    print(f"Δ-Spalten: {diffs2}")
    for c in diffs2:
        print(f"  {c}: {real.get(c)!r} → {row_back.get(c)!r}")
    print(f"\nReverse-Warnungen ({len(warns_real)}):")
    for w in warns_real:
        print(f"  - {w}")
