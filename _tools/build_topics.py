#!/usr/bin/env python3
"""Regenerate the topic pages and the homepage table of contents.

Reads the numbered markdown pages (NN-slug.md) from the svrnsrc.ai research
repo and writes topics/<slug>.html, then rewrites the <ol class="toc"> block
in index.html. Handles the markdown subset those pages use: #/## headings,
paragraphs, - and 1. lists, pipe tables, **bold**, *italic*, `code`, and
[links](x.md).

Usage: python3 _tools/build_topics.py [SOURCE_DIR]
SOURCE_DIR defaults to ~/Projects/svrnsrc.ai/research/docs/sovereign-source-ai.
Jekyll skips _-prefixed folders, so this script is not published.
"""
import html
import re
import sys
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
SRC = Path(sys.argv[1]).expanduser() if len(sys.argv) > 1 else (
    Path.home() / "Projects/svrnsrc.ai/research/docs/sovereign-source-ai")
OUT = SITE / "topics"


TITLES: dict[str, str] = {}  # slug -> page title, filled before rendering


def slug(md_name: str) -> str:
    return re.sub(r"^\d+-", "", md_name).removesuffix(".md")


def inline(text: str) -> str:
    t = html.escape(text, quote=False)
    t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![*\w])\*([^*\s][^*]*)\*(?!\*)", r"<em>\1</em>", t)

    def link(m):
        label, href = m.group(1), m.group(2)
        if href.endswith(".md"):
            # Cross-page links always show the target page's own title.
            label = html.escape(TITLES.get(slug(href), label))
            href = slug(href) + ".html"
        return f'<a href="{html.escape(href)}">{label}</a>'

    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)


SOURCES = {
    "sovereign-source-ai-manifesto": "Manifesto",
    "sovereign-source-ai-master-summary": "Master summary",
    "4": "Four-plane architecture notes",
}
CITE = re.compile(r"\s*[(\[]`?(" + "|".join(re.escape(k) for k in SOURCES) + r")\.md`?[)\]]\s*$")


def cite(item: str) -> str:
    """Turn a trailing (`file.md`) or [file.md] source tag into a readable <cite>."""
    m = CITE.search(item)
    if not m:
        return inline(item)
    return f'{inline(item[:m.start()])} <cite>{SOURCES[m.group(1)]}</cite>'


def render(md: str) -> tuple[str, str, str]:
    """Return (title, summary_text, body_html). Body excludes the H1."""
    lines = md.splitlines()
    title = lines[0].lstrip("# ").strip()
    out, para, i = [], [], 1
    summary = None

    def flush():
        nonlocal summary
        if para:
            text = " ".join(para)
            if summary is None:
                summary = text
                out.append(f'<p class="topic-summary">{inline(text)}</p>')
            else:
                out.append(f"<p>{inline(text)}</p>")
            para.clear()

    while i < len(lines):
        ln = lines[i]
        if not ln.strip():
            flush(); i += 1; continue
        if ln.startswith("## "):
            flush()
            h = ln[3:].strip()
            hid = re.sub(r"[^a-z0-9]+", "-", h.lower()).strip("-")
            out.append(f'<h2 id="{hid}">{inline(h)}</h2>')
            i += 1; continue
        if ln.startswith("|"):
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            head, body = rows[0], [r for r in rows[1:] if not all(re.fullmatch(r":?-+:?", c) for c in r)]
            t = ['<div class="table-wrap"><table>', "<thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in body:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table></div>")
            out.append("".join(t)); continue
        m_ul, m_ol = re.match(r"^- (.*)", ln), re.match(r"^\d+\. (.*)", ln)
        if m_ul or m_ol:
            flush()
            tag, pat = ("ul", r"^- (.*)") if m_ul else ("ol", r"^\d+\. (.*)")
            items = []
            while i < len(lines) and (re.match(pat, lines[i]) or (lines[i].startswith("  ") and items)):
                m = re.match(pat, lines[i])
                if m: items.append(m.group(1))
                else: items[-1] += " " + lines[i].strip()
                i += 1
            out.append(f"<{tag}>" + "".join(f"<li>{cite(x)}</li>" for x in items) + f"</{tag}>")
            continue
        para.append(ln.strip()); i += 1
    flush()
    return title, summary or "", "\n".join(out)


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} · Sovereign Source AI</title>
<meta name="description" content="{desc}">
<link rel="icon" type="image/svg+xml" href="../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css?v=20261005">
</head>
<body>

<div class="ghost" aria-hidden="true">
  <span class="ghost-line">Sovereign Source AI</span>
  <span class="ghost-line">Topics</span>
</div>

<header class="header">
  <div class="header-inner">
    <a href="../index.html" class="logo" aria-label="Sovereign Source AI home">
      <img class="logo-mark" src="../logo.svg" alt="Sovereign Source AI" height="20" width="38">
      <span class="logo-text">Sovereign Source AI</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="../index.html#the-architecture">The architecture</a>
      <a href="../index.html#topics">Topics</a>
      <a href="../manifesto.html" class="nav-cta">Read the manifesto</a>
    </nav>
  </div>
</header>

<main>
<article class="prose topic">
  <h1>{title}</h1>
{body}
  <nav class="pager" aria-label="Topic navigation">
    {prev}
    {next}
  </nav>
  <a href="../index.html#topics" class="back-link">All topics</a>
</article>
</main>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo-text">Sovereign Source AI</span>
      <p class="footer-tagline">sovsrc.ai</p>
    </div>
    <nav class="footer-nav" aria-label="Footer navigation">
      <a href="../index.html">Home</a>
      <a href="../manifesto.html">The manifesto</a>
      <a href="../news/">News</a>
      <a href="mailto:hello@sovsrc.ai">hello@sovsrc.ai</a>
    </nav>
  </div>
</footer>

</body>
</html>
"""


def main():
    files = sorted(SRC.glob("[0-9][0-9]-*.md"))
    if not files:
        sys.exit(f"no NN-*.md pages found in {SRC}")
    OUT.mkdir(exist_ok=True)
    for f in files:
        TITLES[slug(f.name)] = f.read_text().splitlines()[0].lstrip("# ").strip()
    pages = []
    for f in files:
        title, summary, body = render(f.read_text())
        pages.append((f.name, slug(f.name), title, summary, body))
    total = len(pages)
    for idx, (_, s, title, summary, body) in enumerate(pages):
        prev = next_ = "<span></span>"
        if idx > 0:
            p = pages[idx - 1]
            prev = f'<a class="pager-prev" href="{p[1]}.html"><span class="pager-label">Previous</span>{html.escape(p[2])}</a>'
        if idx < total - 1:
            n = pages[idx + 1]
            next_ = f'<a class="pager-next" href="{n[1]}.html"><span class="pager-label">Next</span>{html.escape(n[2])}</a>'
        first_sentence = re.split(r"(?<=\.)\s", summary, maxsplit=1)[0]
        (OUT / f"{s}.html").write_text(PAGE.format(
            title=html.escape(title), desc=html.escape(first_sentence, quote=True),
            num=f"{idx + 1:02d}", total=total, body=body, prev=prev, next=next_))
    # Homepage table of contents
    cards = []
    for idx, (_, s, title, summary, _) in enumerate(pages):
        first_sentence = re.split(r"(?<=\.)\s", summary, maxsplit=1)[0]
        cards.append(
            f'      <li>\n        <a class="toc-item" href="topics/{s}.html">\n'
            f'          <span class="toc-num">{idx + 1:02d}</span>\n'
            f'          <span class="toc-title">{html.escape(title)}</span>\n'
            f'          <span class="toc-desc">{inline(first_sentence)}</span>\n'
            f'        </a>\n      </li>')
    index = SITE / "index.html"
    toc = re.compile(r'(    <ol class="toc">\n).*?(\n    </ol>\n)', re.S)
    page, n = toc.subn(lambda m: m.group(1) + "\n".join(cards) + m.group(2), index.read_text())
    if n != 1:
        sys.exit('index.html: expected exactly one <ol class="toc"> block')
    index.write_text(page)
    print(f"wrote {total} topic pages and the index.html table of contents")


if __name__ == "__main__":
    main()
