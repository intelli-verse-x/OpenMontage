# Build Director — Playable Pipeline

## When To Use

Fifth stage. Assemble the playable and **enforce the `playable_compliance` gate**. This is the build seam: OpenMontage owns the creative artifacts (script + scene_plan + asset_manifest); the actual authoring of the self-contained `index.html` is delegated to the content-factory **build adapter** so this pipeline doesn't re-implement an HTML/CSS/JS engine. The adapter is **thin** — it does not re-derive copy, design, or brand.

This is the analogue of a video pipeline's compose stage, but the runtime is **not** `video_compose`/HyperFrames/Remotion — a playable is interactive HTML5, so there is no slideshow-risk re-check and no re-editable video artifact. The gate here is `validate_playable`.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior | `script`, `scene_plan`, `asset_manifest` | what to build |
| Adapter | content-factory `pipelines.catalog.playable_quiz_ad.PlayableQuizAdPipeline` | build + validate + package |
| Service | `services.playable.ad_playable` (`build_playable`, `validate_playable`) | builder + gate |
| Gate | `validate_playable` | network-compliance + interactivity |

## The Content-Factory Adapter (thin build seam)

```python
# content-factory: pipelines/catalog/playable_quiz_ad.py
from pipelines.catalog.playable_quiz_ad import PlayableQuizAdPipeline

pipe = PlayableQuizAdPipeline(chat_model=chat_model_or_none)
report = pipe(
    app_name=brief["app_name"],
    website_url=brief.get("website_url"),
    domain_hint=brief.get("genre", "quiz / trivia"),
    num_questions=len(script["questions"]),
    app_store_url=brief["store"]["app_store_url"] or "",
    play_store_url=brief["store"]["play_store_url"] or "",
    cta_button=script["cta_button"],
    ground_from_site=bool(brief.get("website_url")),
)
# report.index_path / report.manifest_path / report.zip_path
# report.compliant / report.checks / report.notes / report.size_bytes
```

Notes:
- The adapter re-grounds brand + (optionally) re-authors questions only because it is also runnable standalone. **When called from OM, pass the approved artifacts through** — do not let it invent new copy. If the adapter regenerates, reconcile its output against `script`/`asset_manifest` and prefer the OM artifacts; flag any drift as a reviewer finding.
- The builder lives in `services.playable.ad_playable.build_playable`; the gate in `validate_playable`. Either can be called directly for a fully-OM-native build.

## Process

### 1. Build
Call the adapter (or `build_playable(spec, out_dir)` directly). Output is exactly:
- `index.html` — one self-contained file (inline CSS/JS, icon as data URI, only `mraid.js` external),
- `playable_manifest.json` — build manifest (format `ivx_playable_ad_v1`, size, sha256, store, networks),
- `<build_id>.zip` — the network upload package.

### 2. Run the Compliance Gate (MANDATORY)
`validate_playable(build)` must return `compliant == true` with every required check:

| Check | Means |
|-------|-------|
| `single_file` | one `index.html` exists |
| `no_external_assets` | only `mraid.js` may be external; no other http(s) asset refs |
| `mraid_aware` | store taps route via `mraid.open()` with fallbacks |
| `has_cta` | a working store CTA exists |
| `interactive` | genuine tap-driven core loop present |
| `viewport_meta` | mobile viewport declared |
| `size_within_hard_limit` | ≤ 5 MB (and ideally ≤ 2 MB for Meta/Google) |

If any required check is `false`, do NOT report success — fix or send back per the EP's gate routing.

### 3. Smoke-Test the Flow
Open `index.html` headless (Playwright), confirm the quiz screen renders, tap through the answers, and confirm the end-card CTA appears. Capture two screenshots (quiz + end-card) for the publish stage / human review.

### 4. Verify Output
- [ ] `index.html` exists and opens; quiz → end-card flow reachable.
- [ ] Compliance verdict == pass (all required checks true).
- [ ] CTA resolves a store/fallback URL (iOS vs Android) via mraid → clickTag → window.open.
- [ ] `size_bytes` ≤ budget for every target network; note in `warnings` if above the 2 MB soft limit.

## Output — `render_report` artifact

Must include:
- `index_path`, `manifest_path`, `zip_path`
- `compliant` (bool) + `checks` (map) + `notes[]`
- `size_bytes`, `sha256`, `num_questions`
- `brand_grounded`, `accent_color`, `icon_used`, `questions_source`
- `screenshots[]` (quiz + end-card) for review
- `final_review` summary

## Common Pitfalls
- Reporting success when a required compliance check is `false`.
- Letting the adapter re-author copy that diverges from the approved `script` (the seam is thin — pass artifacts through).
- Shipping with an un-inlined asset (fails `no_external_assets`).
- Skipping the headless smoke-test, so a build that renders blank or has a dead CTA slips through.
