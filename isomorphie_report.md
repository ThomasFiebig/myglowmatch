# Isomorphie-Report — wl_adapter gegen MONAT-produktdatenbank
**Datenquelle:** `test_results_20260701_115939.json`  
**Produkte getestet:** 37  
**Methode:** jede Original-Zeile durch `from_produktdatenbank_row` (Reverse) → `to_produktdatenbank_row` (Forward); Δ pro Spalte.

## Δ pro Spalte
| Spalte | Δ-Anzahl | Kategorie | Beispiele |
|---|---|---|---|
| `slot_typ` | 5 / 37 | Adapter-Δ | `ir_clinical_kopfhautserum`: `kopfhaut_taeglich` → `kopfhaut`; `scalp_comfort_serum`: `kopfhaut_taeglich` → `kopfhaut`; `curl_auffrischer`: `styling_3` → `styling_1` |
| `kombinationen` | 22 / 37 | **Design (erwartet)** | `erweiterte_feuchtigkeit_spuelung`: `feuchtigkeits_shampoo` → ``; `feuchtigkeits_shampoo`: `erweiterte_feuchtigkeit_spuelung` → ``; `ir_clinical_shampoo`: `ir_clinical_spuelung` → `` |
| `kombi_optional` | 29 / 37 | **Design (erwartet)** | `entwirrungsspray`: `rejuvabeads` → ``; `erweiterte_feuchtigkeit_spuelung`: `super_feuchtigkeitsmaske` → ``; `feuchtigkeits_shampoo`: `super_feuchtigkeitsmaske` → `` |

## Reverse-Warnungen (aggregiert)
| Warnungs-Kategorie | Vorkommen | Beispiel |
|---|---|---|
| kombinationen/kombi_optional | 35 | `entwirrungsspray`: kombinationen/kombi_optional gehen beim Reverse verloren |
| produktlinie='studio_one' | 5 | `fohncreme`: produktlinie='studio_one' geht beim Reverse verloren |
| slot_typ | 5 | `ir_clinical_kopfhautserum`: slot_typ 'kopfhaut_taeglich' auf UI-Slot 'kopfhaut' verschmolzen |
| produktlinie='basis' | 4 | `entwirrungsspray`: produktlinie='basis' geht beim Reverse verloren |
| produktlinie='smoothing' | 4 | `smoothing_deep_conditioner`: produktlinie='smoothing' geht beim Reverse verloren |
| produktlinie='bond_iq' | 4 | `bond_iq_leave_in`: produktlinie='bond_iq' geht beim Reverse verloren |
| produktlinie='erw_feuchtigkeit' | 3 | `erweiterte_feuchtigkeit_spuelung`: produktlinie='erw_feuchtigkeit' geht beim Reverse verloren |
| produktlinie='ir_clinical' | 3 | `ir_clinical_kopfhautserum`: produktlinie='ir_clinical' geht beim Reverse verloren |
| produktlinie='reinigende' | 3 | `kopfhaut_peeling`: produktlinie='reinigende' geht beim Reverse verloren |
| produktlinie='curl_perfection' | 3 | `curl_auffrischer`: produktlinie='curl_perfection' geht beim Reverse verloren |
| produktlinie='renew' | 3 | `renew_shampoo`: produktlinie='renew' geht beim Reverse verloren |
| produktlinie='volumen' | 2 | `revitalize_spuelung`: produktlinie='volumen' geht beim Reverse verloren |
| produktlinie='scalp_comfort' | 2 | `scalp_comfort_behandlung`: produktlinie='scalp_comfort' geht beim Reverse verloren |
| produktlinie='monat_black' | 1 | `monat_black`: produktlinie='monat_black' geht beim Reverse verloren |

## Pro-Produkt Δ-Verteilung
| Produkt | Δ-Spalten | Warnungen |
|---|---|---|
| `bond_iq_night_day_serum` | 3 | 3 |
| `erweiterte_feuchtigkeit_spuelung` | 2 | 2 |
| `feuchtigkeits_shampoo` | 2 | 2 |
| `ir_clinical_kopfhautserum` | 2 | 3 |
| `ir_clinical_shampoo` | 2 | 2 |
| `ir_clinical_spuelung` | 2 | 2 |
| `scalp_comfort_serum` | 2 | 3 |
| `smoothing_deep_conditioner` | 2 | 2 |
| `smoothing_shampoo` | 2 | 2 |
| `bond_iq_leave_in` | 2 | 2 |
| `bond_iq_shampoo` | 2 | 2 |
| `bond_iq_spuelung` | 2 | 2 |
| `curl_auffrischer` | 2 | 3 |
| `curl_gelee` | 2 | 3 |
| `renew_shampoo` | 2 | 2 |
| `renew_spuelung` | 2 | 2 |
| `replenish_maske` | 2 | 2 |
| `restore_leave_in` | 2 | 2 |
| `smoothing_tiefenbehandlung` | 2 | 2 |
| `essig_shampoo` | 2 | 2 |
| `entwirrungsspray` | 1 | 2 |
| `fohncreme` | 1 | 2 |
| `hitzeschutzspray` | 1 | 2 |
| `kopfhaut_peeling` | 1 | 2 |
| `moxie_mousse` | 1 | 2 |
| `rejuvabeads` | 1 | 2 |
| `rejuveniqe_oel` | 1 | 2 |
| `revitalize_spuelung` | 1 | 2 |
| `revive_shampoo` | 1 | 2 |
| `scalp_comfort_behandlung` | 1 | 2 |
| `smoothing_fohn_spray` | 1 | 2 |
| `the_champ` | 1 | 2 |
| `volumen_spray` | 1 | 2 |
| `curl_creme` | 1 | 2 |
| `essig_spuelung` | 1 | 2 |
| `monat_black` | 0 | 1 |
| `super_feuchtigkeitsmaske` | 0 | 1 |
