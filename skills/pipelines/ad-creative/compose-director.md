# Compose Director — Ad-Creative Pipeline

## When To Use

Render the primary variant and every declared aspect variant via the locked runtime, verifying the direct-response-critical properties: muted hook legibility, safe-zone captions, and a readable end card.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime` and dispatch through `video_compose.execute()`. For `hyperframes` (end cards / kinetic hooks), `lint` + `validate` must pass before render. A silent runtime swap is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if unavailable.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `edit_decisions` (incl. `variant_reframes`), `asset_manifest` | What to render |
| Tools | `video_compose`, `hyperframes_compose`, `audio_mixer` | Rendering + mix |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check |

## Process

### 1. Pre-render slideshow re-check
Re-score the final scene plan. `fail` → do NOT render; send back.

### 2. Render the primary (9:16)
1080×1920 @ 30fps (platform default). Captions in the center band (out of top ~200px / bottom ~300px / right ~120px); caption entrances fast (~200–250ms decelerate ease) so text never lags the VO; end card composited static-stable.

### 3. Render aspect variants
Apply `variant_reframes` per shot — subject re-centered per crop_center. **Letterboxing is a reject.** Text layouts re-flowed per aspect (1:1 and 16:9 have their own safe margins), not scaled.

### 4. Mix + loudness
VO dominant; music bed under; normalize to platform ad spec (≈ −14 LUFS integrated, true peak ≤ −1 dBTP). The ad must also fully work muted — audio is enhancement.

### 5. Verify (per variant)

**File checks:**
- [ ] Valid MP4 at the variant's spec; duration ∈ [15, 30]s and matches the edit.

**Direct-response checks (frame-sample):**
- [ ] 0–2s: hook text fully legible muted.
- [ ] By 3s: product visibly on screen.
- [ ] End card: holds ≥1.5s, CTA copy legible at phone scale.
- [ ] Captions inside the variant's safe zones throughout.
- [ ] Slideshow re-check verdict recorded in `render_report`.

## Common Pitfalls

- Verifying the 9:16 and assuming the reframes are fine — check every variant's text placement.
- Caption animation so decorative it delays word visibility.
- Loudness set for sound-on impact, clipping platform normalization.

## References

- Safe zones: https://zeely.ai/blog/tiktok-safe-zones/
- Motion duration/easing tokens (fast entrances ~200-250ms): https://m3.material.io/styles/motion/easing-and-duration
