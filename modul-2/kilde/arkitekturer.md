@@ intro
Arkitektur handler om hvordan data, server og klient settes sammen. Samme kart kan bygges på mange måter, med store forskjeller i kostnad, drift, sikkerhet og fleksibilitet. Her er fire vanlige mønstre, bygget av verktøyene fra de foregående temaene. Hovedregelen er å velge det enkleste mønsteret som løser oppgaven.

@@ innhold
#### Fire mønstre i oversikt

| Mønster | Slik ser det ut | Passer når | Passer ikke når | Eksempel |
|---|---|---|---|---|
| **1. Frontend-only** | Nettleser → andres tjenester eller egne statiske filer | Åpne data, prototyper og enkel publisering uten drift. | Du trenger å skrive data, holde noe hemmelig eller styre tilgang. | [Frontend-only kartapp](https://alexanno.github.io/is930-demoer/Frontend-only%20kartapp/index.html) |
| **2. Frontend + backend-API (+ PostGIS)** | Nettleser → API → database | Data som endres, spørringer mot egen database, og når nøkler og passord må skjules. | Statiske filer holder. | [postgis-sql-api](https://github.com/alexanno/postgis-sql-api) |
| **3. 3-lags med kartserver** | Klient → kartserver → database eller filer | Mange ulike klienter skal bruke de samme dataene via standardtjenester (WMS, WFS, OGC API). | Du lager en liten app for noen få brukere. | Kartverkets og Geonorges tjenester, GeoServer + PostGIS |
| **4. Caching og tile-pyramider** | Forhåndslagde fliser, med cache eller CDN foran | Mange brukere og tunge kart der dataene sjelden endres. | Dataene endres hele tiden eller hver bruker spør om noe unikt. | Kartverkets kartfliser, PMTiles |

#### 1. Frontend-only

{{flow: Nettleser // HTML og JavaScript | Andres tjenester // Kartverket, Geonorge, OpenStreetMap ~ Figur: Variant a: appen bruker andres tjenester}}

{{flow: Nettleser // HTML og JavaScript | Egne filer på statisk lagring // PMTiles, COG, GeoParquet ~ Figur: Variant b: cloud native, egne filer leses direkte}}

Appen har ingen egen server. I **variant a** er backend «andres problem»: nettleseren spør tjenester som Kartverket, Geonorge og OpenStreetMap, som selv har kartserver og database bak seg. Appen din er altså en klient i andres 3-lags arkitektur. Demoappen viser hvor mye du får til med én HTML-fil: bakgrunnskart som kartfliser, et WMS-lag, og oppslag på stedsnavn, kommune og høyde. **Variant b** er cloud native: du legger egne filer (PMTiles, COG eller GeoParquet) på statisk lagring og leser dem direkte, slik beskrevet i [Databaser og lagring](side:databaser-og-lagring).

Pris du betaler: alt er offentlig, så nøkler i koden kan leses av alle. I variant a er du avhengig av at andre holder tjenestene oppe og beholder vilkårene sine. Bruk for eksempel [OpenStreetMaps flisregler](https://operations.osmfoundation.org/policies/tiles/) og lisensen til hvert lag.

#### 2. Frontend + backend-API + PostGIS

{{flow: Nettleser | API // Node, Python eller edge function | PostGIS // database med geodata ~ Figur: backend mellom nettleser og database}}

Når dataene ligger i en database, må noe stå imellom: et API som tar imot forespørsler, spør PostGIS og returnerer for eksempel GeoJSON. Nettleseren får aldri databasepassordet. [postgis-sql-api](https://github.com/alexanno/postgis-sql-api) er et lite eksempel på dette, og [Supabase-oppgaven fra IS-218](https://github.com/alexanno/GeografiskAI_UiA_IS-218/blob/main/V2025/07-Geografisk%20IT-utvikling/supabase_tutorial.md) viser det samme som en «edge function».

```text
GET /api/sqlapi?sql=select navn from skole order by geom <-> 'SRID=4326;POINT(8.0 58.15)' limit 3
```

Dette eksempelet sender fri SQL fra nettleseren og er kun egnet i undervisning, med en databasebruker som bare kan lese. I virkelige løsninger lager du faste endepunkter, for eksempel `/skoler?kommune=4204`, eller bruker ferdige verktøy som [pg_featureserv](https://github.com/CrunchyData/pg_featureserv) eller Supabase.

#### 3. 3-lags med kartserver

{{flow: Klient // nettleser, QGIS, andre systemer | Kartserver // GeoServer, MapServer, pygeoapi | Database eller filer // PostGIS, GeoPackage ~ Figur: presentasjon, logikk og data i hver sin del}}

Klient, tjeneste og data er hvert sitt lag. Ved å publisere data som standardtjenester (WMS, WFS, OGC API, se [API-standarder](side:api-standarder)) kan mange ulike klienter bruke samme tjeneste: nettleseren, QGIS og andre systemer. Slik er de nasjonale tjenestene på Geonorge bygget. Kostnaden er at du selv må drifte, oppdatere og sikre serveren. Programvaren står i [Desktop, web og serverprogramvare](side:desktop-web-og-serverprogramvare).

#### 4. Caching og tile-pyramider

{{flow: Nettleser | Cache eller CDN // MapProxy, nettleser-cache | Kartserver eller fliser ~ Figur: cache foran tjenesten}}

Ved å lage ferdige fliser for alle zoomnivåer (en *pyramide*) og legge dem i en cache eller et CDN slipper serveren å tegne kartet på nytt for hver bruker. Resultatet er raskt og billig, men fungerer best når dataene sjelden endres. PMTiles er en hel flispyramide i én fil. Oppdateringer betyr at fliser må lages om og cachen tømmes. Dette mønsteret legges som regel til oppå mønster 2 eller 3.

#### Velg arkitektur

| Spørsmål | Peker mot |
|---|---|
| Er dataene åpne, og endres de sjelden? | Frontend-only (eventuelt cloud native) |
| Må noen kunne endre data, eller må noe holdes hemmelig? | Frontend + backend-API |
| Skal mange ulike systemer bruke tjenesten din? | 3-lags med standardtjenester |
| Mange brukere eller tunge kart? | Legg til caching |

Mønstrene kan kombineres, for eksempel frontend + API + PostGIS bak, med cache foran.

@@ aktivitet
- Åpne [demoappen](https://alexanno.github.io/is930-demoer/Frontend-only%20kartapp/index.html), bytt bakgrunn, slå på naturvern og klikk i kartet. Åpne nettleserens utviklerverktøy (fanen *Network*). Hvor mange ulike tjenester snakker appen med, og hvem drifter dem?
- Hva skjer med en frontend-only-app hvis en av tjenestene den bruker går ned eller endrer vilkår? Hva kan du gjøre for å redusere risikoen?
- Tegn arkitekturen for en case fra din virksomhet, for eksempel «kunder på kart». Hvilket mønster velger du, og hvorfor ikke de andre?
- Be en KI-agent legge et nytt WMS-lag fra [Geonorge kartkatalog](https://kartkatalog.geonorge.no/) til demoappen. Hva måtte endres?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [MapLibre: Add a WMS source](https://maplibre.org/maplibre-gl-js/docs/examples/add-a-wms-source/)
- [Cloud-Native Geospatial: guide](https://guide.cloudnativegeo.org/)

@@ interessert
- [postgis-sql-api (GitHub)](https://github.com/alexanno/postgis-sql-api)
- [supabase_geojson_sqlapi (GitHub)](https://github.com/alexanno/supabase_geojson_sqlapi)
- [Kartverkets kartfliser: WMTS GetCapabilities](https://cache.kartverket.no/v1/wmts/1.0.0/WMTSCapabilities.xml)
- [PMTiles: dokumentasjon](https://docs.protomaps.com/pmtiles/)
