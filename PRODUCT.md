# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

No primary audience is chosen yet (open decision). The site currently speaks to a mix of:

- institutional buyers: technology, security, and architecture leaders at banks, public-sector bodies, and other regulated organizations weighing AI control and vendor exit;
- builders: engineers and open-source developers who may adopt or contribute to the architecture and a future open core;
- investors, advisors, and prospective design partners assessing the thesis.

When a primary audience is chosen, record it here; until then, work should not optimize for one group at the others' expense.

## Product Purpose

sovsrc.ai publishes the Sovereign Source AI (SSA) thesis: the manifesto and a set of architecture topic pages. Its job is to make the argument clearly enough that the right readers want to talk.

Success: a reader who is convinced starts a conversation with the founder (design partner, pilot, advisory, or collaboration). The site has no contact route yet; adding one is an open decision (channel not chosen).

## Positioning

Sovereignty is a system property, not a hosting choice. Self-hosting a model or downloading open weights is not sovereignty; a system is sovereign when its complete operational stack can be owned, inspected, governed, deployed, modified, moved, and operated independently of any single external provider.

SSA is an LLM-neutral, cloud-neutral, vendor-replaceable architecture built on seven layers (Intent, Governance, Decision, Capability, Execution, Verification, Evidence). The goal is credible exit and retained control, not rejection of commercial services. Commercial and open products (Palantir, Payload, Supabase, PostHog, MCP servers, open and frontier models) may participate, but none owns the institutional model.

## Operating Context

- Readers arrive to evaluate an idea, often before any product exists; the manifesto and topic pages are the whole product experience today.
- Topic pages are generated from numbered markdown pages in the separate svrnsrc.ai research repo (`research/docs/sovereign-source-ai/`) by `_tools/build_topics.py`, which also rewrites the homepage table of contents.

## Capabilities and Constraints

- Static HTML/CSS served by GitHub Pages (Jekyll, legacy build) at sovsrc.ai (`CNAME`). No framework or build step beyond the topic generator.
- Pages: `index.html` (homepage), `manifesto.html`, `topics/*.html` (10 generated topic pages), `logo-concepts.html` (internal logo review page).
- Folders starting with `_` and files listed in `_config.yml` `exclude` are not published.
- Terminology: "Sovereign Source AI" (SSA), "SovSrc" / sovsrc.ai, Sovereign Skills, SSIL (Sovereign Source Intent Language), work orders, seven layers, four planes (Intention, Governance, Verification, Evidence).
- Open decisions: primary audience; contact channel; open-source license; trademark clearance.

## Brand Commitments

- Names: "Sovereign Source AI" (descriptive), "SovSrc" / sovsrc.ai (concise). The research lists sovereignsource.ai as a possible manifesto or specification destination; it is not in use.
- Existing assets: `logo.svg` and `favicon.svg` (the US flag).
- Voice: declarative and plain, as in the manifesto. The canonical formulations are "Intent → Decide → Constrain → Execute → Verify → Prove"; "Models reason. Policies authorize. Capabilities constrain. Execution acts. Audit proves."; and "No artifact without intent. No agent without policy. No execution without isolation. No dependency without provenance. No release without evidence."
- Trademarks are not cleared. Do not add ™ or ® marks or imply registered status.

## Evidence on Hand

- The manifesto (`manifesto.html`; source `research/docs/sovereign-source-ai-manifesto.md` in the svrnsrc.ai repo).
- Ten architecture topic pages (`topics/`), drafted from the research and quoting it with named sources.
- Research documents in the svrnsrc.ai repo: master summary, four-plane architecture notes, sovereignty-test design.

Absences that future work must not fabricate: released software, customers, pilots, design partners, users, testimonials, benchmarks, metrics, pricing, license terms, funding, team members beyond the founder, and partnerships with any named vendor.

## Product Principles

1. Claim only what exists. Today that is a thesis and an architecture; describe plans as plans.
2. The argument is the product. Clarity and readability of the manifesto and architecture come before decoration.
3. Stay vendor-neutral. Named products appear only as replaceable examples, never as endorsements or dependencies.
4. Lead toward a conversation. A convinced reader should always have an obvious next step once a contact route exists.
