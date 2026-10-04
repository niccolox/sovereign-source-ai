#!/usr/bin/env python3
"""Generate the ad landing pages under lp/.

Each entry in PAGES becomes lp/<slug>/index.html, a single-purpose page for
Google and Meta ad traffic: one headline matched to the ad, the problem as the
visitor lives it today, what we build, what stays theirs, how it starts, and
one action (book a call). Pages are noindex and are not linked from the site
nav; they exist to receive ad clicks.

The booking link lives in one place, lp/lp.js. Until it is set, every
"Book a call" button falls back to an email with a page-specific subject, so
no page ever dead-ends.

Content follows PRODUCT.md: no prices, durations, clients, metrics or
testimonials. Examples describe what we build, not past work.

Usage: python3 _tools/build_landing.py
Jekyll skips _-prefixed folders, so this script is not published.
"""
import html
from pathlib import Path
from urllib.parse import quote

from excluded_markets import EXCLUDED

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "lp"
EMAIL = "niccolox@devekko.com"

# Shared across pages: what stays the customer's, and how an engagement starts.
GUARANTEES = [
    ("You own it", "The data, code, and credentials live in accounts you control."),
    ("You can leave", "Open formats and written documentation mean anyone can take over without a rebuild."),
    ("You can see what agents did", "Every action is recorded: what it read, what it proposed, and who approved it."),
    ("You choose the AI", "Nothing is tied to one model provider. You decide which models see what."),
]
STEPS = [
    ("A call about one task", "Tell us the job that eats your week and the tools it touches. We will say plainly whether it is worth building."),
    ("Build it in your accounts", "We set up the data and connections in accounts you own, starting with the tools that task needs."),
    ("Run it with a person in charge", "The agent drafts, checks, or flags. Someone on your team approves anything that matters."),
    ("Hand over", "You get the code, the documentation, and the access. Keep us on for support, or don't."),
]

PAGES = [
    {
        "slug": "invoices",
        "title": "Invoices read, matched and checked before approval",
        "description": "We build an agent that reads incoming invoices, matches them to vendors and purchase orders, flags anything unusual, and queues them for approval.",
        "ghost": ["Read. Match. Check.", "Nothing paid twice.", "Approved by you."],
        "h1": "Invoices in, checked, ready to approve.",
        "sub": "Invoices arrive as PDFs and email attachments, and someone types them into the accounting system. We build an agent that reads each one, matches it to the vendor and order, flags anything odd, and queues it for your approval.",
        "today_heading": "What accounts payable looks like today",
        "today": [
            ("Retyping PDFs", "Line items keyed in by hand from attachments."),
            ("Matching by eye", "Checking each invoice against the purchase order and the receipt."),
            ("Duplicates and drift", "Double-billed invoices and price changes slip through."),
            ("Approval by inbox", "Sign-off happens in email threads nobody can find later."),
        ],
        "build": [
            ("Read every invoice", "Vendor, amounts, dates and line items pulled from PDFs and email into structured records."),
            ("Match and check", "Each invoice is matched to its vendor and purchase order, and checked for duplicates and price changes."),
            ("Queue for approval", "Clean invoices wait for one click. Anything unusual is flagged with the reason. Nothing is paid without a person."),
        ],
    },
    {
        "slug": "morning-brief",
        "title": "A morning brief of what needs your attention today",
        "description": "We build an agent that looks across sales, jobs, cash and customer messages each morning and tells you what changed, why it matters, and what to do.",
        "ghost": ["What changed overnight?", "What matters today?", "What to do about it."],
        "h1": "What needs your attention today, on one page.",
        "sub": "The answer to \"what should I worry about this morning?\" is spread across five dashboards. We build an agent that reads them for you and writes a short brief: what changed, the evidence, why it matters, and a suggested next step.",
        "today_heading": "How you find problems today",
        "today": [
            ("Five dashboards", "Sales, jobs, cash, customer messages and ads, each in its own app."),
            ("Found too late", "A slipping project or a spike in complaints surfaces days after it starts."),
            ("Numbers that disagree", "Every tool counts jobs and revenue a little differently."),
            ("No time to look", "Busy weeks are exactly when nobody checks."),
        ],
        "build": [
            ("One copy of the numbers", "Your tools feed one warehouse in your account, so the figures agree."),
            ("A written brief", "Each morning: what changed, the evidence behind it, why it matters, and how confident the agent is."),
            ("Suggestions, not actions", "The brief recommends a next step. You decide what to do about it."),
        ],
    },
    {
        "slug": "own-your-data",
        "title": "One data warehouse for all your tools, in an account you own",
        "description": "We connect the SaaS tools you already pay for into one data warehouse in your own account, so reports stop being spreadsheets someone rebuilds by hand.",
        "ghost": ["One copy of the truth.", "In your account.", "Yours if you leave."],
        "h1": "All your business data, in one place you own.",
        "sub": "Jobs in one app, invoices in another, customers in a third. We connect the tools you already use into one warehouse in your own cloud account, so the numbers line up and the weekly spreadsheet goes away.",
        "today_heading": "What scattered data costs today",
        "today": [
            ("The weekly spreadsheet", "Someone exports, pastes and fixes the same report every week."),
            ("Three versions of a customer", "The same person spelled three ways across three systems."),
            ("Data you rent", "Your history lives in vendors' clouds, on their terms."),
            ("Nothing for AI to stand on", "Agents are only as good as the data they can read."),
        ],
        "build": [
            ("A warehouse in your account", "Your data in open formats such as Postgres, in a cloud account you own."),
            ("Connectors to your tools", "Pulls from accounting, CRM, payments, scheduling and project tools, then cleans and matches records."),
            ("Reports that rebuild themselves", "The numbers you check every week, refreshed on their own and consistent across tools."),
        ],
    },
    {
        "slug": "where-to-start",
        "title": "AI for your business: find the one job worth automating first",
        "description": "Not sure where AI fits in your business? Start with one conversation about the work that eats your week, and get a plain answer on whether it is worth building.",
        "ghost": ["Where does AI fit?", "Start with one task.", "A plain answer."],
        "h1": "Find the one job AI should take off your plate.",
        "sub": "You don't need an AI strategy. You need to know which repetitive job is worth handing to an agent, and which isn't. Start with a conversation about your week, and get a plain answer.",
        "today_heading": "Why AI hasn't stuck yet",
        "today": [
            ("A chatbot nobody uses", "Generic tools that don't know your business or your data."),
            ("Too many options", "Every vendor says AI. None says where to start."),
            ("Fear of lock-in", "Handing your process to a tool you can't leave."),
            ("No one to build it", "Your team runs the business. Nobody has time to wire AI into it."),
        ],
        "build": [
            ("A map of your work", "Where the hours go, which tools are involved, and which jobs repeat."),
            ("A short list, ranked", "The jobs where an agent would help, and the ones where it wouldn't, with the reasons."),
            ("One built for real", "If one is worth it, we build it in your accounts, with a person approving what matters."),
        ],
    },
    {
        "slug": "professional-services",
        "title": "AI for professional services firms: less admin, more billable work",
        "description": "We build agents for professional services firms: client intake, first drafts from your templates, and time and billing checks before invoices go out.",
        "ghost": ["Intake. Draft. Bill.", "From your templates.", "Reviewed by you."],
        "h1": "Less admin between you and billable work.",
        "sub": "Intake forms, first drafts and billing cleanup eat the hours you'd rather bill. We build agents that gather client documents, draft from your own templates, and check time against invoices before they go out.",
        "today_heading": "Where the unbilled hours go",
        "today": [
            ("Chasing documents", "Intake by email, with missing pieces found late."),
            ("Blank-page drafts", "Letters, proposals and reports started from scratch, again."),
            ("Billing cleanup", "Time entries reconciled by hand before every invoice run."),
            ("Reporting by spreadsheet", "Pipeline and utilization pulled from CRM and accounting manually."),
        ],
        "build": [
            ("Intake that finishes itself", "Gathers client documents, checks what's missing, and flags possible conflicts for review."),
            ("First drafts from your templates", "Letters, proposals and reports drafted in your format, for a professional to edit and sign."),
            ("Billing checked before it goes", "Time and expenses reconciled against engagements, with gaps flagged before invoices go out."),
        ],
    },
    {
        "slug": "field-services",
        "title": "AI for contractors and local services: quotes, scheduling, job costing",
        "description": "We build agents for field and local service businesses: quote drafts from job notes, scheduling suggestions, review replies, and job costing tied to invoices.",
        "ghost": ["Walk the job.", "Quote the same day.", "Know what it cost."],
        "h1": "Quotes out the same day you walk the job.",
        "sub": "Quotes wait until the evening, schedules live on a whiteboard, and nobody knows what a job really cost until tax time. We build agents that draft quotes from your notes and past prices, and tie hours and materials back to every invoice.",
        "today_heading": "Where the evenings go",
        "today": [
            ("Quotes after dark", "Notes from the site turned into a quote at the kitchen table."),
            ("Scheduling by phone", "Crews, travel and callbacks juggled by memory."),
            ("Reviews left unanswered", "No time to reply, good or bad."),
            ("Guessing job margins", "Hours and materials never tied back to the invoice."),
        ],
        "build": [
            ("Quote drafts from job notes", "Photos and notes turned into a quote using your past pricing, ready for you to adjust and send."),
            ("Scheduling suggestions", "Proposed schedules that account for crews, travel and job length. You confirm."),
            ("Job costing that adds up", "Hours and materials matched to each invoice, so you know which jobs pay."),
        ],
    },
    {
        "slug": "compliance",
        "title": "Compliance checks recorded, reviewed and ready for an audit",
        "description": "We build agents that check documents against your rules, track privacy and data requests, and keep an audit trail of what was checked, by whom, and when.",
        "ghost": ["Checked against your rules.", "Reviewed by a person.", "On file for the audit."],
        "h1": "Every check recorded. Every approval on file.",
        "sub": "Compliance work is careful, repetitive, and has to be provable later. We build agents that check documents against your own rules and flag issues for review, with a record of what was checked, by whom, and when.",
        "today_heading": "What compliance work looks like today",
        "today": [
            ("Checklists by hand", "Documents checked line by line against rules in a binder."),
            ("Requests in an inbox", "Privacy and data requests tracked in email, with deadlines at risk."),
            ("Proof assembled later", "Audit evidence rebuilt from memory when someone asks."),
            ("Policies nobody can find", "Staff ask the same procedure questions again and again."),
        ],
        "build": [
            ("Checks against your rules", "Documents and labels checked against your requirements, with issues flagged for a reviewer. The agent never signs off."),
            ("Requests tracked to completion", "Privacy and data requests logged, routed and followed until they're closed."),
            ("An audit trail by default", "Every check records what was read, what was found, and who approved it."),
        ],
    },
    {
        "slug": "no-lock-in",
        "title": "Use AI without handing your business to a vendor",
        "description": "We build AI agents on your data, in your accounts, written down so you can switch models or vendors without starting over.",
        "ghost": ["Your logic. Your data.", "Any model.", "Free to leave."],
        "h1": "Use AI without handing over your business.",
        "sub": "Most AI tools want your data in their cloud and your process in their prompts. When prices change or the tool disappears, you start over. We build agents on your data, in your accounts, so you can change the model or the vendor and keep everything that matters.",
        "today_heading": "What AI tools quietly take",
        "today": [
            ("Your data", "Copied into a vendor's cloud, on their terms."),
            ("Your process", "Business rules buried in someone else's prompts and workflows."),
            ("Your choice of model", "Locked to whichever AI the tool picked for you."),
            ("Your exit", "Leaving means rebuilding from scratch."),
        ],
        "build": [
            ("Your rules, written down", "How your business decides things, captured as plain, documented logic you own, not hidden in prompts."),
            ("Any model, swappable", "Agents work with hosted or open models. Change providers without rewriting the business logic."),
            ("Everything in your accounts", "Data, code and credentials in accounts you control, handed over with documentation."),
        ],
    },
    {
        "slug": "knowledge-search",
        "title": "Answers from your own documents, with the source attached",
        "description": "We build an agent that answers staff questions from your own procedures, contracts and past work, and shows exactly where each answer came from.",
        "ghost": ["Ask once.", "Answered from your files.", "Source attached."],
        "h1": "Answers from your own documents, not the internet.",
        "sub": "Your procedures, contracts, price sheets and past work hold most of the answers your team needs. They're just scattered across drives and inboxes. We build an agent that answers from your own files and shows the source, so people can check it.",
        "today_heading": "How answers get found today",
        "today": [
            ("Ask the one who knows", "The same questions go to the same person, all day."),
            ("Search five places", "Drives, inboxes, wikis and old tickets, one at a time."),
            ("Out-of-date copies", "Three versions of the procedure, and nobody sure which is current."),
            ("Knowledge that walks out", "When someone leaves, what they knew leaves with them."),
        ],
        "build": [
            ("Your documents, indexed", "Procedures, contracts, price sheets and past work gathered from where they already live, in your account."),
            ("Answers with sources", "Every answer links to the document and passage it came from, so anyone can check it."),
            ("Access you control", "People only get answers from documents they're allowed to see. Nothing is shared with a vendor's training set."),
        ],
    },
    {
        "slug": "lead-follow-up",
        "title": "Every inquiry answered while it's still warm",
        "description": "We build an agent that reads each new inquiry, sorts it, drafts a reply with the right next step, and logs it in your CRM, for a person to send.",
        "ghost": ["Every inquiry.", "Answered the same day.", "Logged where it belongs."],
        "h1": "Every inquiry answered while it's still warm.",
        "sub": "Inquiries arrive by web form, email and phone message, and the good ones wait behind the rest. We build an agent that reads each one, sorts it, drafts a reply with the right next step, and logs it in your CRM. A person sends it.",
        "today_heading": "Where new business slips today",
        "today": [
            ("Replies a day late", "Inquiries sit until someone has a free hour."),
            ("Every lead looks the same", "The serious ones wait behind the tire-kickers."),
            ("The CRM is behind", "Notes live in inboxes, not where the team can see them."),
            ("No follow-up", "Quiet leads are forgotten instead of nudged."),
        ],
        "build": [
            ("Each inquiry read and sorted", "Web forms, email and messages gathered in one queue, sorted by fit and urgency using rules you set."),
            ("A reply drafted", "A reply in your voice with the right next step: a booking link, a question, or a polite no. A person sends it."),
            ("Logged and followed up", "Every inquiry recorded in your CRM, with follow-up reminders for the ones that go quiet."),
        ],
    },
]

def e(text: str) -> str:
    return html.escape(text, quote=True)


def mailto(page: dict) -> str:
    subject = quote(f"One task: {page['slug'].replace('-', ' ')}")
    return f"mailto:{EMAIL}?subject={subject}"


def rows(items, num=False) -> str:
    out = []
    for i, (title, desc) in enumerate(items, 1):
        n = f'\n        <span class="layer-num">{i:02d}</span>' if num else ""
        out.append(
            f"      <li>{n}\n"
            f'        <span class="layer-title">{e(title)}</span>\n'
            f'        <span class="layer-desc">{e(desc)}</span>\n'
            f"      </li>"
        )
    return "\n".join(out)


def render(p: dict) -> str:
    ghost = "\n".join(f'  <span class="ghost-line">{e(g)}</span>' for g in ["Sovereign Source AI", *p["ghost"]])
    guarantees = "\n".join(
        f"      <div>\n        <dt>{e(t)}</dt>\n        <dd>{e(d)}</dd>\n      </div>" for t, d in GUARANTEES
    )
    book = f'<a class="btn" href="{e(mailto(p))}" data-book>Book a call</a>'
    email = f'<a class="btn-quiet" href="{e(mailto(p))}">Or email us</a>'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<!-- Generated by _tools/build_landing.py; edit the script, not this file. -->
<title>{e(p['title'])} · Sovereign Source AI</title>
<meta name="description" content="{e(p['description'])}">
<meta name="robots" content="noindex">
<link rel="icon" type="image/svg+xml" href="../../favicon.svg">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Instrument+Sans:ital,wght@0,400..700;1,400..700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../../style.css">
</head>
<body class="biz lp">

<div class="ghost" aria-hidden="true">
{ghost}
</div>

<header class="header">
  <div class="header-inner">
    <a href="../../index.html" class="logo" aria-label="Sovereign Source AI home">
      <img class="logo-mark" src="../../logo.svg" alt="Sovereign Source AI" height="20" width="38">
      <span class="logo-text">Sovereign Source AI</span>
    </a>
    <nav class="nav" aria-label="Main navigation">
      <a href="{e(mailto(p))}" class="nav-cta" data-book>Book a call</a>
    </nav>
  </div>
</header>

<main>

<section class="hero">
  <div class="hero-inner">
    <h1 class="hero-title">{e(p['h1'])}</h1>
    <p class="hero-sub">{e(p['sub'])}</p>
    <div class="cta-row">
      {book}
      <a class="btn-quiet" href="#what-we-build">See what we build</a>
    </div>
  </div>
</section>

<section class="section" id="today">
  <div class="section-inner">
    <h2 class="section-heading">{e(p['today_heading'])}</h2>
    <ul class="layers">
{rows(p['today'])}
    </ul>
  </div>
</section>

<section class="section" id="what-we-build">
  <div class="section-inner">
    <h2 class="section-heading">What we build</h2>
    <p class="section-intro">Built in accounts you own. The agent drafts, checks, or flags; a person makes the call.</p>
    <ol class="layers offer">
{rows(p['build'])}
    </ol>
  </div>
</section>

<section class="formulations" aria-labelledby="guarantees-heading">
  <div class="formulations-inner">
    <h2 class="section-heading" id="guarantees-heading">Built so you are never stuck</h2>
    <dl class="guarantees">
{guarantees}
    </dl>
  </div>
</section>

<section class="section" id="how-it-starts">
  <div class="section-inner">
    <h2 class="section-heading">How it starts</h2>
    <ol class="layers steps">
{rows(STEPS, num=True)}
    </ol>
  </div>
</section>

<section class="section claim-section" id="talk">
  <div class="section-inner">
    <h2 class="section-heading">Start with one task</h2>
    <p class="claim-text">
      Sovereign Source AI is new, so we take on a few businesses at a time. Book a call,
      tell us the job you'd most like off your plate, and we will tell you plainly
      whether it is worth building.
    </p>
    <div class="cta-row">
      {book}
      {email}
    </div>
  </div>
</section>

</main>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-brand">
      <span class="footer-logo-text">Sovereign Source AI</span>
      <p class="footer-tagline">sovsrc.ai</p>
    </div>
    <nav class="footer-nav" aria-label="Footer navigation">
      <a href="../../index.html">Home</a>
      <a href="../../business/">What we build</a>
      <a href="../../manifesto.html">Manifesto</a>
      <a href="mailto:{EMAIL}">{EMAIL}</a>
    </nav>
  </div>
</footer>

<script src="../lp.js"></script>
</body>
</html>
"""



def check(p: dict) -> None:
    assert len(p["today"]) == 4 and len(p["build"]) == 3, p["slug"]
    hit = EXCLUDED.search(render(p))
    assert not hit, f"{p['slug']}: excluded-market term {hit.group(0)!r}"


def main() -> None:
    slugs = [p["slug"] for p in PAGES]
    assert len(slugs) == len(set(slugs)), "duplicate slug"
    for p in PAGES:
        check(p)
        d = OUT / p["slug"]
        d.mkdir(parents=True, exist_ok=True)
        (d / "index.html").write_text(render(p))
    print(f"wrote {len(PAGES)} pages to {OUT.relative_to(SITE)}/")


if __name__ == "__main__":
    main()
