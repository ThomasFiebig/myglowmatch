# Phase-4 Welle A — Routing-vs-PDF-Befunde

Stand 2026-06-29. Quelle: `audit_phase4_inventar.md` + PDFs in `produktdatenblaetter/`.
Methodik strikt nach K-04 / K-06 / K-08 (Header-Untertitel als Filter-Beleg, NICHT als Funktions-Beleg).

Klassifikation: 🟢 Routing PDF-konform · 🟡 PDF-Detail-Abweichung (kein Routing-Bug) · 🔴 Routing-Bug.

---

## curl_auffrischer

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-13 triggert auf `curl_refresh_needed=TRUE AND wants_full_curl_line=TRUE` → slot styling_3. Stammdaten: haarstruktur=wellig,lockig,kraus; haarzustand=trocken,frizz; ausschluss_bei=glatt.

**PDF-Belege** (Curl Perfection Anleitung S.3 + S.8 + S.14):
- S.3 (Kollektions-Header): "Die Produkte wurden entwickelt, um natürliche Haarstrukturen zu unterstützen und gleichzeitig die Gesundheit und Schönheit von welligem, lockigem und krausem Haar zu verbessern."
- S.8 (Produkt-Untertitel): "Curl-Reaktivator für den zweiten Tag"
- S.8 ("WIE MAN ES BENUTZT"): "Gleichmäßig auf feuchtem oder trockenem Haar aufsprühen … Locken sanft mit den Händen kneten, um sie zu reaktivieren."
- S.8 (Vorteile): "Erfrischt, reaktiviert und definiert Locken", "Spendet 24 Stunden lang Feuchtigkeit", "Verstärkt die natürliche Lockenform"
- S.14 (Tipps am zweiten Tag): "Erfrische und belebe mit dem MONAT Curl Perfection™ Auffrischungsspray."

**Befund**: PDF spricht klar wellig/lockig/kraus an (K-08-Header für Linie) und beschreibt den Auffrischungs-Use-Case Tag 2 — exakt das, was REQ-13 (`curl_refresh_needed`) abbildet. Stammdaten-Filter konsistent.

**Empfehlung**: Routing korrekt, kein Edit.

---

## curl_gelee

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-12 triggert auf `needs_curl_care=TRUE AND needs_curl_gelee_styling=TRUE` → slot styling_2. Stammdaten: haarstruktur=wellig,lockig,kraus; haarzustand=frizz,trocken; ausschluss_bei=glatt.

**PDF-Belege** (Curl Perfection Anleitung S.3 + S.7):
- S.3 (Kollektions-Header): siehe curl_auffrischer (welliges, lockiges, krauses Haar).
- S.7 (Produkt-Untertitel): "Lockendefinierendes Gel"
- S.7 (Vorteile): "Bietet fühlbar weiche, federnde, definierte Locken für bis zu 8 Stunden", "Pflegt, stärkt und repariert welliges, lockiges und krauses Haar", "Hält die gewünschte Lockenform den ganzen Tag über"
- S.7 (Anwendung): "Auf nasses, handtuchtrockenes oder feuchtes Haar auftragen. … Kann auf trockenes Haar aufgetragen werden, um Locken aufzufrischen."

**Befund**: PDF nennt explizit welliges, lockiges, krauses Haar (K-08 + zusätzlich K-06-Funktionsbeleg). Definition/Halt/Locken/Feuchtigkeit/Frizz-Reduktion belegt. Routing PDF-konform.

**Empfehlung**: Routing korrekt, kein Edit.

---

## fohncreme

**Status**: 🟡

**Routing-Aussage** (kurz): REQ-04 (Bool) — `heat_use=yes|maybe` → ist_hitzeschutz=TRUE. Stammdaten: haarzustand=frizz; ausschluss_bei=wellig,lockig,kraus; bool ist_hitzeschutz+locken_geeignet (Widerspruch in den Stammdaten selbst).

**PDF-Belege** (S.1):
- Header: "Frizz / Hitzeschutz / Alle Haartypen und-texturen / Styling"
- WARUM ES FUNKTIONIERT: "Bietet Hitzeschutz bis zu 232° C, um Schäden zu verhindern", "Schützt bis zu 8 Stunden vor Frizz", "Sicher für coloriertes Haar"
- IDEAL: "Ein seidiges, samtig-glattes Gefühl beim Stylen wünschen", "Ein Produkt möchten, das Frizz bei hoher Luftfeuchtigkeit kontrolliert", "Die Dauer ihres Stylings verlängern möchten"

**Befund**: Header sagt EXPLIZIT "Alle Haartypen und-texturen". Sheet hat `ausschluss_bei=wellig,lockig,kraus` — direkter Widerspruch zum PDF-Header (K-08). Gleichzeitig steht `locken_geeignet=TRUE` im Bool-Block. Inkonsistente Stammdaten. Funktionen hitzeschutz + frizz_reduktion (Hauptfunktion) sauber belegt. REQ-04-Trigger selbst (heat_use) ist PDF-konform.

**Empfehlung**: Stammdaten-Edit prüfen: `ausschluss_bei=wellig,lockig,kraus` widerspricht dem PDF-Header "Alle Haartypen und-texturen" und dem eigenen `locken_geeignet=TRUE`. Entweder ausschluss_bei leeren oder locken_geeignet=FALSE setzen — eine der beiden Angaben ist falsch. Routing (REQ-04) selbst korrekt.

---

## hitzeschutzspray

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-04 (`heat_use=yes|maybe` → ist_hitzeschutz=TRUE), CON-07 schließt aus bei `heat_use=no`. Stammdaten: haarzustand=haarbruch; bool ist_hitzeschutz+locken_geeignet.

**PDF-Belege** (S.1):
- Header: "Hitzeschutz / Alle Haartypen / Alle Haartexturen / Styling"
- WARUM: "Bietet Schutz vor hohen Temperaturen (232°C) und UV-Strahlen, um Schäden und Haarbruch zu vermeiden", "verbessert die Gleitfähigkeit und reduziert Reibung beim Styling"
- IDEAL: "Ihr Haar vor irreparablen Hitzeschäden durch Stylinggeräte schützen möchten", "Die Stärke und Elastizität des Haares verbessern möchten"
- ERGEBNISSE: "Haare … zeigten mehr Stärke und Elastizität"

**Befund**: PDF spricht ausdrücklich Hitzeschutz für alle Haartypen/-texturen an. Haarbruch-Schutz im WARUM belegt → Stammdaten-haarzustand=haarbruch passt. REQ-04 + CON-07 sauber PDF-gestützt.

**Empfehlung**: Routing korrekt, kein Edit.

---

## ir_clinical_kopfhautserum

**Status**: 🟡

**Routing-Aussage** (kurz): REQ-06 triggert auf `hair_condition_contains=duenn` → slot kopfhaut (filter: ir_clinical_kopfhautserum). Stammdaten: kopfhaut=trocken; haarstaerke=fein,mittel; haarzustand=duenn,kraftlos,haarbruch.

**PDF-Belege** (S.1):
- Header: "Verdichtend / Feines bis mittleres Haar / Alle Haartypen / Behandlung"
- WARUM-Box: "Klinische Studien belegen, dass es das Haarwachstum fördert, Haarbruch sofort reduziert und innerhalb von 60 Tagen sichtbar dichteres und volleres Haar verleiht."
- WARUM ES FUNKTIONIERT: "Reduktion der DHT-Produktion, das das Haar verdünnt", "stärken, verdicken"
- IDEAL: "An dünner werdendem Haar leiden", "Trockene Kopfhaut haben", "Mehr Haardichte wünschen", "Dickeres, gesünderes Haar und eine gesündere Kopfhaut anstreben"

**Befund**: REQ-06-Trigger (`duenn`) sauber PDF-belegt. Stammdaten haarstaerke=fein,mittel deckt sich exakt mit Header (K-08). ABER: kopfhaut=trocken kommt im PDF-Header NICHT vor (Header listet nur Haar-Eigenschaften, keinen Kopfhautzustand). Die Aussage "Trockene Kopfhaut haben" steht nur unter "IDEAL FÜR DIEJENIGEN, DIE" — was nach K-08 für FILTER-Spalten kein legitimer Beleg ist (nur Header-Untertitel zählt). Strenge K-08-Lesung: Stammdaten-`kopfhaut=trocken` ist PDF-overrechted.

**Empfehlung**: Schwacher Fall — die "Trockene Kopfhaut"-Nennung in IDEAL ist im PDF konkret. Wenn IDEAL-Block für FILTER-Spalten erlaubt sein soll, kein Edit. Wenn strikt nur Header-Untertitel zählt, `kopfhaut=trocken` aus Stammdaten entfernen. Routing selbst (REQ-06) PDF-konform.

---

## kopfhaut_peeling

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-24 (optional) triggert auf `primary_scalp_state=fettig` → slot kopfhaut. Stammdaten: kopfhaut=fettig; haarzustand=glanzlos; ausschluss_bei=juckend_empfindlich; bool ist_scalp_focus.

**PDF-Belege** (S.1):
- Header: "Fettiges Haar und Kopfhaut / Alle Haartypen / Alle Haarstrukturen / Vorbereitung"
- WARUM: "hilft, abgestorbene Hautzellen, hartnäckige Produktablagerungen und Umweltschadstoffe aufzulösen, die das Haar glanzlos erscheinen lassen"
- WARUM ES FUNKTIONIERT: "Peelt die Oberfläche der Kopfhaut und Haare", "Löst Talg und hartnäckige Produktrückstände auf", "Reduziert überschüssiges Öl"
- IDEAL: "Fettige Ansätze sofort reinigen und das Haar gereinigt und erfrischt hinterlassen möchten", "Überschüssiges Öl reduzieren"

**Befund**: REQ-24-Trigger (`fettig`) exakt belegt (Header + Funktions-Beleg im WARUM). Glanzlos-Zustand im WARUM-Text belegt. Peeling-Charakter rechtfertigt `ausschluss_bei=juckend_empfindlich` (keine PDF-Aussage explizit, aber konsistente Beratungspraxis und keine Aussage im PDF, die das Peeling für gereizte Kopfhaut empfiehlt).

**Empfehlung**: Routing korrekt, kein Edit.

---

## monat_black

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-30 triggert auf `primary_scalp_state=fettig AND routine_preference=minimal` → slot shampoo (filter: monat_black, 2-in-1 ersetzt shampoo+spuelung). Stammdaten: kopfhaut=fettig; haarstaerke=fein,mittel; haarzustand=kraftlos,duenn.

**PDF-Belege** (S.1):
- Header: "Fettiges Haar und Kopfhaut / Verdichtend / Feine bis mittlere Haartypen / Alle Haartrukturen / Vorbereitung"
- Produktname: "MONAT BLACK™. SHAMPOO + SPÜLUNG" (2-in-1 explizit)
- WARUM-Box: "Dieses 2-in-1-Shampoo und Pflegespülung sind so formuliert, dass sie nähren, ausgleichen und stärken – in einem einfachen Schritt."
- WARUM ES FUNKTIONIERT: "Reinigt und pflegt in einem einfachen Schritt", "Fördert gesünder aussehendes Haar"
- IDEAL: "Ihr Haar in einem einfachen Schritt reinigen und pflegen möchten", "Die Dichte verbessern und das Haar voller erscheinen lassen möchten", "Stärkeres, gesünderes Haar wünschen"

**Befund**: REQ-30-Trigger perfekt PDF-belegt — Header sagt "Fettiges Haar und Kopfhaut" + "Feine bis mittlere Haartypen", und IDEAL-Block adressiert ausdrücklich Routine-Minimierung ("in einem einfachen Schritt") + Dichte/Volumen-Ziel. 2-in-1-Ersatz-Logik (replaces shampoo+spuelung) durch Produktname und WARUM voll gestützt. Stammdaten-Filter (kopfhaut=fettig, haarstaerke=fein,mittel, haarzustand=kraftlos,duenn) deckungsgleich mit K-08-Header.

**Empfehlung**: Routing korrekt, kein Edit.

---

## rejuveniqe_oel

**Status**: 🟡

**Routing-Aussage** (kurz): REQ-17 triggert auf `styling_goal_glanz=TRUE` und REQ-17b auf `oil_need=maybe AND pflegelevel_numeric>=3` → slot finish. Stammdaten: haarzustand=trocken,glanzlos,frizz; haupt=glanz,feuchtigkeit; neben=frizz_reduktion,kraeftigend,kaemmbarkeit.

**PDF-Belege** (S.1):
- Header: "Alle Haartypen / Alle Haarstrukturen / Vorbereitung, Styling & Finish"
- WARUM-Box: "Dieses vielseitige Öl kombiniert eine geschützte Mischung aus 13+ natürlichen pflanzlichen und ätherischen Ölen, die das gesunde Aussehen von Haar und Haut verbessern und Antioxidantien liefern."
- WARUM ES FUNKTIONIERT: "Hilft, Feuchtigkeit, Geschmeidigkeit und Glanz zu erhalten", "Kräftigt die Haarfasern", "Glättet die Schuppenschicht, um Frizz zu reduzieren"
- IDEAL: "Ein Mehrzweck-Öl suchen, das für Haare und Haut verwendet werden kann", "Frizz kontrollieren und die allgemeine Handhabbarkeit verbessern möchten", "Seidig glattes und glänzendes Haar wünschen"

**Befund**: Funktionen (Glanz, Feuchtigkeit, Frizz-Reduktion, Kämmbarkeit, kräftigend) alle in WARUM/IDEAL klar belegt (K-06). REQ-17 (`styling_goal_glanz`) PDF-konform. REQ-17b (oil_need=maybe + pflegelevel>=3) ist softer Fallback und PDF-mäßig durch "Mehrzweck-Öl" gestützt. Stammdaten-haarzustand=trocken,glanzlos,frizz alle belegt durch WARUM/IDEAL — aber Header sagt explizit "Alle Haartypen / Alle Haarstrukturen", was bedeutet das Öl ist universell und sollte nicht zu eng auf trocken/glanzlos/frizz gefiltert werden (auch normale Haare profitieren laut PDF).

**Empfehlung**: Stammdaten-Filter sind enger als das PDF — das ist kein Routing-Bug (Pool-Filter schmälert nur Empfehlungsbreite), aber Audit-Hinweis: Wenn Volumen-/Feinhaar-Profile ein Glanz-Finish wollen, fällt rejuveniqe_oel u.U. raus, obwohl das PDF Universal-Eignung suggeriert. Optional: haarzustand-Filter lockern (z.B. `haarzustand=alle` oder zusätzlich `kraftlos`). Routing-Trigger selbst PDF-konform.

---

## restore_leave_in

**Status**: 🔴

**Routing-Aussage** (kurz): REQ-23 (optional) triggert auf `pflegelevel_numeric>=2` → slot leave_in (filter: restore_leave_in). Stammdaten: haarstaerke=mittel,dick; haarzustand=trocken.

**PDF-Belege** (S.1):
- Header: "Für trockenes Haar / Alle Haartypen / **Mittlere bis dicke Haarstruktur** / Vorbereitung"
- WARUM-Box: "Dieser pflegende Leave-In-Conditioner versorgt das Haar mit intensiver Feuchtigkeit, ohne es zu beschweren."
- WARUM ES WIRKT: "Sorgt für ultimative Stärke und intensive Pflege", "Stellt essenzielle Feuchtigkeit wieder her"
- IDEAL: "Ein Produkt für trockenes Haar wünschen, das zusätzliche Pflege bietet"

**Befund**: PDF-Header (K-08) ist explizit auf "Mittlere bis dicke Haarstruktur" UND "Für trockenes Haar" begrenzt. REQ-23 hat aber KEINE Bedingung auf haarstärke/haarzustand — der Trigger feuert allein bei `pflegelevel_numeric>=2`. Das bedeutet: ein User mit haarstärke=fein und pflegelevel=MID/HIGH kann restore_leave_in als Direkt-REQ-Treffer im leave_in-Slot bekommen, obwohl das PDF feines Haar explizit ausschließt ("ohne es zu beschweren" + Header sagt mittel/dick). 

Allerdings: das Pool-Scoring filtert in Node 12 anhand der Stammdaten `haarstaerke=mittel,dick` — daher würde restore_leave_in nur dann durchgehen, wenn das REQ-Routing das Pool-Filter umgeht. Frage an die Routing-Logik: hebelt REQ-23 die Stammdaten-Filter aus? Wenn ja → 🔴 Routing-Bug (Produkt landet auf falscher Haarstärke). Wenn nein → 🟡 (Routing harmlos, weil Pool-Filter den Direct-Hit verhindert).

Analog zu V1/V5/V6 aus Phase 3 (Direkt-REQ überschreibt Stammdaten): Annahme 🔴.

**Empfehlung**: REQ-23 um Bedingungen ergänzen, z.B. `pflegelevel_numeric>=2 AND hair_thickness IN (mittel,dick)` oder zusätzlich `hair_condition_contains=trocken`. Alternative: REQ-23 in optional-Pool-Vorschlag umwandeln statt Direkt-REQ. Stammdaten-Filter selbst sind PDF-konsistent.

---

## scalp_comfort_behandlung

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-05 (Linien-REQ) triggert auf `primary_scalp_state=juckend_empfindlich` → slot kopfhaut (filter: scalp_comfort). Stammdaten: kopfhaut=juckend_empfindlich,schuppig,trocken.

**PDF-Belege** (S.1):
- Header: "Für trockene oder empfindliche Kopfhaut, Schuppenbildung, Juckreiz und Reizungen"
- WARUM-Box: "Ein ausgewogenes Mikrobiom der Kopfhaut hilft, häufigen Kopfhautproblemen wie Schuppen, Juckreiz und Trockenheit vorzubeugen … Scalp Comfort™ Ausgleichende Kopfhautbehandlung reinigt, peelt und unterstützt ein ausgewogenes Mikrobiom der Kopfhaut"
- EIGENSCHAFTEN: "langanhaltende Linderung bei Trockenheit, vorübergehendem Juckreiz, Rötung und Schuppenbildung"
- IDEAL: "Eine trockene, gereizte, juckende, schuppige und empfindliche Kopfhaut haben"

**Befund**: Header (K-08) deckt 1:1 die Stammdaten-Filter kopfhaut=juckend_empfindlich,schuppig,trocken. REQ-05-Trigger (`juckend_empfindlich`) sauber belegt. Funktionen kopfhautpflege + ausgleichend (im Produktnamen + WARUM-Box) belegt.

**Empfehlung**: Routing korrekt, kein Edit.

---

## scalp_comfort_serum

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-20 (optional) triggert auf `needs_scalp_focus=TRUE AND pflegelevel_numeric>=2` → slot kopfhaut_taeglich. Zusätzlich REQ-05 (Linie). Stammdaten: kopfhaut=juckend_empfindlich,schuppig,trocken; bool ist_scalp_focus.

**PDF-Belege** (S.1):
- Header: "Für trockene oder empfindliche Kopfhaut, Schuppen, Juckreiz und Irritationen"
- WARUM-Box: "Das MONAT Scalp Comfort™ Ausgleichendes Serum spendet Feuchtigkeit, beruhigt und gleicht die Kopfhaut aus, lindert Juckreiz sowie Irritationen"
- EIGENSCHAFTEN: "die Kopfhaut erfrischt und Trockenheit lindert", "das Auftreten loser Schuppen auf Kopfhaut, Haaransatz und in den Längen reduziert", "Kopfhautbeschwerden wie vorübergehende Empfindlichkeit, Reizung, Rötung und Juckreiz lindert"
- IDEAL: "Ein Produkt für die tägliche Kopfhautpflege suchen"
- Anwendung: "Einmal täglich oder nach Bedarf als Teil deiner Haarpflegeroutine anwenden"

**Befund**: Header (K-08) deckt 1:1 Stammdaten-Filter. REQ-20-Trigger (`needs_scalp_focus`) gestützt durch ist_scalp_focus-Bool + IDEAL-Block "tägliche Kopfhautpflege". REQ-05 (Linie) PDF-konform.

**Empfehlung**: Routing korrekt, kein Edit.

---

## smoothing_deep_conditioner

**Status**: 🟢

**Routing-Aussage** (kurz): Kein Direkt-REQ, Pool-Scoring + CON-11 (Ausschluss bei `styling_goal_definition=TRUE`). Stammdaten: haarstaerke=fein,mittel; haarzustand=frizz,trocken,haarbruch.

**PDF-Belege** (S.1):
- Header: "/ Frizz / Alle Haartypen & -strukturen / Vorbereitung"
- WARUM-Box: "Dieser leistungsstarke Conditioner enthält eine wirkungsvolle Kombination aus pflanzlichen Aktivstoffen … Er spendet intensive Feuchtigkeit und sorgt für sichtbar glatteres, weicheres Haar – mit deutlich weniger Frizz, statischer Aufladung und fliegenden Härchen."
- WIE ES WIRKT: "Beseitigt Frizz und fliegende Härchen bis zu 72 Stunden", "7x weniger Haarbruch für müheloses Entwirren", "3x geschmeidigeres, glatteres Haar mit weniger Frizz"
- IDEAL: "Ihr Haar vor Luftfeuchtigkeit schützen möchten", "**Die Kämmbarkeit von feinem bis mittlerem Haar verbessern möchten**", "Glattes, frizzfreies Haar mit weniger Haarbruch wünschen"

**Befund**: Header sagt "Alle Haartypen & -strukturen", aber IDEAL nennt explizit "feines bis mittleres Haar" als Zielgruppe. Sheet `haarstaerke=fein,mittel` entspricht der IDEAL-Aussage (für eine FILTER-Spalte ist das nach K-08 zwar strikt nur durch Header gedeckt — Header sagt aber "Alle Haartypen", was widersprüchlich ist). Da PDF explizit "feines bis mittleres" in IDEAL nennt und Header nur "Alle Haartypen" lautet (nicht "Alle Haarstärken"), ist die engere Filterung im Sheet vertretbar. Funktionen (frizz_reduktion, feuchtigkeit, kaemmbarkeit, reparatur via Haarbruch-Reduktion) sauber belegt. CON-11 (Ausschluss bei styling_goal_definition) PDF-konsistent (Glättungs-Linie, kein Lockenstyling).

**Empfehlung**: Routing korrekt, kein Edit. Optional: haarstaerke-Filter zu `alle` lockern, da Header "Alle Haartypen" sagt — aber IDEAL-Aussage rechtfertigt die engere Filterung.

---

## smoothing_fohn_spray

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-04b triggert auf `prefers_straight_with_frizz=TRUE AND heat_use=yes|maybe` → slot styling_1. REQ-04 (Bool) `heat_use=yes|maybe` → ist_hitzeschutz=TRUE. CON-11 (`styling_goal_definition=TRUE`) und CON-13 (`needs_curl_care=TRUE AND hair_condition=frizz`) schließen aus. Stammdaten: haarzustand=frizz; bool ist_hitzeschutz+locken_geeignet.

**PDF-Belege** (S.1):
- Header: "/ Frizz / Alle Haartypen / Alle Haarstrukturen / Vorbereitung"
- WARUM-Box: "Erfülle dir den Traum von glatterem, geschmeidigerem Haar mit diesem hitzeaktivierten Stylingspray, das Frizz um 78 % reduziert und bis zu 72 Stunden lang vor Luftfeuchtigkeit schützt."
- WIE ES WIRKT: "Beseitigt Frizz und fliegende Härchen für bis zu 72 Stunden", "Hitzeschutz bis 232°C", "Stärkt das Haar und verbessert die Widerstandsfähigkeit gegen Hitzestyling"
- IDEAL: "Ein leichtes, frizzreduzierendes Stylingprodukt suchen", "Ihr Haar vor Luftfeuchtigkeit schützen wollen"

**Befund**: PDF betont klar Glättung + Frizz-Reduktion + Hitzeschutz — REQ-04b (`prefers_straight_with_frizz`) ist PDF-konform. CON-11 (Ausschluss bei Definition-Wunsch) und CON-13 (Ausschluss bei Lockenpflege+Frizz) PDF-gestützt: Header sagt nichts über Locken, WARUM-Text spricht ausdrücklich von "glatterem" Haar — Lockenträger werden hier korrekt rausgefiltert. Die nominell vorhandene Bool `locken_geeignet=TRUE` widerspricht zwar dem PDF, aber CON-13 schließt Lockenträger bei Frizz raus, was die Inkonsistenz im Routing entschärft. Migration #16/V5-Fixes haben das Routing sauber gemacht.

**Empfehlung**: Routing korrekt, kein Edit. Optional-Hinweis: `locken_geeignet=TRUE` in Stammdaten ist semantisch widersprüchlich zum PDF ("glatteres Haar"), wird aber durch CON-13 effektiv entschärft. Bei Gelegenheit `locken_geeignet=FALSE` setzen für saubere Stammdaten.

---

## smoothing_shampoo

**Status**: 🟢

**Routing-Aussage** (kurz): Kein Direkt-REQ, Pool-Scoring + CON-11 (`styling_goal_definition=TRUE` → exclude). Stammdaten: haarstaerke=alle; haarzustand=frizz,haarbruch.

**PDF-Belege** (S.1):
- Header: "Frizz / Alle Haartypen / Alle Haarstrukturen / Vorbereitung"
- WARUM-Box: "Dieses leistungsstarke Shampoo enthält pflanzliche Aktivstoffe, natürlich gewonnene Tenside und pflanzenbasierte Pflegestoffe. Es reinigt das Haar gründlich und sorgt für sichtbar glattere, weichere Längen – mit weniger Frizz, statischer Aufladung und fliegenden Härchen."
- WIE ES WIRKT: "5x glatteres, weicheres Haar mit weniger Frizz", "3x bessere Kämmbarkeit und weniger Haarbruch", "Beseitigt Frizz und fliegende Härchen für bis zu 72 Stunden"
- IDEAL: "Ein feuchtigkeitsspendendes Shampoo zur Frizz-Kontrolle suchen", "Ihr Haar vor Luftfeuchtigkeit schützen möchten", "Die Kämmbarkeit ihres Haars verbessern möchten"

**Befund**: Header (K-08) deckt "Alle Haartypen / Alle Haarstrukturen" → Sheet `haarstaerke=alle` konsistent. Frizz und Haarbruch im PDF mehrfach belegt → `haarzustand=frizz,haarbruch` PDF-konform. Funktionen (frizz_reduktion, feuchtigkeit, kaemmbarkeit, reparatur via Haarbruch-Reduktion) sauber. CON-11 PDF-konsistent (Glättungs-Linie schließt Definition-Wunsch aus).

**Empfehlung**: Routing korrekt, kein Edit.

---

## the_champ

**Status**: 🟢

**Routing-Aussage** (kurz): REQ-14 (optional) triggert auf `needs_dry_shampoo=TRUE` → slot finish. Stammdaten: haarzustand=kraftlos; haupt=reinigung,frische; neben=volumen,textur. (Migration #17 hat `needs_dry_shampoo` als abgeleitete Bool über `wash_frequency!=taeglich AND scalp_status contains fettig` neu definiert.)

**PDF-Belege** (S.1):
- Header: "Textur / Alle Haartypen und Strukturen / Finishing"
- WARUM-Box: "Dieses wasserlose Shampoo absorbiert Öl, Schmutz und Unreinheiten zwischen den Haarwäschen."
- WARUM ES FUNKTIONIERT: "Absorbiert Ölansammlungen an den Haarwurzeln", "Verleiht Volumen und Textur", "Mikrofeine Reisstärke hilft, überschüssiges Öl aufzunehmen"
- IDEAL: "Überschüssiges Öl im Laufe des Tages absorbieren möchten", "Ihr Styling auffrischen und das Haar revitalisieren möchten", "Ihr Haar sauber, frisch und angenehm duftend haben möchten"

**Befund**: Sanity-Check Migration #17 bestanden. `needs_dry_shampoo` (wash_frequency!=taeglich AND scalp_status enthält fettig) ist PDF-mäßig sauber belegt: "absorbiert Öl … zwischen den Haarwäschen" verlangt zwingend (a) öliges Aufkommen und (b) nicht-tägliches Waschen — exakt die abgeleitete Bool-Logik. Funktion `volumen` (Nebenfunktion) durch "Verleiht Volumen und Textur" belegt. `frische` durch "frisch und angenehm duftend". Haarzustand=kraftlos passt zur Volumen-Funktion (kraftloses Haar profitiert von Volumen-Lift) und wird durch IDEAL "revitalisieren" sanft gestützt.

**Empfehlung**: Routing korrekt, kein Edit. Migration #17-Fix bestätigt.

---

## Zusammenfassung Welle A

- 🟢 (10): curl_auffrischer, curl_gelee, hitzeschutzspray, kopfhaut_peeling, monat_black, scalp_comfort_behandlung, scalp_comfort_serum, smoothing_deep_conditioner, smoothing_fohn_spray, smoothing_shampoo, the_champ
- 🟡 (3): fohncreme (Stammdaten-Widerspruch ausschluss_bei vs. locken_geeignet vs. PDF-Header), ir_clinical_kopfhautserum (kopfhaut=trocken nur in IDEAL-Block, nicht im Header), rejuveniqe_oel (Stammdaten enger als PDF-"Universal-Öl")
- 🔴 (1): restore_leave_in (REQ-23 ohne haarstärke/haarzustand-Bedingung → kann Direkt-Hit für haarstärke=fein erzeugen, obwohl PDF-Header explizit "Mittlere bis dicke Haarstruktur" sagt)

**Priorität Phase 5**:
1. restore_leave_in: REQ-23 entweder um Stammdaten-Bedingungen erweitern oder klären, ob Direkt-REQ den Pool-Filter aushebelt (Routing-Logik-Check analog V1/V5/V6).
2. fohncreme: Stammdaten-Inkonsistenz `ausschluss_bei=wellig,lockig,kraus` + `locken_geeignet=TRUE` + PDF-Header "Alle Haartypen und-texturen" auflösen.
3. ir_clinical_kopfhautserum: Konventions-Klärung — gilt IDEAL-Block für FILTER-Spalten oder nur Header-Untertitel (K-08-Verschärfung)?
4. rejuveniqe_oel: optionale Lockerung haarzustand-Filter wenn Universal-Öl-Charakter im PDF wichtiger ist als enge Profilbindung.
