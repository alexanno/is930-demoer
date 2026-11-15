#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["markdown-it-py"]
# ///
"""Bygger Canvas-siden for øvingene (pages/ovinger.html) fra ovinger.md.

Øvingene har nummererte lister med kodeblokker inni, som bygg.py ikke støtter.
Derfor brukes markdown-it-py (CommonMark), og HTML-en får samme innebygde
stiler og «smartdesigner»-ramme som de andre sidene. Kjør med:

    uv run bygg_ovinger.py
"""
import re
from pathlib import Path

from markdown_it import MarkdownIt

from bygg import PRE_STYLE, TABLE_STYLE, T, Ids

ROOT = Path(__file__).resolve().parent
KILDE = ROOT / "ovinger.md"
PAGES = ROOT / "pages"
GITHUB = "https://github.com/alexanno/is930-demoer/blob/main/modul-3/"
TITTEL = "Øvinger"

md = MarkdownIt("commonmark").enable("table")


def stil(h):
    """Legger innebygde stiler på HTML fra markdown-it, siden Canvas fjerner <style>."""
    h = re.sub(r'<pre><code class="language-\w+">', f'<pre style="{PRE_STYLE}"><code>', h)
    h = h.replace("<pre><code>", f'<pre style="{PRE_STYLE}"><code>')
    h = h.replace("<table>", f'<div style="overflow-x: auto;">\n<table border="1" cellpadding="6" style="{TABLE_STYLE}">')
    h = h.replace("</table>", "</table>\n</div>")
    h = h.replace("<thead>\n<tr>", '<thead>\n<tr style="background-color: rgba(0,0,0,0.08);">')
    h = h.replace("<th>", '<th style="text-align: left;">')
    h = h.replace("<blockquote>", '<blockquote style="margin: 8px 0 8px 8px; padding: 4px 14px; border-left: 4px solid rgba(128, 128, 128, 0.5);">')

    def lenke(m):
        url = m.group(1)
        if url.startswith(("http", "#")):
            mal = ' target="_blank"' if url.startswith("http") else ""
            return f'<a href="{url}"{mal}>'
        url = re.sub(r"^\.\./", "", url)
        base = GITHUB if not url.startswith("modul-") else GITHUB.replace("modul-3/", "")
        return f'<a href="{base}{url}" target="_blank">'

    return re.sub(r'<a href="([^"]+)">', lenke, h)


def deler(tekst):
    """Deler ovinger.md i (intro, [(tittel, innhold), ...])."""
    tekst = tekst.replace('<a id="data"></a>\n', "")
    tekst = re.sub(r"^# .*\n", "", tekst, count=1)
    biter, i_kode = [[]], False
    for linje in tekst.split("\n"):
        if linje.startswith("```"):
            i_kode = not i_kode
        if not i_kode and linje.startswith("## "):
            biter.append([linje[3:]])
        else:
            biter[-1].append(linje)
    intro = "\n".join(biter[0])
    seksjoner = []
    for b in biter[1:]:
        innhold = re.sub(r"\n---\s*$", "", "\n".join(b[1:]).strip())
        seksjoner.append((b[0].strip(), innhold.strip()))
    return intro.strip(), seksjoner


def bygg():
    intro, seksjoner = deler(KILDE.read_text(encoding="utf-8"))
    i, v = Ids("ov"), T
    kort = []
    for tittel, innhold in seksjoner:
        anker = ' id="data"' if tittel == "Data" else ""
        kort.append(f"""<div class="w-full md:min-w-72 min-w-auto mb-3 mt-3 rounded-2xl md:w-full p-3 md:mb-6 md:mt-6" data-component-id="cmmyu8nra00ymmy9yiuz0ulhd_15" id="{i()}" style="background-color: var({v}lwme);">
<div class="flex border flex-col rounded-2xl md:mt-0 md:mb-0 mb-0 mt-0 md:p-5 p-5 w-full" id="{i()}" style="border-color: transparent; background-color: var({v}ndju); color: var({v}plgs);">
<div class="flex-1" id="{i()}">
<h3 class="mt-2 mb-2"{anker}>{tittel}</h3>
<div class="mt-3 mb-3" data-component-type="rte" id="{i()}">
{stil(md.render(innhold))}
</div>
</div>
</div>
</div>""")
    side = f"""<!doctype html>
<html lang="no"><head><meta charset="utf-8">
<title>{TITTEL}</title></head>
<body>
<h1>{TITTEL}</h1>
<div class="_smartdesigner" data-template-id="cmpfeifoe001v3kta1pxa8gnn_50">
<div class="rounded-lg pl-3 mb-2 pr-3 pt-2 pb-2 mt-10" data-component-type="rte" id="{i()}" style="color: black; background-color: var({v}lwme);">
<h2 id="{i()}">{TITTEL}</h2>
</div>
<section class="flex flex-col flex-wrap md:flex-row items-center justify-evenly pt-0 pb-0 mb-7 mt-8 md:mb-8" id="{i()}" style="gap: 0 2rem;">
<div class="min-w-auto flex flex-col items-center md:items-start md:text-left justify-center md:p-0 mr-0 p-0 w-full flex-grow" id="{i()}">
<div class="mt-0 mr-0 md:mr-0 pr-0 pl-0 md:pr-0 mb-0" data-component-type="rte" id="{i()}" style="color: var({v}nlka);">
{stil(md.render(intro))}
</div>
</div>
</section>
{chr(10).join(kort)}
</div>
</body></html>
"""
    PAGES.mkdir(exist_ok=True)
    (PAGES / "ovinger.html").write_text(side, encoding="utf-8")
    print("bygget ovinger.html")


if __name__ == "__main__":
    bygg()
