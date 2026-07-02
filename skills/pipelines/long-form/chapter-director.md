# Chapter Director — Long-Form Pipeline

## When To Use

Design the chapter arc — the video's retention architecture. Output is a `scene_plan` artifact at chapter granularity: one entry per chapter with objective, beat outline, cliff, and the placement of re-engagement beats.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation (chapter arc) |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Thesis, type, chapter count, research |

## Operating Principles

- **A chapter plan is a retention plan.** Chapters are ordered by escalating tension toward the thesis payoff, not by topic taxonomy.
- **The cold open is chapter zero.** Plan a 30–60s open that leads with the key insight or the most arresting moment from the research — never a channel intro. This is the single highest-leverage decision in the video.
- **Cliffs, not summaries.** Every chapter ends on a forward pull (an unanswered question, a reversal tease). A chapter that ends conclusively invites the viewer to leave satisfied — early.

## Process

### 1. Plan the cold open
Choose the video's single most arresting fact/moment/question from the research. The open states it, stakes it ("by the end you'll see why everyone got this wrong"), and cuts straight into chapter 1. ≤60 seconds.

### 2. Sequence the chapters
One entry per chapter: objective (what the viewer knows/feels after it), 4–8 beat outline grounded in research findings, estimated minutes, and the **cliff** into the next chapter. The final chapter pays off the thesis explicitly.

### 3. Place re-engagement beats
Mark concrete pattern interrupts near the ~25% and ~65% marks of total runtime: a format change (archival insert, on-screen demonstration, tonal shift), a direct question to the viewer, or a mid-video re-hook ("that was the official story — here's what the records show"). These are retention infrastructure; the script stage writes them as real moments.

### 4. Design the retention-curve intent
Note the expected curve shape and countermeasures: Cliff (weak open) → the cold-open plan; Gradual Decline (pacing) → pacing changes per chapter; Bumps (chapters that spike) → those are the shorts-extraction candidates for publish.

### 5. Chapter visual identities
One line per chapter on how its look/grammar differs (location, palette shift, graphic language) so chapter boundaries are *felt*, not just labeled.

### Quality Gate
- [ ] Cold open leads with the key insight; ≤60s; no intro.
- [ ] One entry per chapter; objectives distinct; escalation toward the payoff.
- [ ] Every chapter ends on a written cliff.
- [ ] Re-engagement beats placed near 25%/65% with concrete mechanisms.
- [ ] Chapter visual identities noted.

## Common Pitfalls

- Chronological order by default — order by tension, use time jumps when they serve the thesis.
- Beats the research can't support (send back to idea for more research instead of inventing).
- Re-engagement "beats" that are just topic changes with no format shift.

## References

- First-30s drop; pattern interrupts; curve shapes (cliff/gradual/bump): https://prepublish.ai/guides/youtube-retention-guide
- Re-engagement beats at 25%/65%; benchmarks: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
