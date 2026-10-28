@@ intro
Denne siden er det faglige underlaget for Samling 2 – Teknologi og databehandling tirsdag 3. november kl. 09:00–13:00. Her finner du agenda, læringsmål og en oversikt over temaene vi tar for oss, med lenker til utdypende temasider og eksterne eksempler. Se gjennom siden før samlingen, og bruk den som oppslagsverk etterpå.
Modul 1 handlet om hva geografiske data er og hvor de kommer fra. Nå ser vi på hva vi gjør med dem: hvilke operasjoner vi kan utføre, med hvilke verktøy, og hvordan verktøyene settes sammen til løsninger. Hvert tema har en kort aktivitet du kan prøve selv.

@@ laeringsmaal
- orientere deg i verktøylandskapet for geografisk IT og velge kategori av verktøy ut fra oppgaven
- forklare de seks grunnleggende geografiske operasjonene (buffer, klipp, romlig kobling, nærhet, aggregering og overlay) og utføre enkle varianter i QGIS eller med et par linjer kode
- skille mellom desktop-, web- og serverprogramvare, og nevne eksempler på hver
- beskrive hvordan geografiske data lagres i databaser og filer, og når PostGIS, GeoPackage og skybaserte formater passer
- velge mellom kommandolinje, biblioteker og grafiske verktøy for en gitt oppgave
- beskrive fire arkitekturmønstre for kartløsninger og velge det enkleste som løser oppgaven
- vurdere datakvalitet og metadata før du tar et datasett i bruk
- vurdere hva KI-agenter kan bidra med i geografisk databehandling, og hvordan du styrer og kontrollerer dem

@@ agendatekst
Samling 2 – Teknologi og databehandling · tirsdag 3. november · [Zoom](https://uia.instructure.com/[ZOOM-LENKE])

@@ agenda
| Tid | Varighet | Aktivitet | Format | Innhold |
|---|---|---|---|---|
| 09:00–09:15 | 15 min | Åpning | Plenum | Repetisjon fra Modul 1 og oversikt over verktøylandskapet. |
| 09:15–10:00 | 45 min | Case og demo | Skjermdeling | Geografiske operasjoner steg for steg: buffer, romlig kobling og klipp i QGIS og i kode. |
| 10:00–10:10 | 10 min | Pause | – | – |
| 10:10–10:50 | 40 min | Disseksjon | Plenum | Programvare, databaser, CLI og biblioteker: hvordan verktøyene henger sammen. |
| 10:50–11:20 | 30 min | Lunsj | – | – |
| 11:20–12:00 | 40 min | Gruppearbeid | Breakout rooms, 3–4 per gruppe | Velg en oppgave fra din egen virksomhet. Hvilke operasjoner trengs, hvilke verktøy passer, og hvilken arkitektur vil du bruke? |
| 12:00–12:15 | 15 min | Oppsummering | Plenum | Gruppene rapporterer, og vi reflekterer sammen. |
| 12:15–12:25 | 10 min | Pause | – | – |
| 12:25–12:55 | 30 min | Case: KI-agenter og stack-valg | Plenum | Demo: en agent bygger en kartapp. Vi sjekker datakvalitet og resultat, og diskuterer hva vi velger å bygge. |
| 12:55–13:00 | 5 min | Avrunding | Plenum | |

@@ toc
verktoylandskapet|Verktøylandskapet|Geografisk IT har et stort utvalg av verktøy. Med et felles kart over kategoriene blir det lettere å velge riktig verktøy til riktig oppgave.
geografiske-operasjoner|Geografiske operasjoner|Seks operasjoner dekker det meste av hva du gjør med geodata. Når du kjenner dem, kjenner du igjen oppgavene i alle verktøy og kan gi gode oppdrag til en KI-agent.
desktop-web-og-serverprogramvare|Desktop, web og serverprogramvare|Samme oppgave kan løses i et skrivebordsprogram, en nettjeneste eller på en server. Temaet gir en oversikt over hva som finnes og hvem det passer for.
databaser-og-lagring|Databaser og lagring|Hvor dataene ligger bestemmer hva du kan gjøre med dem. Vi ser på databaser, filer og skybaserte formater.
cli-og-biblioteker|CLI og biblioteker|Kommandolinje og biblioteker gjør det mulig å automatisere og gjenta arbeid. Det er også språket KI-agenter bruker når de jobber med geodata.
arkitekturer|Arkitekturer|Fire mønstre for å sette sammen dataene, serverne og kartet. Hovedregelen er å velge det enkleste som løser oppgaven.
datakvalitet-og-metadata|Datakvalitet og metadata|Et datasett som ser riktig ut kan likevel være feil, gammelt eller uten lisens. Her er sjekklisten du bør gå gjennom før bruk.
ki-agenter-og-stack-valg|KI-agenter og stack-valg|Agenter gjør mye av det tekniske arbeidet raskere, men du må kunne styre og kontrollere dem, og velge hva de skal bygge.

@@ oppsummering
- Seks operasjoner dekker mesteparten av geografisk databehandling. Sjekk alltid koordinatsystemet før du måler avstand eller areal.
- Verktøyene kan grupperes i desktop, web, server, database, CLI og biblioteker. Samme oppgave kan ofte løses på flere måter.
- Velg det enkleste arkitekturmønsteret som løser oppgaven: frontend-only, frontend med API og database, 3-lags med kartserver, eller forhåndslagde fliser.
- Metadata og kvalitetssjekker er det som skiller et brukbart datasett fra et upålitelig.
- En KI-agent er en rask praktikant: godt egnet til å gjøre arbeid, men du må kunne kontrollere resultatet.

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
<!-- TODO: velg kapitler fra Rød -->

@@ interessert
- Se litteraturlistene på hver av temasidene for utdypende kilder.
