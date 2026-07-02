# Scene Director — Talking-Head Pipeline

## When To Use

You plan how attention moves across the narration. This is the **anti-static stage** and the pipeline's hard gate: a talking head that is one motionless portrait reading text scores `fail` on the slideshow-risk gate and loses retention. Motion here comes from the **captions and section cadence** (and optional B-roll cutaways), since the face itself is a single portrait with a lip overlay.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | Sections + persona + brand |
| Gate | `lib/slideshow_risk.py` | Section-level anti-static scoring |
| Playbook | Active style playbook | Caption motion + typography defaults |

## The Slideshow Gate (why this stage is hard)

`score_slideshow_risk(sections, renderer_family="composite-talking-head", render_runtime="composite")` scores six dimensions. Talking heads fail when:

- sections lack a stated `information_role` (what idea the beat lands),
- nothing moves but the mouth — no caption motion, no emphasis change, no cutaway (`shot_intent`),
- every section uses the same caption template / framing,
- one long undifferentiated monologue with no beats.

Your plan must give **every section** both an `information_role` and a motivated motion `shot_intent`, and must **vary caption emphasis/framing** across sections.

## Scene Shape (mirrors the compose adapter)

The composite render is the presenter portrait + lip overlay + a timed caption per section. Plan the beats explicitly:

| Beat type | Role | Motion |
|-----------|------|--------|
| `hook` | States the stakes/promise; opens muted-legible | kinetic caption reveal over the presenter |
| `point` | Delivers one idea from a section | caption emphasis change; optional **motivated B-roll cutaway** to illustrate the idea |
| `proof` | Concrete example/number | callout caption / emphasized keyword |
| `cta` | The takeaway / install action | confident closing caption |

## Process

### 1. Open With the Hook Beat
- `type: hook`, `information_role: "states the core promise / problem"`.
- `shot_intent: "open muted with a legible hook caption animating over the presenter in the first 5s"`.

### 2. Plan One Beat Per Section
For each narration section, give it a distinct purpose and motion:
- `information_role`: what idea this beat lands — concrete, not "presenter talks".
- `shot_intent`: the motion that earns attention this beat — e.g. `"emphasize the keyword 'spaced repetition' as the caption snaps in"`, or `"cut to a 2s B-roll of the streak screen while the line about progress plays"`. The motion must be **motivated**, never arbitrary.
- **Vary caption emphasis / framing** across beats (keyword highlight, full-line, lower-third vs centered). Do not repeat one template — variation is what defeats the gate.

### 3. Optional B-roll Cutaways (recommended for longer pieces)
- For sections that describe something visual, plan a short cutaway (a screenshot/clip) over the narration, then return to the presenter. This is the strongest anti-static lever for talking heads.
- Keep the presenter as the spine; cutaways are seasoning, not the meal.

### 4. Close With the CTA Beat
- `type: cta`, `information_role: "delivers the takeaway / drives the action"`, `shot_intent: "land the closing caption with a confident hold on the presenter"`.

### 5. Score Before Checkpointing (MANDATORY)
Run `score_slideshow_risk(sections, renderer_family="composite-talking-head", render_runtime="composite")`:
- verdict `strong` / `acceptable` → proceed.
- verdict `revise` → add caption motion / vary framing / add a B-roll cutaway, then re-score.
- verdict `fail` → do not checkpoint; revise until ≥ `acceptable`.
Record the verdict + per-dimension breakdown in `scene_plan.metadata.slideshow_risk`.

### 6. Quality Gate
- [ ] Every section beat has a concrete `information_role`.
- [ ] Every beat has a motivated motion `shot_intent` (caption motion / emphasis / cutaway — not "talks").
- [ ] Caption emphasis / framing varies across beats.
- [ ] Hook precedes points; CTA closes.
- [ ] Slideshow-risk verdict ≥ `acceptable` (no `fail`).

## Common Pitfalls

- Planning a single motionless portrait for the whole runtime — the gate reads this as a slideshow of one frame.
- "Presenter explains the feature" as an information_role — say what the beat *proves*.
- The same caption template every beat, which reinforces the static feel.
- Skipping the pre-checkpoint slideshow score and discovering the `fail` at compose.
