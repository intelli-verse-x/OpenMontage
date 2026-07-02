# Executive Producer — Talking-Head Pipeline

## When to Use

You are the **Executive Producer (EP)** for a presenter-led talking-head explainer. You orchestrate the pipeline serially — spawning each stage director, reviewing its artifact against the manifest's `review_focus` and `success_criteria`, and either passing it forward or sending it back for revision.

This pipeline is a **reference port** of content-factory's `hyperframes_talking_head` pipeline onto the OpenMontage template. The creative decisions (idea → script → scene_plan → edit) live here as director skills with provider scoring and the slideshow-risk gate; input synthesis (TTS narration + presenter portrait) and the composite render are delegated to the content-factory **compose adapter** (`TalkingHeadPipeline.compose_from_artifacts`), which produces a *re-editable* HyperFrames artifact (P1: editable caption + brand overlay over the rendered video).

## Why This Exists

Talking heads have one dominant failure mode: **a static portrait reading text at the viewer.** With no motion beyond the lip overlay, a long monologue reads as a slideshow of one frame and loses retention. The EP's job is to enforce, at the earliest possible stage, that:

- the narration is broken into **sections** with changing caption emphasis (motion comes from the captions + section cadence, not just the mouth), and
- every section beat has a stated `information_role` (what idea it lands) and a `shot_intent`/motion purpose.

Secondary failure modes the EP catches: a hook that takes too long to land, lip-sync that isn't actually on the mouth (the bug class this port fixed), captions that aren't synced to the audio, and silent provider swaps (TTS/image) that ignore scoring + budget.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Pipeline | `pipeline_defs/talking-head-composite.yaml` | Stage definitions, review focus, success criteria |
| Skills | All 7 director skills + `meta/reviewer` + `meta/checkpoint-protocol` | Stage execution + review |
| Scoring | `lib/scoring.py` | Provider routing for narration (`tts_selector`) + portrait (`image_selector`) |
| Gate | `lib/slideshow_risk.py` | Anti-static gate at scene_plan + compose (`renderer_family=composite-talking-head`) |
| Budget | `tools/cost_tracker.py` | Spend governance (default $0.50) |
| Adapter | content-factory `TalkingHeadPipeline.compose_from_artifacts` | Input synthesis + composite render + re-editable artifact |

## Cumulative State

```
EP_STATE:
  pipeline: talking-head-composite
  playbook: <clean-professional | flat-motion-graphics>
  aspect: 9:16            # 9:16 default; 16:9 / 1:1 supported
  presenter: null         # persona/identity for the portrait + voice
  voice_id: null          # resolved by tts_selector, may be overridden in brief
  emotion: calm
  target_duration_seconds: <auto from narration length>
  budget_total_usd: 0.50
  budget_spent_usd: 0.0

  # talking-head specific
  render_runtime: composite     # locked at idea; rendered by the CF avatar renderer
  section_count: 0
  slideshow_verdict: null       # strong | acceptable | revise | fail
  transcript_source: null       # whisper | script-timed

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
1. Load `pipeline_defs/talking-head-composite.yaml`.
2. Select the playbook (default `clean-professional`; `flat-motion-graphics` for energetic/brand-heavy explainers).
3. Set budget from `orchestration.budget_default_usd` ($0.50). Cost here is the TTS call + one portrait generation; the composite render is local/free. Budget governs the synthesized assets.
4. Initialize EP_STATE; lock `render_runtime = composite`.

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
  1. PROBE output: duration ≈ narration length, resolution == aspect preset, valid MP4.
  2. LIP-SYNC CHECK: sample frames during speech vs silence — the mouth opens/closes
     ON the presenter's mouth (not the chest), and tracks the audio.
  3. CAPTION CHECK: captions present, legible, and time-aligned to the narration.
  4. SLIDESHOW RE-CHECK: re-score the final scene plan; verdict must be ≥ acceptable.
  5. RE-EDITABLE CHECK (P1): render_report carries editable_artifact_dir + studio_url
     and editable.json exists — the agent can hand a Studio URL to a human and
     receive caption/brand edits back.
  6. BUDGET RECONCILIATION: spend ≤ budget; log per-stage.
  7. DECISION: all pass → APPROVE for publish; else send back to the responsible stage.
```

## EP-Specific Cross-Stage Checks

### After IDEA
- Topic, presenter persona, voice, emotion, and aspect chosen.
- `render_runtime` locked to `composite` in `decision_log` (no hyperframes/remotion/ffmpeg substitution — the deliverable is a lip-synced presenter).
- Target duration is derived from the planned narration, not padded.

### After SCRIPT
- Narration is spoken-word and conversational; opens on a hook sentence.
- Broken into ordered sections, each one idea, each captionable.
- Closes on a concrete takeaway or CTA.

### After SCENE_PLAN (HARD GATE)
- Every section beat has `information_role` AND a motion/`shot_intent` (caption emphasis change, B-roll cutaway, or framing shift).
- Caption cadence varies (not one repeated template).
- Run `score_slideshow_risk(sections, renderer_family="composite-talking-head", render_runtime="composite")`.
  - verdict `fail` → SEND_BACK to scene_plan (do not proceed).
  - verdict `revise` → require one revision pass adding motion/caption variety.
  - Store verdict in EP_STATE.slideshow_verdict.

### After ASSETS
- Narration audio present (synthesized via `tts_selector`) + presenter portrait present (resolved or via `image_selector`).
- Confirm `selected_provider` + `provider_score` recorded for each synthesized asset (scoring audit trail). No hardcoded TTS/image provider.
- Budget gate: if spent > 90% of budget and stages remain, alert + drop optional music.

### After EDIT
- Caption timeline aligned to narration sections; `render_runtime == "composite"`.
- `compose_adapter_inputs` assembled (title, narration/sections, portrait, brand).
- Duration matches narration; no dead air.

### After COMPOSE
- Render came from `compose_from_artifacts` (composite avatar renderer; NO silent runtime swap).
- Output exists + passes ffprobe; resolution == aspect preset; fps == target.
- Lip movement is on the mouth and audio-synced; captions legible.
- Slideshow re-check passes.
- render_report records `editable_artifact_dir` + `studio_url` (P1).

## Feedback Templates

### To Scene Director
```
EP FEEDBACK — Scene Plan Revision Required
Reason: slideshow-risk verdict={verdict} (avg={avg})
Affected sections: {section_ids}
Fix: add a concrete information_role + motion/shot_intent per section; vary caption emphasis; consider a B-roll cutaway; do not repeat one template.
```

### To Compose Director
```
EP FEEDBACK — Re-render Required
Reason: {lip_sync_off_mouth | not_audio_synced | runtime_swap | missing_editable_artifact | caption_unsynced}
Expected: composite render at {WxH}@{fps}, mouth-on-face audio-synced lip movement, burned captions, editable.json + studio_url present.
Actual: {what was produced}
```

## Quality Gates Summary

| Gate | After | Checks | Fail Action |
|------|-------|--------|-------------|
| G1 | idea | Presenter/voice/aspect, runtime lock (composite), duration | Revise idea |
| G2 | script | Hook, spoken-word narration, ordered sections, CTA | Revise script |
| G3 | scene_plan | information_role + motion intent, **slideshow ≥ acceptable** | Revise / send-back |
| G4 | assets | Narration + portrait present, scoring audit trail, budget | Revise assets |
| G5 | edit | Caption timing, runtime lock, compose_adapter_inputs | Revise edit |
| G6 | compose | runtime lock, ffprobe, lip-sync on mouth, slideshow re-check, editable artifact | Revise / send-back |
| G7 | publish | Placement spec, metadata, editable reference preserved | Revise publish |

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max total send-backs | 2 |
| Max total budget | $0.50 (configurable) |
| Max total wall-time | 12 minutes |

## Common Pitfalls

- **Static talking head** — the defining risk. Never accept a scene plan whose sections lack motion/caption variety.
- **Lip-sync off the mouth** — the overlay must sit on the presenter's mouth and track the audio (closed in silence, open during speech), not paint a blob on the chest.
- **Unsynced captions** — captions must be time-aligned to the narration (script-timed or Whisper), not a static block.
- **Silent provider swap** — narration must route through `tts_selector` and the portrait through `image_selector`; no hardcoded provider.
- **Forgetting the re-editable artifact** — a render without `editable.json` + `studio_url` breaks the agent → Studio → agent round-trip that defines P1.
