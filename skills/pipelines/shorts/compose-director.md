# Compose Director — Shorts Pipeline

## When To Use

Render the final short via the runtime locked in `edit_decisions`, verify the stickiness-critical properties (hook legibility, safe zones, loop seam), and produce the `render_report` + `final_review`.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime` and dispatch through `video_compose.execute()`:
- `remotion` → remotion-composer project;
- `hyperframes` → `hyperframes_compose` (lint + validate must pass before render);
- `cloud` → the content-factory ViralShorts compose adapter.

A silent runtime swap is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if the locked runtime is unavailable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `edit_decisions`, `asset_manifest`, `scene_plan` | What to render |
| Tools | `video_compose`, `hyperframes_compose`, `audio_mixer` | Rendering + mix |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check |

## Process

### 1. Pre-render slideshow re-check
Re-score the final scene plan. `fail` → do NOT render; send back to scene_plan.

### 2. Compose
- Canvas 1080×1920 (or platform target), 30fps unless the platform brief says otherwise.
- Captions placed in the center band: nothing persistent in top ~200px, bottom ~300px, right ~120px.
- Caption animation: word-timed reveals synced to VO; use fast entrances (~200–250ms, decelerate ease) so text never lags the voice.
- Mix: VO dominant, music −18 to −14 LUFS under VO, loudness normalized to platform spec (≈ −14 LUFS integrated).

### 3. Render + verify

**File checks:**
- [ ] Valid MP4, 9:16 at target resolution/fps, duration ∈ [15, 60]s and ±10% of target.

**Stickiness checks (frame-sample):**
- [ ] 0–2s: hook promise fully legible with sound off.
- [ ] Captions present from the first word; no caption clipped by safe-zone bands.
- [ ] Last frame → first frame: loop seam is smooth (no luminance/composition jolt).
- [ ] Slideshow re-check verdict recorded in `render_report` (governance audit trail).

### 4. Final review
Record verification notes, warnings, and the per-check results in `final_review`. For multi-part briefs, repeat per part and cross-check visual consistency between parts.

## Common Pitfalls

- Rendering before the slideshow re-check — drift introduced at assets/edit gets baked in.
- Caption block bottom-aligned into the TikTok caption bar.
- Normalizing loudness after the mix approval instead of during it.
- Verifying duration but not the loop seam — replays are the heaviest-weighted signal.

## References

- TikTok safe zones: https://zeely.ai/blog/tiktok-safe-zones/
- Replay weighting / completion focus: https://www.digitalapplied.com/blog/short-form-video-strategy-shorts-tiktok-reels-2026
- Motion timing tokens (entrances ~250ms decelerate, exits ~200ms accelerate): https://m3.material.io/styles/motion/easing-and-duration
