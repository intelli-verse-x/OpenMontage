# Scene Director — Long-Form Pipeline

## When To Use

Turn the script into per-chapter shot plans: evidential b-roll, chapter visual identities, and the shot grammar shifts that make pattern interrupts land. Carries the **anti-slideshow hard gate per chapter**.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `script`, chapter arc (visual identities) | Beats + look per chapter |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow scoring per chapter |
| Tool | `frame_sampler` (optional) | Reference checks |

## Operating Principles

- **B-roll is evidence.** Every visual proves or advances the narration's current claim (`information_role`). Generic wallpaper b-roll over narration is the long-form slideshow failure mode.
- **Chapter boundaries are visible.** Apply each chapter's visual identity from the arc (palette shift, location change, graphic language) so a viewer scrubbing the timeline can *see* the chapters.
- **Interrupts change the grammar.** At the 25%/65% beats, the shot language itself shifts (e.g. narrative footage → full-screen data graphics; archival stills → present-day motion).

## Process

### 1. Shots per chapter
For each script beat: `information_role` (which claim this proves), `shot_intent`, source intent (stock / generated / archival / graphic), framing, est duration. 16:9 composition; scenes at 1920×1080 intent.

### 2. Visual variety budget
No more than ~3 consecutive shots of the same type (e.g. stock aerial after stock aerial); alternate scale and source type. Narration-heavy stretches get cutaway inserts at least every 10–15s.

### 3. Interrupt scenes
Design the 25%/65% moments as their own mini shot plans with a distinct grammar; these should also be the most clip-able moments (publish extracts shorts from retention bumps).

### 4. Chapter cards
Plan the chapter-title treatment (consistent template, per-chapter variation) — typically a HyperFrames overlay pass at compose.

### 5. Score per chapter
`score_slideshow_risk` per chapter; any `fail` → rework that chapter before submitting.

### Quality Gate
- [ ] Every shot has `information_role` + `shot_intent`; b-roll evidential.
- [ ] Chapter visual identities applied; boundaries visible.
- [ ] Interrupt scenes have distinct grammar.
- [ ] No >15s narration stretch without a visual change.
- [ ] Slideshow verdict ≥ acceptable per chapter.

## Common Pitfalls

- Wallpaper b-roll ("city timelapse" over everything) — the gate exists for this.
- Chapter 5 quietly reusing chapter 1's grammar (flattens the escalation).
- Interrupts staged as narration-over-different-footage instead of a real format change.

## References

- Pattern interrupts / retention-curve countermeasures: https://prepublish.ai/guides/youtube-retention-guide
