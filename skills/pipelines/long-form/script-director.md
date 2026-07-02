# Script Director — Long-Form Pipeline

## When To Use

Write the full narration from the chapter arc: the cold open, every chapter's beats, the pattern interrupts as concrete moments, and the close. Long-form scripts pass a **multi-LLM reviewer panel** before approval.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["chapters"]["scene_plan"]` | Arc, cliffs, beat placement |
| Skill | `meta/reviewer` | Multi-model review panel |
| Tool | `text_director` (optional) | LLM drafting, routed via `lib/scoring.py` |

## Operating Principles

- **The first 30 seconds are the whole game.** Hook + stake, spoken in the video's own voice, zero throat-clearing. More than 40% audience loss in the first 30s means the open failed — write it to survive that test.
- **Spoken word, not essay.** Sentences you can breathe through; contractions; rhetorical questions used sparingly and answered.
- **Claims carry sources.** Every factual claim maps to a research source from the brief; unsourced claims get cut or hedged explicitly.
- **Pattern interrupts are written moments.** "At the 65% beat, we stop the narrative and run the numbers on screen" — a directive the scene stage can shoot.

### Pacing by content type
`measured` (documentary): longer beats, silence tolerated. `steady` (educational): concept → example → recap loops. `dynamic` (explainer): fast beats, frequent visual handoffs. `natural` (interview): scripted framing around unscripted answers. `deliberate` (deep_dive): dense, but a breather every 2–3 minutes.

## Process

### 1. Write the cold open (30–60s)
The arresting moment first, then the stake, then a hard cut into chapter 1. Read it aloud; cut every word that delays the hook.

### 2. Write the chapters
Follow each chapter's beat outline. End each chapter with its cliff verbatim from the arc (or stronger). Write the re-engagement beats as full scripted moments at their planned positions.

### 3. Write the close
Pay off the thesis explicitly; end with one forward action (subscribe framed around the content promise, or the next question). No 3-minute outro — close within 60s of the payoff.

### 4. Run the reviewer panel
`meta/reviewer` with at least two distinct models when available (content-factory used a 3-model panel). Reviewers check: factual support, hook strength, pacing sag, cliff quality. Record disagreements + resolutions in `metadata.review_panel`. Address material notes before submitting.

### 5. Build the script artifact
Per-chapter narration with beat markers, timed re-engagement moments, source map (claim → source), voice/tone notes, `metadata.review_panel`.

### Quality Gate
- [ ] Cold open survives the 30s test (hook + stake, no intro).
- [ ] Every chapter ends on its cliff; interrupts written as moments.
- [ ] Every claim mapped to a source.
- [ ] Reviewer panel run; notes addressed and recorded.
- [ ] Estimated read time within ±10% of target duration.

## Common Pitfalls

- An open that sets context before earning attention.
- Essay prose that narrates poorly (read everything aloud).
- Sagging middles: chapters 3–4 without a written interrupt are where gradual-decline curves die.
- Skipping the reviewer panel to save time — it's the quality gate that survives from the source pipeline.

## References

- First-30s threshold; lead with key insight: https://prepublish.ai/guides/youtube-retention-guide
- Benchmarks + re-engagement beats: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
