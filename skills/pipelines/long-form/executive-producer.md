# Executive Producer — Long-Form Pipeline

## When to Use

You are the **Executive Producer (EP)** for a long-form video (10–60 minutes): documentary, educational, explainer, interview-style, or deep-dive. You orchestrate serially with a dedicated `chapters` planning stage between idea and script, and you enforce **retention architecture** — the chapter plan is a retention plan, not a table of contents.

This pipeline is the port of content-factory's `long_form_video` pipeline (with the generated `documentary` pipeline's narrative craft). It is distinct from `documentary-montage`, which assembles retrieval-first montages from an existing library.

## Why This Exists

Long-form retention is architectural. The benchmarks: videos under 5 minutes hold 65–75% average retention, 10–15 minutes hold 40–50%, and 15+ minutes hold 35–45% — and the single largest drop in nearly every video happens in the **first 30 seconds**. The EP enforces three retention invariants:

1. **Cold open with the key insight** — never a channel intro (this alone is worth +15–20pp retention past 30s).
2. **Re-engagement beats at ~25% and ~65%** — planned pattern interrupts, verified against the FINAL runtime at edit.
3. **Chapter cliffs** — every chapter ends pulling forward.

## Content Types (locked at idea, from the manifest)

| Type | Target | Chapters | Pacing |
|------|--------|----------|--------|
| documentary | 30 min | 5 | measured |
| educational | 20 min | 4 | steady |
| explainer | 15 min | 3 | dynamic |
| interview | 45 min | 6 | natural |
| deep_dive | 40 min | 6 | deliberate |

## Cumulative State

```
EP_STATE:
  pipeline: long-form
  content_type: null
  thesis: null              # the one-sentence question/claim the video answers
  chapter_count: 0
  target_minutes: 0
  narrator_voice_id: null   # locked at assets after test-line approval
  budget_total_usd: 5.00
  render_runtime: null      # locked at edit
  artifacts: {idea, chapters, script, scene_plan, assets, edit, compose, publish}
  revision_counts: {}
```

## Execution Protocol

Order: `idea → chapters → script → scene_plan → assets → edit → compose → publish`. Standard gate loop (PASS / REVISE max 3 / SEND_BACK max 2 total).

### Cross-Stage Checks

**After IDEA** — content type + matched duration/chapters; thesis is ONE sentence; audience + retention expectation stated.

**After CHAPTERS** — arc escalates to the thesis payoff; no redundant chapters; cold-open plan leads with the key insight; re-engagement beats marked near 25%/65%; every chapter ends on a cliff.

**After SCRIPT** — first 30s = hook + stake, zero throat-clearing; pattern interrupts written as concrete moments; the multi-LLM reviewer panel's notes addressed (run `meta/reviewer` with at least two distinct models when available; record disagreements + resolutions in the artifact).

**After SCENE_PLAN (HARD GATE)** — every scene has `information_role` + `shot_intent`; b-roll is evidential; visual grammar shifts at chapter boundaries. `score_slideshow_risk` per chapter; any `fail` → SEND_BACK.

**After ASSETS** — one narrator voice, test-line approved before batch; stock-first b-roll for real-world subjects; music ~15% under narration; audit trail complete.

**After EDIT** — cold open intact; branding ≤3s and after the hook; re-engagement beats verified against FINAL runtime; no segment sags >90s without change; duration ±10% of target.

**After COMPOSE** — 1920×1080/24fps (or override); loudness normalized; chapter cards consistent; first-30s frame-sample passes; slideshow re-check per chapter.

**After PUBLISH** — chapter timestamps from the final cut; thumbnail/title honest to the thesis; shorts-extraction candidates listed.

## Final QA

1. PROBE: duration ±10% of target, spec-correct, valid file.
2. FIRST-30s CHECK: frame-sample + listen; hook and stake present, no intro.
3. RETENTION-BEAT CHECK: re-engagement moments exist at ~25%/~65% of actual runtime.
4. CHAPTER CHECK: boundaries match the published timestamps; each ends forward-pulling.
5. BUDGET RECONCILIATION.

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max total send-backs | 2 |
| Max total budget | $5.00 |
| Max total wall-time | 45 minutes |

## Common Pitfalls

- Accepting a chapter plan that's a topic outline with no retention architecture.
- A "quick channel intro" before the hook — the first-30s drop is unforgiving.
- Verifying beat placement against planned durations instead of the final cut.
- Comparing this video's retention % against short-video baselines (use length-matched benchmarks).

## References

- Retention benchmarks by length; 25%/65% re-engagement beats: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
- First-30s drop; >40% = weak hook; lead with key insight: https://prepublish.ai/guides/youtube-retention-guide
