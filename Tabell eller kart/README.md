# Tabell eller kart?

En demo til bruk i undervisning: ett og samme datasett vist som en tabell og
som et kart. Tabellen viser hvert punkt med koordinatene som WKT-tekst
(`POINT (8.0031 58.1647)`) og attributter som tekst og tall. Kortet kan "snus" for
å vise de samme dataene i et kart. Poenget er at sammenhenger som er nesten
umulige å se i tabellen, blir umiddelbart intuitive i kartet.

Datasettet (`smiley.geojson`) er 59 punkter som danner en smiley. Prøv først å
gjette hva dataene forestiller ved å lese tabellen, og snu deretter kortet.

Åpne `index.html` gjennom en lokal server, f.eks.:

```
python3 -m http.server
```

(Siden henter GeoJSON-filen med `fetch`, så den fungerer ikke med `file://`.)

## Hva demoen skal vise

- **Tabellen skjuler romlige mønstre.** Koordinater som tekst er
  presise, men det er svært vanskelig å se at punktene danner et ansikt.
- **Kartet utnytter synet vårt.** Posisjon, farge og størrelse leses av på et
  øyeblikk – vi ser øyne, munn og ansiktsform uten å regne på noe.
- **Samme data, to visninger.** Ingenting er endret mellom forsiden og
  baksiden av kortet; bare representasjonen.
