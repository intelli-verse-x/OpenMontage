# Asset Director — Music-Video Pipeline

## When To Use

Produce the track (if generated) and every shot's footage. **The audio must be finalized and approved before clip generation is accepted** — the beat map, and therefore every cut, derives from it.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `script`, `brief` | Shots + treatment + character refs |
| Tools | `video_selector` (required), `music_gen`, `image_selector`, `subtitle_gen` | Generation |
| Scoring | `lib/scoring.py` | Provider routing + audit trail |

## Operating Principles

- **Audio first, always.** Generate/ingest the track, get it approved, THEN generate clips. A re-generated track shifts every beat.
- **Character consistency is preserve-mode.** For declared characters, generate from the canonical reference and **skip img2img enhancement on frames containing them** (enhancement drifts identity) — this mirrors content-factory's `preserve_character_consistency: true`.
- **Motion in every prompt.** Clip prompts carry the shot's action + impact moment, not just the scene description.

## Process

### 1. Finalize the track
- `generated`: `music_gen` with the brief's spec; present for approval; record provider + score. Confirm the section map against the actual generated structure (it may differ from the spec — update the treatment times if so, via the EP).
- `supplied`: verify format/quality; extract runtime.
- Mark `EP_STATE.audio_final = true` only after approval.

### 2. Generate clips per shot
`video_selector` routed via `lib/scoring.py`. Prompts: world palette + motif state + subject action + camera motion + energy. Generate at the primary aspect; the flagged vertical-cut shots also need center-safe compositions. Verify each clip contains the planned **impact moment** — a clip without its action is a reject.

### 3. Character shots
Include the canonical reference (image or exact description) in every prompt featuring the character; spot-check identity across all appearances before accepting the batch; no img2img enhancement on these frames.

### 4. Lyric captions (optional)
If the brief flags a lyric video: `subtitle_gen` word-timed to the vocal; styled per the playbook.

### 5. Budget
Clips are the cost center. Estimate per-shot cost × shot count before batch generation; if projected spend > budget, reduce shot count in low-energy sections first (verses tolerate longer holds; choruses don't).

### Quality Gate
- [ ] Final approved audio present; `audio_final` set.
- [ ] One clip per shot containing its action/impact moment.
- [ ] Character identity consistent across all appearances.
- [ ] Every generated asset records `selected_provider` + `provider_score`.
- [ ] Spend ≤ budget.

## Common Pitfalls

- Generating clips against a draft track "to save time" — beat drift wastes the entire batch.
- Accepting pretty clips that lack the planned action (nothing lands on the beat later).
- Enhancing character frames with img2img and drifting their identity.
