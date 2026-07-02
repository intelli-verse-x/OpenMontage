# Asset Director — App-Preview Pipeline

## When To Use

Produce the assets the composition needs: resolved + phone-framed screenshots (one per planned screen scene), per-screen captions in order, and — only when they earn it — an optional generated background and a muted-autoplay music bed.

## Provider Routing via Scoring (the P2 contract)

This stage **never hardcodes a provider.** Any generated asset goes through a selector tool that delegates to `lib/scoring.py`:

- `image_selector` (capability `image_generation`) — for optional generated backgrounds or a teaser-card visual in brief mode. It ranks all available providers (`flux`, `imagen`, `recraft`, stock, …) via `rank_providers(candidates, task_context)` and picks the highest-scored *available* one.
- `tts_selector` — optional voiceover when the brief requests one (the content-factory source pipeline supports narrated previews). The preview must still fully work muted — VO is reinforcement for hosted/social cuts, never the carrier of the store preview.
- `music_gen` — optional background music bed.
- `subtitle_gen` — optional burned captions (the composition usually renders captions natively, so this is rarely needed).

Build `task_context` with `budget_remaining_usd` (from the cost tracker), `style_keywords` (from the playbook/brand), and `asset_type`. Every generated asset must record `selected_provider` + `provider_score` in the manifest so the routing decision is auditable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["idea"]["brief"]` | What to stage |
| Scoring | `lib/scoring.py` (via selector tools) | Provider routing |
| Tools | `image_selector`, `music_gen`, `subtitle_gen`, `frame_sampler` | Generation / framing |
| Budget | `tools/cost_tracker.py` | Spend governance |

## Process

### 1. Resolve Screenshots (screenshots mode)
- Source order: explicit `screenshot_urls` → `screenshot_dir` → `bundle_id` (enriched catalog).
- Stage one image per planned `screen_demo` scene, in caption order.
- Use `frame_sampler` only if you need to pick the most legible crop of a tall screen.
- The composition phone-frames each screen and applies the planned Ken-Burns push — you do **not** pre-render motion here; you stage clean source images.

### 2. Brief Mode — prepare teaser cards
- No screenshots: each `text_card` scene gets its caption; optionally one generated brand background via `image_selector` (scored, not hardcoded).

### 3. Optional Voiceover (brief-requested only)
- If the brief requests narration, route via `tts_selector` (scored, not hardcoded): one voice, brisk read of the per-screen benefit lines.
- Every VO claim must also exist as on-screen text — store autoplay is muted, so audio may never carry information alone.
- Record the voice ID + provider score in `metadata.provider_selections`.

### 4. Optional Music Bed (muted-autoplay aware)
- App previews autoplay **muted** in the store, so music is decorative. Add a bed only if the brief calls for a hosted/social cut.
- If used, route via `music_gen`, gain-stage low (it must never fight the voiceover), and record loudness in `metadata.audio_settings`.

### 5. Budget Discipline
- Screenshots are resolved, not generated — near-zero cost. Only generated backgrounds/music spend budget.
- Before any paid call: `cost_tracker.estimate → reserve`; after: `reconcile`. If spend would exceed the $0.50 cap, drop the optional asset rather than blocking.

### 6. Build the Asset Manifest
Every asset has a schema-valid `type` + `scene_id`. Use `metadata` for:
- `framed_screens` (path + scene_id + caption, in order)
- `input_mode`
- `provider_selections` (selected_provider + provider_score per generated asset)
- `audio_settings`

### 7. Quality Gate
- [ ] One framed screen asset per planned screen scene (or one card per text scene in brief mode).
- [ ] Captions present and correctly ordered.
- [ ] If VO requested: single voice via `tts_selector`, and every VO claim exists as on-screen text.
- [ ] Every generated asset records `selected_provider` + `provider_score`.
- [ ] No hardcoded provider anywhere — generation went through a selector.
- [ ] Spend ≤ budget.

## Common Pitfalls

- Calling `flux_image` / a specific provider directly instead of `image_selector` (breaks scoring + audit).
- Generating decorative art when real screens already carry the message.
- A loud music bed on a muted-autoplay preview.
- Losing caption order so screen N shows screen M's benefit.
