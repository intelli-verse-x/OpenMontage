# Publish Director — Music-Video Pipeline

## When To Use

Package the hero cut and platform variants with music-appropriate metadata, choose the cover frame, and record the localization handoff if declared.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `render_report`, `final_review`, `brief` | Outputs + targets |

## Process

### 1. Package the variants
- Hero (16:9, YouTube): full track.
- Vertical chorus cut (9:16, Shorts/Reels/TikTok): the flagged section, loop-checked. This is the discovery asset — treat it as first-class, not an afterthought.
- Any additional declared aspects.

### 2. Metadata
- Title: artist/track-forward ("Artist — Track (Official Video)" pattern or the brief's convention).
- Description: track credits, generation credits where policy requires, timestamped section markers for the hero cut.
- Tags/hashtags: genre + mood + platform music tags. Vertical cut caption references the full video.

### 3. Cover frame
A visual-peak frame (usually final chorus) where the motif is legible. For the vertical cut, the cover must work as a feed thumbnail.

### 4. Rights + attribution check
Record the song source (generated: provider + license terms; supplied: rights-holder confirmation from the brief) in the publish log. Do not publish supplied-audio videos without the rights note.

### 5. Localization handoff (if declared)
Subtitled/dubbed variants (lyric translations, intro cards) → hand off to `localization-dub` with the master + caption files; record the handoff manifest.

### 6. Export + log
Export directory: hero + variants + covers + `metadata.json` per platform; `publish_log` records paths, rights note, and handoffs.

### Quality Gate
- [ ] Hero + all declared variants exported and spec-checked per platform.
- [ ] Vertical cut loops cleanly and carries its own metadata.
- [ ] Cover frames on visual peaks.
- [ ] Rights/attribution note recorded.

## Common Pitfalls

- Shipping only the hero and skipping the vertical cut — the discovery engine.
- A cover frame from a verse valley instead of a chorus peak.
- Missing rights documentation for supplied audio.
