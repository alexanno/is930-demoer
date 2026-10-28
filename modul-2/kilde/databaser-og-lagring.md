@@ intro
SQL er et av de kraftigste verktøyene i geografisk analyse: du beskriver hva du vil ha, og databasen finner raskeste måte å regne det ut på, også for millioner av objekter. Her ser du hvorfor spatial SQL er verdt å lære, hvilke databaser som finnes, hvordan data kan lagres, og hvordan cloud native-formater kan brukes som en skrivebeskyttet «database».

@@ innhold
#### Hvorfor spatial SQL?

- **Deklarativt:** du sier hva du vil ha, ikke hvordan du får det. Spørringen er samtidig dokumentasjonen av analysen.
- **Skalerer:** databasen bruker romlig indeks og spørreoptimalisering, så «hva ligger her?» slipper å sjekke alle objekter.
- **Overførbart:** `ST_`-funksjonene bygger på standarden OGC Simple Features og er nesten like i PostGIS, DuckDB, BigQuery, Databricks og SQL Server. KI-agenter er også gode på SQL, noe vi kommer tilbake til i siste tema.

```sql
-- PostGIS: bygg innen 100 m fra vassdrag
SELECT b.* FROM bygg b JOIN vassdrag v ON ST_DWithin(b.geom, v.geom, 100);

-- PostGIS: nærmeste brannstasjon til et punkt (<-> bruker den romlige indeksen)
SELECT navn FROM brannstasjon ORDER BY geom <-> ST_SetSRID(ST_MakePoint(88423, 6466808), 25833) LIMIT 1;

-- Antall bygg per kommune
SELECT k.kommunenavn, count(*) FROM bygg b JOIN kommuner k ON ST_Within(b.geom, k.geom) GROUP BY k.kommunenavn;
```

Flere eksempler står i [Geografiske operasjoner](side:geografiske-operasjoner). Vil du øve, er [PostGIS-introduksjonen](https://postgis.net/workshops/postgis-intro/) et godt sted å begynne.

#### Databaser med geografisk støtte

| Database | Type | Skalerer til | Lisens | Bruk når |
|---|---|---|---|---|
| **[PostgreSQL + PostGIS](https://postgis.net/)** | Databaseserver | Store datamengder og mange samtidige brukere | Åpen kildekode | Standardvalget for delte geodatabaser med flere brukere og oppdateringer. |
| **[DuckDB](https://duckdb.org/docs/stable/core_extensions/spatial/overview.html) (spatial)** | Innebygd, kjører i prosessen din. Ingen server. | Millioner til milliarder rader på én maskin | Åpen kildekode (MIT) | Rask analyse direkte på GeoParquet- og GeoPackage-filer, lokalt eller mot skylagring. |
| **[SQLite/SpatiaLite + GeoPackage](https://www.geopackage.org/)** | Innebygd fildatabase | Opptil noen gigabyte | Åpen kildekode | Én fil å dele, til feltarbeid og mindre prosjekter. |
| **[SQL Server (spatial)](https://learn.microsoft.com/en-us/sql/relational-databases/spatial/spatial-data-sql-server)** | Databaseserver (Microsoft) | Store datamengder | Kommersiell | Organisasjoner som allerede har Microsoft-plattformen. |
| **[BigQuery GIS](https://cloud.google.com/bigquery/docs/geospatial-intro)** | Skybasert datavarehus (Google) | Svært store datamengder | Betaling per spørring | Analyse av store datasett uten å drifte en server. |
| **[Databricks](https://docs.databricks.com/aws/en/sql/language-manual/sql-ref-st-geospatial-functions.html)** | Skybasert dataplattform | Svært store datamengder | Kommersiell | Virksomheter som har Databricks som felles dataplattform. Støtter geometrityper og `ST_`-funksjoner. |
| **[Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/real-time-intelligence/map/about-fabric-maps)** | Skybasert dataplattform (Microsoft) | Svært store datamengder | Kommersiell | Virksomheter som bruker Microsoft og Azure. Geografiske funksjoner og kartvisning (Maps in Fabric). |

Databricks og Fabric brukes av mange norske virksomheter som felles dataplattform, og geodata er der et tillegg. Sjekk hvilke romlige funksjoner plattformen har før dere planlegger analysene dit. Se også tabellen over verktøykategorier i [Verktøylandskapet](side:verktoylandskapet).

#### Lagringsstrukturer: fil, database eller objektlagring?

| Struktur | Eksempler | Egenskaper | Passer når | Vær oppmerksom på |
|---|---|---|---|---|
| **Fil** | GeoPackage, GeoParquet, Shapefile | Enkel å dele og kopiere. Ingen server. | Dele, arkivere og analysere på én maskin. | Vanskelig med flere som skriver samtidig. Tilgang styres bare med filrettigheter. |
| **Database** | PostGIS, SQL Server | Flere brukere samtidig, transaksjoner, tilgangsstyring og romlig indeks. | Data som endres og brukes av mange. | Må driftes, sikres og sikkerhetskopieres. |
| **Objektlagring i sky** | S3, Azure Blob og Google Cloud Storage med COG, GeoParquet eller PMTiles | Billig og svært skalerbar. Leses via HTTP. | Store datasett som sjelden endres og deles bredt. | Ingen transaksjoner. Tilgang styres per fil eller URL. |

To begreper forklarer mye av ytelsen. En **romlig indeks** (for eksempel R-tre eller GiST) gjør at databasen raskt finner objekter i et område uten å lese alt. **Kolonnebasert lagring** (som i Parquet) leser bare kolonnene du spør etter, som gir rask analyse av brede tabeller. Formatene er beskrevet i [Lagringsformater](side:lagringsformater).

#### Cloud native som skrivebeskyttet «database»

Cloud native-formater er laget slik at klienten kan hente bare delene av en fil den trenger, med HTTP range requests. En fil på objektlagring oppfører seg da som en skrivebeskyttet database: du spør, og får tilbake bare det du trenger, uten at noen server kjører.

```sql
-- DuckDB leser en GeoParquet-fil direkte fra web. Ingen nedlasting, ingen server.
INSTALL httpfs; LOAD httpfs;
SELECT name, ST_Area(geometry) AS areal
FROM read_parquet('https://raw.githubusercontent.com/opengeospatial/geoparquet/main/examples/example.parquet')
ORDER BY areal DESC;
```

| Format | Leser bare … | Typisk «spørring» |
|---|---|---|
| **COG** (raster) | …utsnittet og oppløsningen du ber om | Vis et satellittbilde i nettleseren. |
| **PMTiles** (vektorfliser) | …flisene som vises i kartvinduet | Vis store kartdatasett fra statisk hosting. |
| **FlatGeobuf** (vektor) | …objektene innenfor et utsnitt | Hent bygg i et område. |
| **GeoParquet** (vektor) | …kolonnene og radgruppene spørringen trenger | Tell, summer og filtrer store datasett med DuckDB. |

Begrensninger du må kjenne til: det går ikke an å skrive eller oppdatere, det finnes ingen transaksjoner, og tilgangsstyring skjer per fil eller URL (for eksempel med tidsbegrensede, signerte lenker). Ytelsen avhenger også av hvordan filen er bygget opp. [Overture Maps](https://docs.overturemaps.org/getting-data/duckdb/) viser hvordan du spør hele verdens bygg- og stedsdata med DuckDB. Mer finner du i [Cloud-Native Geospatial: guide](https://guide.cloudnativegeo.org/).

@@ aktivitet
- Kjør DuckDB-spørringen over (`uv run --with duckdb python`, se CLI og biblioteker). Endre den til å velge kontinent eller land du er interessert i. Hva leste DuckDB egentlig fra nettet?
- Åpne [GeoLibre-tutorialen om Spatial SQL](https://geolibre.app/tutorials/spatial-sql/) og kjør en spørring. Hva er likt og ulikt PostGIS-eksemplene?
- Velg tre datasett fra din virksomhet. Ville du lagret dem som fil, i database eller på objektlagring? Begrunn.

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [Cloud-Native Geospatial: guide](https://guide.cloudnativegeo.org/)
- [PostGIS: Introduction (workshop)](https://postgis.net/workshops/postgis-intro/)

@@ interessert
- [DuckDB: spatial extension](https://duckdb.org/docs/stable/core_extensions/spatial/overview.html)
- [Overture Maps: hente data med DuckDB](https://docs.overturemaps.org/getting-data/duckdb/)
- [GeoParquet-spesifikasjonen](https://geoparquet.org/)
- [PostGIS: dokumentasjon](https://postgis.net/documentation/)
