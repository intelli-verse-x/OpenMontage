# Publish Director — Series Pipeline

## When To Use

Package the approved episodes as a series: per-episode metadata, playlist/series structure, thumbnail set, release schedule, and the localization handoff when locales were declared.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `render_report`, `final_review`, `brief` | Episodes + declarations |
| Pipeline | `localization-dub` | Handoff target for declared locales |

## Process

### 1. Per-episode metadata
- Title pattern: consistent series prefix + episode-specific hook phrase ("ML in 5 — E3: Why your model lies").
- Description: episode summary (2–3 lines) + series links (previous/next/playlist) + chapter timestamps (from the arc's chapter plan).
- Tags/hashtags per platform.

### 2. Series structure
Playlist (YouTube) / series collection metadata: series title, description, ordered episode list. Verify episode order matches the arc.

### 3. Thumbnails
One template from the style bible, per-episode variation (episode number + key visual). Sample all thumbnails side-by-side: they must read as one series at a glance.

### 4. Release schedule
Cadence from the brief (e.g. weekly, same weekday/time). Record the full schedule in the publish_log. For learning series, sequential release order is mandatory (curriculum depends on it).

### 5. Localization handoff (if locales declared)
For each declared locale: record the handoff entry — episode files + scripts + voice notes → `localization-dub` pipeline. Do not attempt in-pipeline dubbing; the dedicated pipeline owns voice cloning/subtitle localization.

### 6. Export + log
Export directory: per-episode video + thumbnail + `metadata.json`, series-level `series.json` (order, schedule, playlist metadata), localization handoff manifest.

### Quality Gate
- [ ] Every episode has complete metadata + chapter timestamps.
- [ ] Playlist order matches the arc; schedule recorded.
- [ ] Thumbnail set reads as one series.
- [ ] Localization handoff manifest present when locales declared.

## Common Pitfalls

- Chapter timestamps drifting from the final cut (regenerate from the rendered files, not the plan).
- Thumbnails redesigned per episode instead of templated.
- Dubbing attempted inline instead of handing off to localization-dub.
