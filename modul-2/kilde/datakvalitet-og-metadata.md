@@ intro
Et datasett som ser riktig ut på kartet kan likevel være gammelt, unøyaktig, ufullstendig eller ha en lisens du ikke har lov til å bruke. *Metadata*, altså data om dataene, forteller deg dette, og kvalitetselementene gir deg språk for å vurdere det. Her er sjekklisten du bør gå gjennom før du tar et datasett i bruk. Det er også stegene som oftest hoppes over, både av mennesker og KI-agenter.

@@ innhold
#### Sjekkliste før du tar i bruk et datasett

Eksempelkolonnen bruker metadataene til [FKB-Bygning i Geonorge kartkatalog](https://kartkatalog.geonorge.no/metadata/fkb-bygning/8b4304ea-4fb0-479c-a24d-fa225e2c6e97) (lest oktober 2026).

| Spørsmål | Hva du ser etter | Eksempel: FKB-Bygning |
|---|---|---|
| **Hva er det?** | Innhold, objekttyper, formål og avgrensninger. Står i produktspesifikasjonen. | Bygningsdata i Felles kartdatabase (FKB), med lenke til produktspesifikasjon. |
| **Hvem eier det, og hva får jeg bruke det til?** | Eier, lisens og tilgangsrestriksjoner. | Tilgangsrestriksjonen er «Norge digitalt begrenset». Det er altså ikke åpne data, selv om en WMS-tjeneste finnes. |
| **Hvor ferskt er det?** | Oppdateringsfrekvens og dato for siste oppdatering. | Oppdatert kontinuerlig. Sjekk også siste oppdateringsdato. |
| **Hvor nøyaktig er det?** | Datakilde, målemetode, detaljnivå og posisjonsnøyaktighet. | Hovedsakelig fotogrammetri fra flybilder. Detaljnivået varierer mellom FKB-A (mest detaljert) og FKB-D. |
| **Er det komplett?** | Geografisk dekning og kjente hull. | Metadata har lenke til dekningskart. Data leveres fylkesvis, kommunevis eller for hele landet. |
| **Hvilket koordinatsystem?** | Horisontalt og vertikalt referansesystem. | EUREF89 UTM sone 32 med høyder i NN2000. |
| **Henger dataene sammen?** | Gyldige geometrier, kodelister og manglende verdier. Dette sjekker du selv, se under. | Ikke i metadata. Må testes. |

#### Fem kvalitetselementer og egnethet

Kvalitet i geodata beskrives med noen faste elementer fra standarden ISO 19157:

| Element | Spørsmålet | Eksempel |
|---|---|---|
| **Fullstendighet** | Mangler noe, eller er noe med som ikke skal være der? | Nye bygg mangler, eller revne bygg ligger fortsatt i datasettet. |
| **Logisk konsistens** | Følger dataene reglene for format, kodelister og geometri? | Polygoner med selvkryss, eller en bygningstype som ikke finnes i kodelisten. |
| **Posisjonsnøyaktighet** | Hvor nær ligger posisjonen den sanne posisjonen? | Eiendomsgrenser målt i felt mot grenser digitalisert fra gamle kart. |
| **Tematisk nøyaktighet** | Er attributtene riktige? | Feil bygningstype eller bruksareal. |
| **Tidsmessig kvalitet** | Hvor aktuelle er dataene, og hva gjelder tidspunktet? | Flybilder fra 2019 sier ikke noe om hvordan det ser ut i 2026. |

I tillegg kommer spørsmålet som teller mest: er dataene **egnet til formålet mitt**? Kvalitet er ikke absolutt. Et datasett kan være godt nok til et oversiktskart, men for dårlig til en byggesak.

#### Metadata i praksis

Metadata følger standarden ISO 19115, og i Norge brukes en norsk profil. På [Geonorge](https://www.geonorge.no/) finner du dem som beskrivelsen av hvert datasett i [kartkatalogen](https://kartkatalog.geonorge.no/). Se også [Kartverkets oversikt over standarder](https://www.kartverket.no/geodataarbeid/standarder). Lager du data selv, bør du beskrive dem like grundig: hva de inneholder, hvor de kommer fra, når de ble laget og hvilken lisens som gjelder. Virksomheter som publiserer i Geonorge bruker [metadataeditoren](https://editor.geonorge.no/).

#### Enkle tekniske kontroller

Metadata forteller hva dataene *skal* være. Noen enkle spørringer viser hvordan de faktisk er:

```sql
INSTALL spatial; LOAD spatial;

-- Antall objekter, manglende og ugyldige geometrier
SELECT count(*) AS antall,
       count(*) FILTER (WHERE geom IS NULL) AS uten_geometri,
       count(*) FILTER (WHERE NOT ST_IsValid(geom)) AS ugyldige
FROM st_read('bygg.gpkg');

-- Manglende verdier i en kolonne
SELECT count(*) FILTER (WHERE bruksareal IS NULL) AS mangler_areal FROM st_read('bygg.gpkg');

-- Duplikater på identifikator
SELECT bygg_id, count(*) FROM st_read('bygg.gpkg') GROUP BY bygg_id HAVING count(*) > 1;

-- Utstrekning: ligger koordinatene der de skal? (for punktdata)
SELECT min(ST_X(geom)), max(ST_X(geom)), min(ST_Y(geom)), max(ST_Y(geom)) FROM st_read('bygg.gpkg');
```

I QGIS finnes tilsvarende verktøy, for eksempel [Check validity](https://docs.qgis.org/latest/en/docs/user_manual/processing_algs/qgis/vectorgeometry.html#check-validity). Og husk koordinatsystemet: en feil her gir stille feil i alle senere beregninger, som vi så i [Geografiske operasjoner](side:geografiske-operasjoner).

@@ aktivitet
- Velg et datasett i [Geonorge kartkatalog](https://kartkatalog.geonorge.no/) som er relevant for jobben din. Gå gjennom de seks første spørsmålene i sjekklisten. Hva gjør du hvis svaret på ett av dem er «vet ikke»?
- Sammenlign metadata for FKB-Bygning med en annen bygningskilde, for eksempel OpenStreetMap eller Overture Maps. Hvilken passer best til (a) å vise bygg på et kart og (b) å telle bygg i en kommune?
- Kjør kvalitetsspørringene på et datasett du har. Hvor mange ugyldige geometrier eller manglende verdier finner du?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [Essentials of Geographic Information Systems: Data about data (metadata)](https://saylordotorg.github.io/text_essentials-of-geographic-information-systems/s07-02-data-about-data.html)
- [Essentials of Geographic Information Systems: Data quality](https://saylordotorg.github.io/text_essentials-of-geographic-information-systems/s09-04-data-quality.html)

@@ interessert
- [Geonorge kartkatalog](https://kartkatalog.geonorge.no/)
- [Kartverket: Standarder](https://www.kartverket.no/geodataarbeid/standarder)
- [Norsk lisens for offentlige data (NLOD) 2.0](https://data.norge.no/nlod/no/2.0)
- [Felles kartdatabase (FKB): datasettbeskrivelse](https://data.norge.no/en/datasets/92df56fb-0625-30bc-9305-f8cad94db1a0/felles-kartdatabase-fkb)
