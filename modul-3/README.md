# Modul 3: Geografisk analyse og kunstig intelligens

Arbeidsmappe for Modul 3. Foreløpig inneholder den disposisjon, agenda og øvinger. Innholdssidene skrives senere i `kilde/` med samme format som [modul-2](../modul-2/).

| Fil | Innhold |
|---|---|
| [disposisjon.md](disposisjon.md) | Modulside og tre temasider: formål, innhold, aktivitet og kilder for hver side |
| [agenda.md](agenda.md) | Agenda for samlingen 09:15–13:00, med kjørenotater og forberedelser |
| [ovinger.md](ovinger.md) | Øvinger og tutorials som studentene velger fritt fra i verkstedene |
| [ovinger/sjekk_oppsett.py](ovinger/sjekk_oppsett.py) | Testskript studentene kjører med `uv run` før samlingen |
| [ovinger/finn_feilen.py](ovinger/finn_feilen.py) | Skript med innplantede feil til Ø6 (fasit i agenda.md) |

## Modulbeskrivelse (fra studieplanen)

Modulen gir en oversikt over KI-teknikker som er relevante for geodata. KI-agenter i geografisk arbeidsflyt illustreres gjennom eksempler og demonstrasjoner: generering av analysekode, datavask, formatkonvertering og kartografisk visualisering. Sentrale analysetyper – nærhet, tetthet, dekningsanalyse – gjennomgås konseptuelt med casestudier fra forvaltning og næringsliv.

## Temasider

1. **Oppsett, agenter og skills** – agent, uv, instruksjonsfil, og skills andre har laget
2. **Nærhet, tetthet og dekning** – analysetypene, valgene som styrer svaret, og casestudier
3. **Kritisk vurdering og ansvar** – dømmekraft, ikke sjekklister

Kurset handler i hovedsak om vektordata. Raster og satellittbilder nevnes bare med henvisninger.

## Gjenstår (TODO)

- [ ] Eksempeldata med reell fordeling for tetthet og dekning (`eksempeldata/`, se [ovinger.md](ovinger.md#data))
- [ ] Sette dato i agenda og på modulsiden (`kilde/modulside.md`)
- [ ] Velge kapitler fra Rød (2023)

## Bygge Canvas-sider

`python3 bygg.py` leser `kilde/*.md` og skriver ferdige HTML-sider til `pages/`, som limes inn i Canvas (samme oppsett som [modul-2](../modul-2/)). Zoom-lenker er ikke med.
