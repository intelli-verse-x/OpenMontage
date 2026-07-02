# Executive Producer — Playable Pipeline

## When to Use

You are the **Executive Producer (EP)** for an interactive HTML5 **playable ad** — a tappable mini-game that demonstrates an app/game's core loop in seconds and closes on a store CTA. You orchestrate the pipeline serially — spawning each stage director, reviewing its artifact against the manifest's `review_focus` and `success_criteria`, and either passing it forward or sending it back.

This pipeline is the port of content-factory's `playable_quiz_ad` pipeline onto the OpenMontage template. The creative decisions (idea → script → design → assets) live here as director skills with provider scoring; the actual build is delegated to the content-factory **build adapter** (`PlayableQuizAdPipeline`) which emits a *single self-contained* `index.html` + build manifest + zip and validates it.

## Why This Exists

A playable ad has one dominant failure mode: **it isn't actually playable.** A non-interactive auto-playing animation with a CTA slapped on the end is rejected by networks and converts poorly. The EP enforces, from the earliest stage, that:

- the user **does something** (taps an answer) and gets **immediate feedback**, and
- the build is **one self-contained file** (no external asset fetches) under the **size budget**, with a **working store CTA**.

Secondary failure modes the EP catches: external asset requests that break offline playback, a CTA that doesn't open the store, oversized builds that networks reject, and silent provider swaps that ignore budget.

This is NOT a video pipeline. There is no timeline/edit stage, and the **slideshow-risk gate does not apply** — it is replaced by the **`playable_compliance`** gate (see the manifest `quality_gate`).

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Pipeline | `pipeline_defs/playable.yaml` | Stage definitions, review focus, success criteria, `quality_gate` |
| Skills | 6 director skills + `meta/reviewer` + `meta/checkpoint-protocol` | Stage execution + review |
| Scoring | `lib/scoring.py` | Provider routing for question writing + brand/icon generation |
| Gate | `services.playable.ad_playable.validate_playable` | Network-compliance + interactivity gate |
| Budget | `tools/cost_tracker.py` | Spend governance (default $0.25) |
| Adapter | content-factory `pipelines.catalog.playable_quiz_ad.PlayableQuizAdPipeline` | Build + validate + package |

## Cumulative State

```
EP_STATE:
  pipeline: playable
  playbook: <flat-motion-graphics | clean-professional>
  app_name: <e.g. QuizVerse>
  genre: <quiz | trivia | puzzle | ...>
  archetype: quiz_taste_test       # the playable mini-game type
  website_url: <url | null>        # for brand grounding
  target_networks: [applovin, ironsource, unity, meta, google]
  size_budget_bytes: 2097152       # 2 MB preferred; 5 MB hard ceiling
  store:
    app_store_url: null
    play_store_url: null
    fallback_url: null
  budget_total_usd: 0.25
  budget_spent_usd: 0.0

  compliance_verdict: null         # pass | fail (playable_compliance gate)
  brand_grounded: false
  questions_source: null           # llm | fallback

  artifacts:
    idea: null          # → brief, decision_log
    script: null        # → script (questions + end-card copy)
    design: null        # → scene_plan (states + interaction)
    assets: null        # → asset_manifest (palette + icon)
    build: null         # → render_report, final_review
    publish: null       # → publish_log

  revision_counts: {}
  issues_log: []
```

## Execution Protocol

### Phase 0: Initialize
1. Load `pipeline_defs/playable.yaml`.
2. Select the playbook (default `flat-motion-graphics`; `clean-professional` for utility/finance apps).
3. Set budget from `orchestration.budget_default_usd` ($0.25). Playables are near-zero cost — the build is pure local front-end; the only spend is optional LLM question writing and optional generated icon/background.
4. Resolve the size budget from the strictest target network (Meta/Google ≈ 2 MB; AppLovin/ironSource ≈ 5 MB).
5. Initialize EP_STATE.

### Phase 1: Execute Stages Serially
Order: `idea → script → design → assets → build → publish`

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
  1. OPEN the built index.html in a headless browser (Playwright). Confirm the
     quiz screen renders and tapping an answer advances to the end-card CTA.
  2. COMPLIANCE: confirm validate_playable verdict == pass (all required_checks true).
  3. STORE CTA: confirm the CTA resolves a store/fallback URL and is wired through
     mraid.open() → clickTag → window.open.
  4. SIZE: index.html ≤ size budget for every target network.
  5. BUDGET RECONCILIATION: spend ≤ budget; log per-stage.
  6. DECISION: all pass → APPROVE for publish; else send back to the responsible stage.
```

## EP-Specific Cross-Stage Checks

### After IDEA
- App name + genre + the single core loop to demonstrate are chosen.
- Playable archetype set (default `quiz_taste_test`). Target networks + their size limits recorded.
- Store destinations captured (App Store / Play Store URLs) or a fallback URL set in EP_STATE.store.

### After SCRIPT
- Interaction is obvious: a first-time user can win within ~10 seconds.
- N quiz questions, each with 4 short options and exactly one correct; difficulty mixes easy/medium; on-genre.
- End-card copy present: headline (≤4 words ideal), blurb, CTA button label.
- If questions were LLM-authored: `selected_provider` + `provider_score` recorded (scoring audit trail). No hardcoded provider.

### After DESIGN
- Portrait, mobile-first; tap targets large and one-handed reachable.
- Explicit state flow: quiz → feedback → end-card. No passive auto-play, no dead ends.
- The plan can satisfy the `playable_compliance` intent checks (interactive, viewport, has_cta).

### After ASSETS
- If a website URL exists: brand grounded (accent palette + icon). Icon embedded as a data URI and downscaled to stay within budget.
- Any generated asset (icon/background) routes via `image_selector` → `lib/scoring.py`; `selected_provider` + `provider_score` recorded.
- No asset introduces a runtime external fetch (everything inlineable).

### After BUILD (HARD GATE)
- The build delegated to the content-factory adapter — copy/design were passed through, not re-derived.
- Output is ONE self-contained `index.html` + build manifest + zip.
- Run `validate_playable(build)`; verdict MUST be `pass`. Store in EP_STATE.compliance_verdict.
  - `fail` → SEND_BACK to the stage that owns the failing check:
    - `interactive`/`has_cta` → design; `no_external_assets`/`size_within_hard_limit` → assets; `single_file`/`mraid_aware`/`viewport_meta` → build.

## Feedback Templates

### To Build Director
```
EP FEEDBACK — Rebuild Required
Reason: playable_compliance verdict=fail
Failing checks: {checks}
Fix: {single self-contained file | inline all assets | wire MRAID store CTA | trim to size budget}
```

### To Design Director
```
EP FEEDBACK — Design Revision Required
Reason: {passive_autoplay | no_clear_cta | unreachable_state}
Fix: make the core loop tap-driven with immediate feedback; ensure quiz → feedback → end-card CTA is reachable with no dead ends.
```

## Quality Gates Summary

| Gate | After | Checks | Fail Action |
|------|-------|--------|-------------|
| G1 | idea | Archetype, networks + size limits, store CTA destinations | Revise idea |
| G2 | script | Interaction legibility, fair on-genre questions, scoring audit trail | Revise script |
| G3 | design | Tap-driven loop, immediate feedback, reachable states | Revise design |
| G4 | assets | Brand grounding, inlineable assets, scoring audit trail, budget | Revise assets |
| G5 | build | **playable_compliance == pass**, single file, MRAID CTA, size | Revise / send-back |
| G6 | publish | Per-network package, store URLs verified, preview screenshots | Revise publish |

## Execution Limits

| Limit | Value |
|-------|-------|
| Max revisions per stage | 3 |
| Max total send-backs | 2 |
| Max total budget | $0.25 (configurable) |
| Max total wall-time | 8 minutes |

## Common Pitfalls

- **Not actually playable** — the defining risk. Never accept a design that auto-plays without genuine user interaction.
- **External asset requests** — a playable that fetches a font/image at runtime breaks offline playback and fails review. Everything must be inlined.
- **Oversized build** — Meta/Google reject >2 MB; keep the icon downscaled and the file lean.
- **Dead CTA** — the store button must open the correct destination per platform via MRAID with fallbacks.
- **Silent provider swap** — question writing / icon generation must route through scoring; escalate if a provider is unavailable rather than substituting.
