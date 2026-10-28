#!/bin/bash
# Starter QGIS med forenklet grensesnitt og åpner Verdenskart (befolkning).
# Bruker en egen profil ("skole"), så vanlig QGIS-oppsett på maskinen røres ikke.
DIR="$(cd "$(dirname "$0")" && pwd)"
QGIS_APP="${QGIS_APP:-$(ls -d /Applications/QGIS*.app 2>/dev/null | sort -V | tail -1)}"
if [ -z "$QGIS_APP" ]; then
  osascript -e 'display dialog "Fant ikke QGIS i Programmer-mappen. Installer QGIS fra qgis.org." buttons {"OK"} with icon stop'
  exit 1
fi
BIN="$QGIS_APP/Contents/MacOS/QGIS"
[ -x "$BIN" ] || BIN="$QGIS_APP/Contents/MacOS/qgis"
nohup "$BIN" --profile skole --code "$DIR/oppsett.py" "$DIR/verdenskart-befolkning.qgz" >/dev/null 2>&1 &
exit 0
