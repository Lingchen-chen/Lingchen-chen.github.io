# Lingchen Yang

Personal website: [lingchen-chen.github.io](https://lingchen-chen.github.io/).

The website uses plain HTML and CSS. Local preview and deployment checks use Python 3.9 or newer and its standard library; no packages need to be installed.

## Preview

From this directory:

```sh
python3 -m http.server 4173 --bind 127.0.0.1
```

Open [the homepage](http://127.0.0.1:4173/) or [all publications](http://127.0.0.1:4173/publications/).

## Edit

- `index.html`: biography, research introduction, and selected work.
- `publications/index.html`: all publications grouped by year, with expandable abstracts and author lists.
- `assets/css/style.css`: shared typography, layouts, responsive rules, and highlight colors. General emphasis uses `--accent`; awards use `--award`.
- The homepage's native `Email` disclosure expands to show the address as plain text with `[at]`, without a mailto link or JavaScript.
- `assets/img/social-preview.svg` and `.png`: editable sharing card and its 1200 × 630 raster export. Both main pages reference the PNG through Open Graph and Twitter metadata; update the absolute image URLs if the site's domain changes.
- `assets/img/`: portrait and original research images, including publication previews and posters.
- `data/publications.bib`: retained bibliography. When adding or removing a paper, update this file and the complete publication page; add it to the homepage if appropriate.
- `data/deferred-publications.bib`: citations temporarily excluded from the public list, retained for future restoration. Their source records use `visible: false` in `data/publication-sources.json`.
- `data/publication-sources.json`: verified metadata, source URLs, and figure provenance for newly added papers; these records also distinguish later publication titles from earlier arXiv titles.
- `404.html`, `robots.txt`, and `sitemap.xml`: navigation and indexing support.

All navigation between the homepage and publication page uses local links. The existing `/publications/` address is preserved.
The two small files in `_design-preview/` redirect previously shared preview links to the current pages.

## Validate and package

```sh
python3 scripts/check_site.py
python3 scripts/build.py
```

Validation checks internal navigation, image and stylesheet references, duplicate IDs, and coverage of every bibliography record. The build copies only public website files into `dist/` and checks that output again. The bibliography, scripts, repository metadata, and development files are excluded from the deployment package.

To inspect the deployment package:

```sh
python3 -m http.server 4174 --bind 127.0.0.1 --directory dist
```

## Deployment

The GitHub Actions workflow validates pull requests. Pushes to `main` or `master`, and manual workflow runs, package the website and publish `dist/` to the existing `gh-pages` branch. Keep GitHub Pages configured to serve that branch. The `.nojekyll` file tells GitHub Pages to serve the static files directly.

The existing license notice is retained in `LICENSE`.
