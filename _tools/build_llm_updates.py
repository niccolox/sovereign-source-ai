#!/usr/bin/env python3
"""Build the llm/ section from the sovsrc.llm update entries.

Reads research/llm-updates/data/<id>.json from the svrnsrc.ai research repo
(written by tools/llm_updates/watch.py there, one entry for each change to the
sovsrc.llm repository) and writes:

  llm/index.html   the stream, newest first, grouped by day
  llm/<id>.html    one page for each change
  llm/feed.xml     an Atom feed of the same entries

Pages whose entry is gone are removed. Entries that use excluded-market language
(see excluded_markets.py) are left out. Commit and file links go to GitHub only
for commits that are pushed.

Usage: python3 _tools/build_llm_updates.py [DATA_DIR]
DATA_DIR defaults to ~/Projects/svrnsrc.ai/research/llm-updates/data.
Jekyll skips _-prefixed folders, so this script is not published.
"""
import datetime as dt
import html
import json
import sys
from pathlib import Path
from urllib.parse import quote

from excluded_markets import EXCLUDED

SITE = Path(__file__).resolve().parent.parent
DATA = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else (
    Path.home() / "Projects/svrnsrc.ai/research/llm-updates/data")
OUT = SITE / "llm"
BASE_URL = "https://sovsrc.ai/llm/"
FEED_ITEMS = 30

esc = html.escape


def day(iso: str) -> str:
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.day} {d.strftime('%b %Y')}"


def count(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def pushed(entry: dict) -> list[dict]:
    return [c for c in entry["commits"] if c["pushed"]]


def status(entry: dict) -> str:
    """Where the change is: on GitHub, committed on the author's machine, or not committed."""
    if pushed(entry):
        return ", ".join(f'<a href="{esc(entry["repo"])}/commit/{c["sha"]}" rel="noopener">'
                         f'commit <code>{c["sha"][:7]}</code></a>' for c in pushed(entry))
    return "Committed, not on GitHub yet" if entry["commits"] else "Draft, not committed yet"


def file_ref(entry: dict, path: str) -> str:
    """Link to the file as of the newest pushed commit; plain text when there is none."""
    f = next(f for f in entry["files"] if f["path"] == path)
    if not pushed(entry) or f["status"] == "deleted":
        return f"<code>{esc(path)}</code>"
    return (f'<a href="{esc(entry["repo"])}/blob/{pushed(entry)[-1]["sha"]}/{quote(path)}" rel="noopener">'
            f"<code>{esc(path)}</code></a>")


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Sovereign Source AI</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="alternate" type="application/atom+xml" title="sovsrc.llm updates" href="feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css?v=20261005">
</head>
<body>

<div class="ghost" aria-hidden="true">
  <span class="ghost-line">Sovereign Source AI</span>
  <span class="ghost-line">sovsrc.llm</span>
</div>

<header class="header">
  <div class="header-inner">
    <a href="../index.html" class="logo" aria-label="Sovereign Source AI home">
      <img class="logo-mark" src="../logo.svg" alt="Sovereign Source AI" height="20" width="38">
      <span class="logo-text">Sovereign Source AI</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="../news/" class="nav-mid">News</a>
      <a href="./">sovsrc.llm updates</a>
      <a href="../index.html#talk" class="nav-cta">Talk to us</a>
    </nav>
  </div>
</header>

<main>
"""

FOOT = """</main>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo-text">Sovereign Source AI</span>
      <p class="footer-tagline">sovsrc.ai</p>
    </div>
    <nav class="footer-nav" aria-label="Footer navigation">
      <a href="../index.html">Home</a>
      <a href="../news/">News</a>
      <a href="./">sovsrc.llm updates</a>
      <a href="feed.xml">Feed</a>
      <a href="../manifesto.html">The manifesto</a>
      <a href="mailto:hello@sovsrc.ai">hello@sovsrc.ai</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def render_index(entries: list[dict], repo: str) -> str:
    parts = [HEAD.format(
        title="sovsrc.llm updates",
        desc="Each change to the sovsrc.llm specification: an LLM project that uses source material "
             "with permission, gives credit, and plans rewards for creators."),
        '<article class="prose news">\n'
        '  <h1>sovsrc.llm updates</h1>\n'
        '  <p class="topic-summary">\n'
        '    sovsrc.llm is a specification for an LLM that uses source material with permission,\n'
        '    gives credit to the people who made it, and plans rewards for creators.\n'
        '  </p>\n'
        '  <p>\n'
        '    The project is at specification stage. No application, trained model, or payment system\n'
        '    exists. This page gets a new entry each time the\n'
        f'    <a href="{esc(repo)}" rel="noopener">repository</a> changes.\n'
        '    A machine writes the summaries from the change, so read the source before you quote a summary.\n'
        '  </p>\n']
    days: dict[str, list[dict]] = {}
    for e in entries:
        days.setdefault(e["when"][:10], []).append(e)
    for d, group in days.items():
        parts.append(f'\n  <section class="news-scan" id="day-{d}">\n'
                     f'    <h2>{day(d)}</h2>\n'
                     f'    <p class="news-week-meta">{count(len(group), "update", "updates")}</p>\n'
                     '    <ul class="news-list">\n')
        for e in group:
            parts.append(
                '      <li>\n'
                f'        <a class="news-title" href="{e["id"]}.html">{esc(e["title"])}</a>\n'
                f'        <p class="news-meta">{status(e)} · {count(len(e["files"]), "file", "files")}</p>\n'
                f'        <p class="news-summary">{esc(e["summary"])}</p>\n'
                '      </li>\n')
        parts.append('    </ul>\n  </section>\n')
    if not entries:
        parts.append('  <p>No update is published yet.</p>\n')
    parts.append('\n  <a href="../index.html" class="back-link">Back to home</a>\n</article>\n' + FOOT)
    return "".join(parts)


def render_page(e: dict, newer: dict | None, older: dict | None) -> str:
    parts = [HEAD.format(title=esc(e["title"]), desc=esc(e["summary"], quote=True)),
             '<article class="prose news">\n'
             f'  <h1>{esc(e["title"])}</h1>\n'
             f'  <p class="topic-summary">{esc(e["summary"])}</p>\n'
             f'  <p class="news-meta"><time datetime="{esc(e["when"])}">{day(e["when"])}</time> · {status(e)}</p>\n']
    for c in e["changes"]:
        refs = ", ".join(file_ref(e, p) for p in c["paths"])
        parts.append(f'\n  <h2>{esc(c["heading"])}</h2>\n'
                     f'  <p>{esc(c["detail"])}</p>\n'
                     f'  <p class="news-meta">{refs}</p>\n')
    parts.append('\n  <h2>Files in this change</h2>\n'
                 '  <div class="table-wrap"><table>\n'
                 '    <thead><tr><th>File</th><th>Change</th><th>Lines</th></tr></thead>\n    <tbody>\n')
    for f in e["files"]:
        parts.append(f'      <tr><td>{file_ref(e, f["path"])}</td><td>{esc(f["status"])}</td>'
                     f'<td>+{f["added"]} −{f["deleted"]}</td></tr>\n')
    parts.append('    </tbody>\n  </table></div>\n')
    note = ("A machine wrote this summary from the change. Read the source before you quote it."
            if e["written_by"] == "model" else
            "This page lists the change from the commit record. It has no written summary.")
    parts.append(f'  <p class="news-meta">{note}</p>\n\n'
                 '  <nav class="pager" aria-label="Update navigation">\n')
    for cls, label, other in (("pager-prev", "Older", older), ("pager-next", "Newer", newer)):
        parts.append(f'    <a class="{cls}" href="{other["id"]}.html"><span class="pager-label">{label}</span>'
                     f'{esc(other["title"])}</a>\n' if other else '    <span></span>\n')
    parts.append('  </nav>\n  <a href="./" class="back-link">All updates</a>\n</article>\n' + FOOT)
    return "".join(parts)


def render_feed(entries: list[dict]) -> str:
    def stamp(e: dict) -> str:
        return dt.datetime.fromisoformat(e["updated"]).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    parts = ['<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">\n'
             '  <title>sovsrc.llm updates</title>\n'
             f'  <id>{BASE_URL}</id>\n'
             f'  <link href="{BASE_URL}"/>\n'
             f'  <link rel="self" href="{BASE_URL}feed.xml"/>\n'
             '  <author><name>Sovereign Source AI</name></author>\n'
             f'  <updated>{max(map(stamp, entries), default="1970-01-01T00:00:00Z")}</updated>\n']
    for e in entries[:FEED_ITEMS]:
        url = f'{BASE_URL}{e["id"]}.html'
        parts.append(f'  <entry>\n    <title>{esc(e["title"])}</title>\n    <id>{url}</id>\n'
                     f'    <link href="{url}"/>\n    <updated>{stamp(e)}</updated>\n'
                     f'    <summary>{esc(e["summary"])}</summary>\n  </entry>\n')
    parts.append('</feed>\n')
    return "".join(parts)


def load() -> tuple[list[dict], int]:
    entries, dropped = [], 0
    for f in sorted(DATA.glob("*.json")):
        e = json.loads(f.read_text())
        try:
            paths = {x["path"] for x in e["files"]}
            ok = (e["id"] == f.stem and e["repo"].startswith("https://github.com/")
                  and e["written_by"] in ("model", "rules")
                  and all(set(c["paths"]) <= paths for c in e["changes"])
                  and all(len(c["sha"]) == 40 and isinstance(c["pushed"], bool) for c in e["commits"]))
            dt.datetime.fromisoformat(e["when"]), dt.datetime.fromisoformat(e["updated"])
            text = " ".join([e["title"], e["summary"]] + [c["heading"] + " " + c["detail"] for c in e["changes"]])
        except (KeyError, TypeError, ValueError):
            ok = False
        if not ok:
            sys.exit(f"{f.name}: not an update entry")
        if EXCLUDED.search(text):
            dropped += 1
            continue
        entries.append(e)
    entries.sort(key=lambda e: dt.datetime.fromisoformat(e["when"]), reverse=True)
    return entries, dropped


def main():
    if not DATA.is_dir():
        sys.exit(f"no update data folder at {DATA}")
    entries, dropped = load()
    OUT.mkdir(exist_ok=True)
    keep = {"index.html"} | {f'{e["id"]}.html' for e in entries}
    for old in OUT.glob("*.html"):
        if old.name not in keep:
            old.unlink()
    repo = entries[0]["repo"] if entries else "https://github.com/niccolox/sovsrc.llm-ip-ideas"
    (OUT / "index.html").write_text(render_index(entries, repo))
    for i, e in enumerate(entries):
        (OUT / f'{e["id"]}.html').write_text(render_page(
            e, entries[i - 1] if i else None, entries[i + 1] if i + 1 < len(entries) else None))
    (OUT / "feed.xml").write_text(render_feed(entries))
    print(f"wrote llm/index.html, llm/feed.xml and {count(len(entries), 'update page', 'update pages')}"
          f" ({dropped} left out as excluded markets)")


if __name__ == "__main__":
    main()
