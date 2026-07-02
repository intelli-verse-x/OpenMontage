# Publish Director — Shorts Pipeline

## When To Use

Package the approved render(s) for the target platform(s): metadata, cover frame, scheduling, and — for multi-part or region-variant briefs — the full release kit (ordering, pinned comments, QR end-card checks).

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `render_report`, `final_review`, `brief` | What to publish + variant declarations |

## Process

### 1. Per-platform metadata
- Title: front-load the hook phrase (first ~40 chars are what feeds show).
- Description: 1–2 lines + hashtag set per platform; for `quiz_mystery`, include the part indicator ("Part 1/3") and the series tag.
- Hashtags: 3–5 targeted per platform; no hashtag walls.

### 2. Cover frame
Pick a frame where the hook text is fully legible — usually within the first 2 seconds. Never a mid-transition frame.

### 3. Multi-part release kit (quiz_mystery and declared series)
- Schedule parts in order with a consistent gap (e.g. 24h) so Part 1's comments prime Part 2.
- Pinned-comment template per part ("Answer in Part 3 — follow so you don't miss it").
- Cross-link: each description references the previous/next part.
- If the brief requested a QR end card, verify the QR resolves and is inside safe zones.

### 4. Region variants
For each declared region (e.g. India / USA): apply the region's peak posting window, hashtag set, and caption style from the brief. One master video, N metadata entries in the publish_log.

### 5. Export + log
Export directory: video(s) + cover(s) + `metadata.json` per platform/region. `publish_log` records paths, platforms, schedule, and templates used.

### Quality Gate
- [ ] Duration/dimensions satisfy each target platform's spec.
- [ ] Cover frame legible; hook phrase in the title.
- [ ] Multi-part: order, gaps, pinned comments, cross-links all present.
- [ ] Region variants: complete metadata set per region.

## Common Pitfalls

- Publishing Part 2 before Part 1 has its pinned comment set — the loop between parts is the growth engine.
- One global hashtag set for all regions when the brief declared variants.
- A cover frame chosen for aesthetics that doesn't state the hook.

## References

- Platform algorithm behavior / distribution mechanics: https://medium.com/@antoinelacombled/cracking-the-youtube-shorts-algorithm-a-study-of-3-3-billion-views-4711fdf7931b
- Short-form platform strategy (2026): https://www.digitalapplied.com/blog/short-form-video-strategy-shorts-tiktok-reels-2026
