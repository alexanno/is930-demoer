#!/usr/bin/env python3
"""Setter sammen Canvas-sider for Modul 2.

Leser kilde/*.md (enkel markdown med @@-seksjoner) og skriver ferdige
HTML-sider til pages/. Malen følger sidene i canvas-kopi/pages/
(Canvas «smartdesigner»). Bruker bare standardbiblioteket:

    python3 bygg.py            # bygg alle sider
    python3 bygg.py arkitekturer   # bygg én side (slug)

Kildeformat (kilde/<slug>.md):

    @@ intro        kort introduksjon (avsnitt)
    @@ innhold      markdown: #### overskrifter, avsnitt, - lister, | tabeller |,
                    ``` kodeblokker ```, {{flow: A // tekst | B | C ~ figurtekst}}
    @@ aktivitet    - punktliste
    @@ utvalgt      - punktliste (litteratur)
    @@ interessert  - punktliste (litteratur)
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KILDE = ROOT / "kilde"
PAGES = ROOT / "pages"

# (slug, tittel, id-prefiks)
TEMA = [
    ("verktoylandskapet", "Verktøylandskapet", "vl"),
    ("geografiske-operasjoner", "Geografiske operasjoner", "go"),
    ("desktop-web-og-serverprogramvare", "Desktop, web og serverprogramvare", "pv"),
    ("databaser-og-lagring", "Databaser og lagring", "db"),
    ("cli-og-biblioteker", "CLI og biblioteker", "cb"),
    ("arkitekturer", "Arkitekturer", "ar"),
    ("datakvalitet-og-metadata", "Datakvalitet og metadata", "dk"),
    ("ki-agenter-og-stack-valg", "KI-agenter og stack-valg", "ks"),
]
MODUL_SLUG = "modul-2-geografisk-databehandling-og-teknologi"
MODUL_TITTEL = "Modul 2: Geografisk databehandling og teknologi"

T = "--sd-cmh3doa2r001d2e1fu32oz11u-"   # fargevariabler, temasider
M = "--sd-cmgt9orvp009xjedjnjwe2uhk-"   # fargevariabler, modulside
CANVAS = "https://uia.instructure.com/courses/21461/pages/"
ICON = "https://www.uia.no/intranett/arbeidsstotte/undervisningsstotte/canvas/canvas-design-bilder/ikoner-med-ramme/"


# ---------------------------------------------------------------- inline
def inline(s):
    """Inline markdown: `kode`, **fet**, *kursiv*, [tekst](url)."""
    codes = []

    def keep(m):
        codes.append("<code>" + html.escape(m.group(1), quote=False) + "</code>")
        return f"\x00{len(codes) - 1}\x00"

    s = re.sub(r"`([^`]+)`", keep, s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![\*\w])\*([^*\n]+)\*(?![\*\w])", r"<em>\1</em>", s)

    def link(m):
        url = m.group(2)
        if url.startswith("side:"):  # intern lenke til en Canvas-side (slug)
            url = CANVAS + url[len("side:"):]
        url = re.sub(r"&(?!amp;)", "&amp;", url)
        target = ' target="_blank"' if url.startswith("http") else ""
        return f'<a href="{url}"{target}>{m.group(1)}</a>'

    s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, s)
    return re.sub(r"\x00(\d+)\x00", lambda m: codes[int(m.group(1))], s)


# ---------------------------------------------------------------- blokker
PRE_STYLE = ("overflow-x: auto; padding: 10px; border-width: 1px; border-style: solid; "
             "border-color: rgba(128, 128, 128, 0.5); border-radius: 8px;")
TABLE_STYLE = "border-collapse: collapse; width: 100%;"


def table(lines):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in lines]
    head, body = rows[0], rows[2:]
    out = ['<div style="overflow-x: auto;">',
           f'<table border="1" cellpadding="6" style="{TABLE_STYLE}">', "<thead>",
           '<tr style="background-color: rgba(0,0,0,0.08);">']
    out += [f'<th style="text-align: left;">{inline(c)}</th>' for c in head]
    out += ["</tr>", "</thead>", "<tbody>"]
    for r in body:
        out.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
    out += ["</tbody>", "</table>", "</div>"]
    return "\n".join(out)


def flow(spec):
    """{{flow: A // tekst | B | C ~ figurtekst}}"""
    caption = ""
    if "~" in spec:
        spec, caption = spec.rsplit("~", 1)
    boxes = []
    for part in spec.split("|"):
        title, _, sub = part.strip().partition("//")
        sub = f'<br/><span style="font-size: 0.85em;">{inline(sub.strip())}</span>' if sub else ""
        boxes.append('<td style="vertical-align: middle; padding: 10px; border-radius: 10px; '
                     'background-color: rgba(128, 128, 128, 0.15); border: 2px solid currentcolor;">'
                     f"<strong>{inline(title.strip())}</strong>{sub}</td>")
    cells = '<td style="font-size: 1.5em; vertical-align: middle; padding: 0 6px;">→</td>'.join(boxes)
    out = ['<div style="overflow-x: auto; margin: 16px 0;">',
           '<table cellpadding="0" cellspacing="0" style="border-collapse: separate; margin: 0 auto; text-align: center;">',
           f"<tbody><tr>{cells}</tr></tbody>", "</table>"]
    if caption.strip():
        out.append(f'<p style="text-align: center; font-size: 0.9em; margin-top: 8px;"><em>{inline(caption.strip())}</em></p>')
    out.append("</div>")
    return "\n".join(out)


def bullets(lines):
    """Punktlister med ett undernivå (to mellomrom innrykk). «1.» gir nummerert liste."""
    items = []
    for l in lines:
        m = re.match(r"^(\s*)(-|\d+\.)\s+(.*)$", l)
        if m:
            items.append([1 if len(m.group(1)) >= 2 else 0, m.group(3), m.group(2) != "-"])
        elif items and l.strip():
            items[-1][1] += " " + l.strip()
    tag = "ol" if items[0][2] else "ul"
    out, k = [f"<{tag}>"], 0
    while k < len(items):
        li = f"<li>{inline(items[k][1])}"
        k += 1
        sub = []
        while k < len(items) and items[k][0] == 1:
            sub.append(f"<li>{inline(items[k][1])}</li>")
            k += 1
        if sub:
            li += "\n<ul>\n" + "\n".join(sub) + "\n</ul>\n"
        out.append(li + "</li>")
    out.append(f"</{tag}>")
    return "\n".join(out)


def markdown(text):
    lines = text.split("\n")
    out, i = [], 0
    while i < len(lines):
        l = lines[i]
        if not l.strip():
            i += 1
        elif l.startswith("```"):
            j = i + 1
            while not lines[j].startswith("```"):
                j += 1
            code = html.escape("\n".join(lines[i + 1:j]), quote=False)
            out.append(f'<pre style="{PRE_STYLE}"><code>{code}</code></pre>')
            i = j + 1
        elif l.startswith("####"):
            out.append(f"<h4>{inline(l.lstrip('# ').strip())}</h4>")
            i += 1
        elif l.startswith("{{flow:"):
            out.append(flow(l[len("{{flow:"):].rstrip().removesuffix("}}")))
            i += 1
        elif l.startswith("|"):
            j = i
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            out.append(table(lines[i:j]))
            i = j
        elif re.match(r"^\s*(-|\d+\.)\s", l):
            j = i
            while j < len(lines) and lines[j].strip() and (re.match(r"^\s*(-|\d+\.)\s", lines[j]) or lines[j].startswith("  ")):
                j += 1
            out.append(bullets(lines[i:j]))
            i = j
        elif l.startswith("<"):
            out.append(l)
            i += 1
        else:
            j = i
            while j < len(lines) and lines[j].strip() and not re.match(r"^(\s*(-|\d+\.)\s|\||####|```|\{\{|<)", lines[j]):
                j += 1
            out.append(f"<p>{inline(' '.join(x.strip() for x in lines[i:j]))}</p>")
            i = j
    return "\n".join(out)


def parse(path):
    sec, cur = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        m = re.match(r"^@@ (\w+)\s*$", line)
        if m:
            cur = m.group(1)
            sec[cur] = []
        elif cur:
            sec[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in sec.items()}


class Ids:
    def __init__(self, prefix):
        self.p, self.n = prefix, 0

    def __call__(self):
        self.n += 1
        return f"{self.p}{self.n:02d}"


# ---------------------------------------------------------------- temaside
def litteratur_boks(i, c1, c2, v, cid_ref):
    return f"""<div class="flex flex-col relative pl-5 pb-6 border-2 pt-10 pr-5 rounded-2xl mb-6 mt-16 w-full ml-0 mr-0" data-component-id="cm0ccc7x20005qq7zncbedcn3_9" id="{i()}" style="background-color: transparent; border-color: var({v}nlka);">
<div class="absolute m-0 rounded-full w-16 h-16" id="{i()}" style="max-width: 100px; top: -32px; left: 2rem; background-color: var({v}ndju);"><img alt="" class="md:p-0 p-0 md:m-0 m-0 rounded-full w-16 bg-contain bg-center bg-no-repeat object-contain object-center h-16 md:border-0 border-0" data-api-endpoint="https://uia.instructure.com/api/v1/files/2628672" data-api-returntype="File" id="{i()}" loading="lazy" src="{ICON}litteratur_ramme.svg" style="border-color: var({v}pkhs);"/></div>
<div class="flex items-center mb-2 mt-0 md:p-0 pt-0 pl-0 w-full" id="{i()}">
<h3 class="mce-content-body mce-edit-focus md:border-0 border-0 md:m-0 mt-0 md:p-0 pt-0 w-full" id="{i()}" style="position: relative;"><span id="{i()}">Litteratur</span></h3>
</div>
<span class="inline-block pt-1 pb-1 pl-2 pr-2 rounded !bg-opacity-10 text-xs tracking-widest uppercase mb-1 w-40" id="{i()}" style="background-color: var({v}jdvv); color: var({v}bzai);"><span id="{i()}" style="color: var({v}hdbb);"><strong id="{i()}"><span id="{i()}">UTVALGT</span></strong></span></span>
<div class="m-0 p-0" data-component-type="rte" id="{i()}">
{c1}
</div>
<span class="inline-block pt-1 pb-1 pl-2 pr-2 rounded !bg-opacity-10 text-xs tracking-widest uppercase mb-1 w-40 mt-2" id="{i()}" style="background-color: var({v}wcil); color: var({v}jfnw);"><span id="{i()}"><strong id="{i()}"><span id="{i()}">Hvis interessert</span></strong></span></span>
<div class="m-0 p-0" data-component-type="rte" id="{i()}">
{c2}
</div>
</div>"""


def tema_side(slug, tittel, prefix):
    s = parse(KILDE / f"{slug}.md")
    i, v = Ids(prefix), T
    aktivitet = bullets(s["aktivitet"].split("\n"))
    page = f"""<!doctype html>
<html lang="no"><head><meta charset="utf-8">
<title>{tittel}</title></head>
<body>
<h1>{tittel}</h1>
<div class="_smartdesigner" data-template-id="cmpfeifoe001v3kta1pxa8gnn_50">
<div class="rounded-lg pl-3 mb-2 pr-3 pt-2 pb-2 mt-10" data-component-id="cmm0a4b4g00l5my9y9x0arybn_12" data-component-type="rte" id="{i()}" style="color: black; background-color: var({v}lwme);">
<h2 id="{i()}">{tittel}</h2>
</div>
<section class="flex flex-col flex-wrap md:flex-row items-center justify-evenly pt-0 pb-0 mb-7 mt-8 md:mb-8" data-component-id="cmo15xe7t0198my9yrwiw5weu_5" id="{i()}" style="gap: 0 2rem;">
<div class="min-w-auto flex flex-col items-center md:items-start md:text-left justify-center md:p-0 mr-0 p-0 w-full flex-grow" id="{i()}">
<div class="mt-0 mr-0 md:mr-0 pr-0 pl-0 md:pr-0 mb-0" data-component-type="rte" id="{i()}" style="color: var({v}nlka);">
{markdown(s["intro"])}
</div>
</div>
</section>
<div class="w-full md:min-w-72 min-w-auto mb-3 mt-3 rounded-2xl md:w-full p-3 md:mb-6 md:mt-6" data-component-id="cmmyu8nra00ymmy9yiuz0ulhd_15" id="{i()}" style="background-color: var({v}lwme);">
<div class="flex border flex-col rounded-2xl md:mt-0 md:mb-0 mb-0 mt-0 md:p-5 p-5 w-full" id="{i()}" style="border-color: transparent; background-color: var({v}ndju); color: var({v}plgs);">
<div class="flex-1" id="{i()}">
<h3 class="mt-2 mb-2" id="{i()}">Innhold</h3>
<div class="mt-3 mb-3" data-component-type="rte" id="{i()}">
{markdown(s["innhold"])}
</div>
</div>
</div>
</div>
<section class="flex md:flex-row flex-col flex-wrap justify-evenly p-0 mb-5 md:p-0" data-component-id="cmm08sjke00l2my9ymxuxjfwh_9" data-component-type="grid-row" id="{i()}">
<div class="flex flex-grow md:w-6/12 w-full md:min-w-80 pl-2 pr-2" data-component-type="grid-column" id="{i()}">
<div class="flex flex-col relative pl-5 pb-6 border-2 pt-10 pr-5 rounded-2xl mb-6 mt-16 w-full ml-0 mr-0" data-component-id="cm0cco1ip000bqq7zn28mcpzx_5" id="{i()}" style="background-color: transparent; border-color: var({v}nlka);">
<div class="absolute m-0 rounded-full w-16 h-16" id="{i()}" style="max-width: 100px; top: -32px; left: 2rem; background-color: var({v}ndju);"><img alt="" class="md:p-0 p-0 md:m-0 m-0 bg-contain bg-center bg-no-repeat object-contain object-center w-16 h-16 rounded-full md:border-0 border-0" data-api-endpoint="https://uia.instructure.com/api/v1/files/2639266" data-api-returntype="File" id="{i()}" loading="lazy" src="{ICON}aktivitet_ramme.svg" style="border-radius: 50%; border-color: var({v}pkhs);"/></div>
<div class="flex items-center mb-2 mt-0 md:p-0 pt-0 pl-0 w-full" id="{i()}">
<h3 class="mce-content-body mce-edit-focus md:border-0 border-0 md:m-0 mt-0 md:p-0 pt-0 w-full" id="{i()}" style="position: relative;"><span id="{i()}">Aktivitet</span></h3>
</div>
<div class="p-0 mt-0" data-component-type="rte" id="{i()}">
<p id="{i()}">Forslag til øvelser du kan prøve på egenhånd:</p>
{aktivitet}
</div>
</div>
</div>
<div class="flex flex-grow md:w-6/12 w-full md:min-w-80 pl-2 pr-2" data-component-type="grid-column" id="{i()}">
{litteratur_boks(i, bullets(s["utvalgt"].split(chr(10))), bullets(s["interessert"].split(chr(10))), v, None)}
</div>
</section>
</div>
</body></html>
"""
    (PAGES / f"{slug}.html").write_text(page, encoding="utf-8")
    return page


# ---------------------------------------------------------------- modulside
def agenda_tabell(text):
    rows = [[c.strip() for c in l.strip().strip("|").split("|")] for l in text.split("\n") if l.startswith("|")]
    head, body = rows[0], rows[2:]
    w = ["15%", "9%", "17%", "13%", "46%"]
    out = ['<div style="overflow-x: auto;">',
           '<table style="width: 100%; border-collapse: collapse; font-size: 15px;">', "<thead>",
           '<tr style="background-color: #1f2d3d; color: #ffffff; text-align: left;">']
    out += [f'<th scope="col" style="padding: 12px 14px; width: {w[k]}; border: 1px solid #1f2d3d;">{h}</th>' for k, h in enumerate(head)]
    out += ["</tr>", "</thead>", "<tbody>"]
    n = 0
    for r in body:
        pause = r[2].lower() in ("pause", "lunsj")
        if pause:
            st = "background-color: #eef1f3; color: #5b6770; font-style: italic;"
        else:
            st = "background-color: " + ("#f5f7f8" if n % 2 == 0 else "#ffffff") + ";"
            n += 1
        cells = []
        for k, c in enumerate(r):
            c = inline(c)
            if k == 2 and not pause:
                c = f"<strong>{c}</strong>"
            cells.append(f'<td style="padding: 10px 14px; vertical-align: top; width: {w[k]}; border: 1px solid #c7cdd1;">{c}</td>')
        out.append(f'<tr style="{st}">' + "".join(cells) + "</tr>")
    out += ["</tbody>", "</table>", "</div>"]
    return "\n".join(out)


def modulside():
    s = parse(KILDE / "modulside.md")
    i, v = Ids("m2"), M
    toc = [l.split("|") for l in s["toc"].split("\n") if l.strip()]  # slug|tittel|motivasjon
    toc_ol = "\n".join(f'<li><a href="#{a.strip()}">{b.strip()}</a></li>' for a, b, c in toc)
    toc_ol += '\n<li><a href="#oppsummering">Oppsummering og videre lesing</a></li>'
    blokker = []
    for n, (a, b, c) in enumerate(toc, 1):
        a, b, c = a.strip(), b.strip(), c.strip()
        blokker.append(f"""<h3 id="{a}">{n}. {b}</h3>
<p>{inline(c)}</p>
<p><a href="{CANVAS}{a}">Åpne temasiden: {b}</a> · <a href="#toc">↑ Tilbake til innholdsfortegnelsen</a></p>""")
    blokker.append(f"""<h3 id="oppsummering">Oppsummering og videre lesing</h3>
{markdown(s["oppsummering"])}
<p><a href="#toc">↑ Tilbake til innholdsfortegnelsen</a></p>""")
    tema_blokker = "\n".join(blokker)
    page = f"""<!doctype html>
<html lang="no"><head><meta charset="utf-8">
<title>{MODUL_TITTEL}</title></head>
<body>
<h1>{MODUL_TITTEL}</h1>
<div class="_smartdesigner" data-template-id="cmp6pgjoj006gcuh6negcf7yi_43">
<header class="w-full flex items-center justify-center relative overflow-hidden mb-6" data-component-type="absolute-header" id="{i()}"><img alt="" class="w-full bg-scroll object-center bg-cover rounded-2xl h-56 bg-center" data-component-type="img-with-bg-img" id="{i()}" loading="lazy" role="presentation" src="https://d37iccs1g8grfy.cloudfront.net/assets/transparent-src.png" style="background-image: linear-gradient(90deg, color-mix(in srgb, var({v}btus), transparent 80%), color-mix(in srgb, var({v}btus), transparent 80%)), url('https://images.unsplash.com/photo-1521295121783-8a321d551ad2?crop=entropy&amp;cs=tinysrgb&amp;fit=max&amp;fm=jpg&amp;ixid=M3wzMzgxNjF8MHwxfHNlYXJjaHwxMXx8aW1taWdyYXRpb258ZW58MHx8fHwxNzc1NTc1MTE1fDA&amp;ixlib=rb-4.1.0&amp;q=80&amp;w=1080');"/></header>
<div class="mb-3 mt-3" data-component-type="rte" id="{i()}" style="color: var({v}nlka);">
<h1 id="{i()}">{MODUL_TITTEL}</h1>
{markdown(s["intro"])}
</div>
<div class="flex flex-col relative pl-5 pb-6 border-2 pt-10 pr-5 rounded-2xl mb-6 mt-16 ml-0 mr-0 w-full" id="{i()}" style="background-color: transparent; border-color: var({v}nlka);">
<div class="absolute m-0 rounded-full w-16 h-16" id="{i()}" style="max-width: 100px; top: -32px; left: 2rem; background-color: var({v}ndju);"><img alt="" class="md:p-0 p-0 md:m-0 m-0 md:border-0 border-0 bg-contain bg-center bg-no-repeat object-contain object-center w-16 h-16" data-api-endpoint="https://uia.instructure.com/api/v1/files/3301895" data-api-returntype="File" id="{i()}" loading="lazy" src="{ICON}leringsmal_ramme2.svg"/></div>
<div class="flex items-center mb-2 mt-0 md:p-0 pt-0 pl-0" id="{i()}">
<h3 class="md:border-0 border-0 md:m-0 mt-0 md:p-0 pt-0 w-full" id="{i()}"><span id="{i()}">Etter denne modulen kan du</span></h3>
</div>
<div class="p-0 mt-0" data-component-type="rte" id="{i()}">
{markdown(s["laeringsmaal"])}
</div>
</div>
<div class="border border-0 pr-6 pl-6 pb-6 pt-4 w-full rounded-2xl ml-0 mr-0 md:ml-0 md:mr-0 mt-8 mb-8" id="{i()}" style="border-color: transparent; background-color: var({v}lwme); color: var({v}hwjc);">
<h2 class="mt-2 mb-2" id="{i()}">Agenda</h2>
<div class="mt-3 mb-3" data-component-type="rte" id="{i()}">
<p>{inline(s["agendatekst"])}</p>
{agenda_tabell(s["agenda"])}
</div>
</div>
<div class="border border-0 pr-6 pl-6 pb-6 pt-4 w-full rounded-2xl ml-0 mr-0 md:ml-0 md:mr-0 mt-8 mb-8" id="{i()}" style="border-color: transparent; background-color: var({v}lwme); color: var({v}hwjc);">
<h2 class="mt-2 mb-2" id="toc">Innhold i modulen</h2>
<div class="mt-3 mb-3" data-component-type="rte" id="{i()}">
<p>Under finner du hvert tema med en kort motivasjon for hvorfor det er viktig. Hopp direkte til et tema, og bruk lenken tilbake for å komme til innholdsfortegnelsen igjen.</p>
<ol>
{toc_ol}
</ol>
</div>
</div>
<section class="flex flex-col w-full min-w-auto mx-auto pl-0 pr-0 md:w-full md:min-w-auto max-w-4xl pt-0 pb-0" data-component-id="cmrbt732a0187nvfibp7lvxi8_4" id="{i()}">
<div class="mt-3 mb-3" data-component-type="rte" id="{i()}">
{tema_blokker}
</div>
</section>
<div class="flex flex-col relative pl-5 pb-6 pt-10 pr-5 rounded-2xl mb-6 mt-16 w-full ml-0 mr-0 md:ml-0 md:mr-0 border border-2" data-component-id="cmk9iuwll006dz7lqo3v7yqvj_14" id="{i()}" style="background-color: transparent; border-color: var({v}nlka);">
<div class="absolute m-0 rounded-full w-16 h-16" id="{i()}" style="max-width: 100px; top: -32px; left: 2rem; background-color: var({v}ndju);"><img alt="" class="md:p-0 p-0 md:m-0 m-0 rounded-full w-16 bg-contain bg-center bg-no-repeat object-contain object-center h-16 md:border-0 border-0" data-api-endpoint="https://uia.instructure.com/api/v1/files/2628672" data-api-returntype="File" id="{i()}" loading="lazy" src="{ICON}litteratur_ramme.svg" style="border-color: var({v}pkhs);"/></div>
<div class="flex items-center mb-2 mt-0 md:p-0 pt-0 pl-0" id="{i()}">
<h3 class="mce-content-body mce-edit-focus md:border-0 border-0 md:m-0 mt-0 md:p-0 pt-0 w-full" id="{i()}"><span id="{i()}">Litteratur</span></h3>
</div>
<span class="inline-block pt-1 pb-1 pl-2 pr-2 rounded !bg-opacity-10 text-xs tracking-widest uppercase mb-1 w-40" id="{i()}" style="background-color: var({v}jdvv); color: var({v}hdbb);"><span id="{i()}"><strong id="{i()}"><span id="{i()}">UTVALGT</span></strong></span></span>
<div class="m-0 p-0" data-component-type="rte" id="{i()}">
{bullets(s["utvalgt"].split(chr(10)))}
</div>
<span class="inline-block pt-1 pb-1 pl-2 pr-2 rounded !bg-opacity-10 text-xs tracking-widest uppercase mb-1 w-40 mt-2" id="{i()}" style="background-color: var({v}wcil); color: var({v}jfnw);"><span id="{i()}"><strong id="{i()}"><span id="{i()}">Hvis interessert</span></strong></span></span>
<div class="m-0 p-0" data-component-type="rte" id="{i()}">
{bullets(s["interessert"].split(chr(10)))}
</div>
</div>
</div>
</body></html>
"""
    (PAGES / f"{MODUL_SLUG}.html").write_text(page, encoding="utf-8")


def main():
    PAGES.mkdir(exist_ok=True)
    valgt = sys.argv[1:]
    for slug, tittel, prefix in TEMA:
        if (not valgt or slug in valgt) and (KILDE / f"{slug}.md").exists():
            tema_side(slug, tittel, prefix)
            print("bygget", slug)
    if (not valgt or "modulside" in valgt) and (KILDE / "modulside.md").exists():
        modulside()
        print("bygget", MODUL_SLUG)


if __name__ == "__main__":
    main()
