---
name: csync-design
description: Use when designing or reviewing a C-Sync screen (Streamlit UI, deck captures, dashboards for safety-critical, offline, dark interfaces): applies 8 checked principles, audits against them, and produces a blind 5-second test.
---

# csync-design

Adapted from `unslop` by Damir Sokolovsky (@heydamir), CC BY 4.0, https://heydamir.design/unslop (credit required in any copy or adaptation), and from the token practice of the team's portfolio. No code copied: principles restated. Never judge the visual effect yourself; prepare a test for people.

## Run it
1. Render the screen (Playwright, fixed 1280 px width, days 7, 9, 10) and look at the real pixels, not only the code.
2. Write the direction in five lines before editing: product, character (concrete words; never clean, modern, premium), world, moments (where richness is allowed), signature (one detail only this product has). Show it and stop if the user is present.
3. Audit against the eight principles. List each failing item with where it lives. If nothing fails, say so and stop.
4. Fix one principle at a time across the whole screen, in order P4, P3, P5, P2, P8, P7, P6.
5. Prove it, with tools: axe-core WCAG A+AA on each screen with normal and reduced motion (0 violations), Lighthouse accessibility, measured contrast ratios, the project's tests green. Report numbers, including those that do not discriminate.
6. Prepare the blind test: images renamed X/Y, key kept apart, 8 written criteria, 3 to 5 people who have never seen the project. A gap under 2 votes of 5 decides nothing.

## The eight principles
- **P1 Direction first.** Five lines, derived from the product, before any edit.
- **P2 One rich zone.** The state cards and the decision carry the colour and the craft. Chrome, backgrounds, buttons and labels stay quiet. Decoration (halos, orbs, floating shapes, glowing grids) is filler unless it is the one signature.
- **P3 One tinted neutral ramp, three text roles, one accent.** Accent text at 4.5:1 or more. State colours (green, amber, coral, grey) mean states only and are never reused as decoration.
- **P4 4 px grid.** Equal things share one size. Space inside a group is smaller than space between groups.
- **P5 Type.** Sentence case, two weights, tabular figures, no negative tracking on small text, no uppercase tracked labels.
- **P6 One source of values.** Every colour, size and duration comes from `csync/config/theme.json` or a named CSS variable. No colour in `app.py` (test enforced).
- **P7 Motion explains.** Transition named properties only, one easing curve, no loops that carry no meaning, a `prefers-reduced-motion` fallback for every animation, an entrance at most once.
- **P8 Never colour alone; unknown never looks normal.** Icon plus word on every state; a context-only card is dashed and dimmed; missing data is never drawn as normal.

## Do not
- Do not add effects to look finished, and do not swap one trend for another (glass, grain, neon, bento).
- Do not invent data, claims or features; synthetic data stays labelled on screen.
- Do not claim a design "works" from a screenshot: cite the tool result or the test with people.
- Do not change a screen the audit finds clean.

## Known conflict in this repo
`docs/DESIGN_DIRECTION.md` (Monolith Glass) uses halos, a wireframe polyhedron, glass, uppercase kickers and 7 background animations, which P2, P5 and P7 reject. Two CSS profiles exist (`CSYNC_STYLE=glass` default, `quiet`); the choice is the team lead's, after the people test (`docs/DESIGN_TEST_5S.md`).
