# Tilgjengelighet og fargesynsavvik

## Innhold

- [Bakgrunn](#bakgrunn)
- [CVD-trygg-merket](#cvd-trygg-merket)
- [Simulering](#simulering)
- [Skalaer merket CVD-trygge](#skalaer-merket-cvd-trygge)

## Bakgrunn

Rundt 8 % av menn og under 1 % av kvinner med nordeuropeisk bakgrunn har en form for fargesynsavvik (CVD), i de fleste tilfeller rød–grønn (protanopi/deuteranopi). Et kart som bare skiller klasser med rød–grønn-kontrast, er vanskelig å lese for denne gruppen. Unngå derfor skalaer som RdYlGn og Spectral når fargeblinde er en mulig målgruppe.

## CVD-trygg-merket

Merket kommer fra kildenes egne tester: RColorBrewers `colorblind`-liste og CARTOColors' «Safe»-palett. En skala uten merket er ikke nødvendigvis utrygg; den er bare ikke eksplisitt testet i kildedataene.

## Simulering

Demoen simulerer protanopi, deuteranopi og tritanopi med modellen til Machado, Oliveira & Fernandes (2009). Matrisene (rad for rad) multipliseres med lineær RGB (sRGB→lineær, matrise, lineær→sRGB):

```
protan: 0.152286  1.052583 -0.204868
        0.114503  0.786281  0.099216
       -0.003882 -0.048116  1.051998

deutan: 0.367322  0.860646 -0.227968
        0.280085  0.672501  0.047413
       -0.011820  0.042940  0.968881

tritan: 1.255528 -0.076749 -0.178779
       -0.078411  0.930809  0.147602
        0.004733  0.691367  0.303900
```

Simuleringen er kun visuell. Eksporterte fargekoder er alltid de ekte verdiene.

## Skalaer merket CVD-trygge

- Sekvensiell: alle ColorBrewer-sekvensene, samt Viridis, Magma, Inferno, Plasma og Cividis
- Divergerende: RdBu, PiYG, PRGn, RdYlBu, BrBG, PuOr
- Kvalitativ: Set2, Dark2, Paired, Safe (CARTOColors) og Okabe–Ito
