#!/usr/bin/env python3
"""Rechtstext-Seite (DE + EN) aus den Markdown-Dateien einer App erzeugen.

Quelle bleibt das App-Projekt, damit App und Website denselben Text zeigen, z. B.:

    python3 tools/legal.py ../Frequenzo/assets/legal/privacy_de.md \
        ../Frequenzo/assets/legal/privacy_en.md frequenzo/datenschutz.html

Unterstützt genau das Format der App-Texte: `#`/`##` Überschriften, Absätze
(einfacher Zeilenumbruch = <br>), `- ` Listen, **fett** und [Links](https://…).
"""

import html
import re
import sys
from pathlib import Path

HEADER = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <link rel="stylesheet" href="/assets/style.css">
</head>
<body>
  <header class="site">
    <div class="wrap">
      <a class="brand" href="/">Saez24</a>
      <nav><a href="/frequenzo/">Frequenzo</a><a href="/streamy/">Streamy</a><a href="/finoro/">Finoro</a></nav>
    </div>
  </header>
  <main>
    <div class="wrap legal">
"""

FOOTER = """    </div>
  </main>
  <footer class="site">
    <div class="wrap">
      <span>© 2026 Saez24</span>
      <a href="/impressum.html">Impressum</a>
      <a href="/datenschutz.html">Datenschutz</a>
      <a href="https://github.com/Saez24">GitHub</a>
    </div>
  </footer>
</body>
</html>
"""


def inline(text: str) -> str:
    text = html.escape(text, quote=False)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    return re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', text)


def render(markdown: str) -> str:
    out: list[str] = []
    paragraph: list[str] = []
    in_list = False

    def flush() -> None:
        nonlocal in_list
        if paragraph:
            out.append("<p>" + "<br>\n".join(inline(line) for line in paragraph) + "</p>")
            paragraph.clear()
        if in_list:
            out.append("</ul>")
            in_list = False

    for raw in markdown.splitlines():
        line = raw.rstrip()
        if not line:
            flush()
        elif line.startswith("## "):
            flush()
            out.append(f"<h2>{inline(line[3:])}</h2>")
        elif line.startswith("# "):
            flush()
            out.append(f"<h1>{inline(line[2:])}</h1>")
        elif line.startswith("- "):
            if paragraph:
                flush()
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append(f"<li>{inline(line[2:])}</li>")
        else:
            if in_list:
                flush()
            paragraph.append(line)
    flush()
    return "\n".join("      " + line for line in out)


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    de, en, target = (Path(arg) for arg in sys.argv[1:])
    title = de.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    body = (
        '      <section lang="de">\n      <p class="lang">Deutsch · <a href="#en">English</a></p>\n'
        + render(de.read_text(encoding="utf-8"))
        + '\n      </section>\n      <section lang="en" id="en">\n      <p class="lang">English</p>\n'
        + render(en.read_text(encoding="utf-8"))
        + "\n      </section>\n"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(HEADER.format(title=html.escape(title)) + body + FOOTER, encoding="utf-8")
    print(f"{target} geschrieben")


if __name__ == "__main__":
    main()
