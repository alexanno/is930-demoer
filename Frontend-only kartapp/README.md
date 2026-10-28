# Frontend-only kartapp

En demo til bruk i undervisning: en komplett kartapp i én HTML-fil, uten egen server, database eller API-nøkler.
Kartfliser, et WMS-lag og tre ulike oppslag kommer fra tjenester som Kartverket, Miljødirektoratet, OpenStreetMap og EOX
drifter. Poenget er at du kan få til veldig mye ved å bruke andres tjenester, og at du kan se nøyaktig hvilke kall appen gjør.

Åpne `index.html` gjennom en lokal server, f.eks.:

```
uv run python -m http.server 8000
```

og gå til `http://localhost:8000` (siden bruker ES-moduler, så den fungerer ikke med `file://`).

## Hva demoen skal vise

- **Frontend-only betyr ikke «uten backend».** Appen har ingen egen server, men er klient i andres
  3-lags arkitektur: nettleseren spør Kartverkets kartserver, Miljødirektoratets WMS og Geonorges oppslagstjenester,
  som alle har database og server bak seg.
- **Kartfliser (WMTS/XYZ)** er bakgrunnskartene: Kartverket Topo og Gråtone, OpenStreetMap og Sentinel-2 fra EOX.
  MapLibre henter bare flisene som vises i kartvinduet.
- **WMS** er et lag fra Miljødirektoratet (naturvernområder). Til MapLibre er WMS bare en raster-kilde med
  en `GetMap`-adresse, og `GetFeatureInfo` brukes for å spørre «hva ligger her?» når du klikker.
- **REST-oppslag** mot Geonorge: stedsnavn (søk), kommune og høyde for punktet du klikker på.
- **Loggen i panelet** viser hvert kall. Åpne nettleserens utviklerverktøy (fanen *Network*) for å se det samme.

## Tjenestene som er brukt

| Hva | Tjeneste | Merknad |
|---|---|---|
| Kartfliser | [Kartverket kartfliser (WMTS)](https://cache.kartverket.no/v1/wmts/1.0.0/WMTSCapabilities.xml) | Åpne data, CC BY 4.0 |
| Kartfliser | [OpenStreetMap](https://operations.osmfoundation.org/policies/tiles/) | Vennligst følg retningslinjene for flisbruk. Ikke til tung trafikk |
| Satellittbilder | [Sentinel-2 cloudless, EOX](https://s2maps.eu) | CC BY-NC-SA 4.0: kun ikke-kommersiell bruk |
| WMS og GetFeatureInfo | Miljødirektoratet, vern | [GetCapabilities](https://kart.miljodirektoratet.no/arcgis/services/vern/MapServer/WMSServer?service=WMS&request=GetCapabilities) |
| Stedsnavn | [Kartverket stedsnavn-API](https://ws.geonorge.no/stedsnavn/v1/) | Åpent REST-API |
| Kommune | [Kommuneinfo-API](https://ws.geonorge.no/kommuneinfo/v1/) | Åpent REST-API |
| Høyde | [Høydedata-API](https://ws.geonorge.no/hoydedata/v1/) | Åpent REST-API |

## Prøv selv

Be en KI-agent om å legge til et nytt lag, for eksempel et annet WMS-lag fra [Geonorge kartkatalog](https://kartkatalog.geonorge.no/),
og se hva som må endres. Svaret er vanligvis: bare en ny kilde og et nytt lag i JavaScript-koden.
