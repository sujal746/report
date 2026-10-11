# report

Kixly business development material.

## Website

The BD pilot plan is published with GitHub Pages from the `docs/` folder:

**https://sujal746.github.io/report/**

## Contents

| Path | What it is |
|---|---|
| `Kixly-Zero-Budget-BD-Pilot-Plan.md` | Source of the report. Edit this, then rebuild the site. |
| `docs/` | Generated static site (GitHub Pages source). |
| `site/build.py` | Build script: Markdown → `docs/index.html`. |
| `site/template.html` | Page shell. |
| `site/assets/` | Styles, nav script, favicon. |

## Rebuilding the site

```bash
python3 -m venv .venv
.venv/bin/pip install markdown
.venv/bin/python site/build.py
```

Then commit `docs/` and push. GitHub Pages redeploys automatically.

## About the report

A 14–21 day, low-cost acquisition pilot for Kixly: 4–5 outreach agents
targeting competitor/prediction-market users (priority 1), Korean-language
sports communities (priority 2) and existing users (priority 3), with
Day 7 / Day 14 / Day 21 decision gates.

The pilot has **not** run yet. The report contains no campaign results — all
forward-looking figures are labelled as assumptions.
