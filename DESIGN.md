---
name: Sovereign Source AI
description: A black, type-only manifesto site where hairline rules carry all structure.
colors:
  ground-black: "#000000"
  band-black: "#0a0a0a"
  type-white: "#ffffff"
  body-gray: "#a3a3a3"
  label-gray: "#909090"
  hairline: "#1a1a1a"
  stroke-dark: "#333333"
  flag-red: "#BF0D3E"
typography:
  display:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.4rem, 5.5vw, 4.8rem)"
    fontWeight: 400
    lineHeight: 1.08
    letterSpacing: "-0.025em"
  headline:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.6rem, 3vw, 2.6rem)"
    fontWeight: 450
    letterSpacing: "-0.02em"
  statement:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.2rem, 2.5vw, 1.8rem)"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "-0.02em"
  title:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.2rem"
    fontWeight: 500
    lineHeight: 1.3
    letterSpacing: "-0.02em"
  body:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.6
  prose:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1rem, 1.6vw, 1.1rem)"
    fontWeight: 400
    lineHeight: 1.75
  intro:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.1rem, 1.8vw, 1.3rem)"
    fontWeight: 400
    lineHeight: 1.6
  lead:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "1.15rem"
    fontWeight: 400
    lineHeight: 1.6
  prose-h1:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(2.2rem, 4vw, 3.6rem)"
    fontWeight: 400
    lineHeight: 1.1
    letterSpacing: "-0.025em"
  prose-h2:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.3rem, 2.2vw, 1.7rem)"
    fontWeight: 500
    letterSpacing: "-0.02em"
  ui:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.95rem"
    fontWeight: 400
    lineHeight: 1.6
  small:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.85rem"
    fontWeight: 450
    lineHeight: 1.6
  label:
    fontFamily: "Instrument Sans, Helvetica Neue, Arial, sans-serif"
    fontSize: "0.75rem"
    fontWeight: 500
    lineHeight: 1.6
    letterSpacing: "0.05em"
    fontFeature: "tnum"
rounded:
  hairline: "2px"
spacing:
  row: "1.25rem"
  block: "2rem"
  section-pad: "24px 40px"
  gutter: "clamp(1.5rem, 5vw, 4rem)"
  column-gap: "clamp(1.5rem, 3vw, 2.5rem)"
  measure: "1200px"
components:
  button-primary:
    backgroundColor: "{colors.type-white}"
    textColor: "{colors.ground-black}"
    typography: "{typography.body}"
    rounded: "{rounded.hairline}"
    padding: "0.85rem 1.4rem"
  button-quiet:
    backgroundColor: "transparent"
    textColor: "{colors.type-white}"
    typography: "{typography.body}"
    padding: "0 0 0.1em"
  nav-link:
    textColor: "{colors.body-gray}"
    padding: "0"
  nav-link-hover:
    textColor: "{colors.type-white}"
  rule-row:
    backgroundColor: "transparent"
    textColor: "{colors.body-gray}"
    padding: "1.25rem 0 2rem"
  guarantee-row:
    backgroundColor: "{colors.band-black}"
    textColor: "{colors.body-gray}"
    padding: "1.25rem 0"
  time-entry:
    backgroundColor: "{colors.ground-black}"
    textColor: "{colors.body-gray}"
    padding: "0.75rem 1rem"
---

# Design System: Sovereign Source AI

## Overview

**Creative North Star: "The Plain Declaration"**

The site is a statement printed in white on black. There are no images, no illustrations, no cards and no color fields: the argument is set in one sans family, and every structural decision is made with a 1px hairline, a change between white and gray, or a step in type size. The only atmosphere is the ghost layer, oversized lines of the manifesto set behind the page at near-invisible contrast, rotated a few degrees, fixed while the content scrolls over them.

Density is architectural rather than busy: generous vertical padding, long measures held to 46 to 70 characters, and index grids where each item is a stack of number, title and description under a top rule. The voice is declarative and plain, and the visual system matches it. Emphasis comes from moving text from gray to white, never from adding a color, a box or a badge.

Color is withheld until it means something. The flag red from the US flag mark appears exactly once in the shipped CSS, as the rule that marks the moment time is handed back in the homepage's "A Monday, twice" comparison.

**Key Characteristics:**
- Pure black ground (#000000) with one slightly lifted band (#0a0a0a) for statement sections.
- One typeface, Instrument Sans variable (400 to 700), with weights 400, 450 and 500 doing all the work.
- Hairline rules (#1a1a1a) as the only structural device; containers are rows, never boxes.
- White for what matters, gray for what supports it.
- Fixed ghost text behind all content as the signature atmosphere.
- Flag red as a single, sparing time marker; the flag logo carries the full flag palette.

## Colors

A near-monochrome palette: black ground, white and two grays for type, two dark grays for lines, and one red held in reserve.

### Primary
- **Type White** (#ffffff): headings, titles, the primary button fill, active emphasis inside gray copy (strong, em, links), and focus outlines. Also the selection highlight, inverted onto black.

### Tertiary
- **Flag Red** (#BF0D3E): taken from the logo's flag. Used only as the 1px top rule of the freed-time block in the homepage time axis. It marks a moment; it never fills, never colors text, never decorates.

### Neutral
- **Ground Black** (#000000): the page ground, the sticky header (at 85% opacity with a 12px blur), the footer, and the masking background on time-axis elements that must interrupt the hour hairlines.
- **Band Black** (#0a0a0a): the one tonal step, used for full-width statement bands (the formulations and the guarantees) bounded by hairlines top and bottom.
- **Body Gray** (#a3a3a3): running copy, descriptions, intros, nav links at rest.
- **Label Gray** (#909090): numbers, times, captions, footer links, footer tagline, and underline colors for quiet links.
- **Hairline** (#1a1a1a): every structural rule: section tops, row separators, header and footer borders, hour lines on the time axis. Also the ghost text color (at 0.18 opacity).
- **Stroke Dark** (#333333): the scrollbar thumb and the left edge of the "Today" time-axis entries; a step brighter than the hairline where a line must read against a hairline grid.

### Named Rules
**The Gray-to-White Rule.** Emphasis is a move from Body Gray to Type White. No highlight color, no background tint, no badge.

**The One Red Rule.** Flag Red appears as a single hairline marking handed-back time. If a second red element seems needed, the composition is wrong.

## Typography

**Display Font:** Instrument Sans (with Helvetica Neue, Arial, sans-serif)
**Body Font:** Instrument Sans (same family)
**Label/Mono Font:** Instrument Sans with tabular numerals; ui-monospace only for inline code in topic prose.

**Character:** A single contemporary grotesque used at its lighter weights. Large sizes run at 400 with tight negative tracking, so headlines read as calm statements rather than shouts. Instrument Sans is the established brand face and is flagged by generic detectors as an overused font; that flag is recorded as an intentional exception.

### Hierarchy
- **Display** (400, clamp(2.4rem, 5.5vw, 4.8rem), 1.08, -0.025em): the page's one headline, held to 14 to 16ch and balanced. Topic and manifesto h1 run the same character a step smaller (clamp(2.2rem, 4vw, 3.6rem), 1.1).
- **Headline** (450, clamp(1.6rem, 3vw, 2.6rem), -0.02em): section headings. In long-form prose, h2 drops to 500 at clamp(1.3rem, 2.2vw, 1.7rem) and sits under a hairline.
- **Statement** (400, clamp(1.2rem, 2.5vw, 1.9rem), 1.4 to 1.5, -0.02em): formulations, the claim, and the time axis's closing line. Statements are sentences, set large, never italic.
- **Title** (500, 1.2rem, 1.3, -0.02em): row and grid titles, column heads, guarantee terms.
- **Body** (400, 0.95 to 1.1rem, 1.6 to 1.7): descriptions and intros in Body Gray, measure 56 to 60ch. Long-form prose runs at 1.75 line height in a 720px column.
- **Label** (500, 0.75rem, 0.05 to 0.1em tracking, tabular numerals): two-digit index numbers, clock times, pager labels. Uppercase only for the pager's "Previous/Next" and inline lead-ins.

### Type Tokens
`style.css` carries the ramp as custom properties on `:root`: `--fs-label`, `--fs-small`, `--fs-ui`, `--fs-body`, `--fs-lead`, `--fs-title`, `--fs-prose`, `--fs-intro`, `--fs-statement`, `--fs-prose-h2`, `--fs-headline`, `--fs-prose-h1`, `--fs-display`. Every font size outside the ghost layer uses one of them; the ghost lines keep their own oversized clamps because they are atmosphere, not text. Inline code in topic prose uses `ui-monospace, SFMono-Regular, Menlo, monospace`.

### Named Rules
**The Light Weight Rule.** Nothing on the site is set heavier than 500. Hierarchy comes from size and white-versus-gray, not weight.

**The Tabular Time Rule.** Every number that counts or tells time (index numbers, clock times) uses tabular numerals in Label Gray.

## Layout

A single centered measure (1200px) with horizontal padding of 40px inside sections and a fluid gutter (clamp(1.5rem, 5vw, 4rem)) in header and footer. Sections stack vertically, each opened by a 1px hairline top border; statement sections and closing sections drop that border.

Index content uses one shared grid: N equal columns (4 by default, 5 for topics, 3 for the offer) with a column gap of clamp(1.5rem, 3vw, 2.5rem), each cell a vertical stack under a top rule. Grids step to 2 columns at 1100px and 1 column at 768px. Definition rows (the guarantees) use a two-column grid, a term column of 12 to 18rem beside a description held to 60ch, collapsing to one column at 768px.

The homepage time axis is a three-column grid (a 3.5rem axis column and two equal tracks) over 14 rows of 15-minute slots (3.5rem each), so entries sit at their real clock times and empty time is visible as empty space. Below 960px the axis column drops, the tracks stack, and slots compress to 1.6rem.

The header nav sheds links by priority (minor links below 1240px, mid links below 960px, all below 768px); the footer always lists every link.

**The Empty Space Is the Argument Rule.** When a layout represents time or quantity, space is allocated to scale, and the empty stretch is left empty rather than filled.

## Elevation & Depth

The system is flat. There are no box shadows anywhere. Depth comes from three things only: the fixed ghost-text layer behind everything (z-index 0, content at z-index 1), the sticky header's translucent black with a 12px backdrop blur, and the single tonal step from Ground Black to Band Black for statement bands.

**The No-Shadow Rule.** Surfaces never lift. If something needs separation, give it a hairline or a tonal band.

**The Masking Ground Rule.** Where a hairline grid runs behind content (the time axis's hour lines), the elements that must interrupt it carry a Ground Black background so the lines stop at them instead of crossing them.

## Shapes

Square. Corners are 2px at most, and only on the primary button and the focus outline; everything else has no radius. Lines are always 1px. Rows are open on the sides: a top rule (sometimes a bottom rule on the last row), no side borders, except the time axis, where a left edge marks each entry's column. The manifesto's pull quote uses a 2px left bar in Label Gray.

## Components

### Buttons
Restrained and paired: one solid action, one quiet alternative beside it.
- **Shape:** nearly square (2px radius).
- **Primary:** Type White fill, Ground Black text, 500 weight at 1rem, padding 0.85rem 1.4rem. Hover drops opacity to 0.85 over 0.2s.
- **Quiet:** Type White text with a 1px Label Gray underline (border-bottom, 0.1em below); hover brightens the underline to Type White.
- **Pairing:** the two sit in a wrapping row with a 1rem by 1.75rem gap. The solid button is always the email action; the quiet link points to depth (details page, manifesto).
- **Focus:** 1px Type White outline offset 4px.

### Navigation
- **Header:** sticky, translucent black with blur, hairline bottom. Logo (flag mark at 38 by 20 plus wordmark, 500 weight) left; links right in Body Gray at 0.9rem, 450 weight, hovering to Type White. The call-to-action link is Type White with a 1px white underline.
- **Footer:** wordmark, domain tagline in Label Gray, a wrapping row of every link in Label Gray at 0.85rem, and a hairline-topped note.

### Rule-Lined Rows
The universal container. Each item is a vertical stack (optional two-digit Label number, Title, Body Gray description) under a 1px hairline top, padded 1.25rem above and 2rem below, set in the shared N-column grid. Used for the seven layers, the topics index, the offer, verticals and steps. Numbered lists without a grid (the seven questions) use the same hairline separators with a leading-zero counter hung in the left 3rem.

### Guarantee Rows
A definition list inside a Band Black statement band. Each row is a two-column grid (Title-weight term, Body Gray description at 60ch), separated by hairlines, with a closing hairline under the last row.

### Statement Band
A full-width Band Black section, hairlines top and bottom, generous vertical padding (clamp(4rem, 8vw, 7rem)), holding Statement-size sentences stacked 2.5rem apart in Body Gray. Carries the canonical formulations and the guarantees.

### Time-Axis Comparison (signature)
Two columns share one clock (8:00 to 11:30, 15-minute slots, hour hairlines across both tracks, a hairline at the end time). Left column ("Today"): each task is a block at its real start time and duration, Ground Black background, Label Gray top rule, Stroke Dark left edge, Body Gray text with its time above. Right column: a compact burst of short timed lines in Type White under a Label Gray rule, then one block spanning the remaining time, opened by the Flag Red rule, holding a note and a Statement-size closing line, with the end time pinned to the bottom. Motion: on first view, the right column's lines settle in once, in time order (0.8s, cubic-bezier(0.16, 1, 0.3, 1), 0.12s stagger), from 20% opacity, so content is never invisible; no animation under reduced motion or without IntersectionObserver.

### Ghost Text
Fixed, centered, pointer-transparent lines from the manifesto in Hairline at 0.18 opacity, 400 to 500 weight, very large (up to 18rem), each rotated between -6 and 4 degrees. Below 768px the lines wrap, center, and lose their rotation.

### Long-Form Prose
A 720px column for the manifesto and topic pages: h2s under hairlines, Body Gray paragraphs at 1.75 line height, Type White strong and em, links underlined in Label Gray that brighten on hover, tables ruled by hairlines only, and a two-column pager under a hairline.

## Do's and Don'ts

### Do:
- **Do** build every container as a rule-lined row: a 1px #1a1a1a top rule, open sides, no fill.
- **Do** signal emphasis by moving text from Body Gray (#a3a3a3) to Type White (#ffffff).
- **Do** keep weights at 400, 450 or 500, and set large text at 400 with negative tracking (-0.02em to -0.025em).
- **Do** pair one solid white button with one quiet underlined link, and make the solid one the email action.
- **Do** set times and index numbers in 0.75rem tabular numerals in Label Gray (#909090).
- **Do** give elements that sit over a hairline grid a Ground Black background so lines stop at them.
- **Do** keep motion to one authored moment per page, starting from an already-visible state, and honor reduced motion.

### Don't:
- **Don't** use cards: no tinted or fully bordered boxes around content, no rounded panels, no shadows. Full-width Band Black statement bands are sections, not cards.
- **Don't** use Flag Red (#BF0D3E) for text, fills, buttons or decoration; it is a single hairline marker.
- **Don't** add a second typeface for display or body; Instrument Sans carries every role.
- **Don't** set anything heavier than 500 or use radii above 2px.
- **Don't** add images, icons or illustrations to carry meaning the type and rules already carry; the flag mark is the only picture.
- **Don't** fill empty time or space in a scaled layout to make it look busy.
