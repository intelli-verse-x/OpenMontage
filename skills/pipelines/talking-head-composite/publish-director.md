# Publish Director — Talking-Head Pipeline

## When To Use

Package the rendered talking-head for its target placement with the right metadata and a final spec check, and preserve the re-editable source for future iterations.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["compose"]["render_report"]`, `state.artifacts["compose"]["final_review"]`, `state.artifacts["idea"]["brief"]` | Output + placement |

## Process

### 1. Confirm Placement Spec Compliance
| Placement | Spec |
|-----------|------|
| Shorts / Reels / TikTok | ≤ 60–180s, 1080×1920 (9:16), H.264 MP4, 30fps |
| Square feed | 1080×1080 (1:1), MP4 |
| Web / webinar | 1920×1080 (16:9), MP4 |

Re-probe the output with ffprobe and assert duration, resolution, fps, and codec against the target placement. The duration should match the narration length. Fail back to compose if any check fails.

### 2. Package With Metadata
Assemble the export directory:
- the video MP4 (named per placement convention),
- a poster/first-frame still,
- a `metadata.json` with `title`, `topic`, `presenter`, `voice_id`, `locale`, `aspect`, `duration`, `dimensions`, `captions_burned`, `transcript_source`,
- the `studio_url` + `editable_artifact_dir` from the render_report so the editable source is discoverable for the next iteration.

### 3. Preserve the Re-Editable Source
Do not discard the editable artifact. Record its location (and S3 URI if synced) in the publish log — the whole point of P1 is that this talking-head can be re-opened to tweak captions/brand without re-rendering from scratch.

### 4. Build the Publish Log
- `export_dir`, files exported, placement, locale.
- Spec-check results.
- `editable_artifact` reference (dir + studio_url + s3_uri).
- Synthesis provenance (voice provider + score, portrait provider + score) for auditability.

### 5. Quality Gate
- [ ] Output satisfies the target placement spec (duration, dimensions, fps, codec).
- [ ] Export directory contains the video + poster + metadata.
- [ ] `studio_url` / editable artifact reference preserved in the publish log.
- [ ] Synthesis provenance (voice/portrait provider + score) recorded.

## Common Pitfalls

- Wrong resolution for the declared aspect preset.
- Dropping the editable artifact reference, so the next caption tweak means re-rendering.
- Forgetting the locale tag when a localized cut was requested.
- Losing the synthesis provenance, breaking the scoring audit trail.
