# Øvinger og tutorials – Modul 3

Øvingene er skrevet for Claude Code, men virker med andre agenter (GitHub Copilot, Codex CLI, Gemini CLI). Alle øvingene har samme oppbygning: **mål**, **steg**, **vurder** og **refleksjon**. Vurder-delen inneholder åpne spørsmål, ikke en fasit. Poenget er at du selv skal finne ut hva som må sjekkes.

**Terminal er valgfritt.** Alle kommandoer har en kommentar på hver linje (linjer som starter med `#`) som forklarer hva de gjør. Du kan kjøre dem selv, gjøre det samme i nettleser og filutforsker, eller be agenten gjøre det for deg: «Lag prosjektmappen, last ned dataene og legg dem i `data/`.»

**Velg fritt.** Du bestemmer selv hvilke øvinger du vil gjøre i verkstedene, og i hvilken rekkefølge. Øvingene forutsetter at uv, git og en agent er installert. Ø1 er et godt sted å starte, siden de andre bruker de samme dataene.

| Øving | Tema | Temaside |
|---|---|---|
| Ø1 | Oppsett og første nærhetsanalyse | 1 og 2 |
| Ø2 | Prøv skills andre har laget | 1 |
| Ø3 | Lag en skill for ditt eget fagområde | 1 |
| Ø4 | Tetthet og klynger | 2 |
| Ø5 | Dekningsanalyse | 2 |
| Ø6 | Finn feilen | 3 |
| Ø7 | Samme spørsmål, ulike steder | 3 |
| Ø8 | CTF med KI-agent: Gran Canaria | 2 |

<a id="data"></a>
## Data

Du laster ned dataene selv. Lag mappen `data/` i prosjektet og legg filene der. Ø1, Ø4 og Ø5 bruker de samme filene, så du trenger bare laste dem ned én gang. Ø6 bruker filene som ligger i [ovinger/](ovinger/).

| Data | Kilde | Nedlasting | Brukes i |
|---|---|---|---|
| Bygningspunkt | Matrikkelen – Bygningspunkt, Geonorge | [Metadata og nedlasting](https://kartkatalog.geonorge.no/metadata/uuid/24d7e9d1-87f6-45a0-b38e-3447f8d7f9a1) | Ø1, Ø4, Ø5 |
| Brannstasjoner | DSB via Geonorge | [Metadata og nedlasting](https://kartkatalog.geonorge.no/Metadata/uuid/0ccce81d-a72e-46ca-8bd9-57b362376485) | Ø1, Ø5 |
| Restauranter | Overture Maps (tema *places*) | [Slik henter du data](https://docs.overturemaps.org/getting-data/) | Ø4 |
| Befolkning 250 m | SSB, befolkning på rutenett, via Geonorge | [Alle årganger (tidsserie)](https://kartkatalog.geonorge.no/metadata/befolkning-paa-rutenett-250-m/0c0ad0ce-55e8-4d73-9c12-0eb0e2454acb), [bare 2026](https://kartkatalog.geonorge.no/metadata/befolkning-paa-rutenett-250-m-2026/d8f245c0-a002-4d3b-b833-10c638c6a879) | Ø4, Ø5, Ø6 |

**Slik laster du ned fra Geonorge (bygningspunkt og brannstasjoner):**
1. Åpne lenken i tabellen og klikk på nedlasting i kartkatalogen.
2. Velg område: **Agder** (fylke). Brannstasjonene er landsdekkende, og du kan laste ned hele landet og la agenten velge ut Agder.
3. Velg format **GeoPackage** hvis det finnes. Ellers duger FGDB eller GML. Agenten kan lese dem alle.
4. Velg koordinatsystem **EUREF89 UTM sone 33 (EPSG:25833)**.
5. Last ned, pakk ut zip-filen og legg filen i `data/` som `bygningspunkt.gpkg` og `brannstasjoner.gpkg`.

**Slik laster du ned befolkning (SSB-rutenett):** åpne lenken for 2026 i tabellen over (bruk tidsserie-lenken hvis du vil sammenligne år), og last ned **Agder** som **GeoPackage** i EPSG:25833, på samme måte som over. Du kan også bruke den ferdige filen i repoet: [Befolkning_42_Agder_25833_BefolkningsstatistikkRutenett250m2026_GPKG.gpkg](ovinger/Befolkning_42_Agder_25833_BefolkningsstatistikkRutenett250m2026_GPKG.gpkg). Legg den i `data/` som `befolkning_250m.gpkg`. Filen inneholder:
- Ett lag, `befolkningparutenett_befolkningparuter250m`, med 15 359 ruter på 250 × 250 m i Agder (2026), i EPSG:25833.
- Kolonnene `ssbid250m` (rute-ID), `poptot` (antall innbyggere) og `statistikkar` (årstall). Geometrien heter `omrade`.
- Til sammen 323 535 innbyggere. Bare **bebodde** ruter er med (minste verdi i `poptot` er 1). Ruter uten innbyggere finnes ikke i filen. Husk det når du regner areal, tetthet eller andeler.

**Slik laster du ned restauranter fra Overture Maps:**
```bash
# Forklaring av valgene: --bbox er et rektangel rundt Agder (vest,sør,øst,nord, i grader),
# -f geoparquet er filformatet, --type=place betyr steder (butikker, restauranter m.m.), -o er filen som lagres.
# uvx kjører verktøyet «overturemaps» uten å installere det permanent.
uvx overturemaps download --bbox=6.4,57.9,9.4,59.7 -f geoparquet --type=place -o data/steder_agder.parquet
```
Filen inneholder alle steder, ikke bare restauranter. Be agenten filtrere på kategorien `restaurant` (kolonnen `categories`). Verktøyets dokumentasjon: [overturemaps-py på GitHub](https://github.com/OvertureMaps/overturemaps-py). Datamodellen for steder: [docs.overturemaps.org](https://docs.overturemaps.org/).

---

## Ø1 Oppsett og første nærhetsanalyse

**Mål:** Lage en prosjektmappe der agenten har reglene den trenger for geodata, og gjennomføre en hel nærhetsanalyse på ekte data fra spørsmål til resultat. Danne deg en egen mening om resultatet.

**Steg:**
1. Lag et prosjekt og legg til pakker. Kommandoene kan du også be agenten kjøre:
   ```bash
   # Lag en ny prosjektmappe «naerhet» med et Python-oppsett
   uv init naerhet
   # Gå inn i mappen
   cd naerhet
   # Legg til pakkene: geopandas (geodata), pyogrio (rask filinnlesing), matplotlib (kart)
   uv add geopandas pyogrio matplotlib
   # Lag mappen «data» der datafilene skal ligge
   mkdir data
   # Gjør mappen til et git-repo, så du kan se hva agenten endrer
   git init
   # Legg alle filer til i neste lagring
   git add .
   # Lagre utgangspunktet med meldingen «start»
   git commit -m "start"
   ```
2. Last ned **bygningspunkt** og **brannstasjoner** (se [Data](#data)) og legg dem i `data/`.
3. Lag `CLAUDE.md` (eller `AGENTS.md`) med malen under, og tilpass den.
4. Start agenten i mappen og spør: «Hva vet du om dette prosjektet?» Svarer den ut fra instruksjonsfilen?
5. **Før du spør agenten om analysen:** skriv ned et anslag. Hvor stor andel av boligbyggene i Agder tror du ligger mer enn 5 km fra nærmeste brannstasjon?
6. Gi agenten oppdraget:
   > Hvor mange boligbygg (bygningstype 111–159) ligger mer enn 5 km fra nærmeste brannstasjon, og hvor mange er det per kommune? Lag et skript, kjør det, og lag et kart som viser byggene farget etter avstand.
7. Les planen før du godkjenner. Spør hvis noe er uklart.
8. La agenten kjøre. Les skriptet den lagde. Se på `git diff`.

**Mal for instruksjonsfil:**
```markdown
# Prosjekt: nærhetsanalyse

## Data
- Alle data ligger i `data/`: `bygningspunkt.gpkg` og `brannstasjoner.gpkg`. Ikke last ned andre data uten å spørre.
- Koordinatsystem: EPSG:25833 (UTM 33N, meter).

## Regler
- Kjør Python med `uv run`. Aldri `pip install`. Nye pakker: `uv add`.
- Avstand og areal beregnes i meter (projisert CRS), aldri i grader.
- Skriv analysen som skript i `analyse/`, ikke bare som svar i chatten.
- Lag en plan og vent på godkjenning før du skriver kode.
- Si fra hvis noe er usikkert. Les kolonnenavn fra dataene, ikke gjett.
```

**Vurder (i gruppen):**
- Be agenten beskrive lagene og kolonnene i `data/`. Hvordan kan du finne ut om beskrivelsen stemmer, uten å spørre agenten igjen?
- Hvor nær var anslaget ditt? Hvis det var langt unna: tok du feil, eller tok agenten feil?
- Hvilke bygg regnet agenten som bolig? Hva ville skjedd med svaret hvis fritidsbygg (16x) og garasjer (18x) var med?
- Hva i resultatet ville du måttet bekrefte selv før du viste det til noen?
- Finn én måte å kontrollere svaret på som ikke bruker agentens kode, for eksempel i QGIS.

**Variant (for de raske):** Konverter dataene til EPSG:4326, fjern CRS-regelen fra instruksjonsfilen og kjør på nytt i en ny sesjon. Gjør agenten en feil? Ville du merket det hvis du ikke visste at den kunne skje?
```bash
# Lag en kopi av bygningspunktene i lengde/bredde (EPSG:4326) i stedet for meter (EPSG:25833)
# -t_srs er koordinatsystemet som skal brukes. Først kommer filen som lages, deretter filen den leses fra.
ogr2ogr -t_srs EPSG:4326 data/bygningspunkt_4326.gpkg data/bygningspunkt.gpkg
```

**Refleksjon:** Hvilke regler fra din egen virksomhet burde stått i en slik fil? Avstanden er i luftlinje. Hvordan ville svaret endret seg med kjøreavstand i en fjordkommune, og hvordan ville du forklart det i en rapport?

---

## Ø2 Prøv skills andre har laget

**Mål:** Finne, vurdere og bruke skills fra andre, og se hvordan de endrer måten du jobber med agenten på.

**Steg:**
1. **Les før du installerer.** Åpne [grill-me](https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me) på GitHub og les `SKILL.md`. Hva ber den agenten om å gjøre? Er det noe der du ikke ville latt agenten gjøre?
2. Installer, på én av disse måtene (eller be agenten gjøre det):
   ```bash
   # Måte 1: installer som Claude Code-plugin fra den offisielle plugin-katalogen
   claude plugin install mattpocock-skills@claude-plugins-official
   ```
   ```bash
   # Måte 2: bruk Node til å hente skills fra GitHub. Du får velge hvilke skills du vil ha.
   npx skills@latest add mattpocock/skills
   ```
   ```bash
   # Måte 3 (manuelt): lag skills-mappen i prosjektet hvis den ikke finnes
   mkdir -p .claude/skills
   # Kopier mappen «grill-me» (lastet ned fra GitHub) inn i den
   cp -r grill-me .claude/skills/
   ```
3. Beskriv en analyse du vil gjøre, for eksempel en dekningsanalyse for legevakt i din region, og skriv `/grill-me`. Svar på spørsmålene til agenten er fornøyd.
4. Velg én skill til fra tabellen på temasiden *Oppsett, agenter og skills*, for eksempel `discernment-nudge`, `verification-before-completion` eller `teach`. Bruk den på Ø1-analysen.

**Vurder:**
- Hvilke spørsmål stilte `grill-me` som du ikke hadde tenkt på selv?
- Ble planen bedre, eller bare lengre?
- Hva gjorde den andre skillen annerledes enn agenten gjør uten den?

**Refleksjon:** Mange av de mest populære skillene er laget for å bremse agenten og spørre deg. Hvorfor tror du det er slik? Hvilken av skillene ville du anbefalt til en kollega?

---

## Ø3 Lag en skill for ditt eget fagområde

**Mål:** Lage en skill som gir agenten kunnskap om din egen virksomhet, ditt fagområde og dine egne problemstillinger, og finne ut om den hjelper.

**Steg:**
1. **Start i jobben din, ikke i verktøyet.** Skriv ned tre situasjoner fra eget fagområde der en agent uten bakgrunnskunnskap ville bommet. Eksempler på hva det kan være: interne begreper og forkortelser, datasett og systemer bare dere bruker, standarder og maler dere må følge, koordinatsystem og kilder dere alltid bruker, og vurderinger en kollega ville gjort automatisk.
2. Lag skillen. Du kan be `skill-creator` (fra anthropics/skills) hjelpe deg, eller skrive den selv:
   ```bash
   # Lag mappen for skillen. -p gjør at mellomliggende mapper lages samtidig. Gi mappen et navn som beskriver fagområdet ditt.
   mkdir -p .claude/skills/mitt-fagomrade
   # Lag filen SKILL.md. Den skal ha en «description» som sier når skillen skal brukes, og en brødtekst med kunnskapen.
   touch .claude/skills/mitt-fagomrade/SKILL.md
   ```
   Skriv inn det du la merke til i steg 1: begreper, datakilder, regler og vanlige feil. Skriv det slik du ville forklart det til en ny kollega.
3. Velg tre oppgaver fra egen jobb der du vet hva et godt svar er. Bruk gjerne ekte, anonymiserte eksempler.
4. Kjør hver oppgave i en ny sesjon uten skill og med skill. Noter hva som ble annerledes.
5. Forbedre beskrivelsen (`description`) hvis skillen ikke ble brukt når den skulle.

**Hvis du står fast, kan du låne en idé:** en skill om norske geodata med regler som «bruk EPSG:25833 for Agder», hvor kommunegrenser hentes fra, og at avstand regnes i meter. Det er et eksempel, ikke fasit. En skill fra din egen virksomhet er mer nyttig enn en generell.

**Vurder:** Hvordan vet du om skillen faktisk gjorde svarene bedre, og ikke bare annerledes? Hvor mange ganger må du kjøre en oppgave før du tror på forskjellen?

**Refleksjon:** Hva hører hjemme i en skill, og hva hører hjemme i instruksjonsfilen for ett prosjekt? Hvem i din virksomhet ville hatt nytte av skillen, og hva må være på plass før du tør dele den?

---

## Ø4 Tetthet og klynger

**Mål:** Se hvordan valg av metode og parametere (cellestørrelse, bandwidth, avstand) endrer hvor du finner «hotspots», og velge en metode du kan forsvare.

**Data:** restauranter fra Overture Maps og befolkning på 250 m-rutenett fra SSB (se [Data](#data)). Velg en kommune eller et byområde i Agder, for eksempel Kristiansand.

**Steg:**
1. **Hexagon-aggregering (H3):** be agenten telle restauranter per heksagon på to oppløsninger, for eksempel H3 8 og H3 9, og vise kartene side om side. Be den også regne restauranter per 1000 innbyggere, ved å fordele SSB-rutene på heksagonene. Husk at SSB-filen bare har bebodde ruter.
2. **Rutenett:** gjør det samme per SSB-rute (250 m). Ligner kartet på heksagonene?
3. **Kernel density estimation (KDE):** lag et tetthetskart for restaurantene med to ulike bandwidth, for eksempel 250 m og 1000 m.
4. **Klynger med DBSCAN:** be agenten finne klynger av restauranter med to verdier for `eps` (maks avstand mellom naboer, for eksempel 150 m og 500 m) og `min_samples`. Vis klyngene på kart, og merk hvilke restauranter som regnes som støy.
5. Be agenten finne de fem tetteste områdene med hver metode.

**Vurder:**
- Peker metodene på de samme områdene? Hvis ikke: hvilken er «riktig»?
- Hva skjer med DBSCAN når du dobler `eps`? Er det noe i dataene som tilsier hvilken verdi som er best?
- Er `eps` regnet i meter? Hva ville skjedd om agenten brukte grader?
- Kan kartene sammenlignes, eller har agenten valgt ulike farger og klasser?
- Hvilken variant ville du vist til en politiker, og hvorfor?

**Refleksjon:** Finn en beslutning i din egen virksomhet som bygger på et kart over «hvor det er mest av noe». Hvilke valg av metode og parametere lå bak, og visste mottakeren om dem?

**Dokumentasjon:** [H3](https://h3geo.org/docs) og [h3-py](https://uber.github.io/h3-py/), [DBSCAN i scikit-learn](https://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html), [KDE i scikit-learn](https://scikit-learn.org/stable/modules/density.html#kernel-density).

---

## Ø5 Dekningsanalyse

**Mål:** Beregne hvor stor andel av befolkningen som nås av en tjeneste, og se hvor følsomt svaret er for valgene.

**Data:** bygningspunkt, brannstasjoner og befolkning på 250 m-rutenett (se [Data](#data)), samt en ferdig isochrone-fil (se steg 3).

**Steg:**
1. Bruk gjerne `grill-me` på planen først (se Ø2).
2. **Luftlinje:** be agenten beregne andel innbyggere (fra SSB-rutenettet) innen 5, 10 og 15 km luftlinje fra nærmeste brannstasjon.
3. **Ferdig isochrone fra OpenRouteService:** i stedet for luftlinje bruker du en isochrone (et område som kan nås på en gitt kjøretid) som allerede er laget.
   - Last ned `isokron.geojson` fra underviser (**TODO:** lenke). Den viser hva som nås på 15 minutters kjøring fra et sted i Agder, og ligger i koordinatsystemet EPSG:4326.
   - Be agenten regne ut hvor mange innbyggere (SSB-ruter) og hvor mange boligbygg som ligger innenfor isochronen. Rutene og isochronen har ulike koordinatsystemer. Sjekk at agenten tar høyde for det.
   - Sammenlign med luftlinje på 10 km. Hva er forskjellen?
   - *Vil du lage en egen?* Hent en gratis API-nøkkel på [openrouteservice.org](https://openrouteservice.org/) og se [dokumentasjonen for isochrones](https://giscience.github.io/openrouteservice/api-reference/endpoints/isochrones). Kommandoen under ber om en 15-minutters isochrone for bil fra ett punkt:
     ```bash
     # Be OpenRouteService om en isochrone for kjøring med bil. Bytt DIN_NØKKEL med din egen API-nøkkel.
     # locations er punktet du starter fra (lengde, bredde). range er kjøretiden i sekunder (900 = 15 min).
     # Svaret lagres som GeoJSON i data/isokron.geojson.
     curl -X POST "https://api.openrouteservice.org/v2/isochrones/driving-car" -H "Authorization: DIN_NØKKEL" -H "Content-Type: application/json" -d '{"locations":[[7.99,58.15]],"range":[900]}' -o data/isokron.geojson
     ```
4. **Kjøretid langs vegnettet selv med osmnx:** se veiledningen under. Beregn kjøretid på 10 og 20 minutter fra nærmeste brannstasjon.
5. Be agenten foreslå hvor en ny brannstasjon ville gitt størst økning i dekning.

**Kom i gang med osmnx:**

[osmnx](https://osmnx.readthedocs.io/) laster ned vegnettet fra OpenStreetMap og lar deg regne kjøretid langs det. Start smått: ett tettsted, ikke hele Agder.
```bash
# Legg til osmnx i prosjektet
uv add osmnx
```
Skriptet under viser rekkefølgen. Be gjerne agenten bruke det som utgangspunkt.
```python
import osmnx as ox
import networkx as nx

# Last ned vegnettet for biler i Kristiansand (første gang tar det et minutt)
G = ox.graph_from_place("Kristiansand, Norway", network_type="drive")

# Legg til fartsgrense på hver veg (fra OSM, og et anslag der den mangler)
G = ox.add_edge_speeds(G)

# Regn ut kjøretid i sekunder for hver veg
G = ox.add_edge_travel_times(G)

# Finn vegnettets nærmeste punkt til brannstasjonen (X er lengde og Y er bredde, i grader)
node = ox.distance.nearest_nodes(G, X=7.99, Y=58.15)

# Finn alle punkter som nås innen 10 minutter (600 sekunder) fra brannstasjonen
nådd = nx.ego_graph(G, node, radius=600, distance="travel_time")

# Gjør de nådde vegene om til en GeoDataFrame, så du kan telle bygg og innbyggere innenfor
nodes, edges = ox.graph_to_gdfs(nådd)
```
Dokumentasjon og eksempler:
- [Brukerreferanse for osmnx](https://osmnx.readthedocs.io/en/stable/user-reference.html)
- [Eksempler fra osmnx-utvikleren (Jupyter-notebooks)](https://github.com/gboeing/osmnx-examples)
- [networkx `ego_graph`](https://networkx.org/documentation/stable/reference/generated/networkx.generators.ego.ego_graph.html)
- [r5py](https://r5py.readthedocs.io/) er et alternativ for kjøretid med kollektivtransport og større områder.

**Vurder:**
- Hvor mye endret svaret seg mellom luftlinje, OpenRouteService-isochronen og din egen osmnx-beregning? Overrasket det deg?
- Hvilke forutsetninger ligger i kjøretiden (fartsgrenser, trafikk, tid på døgnet)?
- Er forslaget til ny plassering et sted der det faktisk er mulig å bygge?
- Hvilke av forutsetningene ville en brannsjef protestert på?

**Refleksjon:** Hvem blir usynlige i et befolkningsrutenett (hytteturister, pendlere, de uten fast adresse)? Betyr det noe for konklusjonen?

---

## Ø6 Finn feilen

**Mål:** Øve på å vurdere et resultat du ikke har laget selv.

**Data:** [ovinger/finn_feilen.py](ovinger/finn_feilen.py), et skript som ser KI-generert ut og kjører uten feilmelding. Det henter kommunegrenser for Agder fra [robhop/fylker-og-kommuner](https://github.com/robhop/fylker-og-kommuner) og befolkning fra SSB-rutenettet i [ovinger/](ovinger/), og lager en tabell og et kart over befolkningen i kommunene. Du får ikke vite om det er feil, eller hvor mange.

**Steg:**
1. Kjør skriptet:
   ```bash
   # Gå til mappen der øvingsfilene ligger
   cd modul-3/ovinger
   # Kjør skriptet med uv. uv henter pakkene skriptet trenger første gang.
   uv run finn_feilen.py
   ```
2. Se på tabellen i terminalen og kartet (`kart_befolkning.png`). Skriv ned førsteinntrykket: ser det rimelig ut?
3. Let etter feil **uten** agent i 15 min.
4. Be deretter agenten gå gjennom skriptet. Prøv også med `doubt-driven-development` eller `systematic-debugging`. Fant den det samme som deg?
5. Rett feilene og sammenlign resultatet med førsteinntrykket.

**Vurder:** Hva fikk deg til å mistenke hver feil? Var det noe du visste om geodata, noe i tallene, eller noe på kartet?

**Refleksjon:** Hvilke feil fant du, og hvilke fant agenten? Hva sier det om hvem som bør vurdere hva?

---

## Ø7 Samme spørsmål, ulike steder

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

---

## Ø8 CTF med KI-agent: Gran Canaria

**Mål:** Løse en reell geodata-oppgave med et KI-verktøy, og reflektere over hvor verktøyet hjalp, og hvor det tok feil.

**Steg:**
1. Åpne [notebooken i Colab](https://colab.research.google.com/github/kartAI/skygeo/blob/main/src/skygeo-workshop/gran_canaria_overnatting_tetthet.ipynb). Den beskriver oppgaven og dataene (DuckDB og Overture Maps).
2. Løs CTF-en med en KI-agent (Claude Code eller tilsvarende). Du trenger ikke skrive SQL selv. Hvis agenten ikke virker, bruk chat i Colab. Noter hvilket verktøy du brukte.
3. Be agenten oversette spørringen din til **PostGIS-SQL**. Se på forskjellene fra DuckDB-versjonen.
4. Skriv en kort logg som gruppe (se under).

**Vurder:**
- Hvordan vet du at svaret er riktig, utover at CTF-en godtar det?
- Hva ble endret i oversettelsen til PostGIS? Hva ville stoppet spørringen i en ekte database?

**Refleksjon (logg, ca. 5 setninger):** Hvilket verktøy brukte dere? Hvor tok KI feil? Hvordan oppdaget dere det? Hva var forskjellen mellom DuckDB og PostGIS, og når ville dere valgt det ene eller det andre (fil mot server, flere brukere, indekser)?

**Mer om PostGIS og relasjonsdatabaser:** TODO: lenker til slides, Supabase-tutorials og PostGIS-intro.
