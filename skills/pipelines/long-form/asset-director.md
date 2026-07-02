# Asset Director — Long-Form Pipeline

## When To Use

Resolve narration and every chapter's visuals for a 10–60 minute piece. Volume is the challenge: hundreds of shots, one voice, one look. All generation routes through selectors scored by `lib/scoring.py`.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan` (all chapters), `script` | Shots + narration |
| Tools | `tts_selector` (required), `video_selector`, `image_selector`, `music_gen`, `subtitle_gen` | Resolution |
| Scoring | `lib/scoring.py` | Provider routing + audit trail |

## Operating Principles

- **One narrator, test-first.** Select via `tts_selector` per the brief's voice preference (professional_male / professional_female / warm_friendly / authoritative); generate ONE test paragraph; get approval; then batch the full narration with the locked voice ID + settings (source pipeline defaults: stability 0.7, similarity 0.75).
- **Stock-first for the real world.** Real places/events/objects: stock (Pexels/Pixabay-class) before generation — authenticity reads at documentary length. Generate where stock fails (abstractions, reconstructions, chapter cards).
- **Music is architecture, not wallpaper.** Beds follow the chapter arc's energy; ~15% volume under narration (source default); silence is allowed at dramatic beats.

## Process

### 1. Narration
Test line → approval → batch per chapter (per-chapter files so the editor can conform chapters independently). Record voice ID + settings + provider score.

### 2. Visuals per chapter
Work chapter by chapter against the scene plan's source intents: stock search first for real-world shots; `video_selector`/`image_selector` (scored) for generated ones; graphics/data scenes noted for the compose overlay pass. Verify licences on stock (record source + license per asset).

### 3. Music
`music_gen` per chapter-energy group (not per scene); intro/outro stings + interrupt-moment accents. Gain-staged ~15% under narration.

### 4. Captions
`subtitle_gen` from the final narration per chapter — needed for accessibility and the publish stage's chaptered SRT.

### 5. Budget discipline
Long-form burns budget on volume. Estimate total before batching; prefer stock (cheap) over generation; if projected spend > budget, downgrade generated b-roll in low-stakes beats first, never the interrupt moments.

### Quality Gate
- [ ] One voice ID across all chapters; test-line approved before batch.
- [ ] Every scene resolved; stock licences recorded; evidential shots match their claims.
- [ ] Music per chapter energy at ~15% under narration.
- [ ] Per-chapter caption files present.
- [ ] Scoring audit trail complete; spend ≤ budget.

## Common Pitfalls

- Batch-generating 30 minutes of narration before the voice is approved.
- Generated footage standing in for real events without the script flagging it as reconstruction.
- One music bed looping for 30 minutes (fatigue reads as boredom in the retention curve).
