# Scene Director — App-Preview Pipeline

## When To Use

You plan how the viewer's attention moves through the app's screens. This is the **anti-slideshow stage** and the pipeline's hard gate: an app preview that is just a sequence of static screenshots with a caption each scores `fail` on the slideshow-risk gate and will be rejected.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | Copy + screen count + brand |
| Gate | `lib/slideshow_risk.py` | Scene-level anti-slideshow scoring |
| Tools | `frame_sampler` (optional) | Pick the most legible crop of each screen |
| Playbook | Active style playbook | Motion + typography defaults |

## The Slideshow Gate (why this stage is hard)

`score_slideshow_risk(scenes, renderer_family, render_runtime="hyperframes")` scores six dimensions. App previews fail when:

- scenes lack a stated `information_role` (what the screen proves),
- camera movement has no stated purpose (`shot_intent`),
- every scene uses the same shot size / template,
- text cards dominate (brief mode penalizes typography-only scenes).

Your plan must give **every screen scene** both an `information_role` and a motivated `shot_intent`, and must **vary shot sizes/layouts** across scenes.

## Scene Shape (mirrors the compose adapter)

The composition the adapter authors has three scene kinds. Plan them explicitly:

| Scene type | Role | Motion |
|------------|------|--------|
| `hook` | States the core value prop; opens muted-legible in first 5s | static, kinetic text reveal |
| `screen_demo` | Demonstrates one feature (screenshots mode) | **motivated Ken-Burns push** to draw the eye to the proof |
| `text_card` | One benefit (brief mode only — slideshow-prone, use sparingly) | static |
| `cta` | Drives the install | static, confident close |

## Process

### 1. Open With the Hook Scene
- `type: hook`, `information_role: "states the app's core value proposition"`.
- `shot_intent: "open muted with a legible hook in the first 5s"`.
- `shot_language: { shot_size: full, camera_movement: static }`.

### 2. Plan One Screen Scene Per Screenshot (screenshots mode)
For each screen, give it a distinct purpose and motion:
- `information_role`: `"demonstrates feature: <benefit from the caption>"` — concrete, not "shows the app".
- `shot_intent`: tie the Ken-Burns push to the proof, e.g. `"push in on the streak counter so the eye lands on progress"`. The move must be **motivated**, never arbitrary.
- **Vary `shot_size` across scenes** (alternate `medium` / `wide`) and `camera_movement: push_in` where it earns attention. Use `frame_sampler` to choose the crop that keeps the key UI element readable.
- Do not repeat one template for all screens — variation is what defeats the gate.

### 3. Brief Mode (no screenshots) — minimize text cards
- Each `text_card` has `information_role: "states a single benefit"`.
- Keep them few (2–4). Text-only previews are inherently slideshow-prone; if real screens become available, prefer them.

### 4. Close With the CTA Scene
- `type: cta`, `information_role: "drives the download action"`, `shot_intent: "land the CTA with a confident close"`.

### 5. Score Before Checkpointing (MANDATORY)
Run `score_slideshow_risk(scenes, renderer_family="flat-motion-graphics", render_runtime="hyperframes")`:
- verdict `strong` / `acceptable` → proceed.
- verdict `revise` → add motion intent / vary shot sizes / add a screen, then re-score.
- verdict `fail` → do not checkpoint; revise until ≥ `acceptable`.
Record the verdict + per-dimension breakdown in `scene_plan.metadata.slideshow_risk`.

### 6. Quality Gate
- [ ] Every screen scene has a concrete `information_role`.
- [ ] Every screen scene has a motivated `shot_intent` (no arbitrary push-in).
- [ ] Shot sizes / layouts vary across scenes.
- [ ] Hook precedes screens; CTA closes.
- [ ] Slideshow-risk verdict ≥ `acceptable` (no `fail`).

## Common Pitfalls

- Giving every screen the same `push_in` with no stated reason — the gate reads this as a slideshow.
- "Shows the home screen" as an information_role — say what it *proves*.
- Defaulting to brief-mode text cards when screenshots exist.
- Skipping the pre-checkpoint slideshow score and discovering the `fail` at compose.
