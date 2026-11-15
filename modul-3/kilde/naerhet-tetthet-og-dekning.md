@@ intro
Tre analysetyper svarer på de fleste «hvor»-spørsmål: Hvor langt er det til nærmeste? Hvor er det mest av noe? Hvor mange nås av en tjeneste? Analysene er enkle å kjøre, særlig med en agent, men svaret avhenger av valg som ofte tas uten at noen merker det.

@@ innhold
#### Nærhet

Nærhet handler om avstand til nærmeste, eller om noe ligger innenfor en terskel. Avstanden kan være luftlinje, avstand langs vegnett eller reisetid, og forskjellen kan være stor i en fjordkommune. Operasjonene er beskrevet i [Geografiske operasjoner](side:geografiske-operasjoner) i modul 2.

- `sjoin_nearest` i geopandas
- `ST_DWithin` og `<->` i PostGIS og DuckDB
- osmnx og r5py for vegnett og reisetid

#### Tetthet og klynger

Tetthet viser hvor det er mest av noe. Klynger viser hvor ting ligger i grupper.

- **Tetthet** kan telles per sone (grunnkrets, kommune), per rute (SSB 250 m), per heksagon (H3) eller glattes med kernel density estimation (KDE), der du velger *bandwidth*.
- **Klynger** med DBSCAN finner grupper av punkter uten at du må velge soner eller ruter. Du må velge `eps` (maks avstand mellom naboer) og minste antall punkter.
- **Klyngeanalyse generelt** er en familie av metoder som grupperer objekter etter likhet eller nærhet. DBSCAN grupperer etter tetthet, finner klynger i vilkårlig form og markerer enkeltpunkter som støy. K-means krever at du velger antall klynger på forhånd. Les mer: [Wikipedia om DBSCAN](https://en.wikipedia.org/wiki/DBSCAN), [ArcGIS Pro: Density-based Clustering](https://pro.arcgis.com/en/pro-app/latest/tool-reference/spatial-statistics/densitybasedclustering.htm) og [scikit-learn: Clustering](https://scikit-learn.org/stable/modules/clustering.html).
- Samme data gir ulike kart med ulik cellestørrelse, bandwidth eller `eps`. Metoden og parameterne må følge med kartet.
- **Normaliser.** Vis antall per areal eller per innbygger, aldri bare antall.

#### Dekning

Dekning handler om hvor stor andel av befolkningen eller arealet som nås av en tjeneste.

- Serviceområder og isokroner (område som nås på en gitt kjøretid) kombineres med befolkning på rutenett.
- Terskelen du velger (5, 10 eller 15 minutter) avgjør svaret.
- Lokaliseringsanalyse går ett steg videre: hvor bør neste enhet ligge for å øke dekningen mest?

#### Valgene som styrer svaret

Disse valgene gjelder for alle tre analysetypene:

- **Avstandsmål:** luftlinje, veg eller reisetid
- **Terskel:** 5 km eller 10 km, 10 minutter eller 20 minutter
- **Aggregeringsenhet:** sone, rute, heksagon eller kontinuerlig flate
- **Hvem som telles:** befolkning på bosted teller ikke hytteturister og pendlere
- **Datakildens dekning:** OpenStreetMap er tettere i by enn i distrikt

#### Casestudier

| Case | Sektor | Analysetype | Data |
|---|---|---|---|
| Responstid for brann og redning | Forvaltning | Nærhet og dekning | Brannstasjoner, vegnett, befolkning på rutenett |
| Skolevei og skyss | Kommune | Nærhet (nettverk) | Skoler, adresser, vegnett (NVDB) |
| Legevakt og fastlege i distriktet | Helse | Dekning | Helseinstitusjoner, SSB rutenett |
| Ny butikk eller ladestasjon | Næringsliv | Tetthet og dekning | Befolkning, konkurrenter (OSM), trafikk (NVDB) |
| Mobil- og bredbåndsdekning | Næringsliv og Nkom | Dekning | Nkom dekningskart, befolkning |
| Hytter og fritidsboliger | Plan | Tetthet og klynger | Matrikkelen (bygningstype), kommuneplan |

For hvert case: hvilket spørsmål stilles, hvilke valg ligger bak, og hvordan kan svaret misforstås eller misbrukes?

@@ aktivitet
- Hvor stor andel av boligbyggene i Agder tror du ligger mer enn 5 km fra nærmeste brannstasjon? Skriv ned et anslag, og la en agent beregne det. Hvor nær var du?
- Lag et kart over restauranter i en by du kjenner med to ulike cellestørrelser (H3) og med DBSCAN med to verdier av `eps`. Peker metodene på de samme områdene?
- Beregn andel av innbyggerne som bor innenfor 10 km luftlinje fra en brannstasjon, og sammenlign med 15 minutters kjøring. Hvor mye endret svaret seg?
- Hvilke analyser i din virksomhet er egentlig nærhet, tetthet eller dekning?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [SSB: Befolkning på rutenett](https://www.ssb.no/en/natur-og-miljo/geodata/statistikk/befolkning-pa-rutenett)
- [DSB: dimensjoneringsforskriften](https://www.dsb.no/lover/brannvern-ulykker-og-redning/)

@@ interessert
- [osmnx](https://osmnx.readthedocs.io/) og [r5py](https://r5py.readthedocs.io/) for vegnett og reisetid
- [H3](https://h3geo.org/docs) for heksagonrutenett
- [DBSCAN i scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html)
