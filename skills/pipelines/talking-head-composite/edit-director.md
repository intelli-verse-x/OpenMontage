# Edit Director — Talking-Head Pipeline

## When To Use

Turn the scene plan + assets into a concrete, schema-valid `edit_decisions`: the ordered caption timeline aligned to the narration, the locked render runtime, and the exact inputs the content-factory compose adapter expects.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]`, `state.artifacts["assets"]`, `state.artifacts["script"]` | Beats, audio/portrait, narration |
| Playbook | Active style playbook | Caption pacing + typography defaults |

## Process

### 1. Lock the Runtime
Set `edit_decisions.render_runtime = "composite"` (inherited from idea). The compose stage delegates to the content-factory `compose_from_artifacts` adapter, which runs the composite avatar renderer. Do not change it (`video_compose` cannot render composite — escalate, never substitute).

### 2. Align Captions to the Narration
- Caption timing is **script-timed** (sections distributed across the audio duration) or **transcript-driven** (Whisper word timings when available). The adapter handles burning; your job is the per-section caption text + order + emphasis.
- One caption (or a tight pair) per section beat, in narration order.
- Carry caption emphasis from the scene plan (keyword highlight, full-line, lower-third vs centered).

### 3. Honor the Narration Length
- Total duration follows the audio — do not invent a target that drifts from the narration.
- No leading/trailing dead air; the first caption lands with the hook line, the last with the closing line.

### 4. Plan B-roll Cutaways (if any)
- For beats the scene plan marked as cutaways, record the cutaway asset + its in/out times over the narration, then return to the presenter.

### 5. Assemble `compose_adapter_inputs`
Put everything the adapter needs in `metadata.compose_adapter_inputs` so it does **not** re-derive copy or re-plan:
- `title` (brand + presenter identity for the frame)
- `script_text` (full narration) **or** `sections` (ordered `{text, ...}`)
- `portrait_path` (from assets)
- `audio_path` (from assets)
- `voice_id`, `emotion`
- `aspect`
- `brand_context` (`accent_color`, `name`)

### 6. Keep the Schema Clean
Use `cuts[]` for caption/section segments + durations and `transitions` for any cutaway in/out. App-specific detail lives in `metadata` (`compose_adapter_inputs`, `aspect`, `caption_emphasis`, `audio_settings`).

### 7. Quality Gate
- [ ] `render_runtime == "composite"`.
- [ ] One caption per section, in narration order, with emphasis carried from the scene plan.
- [ ] Total duration matches the narration length; no dead air at head/tail.
- [ ] `metadata.compose_adapter_inputs` carries title, narration/sections, portrait, audio, brand — everything the adapter needs.

## Common Pitfalls

- Changing the runtime off `composite` (the lip-synced presenter only comes from the composite adapter).
- Caption timing that ignores the narration, so text and speech drift apart.
- Captions that start after the first word — muted feed viewers bounce before speech "arrives".
- Caption blocks placed in the bottom ~300px / right ~120px of a 9:16 frame, where platform UI covers them.
- Inventing a fixed duration that doesn't match the audio.
- Forgetting to pass the portrait + audio paths + copy into `compose_adapter_inputs`, leaving the adapter to re-derive them (it is thin by design and won't).

## References

- Captions from the very first word: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- 9:16 platform safe zones (top 150–200px, right 120px, bottom 250–300px): https://zeely.ai/blog/tiktok-safe-zones/
