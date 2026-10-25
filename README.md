# saez24.github.io

Website von Saez24 auf GitHub Pages: <https://saez24.github.io/> — Infos, Downloads und
Datenschutz für die Apps.

| Pfad | Inhalt |
| --- | --- |
| `index.html` | Startseite mit allen Apps |
| `impressum.html`, `datenschutz.html` | Impressum und Datenschutz der Website |
| `frequenzo/`, `streamy/`, `finoro/` | je `index.html` (Vorstellung) und `datenschutz.html` |
| `assets/` | `style.css` (hell/dunkel) und App-Icons |
| `tools/legal.py` | erzeugt eine Datenschutzseite (DE + EN) aus den Markdown-Texten einer App |

Reines HTML/CSS, ohne Build und ohne externe Ressourcen (keine Fonts, Skripte, Analytics) —
sonst bräuchte die Website selbst mehr Datenschutzhinweise. `.nojekyll` schaltet Jekyll ab.
Pfade sind absolut (`/assets/…`), weil die User-Site im Wurzelverzeichnis liegt.

## Datenschutz einer App aktualisieren

Quelle ist das App-Projekt (dort zeigt die App denselben Text):

```bash
python3 tools/legal.py ../Frequenzo/assets/legal/privacy_de.md \
  ../Frequenzo/assets/legal/privacy_en.md frequenzo/datenschutz.html
```

Streamy und Finoro haben noch handgeschriebene Entwürfe; sobald dort Markdown-Texte
existieren, genauso erzeugen.

## Vor dem ersten Veröffentlichen

- [ ] Platzhalter ersetzen: `grep -rn '{{' --include='*.html' .` muss leer sein
      (`{{NAME}}`, `{{EMAIL}}`, `{{ANSCHRIFT}}`; für Frequenzo in den Markdown-Dateien im
      App-Projekt ändern und die Seite neu erzeugen).
- [ ] Impressum: nur nötig bei geschäftsmäßigem Angebot (z. B. Verkauf von Frequenzo Pro).
      Sonst `impressum.html` löschen und die Links im Fuß entfernen.
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
