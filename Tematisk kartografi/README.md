# Tematisk kartografi: fem visualiseringsmetoder

En demo til bruk i undervisning: fem mye brukte metoder for å visualisere
tematiske data på kart, illustrert med ekte, live hentede datasett (ikke
syntetiske tall). Bildene presenteres i [index.html](index.html), sammen med
korte forklaringer og lenker til videre lesning.

Åpne `index.html` direkte i nettleseren – den bruker kun ferdiggenererte
bilder, ingen server nødvendig.

## Metodene

1. **Choropleth** – fylker farget etter befolkningstetthet
2. **Proporsjonale sirkler** – folketall per fylke som arealproporsjonale sirkler
3. **Dot density-kart** – befolkning i Agder-kommunene, disaggregert til prikker
4. **Dorling-kartogram** – folketall per fylke, areal fordreid etter verdi
5. **Heatmap (kernel density estimation)** – samme befolkningspunkter som dot
   density-kartet (Agder), vist som en glattet tetthetsoverflate

Metode 1, 2 og 4 bruker **samme datasett** (folketall per fylke). Det er med
vilje: poenget er å vise hvordan valg av metode endrer hva kartet
kommuniserer, selv når tallene bak er identiske. Choropleth bør vise rater
(tetthet), proporsjonale sirkler kan vise absolutte totaler, og kartogrammet
viser samme totaler som en bevisst arealforvrengning.

Metode 3 og 5 bruker på samme måte **identiske punktdata** (de disaggregerte
befolkningspunktene for Agder): dot density viser dem som diskrete prikker,
heatmap som en kontinuerlig, glattet overflate (kernel density estimation).
Samme data, to måter å representere tetthet på.

## Hvorfor disse fem

Dot map, choropleth, proporsjonale sirkler og heatmap var det brukeren ba om.
Dorling-kartogram er lagt til som et femte, mye brukt eksempel – det er en
naturlig forlengelse av proporsjonale sirkler (samme prinsipp: areal ∝
verdi), men går enda lenger i å forlate geografien, noe som gjør det til et
godt pedagogisk kontrastpunkt til choropleth (som er 100 % geografitro, men
kan skjule verdien bak enhetens faktiske areal).

Andre kjente metoder som *ikke* er med her, men som er naturlige å nevne i
undervisning: **isoline/isaritmiske kart** (konturlinjer, f.eks. høydekoter
eller temperatur – i praksis en annen fremstilling av samme type
kontinuerlig overflate som heatmap-eksemplet bygger på) og **flow maps**
(opprinnelse–destinasjon-strømmer, f.eks. flyttemønstre). Flow maps ble
vurdert for dette oppsettet, men krever en opprinnelse–destinasjon-matrise
(f.eks. flyttetall *mellom* hvert par av fylker) som ikke var praktisk å
hente fra SSBs API innenfor denne demoen.

## Kjøre skriptet selv

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python3 generer_eksempler.py
```

Skriptet henter alt fra nettet ved hver kjøring – ingen tall er hardkodet:

| Data | Kilde | Hentes via |
|---|---|---|
| Fylkesgrenser | Kartverket/Geonorge | `kommuneinfo`-API, ett kall per fylke |
| Kommunegrenser (Agder) | Kartverket/Geonorge | Samme API, filtrert på fylkesnummer 42 |
| Befolkning per fylke/kommune | SSB, tabell [01222](https://www.ssb.no/statbank/table/01222) | Siste tilgjengelige kvartal, hentet automatisk (ikke et fast årstall) |

Fargene i choropleth-kartet (CARTOColors SunsetDark) er tatt fra paletten i
det nabostående verktøyet
[Fargeskalaer for tematiske kart](../Fargeskalaer%20for%20tematiske%20kart/index.html)
i denne repoen, ikke hardkodet på frihånd.

Fordi SSB-dataene oppdateres kontinuerlig, vil befolkningstallene (og dermed
alle fem figurene) se litt annerledes ut hver gang skriptet kjøres på nytt.
Det er en feature, ikke en bug, for en undervisningsdemo – men betyr også at
de konkrete tallene i figurene ikke er "fasit", bare et øyeblikksbilde.

## Designvalg og fallgruver verdt å ta opp i undervisning

- **Choroplethets farge og klassifisering er to uavhengige valg.** Paletten
  er CARTOColors SunsetDark (hentet fra fargeskala-verktøyet nevnt over) i
  stedet for en lysere ColorBrewer-skala som YlOrRd – den holder seg mettet
  og mørk i hele spennet, så ingen klasse blir nesten hvit. Klassene er satt
  med *kvantiler* (nøyaktig 3 fylker per klasse), ikke Jenks natural breaks.
  Jenks ville her presset nesten hele landet inn i én eneste (lyseste) klasse,
  fordi Oslos tetthet er en så ekstrem outlier – korrekt gjengivelse av
  skjevfordelte data, men dårlig egnet til å vise variasjon i resten av
  landet. Kvantiler tvinger frem fargevariasjon over hele kartet, på
  bekostning av at fylker med ganske ulik tetthet kan havne i samme klasse.
  Begge er legitime valg; poenget er at man *velger* dem bevisst.
- **Proporsjonale sirkler skaleres i areal, ikke radius.** `s` i
  matplotlib sin `scatter()` er allerede et arealmål (punkter²), så
  `s = verdi / maks * skala` gir korrekt areal-proporsjonalitet direkte.
  En vanlig feil er å skalere radius lineært med verdien, som gir et
  sterkt overdrevet visuelt inntrykk av forskjeller. Selv korrekt
  areal-skalering er likevel ikke hele historien: Flannery (1956, 1971) viste
  at lesere systematisk undervurderer hvor mye større store sirkler er
  (Stevens' maktlov for arealpersepsjon), og enkelte kartografer bruker
  derfor en "psykologisk" (apparent magnitude) skalering som kompenserer for
  dette. Se lenke i index.html for formelen.
- **Dot density- og heatmap-kartene bruker identiske punktdata.** Prikkene
  plasseres med "rejection sampling" tilfeldig innenfor kommunegrensen (og
  proporsjonalt fordelt mellom øyer/deler ved multipolygoner), ikke på
  faktiske bosteder. Antall innbyggere per prikk er et designvalg som avgjør
  hvor "kornete" eller "jevnt" dot density-kartet ser ut – akkurat som
  KDE-båndbredden avgjør hvor "klumpete" eller "glatt" heatmapet blir. Begge
  kartene er mørke med gjennomsiktige farger (lysegrønne prikker /
  inferno-fargeskala) nettopp for å gjøre denne tetthetseffekten tydelig:
  tette områder blir visuelt lysere/sterkere der mange punkter/høy
  tetthet overlapper.
- **Kartogrammet bruker en enkel, selvskrevet Dorling-algoritme**: sirkler
  starter i fylkets ekte sentroid og flyttes iterativt bort fra hverandre
  til ingen overlapper. Det er ikke den samme implementasjonen som f.eks.
  ArcGIS eller ggplot2-paketter som `cartogram` bruker, men illustrerer
  samme prinsipp.

## Videre lesning (generelt)

- [Axis Maps – The Guide to Cartography](https://www.axismaps.com/guide) –
  kort, visuell gjennomgang av de fleste metodene i denne demoen
- [GIS Geography – Thematic Map types](https://gisgeography.com/map-types/)
- [Wikipedia – Choropleth map](https://en.wikipedia.org/wiki/Choropleth_map),
  [Dot distribution map](https://en.wikipedia.org/wiki/Dot_distribution_map),
  [Proportional symbol map](https://en.wikipedia.org/wiki/Proportional_symbol_map)
  (se spesielt avsnittet om
  [apparent magnitude/Flannery-skalering](https://en.wikipedia.org/wiki/Proportional_symbol_map#Apparent_magnitude_(Flannery)_scaling)),
  [Cartogram](https://en.wikipedia.org/wiki/Cartogram),
  [Heat map](https://en.wikipedia.org/wiki/Heat_map)
- [Fargeskalaer for tematiske kart](../Fargeskalaer%20for%20tematiske%20kart/index.html) –
  verktøyet i denne repoen som choropleth-paletten over er hentet fra

Se de enkelte seksjonene i [index.html](index.html) for metodespesifikke lenker.
