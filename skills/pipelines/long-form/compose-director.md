# Compose Director — Long-Form Pipeline

## When To Use

Render the chaptered timeline via the locked runtime, apply the overlay finishing pass, and verify retention-critical properties at final quality. Produces `render_report` + `final_review`.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime` and dispatch through `video_compose.execute()`. For HyperFrames overlay passes, `lint` + `validate` must pass before render. A silent runtime swap is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if unavailable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `edit_decisions`, `asset_manifest`, `scene_plan` | What to render |
| Tools | `video_compose`, `hyperframes_compose`, `audio_mixer` | Rendering + mix |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check per chapter |

## Process

### 1. Pre-render slideshow re-check
Re-score each chapter's final scene plan. Any `fail` → do NOT render; send back.

### 2. Render
1920×1080 @ 24fps (or brief override). At 10–60 minutes, render per chapter where the runtime supports it, then concatenate — enables per-chapter re-render on failure instead of full re-renders.

### 3. Overlay finishing pass
Chapter title cards at `metadata.chapter_marks`, lower-thirds for speakers/sources, citation cards where the script's source map calls for on-screen attribution, end card in the final 30s. One template, per-chapter variation. Overlays out of caption areas and broadcast-safe margins.

### 4. Mix + loudness
Narration dominant; music ~15% under; normalize integrated loudness for long-session listening (target the platform spec, e.g. −14 LUFS YouTube) with true-peak ≤ −1 dBTP. No loudness jumps at chapter joins (verify at each boundary).

### 5. Verify

**File checks:**
- [ ] Valid container; duration ±10% of target; spec resolution/fps.

**Retention-critical checks:**
- [ ] First-30s frame-sample: hook + stake visible, no intro card before the hook.
- [ ] Chapter cards land exactly at `chapter_marks`; boundaries audible-join clean.
- [ ] Interrupt moments render with their distinct grammar (spot-check both).
- [ ] Slideshow re-check verdict per chapter recorded in `render_report`.

**Consistency checks:**
- [ ] One frame sampled per chapter: palette/type/lower-thirds consistent.
- [ ] Loudness uniform across chapter joins.

## Common Pitfalls

- Monolithic 40-minute render with no per-chapter recovery path.
- Overlay pass skipping lint/validate.
- Loudness normalized per chapter in isolation, producing steps at joins.
- Verifying the file but never frame-sampling the first 30 seconds at final quality.

## References

- First-30s check rationale: https://prepublish.ai/guides/youtube-retention-guide
