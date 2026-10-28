@@ intro
Programvare for geografisk databehandling er lettest å forstå ut fra *rollen* den spiller: et program du jobber i selv (desktop-GIS), en plattform i nettleseren der du lager og deler kart, eller en server som publiserer data til andre systemer. Tabellene under gir deg en rask oversikt med hovedbruk og typiske oppgaver. Lagring og kode har egne temasider.

@@ innhold
#### Desktop-GIS

| Programvare | Lisens | Hovedbruk | Typisk oppgave |
|---|---|---|---|
| **[QGIS](https://qgis.org/)** | Åpen kildekode (GPL) | Fullverdig GIS for visning, redigering, analyse og kartproduksjon. Utvides med plugins og Python. | Utforske data, kjøre analyser og lage kart. Dette er kursets standardverktøy. |
| **[ArcGIS Pro](https://www.esri.com/en-us/arcgis/products/arcgis-pro/overview)** | Kommersiell (Esri) | Desktop-GIS i Esri-økosystemet, tett koblet til ArcGIS Online og ArcGIS Enterprise. | Analyse og forvaltning i organisasjoner som bruker Esri. I Norge selges og støttes Esri-produktene av [Geodata AS](https://www.geodata.no/). |

#### Web-GIS og kartplattformer

| Programvare | Lisens | Hovedbruk | Typisk oppgave |
|---|---|---|---|
| **[GeoLibre](https://geolibre.app/)** | Åpen kildekode | Nytt nettleserbasert GIS, utviklet av en professor i USA. Leser blant annet skybaserte formater og kjører spatial SQL i nettleseren. | Prøve GIS-analyse uten installasjon. Se [tutorials](https://geolibre.app/tutorials/) om bl.a. Spatial SQL, Cloud-Native Data og Vector Analysis. |
| **[ArcGIS Online](https://www.arcgis.com/)** | Kommersiell (Esri) | Skybasert plattform for kart, apper og dashboards. | Publisere kart og dashboards i en organisasjon uten egen serverdrift. |
| **[Felt](https://felt.com/)** | Kommersiell, med gratisnivå | Samarbeidskart i nettleseren. | Dele, tegne på og kommentere kart sammen med kolleger og kunder. |
| **[Mapbox](https://www.mapbox.com/)** | Kommersiell, med gratisnivå | Plattform for utviklere: kartfliser, stiler, søk og ruting. | Egne kartapper med profesjonell kartstil. |
| **[CARTO](https://carto.com/)** | Kommersiell | Analyse og visualisering oppå skydatabaser (blant annet BigQuery, Snowflake og Databricks). | Romlig analyse og dashboards på store datamengder. |
| **[Kepler.gl](https://kepler.gl/)** | Åpen kildekode (MIT) | Utforsking av store punkt- og bevegelsesdata i nettleseren. | Raskt se mønstre i store datasett. |

#### Kartservere og tjenester

Her publiserer du data slik at andre systemer kan bruke dem, gjerne via standardene fra [API-standarder](side:api-standarder).

| Programvare | Lisens | Hovedbruk | Typisk oppgave |
|---|---|---|---|
| **[GeoServer](https://geoserver.org/)** | Åpen kildekode (GPL) | Java-basert kartserver med webgrensesnitt. WMS, WFS, WCS og WMTS fra filer og databaser. | Publisere data fra PostGIS som standardtjenester. |
| **[MapServer](https://mapserver.org/)** | Åpen kildekode (MIT-stil) | Rask kartserver (C) som konfigureres med en tekstfil. WMS og WFS. | Enkle og effektive kartjenester. |
| **[QGIS Server](https://docs.qgis.org/latest/en/docs/server_manual/)** | Åpen kildekode (GPL) | Publiserer et QGIS-prosjekt som WMS, WFS og OGC API med samme symbolikk. | Dele et ferdig stilt kart fra et QGIS-prosjekt. |
| **[MapProxy](https://mapproxy.org/)** | Åpen kildekode (Apache) | Mellomlager (cache) og proxy foran andre kartjenester. | Gjøre en treg WMS rask ved å servere den som flis-tjeneste (WMTS). |
| **[pygeoapi](https://pygeoapi.io/)** | Åpen kildekode (MIT) | Python-server for OGC API (Features, Tiles, Records, Processes). | Lettvekts-API over filer og databaser. |
| **[pg_featureserv](https://github.com/CrunchyData/pg_featureserv)** og **[pg_tileserv](https://github.com/CrunchyData/pg_tileserv)** | Åpen kildekode (Apache) | Lette servere som gjør PostGIS-tabeller om til OGC API Features og vektorfliser. | Raskeste vei fra PostGIS-tabell til web-API. |
| **[Martin](https://maplibre.org/martin/)** | Åpen kildekode (Apache) | Rask server for vektorfliser fra PostGIS, PMTiles og MBTiles. | Vektorfliser til MapLibre-kart. |
| **[TiTiler](https://developmentseed.org/titiler/)** | Åpen kildekode (MIT) | Lager rasterfliser ved behov fra Cloud Optimized GeoTIFF (COG). | Vise satellittbilder og høydemodeller fra skylagring. |
| **[ArcGIS Enterprise](https://www.esri.com/en-us/arcgis/products/arcgis-enterprise/overview)** | Kommersiell (Esri) | Esris serverplattform for egen drift. | Organisasjoner som bruker ArcGIS Pro og vil drifte selv. |

#### Slik velger du

- **Åpen kildekode er ikke det samme som gratis drift.** Du sparer lisens, men betaler med tid til installasjon, oppdatering og sikkerhet.
- **Kommersielle plattformer** gir mindre drift og støtte, men binder deg til en leverandør. Sjekk prisnivå og hvilke formater du kan ta med deg ut igjen.
- **Mange norske virksomheter har allerede en plattform** fra leverandører som Geodata AS (Esri) eller [Norkart](https://www.norkart.no/). Start med å undersøke hva dere har, før dere velger nytt.

Sist kontrollert oktober 2026. Priser, gratisnivåer og funksjoner endres, så sjekk leverandørens egne sider.

@@ aktivitet
- Åpne GeoLibre-tutorialen [«Your First Map»](https://geolibre.app/tutorials/first-map/) og lag et enkelt kart. Hva er likt og hva er annerledes enn i QGIS?
- Legg til Kartverkets kartfliser i QGIS: *Layer → Add Layer → Add WMS/WMTS Layer*, ny tilkobling med adressen `https://cache.kartverket.no/v1/wmts/1.0.0/WMTSCapabilities.xml`. Hvilke kartlag tilbyr de?
- Velg en kartserver fra tabellen. Hvilke standarder støtter den, og ville den passet for å publisere en PostGIS-tabell til en nettside?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [QGIS: User Guide](https://docs.qgis.org/latest/en/docs/user_manual/index.html)
- [GeoLibre: Tutorials](https://geolibre.app/tutorials/)

@@ interessert
- [OSGeo: Software projects](https://www.osgeo.org/projects/)
- [GeoServer: dokumentasjon](https://docs.geoserver.org/)
- [QGIS Server: manual](https://docs.qgis.org/latest/en/docs/server_manual/)
- [pygeoapi: dokumentasjon](https://docs.pygeoapi.io/)
