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

The build reads the owner, repo name and branch from your `git remote`, so all
links inside the page (GitHub, raw Markdown, Pages URL) follow automatically.
There is no account name hardcoded in the content.

## Changing the GitHub account name

The published address is `https://<account>.github.io/report/`, so renaming the
account is what changes it. GitHub does not allow this through the API — do it
at <https://github.com/settings/admin> under **Change username**.

Then, in a clone of this repo:

```bash
./site/after-rename.sh NEW_USERNAME
```

That script updates the git remote, rebuilds the site with the new links, and
pushes. Afterwards, open `https://github.com/NEW_USERNAME/report/settings/pages`
and confirm the source is still the branch + `/docs` (re-save if it looks
blank). The old address keeps redirecting, so links you already shared stay
valid.

To use a custom domain instead, put the domain in `docs/CNAME` and add the DNS
records GitHub specifies.

## About the report

A 14–21 day, low-cost acquisition pilot for Kixly: 4–5 outreach agents
targeting competitor/prediction-market users (priority 1), Korean-language
sports communities (priority 2) and existing users (priority 3), with
Day 7 / Day 14 / Day 21 decision gates.

The pilot has **not** run yet. The report contains no campaign results — all
forward-looking figures are labelled as assumptions.
