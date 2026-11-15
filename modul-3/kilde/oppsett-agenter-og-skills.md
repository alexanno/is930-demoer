@@ intro
I modul 1 og 2 så vi hva agenter er og hvor de gjør feil. Nå setter vi opp et arbeidsmiljø du kan bruke videre: en agent som kan kjøre kode, en Python-installasjon som er lik hos alle, regler agenten følger, og skills som gir den gode arbeidsvaner.

@@ innhold
#### KI-teknikker i oversikt

| Teknikk | Typisk oppgave | Merknad |
|---|---|---|
| **Språkmodeller** | Tolke spørsmål, skrive kode og SQL, oppsummere metadata. | Grunnlaget for resten. |
| **KI-agenter** | Språkmodell, verktøy og en løkke som kjører analysen for deg. | **Hovedtema i modulen.** |
| **Klassisk maskinlæring på vektordata** | Klynger (DBSCAN, k-means) og prediksjon på punkter og polygoner med attributter. | Klynger møter du på [neste side](side:naerhet-tetthet-og-dekning). |
| **Bildeanalyse og raster** | Arealdekke og objektdeteksjon fra flybilder og satellitt. | Dekkes ikke i kurset. Se GeoAI, samgeo og Kartverkets ajourhold av bygg. |

Språkmodellen regner ikke. Den skriver kode som regner. Derfor er kodekjøring kjernen i oppsettet.

#### Agenten og arbeidsrommet

Claude Code (terminal, VS Code eller desktop) brukes som hovedeksempel. Alternativer er GitHub Copilot (gratis for studenter via GitHub Education), Codex CLI og Gemini CLI. Prinsippene er de samme.

- **Prosjektmappen er arbeidsrommet.** Agenten ser filene og kjører kommandoer der. Bruk én mappe per analyse.
- **Tillatelser** styrer hva agenten får lese, skrive, kjøre og hente fra nett. Godkjenn aldri en kommando du ikke forstår.
- **Git er angreknappen.** Lagre (commit) før og etter agentarbeid, og se på diffen.
- **Hva sendes hvor?** Data og kode går til leverandøren. Tenk på personopplysninger, graderte data og virksomhetens retningslinjer. Lokale modeller er et alternativ, men du mister kvalitet og hastighet.

#### uv: Python som er lik hos alle

[uv](https://docs.astral.sh/uv/) installerer Python og pakker med én kommando, låser versjonene og gjør at analysen kan kjøres på nytt på en annen maskin.

```bash
# Lag et nytt prosjekt
uv init naerhet
# Legg til pakker
uv add geopandas pyogrio matplotlib
# Kjør et skript i prosjektets miljø
uv run analyse.py
```

Pakkene og versjonene ligger i `pyproject.toml` og `uv.lock`. Engangsskript kan oppgi pakkene sine selv (PEP 723), eller kjøres med `uv run --with geopandas skript.py`. Regelen du gir agenten er enkel: «Kjør Python med `uv run`, aldri `pip install`.»

#### Instruksjonsfil

`CLAUDE.md` (eller `AGENTS.md`) leses av agenten hver gang den starter. Hold den kort og konkret. Bygg videre på eksempelet fra modul 2. En kort mal for et geoprosjekt:

```markdown
# Prosjekt: nærhetsanalyse

## Data
- Alle data ligger i `data/`. Ikke last ned andre data uten å spørre.
- Koordinatsystem: EPSG:25833 (UTM 33N, meter).

## Regler
- Kjør Python med `uv run`. Aldri `pip install`. Nye pakker: `uv add`.
- Avstand og areal beregnes i meter (projisert CRS), aldri i grader.
- Skriv analysen som skript i `analyse/`, ikke bare som svar i chatten.
- Lag en plan og vent på godkjenning før du skriver kode.
- Si fra hvis noe er usikkert. Les kolonnenavn fra dataene, ikke gjett.
```

#### Skills andre har laget

En skill er en vanlig mappe med instruksjoner som agenten laster når den passer. Skills deles på GitHub. Det finnes tusenvis, og noen samlinger har over 100 000 stjerner. Mange av de mest brukte handler ikke om kode, men om **arbeidsmåte**: å bli utspurt, planlegge, verifisere og lære.

Du kan installere en skill som plugin (`/plugin install ...` i Claude Code), med `npx skills@latest add <repo>` (krever Node), eller ved å kopiere mappen til `.claude/skills/`.

**Les før du installerer.** En skill er instruksjoner (og iblant skript) som agenten følger med dine tillatelser. Behandle den som kode fra en fremmed.

Tabellen under er til egen utforsking (antall stjerner per november 2026, avrundet):

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
| **discernment-nudge** | [anthropics/skills](https://github.com/anthropics/skills) (~187k ★) | Legger til 2–3 spørsmål etter et svar, som hjelper deg å sjekke fakta og antakelser. | Trener din egen kritiske vurdering (se [siste temaside](side:kritisk-vurdering-og-ansvar)). |
| **skill-creator** | anthropics/skills | Hjelper deg å lage, teste og forbedre egne skills. | Utgangspunkt for å lage en skill for egen virksomhet. |
| **pdf**, **docx**, **xlsx** | anthropics/skills | Leser og lager dokumenter og regneark. | Rapporter og tabeller ut av analysen. |
| **find-skills** | [vercel-labs/skills](https://github.com/vercel-labs/skills) | Finner og installerer skills for en oppgave. | Når du lurer på om noen allerede har laget det du trenger. |

Kataloger å bla i: [skills.sh](https://skills.sh), [Claude-plugins](https://claude.com/plugins) og [agentskills.io](https://agentskills.io). Legg merke til at mange av de populære skillene er laget for å *bremse* agenten og spørre deg. Hvorfor tror du det er slik?

#### Lage en egen skill

Instruksjonsfilen gjelder ett prosjekt. En skill kan brukes på tvers av prosjekter og deles med kolleger. En skill er en mappe med `SKILL.md`, eventuelt med `scripts/` og `references/`. Beskrivelsen (`description`) styrer når agenten laster den. Test alltid med og uten skillen på samme oppgave, og bruk `skill-creator` som hjelp.

MCP er neste trinn, når agenten trenger live data eller tilgang til systemer. Det ble introdusert i modul 1.

@@ aktivitet
- Sett opp en prosjektmappe med `uv`, git og en `CLAUDE.md` med reglene over. Start agenten og spør: «Hva vet du om dette prosjektet?» Svarer den ut fra instruksjonsfilen?
- Les `SKILL.md` til `grill-me` på GitHub før du installerer den. Hva ber den agenten om å gjøre? Bruk den deretter på planen for en analyse du vil gjøre.
- Hvilken av skillene i tabellen ville du installert først, og hvorfor?
- Lag en enkel skill for ditt eget fagområde. Kjør tre oppgaver med og uten skillen. Ble svarene bedre, eller bare annerledes?

@@ utvalgt
- [Claude Code: dokumentasjon om oppsett, CLAUDE.md og skills](https://code.claude.com/docs/en/overview)
- [uv: dokumentasjon om prosjekter og skript](https://docs.astral.sh/uv/)
- [Agent Skills (agentskills.io)](https://agentskills.io)

@@ interessert
- Samlingene i tabellen: mattpocock/skills, addyosmani/agent-skills, obra/superpowers og anthropics/skills.
- Janowicz mfl. (2020): *GeoAI*, og [samgeo](https://samgeo.gishub.org/) for de som vil se på raster.
