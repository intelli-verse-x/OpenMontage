# Publish Director — Playable Pipeline

## When To Use

Final stage. Package the validated playable for each target ad network and assemble the human-facing review bundle. Deliverable: the `publish_log` artifact. No new creative decisions here — package, verify, and hand off.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior | `render_report`, `final_review` | the built + validated playable |

## Per-Network Packaging

Most networks accept a **single-file `index.html`** or a **zip** containing it. Use the build's `zip_path` as the base and adapt per network:

| Network | Format | Size limit | Notes |
|---------|--------|-----------|-------|
| AppLovin | zip (index.html) | ~5 MB | MRAID; CTA via `mraid.open()` |
| ironSource | zip (index.html) | ~5 MB | MRAID; single index.html entry |
| Unity Ads | zip (index.html) | ~5 MB | MRAID container |
| Meta (Audience Network) | single index.html | ~2 MB | uses `FbPlayableAd.onCTAClick()` hook (already wired) |
| Google (AdMob) | single index.html | ~2 MB | strict size; verify ≤ 2 MB |

For each **selected** network, confirm the build's `size_bytes` clears that network's limit. If a network's limit is exceeded, flag it (don't silently ship) and route back to the asset stage to trim (usually the icon).

## Verify the Store CTA

- Confirm `store.app_store_url` and/or `store.play_store_url` are present (or a `fallback_url`).
- Confirm the CTA opens the **correct destination per platform** — the build resolves iOS vs Android at runtime. If only a fallback URL exists, note that real store links should replace it before launch.

## Review Bundle

Assemble for human review:
- the per-network packages (zip / index.html),
- the build `playable_manifest.json`,
- the **two preview screenshots** from the build stage (quiz state + end-card CTA).

## Output — `publish_log` artifact

Must include:
- `export_dir`
- `packages[]` — one per target network: `{ network, path, format, size_bytes, within_limit }`
- `store` `{ app_store_url, play_store_url, fallback_url, cta_verified }`
- `previews[]` — screenshot paths
- `warnings[]` — e.g. "fallback URL in place of real store link", "exceeds Meta 2 MB"

## Success Criteria
- Schema-valid `publish_log`.
- Export directory contains the playable zip + manifest + preview screenshots per target network.

## Common Pitfalls
- Shipping a >2 MB build to Meta/Google without flagging the overage.
- Leaving a `fallback_url` in place of real store links without noting it.
- Omitting the preview screenshots, so the human approves a playable they can't see.
