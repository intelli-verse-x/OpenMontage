# Compose Director — Music-Video Pipeline

## When To Use

Render the beat-synced timeline via the locked runtime and verify the properties that make it a music video: exact track conformance, beat alignment at section boundaries, and one coherent visual world.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime` and dispatch through `video_compose.execute()`. For `hyperframes` overlay passes, `lint` + `validate` must pass before render. A silent runtime swap is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if unavailable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `edit_decisions`, `asset_manifest`, `scene_plan` | What to render |
| Tools | `video_compose`, `hyperframes_compose`, `audio_mixer` | Rendering + mix |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check |

## Process

### 1. Pre-render slideshow re-check
Re-score the final scene plan. `fail` → do NOT render; send back.

### 2. Compose against the audio master
- The track is the master clock: total video duration == track duration, sample-accurate. Never stretch/trim audio to fit video.
- Apply cuts at the beat-anticipated timestamps from `edit_decisions`.
- Lyric captions (if any): word-timed, inside safe zones on vertical variants.
- Mix: the track untouched at full level; any SFX/ambience ducked well under it.

### 3. Render + verify

**File checks:**
- [ ] Duration == track length; target aspect/resolution/fps; valid container.

**Beat checks (spot-check at minimum 3 section boundaries):**
- [ ] Chorus entries: the visual change lands with the drop (±1 frame of the anticipated point).
- [ ] Sampled mid-section cuts sit on their assigned beats.

**World checks:**
- [ ] 6-frame sample across sections reads as one video (palette/motif consistent).
- [ ] Declared characters identical across appearances.

**Stickiness checks:**
- [ ] Opening 2s establishes the world (feed-clip hook).
- [ ] Slideshow re-check verdict recorded in `render_report`.

### 4. Vertical variant (if declared)
Render the flagged section as the 9:16 cut: center-weighted reframe (not letterbox), lyric/text inside safe zones (top ~200px, bottom ~300px, right ~120px), loop seam considered (chorus cuts loop naturally if the entry and exit match).

## Common Pitfalls

- Conforming audio to video (fade/trim on the track) instead of the reverse.
- Verifying duration but never spot-checking beat alignment — the defining property.
- Vertical variant produced by letterboxing the 16:9 master.

## References

- Beat alignment practice: https://www.youtube.com/watch?v=yU3U6TdV5Hw
- Vertical safe zones: https://zeely.ai/blog/tiktok-safe-zones/
- Loop design for chorus cuts: https://www.youtube.com/watch?v=gP76Sk_P6Ng
