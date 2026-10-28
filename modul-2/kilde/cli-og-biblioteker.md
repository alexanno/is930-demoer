@@ intro
Kommandolinje og kode gjør arbeid repeterbart: det du gjør én gang kan kjøres på neste datasett, deles med andre og kvalitetssikres. Det er også her KI-agenter er mest nyttige, fordi de kan skrive og kjøre koden for deg. Siden gir et oversiktskart over verktøyene, ikke en kodeopplæring.

@@ innhold
#### GDAL og ogr2ogr: sveitsisk lommekniv for geodata

[GDAL](https://gdal.org/) er biblioteket under motorhjelmen i nesten alle GIS-verktøy, også QGIS og geopandas. Kommandolinjeverktøyene kan lese og skrive over hundre formater. `ogr2ogr` brukes på vektordata, `gdal_translate` og `gdalwarp` på raster. På Windows bruker du *OSGeo4W Shell* som følger med QGIS, på Mac installerer du med `brew install gdal`.

| Oppgave | Kommando |
|---|---|
| Se hva som ligger i en fil | `ogrinfo -so -al kommuner.gpkg` |
| Konvertere format (filendelsen styrer) | `ogr2ogr kommuner.geojson kommuner.gpkg` |
| Reprojisere til lengde/bredde | `ogr2ogr -t_srs EPSG:4326 bygg_4326.gpkg bygg.gpkg` |
| Filtrere på attributt | `ogr2ogr -where "bruksareal > 300" store_bygg.gpkg bygg.gpkg` |
| Hente et rektangulært utsnitt | `ogr2ogr -spat 80000 6460000 90000 6470000 utsnitt.gpkg bygg.gpkg` |
| Lage FlatGeobuf for web | `ogr2ogr bygg.fgb bygg.gpkg` |
| Laste inn i PostGIS | `ogr2ogr -f PostgreSQL PG:"dbname=gis user=bruker" bygg.gpkg -nln bygg` |
| Raster: gjøre om til COG | `gdal_translate -of COG inn.tif ut.tif` |
| Raster: reprojisere | `gdalwarp -t_srs EPSG:25833 inn.tif ut.tif` |

Buffer, klipp og dissolve med `ogr2ogr` står under [Geografiske operasjoner](side:geografiske-operasjoner). Fra GDAL 3.11 finnes også én samlet kommando, for eksempel `gdal vector convert` og `gdal raster info`. De klassiske kommandoene over fungerer i alle versjoner. Flere oppgaver finnes i [IS-218-oppgavene](https://github.com/alexanno/GeografiskAI_UiA_IS-218/blob/main/V2025/03-Geografiske%20informasjonssystemer/tutorials.md#gdal-og-ogr2ogr).

#### Flere kommandolinjeverktøy

| Verktøy | Hva er det? | Typisk oppgave |
|---|---|---|
| **[PROJ](https://proj.org/)** (`projinfo`, `cs2cs`) | Verktøy for koordinatsystemer | Slå opp og transformere mellom koordinatsystemer. |
| **[DuckDB](https://duckdb.org/)** | SQL på filer, som kommandolinje eller bibliotek | Spørre i GeoParquet og GeoPackage uten server. |
| **[osm2pgsql](https://osm2pgsql.org/)** | Importerer OpenStreetMap til PostGIS | Bygge en lokal database av OSM-data. |
| **[osmium](https://osmcode.org/osmium-tool/)** | Filtrerer og klipper OSM-filer | Hente ut for eksempel alle veier i en kommune. |
| **[tippecanoe](https://github.com/felt/tippecanoe)** og **[pmtiles](https://docs.protomaps.com/pmtiles/cli)** | Lager vektorfliser og PMTiles | Gjøre store datasett om til én fil for statiske kart. |
| **[qgis_process](https://docs.qgis.org/latest/en/docs/user_manual/processing/standalone.html)** | Kjører QGIS sine analyseverktøy fra terminalen | Automatisere en QGIS-analyse uten å åpne programmet. |

#### Python-biblioteker

| Bibliotek | Hva er det? | Typisk bruk |
|---|---|---|
| **[geopandas](https://geopandas.org/)** | Tabeller med geometri, bygget på pandas | Lese, analysere og skrive vektordata. Dekker alle seks operasjoner. |
| **[shapely](https://shapely.readthedocs.io/)** | Geometrier og geometrioperasjoner | Buffer, skjæring og avstand på enkeltgeometrier. |
| **[pyproj](https://pyproj4.github.io/pyproj/)** | Koordinatsystemer og transformasjoner | Reprojisere koordinater. |
| **[pyogrio](https://pyogrio.readthedocs.io/)** | Rask lesing og skriving av vektorfiler via GDAL | Lese store filer raskt (brukes av geopandas). |
| **[rasterio](https://rasterio.readthedocs.io/)** | Lesing og skriving av raster | Arbeide med GeoTIFF, COG og høydemodeller. |
| **[duckdb](https://duckdb.org/docs/stable/clients/python/overview.html)** | SQL på geodata fra Python | Analysere GeoParquet og GeoPackage med SQL. |
| **[h3](https://uber.github.io/h3-py/)** | Heksagonalt rutenett (H3) | Aggregere punktdata til like store celler. |
| **[osmnx](https://osmnx.readthedocs.io/)** | Henter vegnett og bygg fra OpenStreetMap | Nettverksanalyse og ruting i notebooks. |
| **[leafmap](https://leafmap.org/)** | Interaktive kart i notebooks | Vise data på kart mens du analyserer. |

#### JavaScript-biblioteker

| Bibliotek | Hva er det? | Typisk bruk |
|---|---|---|
| **[MapLibre GL JS](https://maplibre.org/)** | Åpen kildekode-bibliotek for vektorkart med WebGL | Moderne, raske kartapper med vektorfliser. |
| **[OpenLayers](https://openlayers.org/)** | Fullverdig kartbibliotek | Avanserte kart med WMS, WMTS, WFS og mange koordinatsystemer. |
| **[Leaflet](https://leafletjs.com/)** | Enkelt og lett kartbibliotek | Raske og enkle kart med markører og GeoJSON. |
| **[Turf.js](https://turfjs.org/)** | Geografisk analyse i nettleseren | Buffer, skjæring og nærmeste punkt direkte i JavaScript. |
| **[proj4js](http://proj4js.org/)** | Koordinatomregning | Konvertere mellom koordinatsystemer i nettleseren. |
| **[deck.gl](https://deck.gl/)** | Visualisering av store datasett med WebGL | Vise millioner av punkter eller bevegelser. |
| **[DuckDB-WASM](https://duckdb.org/docs/stable/clients/wasm/overview.html)** | DuckDB som kjører i nettleseren | SQL på GeoParquet uten backend. |

Nettleseren laster ikke moduler fra `file://`, så kartsider med `import` må åpnes via en lokal server: `uv run python -m http.server 8000`, og deretter `http://localhost:8000`.

#### Kom i gang uten oppsett: uv

Python-eksemplene i dette kurset kan kjøres uten å sette opp et miljø på forhånd. Med [uv](https://docs.astral.sh/uv/) henter kommandoen pakkene den trenger hver gang:

```bash
uv run --with geopandas --with pyogrio python eksempel.py
uv run --with duckdb python -c "import duckdb; duckdb.sql('SELECT 42 AS svar').show()"
```

@@ aktivitet
- Kjør `ogrinfo -so -al` på en geofil du har. Hva forteller den om koordinatsystem, geometritype og antall objekter? Konverter filen til et annet format med `ogr2ogr`.
- Kjør et av geopandas-eksemplene fra [Geografiske operasjoner](side:geografiske-operasjoner) med `uv run`. Bytt ut en av filene med egne data.
- Be en KI-agent om å lage en `ogr2ogr`-kommando som klipper et lag til én kommune. Sjekk at kommandoen virker, og at koordinatsystemet stemmer.
- Gå inn på [Turf.js](https://turfjs.org/) og finn funksjonen for buffer. Hvilke av de seks operasjonene finnes i biblioteket?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [GDAL: ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html)
- [GeoPandas: Getting started](https://geopandas.org/en/stable/getting_started.html)

@@ interessert
- [Geographic Data Science with Python (Rey, Arribas-Bel og Wolf)](https://geographicdata.science/book/)
- [uv: dokumentasjon](https://docs.astral.sh/uv/)
- [MapLibre GL JS: dokumentasjon](https://maplibre.org/maplibre-gl-js/docs/)
- [IS-218: oppgaver med GDAL og ogr2ogr](https://github.com/alexanno/GeografiskAI_UiA_IS-218/blob/main/V2025/03-Geografiske%20informasjonssystemer/tutorials.md#gdal-og-ogr2ogr)
