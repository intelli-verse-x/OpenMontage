# Publish Director — App-Preview Pipeline

## When To Use

Package the rendered preview for the target store with the right metadata and a final spec check. App previews have strict store requirements; this stage ensures the export is submission-ready and that the re-editable source is preserved for future iterations.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["compose"]["render_report"]`, `state.artifacts["compose"]["final_review"]`, `state.artifacts["idea"]["brief"]` | Output + store target |

## Process

### 1. Confirm Store Spec Compliance
| Store | Spec |
|-------|------|
| App Store | 15–30s hard window, .mov/.mp4/.m4v, H.264 video + AAC stereo audio, ≤500MB, ≤30fps, device-preset resolution (portrait 1080×1920 or 886×1920; landscape 1920×1080) |
| Play Store | ≤ 30s feature graphic / promo video, 1080×1920 or 1920×1080, MP4 |

Re-probe the output with ffprobe and assert duration, resolution, fps, and codec against the target store. Fail back to compose if any check fails. App Store previews must show **in-app footage only** — flag any lifestyle/device-in-hand footage as a compliance failure.

### 1b. Set the Poster Frame
Apple defaults the poster frame to the 5-second mark. Use `metadata.poster_frame_time_s` from edit_decisions (or pick the cleanest caption-visible frame) and record the chosen timestamp + exported still in the publish log — the poster frame is what most store visitors see before pressing play.

### 2. Package With Metadata
Assemble the export directory:
- the preview MP4 (named per store convention),
- a poster/first-frame still,
- a `metadata.json` with `app_name`, `store`, `locale`, `device_preset`, `duration`, `dimensions`,
- the `studio_url` + `editable_artifact_dir` from the render_report so the editable source is discoverable for the next iteration.

### 3. Preserve the Re-Editable Source
Do not discard the editable artifact. Record its location (and S3 URI if synced) in the publish log — the whole point of P1 is that this preview can be re-opened and tweaked without regenerating from scratch.

### 4. Build the Publish Log
- `export_dir`, files exported, store, locale.
- Spec-check results.
- `editable_artifact` reference (dir + studio_url + s3_uri).

### 5. Quality Gate
- [ ] Output satisfies the target store's preview spec (duration, dimensions, fps, codec).
- [ ] Export directory contains the preview + poster + store metadata.
- [ ] `studio_url` / editable artifact reference preserved in the publish log.

## Common Pitfalls

- Exporting a preview that's a second over the 30s ceiling — stores reject it.
- Wrong resolution for the declared device preset.
- Leaving the poster frame at whatever happens to be at 5s instead of setting it deliberately.
- Dropping the editable artifact reference, so the next edit means starting over.
- Forgetting the locale tag when a localized cut was requested.

## References

- Apple App Preview specifications (duration, codecs, 500MB, resolutions, poster frame): https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/
- Apple App Previews overview (in-app footage requirement): https://developer.apple.com/app-store/app-previews/
