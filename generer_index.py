#!/usr/bin/env python3
"""Genererer rot-index.html med kort for hver demo i repoet.

En "demo" er enhver toppnivå-mappe (unntatt skjulte mapper og mapper i
.gitignore) som inneholder en index.html. Tittel hentes fra <title> i
demoens index.html, beskrivelse fra første avsnitt i demoens README.md.
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def is_ignored(dirname):
    gitignore = ROOT / ".gitignore"
    if not gitignore.exists():
        return False
    patterns = [
        line.strip().rstrip("/")
        for line in gitignore.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]
    return dirname in patterns


def find_demos():
    demos = []
    for entry in sorted(ROOT.iterdir()):
        if not entry.is_dir():
            continue
        if entry.name.startswith("."):
            continue
        if is_ignored(entry.name):
            continue
        index = entry / "index.html"
        if not index.exists():
            continue
        demos.append(entry)
    return demos


def extract_title(index_path):
    html = index_path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE | re.DOTALL)
    if match:
        return re.sub(r"\s+", " ", match.group(1)).strip()
    return index_path.parent.name


def extract_description(folder):
    readme = folder / "README.md"
    if not readme.exists():
        return ""
    lines = readme.read_text(encoding="utf-8", errors="ignore").splitlines()
    paragraph = []
    started = False
    for line in lines:
        stripped = line.strip()
        if not started:
            if stripped.startswith("#") or not stripped:
                continue
            started = True
        if not stripped:
            if paragraph:
                break
            continue
        if stripped.startswith("#"):
            break
        paragraph.append(stripped)
    text = " ".join(paragraph)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"\*\*([^*]*)\*\*", r"\1", text)
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return text.strip()


def build_html(demos):
    cards = []
    for folder in demos:
        index = folder / "index.html"
        title = extract_title(index)
        description = extract_description(folder)
        href = f"{folder.name}/index.html"
        desc_html = f"<p>{description}</p>" if description else ""
        cards.append(f"""      <li class="card">
        <a href="{href}">
          <h2>{title}</h2>
          {desc_html}
        </a>
      </li>""")

    cards_html = "\n".join(cards)

    return f"""<!DOCTYPE html>
<html lang="no">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>IS930 Temasider – demoer</title>
<style>
  :root {{
    color-scheme: light dark;
    --fg: #1a1a1a;
    --bg: #f7f7f5;
    --card-bg: #ffffff;
    --border: #e0e0dc;
    --accent: #2b6cb0;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --fg: #e8e8e6;
      --bg: #1b1b1a;
      --card-bg: #262625;
      --border: #3a3a38;
      --accent: #7ab0e8;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 2.5rem 1.5rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    color: var(--fg);
    background: var(--bg);
  }}
  header {{
    max-width: 960px;
    margin: 0 auto 2rem;
  }}
  h1 {{
    font-size: 1.75rem;
    margin: 0 0 0.5rem;
  }}
  header p {{
    margin: 0;
    opacity: 0.75;
  }}
  ul.cards {{
    list-style: none;
    margin: 0 auto;
    padding: 0;
    max-width: 960px;
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1rem;
  }}
  .card {{
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    transition: border-color 0.15s ease, transform 0.15s ease;
  }}
  .card:hover {{
    border-color: var(--accent);
    transform: translateY(-2px);
  }}
  .card a {{
    display: block;
    padding: 1.25rem;
    text-decoration: none;
    color: inherit;
  }}
  .card h2 {{
    margin: 0 0 0.5rem;
    font-size: 1.15rem;
    color: var(--accent);
  }}
  .card p {{
    margin: 0;
    font-size: 0.92rem;
    line-height: 1.4;
    opacity: 0.85;
  }}
</style>
</head>
<body>
  <header>
    <h1>IS930 Temasider</h1>
    <p>Demoer til bruk i undervisning i tematisk kartografi.</p>
  </header>
  <ul class="cards">
{cards_html}
  </ul>
</body>
</html>
"""


def main():
    demos = find_demos()
    html = build_html(demos)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"Oppdaterte index.html med {len(demos)} demo(er).")


if __name__ == "__main__":
    main()
