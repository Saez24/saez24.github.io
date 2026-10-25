# saez24.github.io

Quellcode der Website <https://saez24.github.io/> — Infos, Downloads und Datenschutz für die
Apps Frequenzo, Streamy und Finoro sowie weitere Projekte aus dem
[Portfolio](https://your-developer.de/).

Reines HTML/CSS ohne Build, alles wird von GitHub Pages ausgeliefert: keine externen
Schriften, Skripte oder Analytics. Das Design entspricht dem Portfolio (Bento-Kacheln, Geist,
Hell/Dunkel-Schalter).

| Pfad | Inhalt |
| --- | --- |
| `index.html` | Startseite |
| `datenschutz.html` | Datenschutz der Website |
| `frequenzo/`, `streamy/`, `finoro/` | je Vorstellung (`index.html`) und `datenschutz.html` |
| `assets/` | `style.css`, `site.js`, Schriften (Geist, OFL), Icons und Screenshots |
| `tools/legal.py` | Seitengerüst (Nav, Footer) und Erzeugung von Datenschutzseiten aus Markdown |

## Lokal ansehen

```bash
python3 -m http.server 8000   # http://localhost:8000
```

## Pflege

- Nav und Footer stehen in jeder Seite; Vorlage ist `header()`/`footer()` in `tools/legal.py`.
- Datenschutzseite einer App aus deren Markdown-Texten (DE + EN) erzeugen:

  ```bash
  python3 tools/legal.py privacy_de.md privacy_en.md frequenzo/datenschutz.html
  ```
