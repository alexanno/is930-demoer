# Ulike bakgrunnskart

En demo til bruk i undervisning: samme kartutsnitt vist gjennom ni forskjellige
bakgrunnskart-tjenester, side om side. Panorer eller zoom i ett kart, og alle
de andre følger med. Poenget er å vise at et "kart" bare er en visning av
data, og at valget av datakilde og kartmotor påvirker hvordan verden ser ut.

Åpne `index.html` gjennom en lokal server, f.eks.:

```
python3 -m http.server
```

(Siden bruker ES-moduler, så den fungerer ikke hvis du åpner filen direkte i
nettleseren med `file://`.)

## Hva demoen skal vise

- **Bakgrunnskart er ikke nøytrale.** Samme sted ser forskjellig ut avhengig
  av hvem som har laget kartet, hva de har valgt å vise, og hvilken stil de
  har brukt.
- **To hovedmåter å levere kartdata på:**
  - **Raster** – ferdig tegnede bilder (PNG-fliser). Enkelt å bruke, men du
    kan ikke endre farger, språk eller hvilke lag som vises.
  - **Vektor** – geometri og egenskaper sendt til nettleseren, som tegner
    kartet selv. Mer arbeid å sette opp, men du kan style det akkurat som du
    vil (se OpenFreeMap-eksemplet).
- **"X-ray"** – Overture-eksemplet fjerner all kartografi og fargelegger
  hvert datalag for seg (vann, bygninger, veier osv.). Det viser hva et
  vektorkart egentlig består av under den pene stilen: rene geometrier med
  egenskaper, ikke et ferdig bilde.
- **MapLibre GL** er kartmotoren som brukes til å vise alt dette

## Kildene som er brukt

| Kart | Type | Kilde |
|---|---|---|
| OpenStreetMap | Raster | Fellesskapsdrevet, åpen kartdatabase ([openstreetmap.org](https://www.openstreetmap.org)) |
| OpenFreeMap Liberty | Vektor | Gratis, åpen vektorkart-tjeneste basert på OSM-data ([openfreemap.org](https://openfreemap.org)) |
| Overture Maps x-ray | Vektor | Åpne kartdata fra [Overture Maps Foundation](https://overturemaps.org) (Amazon, Meta, Microsoft m.fl.), lastet som pmtiles-arkiver og stylet selv i denne demoen for å vise de rå datalagene |
| Kartverket Topo | Raster | Det norske Kartverkets standard topografiske kart |
| Kartverket Topo Raster | Raster | Kartverkets topografiske kart som rasterbilder |
| Kartverket Gråtone | Raster | Samme kartgrunnlag som Topo, men i gråtoner – nyttig som bakgrunn når man skal fremheve egne data oppå |
| ESRI World Imagery | Raster | Satellittbilder fra ESRI sine gratis kartjenester |
| ESRI World Topo | Raster | ESRI sitt topografiske verdenskart |
| 1881 Norkart | Raster | Kartfliser lånt fra 1881.no sin karttjeneste (Norkart-data). Kun til undervisningsformål – ikke bruk nøkkelen i egne produkter |

## Hvordan Overture-eksemplet fungerer

De andre kartene er ferdige tjenester du bare kobler til. Overture gir deg
i stedet rådata – bygninger, vann, veier osv. – pakket i
[pmtiles](https://protomaps.com/docs/pmtiles)-arkiver, ett arkiv per tema,
som lastes direkte i nettleseren (ingen server nødvendig). Demoen gjør tre ting:

1. Registrerer `pmtiles://` som en protokoll MapLibre forstår
   (`pmtiles`-biblioteket gjør jobben).
2. Henter siste versjonsnummer dynamisk fra Overtures
   [STAC-katalog](https://stac.overturemaps.org/catalog.json) (feltet
   `latest`) i stedet for å skrive det inn manuelt – Overture ruller ut nye
   releaser jevnlig, så et hardkodet tall ville sluttet å virke.
3. Tegner hvert datalag (vann, land, bygninger, veier, administrative
   grenser, steder) i sin egen farge på svart bakgrunn – en "x-ray" av
   dataene, i stedet for et ferdig kartografisk uttrykk. Fargene beregnes
   ved å spre dem jevnt rundt fargesirkelen, så hvert lag er tydelig
   forskjellig fra naboene sine.

Se [docs.overturemaps.org](https://docs.overturemaps.org/examples/overture-tiles/)
for flere temaer du kan legge til.
