@@ intro
Denne siden er det faglige underlaget for Samling 3 – Geografisk analyse og kunstig intelligens. Her finner du agenda, læringsmål og en oversikt over temaene vi tar for oss, med lenker til utdypende temasider. Se gjennom siden før samlingen, og bruk den som oppslagsverk etterpå.
Modul 1 handlet om data, og modul 2 om verktøy og operasjoner. Nå bruker vi dem i analyser sammen med en KI-agent, og øver på å vurdere om resultatet holder. Kurset handler i hovedsak om vektordata. Raster og satellittbilder nevnes bare med henvisninger.

@@ laeringsmaal
- sette opp et arbeidsmiljø der en KI-agent skriver og kjører analysekode reproduserbart (agent, uv og instruksjonsfil)
- finne, vurdere og ta i bruk skills andre har laget, og lage en enkel skill selv
- forklare nærhets-, tetthets- og dekningsanalyse, og hvilke valg som påvirker svaret
- bruke en KI-agent til å gjennomføre slike analyser på vektordata
- vurdere kritisk om et analyseresultat er til å stole på, og hvem som har ansvaret for det

@@ agendatekst
Samling 3 – Geografisk analyse og kunstig intelligens · [DATO] · 09:15–13:00. Samlingen er bygget rundt to verksteder der du prøver selv.

@@ agenda
| Tid | Varighet | Aktivitet | Format | Innhold |
|---|---|---|---|---|
| 09:15–10:00 | 45 min | Nærhet, klyngeanalyse og dekning, og demo av skills | Skjermdeling | Mål for dagen og avstemning om oppsett. Nærhet, klyngeanalyse (DBSCAN) og dekning konseptuelt. Forhåndskjørte kjøringer av én nærhetsanalyse med fire modeller. Demo av `grill-me` og `skill-creator++`. |
| 10:00–11:00 | 60 min | Verksted 1: oppsett og første nærhetsanalyse | Breakout rooms, grupper | Sett opp prosjekt med uv og `CLAUDE.md`, og gjennomfør en nærhetsanalyse med agenten. |
| 11:00–11:30 | 30 min | Lunsj | – | – |
| 11:30–11:45 | 15 min | Felles refleksjoner fra verksted 1 | Plenum | Hva overrasket gruppene i agentens arbeid? |
| 11:45–12:15 | 30 min | Verksted 2: CTF med KI-agent | Breakout rooms, 3–4 per gruppe | Gran Canaria-CTF (DuckDB og Overture) løses med KI-verktøy. Deretter oversetter agenten spørringen til PostGIS, og gruppen skriver en kort logg. |
| 12:15–12:30 | 15 min | Pause | – | – |
| 12:30–12:45 | 15 min | Refleksjoner fra verksted 2 | Plenum | Gruppene viser ett resultat hver. «Ville du levert dette til ledelsen i morgen?» |
| 12:45–13:00 | 15 min | Prosjektoppgave og praktisk fremover | Plenum | Gjennomgang av prosjektoppgaven, og praktisk informasjon om det som kommer. |

@@ innhold
#### 1. Oppsett, agenter og skills
- KI-teknikker i oversikt: språkmodeller, agenter, klassisk maskinlæring og raster
- Agenten og arbeidsrommet: prosjektmappe, tillatelser, git og hva som sendes hvor
- uv: Python som er lik hos alle
- Instruksjonsfil (`CLAUDE.md`) for geoprosjekter
- Skills andre har laget, og hvorfor du må lese dem før du installerer
- Lage en egen skill

#### 2. Nærhet, tetthet og dekning
- Nærhet: luftlinje, vegnett og reisetid
- Tetthet og klynger: ruter, heksagoner, KDE og DBSCAN
- Dekning: isokroner, befolkning på rutenett og lokalisering
- Valgene som styrer svaret: avstandsmål, terskel, aggregeringsenhet og hvem som telles
- Casestudier fra forvaltning, helse og næringsliv

#### 3. Kritisk vurdering og ansvar
- Dømmekraft i stedet for sjekklister
- Tre vaner: gjør deg opp en mening først, spør hvordan det kunne vært feil, og se det fra en annens ståsted
- Hvor skjevheter kommer fra: data, modell, metode og oss selv
- Når KI passer, og når det ikke gjør det
- Ansvar og åpenhet om KI-bruk

@@ oppsummering
- uv, en instruksjonsfil og et par gode skills gir bedre og mer repeterbare resultater enn bedre prompter.
- Mange nyttige skills er laget av andre. Les dem før du installerer dem.
- Nærhet, tetthet og dekning er enkle i prinsippet, men svaret avhenger av avstandsmål, aggregeringsenhet og terskler.
- At noe kjører uten feil, betyr ikke at det er riktig. Lag deg en forventning før du ser svaret.
- Ansvaret for analysen er ditt, ikke agentens.

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
<!-- TODO: velg kapitler fra Rød -->

@@ interessert
- Se litteraturlistene på hver av temasidene for utdypende kilder.
