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
EMAIL = "hello@sovsrc.ai"

# Shared across pages: what stays the customer's, and how an engagement starts.
GUARANTEES = [
    ("You own it", "Your data, code, and credentials stay in accounts that you control."),
    ("You can leave", "We use open formats and write documentation. Another team can take over and not build the system again."),
    ("You can see what agents did", "The system records each agent action. The record shows what the agent read, what it proposed, and who approved it."),
    ("You choose the AI", "The system does not depend on one model provider. You decide which models can read which data."),
]
# Shown under the hero and closing buttons. Only founder-confirmed policies
# belong here (PRODUCT.md, Offer); never add a price, duration or result.
ASSURANCE = "The first call is free. You talk to the founder, who designs and builds each project."

STEPS = [
    ("A call about one task", "Tell us about one task that takes a lot of your time. Tell us which tools it uses. We tell you if we should build it."),
    ("Build it in your accounts", "We set up the data and connectors in accounts that you control. We start with the tools for that task."),
    ("Run it with a person in charge", "The agent writes drafts, does checks, and flags problems. A person on your team approves each important action."),
    ("You get the system", "We give you the code, the documentation, and the access. You can keep us for support, but you do not have to."),
]

PAGES = [
    {
        "slug": "invoices",
        "title": "Invoices checked before you approve",
        "nav": "Invoice checks",
        "description": "We build an agent that reads each invoice and matches it to the vendor and purchase order. It flags problems and sends the invoice to you to approve.",
        "ghost": ["The agent checks invoices.", "It flags duplicates.", "You approve each payment."],
        "h1": "The agent checks each invoice before you approve it.",
        "sub": "Invoices come as PDFs and email attachments, and a person types them into the accounting system. We build an agent that reads each invoice and matches it to the vendor and order. It flags problems. Then it sends the invoice to you to approve.",
        "today_heading": "What accounts payable looks like today",
        "today": [
            ("Data entry by hand", "Staff type line items by hand from PDF attachments."),
            ("Checks by eye", "Staff compare each invoice to the purchase order and the receipt by eye."),
            ("Duplicates and price changes", "Vendors bill twice or change prices, and nobody sees it."),
            ("Approval by email", "People approve invoices in email threads. Later, nobody can find the approval."),
        ],
        "build": [
            ("Read each invoice", "The agent gets the vendor, amounts, dates, and line items from PDFs and email. It puts them in structured records."),
            ("Match and check", "The agent matches each invoice to its vendor and purchase order. It checks for duplicates and price changes."),
            ("Send to you to approve", "You approve correct invoices with one click. The agent flags each problem and gives the reason. Only a person can approve a payment."),
        ],
    },
    {
        "slug": "morning-brief",
        "title": "A morning brief of what needs you",
        "nav": "A morning brief",
        "description": "Each morning, the agent reads your sales, jobs, cash, and customer messages. It writes a brief that shows what changed, the evidence, why it is important, how sure it is, and a possible next step.",
        "ghost": ["The brief shows changes.", "It shows what is important.", "You decide what to do."],
        "h1": "One page shows what needs your attention today.",
        "sub": "The information that you need each morning is in five dashboards. We build an agent that reads the dashboards for you. Each morning, it writes a short brief. The brief shows what changed, the evidence, why it is important, how sure the agent is, and a possible next step.",
        "today_heading": "How you find problems today",
        "today": [
            ("Five dashboards", "Sales, jobs, cash, customer messages, and ads are each in a different app."),
            ("Found too late", "You see a late project or more complaints only days after the problem starts."),
            ("Numbers that disagree", "Each tool counts jobs and revenue a little differently."),
            ("No time to look", "In busy weeks, nobody checks."),
        ],
        "build": [
            ("One copy of the numbers", "Your tools send data to one warehouse in your account. All reports use the same numbers."),
            ("A written brief", "Each morning, the brief shows what changed, the evidence, why it is important, how sure the agent is, and a possible next step."),
            ("Suggestions only", "The brief recommends a next step. The agent does not act. You decide."),
        ],
    },
    {
        "slug": "own-your-data",
        "title": "All your business data, in one place",
        "nav": "Own your data",
        "description": "We connect your SaaS tools to one data warehouse in a cloud account that you control. Then nobody makes reports by hand in spreadsheets.",
        "ghost": ["One copy of your data.", "It is in your account.", "You keep it."],
        "h1": "All your business data, in one place that you control.",
        "sub": "Your jobs, invoices, and customers are in three different apps. We connect your tools to one warehouse in a cloud account that you control. Then the numbers agree, and nobody makes the weekly spreadsheet by hand.",
        "today_heading": "What scattered data costs you",
        "today": [
            ("The weekly spreadsheet", "Each week, a person exports, pastes, and corrects the same report."),
            ("Three versions of a customer", "Three systems spell the same customer's name in three ways."),
            ("Data that you rent", "Your business history is in vendors' clouds, and the vendors set the terms."),
            ("No good data for AI", "An agent can only be as good as the data that it reads."),
        ],
        "build": [
            ("A warehouse in your account", "Your data is in an open-source database, such as Postgres, in a cloud account that you control."),
            ("Connectors to your tools", "The connectors get data from your accounting, CRM, payment, schedule, and project tools. Then they clean and match the records."),
            ("Reports that update automatically", "Your weekly reports update automatically. They show the same numbers for all tools."),
        ],
    },
    {
        "slug": "where-to-start",
        "title": "Find the one task for AI",
        "nav": "Where AI fits",
        "description": "We help you find where an AI agent can do useful work in your business. We start with one call about your work. Then we tell you if we should build an agent for a task.",
        "ghost": ["Find where AI fits.", "Start with one task.", "Get a clear answer."],
        "h1": "Find the one task that an AI agent can do for you.",
        "sub": "Find which repetitive task you should give to an agent, and which task you should not. Start with a call about your week. We give you a clear answer.",
        "today_heading": "Why AI does not help you yet",
        "today": [
            ("A chatbot nobody uses", "General AI tools do not have information about your business or your data."),
            ("Too many options", "Each vendor sells AI. No vendor tells you where to start."),
            ("Fear of lock-in", "You do not want to give your process to a tool that you cannot leave."),
            ("No one to build it", "Your team runs the business. Nobody has time to add AI to your work."),
        ],
        "build": [
            ("A map of your work", "We show where the hours go, which tools you use, and which tasks repeat."),
            ("A short list, ranked", "We rank the tasks where an agent can help. We also list the tasks where it cannot help, and say why."),
            ("One agent that we build", "If one task is worth it, we build the agent in your accounts. A person approves each important action."),
        ],
    },
    {
        "slug": "professional-services",
        "title": "AI for professional services firms",
        "nav": "Professional services",
        "description": "We build agents for professional services firms. They help with client intake, write first drafts from your templates, and check time and billing before you send invoices.",
        "ghost": ["Help with intake and drafts.", "The agent uses your templates.", "You review all work."],
        "h1": "Spend less time on administration and more time on billable work.",
        "sub": "Intake forms, first drafts, and billing corrections use hours that you could bill. We build agents that collect client documents and write drafts from your templates. They also compare time to invoices before you send them.",
        "today_heading": "Where the unbilled hours go",
        "today": [
            ("Documents by email", "You ask clients for documents by email. You find missing documents too late."),
            ("Drafts from a blank page", "You write each letter, proposal, and report from the start."),
            ("Billing corrections", "Before you send invoices, staff check each time entry by hand."),
            ("Reports by spreadsheet", "Staff copy pipeline and utilization data from the CRM and the accounting system by hand."),
        ],
        "build": [
            ("Intake help", "The agent collects client documents and finds missing items. It flags possible conflicts of interest for a person to review."),
            ("First drafts from your templates", "The agent writes letters, proposals, and reports in your format. A professional edits and signs each one."),
            ("Billing checks before invoices", "The agent compares time and expenses to each engagement. It flags problems before you send invoices."),
        ],
    },
    {
        "slug": "field-services",
        "title": "AI for contractors and local services",
        "nav": "Contractors and local services",
        "description": "We build agents for local service businesses. The agents write draft quotes from job notes, suggest schedules, and connect job costs to invoices.",
        "ghost": ["Visit the site.", "Send the quote that day.", "Know each job's cost."],
        "h1": "Send your quote on the same day that you visit the site.",
        "sub": "You write quotes in the evening. Your schedule is on a whiteboard. You do not know the cost of a job until tax time. We build agents that write draft quotes from your notes and past prices. They connect hours and materials to each invoice.",
        "today_heading": "Where your evening hours go",
        "today": [
            ("Quotes at night", "You write quotes at home in the evening from your site notes."),
            ("Schedules by phone", "You plan crews, travel, and return visits by phone and from memory."),
            ("Reviews with no reply", "You have no time to reply to reviews, good or bad."),
            ("Unknown job margins", "Nobody connects hours and materials to the invoice, so you do not know your profit."),
        ],
        "build": [
            ("Quote drafts from job notes", "The agent uses your photos, notes, and past prices to write a draft quote. You change it and send it."),
            ("Schedule suggestions", "The agent proposes schedules from crews, travel time, and job length. You approve each schedule."),
            ("Job costs", "The agent matches hours and materials to each invoice. You see which jobs make money."),
        ],
    },
    {
        "slug": "compliance",
        "title": "Compliance checks that we record and you review",
        "nav": "Compliance checks",
        "description": "We build agents that check documents against your rules and track privacy requests. Each agent records what it checked, who approved it, and when.",
        "ghost": ["Checks against your rules.", "A person reviews each result.", "The record is on file."],
        "h1": "We record each check and keep each approval on file.",
        "sub": "Compliance work is slow and repetitive. Later, you must prove that you did it. We build agents that check documents against your rules and flag problems for a person to review. The agent records what it checked, who reviewed it, and when.",
        "today_heading": "What compliance work looks like today",
        "today": [
            ("Checklists by hand", "Staff check documents line by line against rules in a binder."),
            ("Requests in an inbox", "Staff track privacy and data requests in email. They can miss deadlines."),
            ("Evidence from memory", "When an auditor asks, staff rebuild the evidence from memory."),
            ("Policies nobody can find", "Staff cannot find policies, so they ask the same procedure questions again and again."),
        ],
        "build": [
            ("Checks against your rules", "The agent checks documents and labels against your requirements. It flags problems for a reviewer. It does not approve anything."),
            ("Requests tracked until closed", "The agent logs each privacy and data request, sends it to the correct person, and follows it until someone closes it."),
            ("An audit trail by default", "The agent records each check. The record shows what the agent read, what it found, and who approved it."),
        ],
    },
    {
        "slug": "no-lock-in",
        "title": "Use AI and keep control of your business",
        "nav": "AI without lock-in",
        "description": "We build AI agents on your data, in your accounts. We document them, so you can change models or vendors and not start again.",
        "ghost": ["You keep logic and data.", "You can use any model.", "You can leave."],
        "h1": "Use AI and keep control of your business.",
        "sub": "Most AI tools keep your data in their cloud and your process in their prompts. When prices change or the tool closes, you must start again. We build agents on your data, in your accounts. You can change the model or the vendor and keep your data and your rules.",
        "today_heading": "What AI tools take from you",
        "today": [
            ("Your data", "The tool copies your data into the vendor's cloud. The vendor sets the terms."),
            ("Your process", "The tool puts your business rules in its own prompts and workflows."),
            ("Your choice of model", "The tool picks the model, and you cannot change it."),
            ("Your exit", "If you leave, you must build everything again."),
        ],
        "build": [
            ("Your rules, written down", "We write down how your business makes decisions. You own this logic. It is not hidden in prompts."),
            ("Any model", "The agents use hosted or open models. You can change the provider and keep the same business logic."),
            ("Everything in your accounts", "Your data, code, and credentials stay in accounts that you control. We give you the documentation."),
        ],
    },
    {
        "slug": "knowledge-search",
        "title": "Answers from your own documents",
        "nav": "Answers from your documents",
        "description": "We build an agent that answers staff questions from your procedures, contracts, and past work. It shows the source of each answer.",
        "ghost": ["Ask a question.", "The agent reads your files.", "It shows the source."],
        "h1": "The agent answers from your documents. It does not use the internet.",
        "sub": "Your procedures, contracts, price sheets, and past work have most of the answers that your team needs. But these documents are in many drives and inboxes. We build an agent that answers from your files and shows the source, so people can check it.",
        "today_heading": "How your team finds answers today",
        "today": [
            ("Ask the one who knows", "Staff ask the same person the same questions all day."),
            ("Search five places", "Staff search drives, inboxes, wikis, and old tickets, one at a time."),
            ("Old copies", "There are three versions of the procedure. Nobody knows which one is current."),
            ("Lost knowledge", "When a person leaves, their knowledge goes with them."),
        ],
        "build": [
            ("Your documents, indexed", "The agent indexes your procedures, contracts, price sheets, and past work. The documents stay where they are, in your account."),
            ("Answers with sources", "Each answer links to the document and passage that it came from, so anyone can check it."),
            ("Access that you control", "Each person gets answers only from documents that they can see. We set up providers so that they do not train models on your documents."),
        ],
    },
    {
        "slug": "lead-follow-up",
        "title": "Reply to each inquiry on the day it arrives",
        "nav": "Lead follow-up",
        "description": "We build an agent that reads and sorts each new inquiry. It writes a draft reply and records the inquiry in your CRM. A person sends the reply.",
        "ghost": ["Read each inquiry.", "Reply the same day.", "Record it in the CRM."],
        "h1": "Reply to each inquiry on the day it arrives.",
        "sub": "Inquiries come by web form, email, and phone message, and the good ones wait behind the rest. We build an agent that reads and sorts each inquiry. It writes a draft reply with the next step and records the inquiry in your CRM. A person sends the reply.",
        "today_heading": "Where you lose new business today",
        "today": [
            ("Replies a day late", "Inquiries wait until someone has a free hour."),
            ("Every lead looks the same", "Serious buyers wait behind people who only want information."),
            ("The CRM is out of date", "Notes stay in personal inboxes, and the team cannot see them."),
            ("No follow-up", "When a lead does not reply, nobody contacts the lead again."),
        ],
        "build": [
            ("Each inquiry read and sorted", "The agent puts web forms, email, and messages in one queue. It sorts them by fit and urgency with your rules."),
            ("A draft reply", "The agent writes a reply in your voice. The reply gives one next step: a link to book a call, a question, or a polite no. A person sends it."),
            ("Recorded and followed up", "The agent records each inquiry in your CRM. It reminds you to contact leads that do not reply."),
        ],
    },
]

def e(text: str) -> str:
    return html.escape(text, quote=True)


def mailto(page: dict) -> str:
    subject = quote(f"Book a call: {page['nav']}")
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


def menu(current: dict) -> str:
    """Footer menu of every landing page; the current one is marked, not linked away from."""
    items = []
    for q in PAGES:
        cur = ' aria-current="page"' if q is current else ""
        items.append(f'        <li><a href="../{q["slug"]}/"{cur}>{e(q["nav"])}</a></li>')
    return "\n".join(items)


def render(p: dict) -> str:
    ghost = "\n".join(f'  <span class="ghost-line">{e(g)}</span>' for g in ["Sovereign Source AI", *p["ghost"]])
    guarantees = "\n".join(
        f"      <div>\n        <dt>{e(t)}</dt>\n        <dd>{e(d)}</dd>\n      </div>" for t, d in GUARANTEES
    )
    book = f'<a class="btn" href="{e(mailto(p))}" data-book>Book a call</a>'
    address = f'<a class="btn-quiet" href="{e(mailto(p))}">or write to {EMAIL}</a>'
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
<link rel="stylesheet" href="../../style.css?v=20261005">
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
      <a class="btn-quiet" href="#how-it-starts">How it starts</a>
    </div>
    <p class="lp-assure">{e(ASSURANCE)}</p>
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
    <p class="section-intro">We build in accounts that you control. The agent prepares the work. A person approves each decision.</p>
    <ol class="layers offer">
{rows(p['build'])}
    </ol>
    <p class="lp-inline-cta"><a class="btn-quiet" href="{e(mailto(p))}" data-book data-book-label="Talk to us about your task">Tell us about your task</a></p>
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

<section class="formulations" aria-labelledby="guarantees-heading">
  <div class="formulations-inner">
    <h2 class="section-heading" id="guarantees-heading">You stay in control</h2>
    <dl class="guarantees">
{guarantees}
    </dl>
  </div>
</section>

<section class="section claim-section" id="talk">
  <div class="section-inner">
    <h2 class="section-heading">Start with one task</h2>
    <p class="claim-text">
      Sovereign Source AI is a new practice. We work with a small number of businesses
      at one time. Tell us about the one task that you most want to give to an agent.
      We will tell you if we should build it.
    </p>
    <div class="cta-row">
      {book}
      {address}
    </div>
    <p class="lp-assure">{e(ASSURANCE)}</p>
  </div>
</section>

</main>

<footer class="footer">
  <div class="footer-inner">
    <div class="footer-side">
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
    <nav class="lp-menu" aria-labelledby="lp-menu-heading">
      <h2 class="lp-menu-heading" id="lp-menu-heading">Other tasks that we build for</h2>
      <ul class="lp-menu-list">
{menu(p)}
      </ul>
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
