#!/usr/bin/env bash
# Laster ned eksempeldata til data/ for ogr2ogr-demoen.
# Krever: gdal (ogr2ogr), curl og uv (for overturemaps-verktøyet).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data ut

# 1. Natural Earth: land i hele verden (ca. 200 kB)
curl -sL -o data/ne_land.zip \
  https://naturalearth.s3.amazonaws.com/110m_cultural/ne_110m_admin_0_countries.zip

# 2. GeoNorge (Kartverket): kommunegrenser rett fra WFS-tjenesten, lagret som GeoPackage
ogr2ogr -f GPKG -nlt PROMOTE_TO_MULTI -lco GEOMETRY_NAME=geom -select kommunenummer,kommunenavn \
  data/kommuner.gpkg -nln kommuner -overwrite \
  'WFS:https://wfs.geonorge.no/skwms1/wfs.administrative_enheter' app:Kommune

# 3. Overture Maps: bygninger og veger i Kristiansand sentrum (GeoParquet)
uvx overturemaps download --bbox=8.00,58.14,8.03,58.16 -f geoparquet --type=building -o data/bygg.parquet
uvx overturemaps download --bbox=8.00,58.14,8.03,58.16 -f geoparquet --type=segment  -o data/veger.parquet
rm -f data/*.state

echo "Ferdig:"; ls -lh data
