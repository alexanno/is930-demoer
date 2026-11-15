# /// script
# requires-python = ">=3.11"
# dependencies = ["geopandas", "pyogrio"]
# ///
"""Sjekker at uv, Python og geopandas virker. Kjør med: uv run sjekk_oppsett.py"""
import sys
from pathlib import Path

import geopandas as gpd

data = Path(__file__).resolve().parents[2] / "modul-2" / "eksempeldata"
bygg = gpd.read_file(data / "bygg.gpkg")
brann = gpd.read_file(data / "brannstasjon.gpkg")

print(f"Python {sys.version.split()[0]}, geopandas {gpd.__version__}")
print(f"Leste {len(bygg)} bygg og {len(brann)} brannstasjoner i {bygg.crs}")

naermest = gpd.sjoin_nearest(bygg, brann, distance_col="avstand_m")
print(f"Median avstand til nærmeste brannstasjon: {naermest.avstand_m.median():.0f} m")
print("Oppsettet virker.")
