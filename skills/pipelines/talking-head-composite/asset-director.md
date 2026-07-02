# Asset Director — Talking-Head Pipeline

## When To Use

Synthesize the inputs the composite render needs: the **narration audio** (one voiced track), the **presenter portrait** (one front-facing image), per-section captions in order, and — only when it earns it — an optional music bed under the voice.

## Provider Routing via Scoring (the P2 contract)

This stage **never hardcodes a provider.** Every synthesized asset goes through a selector tool that delegates to `lib/scoring.py`:

- `tts_selector` (capability `text_to_speech`) — voices the narration. It ranks all available voice providers (`elevenlabs`, `openai`, `google`, `doubao`, `piper`, …) via `rank_providers(candidates, task_context)` and picks the highest-scored *available* one. If a provider's key is invalid (e.g. ElevenLabs 401), the selector falls through to the next-best available provider — never silently no-ops.
- `image_selector` (capability `image_generation`) — generates the presenter portrait when one isn't provided. Same scoring contract.
- `music_gen` — optional background bed.
- `subtitle_gen` — usually unnecessary (the compose adapter burns captions natively), available if a separate caption asset is needed.

Build `task_context` with `budget_remaining_usd` (from the cost tracker), `style_keywords` (persona/emotion/brand), and `asset_type`. Every synthesized asset must record `selected_provider` + `provider_score` in the manifest so the routing decision is auditable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]`, `state.artifacts["script"]`, `state.artifacts["idea"]["brief"]` | Narration, sections, persona, brand |
| Scoring | `lib/scoring.py` (via selector tools) | Provider routing |
| Tools | `tts_selector`, `image_selector`, `music_gen`, `subtitle_gen` | Synthesis |
| Budget | `tools/cost_tracker.py` | Spend governance |

## Process

### 1. Synthesize the Narration (REQUIRED)
- Feed the full spoken narration (`script.metadata.full_narration`) to `tts_selector` with the chosen `voice_id`/`emotion` in `task_context`.
- The selector picks + calls the best available voice provider and returns the audio path + `selected_provider` + `provider_score`.
- If the top provider's key is invalid, confirm the selector fell through to the next available one (do not ship a silent/empty track).

### 2. Resolve / Generate the Presenter Portrait (REQUIRED)
- If the brief supplied `portrait_path`, use it.
- Otherwise generate via `image_selector` using the persona-derived prompt: **front-facing, head-and-shoulders, mouth closed, evenly lit, centered**, on-brand background. The renderer detects the mouth and overlays motion — a clear front-facing mouth is what makes lip-sync land.
- Record `selected_provider` + `provider_score`.

### 3. Optional Music Bed (under the voice)
- Add a bed only if the brief calls for it. Route via `music_gen`, gain-stage **well under** the narration (the voice is the message), and record loudness in `metadata.audio_settings`.

### 4. Captions
- The compose adapter burns captions from the narration (script-timed, or Whisper when present), so a separate `subtitle_gen` asset is usually unnecessary. Carry the ordered per-section caption text in `metadata.captions` for the edit stage.

### 5. Budget Discipline
- Spend is the one TTS call + (optionally) one portrait generation. Before any paid call: `cost_tracker.estimate → reserve`; after: `reconcile`. If spend would exceed the $0.50 cap, drop the optional music rather than blocking.

### 6. Build the Asset Manifest
Every asset has a schema-valid `type` + (optional) `scene_id`. Use `metadata` for:
- `audio` (narration path + voice + provider selection)
- `portrait` (path + provider selection if generated)
- `captions` (ordered per-section text)
- `provider_selections` (selected_provider + provider_score per synthesized asset)
- `audio_settings`

### 7. Quality Gate
- [ ] Narration audio present and non-empty (synthesized via `tts_selector`).
- [ ] Presenter portrait present (provided or via `image_selector`), front-facing + mouth-closed.
- [ ] Per-section captions present and correctly ordered.
- [ ] Every synthesized asset records `selected_provider` + `provider_score`.
- [ ] No hardcoded provider anywhere — synthesis went through a selector.
- [ ] Spend ≤ budget.

## Common Pitfalls

- Calling `elevenlabs_tts` / a specific provider directly instead of `tts_selector` (breaks scoring + audit, and the 401-fallthrough behavior).
- Generating a 3/4 or stylized portrait whose mouth is hard to locate — lip-sync placement degrades.
- A music bed that fights the narration — the voice must stay dominant.
- Losing caption order so section N shows section M's line.
