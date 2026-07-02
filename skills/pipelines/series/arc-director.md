# Arc Director — Series Pipeline

## When To Use

Plan the episode-by-episode arc and lock the **style bible**. Output is a series-level `scene_plan` artifact: one entry per episode with objective, beats outline, and continuity hooks, plus the visual system every episode reuses.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation (series arc) |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Format, count, personas |
| Playbook | Active style playbook | Base visual language |

## Operating Principles

- **Escalating value.** Episode N must be worth having watched episodes 1..N-1; sequence from foundational → advanced (learning) or setup → payoff (drama).
- **No redundant episodes.** If two episodes share an objective, merge them.
- **The style bible is written once.** Palette, typography, host treatment, lower-thirds, chapter-marker style, end-card design — defined here, reused verbatim by assets/compose.

## Process

### 1. Sequence the episodes
One entry per declared episode: title working line, single objective, 3–6 beat outline, and its continuity hooks (what it recaps from the previous episode, what it teases about the next).

### 2. Apply format pacing
- `learning`: insert recap/assessment episodes at the declared pedagogy ratio; every episode ends on a learning checkpoint; plan quiz-card overlays (HyperFrames finishing pass) where knowledge checks land.
- `drama`: place cliffhangers at episode ends; track character state per episode so callbacks are real.
- `podcast`: chapterize each episode (3–5 chapters); plan chapter-marker overlays.
- `recap`: fix the segment order template all episodes follow.

### 3. Write the style bible
Concrete values, not vibes: hex palette, type stack + sizes, host framing rules, lower-third layout, transition vocabulary, chapter-marker/end-card specs. Note which overlays are a HyperFrames finishing pass at compose.

### 4. Plan re-engagement beats
For each episode, mark where the ~25% and ~65% re-engagement beats land (pattern interrupt: visual change, new segment, question to viewer).

### Quality Gate
- [ ] One entry per declared episode; each objective distinct.
- [ ] Continuity hooks reference real adjacent-episode content.
- [ ] Style bible complete with concrete values.
- [ ] Pedagogy/cliffhanger pacing applied per format.
- [ ] Re-engagement beats marked per episode.

## Common Pitfalls

- Outlining episode 1 in detail and leaving later episodes as titles — every entry needs beats.
- A style bible that's adjectives ("clean, modern") instead of values.
- Recap episodes that summarize instead of re-testing (learning format).

## References

- Re-engagement beats at 25%/65%; pattern interrupts: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
- Retention-curve shapes (cliff/gradual/bump) for arc pacing: https://prepublish.ai/guides/youtube-retention-guide
