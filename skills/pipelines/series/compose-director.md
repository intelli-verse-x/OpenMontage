# Compose Director — Series Pipeline

## When To Use

Render every episode via the locked runtime, apply the HyperFrames finishing pass where planned, and verify per-episode quality plus cross-episode consistency. Produces `render_report` + `final_review`.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime` and dispatch through `video_compose.execute()`. For `hyperframes`, `lint` + `validate` must pass before render. A silent runtime swap is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if unavailable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `edit_decisions`, `asset_manifest`, `scene_plan` | What to render |
| Tools | `video_compose`, `hyperframes_compose`, `audio_mixer` | Rendering + mix |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check per episode |

## Process

### 1. Pre-render slideshow re-check (per episode)
Re-score each episode's final scene plan. Any `fail` → do NOT render that episode; send back to scene_plan.

### 2. Render episodes
Target resolution/fps from the brief; the series grammar constants (bumper, lower-thirds, transitions) come from `edit_decisions.metadata.series_grammar` — identical values every episode.

### 3. HyperFrames finishing pass (where planned)
Apply the planned overlays — chapter markers at chapter starts, quiz cards (learning) after their concepts, end cards in the final 5s — as a HyperFrames overlay pass. Lint + validate the overlay composition before compositing. Overlays respect platform safe zones.

### 4. Mix + loudness
VO/dialogue dominant; series music bed gain-staged under it; normalize each episode to the platform loudness spec so no episode is hotter than its neighbors.

### 5. Verify

**Per episode:**
- [ ] Valid container; duration ±10% of target; resolution/fps correct.
- [ ] Slideshow re-check verdict recorded (governance audit trail).
- [ ] Captions synced; overlays inside safe zones.
- [ ] First-30s frame-sample: hook visible, no cold series intro.

**Cross-episode:**
- [ ] Sample one mid-episode frame per episode; style-bible conformance (palette/type/lower-thirds identical).
- [ ] Loudness within ±1 LU across episodes.
- [ ] Same voice(s) confirmed across episodes (spot-listen).

Record all findings in `final_review`; any cross-episode drift → send back the offending episode only.

## Common Pitfalls

- Rendering all episodes before verifying episode 1 end-to-end — validate the pilot first, then batch.
- Overlay pass skipping lint/validate because "it's just a chapter marker".
- Per-episode loudness normalized in isolation, producing jumps at playlist autoplay boundaries.

## References

- Chapter/bump retention patterns (chapters at bump points): https://prepublish.ai/guides/youtube-retention-guide
- Safe zones for overlay text: https://zeely.ai/blog/tiktok-safe-zones/ , https://kreatli.com/guides/safe-zone-guide
