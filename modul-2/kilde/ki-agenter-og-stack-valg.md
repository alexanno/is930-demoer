@@ intro
KI-agenter som Claude Code, Codex og Copilot kan skrive SQL, GDAL-kommandoer og hele kartapper på minutter. Det flytter arbeidet fra å skrive kode til å formulere oppgaven og kontrollere resultatet. Her ser vi hva agenter er gode på, hvor det typisk går galt, hvordan du styrer dem, og hvordan du velger teknologi når en agent skal bygge for deg.

@@ innhold
#### Hva agenter er gode på, og hvor det går galt

| Godt egnet | Typiske feil å se etter |
|---|---|
| Skrive og forklare spatial SQL (DuckDB, PostGIS). | **Koordinatsystem:** buffer i grader i stedet for meter, eller blanding av EPSG:4326 og UTM. |
| Lage GDAL/ogr2ogr-kommandoer og små Python-skript med geopandas. | **Oppdiktede lag og kolonner** som ikke finnes i dataene dine. |
| Prototype en kartapp raskt. | **Utdaterte API-er:** koden er skrevet mot en eldre versjon av biblioteket. |
| Konvertere mellom formater og rydde i data. | **Stille feil:** skriptet kjører uten feilmelding, men resultatet er feil. |
| Forklare ukjent kode og feilmeldinger. | **Overdesign:** et rammeverk og tre lag der én HTML-fil hadde holdt. |

Et konkret eksempel er MapLibre GL JS fra versjon 6, som bare finnes som ES-modul. Agenter som er trent på eldre eksempler skriver ofte `<script src="maplibre-gl.js">`, og kartet vises aldri. Feilen er lett å rette hvis du vet hva du ser etter, og vanskelig å forstå hvis du ikke gjør det.

#### Slik styrer du en agent

1. **Gi kontekst i en instruksjonsfil.** Filer som `AGENTS.md` eller `CLAUDE.md` leses av agenten ved oppstart. Skriv hvilke versjoner du bruker, hva som ikke skal gjøres og hvordan resultatet testes.
2. **Gi den verktøy og kunnskap.** Skills og MCP-servere gir agenten faste arbeidsmåter og tilgang til systemer, for eksempel en database eller en dokumentasjonskilde.
3. **Krev verifisering.** Be agenten teste selv (kjøre koden, åpne kartet, sjekke at filene finnes), og gjør en egen kontroll av resultatet. For geodata betyr det å se på kartet og sjekke antall objekter, areal og koordinatsystem.

Eksempel på et avsnitt i en instruksjonsfil, hentet fra en erfaring med MapLibre:

```markdown
## MapLibre GL JS (v6+)
- Kun ES-modul. Bruk `import * as maplibregl from ".../maplibre-gl.mjs"` og `<script type="module">`.
- Pin eksakt versjon i CDN-URL-en (sjekk med `npm view maplibre-gl version`).
- Moduler lastes ikke fra file://. Server lokalt med `uv run python -m http.server 8000`.
- Test at kartet laster (`map.on("load")`) før koden leveres.
```

#### Stack-valg: ferdig kompilert løsning eller én HTML-fil?

Når en agent skal bygge, må du også velge *hva* den skal bygge. To ytterpunkter:

| Kriterium | Frontend + backend (kompilert, rammeverk) | Én HTML-fil |
|---|---|---|
| **Deploy** | Bygg-steg og server eller container. | Kopier filen til en statisk vert. |
| **Vedlikehold** | Mange avhengigheter som må oppdateres. | Få avhengigheter, men all kode i én fil. |
| **Sikkerhet** | Nøkler og passord kan holdes på serveren. | Alt er synlig i nettleseren. Aldri hemmelige nøkler. |
| **Datamengde** | Tåler store data og tunge spørringer via database. | Passer små data eller [skybaserte formater](side:arkitekturer). |
| **Hvem kan endre koden?** | Utviklere. | Alle som kan lese HTML, også agenten. |

Den enkleste løsningen som oppfyller kravene vinner. [Frontend-only kartappen](https://alexanno.github.io/is930-demoer/Frontend-only%20kartapp/index.html) er et eksempel på «én HTML-fil»: kartvisning, stedsnavnsøk og oppslag mot Kartverket og Geonorge uten byggesteg og uten backend. Så fort du trenger å skrive data, skjule en nøkkel eller styre tilgang, har du behov for en backend, som i [arkitekturmønster 2](side:arkitekturer).

#### Superhelt eller praktikant?

Agenten er best forstått som en rask og lærevillig praktikant. Den jobber raskt og er sjelden sliten, men den tar ikke ansvar for resultatet. Du må kunne nok til å se når svaret er feil, og ha oversikt over [datakvalitet](side:datakvalitet-og-metadata) og lisenser. Det er kunnskapen fra de foregående temaene (operasjoner, koordinatsystem, lagring, arkitektur) som gjør deg i stand til å gi gode oppdrag og kontrollere svarene.

@@ aktivitet
- Be en KI-agent om å lage en buffer på 100 m rundt vassdrag i et datasett du har. Sjekk koordinatsystemet i resultatet. Fikk du meter eller grader?
- Be en agent bygge en liten kartapp som viser et bakgrunnskart og søker på stedsnavn. Test den. Hvilke feil gjorde den, og hva hadde du kunnet skrevet i en instruksjonsfil for å unngå dem?
- Velg én av tre oppgaver: (a) et kart over kommunene på nettsiden, (b) et registreringsskjema for feltobservasjoner, (c) en kartløsning der brukerne har ulike tilganger. Hva ville du valgt av stack i hver?

@@ utvalgt
- [Rød, J. K. (2023): GIS – Verktøy for å forstå verden, 2. utgave, Fagbokforlaget](https://fagbokforlaget.no/produkt/9788245045222-gis)
- [Claude Code: Best practices](https://code.claude.com/docs/en/best-practices)
- [MapLibre GL JS](https://maplibre.org/maplibre-gl-js/docs/)

@@ interessert
- [Model Context Protocol (MCP)](https://modelcontextprotocol.io/)
- [AGENTS.md: åpent format for instruksjoner til kodeagenter](https://agents.md/)
- [Frontend-only kartapp (kildekode)](https://github.com/alexanno/is930-demoer/tree/main/Frontend-only%20kartapp)
