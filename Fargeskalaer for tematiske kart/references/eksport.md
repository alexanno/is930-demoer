# Eksportformater

Demoen eksporterer valgt skala og klasseantall i seks formater. Eksemplene bruker Blues med 3 klasser.

## Innhold

- [HEX](#hex) · [CSS](#css) · [CSS-variabler](#css-variabler) · [JSON](#json) · [JSON (komplett)](#json-komplett) · [Python](#python)

## HEX

```
#deebf7, #9ecae1, #3182bd
```

## CSS

```css
background: linear-gradient(90deg, #deebf7, #9ecae1, #3182bd);
```

## CSS-variabler

Navnet er skalanavnet i små bokstaver med bindestrek (`ag_GrnYl` → `ag-grnyl`).

```css
:root {
  /* Blues – sekvensiell (ColorBrewer), 3 klasser */
  --blues-1: #deebf7;
  --blues-2: #9ecae1;
  --blues-3: #3182bd;
}
```

Bruk: `el.style.setProperty('--blues-1', '#deebf7')`, `getComputedStyle(el).getPropertyValue('--blues-1')` eller `color: var(--blues-1)`.

## JSON

```json
["#deebf7", "#9ecae1", "#3182bd"]
```

## JSON (komplett)

```json
{
  "navn": "Blues",
  "kilde": "ColorBrewer",
  "type": "Sekvensiell",
  "kontinuerlig": false,
  "antall_klasser": 3,
  "fargeblind_trygg": true,
  "farger": ["#deebf7", "#9ecae1", "#3182bd"]
}
```

## Python

Variabelnavnet er skalanavnet med ikke-alfanumeriske tegn byttet med `_`.

```python
from matplotlib.colors import ListedColormap

Blues = ListedColormap([
    "#deebf7",
    "#9ecae1",
    "#3182bd"
])
```
