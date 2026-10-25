# saez24.github.io

Website von Saez24 auf GitHub Pages: <https://saez24.github.io/> — Infos, Downloads und
Datenschutz für die Apps.

| Pfad | Inhalt |
| --- | --- |
| `index.html` | Startseite mit allen Apps |
| `datenschutz.html` | Datenschutz der Website |
| `frequenzo/`, `streamy/`, `finoro/` | je `index.html` (Vorstellung) und `datenschutz.html` |
| `assets/` | `style.css`, `site.js` (Hell/Dunkel, Menü), `fonts/` (Geist, OFL), App-Icons und `projects/` (Screenshots der Portfolio-Projekte) |
| `tools/legal.py` | Seitengerüst (Nav, Footer) und Erzeugung der Datenschutzseite einer App (DE + EN) |

Design und Aufbau stammen aus dem Portfolio (`../Portfolio`, your-developer.de): Bento-Kacheln,
Geist-Schriften, Lime-Akzent, Hell/Dunkel-Schalter. Farben und Komponenten in
`assets/style.css` sind dort aus `src/styles.scss` und den Komponenten-SCSS portiert – bei
Design-Änderungen im Portfolio hier nachziehen.

Reines HTML/CSS ohne Build. Alles wird von GitHub Pages selbst ausgeliefert, nichts von
fremden Servern (keine externen Schriften, Skripte oder Analytics). Einzige gespeicherte
Angabe ist die Theme-Wahl (`saez24-theme` im `localStorage`), steht so in `datenschutz.html`.
`.nojekyll` schaltet Jekyll ab. Pfade sind absolut (`/assets/…`), weil die User-Site im
Wurzelverzeichnis liegt.

Nav und Footer stehen in jeder Seite ausgeschrieben. Vorlage ist `header()`/`footer()` in
`tools/legal.py` – bei Änderungen dort und in allen Seiten gleich ändern.

## Datenschutz einer App aktualisieren

Quelle ist das App-Projekt (dort zeigt die App denselben Text):

```bash
python3 tools/legal.py ../Frequenzo/assets/legal/privacy_de.md \
  ../Frequenzo/assets/legal/privacy_en.md frequenzo/datenschutz.html
```

Streamy und Finoro haben noch handgeschriebene Entwürfe; sobald dort Markdown-Texte
existieren, genauso erzeugen.

## Vor dem ersten Veröffentlichen

- [x] Platzhalter ersetzt (Verantwortlicher wie im Portfolio). Kontrolle:
      `grep -rn '{{' --include='*.html' .` muss leer sein.
- [ ] Impressum: nur nötig bei geschäftsmäßigem Angebot (z. B. Verkauf von Frequenzo Pro);
      dann Seite anlegen und in `footer()` (`tools/legal.py`) und allen Seiten verlinken.
- [ ] Entwürfe Streamy/Finoro in den jeweiligen Projekten prüfen.

## Veröffentlichen

1. Auf GitHub ein **öffentliches** Repo `Saez24/saez24.github.io` anlegen (leer).
2. `git push -u origin main`
3. *Settings → Pages*: Source „Deploy from a branch“, Branch `main`, Ordner `/ (root)`.
   Nach ein bis zwei Minuten ist die Seite unter <https://saez24.github.io/> erreichbar.

## Lokal ansehen

```bash
python3 -m http.server 8000   # http://localhost:8000
```
