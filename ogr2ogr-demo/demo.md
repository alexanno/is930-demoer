# Demo: ogr2ogr

Kommandoene er hentet fra kursets sider [CLI og biblioteker](../modul-2/kilde/cli-og-biblioteker.md) og [Geografiske operasjoner](../modul-2/kilde/geografiske-operasjoner.md), og tilpasset eksempeldata fra GeoNorge, Natural Earth og Overture Maps. Alle kommandoene er testet med GDAL 3.13.

**Forberedelse (før demoen):** `./last-ned-data.sh` laster ned dataene til `data/`. Resultatene skrives til `ut/`. Kjør alt fra denne mappen.

| Fil | Kilde | Innhold |
|---|---|---|
| `data/ne_land.zip` | Natural Earth | Land i verden (177 polygoner, shapefile i zip) |
| `data/kommuner.gpkg` | GeoNorge, WFS administrative enheter | 357 kommuner, EPSG:4258 |
| `data/bygg.parquet` | Overture Maps | 3 601 bygninger i Kristiansand sentrum, GeoParquet, EPSG:4326 |
| `data/veger.parquet` | Overture Maps | 1 406 vegsegmenter, samme utsnitt |

Grunnmønsteret å vise først:

```
ogr2ogr [valg] <resultat> <kilde> [lag]
```

Resultatet står **først**, kilden etterpå. Formatet gjettes ut fra filendelsen, eller settes med `-f`.

---

## 1. Se hva som ligger i en fil: `ogrinfo`

```bash
# Hvilke lag finnes?
ogrinfo data/kommuner.gpkg

# Sammendrag: geometritype, antall, utstrekning, koordinatsystem og kolonner
ogrinfo -so -al data/kommuner.gpkg

# Samme for en zippet shapefile direkte fra Natural Earth (/vsizip/ leser inni zip-filen)
ogrinfo -so -al /vsizip/data/ne_land.zip

# GeoParquet fra Overture: legg merke til kolonnene (height, class, num_floors ...)
ogrinfo -so -al data/bygg.parquet

# Se noen få rader uten geometri
ogrinfo -geom=NO -al data/kommuner.gpkg -where "kommunenummer < 1000"
```

**Snakkepunkter:** Koordinatsystem (EPSG:4258 for GeoNorge, EPSG:4326 for Overture), geometritype, `Geometry Column` (navnet trengs i SQL) og `Feature Count`.

---

## 2. Konvertere format (filendelsen styrer)

```bash
# Natural Earth (shapefile i zip) til GeoPackage, bare noen få kolonner
ogr2ogr -f GPKG ut/land.gpkg /vsizip/data/ne_land.zip -nln land \
  -nlt PROMOTE_TO_MULTI -select NAME,CONTINENT,POP_EST,ISO_A3

# GeoPackage til GeoJSON
ogr2ogr ut/land.geojson ut/land.gpkg

# Til CSV, med geometrien som WKT-tekst
ogr2ogr -f CSV ut/land.csv ut/land.gpkg -lco GEOMETRY=AS_WKT

# CSV uten geometri, bare de fem største landene (SQL i stedet for -where)
ogr2ogr -f CSV ut/topp5.csv ut/land.gpkg \
  -sql "SELECT NAME, POP_EST FROM land ORDER BY POP_EST DESC LIMIT 5"
cat ut/topp5.csv
```

**Snakkepunkter:** `-f` velger format, `-nln` gir lagnavn, `-select` velger kolonner, `-nlt PROMOTE_TO_MULTI` unngår advarsel når en fil blander Polygon og MultiPolygon.

---

## 3. Reprojisere

```bash
# Kommuner fra EPSG:4258 (lengde/bredde) til UTM sone 32 (meter)
ogr2ogr -t_srs EPSG:25832 ut/kommuner_utm32.gpkg data/kommuner.gpkg

# Sammenlign utstrekningen: grader før, meter etter
ogrinfo -so -al data/kommuner.gpkg        | grep Extent
ogrinfo -so -al ut/kommuner_utm32.gpkg    | grep Extent

# Verden til Web Mercator (EPSG:3857), uten Antarktis som ellers sprenger utstrekningen
ogr2ogr -t_srs EPSG:3857 -f GPKG ut/land_3857.gpkg ut/land.gpkg -where "NAME <> 'Antarctica'"
```

**Snakkepunkter:** `-t_srs` transformerer, `-s_srs` brukes bare hvis filen mangler koordinatsystem (da er det en *tilordning*, ikke en transformasjon). Veien til å få meter for buffer og areal går via et projisert system.

---

## 4. Filtrere på attributt

```bash
# Europeiske land med over 10 millioner innbyggere
ogr2ogr ut/europa.geojson ut/land.gpkg -where "CONTINENT = 'Europe' AND POP_EST > 10000000"

# Bare Kristiansand kommune
ogr2ogr ut/kristiansand.gpkg data/kommuner.gpkg -where "kommunenavn = 'Kristiansand'" -nln kristiansand

# Bare eneboliger fra Overture, med tre kolonner
ogr2ogr ut/hus.gpkg data/bygg.parquet -where "class = 'house'" \
  -select id,class,num_floors -nlt PROMOTE_TO_MULTI -nln hus

# Antall treff
ogrinfo -so -al ut/hus.gpkg | grep "Feature Count"
```

---

## 5. Romlig utsnitt og klipp

```bash
# Rektangel i lengde/bredde (xmin ymin xmax ymax) i kildens koordinatsystem: 474 bygninger
ogr2ogr ut/utsnitt.gpkg data/bygg.parquet \
  -spat 8.005 58.145 8.015 58.152 -nlt PROMOTE_TO_MULTI -nln bygg

# Klipp bygninger til kommunegrensen (en polygon fra et annet lag)
ogr2ogr ut/bygg_kristiansand.gpkg data/bygg.parquet \
  -clipsrc ut/kristiansand.gpkg -nlt PROMOTE_TO_MULTI -nln bygg
```

Fra [Geografiske operasjoner](../modul-2/kilde/geografiske-operasjoner.md) kan det også klippes direkte fra kommunelaget uten å lage en egen fil først:

```bash
ogr2ogr ut/bygg_klippet.gpkg data/bygg.parquet \
  -clipsrc data/kommuner.gpkg -clipsrclayer kommuner -clipsrcwhere "kommunenavn = 'Kristiansand'" \
  -nlt PROMOTE_TO_MULTI -nln bygg
```

**Snakkepunkter:** `-spat` filtrerer (tar med objekter som berører rektangelet), `-clipsrc` *skjærer* geometrien. Filteret `-spat` er raskt, spesielt med romlig indeks.

---

## 6. Spatial SQL med `-dialect sqlite`

SQLite-dialekten gir tilgang til `ST_`-funksjoner (via SpatiaLite/GEOS). Geometrikolonnen heter `geom` i kommunene (satt ved nedlasting) og `geometry` i Overture-filene.

```bash
# Buffer: 25 m rundt hovedveger (reprojiser først, så buffer blir i meter)
ogr2ogr ut/vegbuffer.gpkg data/veger.parquet -t_srs EPSG:25832 \
  -dialect sqlite -sql "SELECT class, ST_Buffer(geometry, 25) AS geom
                        FROM veger WHERE class IN ('primary','secondary','tertiary')" \
  -nln vegbuffer -nlt PROMOTE_TO_MULTI

# Dissolve: kommuner slått sammen til fylker (første to siffer i kommunenummeret)
ogr2ogr ut/fylker.gpkg data/kommuner.gpkg \
  -dialect sqlite -sql "SELECT kommunenummer/100 AS fylkesnr, ST_Union(geom) AS geom
                        FROM kommuner GROUP BY kommunenummer/100" \
  -nln fylker -nlt PROMOTE_TO_MULTI

# Sentroider for kommunene i Agder (fylkesnr 42)
ogr2ogr -f GPKG ut/sentroider.gpkg data/kommuner.gpkg \
  -dialect sqlite -sql "SELECT kommunenavn, ST_Centroid(geom) AS geom
                        FROM kommuner WHERE kommunenummer/100 = 42" \
  -nln sentroider

# Bygninger med minst fem etasjer
ogr2ogr ut/hoye_bygg.gpkg data/bygg.parquet \
  -dialect sqlite -sql "SELECT id, class, num_floors, geometry FROM bygg WHERE num_floors >= 5" \
  -nln hoye_bygg -nlt PROMOTE_TO_MULTI
```

**Snakkepunkter:** Buffer i grader gir meningsløse resultater, derfor `-t_srs EPSG:25832` først (se [Koordinatsystem-fella](../modul-2/kilde/ki-agenter-og-stack-valg.md) for KI-agenter). Romlig kobling og overlay er enklere i DuckDB, PostGIS eller geopandas.

---

## 7. Formater for web og analyse

```bash
# FlatGeobuf: raskt å lese direkte fra nettet, med romlig indeks
ogr2ogr ut/utsnitt.fgb ut/utsnitt.gpkg

# GeoParquet: kolonnebasert, bra for store datamengder og DuckDB
ogr2ogr ut/kommuner.parquet data/kommuner.gpkg

# GeoJSON til nettkart: WGS84, 6 desimaler (ca. 10 cm), RFC 7946
ogr2ogr -f GeoJSON ut/utsnitt.geojson ut/utsnitt.gpkg -t_srs EPSG:4326 \
  -lco RFC7946=YES -lco COORDINATE_PRECISION=6

# Sammenlign filstørrelsene
ls -lh ut/utsnitt.* ut/kommuner.parquet data/kommuner.gpkg
```

---

## 8. Hente data rett fra en tjeneste (WFS)

Dette er samme kommando som lastet ned kommunene i `last-ned-data.sh`.

```bash
# Hvilke lag har tjenesten?
ogrinfo 'WFS:https://wfs.geonorge.no/skwms1/wfs.administrative_enheter'

# Hent bare Agder fylke
ogr2ogr -f GPKG ut/agder.gpkg \
  'WFS:https://wfs.geonorge.no/skwms1/wfs.administrative_enheter' app:Fylke \
  -select fylkesnummer,fylkesnavn -where "fylkesnavn = 'Agder'"
```

---

## 9. Laste inn i PostGIS (bare vist, krever database)

Kommandoen er fra kursets side. Forutsetter en kjørende PostGIS-database `gis`.

```bash
ogr2ogr -f PostgreSQL PG:"dbname=gis user=bruker" ut/hus.gpkg -nln bygg
```

---

## 10. Ny syntaks fra GDAL 3.11: `gdal vector`

De klassiske kommandoene fungerer i alle versjoner. Fra GDAL 3.11 finnes også én samlet kommando med underkommandoer:

```bash
gdal vector convert ut/utsnitt.gpkg ut/utsnitt2.fgb
gdal vector reproject --dst-crs EPSG:25832 ut/utsnitt.gpkg ut/utsnitt_utm.gpkg

# Pipeline: flere steg i én kommando (les, filtrer, reprojiser, skriv)
gdal vector pipeline read data/kommuner.gpkg \
  ! filter --where "kommunenavn='Kristiansand'" \
  ! reproject --dst-crs EPSG:25832 \
  ! write ut/kristiansand_utm.gpkg
```

---

## Feil som kan dukke opp

| Melding | Årsak | Løsning |
|---|---|---|
| `A geometry of type MULTIPOLYGON is inserted into layer of geometry type POLYGON` | Blandede geometrityper i kilden | Legg til `-nlt PROMOTE_TO_MULTI` |
| `Mismatched geometry type` (FlatGeobuf, Parquet) | Samme årsak, men her er det en feil | `-nlt PROMOTE_TO_MULTI` |
| `no such column: geom` | Geometrikolonnen heter noe annet | Se `Geometry Column` i `ogrinfo -so` |
| `not recognized as being in a supported file format` (zip) | Zip må åpnes med `/vsizip/` | `/vsizip/data/ne_land.zip` |
| Bufferen er «feil» | Buffer i grader | Reprojiser til UTM først |

## Fra kursets aktivitetsliste (oppgaver til deltakerne)

- Kjør `ogrinfo -so -al` på en geofil du har. Hva forteller den om koordinatsystem, geometritype og antall objekter? Konverter filen til et annet format.
- Be en KI-agent lage en `ogr2ogr`-kommando som klipper et lag til én kommune. Sjekk at kommandoen virker, og at koordinatsystemet stemmer.

Referanse: [GDAL: ogr2ogr](https://gdal.org/en/stable/programs/ogr2ogr.html) · [IS-218-oppgaver](https://github.com/alexanno/GeografiskAI_UiA_IS-218/blob/main/V2025/03-Geografiske%20informasjonssystemer/tutorials.md#gdal-og-ogr2ogr)
