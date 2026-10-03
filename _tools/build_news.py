#!/usr/bin/env python3
"""Build news/index.html from the news scanner's JSON digests.

Reads research/news/data/YYYY-MM-DD.json from the svrnsrc.ai research repo
(written by tools/news_scan/scan.py there) and renders every scan, newest
first, grouped by theme. Only public fields are shown: title, source, date,
summary, and link. The scanner's "why it matters" notes are internal and are
left out.

Usage: python3 _tools/build_news.py [DATA_DIR]
DATA_DIR defaults to ~/Projects/svrnsrc.ai/research/news/data.
Jekyll skips _-prefixed folders, so this script is not published.
"""
import datetime as dt
import html
import json
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
DATA = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else (
    Path.home() / "Projects/svrnsrc.ai/research/news/data")
OUT = SITE / "news" / "index.html"

# Same keys and order as THEMES in the scanner (tools/news_scan/scan.py).
THEMES = {
    "direct_mentions": "Direct mentions",
    "sovereign_ai": "Sovereign AI",
    "lock_in_and_exit": "Lock-in and exit",
    "open_models": "Open models and self-hosting",
    "agent_governance": "Agent governance",
    "supply_chain_provenance": "Supply chain and provenance",
    "data_sovereignty_regulation": "Data sovereignty and regulation",
    "smb_data_and_agents": "Small business data and agents",
}

esc = html.escape


def span(start: str, end: str) -> str:
    """'26 Sep to 3 Oct 2026', with both years only when they differ."""
    s, e = dt.date.fromisoformat(start), dt.date.fromisoformat(end)
    left = f"{s.day} {s.strftime('%b')}" + (f" {s.year}" if s.year != e.year else "")
    return f"{left} to {e.day} {e.strftime('%b %Y')}"


def short_date(iso: str) -> str:
    if iso == "unknown":
        return "date not given"
    d = dt.date.fromisoformat(iso)
    return f"{d.day} {d.strftime('%b %Y')}"


def count(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def render_scan(scan: dict) -> str:
    start, end = scan["window"]
    items = scan["kept"]
    searches = len(scan.get("searches") or [])
    meta = count(len(items), "story", "stories")
    if searches:
        meta += f" from {count(searches, 'search', 'searches')}"
    parts = [f'<section class="section news-scan" id="scan-{esc(end)}">\n'
             f'  <div class="section-inner">\n'
             f'    <h2 class="section-heading news-week">{esc(span(start, end))}</h2>\n'
             f'    <p class="news-week-meta">{esc(meta)}</p>\n']
    if not items:
        parts.append('    <p class="section-intro">A quiet week. Nothing new met the bar.</p>\n')
    for key, label in THEMES.items():
        group = [i for i in items if i["theme"] == key]
        if not group:
            continue
        parts.append(f'    <div class="news-group">\n'
                     f'      <h3 class="news-theme">{esc(label)}</h3>\n'
                     f'      <ul class="news-list">\n')
        for i in group:
            parts.append(
                '        <li>\n'
                f'          <a class="news-title" href="{esc(i["url"], quote=True)}" rel="noopener">{esc(i["title"])}</a>\n'
                f'          <p class="news-meta">{esc(i["source"])} · '
                f'<time datetime="{esc(i["published"])}">{esc(short_date(i["published"]))}</time></p>\n'
                f'          <p class="news-summary">{esc(i["summary"])}</p>\n'
                '        </li>\n')
        parts.append('      </ul>\n    </div>\n')
    parts.append('  </div>\n</section>\n')
    return "".join(parts)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>News · Sovereign Source AI</title>
<meta name="description" content="News on AI sovereignty, vendor lock-in, open models, agent governance, AI supply chains, data regulation, and small-business data and agents.">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body>

<div class="ghost" aria-hidden="true">
  <span class="ghost-line">Sovereign Source AI</span>
  <span class="ghost-line">News</span>
</div>

<header class="header">
  <div class="header-inner">
    <a href="../index.html" class="logo" aria-label="Sovereign Source AI home">
      <img class="logo-mark" src="../logo.svg" alt="Sovereign Source AI" height="20" width="38">
      <span class="logo-text">Sovereign Source AI</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="../index.html#topics" class="nav-mid">Topics</a>
      <a href="../business/">For small business</a>
      <a href="../index.html#talk" class="nav-cta">Talk to us</a>
    </nav>
  </div>
</header>

<main>

<section class="hero news-hero">
  <div class="hero-inner">
    <h1 class="hero-title">News</h1>
    <p class="hero-def">
      What we are reading: AI sovereignty, lock-in, open models, agent governance,
      AI supply chains, data regulation, and small businesses putting their data to work.
    </p>
    <p class="hero-plain">
      An AI scan finds these each week and we check that every link opens. The summaries
      are machine-written, so read the source before quoting anything. The sources are not.
    </p>
  </div>
</section>

{scans}
</main>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo-text">Sovereign Source AI</span>
      <p class="footer-tagline">sovsrc.ai</p>
    </div>
    <nav class="footer-nav" aria-label="Footer navigation">
      <a href="../index.html">Home</a>
      <a href="../business/">For small business</a>
      <a href="../index.html#topics">Topics</a>
      <a href="../manifesto.html">The manifesto</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def main():
    files = sorted((f for f in DATA.glob("*.json") if re.fullmatch(r"\d{4}-\d{2}-\d{2}\.json", f.name)),
                   reverse=True)
    if not files:
        sys.exit(f"no scan files (YYYY-MM-DD.json) found in {DATA}")
    scans = []
    for f in files:
        scan = json.loads(f.read_text())
        if not isinstance(scan.get("kept"), list) or len(scan.get("window", [])) != 2:
            sys.exit(f"{f.name}: not a news scan file")
        for i in scan["kept"]:
            if i.get("theme") not in THEMES or not str(i.get("url", "")).startswith(("http://", "https://")):
                sys.exit(f"{f.name}: item with unknown theme or non-web URL: {i.get('title')!r}")
        scans.append(scan)
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(PAGE.replace("{scans}", "\n".join(render_scan(s) for s in scans)))
    print(f"wrote news/index.html from {len(scans)} scan(s), {sum(len(s['kept']) for s in scans)} items")


if __name__ == "__main__":
    main()
