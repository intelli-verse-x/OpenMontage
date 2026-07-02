# Asset Director — Series Pipeline

## When To Use

Resolve assets for every scene across ALL episodes: narration (or dialogue voices), visuals, music beds, and captions — with **cross-episode consistency** as the primary constraint. All generation routes through selectors scored by `lib/scoring.py`.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan` (all episodes), `script`, arc style bible | What to resolve |
| Tools | `tts_selector` (required), `image_selector`, `video_selector`, `music_gen`, `subtitle_gen` | Asset resolution |
| Scoring | `lib/scoring.py` | Provider routing + audit trail |

## Operating Principles

- **One voice for the whole series.** Select the narration voice (or host/guest pair for podcast) ONCE, record the exact voice ID in the manifest, and reuse it for every episode. A provider/voice change mid-series is a send-back.
- **Style-bible conformance on every visual.** Palette, framing, and treatment come from the arc; generated b-roll prompts must include the style bible's constraints.
- **Audit trail everywhere.** `selected_provider` + `provider_score` on every generated asset, every episode.

## Process

### 1. Lock voices
`tts_selector` for the narrator (or both podcast personas). Generate a test line per voice, confirm against the brief's persona description, then batch-generate all episodes with the same voice ID + settings. Podcast: distinct, contrasting voices for host vs guest.

### 2. Resolve visuals per episode
Per scene: generate/stock/supplied. Prompts carry `information_role` + `shot_intent` + style-bible constraints. Reuse recurring elements (host treatment, segment cards) from a shared asset set rather than regenerating per episode.

### 3. Music beds
One theme family for the series (intro sting, body bed, outro) generated once via `music_gen` and reused; per-episode variation only where the arc calls for it.

### 4. Captions
`subtitle_gen` per episode from the final VO. One caption style for the series (per style bible), delivered as data files for compose.

### 5. Budget check
Track spend per episode; if total > 90% of budget with episodes unresolved, alert the EP with a per-episode cost breakdown before downgrading.

### Quality Gate
- [ ] Same voice ID(s) across all episodes; test line approved before batch.
- [ ] Every scene in every episode has a resolved asset.
- [ ] Recurring elements shared, not regenerated (consistency + cost).
- [ ] Series music theme reused; caption style uniform.
- [ ] Scoring audit trail complete.

## Common Pitfalls

- Re-running tts_selector per episode and getting a "similar" voice — lock the ID.
- Generating recurring segment cards fresh each episode (drift + waste).
- Batch-generating all narration before the test line is approved.
