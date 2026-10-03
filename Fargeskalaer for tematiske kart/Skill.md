---
name: fargeskalaer-tematiske-kart
description: Velger og forklarer fargeskalaer for tematiske kart (choropleth) og datavisualisering, med ferdige HEX-koder fra ColorBrewer, CARTOColors, Viridis og Okabe–Ito. Bruk når noen skal velge sekvensiell, divergerende eller kvalitativ fargeskala, bestemme antall klasser, sjekke fargeblind-sikkerhet, eller trenger fargekoder som HEX, CSS, JSON eller Python (matplotlib).
---

# Fargeskalaer for tematiske kart

Hjelper med å velge riktig fargeskala for data på kart og i diagrammer, og gir fargekoder klare til bruk. Detaljene ligger i `references/`; les bare filene oppgaven trenger.

## Arbeidsflyt

1. **Bestem datatype** → velg familie:
   - Ordnede verdier lav → høy (tetthet, andel, temperatur): **sekvensiell**
   - Avvik fra et meningsfullt midtpunkt (endring, over/under snitt): **divergerende**
   - Kategorier uten rangering (arealbruk, kommunetype): **kvalitativ**
2. **Velg antall klasser.** Hold deg til 5–7 for kart; færre for kvalitative. Antallet må finnes i kilden (se tabellene i katalogfilene).
3. **Vurder målgruppe.** Skal fargeblinde kunne lese kartet, eller skal det skrives ut i gråtoner? Velg da en skala merket «CVD-trygg», helst Viridis/Cividis (sekvensiell) eller Okabe–Ito (kvalitativ).
4. **Hent fargekodene** fra riktig katalogfil og lever dem i formatet brukeren trenger (se [eksport.md](references/eksport.md)).
5. **Forklar valget kort**: hvorfor denne familien og dette klasseantallet.

## Raske standardvalg

| Behov | Anbefalt utgangspunkt |
|---|---|
| Sekvensiell, generelt | Blues, YlGnBu eller Viridis |
| Sekvensiell, fargeblind-/gråtonesikker | Viridis eller Cividis |
| Divergerende, generelt | RdBu, PuOr eller BrBG (alle CVD-trygge) |
| Kvalitativ, fargeblind-sikker | Okabe–Ito, Safe eller Set2 |

Unngå regnbue-/jet-skalaer og rød–grønn-par (RdYlGn, Spectral) når leserne kan ha fargesynsavvik. Ikke bruk en sekvensiell skala på kategoridata, eller omvendt.

## Innholdsfortegnelse

Les kun det som trengs:

| Fil | Innhold | Les når |
|---|---|---|
| [velge-type.md](references/velge-type.md) | Hvilken type, klasseantall per kilde, perseptuell jevnhet | Brukeren er usikker på type, klasseantall eller hvorfor ikke regnbue |
| [tilgjengelighet.md](references/tilgjengelighet.md) | Fargesynsavvik, CVD-trygg-merket, simuleringsmatriser | Fargeblindhet, universell utforming eller simulering er tema |
| [skalaer-sekvensiell.md](references/skalaer-sekvensiell.md) | 44 sekvensielle skalaer med HEX per klasseantall | Du trenger fargekoder for ordnede data |
| [skalaer-divergerende.md](references/skalaer-divergerende.md) | 16 divergerende skalaer med HEX per klasseantall | Du trenger fargekoder for data med midtpunkt |
| [skalaer-kvalitativ.md](references/skalaer-kvalitativ.md) | 15 kvalitative skalaer med HEX per klasseantall | Du trenger fargekoder for kategorier |
| [eksport.md](references/eksport.md) | HEX, CSS, CSS-variabler, JSON, Python med eksempler | Brukeren vil ha koder i et bestemt format |
| [kilder.md](references/kilder.md) | Kilder og videre lesning | Brukeren ber om referanser |

Hver katalogfil starter med en oversiktstabell (skala, kilde, klasser, CVD) med lenker til detaljene; slå opp i den før du leser hele filen.

## Kilder

ColorBrewer (Brewer & Harrower), CARTOColors (CARTO), Viridis-familien (matplotlib/BIDS) og Okabe–Ito. Alle fargeverdier er hentet direkte fra kildenes datasett.
