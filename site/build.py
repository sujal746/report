#!/usr/bin/env python3
"""
Builds the static Kixly BD pilot report website.

Usage:
    python3 -m venv .venv && .venv/bin/pip install markdown
    .venv/bin/python site/build.py

Reads   : Kixly-Zero-Budget-BD-Pilot-Plan.md
Writes  : docs/index.html  (+ assets, .nojekyll, downloadable .md)
"""

import datetime as dt
import html
import pathlib
import re
import shutil

import markdown

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "Kixly-Zero-Budget-BD-Pilot-Plan.md"
SITE = ROOT / "site"
DOCS = ROOT / "docs"

REPO_URL = "https://github.com/sujal746/report"
RAW_URL = (
    "https://raw.githubusercontent.com/sujal746/report/arena/20c83bcb-report/"
    "Kixly-Zero-Budget-BD-Pilot-Plan.md"
)

# Headline figures shown in the hero. These are planning figures taken from the
# report (section 1.2 and 9.4) and are labelled as assumptions, not results.
STATS = [
    ("310", "unique prospects contacted in 14 days with 5 shillers", "planned volume"),
    ("0–5", "verified depositors expected over 14 days", "illustrative range"),
    ("64%", "of outreach on competitor / prediction-market users", "priority 1"),
    ("14 → 21", "pilot days, with a firm final decision on Day 21", "no Day 28"),
]

TAGS = {
    "FACT": "fact",
    "PROPOSAL": "proposal",
    "ASSUMPTION": "assumption",
    "TO FILL": "tofill",
}


def split_front_matter(text: str):
    """Pull the title block out of the markdown so it can be rendered as a hero."""
    lines = text.split("\n")
    cut = next(i for i, ln in enumerate(lines) if ln.strip() == "---")
    head, body = lines[:cut], lines[cut + 1 :]

    title, subtitle, meta = "", [], []
    for ln in head:
        s = ln.strip()
        if s.startswith("# ") and not title:
            title = s[2:].strip()
        elif s.startswith("### "):
            subtitle.append(s[4:].strip())
        elif s.startswith("**") and ":**" in s:
            key, _, val = s.partition(":**")
            meta.append((key.strip("* ").strip(), val.strip()))
    return title, " ".join(subtitle), meta, "\n".join(body).strip()


def render(md_text: str):
    md = markdown.Markdown(
        extensions=["extra", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "2-3", "permalink": False}},
    )
    body = md.convert(md_text)
    # md.toc arrives wrapped in <div class="toc">; drop it so the nav is the
    # direct parent of the list and the CSS child selectors apply.
    toc = re.sub(r"^\s*<div class=\"toc\">\s*|\s*</div>\s*$", "", md.toc)
    return body, toc.strip()


def _protect(body: str):
    """Park <pre>/<code> blocks so their literal text is never rewritten."""
    store = []

    def stash(m):
        store.append(m.group(0))
        return f"\x00CODE{len(store) - 1}\x00"

    return (
        re.sub(r"<pre>.*?</pre>|<code>.*?</code>", stash, body, flags=re.S),
        store,
    )


def _restore(body: str, store) -> str:
    return re.sub(
        r"\x00CODE(\d+)\x00",
        lambda m: store[int(m.group(1))],
        body,
    )


def polish(body: str) -> str:
    """Small, targeted HTML cleanups the markdown renderer does not do for us."""
    # Warning callouts.
    body = re.sub(
        r"<blockquote>\s*<p>(\s*⚠️)",
        r'<blockquote class="warn"><p>\1',
        body,
    )
    # Scrollable tables.
    body = re.sub(
        r"<table>(.*?)</table>",
        lambda m: f'<div class="table-wrap"><table>{m.group(1)}</table></div>',
        body,
        flags=re.S,
    )

    # Status tags -> coloured badges. Never inside code blocks: those contain
    # literal "[TO FILL]" placeholders that must stay as plain text.
    body, store = _protect(body)
    body = re.sub(
        r"\[(FACT|PROPOSAL|ASSUMPTION|TO FILL)\]",
        lambda m: f'<span class="tag tag-{TAGS[m.group(1)]}">{m.group(1)}</span>',
        body,
    )
    body = _restore(body, store)
    # Heading anchors for deep links / copy.
    def anchor(m):
        return f'<h{m.group(1)} id="{m.group(2)}">{m.group(3)}' \
               f'<a class="anchor" href="#{m.group(2)}" aria-label="Link to this section">#</a>' \
               f"</h{m.group(1)}>"

    body = re.sub(
        r"<h([23]) id=\"([^\"]+)\">(.*?)</h\1>", anchor, body, flags=re.S
    )
    return body


def find_href(toc_html: str, needle: str) -> str:
    m = re.search(
        r'<a href="(#[^"]+)"[^>]*>[^<]*' + re.escape(needle), toc_html, re.I
    )
    return m.group(1) if m else "#"


def main():
    text = SRC.read_text(encoding="utf-8")
    title, subtitle, meta, body_md = split_front_matter(text)
    body, toc = render(body_md)
    body = polish(body)

    action_href = find_href(toc, "One-page action plan")
    risks_href = find_href(toc, "Risks and Mitigation")
    scripts_href = find_href(toc, "Korean-Language Outreach Strategy")

    tpl = (SITE / "template.html").read_text(encoding="utf-8")

    meta_html = "\n".join(
        f'<div class="meta-row"><span>{html.escape(k)}</span>'
        f"<strong>{html.escape(v)}</strong></div>"
        for k, v in meta
    )
    stats_html = "\n".join(
        f'<div class="stat"><div class="stat-num">{n}</div>'
        f'<div class="stat-label">{html.escape(l)}</div>'
        f'<div class="stat-note">{html.escape(note)}</div></div>'
        for n, l, note in STATS
    )

    out = (
        tpl.replace("{{TITLE}}", html.escape(title))
        .replace("{{SUBTITLE}}", html.escape(subtitle))
        .replace("{{META}}", meta_html)
        .replace("{{STATS}}", stats_html)
        .replace("{{TOC}}", toc)
        .replace("{{CONTENT}}", body)
        .replace("{{ACTION_HREF}}", action_href)
        .replace("{{RISKS_HREF}}", risks_href)
        .replace("{{SCRIPTS_HREF}}", scripts_href)
        .replace("{{REPO_URL}}", REPO_URL)
        .replace("{{RAW_URL}}", RAW_URL)
        .replace("{{YEAR}}", str(dt.date.today().year))
        .replace("{{BUILT}}", dt.date.today().strftime("%d %B %Y"))
    )

    DOCS.mkdir(exist_ok=True)
    (DOCS / "index.html").write_text(out, encoding="utf-8")
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    assets_out = DOCS / "assets"
    if assets_out.exists():
        shutil.rmtree(assets_out)
    shutil.copytree(SITE / "assets", assets_out)
    shutil.copy(SRC, DOCS / "kixly-bd-pilot-plan.md")

    print(f"Built {DOCS / 'index.html'} ({len(out):,} bytes)")


if __name__ == "__main__":
    main()
