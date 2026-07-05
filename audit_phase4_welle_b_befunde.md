# Phase-4-Welle-B Befunde — Pool-Scoring-Produkte (Stammdaten-Audit)

Stand 2026-06-29.
Audit-Methodik: 14 Produkte ohne direkte REQ/CON-Referenz kommen via Pool-Scoring (Node 12) in den Routine-Slot. Routing-Korrektheit hängt damit voll an den Stammdaten in produktdatenbank.

Verifikation pro Produkt:
1. Stammdaten-Filter (haarstruktur/haarstaerke/haarzustand/kopfhaut/ausschluss_bei) — PDF-belegbar (K-08 Header-Untertitel + K-03)?
2. hauptfunktion / nebenfunktionen — K-06 belegt (Produktversprechen, IDEAL, FAQ, Test-Bullet, Beschreibung)?

Statuslegende: 🟢 PDF-konform · 🟡 PDF-Detail abweichend, Edit empfohlen · 🔴 Routing-Bug

---

## erweiterte_feuchtigkeit_spuelung

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: glanz, kaemmbarkeit
- haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: trocken,glanzlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Trockenheit / Alle Haartypen / Feine bis mittlere Haartexturen / Vorbereitung"
- S.1 WARUM (Vorteils-Bullet): "Spendet Feuchtigkeit für glatteres, weicheres und glänzenderes Haar"
- S.1 WARUM: "omega-reiche Formel spendet Feuchtigkeit, macht das Haar weich und geschmeidig und verbessert seine Handhabung" (→ feuchtigkeit + kaemmbarkeit)
- S.1 IDEAL: "eine feine bis mittlere Haarstruktur haben und sich eine leichte Spülung wünschen, die hilft, die Feuchtigkeit zu speichern"
- S.1 ERGEBNISSE (Test-Bullet): "Verbesserung des Glanzes um 98 %", "Verbesserung der Kämmbarkeit um 91 %"
- S.1 WARUM DU ES LIEBEN WIRST: "weichere, glattere Strähnen mit strahlendem Glanz"

**Befund**: Stammdaten 1:1 vom PDF gedeckt. Header-Untertitel nennt "Feine bis mittlere Haartexturen" wörtlich → `haarstaerke=fein,mittel` korrekt. "Trockenheit" → `trocken`. Glanz als Test-Bullet UND Produktversprechen → `glanz` als Nebenfunktion sauber (K-07 erfüllt). Kämmbarkeit ebenso (Vorteils-Bullet + Test-Bullet). "Alle Haartypen" deckt `haarstruktur=alle` und `locken_geeignet=TRUE` ab. `haarzustand=glanzlos` ist plausibel (Glanz-Promise) — strikt genommen nennt PDF "Trockenheit" als Zielzustand, nicht "glanzlos"; aber Glanz-Verbesserung + "weicheres, glänzenderes Haar" gilt als implizite Adressierung von glanzlos.

**Empfehlung**: Keine Änderung.

---

## essig_shampoo

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: reinigung, entgiftung · neben: glanz, kopfhautpflege, frische
- kopfhaut: fettig · haarstruktur: alle · haarstaerke: alle · haarzustand: glanzlos
- locken_geeignet: TRUE
- ausschluss_bei: normal, trocken, juckend_empfindlich

**PDF-Belege**:
- S.1 Header-Untertitel: "Fettiges Haar und Kopfhaut / Alle Haartypen / Alle Haartexturen/Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "abgestorbene Hautzellen, hartnäckige Produktablagerungen und Umweltschadstoffe aufzulösen, die das Haar glanzlos erscheinen lassen" (→ reinigung + entgiftung + glanzlos-Adressierung)
- S.1 WARUM: "Reduziert überschüssiges Fett und stellt das Gleichgewicht der Kopfhaut wieder her" (→ kopfhautpflege)
- S.1 WARUM: "Entfernt Schmutz, Öl und Produktablagerungen" (→ entgiftung)
- S.1 WARUM: "Maximiert den Glanz und lässt das Haar geschmeidiger erscheinen" (→ glanz)
- S.1 IDEAL: "Frisches, sauberes und 24 Stunden lang wunderschön aussehendes Haar möchten" (→ frische)
- S.1 IDEAL: "Den Glanz maximieren ... möchten"

**Befund**: Header-Untertitel "Fettiges Haar und Kopfhaut" → `kopfhaut=fettig` belegt. "Alle Haartypen/Alle Haartexturen" → `haarstruktur=alle`, `haarstaerke=alle`, `locken_geeignet=TRUE` belegt. Hauptfunktionen reinigung+entgiftung via Produktversprechen (AHA-Wirkung auf Ablagerungen) + Vorteils-Bullets klar belegt. Glanz, Kopfhautpflege, Frische jeweils mit eigenem Vorteils-Bullet bzw. IDEAL. `ausschluss_bei: trocken, juckend_empfindlich` ist defensiv (AHA-haltiges Reinigungs-Shampoo) und PDF-konform — PDF positioniert Produkt explizit für fettiges/glanzloses Haar, nicht für trockenes/empfindliches.

**Empfehlung**: Keine Änderung.

---

## essig_spuelung

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: reinigung, wash_alternative · neben: glanz, feuchtigkeit, entgiftung, farbschutz, kopfhautpflege
- kopfhaut: - · haarstruktur: alle · haarstaerke: alle · haarzustand: glanzlos, trocken
- locken_geeignet: TRUE
- ausschluss_bei: normal, trocken, juckend_empfindlich

**PDF-Belege**:
- S.1 Header-Untertitel: "Kopfhautpflege / Alle Haartypen / Alle Haartexturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Der perfekte Shampoo-Ersatz für sauberes Haar an waschfreien Tagen" (→ wash_alternative)
- S.1 WARUM DU ES LIEBEN: "Natürliche Weichmacher bewahren die Feuchtigkeit ... Fruchtextrakte für mehr Glanz sorgen" (→ feuchtigkeit + glanz)
- S.1 WARUM: "Entfernt Produktrückstände, Schmutz und Öl" (→ reinigung + entgiftung)
- S.1 WARUM: "Die nicht abfärbende Formel bewahrt die Farbe für bis zu 20 Haarwäschen" (→ farbschutz)
- S.1 WARUM: "Nährt und hydratisiert Haar und Kopfhaut in einem Schritt" (→ kopfhautpflege + feuchtigkeit)
- S.1 IDEAL: "Sauberes und erfrischtes Haar sowie eine gereinigte Kopfhaut, an Shampoo-freien Tagen wünschen"
- S.1 IDEAL: "Produktablagerungen entfernen möchten, ohne ein herkömmliches Shampoo zu verwenden"
- S.1 ERGEBNISSE: "bis zu 12 % mehr Feuchtigkeit bei einmaliger Anwendung", "64 % mehr Glanz", "80 % erlebten eine Verbesserung des Feuchtigkeitsgehalts der Kopfhaut"

**Befund**:
- INKONSISTENZ Sheet-intern: `haarzustand=trocken` UND `ausschluss_bei=trocken` widersprechen sich logisch. PDF stützt klar `haarzustand=trocken` (mehrere Feuchtigkeits-Bullets/Test-Bullets) → der Ausschluss `trocken` ist PDF-widrig.
- `ausschluss_bei: normal`: PDF-widrig — Header sagt "Alle Haartypen". PDF positioniert Produkt als sanften Reinigungs-Ersatz, nicht als Spezialist nur für problematische Haut.
- `ausschluss_bei: juckend_empfindlich`: nicht direkt PDF-belegt, aber defensiv plausibel (Essig). PDF nennt beruhigende Inhaltsstoffe (Aloe Vera, Ingwerwurzel, Bisabolol) — mildert den Ausschluss, bleibt vertretbar als Sicherheitsnetz.
- `kopfhaut: -` (statt `fettig` wie beim essig_shampoo): Header sagt "Kopfhautpflege / Alle Haartypen" — keine fettige Kopfhaut genannt. Stammdaten PDF-konform.
- `haarstaerke: alle`, `haarstruktur: alle`: durch "Alle Haartypen / Alle Haartexturen" PDF-belegt, `locken_geeignet=TRUE` ebenso.
- `haarzustand: glanzlos, trocken`: PDF-konform.
- Hauptfunktionen + Nebenfunktionen: alle mit eigenem Vorteils-Bullet bzw. Test-Bullet belegt (K-06 erfüllt).

**Empfehlung**: `ausschluss_bei` korrigieren auf `juckend_empfindlich` (Entfernung von `normal, trocken`). Damit löst sich auch der interne Widerspruch zu `haarzustand=trocken` auf.

---

## feuchtigkeits_shampoo

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: glanz, kaemmbarkeit, reinigung
- kopfhaut: - · haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: trocken, glanzlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Trockenheit / Feines bis mittleres Haar / Alle Haartypen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Dieses Shampoo reinigt sanft, spendet Feuchtigkeit und verbessert die Kämmbarkeit für weicheres, geschmeidigeres Haar mit strahlendem Glanz"
- S.1 WARUM: "REJUVE-Quench™-Technologie ... liefert einen Feuchtigkeitsschub für sauberes, weicheres und glänzenderes Haar"
- S.1 WARUM: "Versiegelt die Schuppenschicht und schützt das Haar während der Reinigung vor Trockenheit"
- S.1 IDEAL: "Dem Haar schwerelose Feuchtigkeit verleihen möchten", "Das Haar reinigen und gleichzeitig die Feuchtigkeit wiederherstellen möchten", "Den Glanz erhöhen möchten"
- S.1 ERGEBNISSE: "Erhöht die Hydratation der Haare um 20 %", "Verbesserung des Glanzes um 82 %", "Verbesserung der Kämmbarkeit um 70 %"

**Befund**: Header-Untertitel deckt Stammdaten-Filter 1:1 ab: "Trockenheit"→trocken, "Feines bis mittleres Haar"→fein,mittel, "Alle Haartypen"→haarstruktur=alle/locken_geeignet=TRUE. `glanzlos` plausibel über Glanz-Promise (Vorteils-Bullet + Test-Bullet, K-07 erfüllt). Hauptfunktion feuchtigkeit dominiert das gesamte PDF. Alle Nebenfunktionen (glanz, kaemmbarkeit, reinigung) sind sowohl im Produktversprechen als auch in Test-Bullets verankert.

**Empfehlung**: Keine Änderung.

---

## ir_clinical_shampoo

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: verdichtend · neben: reinigung, farbschutz, haarwuchs, staerkend, frische
- kopfhaut: - · haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: duenn, kraftlos, haarbruch
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Verdichtend / Feines bis mittleres Haar / Alle Haartypen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Dieses Shampoo sorgt für ein erfrischendes Reinigungserlebnis und lässt das Haar dicker und voller aussehen" (→ frische + reinigung + verdichtend)
- S.1 WARUM: "Erhöht die Dicke der Haarfaser" (→ verdichtend)
- S.1 WARUM: "Reduziert Haarausfall um 84 %" — Reduktion von Haarausfall, NICHT aktives Wachstum
- S.1 WARUM: "Stärkt das Haar und verhindert Schäden durch Bürsten und Kämmen" (→ staerkend + haarbruch-Ziel)
- S.1 WARUM: "Bewahrt die Haarfarbe für bis zu 20 Haarwäschen" (→ farbschutz)
- S.1 IDEAL: "Weniger Haardichte haben", "Haarbruch durch Bürsten oder Kämmen erleben", "Kräftigeres, dichteres, volleres Haar wünschen", "Ein Shampoo mit einem belebenden, erfrischenden Gefühl möchten"
- S.1 SCHON GEWUSST: "bekämpft Haarausfall und verdichtet das Haar"
- S.2 ERGEBNISSE: "97 % ... sauberer", "86 % weniger Haare in der Bürste", "94 % ... leichter kämmen", "89 % Glanz"
- S.1 DUFT: Rosmarinöl + Minze (→ frische erfrischend-belebend gestützt)

**Befund**:
- Header-Untertitel + IDEAL stützen haarstaerke=fein,mittel und haarstruktur=alle.
- haarzustand=duenn,kraftlos,haarbruch — alle drei PDF-belegt: "weniger Haardichte"→duenn, "Haarausfall ... reduziert"→kraftlos/duenn, "Haarbruch durch Bürsten"→haarbruch.
- Hauptfunktion `verdichtend`: zentral im Header und allen WARUM-Bullets — sauber belegt.
- Nebenfunktion `haarwuchs`: K-06-problematisch. PDF spricht von "Haarausfall reduzieren" und "Haar dicker aussehen" — das ist Anti-Verlust/Verdickung, NICHT Wachstumsstimulation. Im strengen K-04-Sinn nicht belegt; das aktive Wachstums-Versprechen fehlt im PDF. ABER: der Effekt "weniger Haarverlust → mehr Haar bleibt" könnte als Routing-Pragmatismus durchgehen. Im strikten K-04-Sinn ist `haarwuchs` zu streichen.
- Nebenfunktion `reinigung`: trivial belegt (Shampoo + 100% sauberer Haar).
- `farbschutz`: PDF-belegt ("bis zu 20 Haarwäschen").
- `staerkend`: PDF-belegt ("Stärkt das Haar").
- `frische`: PDF-belegt ("erfrischendes Reinigungserlebnis", "belebend, erfrischend").

**Empfehlung**: Nebenfunktion `haarwuchs` aus Stammdaten entfernen — PDF beschreibt nur Anti-Haarausfall und Verdickung, kein aktives Wachstum (gleicher Konflikt wie ir_clinical_kopfhautserum, der in Phase 3 schon angesprochen werden sollte). Routing-Konsequenz: Wenn `haarwuchs` als Pool-Match-Funktion gilt, würde das Shampoo unverdient bei Wachstumswünschen punkten. Restliche Stammdaten korrekt.

---

## ir_clinical_spuelung

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: verdichtend · neben: feuchtigkeit, farbschutz, haarwuchs, staerkend, kaemmbarkeit, frische
- kopfhaut: - · haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: duenn, kraftlos, haarbruch
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Verdichtend / Feines bis mittleres Haar / Alle Haartexturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Diese reichhaltige Pflegespülung bietet ein belebendes, feuchtigkeitsspendendes Erlebnis und sorgt für dichteres, volleres Haar" (→ frische + feuchtigkeit + verdichtend)
- S.1 WARUM: "Erhöht die Dicke der Haarfaser" (→ verdichtend)
- S.1 WARUM: "Reduziert den Haarausfall um 91 %" — Anti-Verlust, nicht Wachstum
- S.1 WARUM: "Stärkt das Haar und verhindert Schäden durch Bürsten und Kämmen" (→ staerkend, haarbruch-Ziel)
- S.1 WARUM: "Pflegt und verbessert die Kämmbarkeit des Haares" (→ kaemmbarkeit)
- S.1 WARUM: "Bewahrt die Haarfarbe für bis zu 20 Haarwäschen" (→ farbschutz)
- S.1 IDEAL: "An geringer Haardichte leiden", "Haarbruch durch Bürsten oder Kämmen erleben", "Kräftigeres, dichteres, volleres Haar wünschen", "Eine Spülung mit belebendem, erfrischendem Gefühl suchen"
- S.2 ERGEBNISSE: "97 % Feuchtigkeit", "97 % Kämmbarkeit", "94 % stärkt", "94 % Glanz", "100 % weicher"
- S.1 DUFT: Rosmarinöl + Minze (→ frische belebend)

**Befund**:
- Header sagt "Alle Haartexturen" (das Shampoo: "Alle Haartypen"). Beides deckt haarstruktur=alle ab.
- haarstaerke=fein,mittel direkt im Header belegt.
- haarzustand=duenn,kraftlos,haarbruch — komplett via IDEAL belegt.
- Hauptfunktion `verdichtend`: sauber durch Header und mehrere WARUM-Bullets belegt.
- `feuchtigkeit`: zentral im Tagline + Test-Bullet (97 %).
- `kaemmbarkeit`: Vorteils-Bullet + Test-Bullet.
- `staerkend`: WARUM-Bullet + Test-Bullet.
- `farbschutz`: WARUM-Bullet.
- `frische`: "belebend, erfrischend" im Tagline + IDEAL.
- `haarwuchs`: gleiche K-04-Problematik wie Shampoo. PDF nennt nur Anti-Haarausfall/Verdickung, kein aktives Wachstum. Im strikten Sinn nicht belegt.

**Empfehlung**: Nebenfunktion `haarwuchs` aus Stammdaten entfernen (analog zum Shampoo). Restliche Stammdaten korrekt.

---

## rejuvabeads

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: reparatur, versiegelung · neben: glanz, kaemmbarkeit, staerkend, frizz_reduktion
- kopfhaut: - · haarstruktur: alle · haarstaerke: alle · haarzustand: spliss, haarbruch, frizz
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Haarschäden / Haarbruch & Spliss / Alle Haartypen / Alle Haarstrukturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Diese revolutionäre Leave-in-Behandlung hilft, Spliss zu versiegeln und hinterlässt das Haar glatt, glänzend und schützt vor weiteren Schäden"
- S.1 WARUM: "Versiegelt Spliss sofort für bis zu 24 Stunden nach der Anwendung" (→ versiegelung)
- S.1 WARUM: "Verleiht dem Haar bei jedem Kämmen Geschmeidigkeit" (→ kaemmbarkeit)
- S.1 WARUM: "Das Haar fühlt sich gesünder und stärker an" (→ staerkend abgeschwächt: "fühlt sich an" — kein objektiver Anspruch)
- S.1 IDEAL: "Spliss sofort versiegeln möchten", "Ihr Haar stärken und besser vor weiteren Schäden schützen wollen", "Verknotungen und Frizz, die mit Spliss und Mikroschäden einhergehen, reduzieren möchten" (→ frizz_reduktion, kaemmbarkeit, staerkend)

**Befund**:
- Header deckt haarstruktur=alle, haarstaerke=alle und haarzustand=spliss,haarbruch direkt ab; `locken_geeignet=TRUE` durch "Alle Haarstrukturen" gedeckt.
- haarzustand=frizz: nur über IDEAL ("Verknotungen und Frizz ... reduzieren möchten") belegt — gilt aber als spliss-/mikroschadens-assoziierter Frizz, nicht als primäres Frizz-Produkt. Im Routing legitim, da im IDEAL genannt.
- `versiegelung`: zentral und mehrfach belegt — sauber als Hauptfunktion.
- `reparatur`: K-04-Grenzfall. PDF nennt nirgends "repariert" oder "stellt wieder her". Es heißt explizit "versiegeln" + "vor weiteren Schäden schützen" — also Schutz-/Symptom-Behandlung, nicht Reparatur. Strikt PDF-konform müsste die Hauptfunktion `reparatur` durch `versiegelung` allein oder durch `staerkend` (für "fühlt sich stärker an") ersetzt werden.
- `glanz`: "hinterlässt das Haar glatt, glänzend" → Produktversprechen-Bullet, K-06 erfüllt.
- `kaemmbarkeit`: zwei Bullets → erfüllt.
- `staerkend`: durch IDEAL-Bullet "Ihr Haar stärken" belegt.
- `frizz_reduktion`: durch IDEAL-Bullet belegt.

**Empfehlung**: Hauptfunktion `reparatur` streichen (PDF widerspricht: "versiegeln" + "schützt vor weiteren Schäden" ≠ Reparatur bestehender Schäden). `versiegelung` als alleinige Hauptfunktion belassen, ggf. `staerkend` von Neben- zu Hauptfunktion hochziehen, da das IDEAL den Stärkungs-Aspekt prominent nennt. Routing-Konsequenz: Bei User-Wünschen "Haar reparieren" sollte rejuvabeads nicht primär gewinnen — die Reparatur-Funktion gehört zu replenish_maske/restore_leave_in/bond_iq.

---

## renew_shampoo

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: glanz, reinigung, kaemmbarkeit
- kopfhaut: - · haarstruktur: alle · haarstaerke: mittel,dick · haarzustand: trocken, glanzlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Trockenes Haar / Alle Haartypen / Mittlere bis dicke Haarstruktur / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Dieses sanfte Reinigungsmittel spendet trockenem Haar tiefenwirksam Feuchtigkeit und macht es weich, leichter kämmbar und lässt es wieder gesünder aussehen"
- S.1 WARUM: "Spendet Ultra-Hydratisierung für trockenes Haar" (→ feuchtigkeit)
- S.1 WARUM: "Reinigt, ohne wichtige Feuchtigkeit zu entziehen" (→ reinigung)
- S.1 WARUM: "Fördert Geschmeidigkeit und Glanz" (→ glanz)
- S.1 IDEAL: "Ihrem Haar ein sofortiges, gesundes Aussehen verleihen möchten", "Ein Reinigungsmittel suchen, das selbst für die schwächsten Haare sanft genug ist", "Die widerspenstiges Haar verhindern möchten" (→ kaemmbarkeit)

**Befund**:
- Header-Untertitel deckt haarstaerke=mittel,dick und haarstruktur=alle/locken_geeignet=TRUE und haarzustand=trocken direkt 1:1 ab.
- haarzustand=glanzlos durch Glanz-Promise als Vorteils-Bullet belegt (K-06+K-07 erfüllt: Vorteils-Bullet "Fördert Geschmeidigkeit und Glanz").
- Hauptfunktion `feuchtigkeit`: zentral und mehrfach belegt.
- `reinigung`: trivial belegt (Shampoo, "sanftes Reinigungsmittel").
- `glanz`: Vorteils-Bullet.
- `kaemmbarkeit`: "leichter kämmbar" im Tagline + "widerspenstiges Haar verhindern" im IDEAL.

**Empfehlung**: Keine Änderung.

---

## renew_spuelung

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: kaemmbarkeit
- kopfhaut: - · haarstruktur: alle · haarstaerke: mittel,dick · haarzustand: trocken
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Trockenes Haar / Alle Haartypen / Mittlere bis dicke Haartexturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "hilft dieser Conditioner, essentielle Feuchtigkeit wiederherzustellen, um die Hydratation auf mittlerem bis dickem, trockenem Haar zu erneuern"
- S.1 WARUM: "Mit Hyaluronsäure formuliert, um Feuchtigkeit zu spenden" (→ feuchtigkeit)
- S.1 WARUM: "Verbessert Kämmbarkeit und Handhabung" (→ kaemmbarkeit)
- S.1 VORTEILE: "Spendet dem Haar Feuchtigkeit", "Liefert intensive Hydration", "Ideal für mittlere bis dicke Haartypen"
- S.1 IDEAL: "Die Handhabbarkeit ihrer Haare verbessern möchten"

**Befund**:
- Header-Untertitel deckt Stammdaten 1:1 ab: haarstaerke=mittel,dick, haarstruktur=alle, locken_geeignet=TRUE, haarzustand=trocken.
- Hauptfunktion `feuchtigkeit`: zentral und mehrfach belegt.
- `kaemmbarkeit`: eigener Vorteils-Bullet + IDEAL.
- KEIN `glanz` im Sheet — und das ist korrekt: PDF nennt nirgends Glanz als Vorteil oder Test-Bullet. Bewusste Engführung gegenüber renew_shampoo und replenish_maske, die Glanz aktiv versprechen. Strikt PDF-konform.
- KEIN `glanzlos` im haarzustand — konsequent zur fehlenden Glanz-Funktion.

**Empfehlung**: Keine Änderung. Stammdaten zeigen exemplarisch saubere PDF-Treue (kein Glanz-Bullet → keine glanz-Funktion).

---

## replenish_maske

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: glanz, kraeftigend, kaemmbarkeit
- kopfhaut: - · haarstruktur: alle · haarstaerke: mittel,dick · haarzustand: trocken, glanzlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Trockenes Haar / Alle Haartypen / Mittlere bis dicke Haartexturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Diese reichhaltige Pflegemaske pflegt und hydratisiert jede einzelne Haarsträhne und stellt Glanz, Kraft und Vitalität des Haares wieder her"
- S.1 WARUM: "Versorgt das Haar intensiv mit Feuchtigkeit" (→ feuchtigkeit)
- S.1 WARUM: "Fördert Geschmeidigkeit und Glanz" (→ glanz)
- S.1 IDEAL: "Verlorene Feuchtigkeit wiedergewinnen möchten", "Verbesserte Haarstruktur und Kämmbarkeit wünschen" (→ kaemmbarkeit), "Weiches und glänzendes Haar wünschen"

**Befund**:
- Header-Untertitel deckt haarstaerke=mittel,dick + haarstruktur=alle/locken_geeignet=TRUE + haarzustand=trocken direkt ab.
- haarzustand=glanzlos durch wiederholtes Glanz-Versprechen (Tagline "stellt Glanz wieder her" + Vorteils-Bullet "Fördert ... Glanz" + IDEAL "Weiches und glänzendes Haar wünschen") sauber abgeleitet.
- Hauptfunktion `feuchtigkeit`: zentral und mehrfach belegt.
- `glanz`: zentral, mehrfach belegt.
- `kraeftigend`: durch Tagline "stellt ... Kraft und Vitalität ... wieder her" belegt (K-06 erfüllt, ist Produktversprechen-Satz, kein bloßes Inhaltsstoff-Bullet).
- `kaemmbarkeit`: durch IDEAL "Verbesserte ... Kämmbarkeit wünschen" belegt.

**Empfehlung**: Keine Änderung.

---

## revitalize_spuelung

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: volumen · neben: feuchtigkeit, staerkend, kaemmbarkeit, reparatur
- kopfhaut: - · haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: kraftlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Volumen / Alle Haartypen / Feine bis mittleres Haar / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Diese leichte, volumengebende Pflegespülung versorgt dünnes, plattes Haar mit wichtigen Nährstoffen, die für mehr Volumen sorgen"
- S.1 WARUM: "Stärkt und schützt das Haar" (→ staerkend)
- S.1 WARUM: "Spendet Feuchtigkeit, ohne das Haar zu beschweren" (→ feuchtigkeit)
- S.1 WARUM: "Lässt Haar mühelos entwirren, um Haarbruch zu verhindern" (→ kaemmbarkeit + haarbruch-Prävention)
- S.1 IDEAL: "Ihr Haar gesund halten und gleichzeitig Fülle bewahren möchten", "Weiches, hydratisiertes Haar ohne Beschwerung möchten", "Starkes und gesundes Haar wünschen"

**Befund**:
- Header-Untertitel deckt haarstaerke=fein,mittel + haarstruktur=alle/locken_geeignet=TRUE direkt ab.
- haarzustand=kraftlos durch Tagline "dünnes, plattes Haar" + IDEAL "Starkes und gesundes Haar wünschen" belegt.
- Hauptfunktion `volumen`: zentral und mehrfach belegt.
- `feuchtigkeit`, `staerkend`, `kaemmbarkeit`: alle drei mit eigenem Vorteils-Bullet.
- `reparatur`: K-04-Verstoß. PDF nennt nur "schützt" und "Haarbruch verhindern" (Prävention), nirgends "repariert" oder Wiederherstellung beschädigter Strukturen. Im strikten Sinn nicht belegt.

**Empfehlung**: Nebenfunktion `reparatur` aus Stammdaten entfernen. PDF positioniert das Produkt rein präventiv/volumengebend, nicht reparierend. Routing-Konsequenz: Sollte bei User-Wunsch "reparieren" nicht gewinnen.

---

## revive_shampoo

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: volumen · neben: reinigung, staerkend, feuchtigkeit, kaemmbarkeit, reparatur
- kopfhaut: - · haarstruktur: alle · haarstaerke: fein,mittel · haarzustand: kraftlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Volumen / Alle Haartypen / Feine bis mittlere Haarstrukturen / Pflege-Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Dieses sanfte Reinigungsshampoo verleiht feinem, platt wirkendem Haar neues Leben. Dank einzigartiger Inhaltsstoffe fördert es gesundaussehendes Haar von den Wurzeln bis in die Spitzen – ohne zu beschweren"
- S.1 WARUM: "Stärkt und schützt das Haar" (→ staerkend)
- S.1 WARUM: "Spendet Feuchtigkeit, ohne das Haar zu beschweren" (→ feuchtigkeit)
- S.1 WARUM: "Erleichtert das Entwirren und hilft, Haarbruch vorzubeugen" (→ kaemmbarkeit + Prävention)
- S.1 IDEAL: "Gesund aussehendes Haar und mehr Fülle erhalten möchten", "Weiches, mit Feuchtigkeit versorgtes Haar wollen", "Stärkeres, gesundes Haar anstreben"

**Befund**:
- Header-Untertitel deckt haarstaerke=fein,mittel + haarstruktur=alle/locken_geeignet=TRUE direkt ab.
- haarzustand=kraftlos durch Tagline "feinem, platt wirkendem Haar" + "Fülle erhalten" belegt.
- Hauptfunktion `volumen`: zentral, mehrfach belegt.
- `reinigung`: trivial belegt ("Reinigungsshampoo").
- `staerkend`, `feuchtigkeit`, `kaemmbarkeit`: alle drei mit eigenem Vorteils-Bullet.
- `reparatur`: K-04-Verstoß (gleicher Befund wie revitalize_spuelung). PDF nennt nur "schützt" und "Haarbruch vorbeugen" — Prävention, nicht Reparatur.

**Empfehlung**: Nebenfunktion `reparatur` aus Stammdaten entfernen (konsistent mit revitalize_spuelung).

---

## smoothing_tiefenbehandlung

**Status**: 🟡

**Stammdaten-Aussage** (kurz):
- haupt: frizz_reduktion · neben: kaemmbarkeit, reparatur
- kopfhaut: - · haarstruktur: alle · haarstaerke: mittel,dick · haarzustand: frizz, haarbruch
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Frizz / Alle Haartypen und -strukturen / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Dieser reichhaltige Conditioner ist ideal für die tägliche Pflege ... auch bei Locken und krausem Haar. Frizz, fliegende Härchen und statische Aufladung werden spürbar reduziert"
- S.1 WIE ES FUNKTIONIERT: "Bekämpft Frizz und fliegende Härchen bis zu 72 Stunden", "Reduziert Haarbruch um bis zu 91 % für leichteres Styling", "Bis zu 6x geschmeidigeres, glatteres Haar mit weniger Frizz"
- S.1 IDEAL: "Eine intensiv frizzreduzierende Pflege für mittleres bis dickes Haar suchen", "Die Kämmbarkeit ihres Haars verbessern möchten", "Sich geschmeidiges, frizzfreies Haar mit weniger Haarbruch wünschen"
- S.1 ERGEBNISSE: "6x bessere Kämmbarkeit im nassen Haar", "5x bessere Kämmbarkeit im trockenen Haar", "Reduziert Haarbruch um 91 %", "80 % mehr Glanz"

**Befund**:
- Header sagt "Alle Haartypen und -strukturen" — deckt haarstruktur=alle und locken_geeignet=TRUE direkt ab. Außerdem Tagline "auch bei Locken und krausem Haar" → besonders gute Lockenabdeckung.
- haarstaerke=mittel,dick wird vom IDEAL direkt PDF-belegt ("für mittleres bis dickes Haar suchen") — ZIELGENAUE Setzung, nicht zu eng nicht zu weit.
- haarzustand=frizz: zentral, mehrfach belegt.
- haarzustand=haarbruch: durch "Reduziert Haarbruch um 91 %" + IDEAL "weniger Haarbruch" — belegt.
- Hauptfunktion `frizz_reduktion`: dominiert das gesamte PDF.
- `kaemmbarkeit`: zwei Test-Bullets (6x/5x) + IDEAL + Vorteils-Bullet — stark belegt.
- `reparatur`: K-04-Verstoß. PDF nennt nur "Reduziert Haarbruch" (Prävention) und Pflege/Konditionierung. Nirgends "repariert" oder Wiederherstellung von Schäden. Strikt nicht belegt.
- Zusätzlich: PDF erwähnt explizit "80 % mehr Glanz" als Test-Bullet — aber `glanz` ist NICHT in Stammdaten-Nebenfunktionen. K-07-Check: Glanz ist Test-Bullet ohne im Produktversprechen verankert zu sein (Tagline + WARUM-Bullets nennen Glanz nicht aktiv). Bleibt zu schwach für K-06; korrekte Nicht-Setzung in Sheet.

**Empfehlung**: Nebenfunktion `reparatur` aus Stammdaten entfernen. PDF stützt nur Prävention und Pflege, keine Reparatur. Glanz bewusst nicht ergänzen (K-07-Schwelle nicht erreicht).

---

## super_feuchtigkeitsmaske

**Status**: 🟢

**Stammdaten-Aussage** (kurz):
- haupt: feuchtigkeit · neben: glanz, elastizitaet, kaemmbarkeit
- kopfhaut: - · haarstruktur: wellig, lockig, kraus · haarstaerke: mittel,dick · haarzustand: trocken, glanzlos
- locken_geeignet: TRUE

**PDF-Belege**:
- S.1 Header-Untertitel: "Locken, Wellen & Coils / Alle Haartypen / Mittlere bis dicke Haarstruktur / Vorbereitung"
- S.1 WARUM DU ES LIEBEN: "Diese ultra-pflegende Maske verleiht dem Haar Geschmeidigkeit, Weichheit und Glanz, bekämpft Brüchigkeit und verbessert Feuchtigkeit und Handhabbarkeit des Haares"
- S.1 WARUM: "Versorgt das Haar mit wichtigen Nährstoffen und tiefgehender Feuchtigkeit" (→ feuchtigkeit)
- S.1 WARUM: "Verwandelt trockene Strähnen in weiches, seidiges Haar" (→ haarzustand=trocken)
- S.1 WARUM: "Fördert die Elastizität und verbessert die Kämmbarkeit" (→ elastizitaet + kaemmbarkeit)
- S.1 IDEAL: "Trockenes Haar regenerieren möchten", "Eine intensive Pflege und luxuriösen Glanz wünschen", "Weiches und besser kämmbares Haar möchten"

**Befund**:
- Header-Untertitel ist exemplarisch deckungsgleich mit Stammdaten:
  - "Locken, Wellen & Coils" → haarstruktur=wellig,lockig,kraus direkt benannt (KEIN "Alle Haartypen" wie bei anderen Renew-Produkten — bewusste Engführung)
  - "Mittlere bis dicke Haarstruktur" → haarstaerke=mittel,dick belegt
  - locken_geeignet=TRUE selbsterklärend
- haarzustand=trocken,glanzlos: beide via Tagline ("Glanz") + Vorteils-Bullets + IDEAL belegt.
- Hauptfunktion `feuchtigkeit`: zentral und mehrfach belegt, Produktname trägt sie.
- `glanz`: in Tagline UND IDEAL UND als zentrale Produkteigenschaft genannt — Vorteil ist Glanz-versprechen.
- `elastizitaet`: explizit als eigener Vorteils-Bullet "Fördert die Elastizität" — sauber K-06.
- `kaemmbarkeit`: Vorteils-Bullet "verbessert die Kämmbarkeit" + IDEAL.

**Empfehlung**: Keine Änderung. Beispielhaft sauberer Stammdaten-Eintrag mit bewusster struktur-Engführung auf Locken/Wellen — entspricht der PDF-Positionierung. Anti-Pattern wäre `haarstruktur=alle` gewesen.

---

## Zusammenfassung — Welle B (14 Produkte)

**Status-Verteilung**:
- 🟢 PDF-konform (keine Änderung): 7 Produkte
  - erweiterte_feuchtigkeit_spuelung, essig_shampoo, feuchtigkeits_shampoo, renew_shampoo, renew_spuelung, replenish_maske, super_feuchtigkeitsmaske
- 🟡 PDF-Detail abweichend (Edit empfohlen): 7 Produkte
  - essig_spuelung, ir_clinical_shampoo, ir_clinical_spuelung, rejuvabeads, revitalize_spuelung, revive_shampoo, smoothing_tiefenbehandlung
- 🔴 Routing-Bug: 0 Produkte

**Wiederkehrende Bug-Muster**:

1. **`haarwuchs`-Inflation** (ir_clinical_shampoo, ir_clinical_spuelung): PDFs nennen "Haarausfall reduzieren" + "Verdichtung", aber kein aktives Wachstumsversprechen. Strikt K-04 ist `haarwuchs` als Nebenfunktion nicht belegt. Routing-Konsequenz: bei haarwuchs-Match würden Shampoo/Spülung unverdient punkten — die Wachstums-Funktion gehört nur an ir_clinical_kopfhautserum, das explizit "Haarausfall bekämpfen" + Test-Bullet bietet (Phase 3 ohnehin schon kritisch).

2. **`reparatur`-Inflation** (rejuvabeads, revitalize_spuelung, revive_shampoo, smoothing_tiefenbehandlung): PDFs sprechen von "schützen", "Haarbruch vorbeugen", "versiegeln" — Prävention oder Symptom-Kontrolle, NICHT Reparatur. Bei rejuvabeads sogar als HAUPTFUNKTION fehlerhaft. Reparatur-Funktion gehört systematisch zu replenish_maske (siehe Wortlaut "stellt ... wieder her") und an bond_iq/restore_leave_in.

3. **`ausschluss_bei` zu defensiv und intern widersprüchlich** (essig_spuelung): `ausschluss_bei=normal,trocken` widerspricht direkt PDF "Alle Haartypen" + zentraler Feuchtigkeits-Aussage. Zusätzlich Sheet-interner Widerspruch (`trocken` in haarzustand UND ausschluss_bei).

**Konkrete Stammdaten-Edits (empfohlen)**:

| produkt_key | Spalte | Ist | Soll |
|---|---|---|---|
| essig_spuelung | ausschluss_bei | normal,trocken,juckend_empfindlich | juckend_empfindlich |
| ir_clinical_shampoo | nebenfunktionen | reinigung,farbschutz,haarwuchs,staerkend,frische | reinigung,farbschutz,staerkend,frische |
| ir_clinical_spuelung | nebenfunktionen | feuchtigkeit,farbschutz,haarwuchs,staerkend,kaemmbarkeit,frische | feuchtigkeit,farbschutz,staerkend,kaemmbarkeit,frische |
| rejuvabeads | hauptfunktion | reparatur,versiegelung | versiegelung,staerkend |
| rejuvabeads | nebenfunktionen | glanz,kaemmbarkeit,staerkend,frizz_reduktion | glanz,kaemmbarkeit,frizz_reduktion |
| revitalize_spuelung | nebenfunktionen | feuchtigkeit,staerkend,kaemmbarkeit,reparatur | feuchtigkeit,staerkend,kaemmbarkeit |
| revive_shampoo | nebenfunktionen | reinigung,staerkend,feuchtigkeit,kaemmbarkeit,reparatur | reinigung,staerkend,feuchtigkeit,kaemmbarkeit |
| smoothing_tiefenbehandlung | nebenfunktionen | kaemmbarkeit,reparatur | kaemmbarkeit |

