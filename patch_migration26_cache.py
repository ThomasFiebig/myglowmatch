#!/usr/bin/env python3
"""
Migration #26 — Cache-Layer via workflowStaticData mit TTL (2026-07-01).

Baut den Live-Workflow um:
  1. Cache-Check + IF-Split + Cache-Write + Merge zwischen Node 02 und Node 04
  2. Loader-Chain 04a→...→13 in den FALSE-Branch der IF-Node
  3. 7 Verbraucher-Nodes bekommen Cache-Fallback-Snippet

TTL 6h. Kein Purge-Endpoint — bei Sheet-Edit entweder max 6h warten oder
in n8n-UI (Workflow > Data > Clear Static Data) manuell nullen.

Sinn:
  - Robustheit gegen Google-Sheets-Ausfall bis zu 6h (Cache liefert weiter)
  - Weniger API-Calls (bei künftiger Skalierung)

Ablauf:
  1. GET Live-Workflow via n8n-API
  2. Backup als workflow_backup_20260701_pre_migration26.json
  3. In-Memory-Umbau (nodes + connections + jsCode-Patches)
  4. Lokale Kopie workflow_migration26_v1.json
  5. PUT — bei HTTP 400 Merge-typeVersion=3→2 downgrade und erneut versuchen
  6. GET-Verifikation
"""

import json
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

BASE_DIR = Path(__file__).parent
BACKUP_PATH = BASE_DIR / "workflow_backup_20260701_pre_migration26.json"
OUT_PATH = BASE_DIR / "workflow_migration26_v1.json"
WORKFLOW_ID = "pwSWA5NatKiLhueB"

TTL_HOURS = 6

# --- Loader → Cache-Key + Verbraucher-Mapping ---
CACHE_TABS = [
    ("priorities",            "04a Prioritäten laden"),
    ("derived_variables",     "05a map_derived_variables laden"),
    ("pflegelevel_scoring",   "06a Pflegelevel-Scoring laden"),
    ("pflegelevel_overrides", "06b Pflegelevel-Overrides laden"),
    ("max_products",          "06c Max-Products laden"),
    ("profil_funktion",       "06d Profil-Funktion-Mapping laden"),
    ("produktdatenbank",      "07 Produktdatenbank laden"),
    ("pool_filter",           "08a Pool-Filter laden"),
    ("slot_rules",            "10 map_slot_rules"),
    ("conflict_rules",        "13 Konfliktregeln laden"),
]

# String-Replaces pro Verbraucher-Node (jsCode). Alt muss EXAKT und EINDEUTIG vorkommen.
CONSUMER_PATCHES = [
    ("04 Prioritäten auflösen", [
        ('const priorityRules = $items("04a Prioritäten laden")',
         'const priorityRules = _fromCache("priorities", "04a Prioritäten laden")'),
    ]),
    ("05 Bool-Flags berechnen", [
        ('const sheetRows = $items("05a map_derived_variables laden")',
         'const sheetRows = _fromCache("derived_variables", "05a map_derived_variables laden")'),
    ]),
    ("06 Pflegelevel berechnen", [
        ('const scoringRules = $items("06a Pflegelevel-Scoring laden")',
         'const scoringRules = _fromCache("pflegelevel_scoring", "06a Pflegelevel-Scoring laden")'),
        ('const overrideRules = $items("06b Pflegelevel-Overrides laden")',
         'const overrideRules = _fromCache("pflegelevel_overrides", "06b Pflegelevel-Overrides laden")'),
        ('const maxRules = $items("06c Max-Products laden")',
         'const maxRules = _fromCache("max_products", "06c Max-Products laden")'),
    ]),
    ("08 Ausschluss-Filter", [
        ('const allProducts = $items("07 Produktdatenbank laden").map(it => it.json);',
         'const allProducts = _fromCache("produktdatenbank", "07 Produktdatenbank laden").map(it => it.json);'),
        ('const poolRules = $items("08a Pool-Filter laden")',
         'const poolRules = _fromCache("pool_filter", "08a Pool-Filter laden")'),
    ]),
    ("11 REQ-Regeln auswerten", [
        ('const ruleItems = $items("10 map_slot_rules");',
         'const ruleItems = _fromCache("slot_rules", "10 map_slot_rules");'),
    ]),
    ("12 Scoring & Slot-Befüllung", [
        ('const profilMapping = $items("06d Profil-Funktion-Mapping laden")',
         'const profilMapping = _fromCache("profil_funktion", "06d Profil-Funktion-Mapping laden")'),
    ]),
    ("14 Konflikte auflösen", [
        ('const rules = $items("13 Konfliktregeln laden").map(item => item.json);',
         'const rules = _fromCache("conflict_rules", "13 Konfliktregeln laden").map(item => item.json);'),
    ]),
]

FALLBACK_PREAMBLE = (
    "// [Migration #26] Cache-Fallback: Cache lesen, sonst Loader.\n"
    "const _c26 = $getWorkflowStaticData('global').cache?.tabs || {};\n"
    "const _fromCache = (key, loaderNode) => {\n"
    "  if (_c26[key] && _c26[key].length) return _c26[key].map(json => ({ json }));\n"
    "  return $items(loaderNode);\n"
    "};\n"
)
PREAMBLE_MARKER = "[Migration #26] Cache-Fallback"


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


def api_call(base_url: str, path: str, api_key: str, method: str = "GET", body=None):
    url = f"{base_url.rstrip('/')}/api/v1{path}"
    data = None
    headers = {"X-N8N-API-KEY": api_key, "Accept": "application/json"}
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode("utf-8"))


def new_id() -> str:
    return str(uuid.uuid4())


def build_cache_check_node() -> dict:
    js = (
        "// [Migration #26] Cache-Check: prüft ob workflowStaticData einen frischen Snapshot hält.\n"
        f"const TTL_MS = {TTL_HOURS} * 60 * 60 * 1000;\n"
        "const store = $getWorkflowStaticData('global');\n"
        "const age = Date.now() - (store.cache?.ts || 0);\n"
        "const cache_valid = !!(store.cache && store.cache.tabs && age < TTL_MS);\n"
        "return items.map(item => ({\n"
        "  json: { ...item.json, __cache_valid: cache_valid, __cache_age_min: Math.round(age / 60000) }\n"
        "}));\n"
    )
    return {
        "parameters": {"jsCode": js},
        "id": new_id(),
        "name": "Cache prüfen",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [80, 64],
    }


def build_cache_if_node() -> dict:
    return {
        "parameters": {
            "conditions": {
                "options": {
                    "caseSensitive": True,
                    "leftValue": "",
                    "typeValidation": "strict",
                    "version": 3,
                },
                "conditions": [
                    {
                        "id": new_id(),
                        "leftValue": "={{ $json.__cache_valid }}",
                        "rightValue": True,
                        "operator": {
                            "type": "boolean",
                            "operation": "true",
                            "singleValue": True,
                        },
                    }
                ],
                "combinator": "and",
            },
            "options": {},
        },
        "id": new_id(),
        "name": "IF Cache gültig",
        "type": "n8n-nodes-base.if",
        "typeVersion": 2.3,
        "position": [240, 64],
    }


def build_cache_write_node() -> dict:
    tabs_lines = ",\n".join(
        f"    {key}: $items({name!r}).map(i => i.json)"
        for key, name in CACHE_TABS
    )
    js = (
        "// [Migration #26] Cache schreiben. Baut store.cache.tabs auf.\n"
        "const store = $getWorkflowStaticData('global');\n"
        "store.cache = {\n"
        "  ts: Date.now(),\n"
        "  tabs: {\n"
        f"{tabs_lines}\n"
        "  },\n"
        "};\n"
        "// WICHTIG: Kunden-Payload zurückgeben, nicht Sheet-Rows — sonst zerlegt Merge den Datenfluss.\n"
        "return $items('02 Felder extrahieren').map(i => ({ json: i.json }));\n"
    )
    return {
        "parameters": {"jsCode": js},
        "id": new_id(),
        "name": "Cache schreiben",
        "type": "n8n-nodes-base.code",
        "typeVersion": 2,
        "position": [2200, -320],
    }


def build_merge_node(type_version: float = 3) -> dict:
    if type_version >= 3:
        params = {"mode": "combine", "combineBy": "combineByPosition", "options": {}}
    else:
        params = {"mode": "combineByPosition", "options": {}}
    return {
        "parameters": params,
        "id": new_id(),
        "name": "Cache Merge",
        "type": "n8n-nodes-base.merge",
        "typeVersion": type_version,
        "position": [400, 64],
    }


def patch_consumer(node: dict, patches: list) -> None:
    code = node["parameters"]["jsCode"]
    if PREAMBLE_MARKER not in code:
        code = FALLBACK_PREAMBLE + "\n" + code
    for old, new in patches:
        if old not in code:
            raise RuntimeError(
                f"Patch-Zeile in Node {node['name']!r} nicht gefunden:\n  {old!r}"
            )
        if code.count(old) != 1:
            raise RuntimeError(
                f"Patch-Zeile in Node {node['name']!r} nicht eindeutig ({code.count(old)}x):\n  {old!r}"
            )
        code = code.replace(old, new)
    node["parameters"]["jsCode"] = code


def rewire_connections(wf: dict, merge_name: str, cache_check: str, cache_if: str,
                       cache_write: str) -> None:
    conns = wf["connections"]

    def link(src: str, dst: str, src_index: int = 0, dst_index: int = 0):
        entry = conns.setdefault(src, {"main": []})
        while len(entry["main"]) <= src_index:
            entry["main"].append([])
        entry["main"][src_index].append({"node": dst, "type": "main", "index": dst_index})

    def drop(src: str):
        conns.pop(src, None)

    # 02 → Cache prüfen (statt 02 → 04a)
    drop("02 Felder extrahieren")
    link("02 Felder extrahieren", cache_check)

    # Cache prüfen → IF
    link(cache_check, cache_if)

    # IF: true → Merge input 0, false → 04a
    link(cache_if, merge_name, src_index=0, dst_index=0)
    link(cache_if, "04a Prioritäten laden", src_index=1)

    # Loader-Kette 04a → 05a → 06a → 06b → 06c → 06d → 07 → 08a → 10 → 13
    loader_chain = [name for _, name in CACHE_TABS]
    for src, dst in zip(loader_chain, loader_chain[1:]):
        drop(src)
        link(src, dst)
    # 13 → Cache schreiben (statt 13 → 14)
    drop(loader_chain[-1])
    link(loader_chain[-1], cache_write)

    # Cache schreiben → Merge input 1
    link(cache_write, merge_name, src_index=0, dst_index=1)

    # Merge → 04
    link(merge_name, "04 Prioritäten auflösen")

    # Verbraucher-Ketten (die Sub-Links, die durch Loader-Umbiegung obsolet werden)
    drop("04 Prioritäten auflösen"); link("04 Prioritäten auflösen", "05 Bool-Flags berechnen")
    drop("05 Bool-Flags berechnen"); link("05 Bool-Flags berechnen", "06 Pflegelevel berechnen")
    drop("06 Pflegelevel berechnen"); link("06 Pflegelevel berechnen", "08 Ausschluss-Filter")
    drop("09 Pool validieren"); link("09 Pool validieren", "11 REQ-Regeln auswerten")
    drop("11 REQ-Regeln auswerten"); link("11 REQ-Regeln auswerten", "14 Konflikte auflösen")
    # 08→09, 14→12, 12→15, 15→17, 17→{19,Test-Mode-Check}, Test-Mode-Check→18/18b bleiben.


def scrub_top_level(wf: dict) -> None:
    for k in ("id", "createdAt", "updatedAt", "versionId", "triggerCount", "tags", "shared",
             "active", "meta", "isArchived", "homeProject", "scopes", "pinData",
             "activeVersion", "activeVersionId", "sourceWorkflowId", "nodeGroups",
             "versionCounter", "description", "staticData"):
        wf.pop(k, None)
    allowed_settings = {"executionOrder", "saveExecutionProgress", "saveManualExecutions",
                        "saveDataErrorExecution", "saveDataSuccessExecution", "errorWorkflow",
                        "timezone", "executionTimeout"}
    if "settings" in wf and isinstance(wf["settings"], dict):
        wf["settings"] = {k: v for k, v in wf["settings"].items() if k in allowed_settings}


def build_patched_workflow(wf: dict, merge_type_version: float):
    cache_check = build_cache_check_node()
    cache_if = build_cache_if_node()
    cache_write = build_cache_write_node()
    merge = build_merge_node(merge_type_version)

    wf["nodes"].extend([cache_check, cache_if, cache_write, merge])

    for node_name, patches in CONSUMER_PATCHES:
        node = next((n for n in wf["nodes"] if n["name"] == node_name), None)
        if node is None:
            raise RuntimeError(f"Verbraucher-Node {node_name!r} nicht gefunden.")
        patch_consumer(node, patches)

    rewire_connections(
        wf,
        merge_name=merge["name"],
        cache_check=cache_check["name"],
        cache_if=cache_if["name"],
        cache_write=cache_write["name"],
    )

    scrub_top_level(wf)
    return wf


def main():
    env = load_env(BASE_DIR / ".env")
    api_key = env.get("N8N_API_KEY")
    base_url = env.get("N8N_BASE_URL")
    if not api_key or not base_url:
        print("FEHLER: N8N_API_KEY/N8N_BASE_URL fehlt in .env", file=sys.stderr)
        return 1

    print(f"[1/5] GET workflow {WORKFLOW_ID} …")
    wf = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)

    print(f"[2/5] Backup → {BACKUP_PATH.name}")
    BACKUP_PATH.write_text(json.dumps(wf, indent=2, ensure_ascii=False))

    print(f"[3/5] In-Memory-Umbau (Merge typeVersion=3, TTL={TTL_HOURS}h)")
    wf_patched = build_patched_workflow(json.loads(json.dumps(wf)), merge_type_version=3)
    OUT_PATH.write_text(json.dumps(wf_patched, indent=2, ensure_ascii=False))
    print(f"      lokale Kopie → {OUT_PATH.name}")

    print(f"[4/5] PUT workflow {WORKFLOW_ID} …")
    try:
        api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf_patched)
        print("      ✓ Deploy erfolgreich (Merge v3).")
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"      ✗ HTTP {e.code}: {body[:400]}")
        if e.code == 400 and "merge" in body.lower():
            print("      → Fallback: Merge typeVersion=3→2, erneut versuchen")
            wf_patched = build_patched_workflow(json.loads(json.dumps(wf)), merge_type_version=2)
            OUT_PATH.write_text(json.dumps(wf_patched, indent=2, ensure_ascii=False))
            try:
                api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key, method="PUT", body=wf_patched)
                print("      ✓ Deploy erfolgreich (Merge v2).")
            except urllib.error.HTTPError as e2:
                body2 = e2.read().decode("utf-8", errors="replace")
                print(f"      ✗ Auch v2 gescheitert: HTTP {e2.code}: {body2[:400]}")
                return 1
        else:
            return 1

    print(f"[5/5] Verifikation via GET …")
    verify = api_call(base_url, f"/workflows/{WORKFLOW_ID}", api_key)
    expected = {"Cache prüfen", "IF Cache gültig", "Cache schreiben", "Cache Merge"}
    present = {n["name"] for n in verify["nodes"]}
    missing = expected - present
    if missing:
        print(f"      ✗ Fehlend nach PUT: {missing}")
        return 1
    consumer_ok = 0
    for node_name, _ in CONSUMER_PATCHES:
        node = next(n for n in verify["nodes"] if n["name"] == node_name)
        if PREAMBLE_MARKER in node["parameters"]["jsCode"]:
            consumer_ok += 1
    print(f"      ✓ Alle 4 neuen Nodes vorhanden, {consumer_ok}/7 Verbraucher enthalten Cache-Fallback.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
