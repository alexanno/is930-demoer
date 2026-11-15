# Agenda – Samling 3: Geografisk analyse og kunstig intelligens

Samling 3 – Geografisk analyse og kunstig intelligens · [DATO] · 09:15–13:00

Samlingen er bygget rundt to verksteder der studentene prøver selv. Gjennomgang i plenum er kort og kobles alltid til det de nettopp har gjort. 30 min lunsj og én pause på 15 min.

## Agenda (format som modulsiden)

| Tid | Varighet | Aktivitet | Format | Innhold |
|---|---|---|---|---|
| 09:15–10:00 | 45 min | Nærhet, klyngeanalyse og dekning, og demo av skills | Skjermdeling | Mål for dagen og avstemning om oppsett (5 min). Nærhet, klyngeanalyse (DBSCAN) og dekning konseptuelt (10 min). Forhåndskjørte kjøringer av én nærhetsanalyse med fire modeller (10 min). Demo av `grill-me` (10 min) og `skill-creator++` (10 min). |
| 10:00–11:00 | 60 min | Verksted 1 | Breakout rooms, grupper | Gruppene velger fritt blant øvingene i [ovinger.md](ovinger.md). Ø1 (prosjekt med uv og `CLAUDE.md`, og en nærhetsanalyse med agenten) er anbefalt start. |
| 11:00–11:30 | 30 min | Lunsj | – | – |
| 11:30–11:45 | 15 min | Felles refleksjoner fra verksted 1 | Plenum | Hva overrasket gruppene i agentens arbeid? |
| 11:45–12:15 | 30 min | Verksted 2 | Breakout rooms, 3–4 per gruppe | Gruppene velger fritt blant øvingene, også Ø8: Gran Canaria-CTF (DuckDB og Overture) løses med KI-verktøy, og agenten oversetter spørringen til PostGIS. Hver gruppe skriver en kort logg. |
| 12:15–12:30 | 15 min | Pause | – | – |
| 12:30–12:45 | 15 min | Refleksjoner fra verksted 2 | Plenum | Gruppene viser ett resultat hver. «Ville du levert dette til ledelsen i morgen?» |
| 12:45–13:00 | 15 min | Prosjektoppgave og praktisk fremover | Plenum | Gjennomgang av prosjektoppgaven, og praktisk informasjon om det som kommer. |

## Kjørenotater

### Før samlingen (sendes ut én uke før)

- Studentene har installert uv, git og en agent som forberedelse og kjørt testskriptet [sjekk_oppsett.py](ovinger/sjekk_oppsett.py). De melder fra hvis noe ikke virker. Oppsett skal ikke ta tid på samlingen.
- Studenter uten tilgang til Claude Code bruker GitHub Copilot (gratis via GitHub Education), Gemini CLI eller Codex CLI. Øvingene virker med alle.
- Les temasiden *Oppsett, agenter og skills*, og bla i tabellen med skills.

### 09:15 Skjermdeling

- **5 min åpning:** avstemning «Har du kjørt testskriptet?» Ja / delvis / nei. De som svarer nei, settes i gruppe med noen som svarer ja i verksted 1. KI-teknikker i oversikt nevnes i en setning: agenter på vektordata er tema, raster og bildeanalyse nevnes bare.
- **10 min analysetyper:** nærhet, klyngeanalyse (DBSCAN) og dekning, med ett case hver. Klyngeanalyse tas i stedet for tetthet: DBSCAN finner grupper av punkter uten at du må velge ruter eller soner. Legg vekt på valgene som styrer svaret (`eps`, minste antall punkter, avstandsmål). Tetthet (heksagoner og KDE) og klynger finnes som øving i Ø4.
- **10 min forhåndskjørt demo:** illustrativ og ikke en rettferdig test. Vis sammenligningstabellen og kommenter, ikke kjør live.
  - **Prompt (likt til alle):** «Hvor mange husstander bor innenfor 15 minutters kjøring fra [sted i Agder]? Bruk Matrikkelen – Bygningspunkt fra Geonorge (Agder) og isokronen i `isokron.geojson`.» Ingen URL, filformat eller koordinatsystem i promptet.
  - **Data:** isokron fra OpenRouteService (GeoJSON, EPSG:4326), laget på forhånd. Bygningspunkter lastes ned av agenten selv fra Geonorge (åpent, ca. 40 MB for Agder, EPSG:25832/25833).
  - **Modeller:** `gemma4:31b-cloud`, `glm-5.3:cloud` (begge via ollama; sjekk at taggene kan kjøres), Haiku 5.5 og Sonnet 5.5, i hver sin desktop-app. Én kjøring hver. Poenget er at ulike modeller og harnesser gjør ulike ting.
  - **Før du viser kjøringene:** spør salen om et anslag, og skriv det ned.
  - **Fasit (lages på forhånd, utenfor KI):** boligbygg (bygningstype 111–159) innenfor isokronen. Husstander finnes ikke i åpne data (kun bygningstype), så korrekt svar sier tydelig at tallet er bygninger, ikke husstander.
  - **Sammenligningstabell:**

    | Rad | Spørsmål |
    |---|---|
    | Nedlasting | Fant den riktig datasett, fylke og format? |
    | CRS | Håndterte den 4326 mot 25832/25833? |
    | Bolig-filter | Brukte den 111–159, eller tok den med fritidsbygg (16x) og garasjer (18x)? |
    | Husstand vs. bygning | Flagget den at dataene ikke har husstander? |
    | Svar og metode | Hvor langt fra fasiten, og var metoden riktig? |

  - **Hovedbudskap:** sjekk metoden, ikke bare svaret. Samme tall kan komme fra feil metode.
  - Bi-budskap: større modell er ikke alltid riktig, men gjør feil som er lettere å se. Alle fire kjører i skyen her, så personvernpoenget om lokale modeller tas som diskusjon.
- **10 min `grill-me`:** installer fra mattpocock/skills. Les `SKILL.md` høyt først: hva ber den agenten om å gjøre? Bruk den på planen for en analyse (gjerne klyngeanalysen fra konseptdelen). Hvilke spørsmål stilte den som vi ikke hadde tenkt på?
- **10 min `skill-creator++`:** vis hvordan en skill lages, testes og forbedres. Poenget er at en skill er en tekstfil du selv kan skrive og måle. Sikkerhet: les skills før du installerer dem. Tabellen med populære skills på temasiden leses i etterkant.

### 10:00 Verksted 1

- Gruppene velger fritt blant øvingene i [ovinger.md](ovinger.md), i den rekkefølgen de vil. Anbefal Ø1 som start, siden de andre bruker de samme dataene. Grupper på 2–3: én styrer agenten, én spiller skeptiker. Bytt roller underveis.
- Hver gruppe noterer **én ting som overrasket dem** i agentens arbeid. Lim inn i felles dokument eller chat.
- Noen kan trenge hjelp med nedlasting av data. Lenkene og fremgangsmåten står i [Data](ovinger.md#data) i ovinger.md.

### 11:30 Felles refleksjoner fra verksted 1

- Gå gjennom gruppenes funn (15 min). Be om konkrete eksempler: hva gjorde agenten, og hvordan oppdaget dere det?
- Knytt funnene til demoen om morgenen: sjekk metoden, ikke bare svaret.

### 11:45 Verksted 2

- Gruppene velger fritt blant øvingene. **Ø8** i [ovinger.md](ovinger.md) er Gran Canaria-CTF ([notebook](https://colab.research.google.com/github/kartAI/skygeo/blob/main/src/skygeo-workshop/gran_canaria_overnatting_tetthet.ipynb)). Notebooken beskriver oppgaven. Studentene trenger ikke skrive SQL.
- **Verktøy:** agent som hovedvei (Claude Code eller tilsvarende), chat i Colab som reserve. Alle noterer hvilket verktøy de brukte.
- Fordeling på 30 min: CTF (ca. 20 min) → PostGIS-oversettelse (ca. 5 min) → logg (ca. 5 min). Grupper som ikke rekker PostGIS, hopper over den og skriver loggen.
- **Logg per gruppe (kort):** verktøy, hvor KI tok feil, hvordan dere oppdaget det. Refleksjonen veier mer enn svaret.
- PostGIS: be agenten oversette DuckDB-spørringen til PostGIS-SQL. Diskuter forskjellene (fil mot server, flerbrukertilgang, indekser) i plenum hvis det er tid.
- Grupper som velger andre øvinger skriver samme type logg: hva de gjorde, hvor KI tok feil, og hvordan de oppdaget det.

### 12:30 Refleksjoner fra verksted 2

- Hver gruppe viser ett resultat fra loggen sin (ca. 1 min hver). De andre stiller ett spørsmål om hvordan det kunne vært feil.
- Du konkluderer selv: sømmen mellom modul 1 og 2 er at studentene bruker det de lærte der til å kvalitetssikre agenten.
- Spørsmål å ha klare: Ville du levert dette? Hva måtte du visst først? Hvem ville vært uenig i konklusjonen? Hvordan skriver du om KI-bruken i rapporten?
- Ikke avslutt med en sjekkliste. Avslutt med spørsmålene studentene selv stilte.

### 12:45 Prosjektoppgave og praktisk fremover

- Gjennomgang av prosjektoppgaven: [TODO: innhold, krav og frister].
- Praktisk: neste samling, innlevering og hvor studentene får hjelp.
- Tre ting å ta med: et oppsett som kan gjentas, skills som får deg til å tenke, og ansvaret er ditt.
- Etter samlingen: resten av øvingene, og bruk oppsettet på en oppgave fra egen jobb før neste samling.

## Underviser: forberedelser

- [ ] Isokron fra OpenRouteService som `isokron.geojson` (15 min bil, sted i Agder)
- [ ] Fasit laget uten KI: boligbygg (111–159) innenfor isokronen, fra Matrikkelen – Bygningspunkt (Agder). Lastes fra `nedlasting.geonorge.no/geonorge/Basisdata/MatrikkelenBygning/`
- [ ] Én forhåndskjørt demo per modell (`gemma4:31b-cloud`, `glm-5.3:cloud`, Haiku 5.5, Sonnet 5.5) og sammenligningstabell
- [ ] Klyngeanalyse (DBSCAN) som konseptcase: eksempeldata og et par `eps`-verdier som viser hvordan svaret endrer seg
- [ ] `grill-me` testet i demo-miljøet, og en analyseplan å bruke den på
- [ ] `skill-creator++` klargjort for demo, med et eksempel som kjører på 10 min
- [ ] Eksempeldata publisert og testet med `uv run` på Windows og Mac
- [ ] `isokron.geojson` lagt ut til studentene (Ø5), og lenken satt inn i ovinger.md
- [ ] Ø6 «Finn feilen» kjørt selv (`uv run finn_feilen.py` i `ovinger/`). Fasit under
- [ ] CTF-notebooken gjennomgått selv (Colab, DuckDB, Overture) og testet med en agent
- [ ] Lenker til slides, Supabase-tutorials og PostGIS-intro lagt inn i Ø8
- [ ] Prosjektoppgaven ferdig og klar til gjennomgang
- [ ] Felles dokument for gruppenes funn og logger
- [ ] Breakout rooms forhåndsdefinert for CTF-gruppene
- [ ] **TODO:** beskriv sømmen mellom modul 1 og 2, og legg ved NTNU-forelesningene om arkitektur

## Underviser: fasit til Ø6 «Finn feilen»

Ikke del denne delen med studentene før de har lett selv. Skriptet [ovinger/finn_feilen.py](ovinger/finn_feilen.py) har to innplantede feil. Resten (kommunegrenser fra robhop, ruter koblet til nærmeste kommune slik at hele befolkningen på 323 535 er med) er riktig.

1. **Kartet viser antall, ikke tetthet.** Choropleth-kartet av `befolkning` viser absolutt antall innbyggere. Antall følger kommunestørrelse og blir et kart over hvor kommunene er store, ikke hvor folk bor tett. Kristiansand dominerer, og småkommuner forsvinner. Riktig: innbyggere per km², eller en annen normalisering.
2. **Tetthet regnet i grader.** `kommuner.geometry.area` gir areal i EPSG:4326, altså grader², og deles på 1e6 som om det var m². Tettheten får urimelige verdier (over 10¹¹ «innbyggere per km²» for Kristiansand), og rangeringen blir feil. geopandas advarer også om det. Riktig: `to_crs("EPSG:25833")` før `.area`, og del på 1e6.

Hva studentene kan merke: tallene i tabellen er absurde, advarselen i terminalen, og at kartet ikke samsvarer med tabellen (kartet viser antall, tabellen «tetthet»). Rekkefølgen på de «tettest befolkede» kommunene kan likne den riktige, siden feil areal skalerer omtrent likt for nabokommuner på samme breddegrad. Poenget er at rangeringen kan se riktig ut selv om enheten er feil.
