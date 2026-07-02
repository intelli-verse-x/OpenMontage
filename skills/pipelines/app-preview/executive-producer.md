# Executive Producer — App-Preview Pipeline

## When to Use

You are the **Executive Producer (EP)** for an App Store / Play Store preview video. You orchestrate the pipeline serially — spawning each stage director, reviewing its artifact against the manifest's `review_focus` and `success_criteria`, and either passing it forward or sending it back for revision.

This pipeline is the **reference port** of content-factory's `hyperframes_app_preview` pipeline onto the OpenMontage template. The creative decisions (idea → script → scene_plan → edit) live here as director skills with provider scoring and the slideshow-risk gate; the actual composition + render is delegated to the content-factory **compose adapter** (`HyperFramesAppPreviewPipeline.compose_from_artifacts`) which produces a *re-editable* HyperFrames artifact (P1).

## Why This Exists

App previews have one dominant failure mode: **they degrade into a screenshot slideshow.** A muted autoplay sequence of static screens with a caption per screen scores `fail` on the slideshow-risk gate and converts poorly. The EP's job is to enforce, at the earliest possible stage, that every screen scene has:

- a stated `information_role` (what this screen proves), and
- a `shot_intent` (why the camera/Ken-Burns move exists).

Secondary failure modes the EP catches: hook not legible muted in the first 5s, duration outside the store's 15–30s window, CTA that doesn't drive the install, and silent provider swaps that ignore budget.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Pipeline | `pipeline_defs/app-preview.yaml` | Stage definitions, review focus, success criteria |
| Skills | All 7 director skills + `meta/reviewer` + `meta/checkpoint-protocol` | Stage execution + review |
| Scoring | `lib/scoring.py` | Provider routing for the assets stage |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow gate at scene_plan + compose |
| Budget | `tools/cost_tracker.py` | Spend governance (default $0.50) |
| Adapter | content-factory `HyperFramesAppPreviewPipeline.compose_from_artifacts` | Compose + render + re-editable artifact |

## Cumulative State

```
EP_STATE:
  pipeline: app-preview
  playbook: <flat-motion-graphics | clean-professional>
  store: <app_store | play_store>
  device_preset: <iphone_6.9 | iphone_6.7 | ipad_13 | google_phone | landscape_hd>
  target_duration_seconds: <15..30>
  budget_total_usd: 0.50
  budget_spent_usd: 0.0

  # app-preview specific
  mode: null              # "screenshots" | "brief"
  screenshot_count: 0
  slideshow_verdict: null # strong | acceptable | revise | fail
  render_runtime: hyperframes  # locked at idea, dispatched by video_compose

  artifacts:
    idea: null          # → brief, decision_log
    script: null        # → script
    scene_plan: null    # → scene_plan
    assets: null        # → asset_manifest
    edit: null          # → edit_decisions
    compose: null       # → render_report, final_review
    publish: null       # → publish_log

  revision_counts: {}
  issues_log: []
```

## Execution Protocol

### Phase 0: Initialize
1. Load `pipeline_defs/app-preview.yaml`.
2. Select the playbook (default `flat-motion-graphics`; `clean-professional` for utility/finance apps).
3. Set budget from `orchestration.budget_default_usd` ($0.50). App previews are near-zero cost — screenshots are resolved, not generated, and HyperFrames render is local/free. Budget exists to govern any optional generated backgrounds/music.
4. Initialize EP_STATE.

### Phase 1: Execute Stages Serially
Order: `idea → script → scene_plan → assets → edit → compose → publish`

```
EXECUTE_STAGE(stage_name):
  1. PREPARE — load the director skill, inject EP_STATE + prior feedback.
  2. SPAWN DIRECTOR — produces its artifact.
  3. REVIEW — schema validation + manifest review_focus + success_criteria + EP cross-stage checks.
  4. GATE — PASS → store + continue; REVISE → re-run with feedback (max 3);
            SEND_BACK(target) → re-execute from target forward (max 2 total).
```

### Phase 2: Final QA
```
FINAL_QA:
  1. PROBE output: duration in [15,30]s, resolution == device preset, valid MP4.
  2. SLIDESHOW RE-CHECK: re-score the final scene plan; verdict must be ≥ acceptable.
  3. HOOK CHECK: hook legible with sound off in first 5s.
  4. RE-EDITABLE CHECK (P1): render_report carries editable_artifact_dir + studio_url
     and editable.json exists — the agent can hand a Studio URL to a human and
     receive edits back.
  5. BUDGET RECONCILIATION: spend ≤ budget; log per-stage.
  6. DECISION: all pass → APPROVE for publish; else send back to the responsible stage.
```

## EP-Specific Cross-Stage Checks

### After IDEA
- Store + device preset + target duration chosen; duration ∈ [15, 30]s.
- `render_runtime` locked to `hyperframes` in `decision_log`.
- Input mode decided: `screenshots` (urls/bundle_id/dir) vs `brief` (teaser cards). Record in EP_STATE.mode.

### After SCRIPT
- Hook is 3–6 words, reads clearly muted.
- Exactly one benefit caption per planned screen; no jargon/hashtags/emojis.
- CTA headline (≤4 words) + supporting line present.

### After SCENE_PLAN (HARD GATE)
- Every screen scene has `information_role` AND `shot_intent`.
- Shot sizes/layouts vary (not one repeated template).
- Run `score_slideshow_risk(scenes, renderer_family=<playbook family>, render_runtime="hyperframes")`.
  - verdict `fail` → SEND_BACK to scene_plan (do not proceed).
  - verdict `revise` → require one revision pass adding motion intent / varying shots.
  - Store verdict in EP_STATE.slideshow_verdict.

### After ASSETS
- One framed screen asset per planned scene (or teaser cards in brief mode).
- If `image_selector` generated any asset (background, teaser art): confirm `selected_provider` + `provider_score` recorded (scoring audit trail). No hardcoded provider.
- Budget gate: if spent > 90% of budget and stages remain, alert + trim optional assets.

### After EDIT
- Ordered timeline: hook card → screens → CTA card.
- Transitions motivated (cross-fade/whip), not random.
- Total duration still within [15, 30]s.

### After COMPOSE
- `edit_decisions.render_runtime == "hyperframes"` (video_compose dispatched to hyperframes_compose; NO silent runtime swap).
- Output exists + passes ffprobe; resolution == preset; fps == target.
- Slideshow re-check passes.
- render_report records the re-editable artifact dir + `studio_url` (P1).

## Feedback Templates

### To Scene Director
```
EP FEEDBACK — Scene Plan Revision Required
Reason: slideshow-risk verdict={verdict} (avg={avg})
Affected scenes: {scene_ids}
Fix: add a concrete information_role + motivated shot_intent per screen; vary shot sizes; do not repeat one template.
```

### To Compose Director
```
EP FEEDBACK — Re-render Required
Reason: {legibility | runtime_swap | missing_editable_artifact}
Expected: hyperframes render at {WxH}@{fps}, editable.json + studio_url present.
Actual: {what was produced}
```

## Quality Gates Summary

| Gate | After | Checks | Fail Action |
|------|-------|--------|-------------|
| G1 | idea | Store/preset/duration, runtime lock, input mode | Revise idea |
| G2 | script | Hook legibility, one caption/screen, CTA | Revise script |
| G3 | scene_plan | information_role + shot_intent, **slideshow ≥ acceptable** | Revise / send-back |
| G4 | assets | One framed asset/scene, scoring audit trail, budget | Revise assets |
| G5 | edit | hook→screens→CTA order, duration window | Revise edit |
| G6 | compose | runtime lock, ffprobe, slideshow re-check, editable artifact | Revise / send-back |
| G7 | publish | Store metadata, spec compliance | Revise publish |

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max total send-backs | 2 |
| Max total budget | $0.50 (configurable) |
| Max total wall-time | 10 minutes |

## Common Pitfalls

- **Slideshow drift** — the defining risk. Never accept a scene plan where screens lack a motion purpose.
- **Hook only works with sound** — App Store autoplay is muted; the first 5s must read silently.
- **Duration outside 15–30s** — Apple/Google reject these; the EP must enforce the window.
- **Silent runtime swap** — compose must stay on `hyperframes`; escalate if unavailable, don't substitute.
- **Forgetting the re-editable artifact** — a render without `editable.json` + `studio_url` breaks the agent → Studio → agent round-trip that defines P1.
