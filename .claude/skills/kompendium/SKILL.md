---
name: kompendium
description: Lag eller oppdater IS-930-kompendiet (kompendium/index.html) fra kildene i repoet: Canvas-temasidene i canvas-kopi/pages, forelesningsslides i slides_forelesninger og modulkildene (modul-2, modul-3). Bruk når brukeren ber om å oppdatere, utvide eller bygge kompendiet, eller har lagt til nye slides, temasider eller kilder.
---

# Kompendium IS-930

`kompendium/index.html` er én selvstendig HTML-fil (norsk bokmål, CSS inline, print-vennlig). Den er en tematisk sammenfatning av kursstoffet, ikke en kopi av Canvas. **Les filen først** og følg stilen og strukturen som allerede finnes. Ikke bygg den på nytt fra bunnen.

## Kilder (alle må sjekkes hver gang)

1. **Temasider:** `canvas-kopi/pages/*.html`. `canvas-kopi/manifest.json` har `updated_at` per side. Ignorer `*-kladd.html`.
2. **Forelesningsslides:** `slides_forelesninger/Forelesning N - dato.pdf` (foretrekk PDF, `pdftotext -layout`). Finnes bare `.pptx`, pakk ut tekst med `unzip -p fil.pptx 'ppt/slides/slide*.xml'` og fjern tagger. Slides kan inneholde stoff som ikke står på Canvas.
3. **Modulkilder:** `modul-2/kilde`, `modul-3/kilde` og `modul-3/agenda.md`.
4. **Demoer i repoet** (mapper med `index.html`, f.eks. `AIS-eksempel`, `Tabell eller kart`) lenkes som demo-bokser.
5. **Nye kilder brukeren nevner** (URL-er, filer): hent dem og legg dem i riktig kapittel.

## Arbeidsgang

1. **Finn hva som er nytt.** Sammenlign mot forrige kompendiumversjon:
   `git log -1 --format=%cI -- kompendium/index.html`, deretter `git status`, `git log --since=<dato> --name-only` og `updated_at` i manifestet. Slides som ikke er nevnt i forordet/kurstabellen regnes som nye. Rapporter listen over nye/endrede kilder til brukeren før du skriver.
2. **Les de nye/endrede kildene i sin helhet.** Ikke gjett fra filnavn.
3. **Plasser stoffet tematisk.** Ordne etter tema, ikke etter modul eller forelesning. Utvid et eksisterende kapittel når temaet finnes. Nytt kapittel (`id="kN"`) bare når temaet ikke passer noe sted. Hold nummerering, innholdsfortegnelse (`nav#toc`), figurnummer («Figur N.») og kryssreferanser konsistente. Nytt kapittel plasseres der det hører tematisk hjemme og resten renummereres.
4. **Skill kilde fra utdypning.** Stoff fra Canvas og slides skrives som vanlig tekst. Stoff som verken står på Canvas eller i slides, hentet fra nett (WebSearch/WebFetch, helst primærkilder), legges i `<div class="web"><span class="t">Utdypning fra nett</span>…</div>` med lenke i kapitlets kildeliste og i «Tilleggskilder fra nett». Ikke finn på lenker eller fakta. Sjekk det du siterer.
5. **Hold kapittelmalen:**
   - `<h2 id="kN">`, deretter `div.sammendrag` («Kort sagt», 3–4 punkter)
   - `<h3>N.M …</h3>`-seksjoner med tekst, `div.tablewrap > table`, `pre><code>` for kode, `figure` (inline SVG med `class="fig"`, eller bilde fra `kompendium/bilder/` med `figcaption`) og `div.demo` for demoer
   - avslutt med `div.kilder` («Canvas: «…», Slides: «Forelesning N», Nett: …»)
6. **Oppdater helheten:** forordet (hvilke moduler/forelesninger kompendiet dekker, fjern «ikke med ennå»-formuleringer som ikke lenger stemmer), ordlisten (`dl.gloss`, alfabetisk), «Litteratur og kilder» og kurstabellen i vedlegget om datoer har endret seg.
7. **Konsistens:** Ved motsigelser mellom Canvas og slides, vis begge og si fra til brukeren. Nyeste kilde gjelder normalt, men avgjør ikke i det stille.

## Sjekk før du er ferdig

- Alle `href="#…"` i innholdsfortegnelsen peker på en eksisterende `id`, og `id`-er er unike.
- Figurnummer er fortløpende, og SVG-markør `id="pil"` er ikke i konflikt (gjenbruk er eksisterende praksis).
- Relative lenker til demoer og `bilder/` virker (`ls`).
- Fungerer i mørk modus (bruk CSS-variablene, ikke faste farger i ny tekst/tabeller).
- Åpne eller sjekk at HTML-en er velformet, f.eks. `python3 -c "import html.parser,sys;html.parser.HTMLParser().feed(open('kompendium/index.html').read())"`.

Avslutt med en kort oppsummering: hvilke kilder som ble lest, hvilke kapitler som ble endret/lagt til, og hva som er åpent (motsigelser, kilder som ikke kunne hentes). Commit bare hvis brukeren ber om det.
