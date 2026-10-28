@@ intro
Geografisk databehandling kan gjøres i hundrevis av verktøy, men nesten alle hører til fem kategorier. Å kjenne kategoriene er viktigere enn å kunne produktene: produktene skifter, men kategorien avgjør hva du kan automatisere, dele og skalere. Denne siden gir deg kartet over landskapet. De neste temasidene går inn i hver kategori.

@@ innhold
#### Fem kategorier

| Kategori | Hva er det? | Eksempler | Typisk bruk | Mer info |
|---|---|---|---|---|
| **Desktop-GIS** | Program du installerer og arbeider interaktivt i. | QGIS, ArcGIS Pro | Utforske, redigere og analysere data, lage kart. | [Desktop, web og server](side:desktop-web-og-serverprogramvare) |
| **Web-GIS og plattformer** | Tjenester i nettleseren der du laster opp data, analyserer og deler kart. | ArcGIS Online, Felt, Mapbox, GeoLibre | Dele kart med andre uten å drifte noe selv. | [Desktop, web og server](side:desktop-web-og-serverprogramvare) |
| **Kartservere** | Programvare som publiserer data som tjenester (WMS, WFS, OGC API, kartfliser). | GeoServer, MapServer, pygeoapi | Gjøre data tilgjengelig for andre systemer og apper. | [Desktop, web og server](side:desktop-web-og-serverprogramvare) |
| **Databaser** | Lagrer data og lar deg analysere dem med SQL. | PostGIS, DuckDB, SQL Server, BigQuery | Store datamengder, gjentatte analyser, mange brukere. | [Databaser og lagring](side:databaser-og-lagring) |
| **Kommandolinje og biblioteker** | Verktøy og kode som kan kjøres på nytt, automatiseres og settes sammen. | GDAL/ogr2ogr, geopandas, MapLibre | Konvertering, automatisering, egne analyser og kartapper. | [CLI og biblioteker](side:cli-og-biblioteker) |

Kategoriene overlapper. QGIS er et desktop-GIS, men kan også publisere tjenester (QGIS Server) og kjøre Python. Poenget er hvilken rolle verktøyet spiller i oppgaven din. Lagringsformatene (GeoPackage, GeoParquet og andre) og API-standardene (WMS, WFS, OGC API) fra [Lagringsformater](side:lagringsformater) og [API-standarder](side:api-standarder) er det som binder kategoriene sammen.

#### Velg kategori ut fra oppgaven

| Jeg vil … | Start med | Fordi |
|---|---|---|
| se på og forstå et nytt datasett | Desktop-GIS | Raskt og visuelt, uten kode. |
| lage et kart jeg kan dele med kolleger eller publikum | Web-GIS-plattform | Ingen drift. Du deler en lenke. |
| gjøre data tilgjengelig som tjeneste for andre systemer | Kartserver | Standardiserte grensesnitt som WMS, WFS og OGC API. |
| kjøre samme analyse på millioner av objekter, eller gjenta den hver uke | Database (SQL) | Skalerer godt, og spørringen dokumenterer analysen. |
| konvertere mange filer eller kjøre en jobb automatisk | Kommandolinje (GDAL) | Én kommando kan gjentas og skriptes. |
| lage min egen kartapp | JavaScript-bibliotek (MapLibre) | Full kontroll over utseende og funksjon. |
| analysere stedfestede data sammen med tabeller og statistikk | Python (geopandas, DuckDB) | Geodata kombineres med resten av dataanalysen. |

#### Tre spørsmål som snevrer inn valget

1. **Hvor store er dataene?** Tusenvis av objekter går i nesten alt. Millioner av objekter peker mot database eller kolonnebaserte formater som GeoParquet.
2. **Hvor ofte skal det gjøres?** En gang kan løses med noen klikk i et GIS. Gjentas det, bør det skriptes eller skrives som SQL.
3. **Hvem skal bruke resultatet?** Bare deg selv, kolleger eller et bredt publikum? Det avgjør om du trenger en delt database, en plattform eller en egen kartapp.

Velg som regel det enkleste verktøyet som løser oppgaven. En KI-agent kan skrive koden for deg, men du må fortsatt vite hvilken type verktøy den bør bruke. Det kommer vi tilbake til i siste tema.

@@ aktivitet
- Velg tre oppgaver fra din egen jobb, for eksempel «vise kunder på kart» eller «oppdatere en kartlagsliste hver måned». Plasser dem i en av de fem kategoriene og begrunn valget.
- Finn ett verktøy du bruker i dag. Hvilken kategori hører det til, og hva ville vært et alternativ i en annen kategori?
- Hva er det enkleste verktøyet som kunne løst en av oppgavene dine? Hva ville fått deg til å velge noe tyngre?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [OSGeo: Software projects](https://www.osgeo.org/projects/) (oversikt over åpen kildekode-prosjekter innen geografisk IT)

@@ interessert
- [Awesome Geospatial](https://github.com/sacridini/Awesome-Geospatial) (kuratert liste over verktøy og biblioteker)
- [Cloud-Native Geospatial Foundation: guide](https://guide.cloudnativegeo.org/)
