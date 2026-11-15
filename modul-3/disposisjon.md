# Disposisjon – Modul 3: Geografisk analyse og kunstig intelligens

Én modulside og tre temasider. Hver temaside har seksjonene `intro`, `innhold`, `aktivitet`, `utvalgt` og `interessert`, som i modul 2. Punktene under er stikkord til innholdet, ikke ferdig tekst.

**Avgrensning mot tidligere moduler:**
- Modul 1 ([KI-agenter og geografisk IT](../canvas-kopi/pages/ki-agenter-og-geografisk-it.html)) introduserte agent-løkken, hallusinering og trappen prompt → instruksjoner → skills → MCP.
- Modul 2 ([KI-agenter og stack-valg](../modul-2/kilde/ki-agenter-og-stack-valg.md)) dekket typiske agentfeil, instruksjonsfiler og valg av stack. [Geografiske operasjoner](../modul-2/kilde/geografiske-operasjoner.md) dekket buffer og nærhet som *operasjoner*.
- Modul 3 går fra introduksjon til **praksis**: eget oppsett, skills andre har laget, hele analyser, og dømmekraften til å vurdere resultatet.
- Kurset handler i hovedsak om **vektordata**. Raster og satellittbilder nevnes med henvisninger, men er ikke tema.

> **TODO (påminnelse):** Beskriv sømmen mellom modul 1 og modul 2 i modul 3: studentene bruker det de lærte i modul 1 og 2 til å kvalitetssikre agenten, ikke bare agenten til å gjøre modul 1 og 2. Legg ved NTNU-forelesningene om arkitektur.

---

## 0. Modulside: Modul 3 – Geografisk analyse og kunstig intelligens

**intro:** Faglig underlag for samling 3. Modul 1 handlet om data, modul 2 om verktøy og operasjoner. Modul 3 handler om å *bruke* dem i analyser sammen med en KI-agent, og om å kunne vurdere om resultatet holder.

**Læringsmål.** Etter modulen skal du kunne
- sette opp et arbeidsmiljø der en KI-agent skriver og kjører analysekode reproduserbart (agent, uv, instruksjonsfil)
- finne, vurdere og ta i bruk skills andre har laget, og lage en enkel skill selv
- forklare nærhets-, tetthets- og dekningsanalyse, og hvilke valg som påvirker svaret
- bruke en KI-agent til å gjennomføre slike analyser på vektordata
- vurdere kritisk om et analyseresultat er til å stole på, og hvem som har ansvaret for det

**Agenda:** se [agenda.md](agenda.md).

**Temasider (toc):**

| Slug | Tittel | Én setning |
|---|---|---|
| `oppsett-agenter-og-skills` | Oppsett, agenter og skills | Et godt oppsett og de riktige skillene gjør agenten mer nyttig enn bedre prompter gjør, og mange av skillene finnes allerede. |
| `naerhet-tetthet-og-dekning` | Nærhet, tetthet og dekning | Tre analysetyper som svarer på de fleste «hvor»-spørsmål i forvaltning og næringsliv. Svaret avhenger av valgene du tar underveis. |
| `kritisk-vurdering-og-ansvar` | Kritisk vurdering og ansvar | Agenten kan gjøre analysen, men bare du kan avgjøre om den holder. Dette handler om dømmekraft, ikke om sjekklister. |

**Oppsummering (stikkord):**
- uv, en instruksjonsfil og et par gode skills gir bedre og mer repeterbare resultater enn bedre prompter.
- Mange nyttige skills er laget av andre. Les dem før du installerer dem.
- Nærhet, tetthet og dekning er enkle i prinsippet, men svaret avhenger av avstandsmål, aggregeringsenhet og terskler.
- At noe kjører uten feil, betyr ikke at det er riktig. Lag deg en forventning før du ser svaret.
- Ansvaret for analysen er ditt, ikke agentens.

**utvalgt:** Rød (2023), kapitler om analyse (TODO). **interessert:** se temasidene.

---

## 1. Oppsett, agenter og skills

*Slår sammen tidligere utkast «KI-teknikker for geodata», «Oppsett for KI-agenter» og «Skills, MCP og kodekjøring».*

**intro:** I modul 1 og 2 så vi hva agenter er og hvor de gjør feil. Nå setter vi opp et arbeidsmiljø du kan bruke videre: en agent som kan kjøre kode, en Python-installasjon som er lik hos alle, regler agenten følger, og skills som gir den gode arbeidsvaner.

**Innhold:**

#### KI-teknikker i oversikt (kort)
- Én tabell med teknikk → typisk oppgave → eksempel:
  - *Språkmodeller:* tolke spørsmål, skrive kode og SQL, oppsummere metadata.
  - *KI-agenter:* språkmodell + verktøy + løkke. Kjører analysen for deg. **Hovedtema i modulen.**
  - *Klassisk maskinlæring på vektordata:* klynger (DBSCAN, k-means) og prediksjon på punkter og polygoner med attributter.
  - *Bildeanalyse og raster:* arealdekke og objektdeteksjon fra flybilder og satellitt. Nevnes med henvisninger (GeoAI, samgeo, Kartverkets ajourhold av bygg), men dekkes ikke i kurset.
- Poeng: språkmodellen regner ikke. Den skriver kode som regner. Derfor er kodekjøring kjernen i oppsettet.

#### Agenten og arbeidsrommet
- Claude Code (terminal, VS Code, desktop) som hovedeksempel. Alternativer: GitHub Copilot (gratis for studenter via GitHub Education), Codex CLI, Gemini CLI. Prinsippene er like.
- Prosjektmappen er arbeidsrommet: agenten ser filene og kjører kommandoer der. Én mappe per analyse.
- Tillatelser: hva agenten får lese, skrive, kjøre og hente fra nett. Godkjenn kommandoer du ikke forstår før du godkjenner dem.
- Git som angreknapp: commit før og etter agentarbeid, og se på diffen.
- Hva sendes hvor? Data og kode går til leverandøren. Personopplysninger, graderte data og virksomhetens retningslinjer. Lokale modeller som alternativ, og hva du mister.

#### uv: Python som er lik hos alle
- Hvorfor: én kommando installerer Python og pakker, låser versjoner, og gjør at analysen kan kjøres igjen på en annen maskin.
- `uv init`, `uv add geopandas`, `uv run analyse.py`, `uv.lock`
- Skript som oppgir pakkene sine selv (PEP 723), og `uv run --with geopandas` for engangsskript.
- Regel til agenten: «Kjør Python med `uv run`, aldri `pip install`.»

#### Instruksjonsfil
- `CLAUDE.md` / `AGENTS.md`: kort mal for geo-prosjekter (CRS, data, mappestruktur, krav om skript og plan). Bygger videre på eksempelet fra modul 2.

#### Skills andre har laget
- Skills deles som vanlige mapper på GitHub. Det finnes tusenvis, og noen samlinger har over 100 000 stjerner. Mange av de mest brukte handler ikke om kode, men om **arbeidsmåte**: å bli utspurt, planlegge, verifisere og lære.
- Slik installerer du: som plugin (`/plugin install ...` i Claude Code), med `npx skills@latest add <repo>` (krever Node), eller ved å kopiere mappen til `.claude/skills/`.
- **Les før du installerer.** En skill er instruksjoner (og iblant skript) som agenten følger med dine tillatelser. Behandle den som kode fra en fremmed.
- Tabell til egen utforsking (antall stjerner per november 2026, avrundet):

| Skill | Samling | Hva den gjør | Hvorfor er den interessant for oss? |
|---|---|---|---|
| **grill-me** / **grilling** | [mattpocock/skills](https://github.com/mattpocock/skills) (~310k ★) | Intervjuer deg om planen din, ett spørsmål om gangen, til dere har felles forståelse. | Tvinger frem valgene du ikke har tatt: avstandsmål, terskel, aggregeringsenhet, datakilde. |
| **grill-with-docs** | mattpocock/skills | Som grill-me, men skriver ordliste og beslutningslogg underveis. | Dokumenterer analysevalgene, så andre kan etterprøve dem. |
| **teach** | mattpocock/skills | Lærer deg et konsept i arbeidsmappen din. | Lær klyngeanalyse eller romlig kobling på dine egne data. |
| **research** | mattpocock/skills | Undersøker et spørsmål mot primærkilder og lagrer funnene som Markdown. | Finne datakilder og dokumentasjon med kildehenvisning. |
| **interview-me** | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (~113k ★) | Finner ut hva du egentlig vil, ikke hva du tror du bør ville. | Uklare bestillinger fra ledelsen: «lag et kart over dekningen». |
| **doubt-driven-development** | addyosmani/agent-skills | Lar en ny kontekst gå kritisk gjennom hver viktig beslutning. | Et innebygd «djevelens advokat» for analysen. |
| **source-driven-development** | addyosmani/agent-skills | Forankrer kode i offisiell dokumentasjon. | Motvirker utdaterte API-er, som MapLibre-eksempelet fra modul 2. |
| **brainstorming** | [obra/superpowers](https://github.com/obra/superpowers) (~311k ★) | Utforsker idé og krav før noe bygges. | Før du starter en ny analyse eller kartløsning. |
| **writing-plans** | obra/superpowers | Lager en trinnvis plan før koding. | Gjør planen synlig, så du kan godkjenne den. |
| **systematic-debugging** | obra/superpowers | Finner årsaken før den foreslår en løsning. | Når resultatet er rart, ikke bare når koden feiler. |
| **verification-before-completion** | obra/superpowers | Krever bevis (kjørt kode, output) før agenten sier at noe er ferdig. | Motvirker «ferdig!» uten at noe er sjekket. |
| **discernment-nudge** | [anthropics/skills](https://github.com/anthropics/skills) (~187k ★) | Legger til 2–3 spørsmål etter et svar, som hjelper deg å sjekke fakta og antakelser. | Trener din egen kritiske vurdering (se side 3). |
| **skill-creator** | anthropics/skills | Hjelper deg å lage, teste og forbedre egne skills. | Utgangspunkt for å lage en skill for egen virksomhet. |
| **pdf**, **docx**, **xlsx** | anthropics/skills | Leser og lager dokumenter og regneark. | Rapporter og tabeller ut av analysen. |
| **find-skills** | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Finner og installerer skills for en oppgave. | Når du lurer på om noen allerede har laget det du trenger. |
| **fargeskalaer-tematiske-kart** | [dette repoet](../Fargeskalaer%20for%20tematiske%20kart/) | Velger fargeskala for tematiske kart. | Et fagspesifikt eksempel laget for kurset. |

- Kataloger å bla i: [skills.sh](https://skills.sh), [Claude-plugins](https://claude.com/plugins), [agentskills.io](https://agentskills.io).
- Diskusjon: hvorfor er så mange av de populære skillene laget for å *bremse* agenten og spørre deg?

#### Lage en egen skill (kort)
- Når holder instruksjonsfilen, og når trengs en skill? Skill = gjenbrukbar på tvers av prosjekter og kolleger.
- Mappe med `SKILL.md`, eventuelt `scripts/` og `references/`. Beskrivelsen styrer når den lastes.
- Test med og uten skill på samme oppgave. Bruk `skill-creator` som hjelp.
- MCP nevnes kort, som neste trinn når agenten trenger live data eller tilgang til systemer (henvis til modul 1).

**Aktivitet:** Ø1, Ø2 og Ø3 i [ovinger.md](ovinger.md). Diskusjon: Hvilken av skillene i tabellen ville du installert først, og hvorfor?

**utvalgt:** Claude Code-dokumentasjon (oppsett, CLAUDE.md, skills), uv-dokumentasjon (prosjekter og skript), agentskills.io.
**interessert:** samlingene i tabellen, Janowicz mfl. (2020) *GeoAI* og samgeo for de som vil se på raster.

---

## 2. Nærhet, tetthet og dekning

**intro:** Tre analysetyper svarer på de fleste «hvor»-spørsmål: Hvor langt er det til nærmeste? Hvor er det mest av noe? Hvor mange nås av en tjeneste? Analysene er enkle å kjøre, særlig med en agent, men svaret avhenger av valg som ofte tas uten at noen merker det.

**Innhold:**
- **Nærhet:** avstand til nærmeste, innenfor en terskel.
  - Luftlinje, avstand langs vegnett og reisetid. Hvor stor er forskjellen i en fjordkommune?
  - Verktøy: `sjoin_nearest` (geopandas), `ST_DWithin` og `<->` (PostGIS/DuckDB), osmnx og r5py for nettverk og reisetid. Henvis til modul 2 for operasjonene.
- **Tetthet og klynger:** hvor er det mest av noe, og hvor ligger det i grupper?
  - Tetthet: antall per sone (grunnkrets, kommune), per rute (SSB 250 m), per heksagon (H3) og kernel density estimation (KDE) med valg av bandwidth.
  - Klynger: DBSCAN finner grupper av punkter uten at du må velge soner eller ruter, men krever valg av `eps` (avstand) og minste antall punkter.
  - Samme data gir ulike kart med ulik cellestørrelse, bandwidth eller `eps`. Metoden og parameterne må følge med kartet.
  - Normalisering: per areal eller per innbygger, aldri bare antall.
- **Dekning:** andel av befolkningen eller arealet som nås av en tjeneste.
  - Serviceområder og isokroner, befolkning på rutenett, valg av terskel.
  - Lokaliseringsanalyse: hvor bør neste enhet ligge?
- **Valgene som styrer svaret** (felles for alle tre): avstandsmål, terskel, aggregeringsenhet, hvem som telles (befolkning på bosted, ikke hytteturister og pendlere), datakildens dekning (OSM er tettere i by enn i distrikt).
- **Casestudier (velg 3–4):**

| Case | Sektor | Analysetype | Data |
|---|---|---|---|
| Responstid for brann og redning | Forvaltning | Nærhet og dekning | Brannstasjoner, vegnett, befolkning på rutenett |
| Skolevei og skyss | Kommune | Nærhet (nettverk) | Skoler, adresser, vegnett (NVDB) |
| Legevakt og fastlege i distriktet | Helse | Dekning | Helseinstitusjoner, SSB rutenett |
| Ny butikk eller ladestasjon | Næringsliv | Tetthet og dekning | Befolkning, konkurrenter (OSM), trafikk (NVDB) |
| Mobil- og bredbåndsdekning | Næringsliv og Nkom | Dekning | Nkom dekningskart, befolkning |
| Hytter og fritidsboliger | Plan | Tetthet og klynger | Matrikkelen (bygningstype), kommuneplan |

- For hvert case: hvilket spørsmål, hvilke valg, og hvordan kan svaret misforstås eller misbrukes?

**Aktivitet:** Ø1, Ø4, Ø5 og Ø8 i [ovinger.md](ovinger.md). Diskusjon: hvilke analyser i din virksomhet er egentlig nærhet, tetthet eller dekning?

**utvalgt:** Rød (2023), SSB statistikk på rutenett, DSB dimensjoneringsforskriften.
**interessert:** osmnx, r5py, H3, DBSCAN i scikit-learn.

---

## 3. Kritisk vurdering og ansvar

*Erstatter tidligere utkast «Bias» og «Sjekk av resultater». Målet er å bygge dømmekraft, ikke å gi en oppskrift. Sjekklister blir utdaterte når verktøyene endres. Evnen til å stille de riktige spørsmålene gjør ikke det.*

**intro:** En agent kan levere en ferdig analyse med kart på få minutter. Den er overbevisende og ofte riktig. Det gjør det vanskeligere, ikke lettere, å oppdage når den er feil. Denne siden handler om hvordan du utvikler vanen og evnen til å vurdere et resultat, og om hvem som har ansvaret når det brukes.

**Innhold:**

#### Hvorfor dømmekraft og ikke oppskrift?
- Feilene endrer seg med hver ny modell og hvert nytt verktøy. En sjekkliste fanger gårsdagens feil.
- Det som varer, er fagkunnskapen (koordinatsystem, operasjoner, data) og vanen med å stille spørsmål.
- Det farligste resultatet er det som ser profesjonelt ut og bekrefter det du trodde fra før.

#### Tre vaner
1. **Gjør deg opp en mening før du ser svaret.** Hvor mange bygg tror du ligger mer enn 3 km fra en brannstasjon? Et grovt anslag gjør at du reagerer når svaret er 10 ganger for stort.
2. **Spør hvordan det kunne vært feil.** Tenk deg at analysen viste seg å være feil om et halvt år. Hva var mest sannsynlig årsak? Dataene, metoden, koden eller spørsmålet?
3. **Se det fra en annens ståsted.** Hva ville brannsjefen, en innbygger i distriktet eller en kollega som ikke liker konklusjonen spurt om?

#### Hvor skjevheter kommer fra (kort, som linse)
- Ett avsnitt, ikke en egen gjennomgang: data (ujevn dekning, hvem som er registrert), modell (kjenner Oslo bedre enn Bykle, og bekrefter gjerne det du antyder), metode (aggregeringsenhet, terskler, luftlinje) og oss selv (vi stoler for mye på maskinen).
- Henvisninger for de som vil lese mer: Haklay (2010), Manvi mfl. (2024), Parasuraman og Manzey (2010).

#### La verktøyene trene deg, ikke erstatte deg
- Skills som `grill-me`, `interview-me` og `discernment-nudge` er laget for å få *deg* til å tenke, ikke for å tenke for deg.
- Be agenten forklare hvorfor, ikke bare hva. Hvis du ikke kan forklare analysen til en kollega, er du ikke ferdig.
- Risikoen ved å slutte å øve: ferdighetene som trengs for å vurdere svaret, er de samme som agenten tar over.

#### Når passer KI, og når passer det ikke?
- Passer: når du kan vurdere svaret, når arbeidet er repetitivt, ved utkast og utforsking.
- Passer dårlig: når du ikke kan vurdere svaret, når feil rammer enkeltpersoner, når dataene ikke kan deles med leverandøren.

#### Ansvar og åpenhet
- Agenten tar ikke ansvar. Hvem signerer analysen?
- Hva bør stå om KI-bruk i en rapport: verktøy, hva KI gjorde, hva du vurderte selv, og hvordan.
- Rammer: EUs KI-forordning (kort om risikonivåer), personvern for lokasjonsdata, Digdirs veiledning, egen virksomhets retningslinjer.

**Aktivitet:** Ø6, Ø7 og Ø8 i [ovinger.md](ovinger.md) (med loggen fra verkstedene), og diskusjonen på slutten av samlingen: «Ville du levert dette resultatet til ledelsen i morgen? Hva måtte du visst først?»

**utvalgt:** Digdir: veiledning for ansvarlig bruk av KI, Datatilsynet om KI og personvern.
**interessert:** Haklay (2010) om OSM-kvalitet, Manvi mfl. (2024) *Large Language Models are Geographically Biased*, Parasuraman og Manzey (2010) om automatiseringsbias, GeoBenchX (fra modul 1).
