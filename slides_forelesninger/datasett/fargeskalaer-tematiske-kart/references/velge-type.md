# Velge type, antall klasser og skala

## Innhold

- [Hvilken type?](#hvilken-type)
- [Hvor mange klasser?](#hvor-mange-klasser)
- [Perseptuell jevnhet: hvorfor ikke regnbuen?](#perseptuell-jevnhet-hvorfor-ikke-regnbuen)

## Hvilken type?

**Sekvensiell** brukes når dataene har en naturlig rekkefølge fra lav til høy: befolkningstetthet, inntekt, temperatur, andel i prosent. Skalaen går typisk fra lys til mørk i én eller to beslektede fargetoner, slik at «mer» alltid oppfattes som «mørkere» eller «sterkere».

**Divergerende** brukes når dataene har et meningsfullt midtpunkt: avvik fra et gjennomsnitt, endring fra ett år til et annet, flertall for/mot. To kontrasterende farger møtes i en nøytral, lys midtfarge, slik at retningen (over/under midtpunktet) er det første man leser av kartet.

**Kvalitativ** brukes til kategorier uten rangering: arealbruk, kommunetype, administrative inndelinger. Fargene bør være lette å skille fra hverandre, men ingen av dem skal oppfattes som «mer» eller «mindre» enn de andre.

Velger man feil familie, forteller kartet en historie dataene ikke har, for eksempel at to kategorier ser ut til å ligge på en skala, eller at et nøytralt avvik ser ut som en lav verdi.

## Hvor mange klasser?

Brewer og Harrowers anbefalinger (og ColorBrewer-verktøyet selv) peker på at de fleste lesere ikke klarer å skille mer enn **5–7 klasser** pålitelig på et choroplethkart, selv om ColorBrewers skalaer tilbyr opptil 9–12 farger. Flere klasser gir finere oppløsning, men gjør kartet vanskeligere å lese raskt og øker sjansen for at naboklasser forveksles, spesielt i trykk eller for lesere med fargesynsavvik.

Antall klasser er begrenset til det kilden har definert:

- ColorBrewer sekvensiell: 3–9 (YlOrRd: 3–8)
- ColorBrewer divergerende: 3–11
- ColorBrewer kvalitativ: 3–8, 3–9 eller 3–12 avhengig av skala
- CARTOColors sekvensiell og divergerende: 2–7; kvalitativ: 2–11
- Viridis-familien: kontinuerlig, vilkårlig antall (verktøyet tilbyr 3–11)
- Okabe–Ito: 2–8

## Perseptuell jevnhet: hvorfor ikke regnbuen?

Klassiske regnbue-/jet-skalaer (blå→grønn→gul→rød) oppfattes ikke som jevnt fordelt av øyet. Enkelte overganger (gul→grønn) virker nesten like, mens andre (blå→cyan) virker som et stort sprang, selv om datasprangene er like. Det gir falske «grenser» i kartet som ikke finnes i dataene.

**Viridis-familien** (Viridis, Magma, Inferno, Plasma, Cividis), utviklet for matplotlib, er konstruert slik at lysstyrken øker jevnt gjennom hele skalaen. De er perseptuelt jevne, lesbare i gråtoneutskrift og, siden de følger én lysstyrkebane, i stor grad trygge for fargesynsavvik. De har blitt en uformell standard i vitenskapelig visualisering.
