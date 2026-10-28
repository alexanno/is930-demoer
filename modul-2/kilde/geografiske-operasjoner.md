@@ intro
Nesten all geografisk analyse er satt sammen av noen få byggeklosser. Når du kjenner de seks operasjonene under, gjenkjenner du dem i ethvert verktøy, fra QGIS-menyer til SQL og kode. Siden er bevisst kort: forklaring først, et lite utvalg tekniske eksempler nederst, og lenker til manualene for resten.

@@ innhold
#### Før du begynner: bruk et koordinatsystem i meter

Avstander og arealer regnes i koordinatsystemets enhet. En buffer på «100» i EPSG:4326 betyr 100 *grader*, ikke 100 meter. For norske data bruker du et projisert system i meter, for eksempel EPSG:25832 eller 25833 (se [Projeksjoner, kartografi og visualiseringsmetoder](side:projeksjoner-kartografi-og-visualiseringsmetoder)). Sjekk alltid koordinatsystemet før du måler.

#### Seks operasjoner steg for steg

| Operasjon | Spørsmålet den svarer på | Eksempel fra norsk forvaltning og næringsliv | Pass opp | QGIS |
|---|---|---|---|---|
| **1. Buffer** | Hva ligger innenfor en viss avstand fra et objekt? | Sonen på 100 m langs sjø og vassdrag der byggeforbudet i plan- og bygningsloven § 1-8 gjelder. | Enheten er koordinatsystemets enhet. Overlappende buffere kan slås sammen eller beholdes hver for seg. | [Buffer](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#buffer) |
| **2. Klipp (clip)** | Gi meg bare den delen av laget som ligger innenfor dette området. | Vegnett eller bygg klippet til én kommune. | Du beholder bare attributtene til laget du klipper. Klippeområdet tilfører ingenting. | [Clip](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#clip) |
| **3. Romlig kobling** | Hvilke egenskaper har stedet objektet ligger på? | Hvilken kommune, grunnkrets eller reguleringsplan ligger hvert bygg i? | Et objekt kan treffe flere områder og gi flere rader. Velg riktig relasjon: innenfor, krysser eller berører. | [Join attributes by location](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#join-attributes-by-location) |
| **4. Nærhet** | Hva er nærmest, og hva ligger innenfor X meter? | Nærmeste brannstasjon fra en bolig, eller skoler innenfor 1 km fra en vei. | Luftlinje er ikke veilengde (se ruteberegning under). Store datasett trenger romlig indeks. | [Join attributes by nearest](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeneral.html#join-attributes-by-nearest) |
| **5. Aggregering** | Hvor mange eller hvor mye finnes i hvert område? Og kan områder slås sammen? | Antall bygg og samlet bruksareal per grunnkrets. Grunnkretser slått sammen til kommuner (dissolve). | Objekter må kobles til riktig område før de telles. Objekter som krysser en grense kan telles flere ganger. | [Count points in polygon](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoranalysis.html#count-points-in-polygon), [Dissolve](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#dissolve) |
| **6. Overlay** | Hvordan overlapper to lag, og hva er felles eller ulikt? | Hvilke deler av hver eiendom ligger i en flomsone eller faresone. | Resultatet får attributter fra begge lag og deles opp i mindre biter. Regn ut areal på nytt etterpå. | [Intersection](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#intersection) |

#### Klipp, intersect eller overlay?

Disse blandes ofte sammen. Forskjellen er hva du får tilbake:

| Operasjon | Du får | Attributter fra | Bruk når |
|---|---|---|---|
| **Clip** | Delene av lag A som ligger innenfor B | Bare A | Du vil ha et utsnitt av A. |
| **Intersection** | Områder der A og B overlapper | A og B | Du vil vite hvor og hvor mye de overlapper. |
| **Union** | Alt fra A og B, delt opp der de overlapper | A og B | Du vil samle to områdelag til ett. |
| **Difference** | Delene av A som ikke ligger i B | Bare A | Du vil ha det som ligger utenfor, for eksempel bygg utenfor en faresone. |

Alle fire finnes som verktøy i QGIS under *Vector → Geoprocessing Tools*: [Clip](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#clip), [Intersection](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#intersection), [Union](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#union) og [Difference](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html#difference).

#### Tekniske eksempler

Samme operasjoner som kode. Eksemplene bruker små syntetiske datasett i EPSG:25833 (meter) rundt Kristiansand: `bygg` (punkter), `vassdrag` (linjer), `kommuner` og `grunnkrets` (flater), `brannstasjon` (punkter), `eiendom` og `faresone` (flater). Du finner dem i [eksempeldata](https://github.com/alexanno/is930-demoer/tree/main/modul-2/eksempeldata), eller bytter ut filnavn og kolonner med dine egne data. Hvordan du kjører kode uten oppsett, står på siden [CLI og biblioteker](side:cli-og-biblioteker).

**SQL med DuckDB** (samme `ST_`-funksjoner finnes i PostGIS og de fleste databaser):

```sql
INSTALL spatial; LOAD spatial;   -- én gang per økt

-- 1 Buffer: 100 m rundt vassdrag
SELECT navn, ST_Buffer(geom, 100) AS geom FROM st_read('vassdrag.gpkg');

-- 2 Klipp: vassdrag innenfor Kristiansand kommune
SELECT v.navn, ST_Intersection(v.geom, k.geom) AS geom
FROM st_read('vassdrag.gpkg') v, st_read('kommuner.gpkg') k
WHERE k.kommunenavn = 'Kristiansand' AND ST_Intersects(v.geom, k.geom);

-- 3 Romlig kobling: hvilken kommune ligger hvert bygg i?
SELECT b.bygg_id, k.kommunenavn
FROM st_read('bygg.gpkg') b JOIN st_read('kommuner.gpkg') k ON ST_Within(b.geom, k.geom);

-- 4 Nærhet: nærmeste brannstasjon og avstand i meter for hvert bygg
SELECT b.bygg_id, s.navn, ST_Distance(b.geom, s.geom) AS meter
FROM st_read('bygg.gpkg') b,
     LATERAL (SELECT navn, geom FROM st_read('brannstasjon.gpkg') s
              ORDER BY ST_Distance(b.geom, s.geom) LIMIT 1) s;
-- bare bygg innen 100 m fra vassdrag: ... WHERE ST_DWithin(b.geom, v.geom, 100)

-- 5 Aggregering: antall bygg og samlet bruksareal per grunnkrets
SELECT g.grunnkretsnummer, count(*) AS antall_bygg, sum(b.bruksareal) AS sum_areal
FROM st_read('bygg.gpkg') b JOIN st_read('grunnkrets.gpkg') g ON ST_Within(b.geom, g.geom)
GROUP BY g.grunnkretsnummer;
-- ...og dissolve: grunnkretser slått sammen til kommuner
SELECT kommunenummer, ST_Union_Agg(geom) AS geom FROM st_read('grunnkrets.gpkg') GROUP BY kommunenummer;

-- 6 Overlay: hvor stor andel av hver eiendom ligger i faresonen?
SELECT e.gnr_bnr, ST_Area(ST_Intersection(e.geom, f.geom)) / ST_Area(e.geom) AS andel
FROM st_read('eiendom.gpkg') e JOIN st_read('faresone.gpkg') f ON ST_Intersects(e.geom, f.geom);
```

**Python med geopandas:**

```python
import geopandas as gpd

bygg = gpd.read_file("bygg.gpkg")
vassdrag = gpd.read_file("vassdrag.gpkg")
kommuner = gpd.read_file("kommuner.gpkg")
brann = gpd.read_file("brannstasjon.gpkg")
grunnkrets = gpd.read_file("grunnkrets.gpkg")
eiendom = gpd.read_file("eiendom.gpkg")
faresone = gpd.read_file("faresone.gpkg")
print(bygg.crs)  # sjekk koordinatsystemet først

buffer = vassdrag.buffer(100)                                                  # 1 buffer
klipp = gpd.clip(vassdrag, kommuner[kommuner.kommunenavn == "Kristiansand"])  # 2 klipp
kobling = gpd.sjoin(bygg, kommuner[["kommunenavn", "geometry"]], predicate="within")      # 3 kobling
naermeste = gpd.sjoin_nearest(bygg, brann[["navn", "geometry"]], distance_col="meter")  # 4 nærhet
per_krets = (gpd.sjoin(bygg, grunnkrets, predicate="within")                   # 5 aggregering
             .groupby("grunnkretsnummer")
             .agg(antall_bygg=("bygg_id", "size"), sum_areal=("bruksareal", "sum")))
kommuner_av_krets = grunnkrets.dissolve(by="kommunenummer")                    # 5 dissolve
overlay = gpd.overlay(eiendom, faresone, how="intersection")                   # 6 overlay
```

**Kommandolinje med ogr2ogr** (egner seg best til buffer, klipp og dissolve. Romlig kobling og overlay er enklere i SQL eller geopandas):

```bash
# Finn navnet på geometrikolonnen (her «geom») og koordinatsystemet
ogrinfo -so kommuner.gpkg kommuner

# 1 Buffer: 100 m rundt vassdrag (SQLite-dialekten gir tilgang til ST_-funksjoner)
ogr2ogr -f GPKG buffer.gpkg vassdrag.gpkg -dialect sqlite -sql "SELECT navn, ST_Buffer(geom, 100) AS geom FROM vassdrag"

# 2 Klipp: vassdrag innenfor Kristiansand kommune
ogr2ogr -f GPKG klippet.gpkg vassdrag.gpkg -clipsrc kommuner.gpkg -clipsrclayer kommuner -clipsrcwhere "kommunenavn = 'Kristiansand'"

# 5 Dissolve: grunnkretser slått sammen til kommuner
ogr2ogr -f GPKG kommuner_av_krets.gpkg grunnkrets.gpkg -dialect sqlite -sql "SELECT kommunenummer, ST_Union(geom) AS geom FROM grunnkrets GROUP BY kommunenummer"
```

#### Fordypning: ruteberegning

Nærhet i luftlinje er ofte ikke nok. Hvor lang tid tar det faktisk å kjøre fra brannstasjonen til huset? Da trenger du *ruteberegning*, som regner på et nettverk i stedet for på flaten.

| Begrep | Betyr |
|---|---|
| **Graf** | Vegnettet som noder (kryss) og kanter (veistrekninger). Hver kant har en kostnad, for eksempel tid eller lengde. |
| **Korteste vei** | Den ruten med lavest samlet kostnad. Algoritmene heter blant annet Dijkstra og A*. Raskeste og korteste rute er ikke alltid den samme ruten. |
| **Isokron** | Området du rekker innen for eksempel 15 minutter fra et punkt. |
| **Avstandsmatrise** | Reisetid eller avstand mellom mange punkter på én gang. |
| **Ruteoptimalisering (VRP)** | Beste rekkefølge på stoppene for ett eller flere kjøretøy, kjent fra distribusjon og hjemmetjeneste. |

Norske vegnettsdata kommer fra Nasjonal vegdatabank (NVDB): se [Forenklet Elveg 2.0](https://data.norge.no/en/datasets/a6e26415-8cd5-30af-a39d-b545aed5bbea/forenklet-elveg-20) og [NVDB rutedatasett](https://data.norge.no/en/datasets/cbf42df2-e109-3412-9176-8d8d4d030645/nvdb-rutedatasett). De fleste åpne rutemotorer bruker OpenStreetMap.

| Tjeneste eller bibliotek | Type | Kostnad og lisens | Passer til |
|---|---|---|---|
| **[OpenRouteService](https://openrouteservice.org/)** | Åpen web-API fra HeiGIT. Kan også driftes selv. | Gratis plan med API-nøkkel og kvoter ([se planer](https://openrouteservice.org/dev/#/signup)). Åpen kildekode. | Ruter, isokroner, avstandsmatriser og optimalisering. Har [QGIS-plugin (ORS Tools)](https://plugins.qgis.org/plugins/ORStools/) og klienter for [Python](https://github.com/GIScience/openrouteservice-py) og JavaScript. |
| **[OSRM](https://project-osrm.org/)** | Rask rutemotor for egen drift. | Åpen kildekode | Mange raske ruter og matriser på OSM-data. |
| **[Valhalla](https://valhalla.github.io/valhalla/)** | Rutemotor med mange transportmåter. | Åpen kildekode | Fleksible profiler og isokroner i egen drift. |
| **[GraphHopper](https://www.graphhopper.com/)** | Rutemotor og kommersiell tjeneste. | Åpen kjerne og betalt tjeneste | Ruter og optimalisering, også som ferdig tjeneste. |
| **[pgRouting](https://pgrouting.org/)** | Utvidelse til PostGIS. | Åpen kildekode | Ruteberegning med SQL på eget vegnett i databasen. |
| **[OSMnx](https://osmnx.readthedocs.io/)** og NetworkX | Python-biblioteker. | Åpen kildekode | Analyse av vegnett i notebooks og undervisning. |
| **QGIS nettverksanalyse** | Innebygde algoritmer (korteste vei, serviceområde). | Åpen kildekode | Engangsanalyser på eget vegnett. Se [QGIS Training Manual](https://docs.qgis.org/latest/en/docs/training_manual/vector_analysis/network_analysis.html). |
| **[OpenTripPlanner](https://www.opentripplanner.org/)** | Reiseplanlegger for kollektivtransport. | Åpen kildekode | Kollektivreiser fra rutedata (GTFS) og OSM. [Entur](https://developer.entur.no/docs/open-services/journey-planner) tilbyr åpent API for norske kollektivreiser. |
| **Google, Mapbox, HERE, Esri** | Kommersielle rutetjenester. | Betaling per forespørsel, ofte med gratisnivå | Produksjon med trafikkdata, kundestøtte og avtalt driftsnivå. |

Start gjerne med [OpenRouteService](https://openrouteservice.org/): du kan teste i nettleseren på [maps.openrouteservice.org](https://maps.openrouteservice.org/), bruke QGIS-pluginen, og senere kalle API-et fra Python eller JavaScript med en gratis nøkkel.

@@ aktivitet
- Last inn kommuner og et vassdragslag i QGIS. Lag en buffer på 100 m. Gjør det først på laget i EPSG:4326 og deretter etter at du har reprojisert til EPSG:25833. Hva ser du, og hvorfor?
- Finn en av de seks operasjonene i QGIS sin *Processing Toolbox*. Hvilke parametere trenger den, og hva er resultatet?
- Kjør én av DuckDB-spørringene på eksempeldataene. Endre bufferavstanden eller faresonen, og se hvordan svaret endres.
- Åpne [maps.openrouteservice.org](https://maps.openrouteservice.org/) og beregn en isokron på 15 minutter fra arbeidsplassen din, først med bil og deretter med sykkel. Hvorfor ser områdene så forskjellige ut?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [QGIS Training Manual: Vector Analysis](https://docs.qgis.org/latest/en/docs/training_manual/vector_analysis/index.html)
- [Essentials of Geographic Information Systems: Geospatial Analysis I, vector operations](https://saylordotorg.github.io/text_essentials-of-geographic-information-systems/s11-geospatial-analysis-i-vector-o.html)

@@ interessert
- [IS-218: Vektoranalyse (forelesningsnotater med flere eksempler)](https://github.com/alexanno/GeografiskAI_UiA_IS-218/blob/main/V2025/10-KI%20og%20GIScience/vektoranalyse.md)
- [QGIS: Vector overlay-verktøy](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectoroverlay.html)
- [DuckDB spatial: funksjoner](https://duckdb.org/docs/stable/core_extensions/spatial/functions.html)
- [GeoPandas: set operations med overlay](https://geopandas.org/en/stable/docs/user_guide/set_operations.html)
- [OpenRouteService: dokumentasjon](https://giscience.github.io/openrouteservice/)
