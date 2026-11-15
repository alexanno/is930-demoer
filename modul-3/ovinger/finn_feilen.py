# /// script
# requires-python = ">=3.11"
# dependencies = ["geopandas", "pyogrio", "matplotlib"]
# ///
"""Befolkning per kommune i Agder: tabell og kart. Kjør med: uv run finn_feilen.py"""
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt

HER = Path(__file__).resolve().parent
KOMMUNER = "https://raw.githubusercontent.com/robhop/fylker-og-kommuner/main/Kommuner-M.geojson"
RUTER = next(HER.glob("Befolkning_42_Agder*.gpkg"))

# Kommunegrenser (robhop/fylker-og-kommuner) for Agder, kommunenummer 42xx
kommuner = gpd.read_file(KOMMUNER)
kommuner = kommuner[kommuner["kommunenummer"].str.startswith("42")].reset_index(drop=True)

# Befolkning på 250 m-ruter (SSB) i EPSG:25833
ruter = gpd.read_file(RUTER)
print(f"Leste {len(kommuner)} kommuner og {len(ruter)} ruter med {ruter['poptot'].sum()} innbyggere")

# Hver rute får kommunen som ligger nærmest rutens midtpunkt
midtpunkt = ruter.assign(geometry=ruter.geometry.centroid)
grenser = kommuner[["kommunenummer", "kommunenavn", "geometry"]].to_crs(ruter.crs)
koblet = gpd.sjoin_nearest(midtpunkt, grenser)

# Summer befolkningen per kommune
befolkning = koblet.groupby("kommunenummer")["poptot"].sum().rename("befolkning")
kommuner = kommuner.merge(befolkning, on="kommunenummer", how="left").fillna({"befolkning": 0})
print(f"Befolkning fordelt på kommuner: {int(kommuner['befolkning'].sum())}")

# Areal og befolkningstetthet per kommune
kommuner["areal_km2"] = kommuner.geometry.area / 1e6
kommuner["tetthet"] = kommuner["befolkning"] / kommuner["areal_km2"]

tettest = kommuner.sort_values("tetthet", ascending=False).head(5)
print("\nFem tettest befolkede kommuner (innbyggere per km²):")
for _, k in tettest.iterrows():
    print(f"  {k['kommunenavn']:<15} {k['tetthet']:>12,.0f}")

# Kart over befolkning per kommune
fig, ax = plt.subplots(figsize=(9, 6))
kommuner.plot(column="befolkning", cmap="YlOrRd", edgecolor="white", linewidth=0.5, legend=True,
              legend_kwds={"label": "Innbyggere"}, ax=ax)
ax.set_title("Befolkning per kommune i Agder")
ax.set_axis_off()
fig.savefig(HER / "kart_befolkning.png", dpi=150, bbox_inches="tight")
print("\nKart lagret som kart_befolkning.png")
