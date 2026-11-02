# Agenda – Samling 3: Geografisk analyse og kunstig intelligens

Samling 3 – Geografisk analyse og kunstig intelligens · [DATO] · 09:15–13:00 · [Zoom](https://uia.instructure.com/[ZOOM-LENKE])

Samlingen er bygget rundt to verksteder der studentene prøver selv. Gjennomgang i plenum er kort og kobles alltid til det de nettopp har gjort. 40 min lunsj og én pause på 10 min.

## Agenda (format som modulsiden)

| Tid | Varighet | Aktivitet | Format | Innhold |
|---|---|---|---|---|
| 09:15–09:30 | 15 min | Åpning | Plenum | Mål for dagen, rask sjekk av oppsett (avstemning), KI-teknikker i oversikt. |
| 09:30–10:00 | 30 min | Nærhet, tetthet og dekning, og en agent som løser en av dem | Skjermdeling | De tre analysetypene konseptuelt. Deretter løser en agent en dekningsanalyse med uv og instruksjonsfil. Vi lar den gjøre en feil. |
| 10:00–10:40 | 40 min | Verksted 1: oppsett og første analyse | Breakout rooms, par | Sett opp prosjekt med uv og `CLAUDE.md`, og gjennomfør en nærhetsanalyse med agenten. |
| 10:40–10:50 | 10 min | Pause | – | – |
| 10:50–11:15 | 25 min | Skills andre har laget | Plenum og demo | Hva fant gruppene? Demo av `grill-me` på en analyseplan. Gjennomgang av tabellen med populære skills. |
| 11:15–11:55 | 40 min | Lunsj | – | – |
| 11:55–12:35 | 40 min | Verksted 2: velg et spor | Breakout rooms, 3–4 per gruppe | A: prøv og lag skills · B: tetthet og MAUP · C: finn feilen. |
| 12:35–12:55 | 20 min | Kritisk vurdering | Plenum | Gruppene viser ett resultat hver. «Ville du levert dette til ledelsen i morgen?» |
| 12:55–13:00 | 5 min | Avrunding | Plenum | Oppsummering og veien videre. |

## Kjørenotater

### Før samlingen (sendes ut én uke før)

- Studentene gjør **Ø0 Installasjon** i [ovinger.md](ovinger.md) og melder fra hvis noe ikke virker. Oppsett skal ikke ta tid på samlingen.
- Studenter uten tilgang til Claude Code bruker GitHub Copilot (gratis via GitHub Education), Gemini CLI eller Codex CLI. Øvingene virker med alle.
- Les temasiden *Oppsett, agenter og skills*, og bla i tabellen med skills.

### 09:15 Åpning

- Avstemning: «Har du kjørt testskriptet?» Ja / delvis / nei. De som svarer nei, settes i par med noen som svarer ja i verksted 1.
- KI-teknikker i oversikt: maks fem minutter med én tabell. Agenter på vektordata er tema. Raster og bildeanalyse nevnes bare.

### 09:30 Analysetyper og demo

- 10 min: nærhet, tetthet og dekning, med ett case hver. Legg vekt på valgene som styrer svaret.
- 20 min demo: «Hvor stor andel av byggene ligger mer enn 3 km fra nærmeste brannstasjon?»
  - Før agenten starter: spør salen om et anslag, og skriv det ned.
  - Vis rekkefølgen: tom mappe → `uv init` → `CLAUDE.md` → plan → godkjenning → skript → kjøring → kart → `git diff`.
  - **Planlagt feil:** kjør først uten instruksjonsfil på data i EPSG:4326, slik at agenten (sannsynligvis) beregner avstand i grader. Sammenlign med anslaget. Hva fikk oss til å reagere?
  - Reserve hvis agenten ikke gjør feilen: et forhåndslaget skript med feilen.

### 10:00 Verksted 1

- Ø1 og Ø2 i [ovinger.md](ovinger.md). Par: én styrer agenten, én spiller skeptiker. Bytt etter 20 min.
- Hver gruppe noterer **én ting som overrasket dem** i agentens arbeid. Lim inn i felles dokument eller chat.

### 10:50 Skills andre har laget

- Start med gruppenes funn (5 min).
- Demo (10 min): installer `grill-me` fra mattpocock/skills. Les `SKILL.md` høyt først: hva ber den agenten om å gjøre? Bruk den på planen for en dekningsanalyse. Hvilke spørsmål stilte den som vi ikke hadde tenkt på?
- Tabellen (10 min): gå raskt gjennom, og poengter at mange av de mest populære skillene handler om arbeidsmåte, ikke kode. Sikkerhet: les før du installerer.
- Avstemning om spor til verksted 2 før lunsj, slik at breakout rooms er klare.

### 11:55 Verksted 2

| Spor | Øving | Passer for |
|---|---|---|
| A: Prøv og lag skills | Ø3 (+ Ø4) | De som vil bygge noe gjenbrukbart for egen virksomhet |
| B: Tetthet og MAUP | Ø5 | De som lager kart og analyser for andre |
| C: Finn feilen | Ø7 | De som skal vurdere andres arbeid |

Alle grupper forbereder ett resultat (kart, skill eller funn) å vise på 2 min.

### 12:35 Kritisk vurdering

- Hver gruppe viser resultatet sitt. De andre stiller ett spørsmål om hvordan det kunne vært feil.
- Diskusjon: Ville du levert dette? Hva måtte du visst først? Hvem ville vært uenig i konklusjonen? Hvordan skriver du om KI-bruken i rapporten?
- Ikke avslutt med en sjekkliste. Avslutt med spørsmålene studentene selv stilte.

### 12:55 Avrunding

- Tre ting å ta med: et oppsett som kan gjentas, skills som får deg til å tenke, og ansvaret er ditt.
- Selvstudium: resten av øvingene, og bruk oppsettet på en oppgave fra egen jobb før neste samling.

## Underviser: forberedelser

- [ ] Demo-prosjekt klart, med og uten `CLAUDE.md` og med data i både EPSG:4326 og 25833
- [ ] Reserveskript med CRS-feilen
- [ ] `grill-me` testet i demo-miljøet, og en analyseplan å bruke den på
- [ ] Eksempeldata publisert og testet med `uv run` på Windows og Mac
- [ ] Skript med innplantede feil til spor C
- [ ] Felles dokument for gruppenes funn
- [ ] Breakout rooms forhåndsdefinert for spor A–C
