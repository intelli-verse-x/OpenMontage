# Executive Producer — Series Pipeline

## When to Use

You are the **Executive Producer (EP)** for an episodic series (learning curriculum, TV-style drama, weekly recap, or podcast-dialogue series). You orchestrate the pipeline serially with one extra planning stage — `arc` — between idea and script, and you enforce **cross-episode consistency** everywhere the single-video pipelines don't have to.

This pipeline is the port of content-factory's `LearningSeriesPipeline` / `TVSeriesPipeline` / `PodcastSeriesPipeline` onto the OpenMontage template.

## Why This Exists

Series fail differently than single videos: the per-episode craft can be fine while the series dies of redundant episodes, drifting style, or broken continuity. The EP owns three series-level invariants:

1. **Escalating value** — every episode has a distinct objective; no filler episodes.
2. **Style bible discipline** — palette/typography/host treatment is defined once at arc and reused verbatim.
3. **Continuity** — recaps, teasers, and callbacks reference real content from adjacent episodes.

Per-episode, the standard retention physics still apply: the steepest drop is in the first 30s of each episode, so every episode leads with its key insight, not a series intro.

## Formats (locked at idea)

| Format | Source | Distinctives |
|--------|--------|--------------|
| `learning` | learning_series | curriculum arc; pedagogy pacing (assessment/recap episodes); learning checkpoint per episode |
| `drama` | tv_series / short_movie_series | narrative arc; cliffhangers; character continuity |
| `recap` | weekly formats | recurring segment template; timely hooks |
| `podcast` | podcast_series | host/guest dialogue; persona consistency; chapterized episodes |

## Cumulative State

```
EP_STATE:
  pipeline: series
  format: null            # learning | drama | recap | podcast
  episode_count: 0
  per_episode_duration_s: 0
  style_bible: null       # locked at arc; hash-checked at compose
  locales: []             # declared target locales → publish hands off to localization-dub
  budget_total_usd: 3.00
  render_runtime: null    # locked at edit
  artifacts: {idea, arc, script, scene_plan, assets, edit, compose, publish}
  per_episode_status: {}
  revision_counts: {}
```

## Execution Protocol

Order: `idea → arc → script → scene_plan → assets → edit → compose → publish`. Standard gate loop (PASS / REVISE max 3 / SEND_BACK max 2 total).

### Cross-Stage Checks

**After IDEA** — format, episode count, per-episode duration, recurring hosts/personas locked. `podcast` format must declare host/guest personas and their dialogue dynamic.

**After ARC** — one entry per episode, each with a distinct objective; style bible complete (palette, type, host treatment, lower-thirds); `learning` format applies pedagogy pacing (recap/assessment episodes at the declared ratio, e.g. every 4th episode).

**After SCRIPT** — every episode opens on its own hook (key insight first, never a series intro); continuity callbacks reference real adjacent-episode content; per-episode CTA/learning checkpoint present.

**After SCENE_PLAN (HARD GATE)** — anti-slideshow per episode: talking-head/dialogue segments intercut with motivated b-roll; run `score_slideshow_risk` per episode; any `fail` → SEND_BACK.

**After ASSETS** — one narration voice (or host/guest pair) consistent across ALL episodes; style-bible consistency on visuals; scoring audit trail on every generated asset.

**After EDIT** — every episode follows intro → body → recap/teaser; re-engagement beats planted near the 25% and 65% marks of each episode; `render_runtime` locked.

**After COMPOSE** — per-episode ffprobe + slideshow re-check; style consistency spot-check across episodes (sample one frame per episode, compare against style bible); HyperFrames finishing pass (chapter markers, quiz cards, end cards) applied where the arc planned it.

**After PUBLISH** — playlist/series metadata, thumbnails from one template, release cadence recorded; localization plan present when locales declared.

## Final QA

1. Per-episode: duration ±10% of target, valid container, loudness in spec.
2. Cross-episode: same voice, same style bible, no continuity contradictions.
3. First-30s check per episode: hook present, no cold series intro.
4. Budget reconciliation across all episodes.

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max total send-backs | 2 |
| Max total budget | $3.00 (scale with episode count) |
| Max total wall-time | 30 minutes |

## Common Pitfalls

- Approving a great pilot and letting episodes 3+ drift off the style bible.
- Episode intros that recap the whole series — the first 30s belong to this episode's hook.
- Pedagogy pacing skipped in learning format (viewers churn without recap/assessment beats).
- Letting each episode pick its own voice/provider — consistency is the product.

## References

- First-30s drop dominates; lead with the key insight: https://prepublish.ai/guides/youtube-retention-guide
- Retention benchmarks by length; re-engagement beats at 25%/65%: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
