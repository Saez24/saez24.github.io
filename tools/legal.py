#!/usr/bin/env python3
"""Rechtstext-Seite (DE + EN) aus den Markdown-Dateien einer App erzeugen.

Quelle bleibt das App-Projekt, damit App und Website denselben Text zeigen, z. B.:

    python3 tools/legal.py ../Frequenzo/assets/legal/privacy_de.md \
        ../Frequenzo/assets/legal/privacy_en.md frequenzo/datenschutz.html

Unterstützt genau das Format der App-Texte: `#`/`##` Überschriften, Absätze
(einfacher Zeilenumbruch = <br>), `- ` Listen, **fett** und [Links](https://…).

`header()` und `footer()` sind das Gerüst aller Seiten (Nav, Footer). Wer Nav oder
Footer ändert, ändert sie hier und in den handgeschriebenen Seiten gleich.
"""

import html
import re
import sys
from pathlib import Path

APPS = (("frequenzo", "Frequenzo"), ("streamy", "Streamy"), ("finoro", "Finoro"))
GITHUB = "https://github.com/Saez24"
PORTFOLIO = "https://your-developer.de/"

ICON_GITHUB = (
    '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 .297c-6.63 0-12 5.373-12 '
    "12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042"
    "-1.61-4.042-1.61-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.838 "
    "1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332"
    "-5.466-5.93 0-1.31.467-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 "
    "1.98-.4 3-.405 1.02.005 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176"
    ".765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896"
    "-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12\"/></svg>"
)
ICON_GLOBE = (
    '<svg class="icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 '
    "0-20zm6.93 6h-2.95a15.65 15.65 0 0 0-1.38-3.56A8.03 8.03 0 0 1 18.93 8zM12 4.04c.83 1.2 1.48 2.53 "
    "1.91 3.96h-3.82c.43-1.43 1.08-2.76 1.91-3.96zM4.26 14A8.2 8.2 0 0 1 4 12c0-.69.1-1.36.26-2h3.38a16.5 "
    "16.5 0 0 0 0 4H4.26zm.82 2h2.95c.32 1.25.78 2.45 1.38 3.56A7.99 7.99 0 0 1 5.08 16zm2.95-8H5.08a7.99 "
    "7.99 0 0 1 4.33-3.56A15.65 15.65 0 0 0 8.03 8zM12 19.96c-.83-1.2-1.48-2.53-1.91-3.96h3.82c-.43 1.43"
    "-1.08 2.76-1.91 3.96zM14.34 14H9.66a14.7 14.7 0 0 1 0-4h4.68a14.7 14.7 0 0 1 0 4zm.25 5.56c.6-1.11 "
    '1.06-2.31 1.38-3.56h2.95a8.03 8.03 0 0 1-4.33 3.56zM16.36 14a16.5 16.5 0 0 0 0-4h3.38a8.2 8.2 0 0 1 0 4h-3.38z"/></svg>'
)
ICON_SUN = (
    '<svg class="icon icon--sun" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 '
    "0-10zM2 13h2a1 1 0 0 0 0-2H2a1 1 0 0 0 0 2zm18 0h2a1 1 0 0 0 0-2h-2a1 1 0 0 0 0 2zM11 2v2a1 1 0 0 0 2 "
    "0V2a1 1 0 0 0-2 0zm0 18v2a1 1 0 0 0 2 0v-2a1 1 0 0 0-2 0zM5.99 4.58a1 1 0 0 0-1.41 1.41l1.06 1.06a1 1 0 "
    "0 0 1.41-1.41L5.99 4.58zm12.37 12.37a1 1 0 0 0-1.41 1.41l1.06 1.06a1 1 0 0 0 1.41-1.41l-1.06-1.06zm1.06"
    "-10.96a1 1 0 0 0-1.41-1.41l-1.06 1.06a1 1 0 0 0 1.41 1.41l1.06-1.06zM7.05 18.36a1 1 0 0 0-1.41-1.41l"
    '-1.06 1.06a1 1 0 0 0 1.41 1.41l1.06-1.06z"/></svg>'
)
ICON_MOON = (
    '<svg class="icon icon--moon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3a9 9 0 1 0 9 9c0-.46'
    '-.04-.92-.1-1.36a5.39 5.39 0 0 1-4.4 2.26 5.4 5.4 0 0 1-3.14-9.8c-.44-.06-.9-.1-1.36-.1z"/></svg>'
)
ICON_MENU = (
    '<svg class="icon icon--menu" viewBox="0 0 24 24" aria-hidden="true">'
    '<path d="M3 18h18v-2H3v2zm0-5h18v-2H3v2zm0-7v2h18V6H3z"/></svg>'
)
ICON_CLOSE = (
    '<svg class="icon icon--close" viewBox="0 0 24 24" aria-hidden="true"><path d="M19 6.41 17.59 5 12 '
    '10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/></svg>'
)


def _links(current: str) -> str:
    return "".join(
        f'<a class="nav__link" href="/{slug}/"'
        + (' aria-current="page"' if slug == current else "")
        + f">{name}</a>"
        for slug, name in APPS
    ) + '<a class="nav__link" href="/#projekte">Projekte</a>'


def header(title: str, current: str = "", main: str = "", description: str = "") -> str:
    """Kopf bis einschließlich `<main>`; `current` markiert die App in der Nav."""
    cls = f' class="{main}"' if main else ""
    meta = f'\n  <meta name="description" content="{html.escape(description)}">' if description else ""
    return f"""<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>{meta}
  <meta name="theme-color" content="#0d1410">
  <link rel="preload" href="/assets/fonts/geist-variable.woff2" as="font" type="font/woff2" crossorigin>
  <link rel="stylesheet" href="/assets/style.css">
  <script src="/assets/site.js"></script>
</head>
<body>
  <a class="skip-link" href="#main">Zum Inhalt springen</a>
  <nav class="nav" aria-label="Hauptnavigation">
    <div class="nav__inner">
      <a class="nav__logo" href="/" aria-label="Saez24, Startseite">
        <span class="nav__logo-mark" aria-hidden="true">S</span>
        <span class="nav__logo-text">Saez24</span>
      </a>
      <div class="nav__links">{_links(current)}</div>
      <div class="nav__actions">
        <a class="nav__icon-btn nav__ext" href="{GITHUB}" aria-label="GitHub" title="GitHub">{ICON_GITHUB}</a>
        <a class="nav__icon-btn nav__ext" href="{PORTFOLIO}" aria-label="Portfolio" title="Portfolio">{ICON_GLOBE}</a>
        <button class="nav__icon-btn nav__theme" type="button" aria-label="Design wechseln">{ICON_SUN}{ICON_MOON}</button>
        <button class="nav__icon-btn nav__hamburger" type="button" aria-label="Navigation öffnen" aria-expanded="false" aria-controls="nav-drawer">{ICON_MENU}{ICON_CLOSE}</button>
      </div>
    </div>
    <div class="nav__drawer" id="nav-drawer" hidden>
      {_links(current)}
      <a class="nav__link" href="{GITHUB}">GitHub</a>
      <a class="nav__link" href="{PORTFOLIO}">Portfolio</a>
    </div>
  </nav>
  <main id="main"{cls}>
"""


def footer() -> str:
    return f"""  </main>
  <footer class="footer">
    <div class="container">
      <div class="footer__content">
        <div class="footer__brand">
          <span class="footer__logo-dot" aria-hidden="true"></span>
          <span class="footer__brand-name">Saez24</span>
          <span>· Kleine Apps ohne Tracking.</span>
        </div>
        <div class="footer__channels">
          <a class="footer__channel" href="{GITHUB}" aria-label="GitHub" title="GitHub">{ICON_GITHUB}</a>
          <a class="footer__channel" href="{PORTFOLIO}" aria-label="Portfolio" title="Portfolio">{ICON_GLOBE}</a>
        </div>
      </div>
      <div class="footer__bottom">
        <span>© 2026 Saez24</span>
        <nav class="footer__legal" aria-label="Rechtliches">
          <a href="/datenschutz.html">Datenschutz</a>
          <span class="footer__sep" aria-hidden="true">·</span>
          <a href="{PORTFOLIO}">Portfolio</a>
        </nav>
      </div>
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
    return "\n".join("        " + line for line in out)


def main() -> None:
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    de, en, target = (Path(arg) for arg in sys.argv[1:])
    title = de.read_text(encoding="utf-8").splitlines()[0].lstrip("# ").strip()
    body = (
        '    <div class="legal__container">\n'
        '      <section lang="de">\n        <p class="lang">Deutsch · <a href="#en">English</a></p>\n'
        + render(de.read_text(encoding="utf-8"))
        + '\n      </section>\n      <section lang="en" id="en">\n        <p class="lang">English</p>\n'
        + render(en.read_text(encoding="utf-8"))
        + "\n      </section>\n    </div>\n"
    )
    target.parent.mkdir(parents=True, exist_ok=True)
    current = target.parent.name
    target.write_text(header(title, current, main="legal") + body + footer(), encoding="utf-8")
    print(f"{target} geschrieben")


if __name__ == "__main__":
    main()
