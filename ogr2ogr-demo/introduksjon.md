# ogr2ogr: introduksjon

`ogr2ogr` leser og skriver vektordata (punkter, linjer, flater) i over hundre formater. Kommandoen har alltid samme oppbygning:

```
ogr2ogr  [valg]  resultat  kilde  [lag]
```

**Resultatet står først, kilden etterpå.** Det er lett å snu om på, og da overskriver du kildefilen.

Kjør alt fra mappen `ogr2ogr-demo`. Dataene lastes ned med `./last-ned-data.sh`.

---

## 0. Se hva som finnes: `ogrinfo`

```bash
ogrinfo -so -al data/kommuner.gpkg
```

Viser antall objekter, geometritype, koordinatsystem og kolonner. Gjør dette før du gjør noe annet.

For å ha en GeoPackage med flere lag til punkt 3, lager vi en:

```bash
mkdir -p ut
ogr2ogr -f GPKG ut/eksempel.gpkg data/kommuner.gpkg kommuner
ogr2ogr -update ut/eksempel.gpkg /vsizip/data/ne_land.zip -nln land -nlt PROMOTE_TO_MULTI -select NAME,CONTINENT,POP_EST
ogrinfo ut/eksempel.gpkg
```

Svaret viser to lag: `kommuner` og `land`.

---

## 1. Konvertere filformat

Formatet gjettes fra filendelsen.

```bash
ogr2ogr ut/kommuner.geojson data/kommuner.gpkg
ogr2ogr ut/kommuner.fgb     data/kommuner.gpkg
ogr2ogr ut/kommuner.shp     data/kommuner.gpkg
```

Vil du bestemme formatet selv, bruker du `-f`:

```bash
ogr2ogr -f GeoJSON ut/kommuner.json data/kommuner.gpkg
```

Se alle formater med `ogr2ogr --formats`.

---

## 2. Reprojisere

`-t_srs` («target SRS») velger koordinatsystemet i resultatet.

```bash
# Fra grader (EPSG:4258) til meter (UTM sone 32, EPSG:25832)
ogr2ogr -t_srs EPSG:25832 ut/kommuner_utm32.gpkg data/kommuner.gpkg

# Sjekk utstrekningen før og etter
ogrinfo -so -al data/kommuner.gpkg       | grep Extent
ogrinfo -so -al ut/kommuner_utm32.gpkg   | grep Extent
```

Før står tallene som grader (4 til 31, 57 til 71), etterpå som meter (234 758 til 1 339 069).

Nettkart (MapLibre, Leaflet) vil ha GeoJSON i EPSG:4326:

```bash
ogr2ogr -t_srs EPSG:4326 ut/kommuner_4326.geojson data/kommuner.gpkg
```

---

## 3. Velge ett lag fra en GeoPackage og lage GeoJSON

En GeoPackage kan inneholde mange lag. Skriver du lagnavnet etter kilden, er det bare det laget som konverteres.

```bash
# Uten lagnavn: alle lag blir med (bra for GPKG til GPKG, upraktisk for GeoJSON)
# Med lagnavn: bare ett lag
ogr2ogr ut/land.geojson ut/eksempel.gpkg land
```

Du får `land.geojson` med 177 land, uten kommunene.

---

## 4. Filtrere med `-where`

`-where` tar et SQL-uttrykk, som i en vanlig `WHERE`-setning.

```bash
# Tekst: bruk enkeltfnutter inni dobbeltfnuttene
ogr2ogr ut/kristiansand.geojson ut/eksempel.gpkg kommuner -where "kommunenavn = 'Kristiansand'"

# Tall
ogr2ogr ut/store_land.geojson ut/eksempel.gpkg land -where "POP_EST > 100000000"

# Flere vilkår
ogr2ogr ut/europa.geojson ut/eksempel.gpkg land -where "CONTINENT = 'Europe' AND POP_EST > 10000000"

# Agder: kommunenummer fra 4200 til 4299 (25 kommuner)
ogr2ogr ut/agder.geojson ut/eksempel.gpkg kommuner -where "kommunenummer >= 4200 AND kommunenummer < 4300"

# Tell treffene
ogrinfo -so -al ut/europa.geojson | grep "Feature Count"
```

---

## Alt i ett

Én kommando som velger lag, filtrerer, reprojiserer og konverterer:

```bash
ogr2ogr -f GeoJSON ut/kristiansand_4326.geojson ut/eksempel.gpkg kommuner \
  -where "kommunenavn = 'Kristiansand'" -t_srs EPSG:4326
```

Dra resultatfilen inn i QGIS eller [geojson.io](https://geojson.io) for å se det.

## Tre ting å huske

1. Resultatet først, kilden etterpå.
2. Kjør `ogrinfo -so -al` for å se lag, kolonner og koordinatsystem.
3. Valgene kan kombineres fritt i samme kommando.
