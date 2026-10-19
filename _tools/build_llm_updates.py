#!/usr/bin/env python3
"""Build the llm/ section from the sovsrc.llm update entries.

Reads research/llm-updates/data/<id>.json from the svrnsrc.ai research repo
(written by tools/llm_updates/watch.py there, one entry for each commit to the
sovsrc.llm repository) and writes:

  llm/index.html   the sovsrc.llm landing page, with the latest updates
  llm/updates.html the stream, newest first, grouped by day
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

# Public full-length articles live outside the generated update directory.
PUBLIC_ARTICLES = {
    "docs/SUPER_ANTHROPOCENE_ARTICLE.md": (
        "https://sovsrc.si/docs/SUPER_ANTHROPOCENE_ARTICLE.html",
        "Read the full Super Anthropocene article and infographic",
    ),
}

esc = html.escape


def day(iso: str) -> str:
    d = dt.date.fromisoformat(iso[:10])
    return f"{d.day} {d.strftime('%b %Y')}"


def count(n: int, one: str, many: str) -> str:
    return f"{n} {one if n == 1 else many}"


def pushed(entry: dict) -> list[dict]:
    return [c for c in entry["commits"] if c["pushed"]]


def status(entry: dict) -> str:
    """Where the change is: on GitHub, or committed on the author's machine only."""
    if pushed(entry):
        return ", ".join(f'<a href="{esc(entry["repo"])}/commit/{c["sha"]}" rel="noopener">'
                         f'commit <code>{c["sha"][:7]}</code></a>' for c in pushed(entry))
    return "Committed, not on GitHub yet"


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
<link rel="stylesheet" href="../style.css?v=20261010">
</head>
<body{body}>

<div class="ghost" aria-hidden="true">
  <span class="ghost-line">Sovereign Source AI</span>
  <span class="ghost-line">sovsrc.llm</span>{ghost}
</div>

<header class="header">
  <div class="header-inner">
    <a href="../index.html" class="logo" aria-label="Sovereign Source AI home">
      <img class="logo-mark" src="../logo.svg" alt="Sovereign Source AI" height="20" width="38">
      <span class="logo-text">Sovereign Source AI</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
{nav}
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
      <a href="./">sovsrc.llm</a>
      <a href="updates.html">sovsrc.llm updates</a>
      <a href="feed.xml">Feed</a>
      <a href="../manifesto.html">The manifesto</a>
      <a href="mailto:hello@sovsrc.ai">hello@sovsrc.ai</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


STREAM_NAV = """      <a href="../news/" class="nav-mid">News</a>
      <a href="./">sovsrc.llm</a>
      <a href="updates.html">Updates</a>
      <a href="./#talk" class="nav-cta">Talk to us</a>"""


def head(title: str, desc: str, nav: str = STREAM_NAV, body: str = "", ghost: str = "") -> str:
    return HEAD.format(title=title, desc=desc, nav=nav, body=body, ghost=ghost)


def render_stream(entries: list[dict], repo: str) -> str:
    parts = [head(
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
        '    exists. This page gets a new entry for each commit to the\n'
        f'    <a href="{esc(repo)}" rel="noopener">repository</a>.\n'
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
    parts.append('\n  <a href="./" class="back-link">About sovsrc.llm</a>\n</article>\n' + FOOT)
    return "".join(parts)


# ------------------------------------------------------------------ landing
# The landing copy is fixed text drawn from the sovsrc.llm README. sovsrc.llm is at
# specification stage, so every plan, rate, and term here is described as a proposal.
LANDING_NAV = """      <a href="#how-it-works" class="nav-mid">How it works</a>
      <a href="#rewards" class="nav-mid">Rewards</a>
      <a href="#documents" class="nav-minor">Documents</a>
      <a href="updates.html">Updates</a>
      <a href="#talk" class="nav-cta">Talk to us</a>"""

LANDING_GHOST = """
  <span class="ghost-line">Permission before use.</span>
  <span class="ghost-line">Honest attribution.</span>
  <span class="ghost-line">Payment by agreement.</span>"""

FLOW = [
    ("A creator gives permission", "Each work has a record of the allowed purpose, recipients, territory, and duration."),
    ("The system checks the record", "The check is made before a work is used, and again before an answer goes out."),
    ("The use is recorded", "The credit receipt and the usage record are saved before the answer goes out. Agreed rewards are calculated from them."),
    ("The answer shows its sources", "Each answer comes with the evidence that supports it."),
]

SUBJECTS = [
    ("IP and source works", "Reviewed rights, scoped licenses, and evidence of use."),
    ("Ideas and research", "Concrete proposals, records of adoption, and agreed rewards."),
    ("Contributions", "Code, improvements, prompts, workflows, curation, and evaluation."),
    ("Influences", "Documented acknowledgments and lineage. Credit only, unless payment is expressly agreed."),
    ("Combined work", "Upstream obligations stay in place. New contributions are recorded separately."),
]

# (share of the contributor pool, track, proposed allocation basis)
TRACKS = [
    (60, "Training and licensed corpus", "Approved, deduplicated training exposure and quality weights that are set in advance."),
    (20, "Prompt and workflow reuse", "Verified paid executions of accepted versions."),
    (20, "Ideas, contributions, and influences", "Agreed adoption points with reviewed evidence. An influence share needs an explicit agreement."),
]
POOL_SHARE = 20  # percent of eligible collected revenue

COMMITMENTS = [
    ("Permission before use", "Each asset has a record of the allowed purpose, recipients, territory, and duration."),
    ("Honest attribution", "A verified quotation, a retrieved source, and an estimated influence are different things. The record says which one applies."),
    ("Voluntary syndicates", "Creators can join a group that administers their work under an accepted charter. Membership does not transfer ownership."),
    ("Private conversations", "Conversations are private by default. Shared training needs separate consent."),
    ("Reproducible payments", "The system keeps the event history, calculates exact amounts, and does not settle the same event twice."),
    ("Review and appeal", "Creators can dispute ownership, missing credit, and payments. They can revoke permission."),
]

DOCUMENTS = [
    ("docs/SOVEREIGN_SOURCE_AI_CODEX_SPEC.md", "Project and implementation specification",
     "The SIP framework, requirements, data records, APIs, milestones, and acceptance tests."),
    ("docs/SOLUTION_ARCHITECTURE.md", "Solution architecture",
     "Stack responsibilities, workflows, model selection, and training gates."),
    ("docs/FRONTIER_LAB_IP_AND_CREATOR_REWARDS_AUDIT.md", "Frontier lab terms audit",
     "Eight organizations compared on IP, training permissions, attribution, and compensation."),
    ("licenses/SS-SIP-0.1.md", "SS-SIP license draft",
     "A custom license draft for source sharing, contributor credit, and influence notices."),
    ("licenses/SYNDICATE-MARKETPLACE-TERMS-0.1.md", "Syndicate marketplace terms",
     "Opt-in listings, commissions, creator rewards, payouts, and appeals."),
]

MAILTO = "mailto:hello@sovsrc.ai?subject=sovsrc.llm"


def rows(items, cls: str, tag: str = "ul") -> str:
    """Rule-lined rows (title over description) in the shared index grid."""
    lis = "".join(f'      <li>\n        <span class="layer-title">{esc(t)}</span>\n'
                  f'        <span class="layer-desc">{esc(d)}</span>\n      </li>\n' for t, d in items)
    return f'    <{tag} class="layers {cls}">\n{lis}    </{tag}>\n'


def pool() -> str:
    """The proposed rewards pool, drawn to scale (see .pool in style.css)."""
    def labels(items, cols: str, cls: str = "") -> str:
        lis = "".join(f'        <li style="--share: {n}"><span class="pool-num">{n}%</span><span class="layer-title">{esc(t)}</span>'
                      f'<span class="layer-desc">{esc(d)}</span></li>\n' for n, t, d in items)
        return f'      <ul class="pool-labels{cls}" style="--cols: {cols}">\n{lis}      </ul>\n'

    rest = 100 - POOL_SHARE
    tracks = "".join(f'<span style="--share: {n}"></span>' for n, _, _ in TRACKS)
    return (
        '    <div class="pool">\n'
        + labels([(POOL_SHARE, "Creator rewards pool", "The proposed share for creators."),
                  (rest, "The rest of eligible revenue", "Outside the pool.")], f"{POOL_SHARE}fr {rest}fr", " pool-top")
        + f'      <div class="pool-bar" aria-hidden="true"><span style="--share: {POOL_SHARE}"></span>'
        f'<span class="pool-rest" style="--share: {rest}"></span></div>\n'
        + '      <svg class="pool-zoom" viewBox="0 0 100 100" preserveAspectRatio="none" aria-hidden="true">'
        f'<line x1="0" y1="0" x2="0" y2="100"/><line x1="{POOL_SHARE}" y1="0" x2="100" y2="100"/></svg>\n'
        f'      <div class="pool-bar pool-tracks-bar" aria-hidden="true">{tracks}</div>\n'
        + labels(TRACKS, " ".join(f"{n}fr" for n, _, _ in TRACKS))
        + '    </div>\n')


def section(sid: str, heading: str, intro: str, body: str, cls: str = "section") -> str:
    return (f'<section class="{cls}" id="{sid}">\n  <div class="section-inner">\n'
            f'    <h2 class="section-heading">{esc(heading)}</h2>\n'
            + (f'    <p class="section-intro">{intro}</p>\n' if intro else "")
            + body + '  </div>\n</section>\n\n')


def render_landing(entries: list[dict], repo: str) -> str:
    cta = (f'    <div class="cta-row">\n      <a class="btn" href="{MAILTO}">Email us about sovsrc.llm</a>\n'
           f'      <a class="btn-quiet" href="{esc(repo)}" rel="noopener">Read the specification on GitHub</a>\n    </div>\n')
    parts = [head(
        title="sovsrc.llm: an LLM that respects intellectual property and ideas",
        desc="sovsrc.llm is a specification for an LLM that uses source material with permission, gives credit, "
             "and proposes rewards for creators. It is at specification stage.",
        nav=LANDING_NAV, body=' class="biz llm"', ghost=LANDING_GHOST),
        '<section class="hero">\n  <div class="hero-inner">\n'
        '    <h1 class="hero-title">An LLM that respects intellectual property and ideas.</h1>\n'
        '    <p class="hero-sub">\n'
        '      sovsrc.llm is a specification for a large language model that uses source material with\n'
        '      permission, gives credit to the people who made it, and pays creators for agreed use.\n'
        '      The project is at specification stage. No application, trained model, or payment system exists.\n'
        '    </p>\n' + cta + '  </div>\n</section>\n\n']

    flow = "".join(f'      <li>\n        <span class="flow-label">{esc(t)}</span>\n'
                   f'        <span class="flow-desc">{esc(d)}</span>\n      </li>\n' for t, d in FLOW)
    parts.append(section(
        "how-it-works", "Permission first. Credit each time. Payment by agreement.",
        "The first planned product is a research assistant that answers from an approved set of documents. "
        "The specification puts the permission checks and the payment decisions outside the model.",
        f'    <ol class="flow" aria-label="From permission to answer">\n{flow}    </ol>\n'))

    parts.append(section(
        "sip", "What the project recognizes",
        "The specification calls its framework Super Intellectual Property (SIP). It recognizes more than formal "
        "rights, through evidence and agreements. It is a proposed framework. It does not claim that a new legal right exists.",
        rows(SUBJECTS, "subjects")
        + '    <div class="principle-callout">\n'
          '      <p class="principle">Ownership, permission, credit, governance, and payment are <strong>five separate records.</strong></p>\n'
          '      <p class="principle">A similarity score cannot establish ownership, permission, or payment eligibility.</p>\n'
          '    </div>\n'))

    parts.append(section(
        "rewards", "The proposed rewards pool, drawn to scale",
        f"The draft puts {POOL_SHARE}% of eligible collected revenue into a creator rewards pool. Eligible revenue is "
        "revenue after refunds, chargebacks, sales taxes, and payment fees. Three tracks divide the pool.",
        pool()
        + '    <p class="section-note">These are proposed contract terms, not legal royalty rates. Credit alone does not '
          'create a payout. The planned pilot labels each payout as simulated.</p>\n'))

    dl = "".join(f'      <div>\n        <dt>{esc(t)}</dt>\n        <dd>{esc(d)}</dd>\n      </div>\n' for t, d in COMMITMENTS)
    parts.append('<section class="formulations" aria-labelledby="commitments-heading">\n  <div class="formulations-inner">\n'
                 '    <h2 class="section-heading" id="commitments-heading">What the specification commits to</h2>\n'
                 f'    <dl class="guarantees">\n{dl}    </dl>\n  </div>\n</section>\n\n')

    docs = "".join(f'      <li>\n        <a class="toc-item" href="{esc(repo)}/blob/HEAD/{quote(path)}" rel="noopener">\n'
                   f'          <span class="toc-title">{esc(t)}</span>\n          <span class="toc-desc">{esc(d)}</span>\n'
                   '        </a>\n      </li>\n' for path, t, d in DOCUMENTS)
    parts.append(section(
        "documents", "What exists today",
        "The repository holds draft documents and no software. The license is a custom draft for legal review. "
        "It is not an OSI-approved license.",
        f'    <ul class="toc">\n{docs}    </ul>\n', cls="section questions-section"))

    if entries:
        latest = "".join(
            f'      <li>\n        <a class="toc-item" href="{e["id"]}.html">\n'
            f'          <span class="toc-num"><time datetime="{esc(e["when"])}">{day(e["when"])}</time></span>\n'
            f'          <span class="toc-title">{esc(e["title"])}</span>\n'
            f'          <span class="toc-desc">{esc(e["summary"])}</span>\n        </a>\n      </li>\n'
            for e in entries[:3])
        parts.append(section(
            "updates", "Latest changes",
            "Each commit to the repository gets a page. A machine writes the summaries from the change, "
            "so read the source before you quote a summary.",
            f'    <ul class="toc updates">\n{latest}    </ul>\n'
            '    <div class="cta-row">\n      <a class="btn-quiet" href="updates.html">See all updates</a>\n'
            '      <a class="btn-quiet" href="feed.xml">Follow the feed</a>\n    </div>\n'))

    parts.append(section(
        "talk", "Tell us what the specification gets wrong", "",
        '    <p class="claim-text">\n'
        '      The project is open for review. If you make source material, work on rights, or build models,\n'
        '      read the drafts and send us your objections.\n'
        '    </p>\n' + cta, cls="section claim-section").rstrip("\n") + "\n")
    text = " ".join(t + " " + d for t, d in FLOW + SUBJECTS + COMMITMENTS)
    if EXCLUDED.search(text):
        sys.exit("landing copy uses excluded-market language")
    return "".join(parts) + FOOT.replace("</main>\n", '</main>\n\n<script src="../home.js" defer></script>\n', 1)


def render_page(e: dict, newer: dict | None, older: dict | None) -> str:
    parts = [head(title=esc(e["title"]), desc=esc(e["summary"], quote=True)),
             '<article class="prose news">\n'
             f'  <h1>{esc(e["title"])}</h1>\n'
             f'  <p class="topic-summary">{esc(e["summary"])}</p>\n'
             f'  <p class="news-meta"><time datetime="{esc(e["when"])}">{day(e["when"])}</time> · {status(e)}</p>\n']
    for source_path, (url, label) in PUBLIC_ARTICLES.items():
        if any(f["path"] == source_path for f in e["files"]):
            parts.append(f'  <p><a href="{esc(url)}">{esc(label)}</a></p>\n')
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
    parts.append('  </nav>\n  <a href="updates.html" class="back-link">All updates</a>\n</article>\n' + FOOT)
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
    keep = {"index.html", "updates.html"} | {f'{e["id"]}.html' for e in entries}
    for old in OUT.glob("*.html"):
        if old.name not in keep:
            old.unlink()
    repo = entries[0]["repo"] if entries else "https://github.com/niccolox/sovsrc.llm-ip-ideas"
    (OUT / "index.html").write_text(render_landing(entries, repo))
    (OUT / "updates.html").write_text(render_stream(entries, repo))
    for i, e in enumerate(entries):
        (OUT / f'{e["id"]}.html').write_text(render_page(
            e, entries[i - 1] if i else None, entries[i + 1] if i + 1 < len(entries) else None))
    (OUT / "feed.xml").write_text(render_feed(entries))
    print(f"wrote llm/index.html, llm/updates.html, llm/feed.xml and {count(len(entries), 'update page', 'update pages')}"
          f" ({dropped} left out as excluded markets)")


if __name__ == "__main__":
    main()
