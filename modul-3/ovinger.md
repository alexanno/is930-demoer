# Øvinger og tutorials – Modul 3

Øvingene er skrevet for Claude Code, men virker med andre agenter (GitHub Copilot, Codex CLI, Gemini CLI). Alle øvingene har samme oppbygning: **mål**, **steg**, **vurder** og **refleksjon**. Vurder-delen inneholder åpne spørsmål, ikke en fasit. Poenget er at du selv skal finne ut hva som må sjekkes.

| Øving | Tema | Temaside | Tid | Når |
|---|---|---|---|---|
| Ø0 | Installasjon og oppsett | 1 | 30 min | Før samlingen |
| Ø1 | Første prosjekt: uv og instruksjonsfil | 1 | 15 min | Verksted 1 |
| Ø2 | Nærhetsanalyse med agent | 2 | 25 min | Verksted 1 |
| Ø3 | Prøv skills andre har laget | 1 | 40 min | Verksted 2, spor A |
| Ø4 | Lag din egen skill | 1 | 40 min | Spor A (forts.) / selvstudium |
| Ø5 | Tetthet og MAUP | 2 | 40 min | Verksted 2, spor B |
| Ø6 | Dekningsanalyse | 2 | 40 min | Selvstudium |
| Ø7 | Finn feilen | 3 | 40 min | Verksted 2, spor C |
| Ø8 | Samme spørsmål, ulike steder | 3 | 20 min | Selvstudium |

<a id="data"></a>
## Data

- **Øvingsdata:** de syntetiske dataene fra modul 2 ([modul-2/eksempeldata](../modul-2/eksempeldata/)): kommuner, grunnkretser, 500 bygg, vassdrag og tre brannstasjoner rundt Kristiansand i EPSG:25833. Siden de er syntetiske, kjenner vi fasiten.
- **Reelle data (TODO, til Ø5, Ø6 og selvstudium):** byggene i modul 2 er jevnt fordelt, og det gir lite å se i tetthet og dekning. Forslag til `modul-3/eksempeldata/` for Kristiansand eller Agder: befolkning på 250 m-rutenett (SSB), bygningspunkter (Matrikkelen via Geonorge, eller OSM), brannstasjoner og vegnett (NVDB eller OSM), grunnkretser.
- **Skript med feil (TODO, til Ø7):** se spesifikasjonen i øvingen.

---

## Ø0 Installasjon og oppsett (før samlingen)

**Mål:** Ha en agent, uv og git som virker, slik at samlingen kan brukes til analyse og ikke til installasjon.

**Steg:**
1. Installer **uv**:
   - Mac/Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
   - Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
2. Installer **git** hvis du ikke har det (`git --version` for å sjekke).
3. Installer en **agent**: Claude Code (se [dokumentasjonen](https://code.claude.com/docs/en/setup)) eller et alternativ. Start den i en tom mappe og be den si hei.
4. Last ned repoet, gå til `modul-3/ovinger` og kjør:
   ```bash
   uv run sjekk_oppsett.py
   ```
   uv laster ned Python og geopandas første gang. Det tar et minutt.

**Vurder:** Skriptet skal avslutte med `Oppsettet virker.` og skrive ut medianavstanden til nærmeste brannstasjon. Virker tallet rimelig, gitt at området er ca. 18 × 12 km med tre stasjoner?

**Refleksjon:** Åpne [sjekk_oppsett.py](ovinger/sjekk_oppsett.py). Kommentaren øverst (`# /// script`) forteller uv hvilke pakker skriptet trenger. Hvorfor gjør det skriptet lettere å dele med andre?

---

## Ø1 Første prosjekt: uv og instruksjonsfil

**Mål:** Lage en prosjektmappe der agenten har reglene den trenger for geodata.

**Steg:**
1. Lag et prosjekt og legg til pakker:
   ```bash
   uv init naerhet && cd naerhet
   uv add geopandas pyogrio matplotlib
   mkdir data && cp ../../modul-2/eksempeldata/{bygg,brannstasjon,kommuner}.gpkg data/
   git init && git add . && git commit -m "start"
   ```
2. Lag `CLAUDE.md` (eller `AGENTS.md`) med malen under, og tilpass den.
3. Start agenten i mappen og spør: «Hva vet du om dette prosjektet?» Svarer den ut fra instruksjonsfilen?

**Mal for instruksjonsfil:**
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

**Vurder:** Be agenten beskrive lagene og kolonnene i `data/`. Hvordan kan du finne ut om beskrivelsen stemmer, uten å spørre agenten igjen?

**Refleksjon:** Hvilke regler fra din egen virksomhet burde stått i en slik fil?

---

## Ø2 Nærhetsanalyse med agent

**Mål:** Gjennomføre en hel analyse fra spørsmål til resultat sammen med agenten, og danne deg en egen mening om resultatet.

**Steg:**
1. **Før du spør agenten:** skriv ned et anslag. Hvor mange av de 500 byggene tror du ligger mer enn 3 km fra nærmeste brannstasjon?
2. Gi agenten oppdraget:
   > Hvor mange bygg ligger mer enn 3 km fra nærmeste brannstasjon, og hvor mange er det per kommune? Lag et skript, kjør det, og lag et kart som viser byggene farget etter avstand.
3. Les planen før du godkjenner. Spør hvis noe er uklart.
4. La agenten kjøre. Les skriptet den lagde. Se på `git diff`.

**Vurder (med partneren din):**
- Hvor nær var anslaget ditt? Hvis det var langt unna: tok du feil, eller tok agenten feil?
- Hva i resultatet ville du måttet bekrefte selv før du viste det til noen?
- Finn én måte å kontrollere svaret på som ikke bruker agentens kode.

**Variant (for de raske):** Konverter dataene til EPSG:4326 (`ogr2ogr -t_srs EPSG:4326 ...`), fjern CRS-regelen fra instruksjonsfilen og kjør på nytt i en ny sesjon. Gjør agenten en feil? Ville du merket det hvis du ikke visste at den kunne skje?

**Refleksjon:** Avstanden er i luftlinje. Hvordan ville svaret endret seg med kjøreavstand i en fjordkommune? Hvordan ville du forklart det i en rapport?

---

## Ø3 Prøv skills andre har laget

**Mål:** Finne, vurdere og bruke skills fra andre, og se hvordan de endrer måten du jobber med agenten på.

**Steg:**
1. **Les før du installerer.** Åpne [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) på GitHub og les `SKILL.md`. Hva ber den agenten om å gjøre? Er det noe der du ikke ville latt agenten gjøre?
2. Installer, på én av disse måtene:
   - Claude Code-plugin: `claude plugin install mattpocock-skills@claude-plugins-official`
   - Med Node: `npx skills@latest add mattpocock/skills` (velg skillene du vil ha)
   - Manuelt: kopier mappen `grill-me` til `.claude/skills/` i prosjektet
3. Beskriv en analyse du vil gjøre, for eksempel en dekningsanalyse for legevakt i din region, og skriv `/grill-me`. Svar på spørsmålene til agenten er fornøyd.
4. Velg én skill til fra tabellen på temasiden *Oppsett, agenter og skills*, for eksempel `discernment-nudge`, `verification-before-completion` eller `teach`. Bruk den på Ø2-analysen.

**Vurder:**
- Hvilke spørsmål stilte `grill-me` som du ikke hadde tenkt på selv?
- Ble planen bedre, eller bare lengre?
- Hva gjorde den andre skillen annerledes enn agenten gjør uten den?

**Refleksjon:** Mange av de mest populære skillene er laget for å bremse agenten og spørre deg. Hvorfor tror du det er slik? Hvilken av skillene ville du anbefalt til en kollega?

---

## Ø4 Lag din egen skill

**Mål:** Lage en skill som gir agenten kunnskap om norske geodata eller din egen virksomhet, og finne ut om den hjelper.

**Steg:**
1. Lag mappen `.claude/skills/norsk-geodata/` med en `SKILL.md`. Start med eksempelet fra modul 1, eller be `skill-creator` (fra anthropics/skills) hjelpe deg.
2. Velg tre oppgaver der du vet hva et godt svar er, for eksempel:
   - «Lag en 500 m buffer rundt vassdrag i `data/vassdrag.gpkg`.»
   - «Hvilket koordinatsystem bør jeg bruke for et kart over Agder?»
   - «Hent kommunegrensene for Agder fra Geonorge.»
3. Kjør hver oppgave i en ny sesjon uten skill og med skill. Noter hva som ble annerledes.
4. Forbedre beskrivelsen (`description`) hvis skillen ikke ble brukt når den skulle.

**Vurder:** Hvordan vet du om skillen faktisk gjorde svarene bedre, og ikke bare annerledes? Hvor mange ganger må du kjøre en oppgave før du tror på forskjellen?

**Refleksjon:** Hva hører hjemme i en skill, og hva hører hjemme i instruksjonsfilen for ett prosjekt? Kunne kolleger i din virksomhet brukt skillen?

---

## Ø5 Tetthet og MAUP

**Mål:** Se hvordan valget av aggregeringsenhet endrer konklusjonen.

**Steg:**
1. Be agenten beregne byggtetthet (bygg per km²) på tre måter: per grunnkrets, per 250 m-rute og per 1 km-rute. Vis tre kart side om side.
2. Be den finne de fem tetteste områdene i hver variant.
3. Med reelle data: gjenta med kjernetetthet (KDE) og to ulike båndbredder.

**Vurder:**
- Peker variantene på de samme områdene? Hvis ikke: hvilken er «riktig»?
- Kan kartene sammenlignes, eller har agenten valgt ulike farger og klasser?
- Hvilken variant ville du vist til en politiker, og hvorfor?

**Refleksjon:** Dette er *the modifiable areal unit problem* (MAUP). Finn et eksempel fra din egen virksomhet der en inndeling i soner kan ha påvirket en beslutning.

---

## Ø6 Dekningsanalyse (selvstudium)

**Mål:** Beregne hvor stor andel av befolkningen som nås av en tjeneste, og se hvor følsomt svaret er for valgene.

**Steg (krever reelle data):**
1. Bruk gjerne `grill-me` på planen først (se Ø3).
2. Be agenten beregne andel innbyggere (fra SSB-rutenett) innen 5, 10 og 15 km luftlinje fra nærmeste brannstasjon.
3. Gjenta med kjøretid langs vegnettet (osmnx eller r5py) for 10 og 20 min.
4. Be agenten foreslå hvor en ny brannstasjon ville gitt størst økning i dekning.

**Vurder:**
- Hvor mye endret svaret seg mellom luftlinje og kjøretid? Overrasket det deg?
- Er forslaget til ny plassering et sted der det faktisk er mulig å bygge?
- Hvilke av forutsetningene ville en brannsjef protestert på?

**Refleksjon:** Hvem blir usynlige i et befolkningsrutenett (hytteturister, pendlere, de uten fast adresse)? Betyr det noe for konklusjonen?

---

## Ø7 Finn feilen

**Mål:** Øve på å vurdere et resultat du ikke har laget selv.

**Data (TODO):** `modul-3/ovinger/finn_feilen.py`, et skript som ser KI-generert ut og kjører uten feilmelding på dataene fra modul 2. Skriptet beregner «andel bygg i flomsone per kommune» og har fire innplantede feil:
1. Bufferen rundt vassdrag beregnes etter omprojisering til EPSG:4326 (grader).
2. `sjoin` med `how="inner"` mister bygg uten treff, så andelen beregnes av feil total.
3. Bygg som ligger på kommunegrensen, telles i begge kommunene.
4. Kartet viser antall og ikke andel, med en divergerende fargeskala.

Studentene får ikke vite hvor mange feil det er.

**Steg:**
1. Kjør skriptet og se på resultatet. Skriv ned førsteinntrykket: ser det rimelig ut?
2. Let etter feil **uten** agent i 15 min.
3. Be deretter agenten gå gjennom skriptet. Prøv også med `doubt-driven-development` eller `systematic-debugging`. Fant den det samme som deg?
4. Rett feilene og sammenlign resultatet med førsteinntrykket.

**Vurder:** Hva fikk deg til å mistenke hver feil? Var det noe du visste om geodata, noe i tallene, eller noe på kartet?

**Refleksjon:** Hvilke feil fant du, og hvilke fant agenten? Hva sier det om hvem som bør vurdere hva?

---

## Ø8 Samme spørsmål, ulike steder (selvstudium)

**Mål:** Oppdage at kvaliteten på svarene kan avhenge av *hvor* du spør om.

**Steg:**
1. Velg to kommuner: en stor (for eksempel Kristiansand) og en liten (for eksempel Bykle eller Kautokeino).
2. Still samme spørsmål om begge, uten nettsøk:
   - «Hvilke nabokommuner har kommunen?»
   - «Hva heter de største tettstedene, og hvor mange bor der?»
   - «Hva er de største arbeidsgiverne?»
3. Kontroller svarene mot SSB, Kartverket og Store norske leksikon.
4. Gjenta med en mindre modell, og med nettsøk slått på.

**Vurder:** Var feilene jevnt fordelt? Sa modellen fra når den var usikker? Hvilken av kildene du kontrollerte mot, stoler du mest på, og hvorfor?

**Refleksjon:** Hva betyr dette for analyser av distrikts-Norge? Hvordan ville du merket det i en analyse der du ikke kjenner stedet?
