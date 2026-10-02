# IS930 Temasider

Samling av frittstående HTML-demoer til bruk i undervisning. [index.html](index.html)
lister alle demoene og genereres automatisk – rediger den ikke for hånd.

## Legge til en ny demo

Lag en ny toppnivå-mappe med en `index.html` (og gjerne en `README.md` med en
kort beskrivelse i første avsnitt), så plukkes den opp automatisk neste gang
`index.html` genereres.

## Oppdatere forsiden

Forsiden genereres av [generer_index.py](generer_index.py):

```
python3 generer_index.py
```

Dette skjer automatisk ved commit via en git-hook. Siden git-hooks ikke er
versjonskontrollert som standard, må hver som kloner repoet kjøre dette én
gang:

```
git config core.hooksPath githooks
```

Hooken ligger i [githooks/pre-commit](githooks/pre-commit).
