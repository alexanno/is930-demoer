"""Genererer eksempelbilder på tematiske kartmetoder, til bruk i undervisning.

Fem metoder illustreres:
  1. Choropleth        – befolkningstetthet per norsk fylke
  2. Proporsjonale sirkler – folketall per norsk fylke (samme data, annen metode)
  3. Dot density-kart   – befolkning i Agder-kommunene, disaggregert til prikker
  4. Dorling-kartogram  – folketall per fylke, areal fordreid etter verdi
  5. Heatmap (KDE)      – samme befolkningspunkter som dot density-kartet (Agder)

Punkt 1, 2 og 4 bruker samme datasett (folketall per fylke) for å vise hvordan
valg av metode endrer hva kartet kommuniserer, selv om dataene er identiske.
Punkt 3 og 5 bruker på samme måte identiske, disaggregerte befolkningspunkter
for Agder – én diskret (prikker) og én kontinuerlig (glattet tetthet) metode.

Datakilder (alle hentet live, ingen tall er hardkodet):
  - Kartverket/Geonorge kommuneinfo-API: fylke- og kommunegrenser
  - SSB tabell 01222: befolkning per fylke/kommune, siste tilgjengelige kvartal

Kjør:
    python3 -m venv .venv && source .venv/bin/activate
    pip install -r requirements.txt
    python3 generer_eksempler.py
"""

from __future__ import annotations

import math
import random
from pathlib import Path

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import requests
from matplotlib.colors import ListedColormap
from scipy.stats import gaussian_kde
from shapely.geometry import Point, shape

HER = Path(__file__).parent
BILDER = HER / "bilder"
BILDER.mkdir(exist_ok=True)

DPI = 150
plt.rcParams.update({"font.size": 11, "axes.titlesize": 14, "axes.titleweight": "bold"})

GEONORGE_KOMMUNEINFO = "https://ws.geonorge.no/kommuneinfo/v1"
SSB_TABELL_01222 = "https://data.ssb.no/api/v0/no/table/01222"

FYLKESNUMMER = {
    "31": "Østfold", "32": "Akershus", "03": "Oslo", "34": "Innlandet",
    "33": "Buskerud", "39": "Vestfold", "40": "Telemark", "42": "Agder",
    "11": "Rogaland", "46": "Vestland", "15": "Møre og Romsdal",
    "50": "Trøndelag", "18": "Nordland", "55": "Troms", "56": "Finnmark",
}


# ---------------------------------------------------------------------------
# Datainnhenting – alt hentes live fra offentlige API-er
# ---------------------------------------------------------------------------

def hent_fylkesgeometri() -> gpd.GeoDataFrame:
    """Henter ekte fylkesgrenser fra Geonorge, ett API-kall per fylke."""
    rader = []
    for nr in FYLKESNUMMER:
        resp = requests.get(f"{GEONORGE_KOMMUNEINFO}/fylker/{nr}/omrade", timeout=30)
        resp.raise_for_status()
        d = resp.json()
        rader.append({
            "fylkesnummer": nr,
            "fylkesnavn": d["fylkesnavn"],
            "geometry": shape(d["omrade"]),
        })
    return gpd.GeoDataFrame(rader, crs="EPSG:4326")


def hent_kommunegeometri(fylkesprefiks: str) -> gpd.GeoDataFrame:
    """Henter ekte kommunegrenser for alle kommuner i et gitt fylke (f.eks. '42' = Agder)."""
    resp = requests.get(f"{GEONORGE_KOMMUNEINFO}/kommuner", timeout=30)
    resp.raise_for_status()
    knrs = [k["kommunenummer"] for k in resp.json() if k["kommunenummer"].startswith(fylkesprefiks)]

    rader = []
    for knr in knrs:
        r = requests.get(f"{GEONORGE_KOMMUNEINFO}/kommuner/{knr}/omrade", timeout=30)
        r.raise_for_status()
        d = r.json()
        rader.append({
            "kommunenummer": knr,
            "kommunenavn": d["kommunenavn"],
            "geometry": shape(d["omrade"]),
        })
    return gpd.GeoDataFrame(rader, crs="EPSG:4326")


def hent_ssb_befolkning(regionkoder: list[str]) -> tuple[dict[str, int], str]:
    """Henter siste tilgjengelige kvartalsvise befolkningstall fra SSB tabell 01222.

    Returnerer (regionkode -> folketall, kvartal-tekst).
    """
    body = {
        "query": [
            {"code": "Region", "selection": {"filter": "item", "values": regionkoder}},
            {"code": "ContentsCode", "selection": {"filter": "item", "values": ["Folketallet11"]}},
            {"code": "Tid", "selection": {"filter": "top", "values": ["1"]}},
        ],
        "response": {"format": "json-stat2"},
    }
    r = requests.post(SSB_TABELL_01222, json=body, timeout=30)
    r.raise_for_status()
    d = r.json()
    indeks = d["dimension"]["Region"]["category"]["index"]
    kvartal = next(iter(d["dimension"]["Tid"]["category"]["label"].values()))
    verdier = {kode: d["value"][i] for kode, i in indeks.items()}
    return verdier, kvartal


def kilde(ax, tekst: str, farge: str = "#555555") -> None:
    ax.annotate(
        tekst, xy=(0.01, 0.01), xycoords="figure fraction",
        fontsize=7.5, color=farge,
    )


# CARTOColors "SunsetDark" (5 klasser) – mørkere og mer mettet i begge ender
# enn ColorBrewer YlOrRd, valgt med utgangspunkt i paletten til verktøyet
# "Fargeskalaer for tematiske kart" i samme repo.
SUNSETDARK_5 = ["#fcde9c", "#f58670", "#e34f6f", "#d72d7c", "#7c1d6f"]


# ---------------------------------------------------------------------------
# 1 + 2 + 4: tre metoder på samme datasett (folketall per fylke)
# ---------------------------------------------------------------------------

def forbered_fylkesdata() -> tuple[gpd.GeoDataFrame, str]:
    fylker = hent_fylkesgeometri()
    befolkning, kvartal = hent_ssb_befolkning(list(FYLKESNUMMER.keys()))
    fylker["befolkning"] = fylker["fylkesnummer"].map(befolkning)
    return fylker, kvartal


def lag_choropleth(fylker: gpd.GeoDataFrame, kvartal: str) -> None:
    fylker = fylker.to_crs(25833)
    fylker["areal_km2"] = fylker.geometry.area / 1e6
    fylker["tetthet"] = fylker["befolkning"] / fylker["areal_km2"]

    fig, ax = plt.subplots(figsize=(6.5, 9))
    fylker.plot(
        column="tetthet", scheme="Quantiles", k=5, cmap=ListedColormap(SUNSETDARK_5),
        linewidth=0.8, edgecolor="white", legend=True, ax=ax,
        legend_kwds={"title": "Innbyggere/km²", "fmt": "{:.1f}", "loc": "lower right",
                     "frameon": False, "title_fontsize": 9, "fontsize": 8},
    )
    ax.set_axis_off()
    ax.set_title(f"Choropleth\nBefolkningstetthet per fylke ({kvartal})")
    kilde(ax, "CARTOColors SunsetDark · klassifisert med kvantiler, 5 klasser (3 fylker/klasse). "
              "Kilde: Geonorge (fylkesgrenser) · SSB tabell 01222 (befolkning)")
    fig.savefig(BILDER / "01_choropleth.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def lag_proporsjonale_sirkler(fylker: gpd.GeoDataFrame, kvartal: str) -> None:
    fylker_25833 = fylker.to_crs(25833)
    sentroider = gpd.GeoSeries(fylker_25833.geometry.centroid, crs=25833).to_crs(4326)
    fylker_4326 = fylker.to_crs(4326)

    fig, ax = plt.subplots(figsize=(6.5, 9))
    fylker_4326.plot(ax=ax, facecolor="#eef2f3", edgecolor="#b0b0b0", linewidth=0.6)

    maks = fylker["befolkning"].max()
    SKALA = 2200  # punktareal (s) ved maks folketall
    # Ren matematisk areal-skalering (s ∝ verdi) brukes her, altså den
    # "riktige" baseline-metoden. I praksis undervurderer lesere gjerne
    # forskjellen mellom store sirkler (Stevens' maktlov), så enkelte
    # kartografer bruker i stedet en psykologisk/persepsjonskorrigert
    # skalering – såkalt "apparent magnitude"- eller Flannery-skalering,
    # se lenke i index.html / README.
    storrelser = fylker["befolkning"] / maks * SKALA
    ax.scatter(sentroider.x, sentroider.y, s=storrelser, color="#2b6cb0", alpha=0.65,
               edgecolor="white", linewidth=0.9, zorder=3)

    for ref_pop in (700_000, 300_000, 75_000):
        ax.scatter([], [], s=ref_pop / maks * SKALA, color="#2b6cb0", alpha=0.65,
                    edgecolor="white", label=f"{ref_pop:,}".replace(",", " "))
    ax.legend(title="Folketall", loc="lower right", labelspacing=1.8, frameon=False,
              fontsize=8, title_fontsize=9)

    ax.set_axis_off()
    ax.set_title(f"Proporsjonale sirkler\nFolketall per fylke ({kvartal})")
    kilde(ax, "Sirkelareal er proporsjonalt med folketall (ikke radius). "
              "Kilde: Geonorge (fylkesgrenser) · SSB tabell 01222 (befolkning)")
    fig.savefig(BILDER / "02_proporsjonale_sirkler.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


def lag_kartogram(fylker: gpd.GeoDataFrame, kvartal: str) -> None:
    fylker_25833 = fylker.to_crs(25833)
    sentroider = fylker_25833.geometry.centroid
    x = sentroider.x.to_numpy().copy()
    y = sentroider.y.to_numpy().copy()
    befolkning = fylker["befolkning"].to_numpy()
    navn = fylker["fylkesnavn"].to_numpy()

    maks_radius = 115_000.0  # meter, kun et visuelt skaleringsvalg
    r = np.sqrt(befolkning / befolkning.max()) * maks_radius

    # Enkel Dorling-kartogram-algoritme: flytt overlappende sirkler fra hverandre
    # iterativt til ingen overlapper lenger (eller til vi gir opp etter N runder).
    for _ in range(400):
        flyttet = False
        for i in range(len(x)):
            for j in range(i + 1, len(x)):
                dx, dy = x[j] - x[i], y[j] - y[i]
                avstand = math.hypot(dx, dy) or 1e-6
                min_avstand = r[i] + r[j] + 3000
                if avstand < min_avstand:
                    flyttet = True
                    overlapp = (min_avstand - avstand) / 2
                    ux, uy = dx / avstand, dy / avstand
                    x[i] -= ux * overlapp
                    y[i] -= uy * overlapp
                    x[j] += ux * overlapp
                    y[j] += uy * overlapp
        if not flyttet:
            break

    # Korte, unike koder brukes inni sirklene i stedet for fulle navn, siden
    # de minste fylkene (f.eks. Finnmark) har for liten sirkel til å vise hele
    # navnet uten at teksten klipper ut over sirkelkanten.
    KODER = {
        "Østfold": "ØF", "Akershus": "AK", "Oslo": "OS", "Innlandet": "IN",
        "Buskerud": "BU", "Vestfold": "VF", "Telemark": "TE", "Agder": "AG",
        "Rogaland": "RO", "Vestland": "VL", "Møre og Romsdal": "MR",
        "Trøndelag": "TR", "Nordland": "NO", "Troms": "TS", "Finnmark": "FI",
    }

    fig, ax = plt.subplots(figsize=(7.5, 9))
    fylker_25833.plot(ax=ax, facecolor="none", edgecolor="#cccccc", linewidth=0.6, zorder=1)
    for xi, yi, ri, na in zip(x, y, r, navn):
        ax.add_patch(plt.Circle((xi, yi), ri, facecolor="#2b6cb0", alpha=0.7,
                                 edgecolor="white", linewidth=0.8, zorder=2))
        ax.annotate(KODER[na], (xi, yi), ha="center", va="center", fontsize=8,
                    color="white", weight="bold", zorder=3, clip_on=False)

    # Avgrens etter de faktiske sirkelposisjonene (ikke de originale polygonene),
    # siden Dorling-algoritmen kan flytte sirkler et stykke fra sitt utgangspunkt.
    ax.set_xlim((x - r).min() - 15_000, (x + r).max() + 15_000)
    ax.set_ylim((y - r).min() - 15_000, (y + r).max() + 15_000)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(f"Dorling-kartogram\nFolketall per fylke ({kvartal})")

    par = list(KODER.items())
    linjer = ["   ".join(f"{k}={v}" for v, k in par[i:i + 5]) for i in range(0, len(par), 5)]
    ax.text(0.5, -0.03, "\n".join(linjer), ha="center", va="top", fontsize=7.5,
            color="#444444", transform=ax.transAxes, clip_on=False)
    kilde(ax, "Sirkelareal ∝ folketall; tynne linjer viser ekte fylkesgrenser til sammenligning. "
              "Kilde: Geonorge (fylkesgrenser) · SSB tabell 01222 (befolkning)")
    fig.savefig(BILDER / "04_kartogram.png", dpi=DPI, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------
# 3 + 5: Dot density og heatmap – samme punktdatasett for Agder, to metoder
# ---------------------------------------------------------------------------

PERSONER_PER_PRIKK = 150


def tilfeldige_punkter_i_polygon(polygon, n: int, rng: random.Random) -> list[Point]:
    """Enkel rejection sampling: kast punkter i boundingboksen, behold de som
    faktisk lander inni polygonet (slik at prikker ikke ender i fjorden)."""
    if n <= 0 or polygon.is_empty:
        return []
    minx, miny, maxx, maxy = polygon.bounds
    punkter = []
    forsok = 0
    makstall_forsok = max(n * 300, 2000)
    while len(punkter) < n and forsok < makstall_forsok:
        forsok += 1
        p = Point(rng.uniform(minx, maxx), rng.uniform(miny, maxy))
        if polygon.contains(p):
            punkter.append(p)
    return punkter


def hent_agder_befolkningspunkter() -> tuple[gpd.GeoDataFrame, list[Point], str]:
    """Henter ekte kommunegrenser + befolkning for Agder, og disaggregerer til
    punkter (1 punkt = PERSONER_PER_PRIKK innbyggere). Brukes som felles
    datagrunnlag for både dot density-kartet og heatmap-eksemplet, slik at de
    to metodene viser nøyaktig samme data på to forskjellige måter."""
    kommuner = hent_kommunegeometri("42")  # Agder
    befolkning, kvartal = hent_ssb_befolkning(list(kommuner["kommunenummer"]))
    kommuner["befolkning"] = kommuner["kommunenummer"].map(befolkning)
    kommuner = kommuner.to_crs(25833)

    rng = random.Random(42)
    alle_punkter: list[Point] = []
    for _, rad in kommuner.iterrows():
        n = max(1, round(rad["befolkning"] / PERSONER_PER_PRIKK))
        geom = rad.geometry
        deler = list(geom.geoms) if geom.geom_type == "MultiPolygon" else [geom]
        areal_sum = sum(d.area for d in deler) or 1.0
        for d in deler:
            n_del = round(n * d.area / areal_sum)
            alle_punkter += tilfeldige_punkter_i_polygon(d, n_del, rng)

    return kommuner, alle_punkter, kvartal


def lag_dotmap(kommuner: gpd.GeoDataFrame, punkter: list[Point], kvartal: str) -> None:
    MORK_BG = "#0d0d0f"

    fig, ax = plt.subplots(figsize=(7.5, 7))
    fig.patch.set_facecolor(MORK_BG)
    ax.set_facecolor(MORK_BG)
    kommuner.plot(ax=ax, facecolor=MORK_BG, edgecolor="#4a4a4a", linewidth=0.5)
    ax.scatter([p.x for p in punkter], [p.y for p in punkter],
               s=4, color="#7CFC9A", alpha=0.35, linewidth=0, zorder=3)

    ax.set_axis_off()
    ax.set_title(f"Dot density-kart\nBefolkning i Agder ({kvartal})", color="white")
    kilde(ax, f"1 prikk = {PERSONER_PER_PRIKK} innbyggere, tilfeldig plassert innenfor kommunegrensen. "
              "Kilde: Geonorge (kommunegrenser) · SSB tabell 01222 (befolkning)", farge="#aaaaaa")
    fig.savefig(BILDER / "03_dot_density.png", dpi=DPI, bbox_inches="tight", facecolor=MORK_BG)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 5: Heatmap / kernel density – samme Agder-punkter som dot density-kartet
# ---------------------------------------------------------------------------

def lag_heatmap(kommuner: gpd.GeoDataFrame, punkter: list[Point], kvartal: str) -> None:
    MORK_BG = "#0d0d0f"
    x = np.array([p.x for p in punkter])
    y = np.array([p.y for p in punkter])

    fig, ax = plt.subplots(figsize=(7.5, 7))
    fig.patch.set_facecolor(MORK_BG)
    ax.set_facecolor(MORK_BG)

    minx, miny, maxx, maxy = kommuner.total_bounds
    pad = 0.04 * max(maxx - minx, maxy - miny)
    xx, yy = np.mgrid[minx - pad:maxx + pad:300j, miny - pad:maxy + pad:300j]
    kde = gaussian_kde(np.vstack([x, y]), bw_method=0.12)
    zz = kde(np.vstack([xx.ravel(), yy.ravel()])).reshape(xx.shape)
    ax.contourf(xx, yy, zz, levels=30, cmap="inferno", zorder=2)
    kommuner.plot(ax=ax, facecolor="none", edgecolor="#777777", linewidth=0.5, zorder=3)

    ax.set_xlim(minx - pad, maxx + pad)
    ax.set_ylim(miny - pad, maxy + pad)
    ax.set_aspect("equal")
    ax.set_axis_off()
    ax.set_title(f"Heatmap (kernel density estimation)\nBefolkning i Agder ({kvartal})", color="white")
    kilde(ax, f"Samme {len(punkter)} befolkningspunkter som dot density-kartet (1 punkt = "
              f"{PERSONER_PER_PRIKK} innbyggere), vist som en glatt tetthetsoverflate. "
              "Kilde: Geonorge (kommunegrenser) · SSB tabell 01222 (befolkning)", farge="#aaaaaa")
    fig.savefig(BILDER / "05_heatmap.png", dpi=DPI, bbox_inches="tight", facecolor=MORK_BG)
    plt.close(fig)


# ---------------------------------------------------------------------------

def main() -> None:
    print("Henter fylkesdata (Geonorge + SSB) ...")
    fylker, kvartal = forbered_fylkesdata()

    print("Lager choropleth ...")
    lag_choropleth(fylker, kvartal)

    print("Lager proporsjonale sirkler ...")
    lag_proporsjonale_sirkler(fylker, kvartal)

    print("Lager Dorling-kartogram ...")
    lag_kartogram(fylker, kvartal)

    print("Henter befolkningspunkter for Agder (Geonorge + SSB) ...")
    kommuner, punkter, agder_kvartal = hent_agder_befolkningspunkter()

    print("Lager dot density-kart (Agder) ...")
    lag_dotmap(kommuner, punkter, agder_kvartal)

    print("Lager heatmap (Agder, samme punkter som dot density) ...")
    lag_heatmap(kommuner, punkter, agder_kvartal)

    print(f"Ferdig. Bilder lagret i {BILDER}/")


if __name__ == "__main__":
    main()
