# Publish Director — Long-Form Pipeline

## When To Use

Package the long-form video with chaptered metadata, an honest thumbnail/title pair, and the shorts-extraction plan that turns retention bumps into discovery assets.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/publish_log.schema.json` | Artifact validation |
| Prior artifacts | `render_report`, `final_review`, `brief`, `edit_decisions.metadata.chapter_marks` | Output + structure |

## Process

### 1. Chapter timestamps
Generate the description's chapter list from the FINAL cut's `chapter_marks` (never the plan). Chapter titles are curiosity-forward, not taxonomy ("The Records Don't Match" beats "Chapter 3: Analysis").

### 2. Title + thumbnail
- Title: the thesis as tension, ≤60 chars, front-loaded. Honest — clickbait debt shows up as a first-30s cliff in the retention curve.
- Thumbnail: one focal subject + ≤3 words; must pair with (not repeat) the title.

### 3. Description + metadata
First 2 lines restate the hook (they show before the fold). Then chapters, sources/citations (from the script's source map — documentary credibility), credits, tags.

### 4. Shorts-extraction plan
List 3–5 clip candidates for the `shorts` pipeline: the interrupt moments and any chapter-opening re-hooks (retention *bumps* make the best shorts). For each: in/out timestamps, the hook line, and the link-back strategy. Record as a handoff manifest — extraction runs as separate `shorts` pipeline work.

### 5. Accessibility + captions
Attach the chaptered SRT from assets; verify caption timing against the final cut.

### 6. Export + log
Export directory: video + thumbnail + `metadata.json` (chapters, description, tags) + SRT + shorts-handoff manifest. `publish_log` records paths and the extraction plan.

### Quality Gate
- [ ] Chapters from the final cut; titles curiosity-forward.
- [ ] Title/thumbnail honest to the thesis and non-duplicative of each other.
- [ ] Sources/citations in the description.
- [ ] Shorts-extraction manifest with timestamps + hooks.
- [ ] SRT verified against the final cut.

## Common Pitfalls

- Chapter timestamps copied from the plan and drifting off the final cut.
- An over-promising thumbnail that buys clicks and pays in retention.
- Skipping the shorts plan — the bumps are the long-form's built-in marketing.

## References

- Retention bumps → clip extraction; curve reading: https://prepublish.ai/guides/youtube-retention-guide
- Watch-time signal / benchmarks: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
