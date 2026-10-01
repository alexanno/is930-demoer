# Fargeskalaer for tematiske kart

Et verktøy for å velge og forstå fargeskalaer i tematisk kartografi og
datavisualisering. **ColorBrewer** (Cynthia Brewer) er utgangspunktet og
kjernen i verktøyet, men det samler også nyere skalaer fra kartografi og
visualisering i samme grensesnitt, med live forhåndsvisning, simulering av
fargeblindhet og ferdig fargekode-eksport — tingene ColorBrewer2.org aldri
har tilbudt i ett grensesnitt.

Åpne `index.html` direkte i nettleseren, eller via en lokal server om du
foretrekker det:

```
python3 -m http.server
```

Siden er ett selvstendig HTML-dokument uten eksterne avhengigheter (ingen
CDN-er, ingen byggesteg), så den fungerer også rett fra disk med `file://`.

## Hva verktøyet viser

- **Tre familier av skalaer** — sekvensiell, divergerende og kvalitativ —
  valgt via fanene øverst, med en kort forklaring av når hver type passer.
- **En syntetisk kartflate** (et sekskantrutenett) som fargelegges med den
  valgte skalaen, slik at man ser hvordan fargene faktisk leser som et kart
  og ikke bare som en fargestrip. «Nye data»-knappen genererer et nytt
  tilfeldig datasett.
- **Antall klasser** justeres med en skyveknapp, begrenset til det antallet
  hver kilde faktisk har definert (3–9 for de fleste ColorBrewer-sekvensene,
  opptil 11–12 for enkelte divergerende/kvalitative skalaer, 3–11 for de
  kontinuerlige viridis-skalaene).
- **Simulering av fargesynsavvik** (protanopi, deuteranopi, tritanopi) på
  forhåndsvisningen, basert på modellen til Machado, Oliveira & Fernandes
  (2009). Simuleringen er kun visuell — fargekodene som eksporteres er
  alltid de ekte verdiene.
- **Eksport** som HEX-liste, CSS-gradient, JSON-array eller en ferdig
  `matplotlib.colors.ListedColormap` i Python.

## Kildene som er brukt

| Kilde | Antall skjema | Merknad |
|---|---|---|
| [ColorBrewer](https://colorbrewer2.org) | 35 | Alle klassiske ColorBrewer-skalaer (sekvensiell, divergerende, kvalitativ), med klassetall hentet fra ColorBrewers eget datasett og fargeblind-merking fra RColorBrewer sin `colorblind`-liste |
| [CARTOColors](https://carto.com/carto-colors) | 34 | CARTOs egne fargepaletter, designet spesifikt for kartografi |
| Viridis-familien | 5 | Viridis, Magma, Inferno, Plasma og Cividis — perseptuelt jevne, kontinuerlige skalaer fra matplotlib/BIDS colormap-prosjektet |
| Okabe–Ito | 1 | Åtte-fargers kvalitativ palett konstruert for å være skillbar ved vanlige typer fargesynsavvik (Okabe & Ito, 2008) |

All fargedata er hentet direkte fra kildenes egne datasett (ikke anslått for
hånd): ColorBrewers eget JSON-eksport, CARTOColors sin TypeScript-kildekode,
og de originale Python-arrayene bak viridis-familien i matplotlib. Se
`index.html` sin «Kilder og videre lesning» for fulle referanser.

### Et par kildespesifikke detaljer

- **CARTOColors sine kvalitative paletter** inkluderer i originalkilden en
  ekstra, fast grå «annet»-farge utover de N kategorifargene (for data med
  en restkategori). Den er fjernet her for at «N klasser» skal bety nøyaktig
  N farger overalt i verktøyet, i tråd med de andre kildene.
- **TealRose (CARTOColors)** hadde et åpenbart kopier-lim-avvik i
  kildedataene, der 4- og 5-fargeversjonen var identiske. 4-fargeversjonen
  her er korrigert ved å fjerne den nøytrale midtfargen fra 5-fargeversjonen.

## Hvorfor dette finnes

ColorBrewer er fortsatt den beste referansen for fargeskalaer i kartografi,
men nettsiden er fra tidlig 2000-tall og dekker ikke skalaer som har blitt
sentrale i visualiseringsmiljøet siden (viridis-familien), eller
kartografi-spesifikke paletter utviklet senere (CARTOColors). Dette
verktøyet er ment som en moderne, undervisningsrettet inngang til fargevalg
for både ColorBrewer og det nyere landskapet — for studenter og andre som
skal lage tematiske kart og trenger en rask, begrunnet måte å velge farger
på.
