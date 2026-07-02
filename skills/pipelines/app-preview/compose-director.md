# Compose Director — App-Preview Pipeline

## When To Use

Render the final preview and produce a **re-editable artifact**. This stage is the P1 swap: the HyperFrames composition is not a one-shot CLI output — it round-trips through the `@hyperframes/sdk` headless engine so an agent can hand a human a Studio URL and receive edits back (agent → Studio → agent).

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime`. It is locked to **`hyperframes`** for this pipeline. `video_compose.execute()` dispatches to `hyperframes_compose` when `render_runtime == "hyperframes"`; `hyperframes lint` + `validate` must both pass before render. A silent swap to `remotion`/`ffmpeg` is a CRITICAL governance violation — escalate per AGENT_GUIDE.md if the runtime is unavailable instead of substituting.

Pass `proposal_packet` to `video_compose.execute()` so the in-tool swap check can confirm the locked runtime matches `edit_decisions`.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | What to render |
| Tools | `video_compose` (dispatch), `hyperframes_compose` (runtime), `audio_mixer` (optional) | Rendering |
| Adapter | content-factory `HyperFramesAppPreviewPipeline.compose_from_artifacts` | Authoring + render + editable artifact |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check |

## The Content-Factory Adapter (thin compose seam)

OpenMontage owns the creative decisions; the actual composition + render is delegated to the content-factory adapter so this pipeline doesn't re-implement an 8k-line authoring engine. The adapter is a **thin compose seam** — it does not re-derive copy or re-plan scenes:

```python
# content-factory: pipelines/catalog/hyperframes_app_preview.py
pipeline = HyperFramesAppPreviewPipeline.init_from_config(
    "configs/pipelines/hyperframes_app_preview.yaml"
)
report = await pipeline.compose_from_artifacts(
    app_name=brief["app_name"],
    copy={                                  # from the script artifact
        "hook": script["hook"],
        "captions": script["captions"],     # one per screen, ordered
        "cta_headline": script["cta_headline"],
        "cta_sub": script["cta_sub"],
    },
    shots=edit_decisions["metadata"]["compose_adapter_inputs"]["framed_screens"],
    device_preset=edit_decisions["metadata"]["device_preset"],
    brand_context=edit_decisions["metadata"].get("brand"),
    render=True,
)
# report → render_report artifact (status, video_path, duration, …)
# report.editable / report.editable_artifact_dir / report.studio_url  ← P1
```

`video_compose`/`hyperframes_compose` is the in-tree path for fully-OM-native renders; the adapter is the reference path that reuses content-factory's authored GSAP composition and its `EditableArtifactStore`. Either way the render_report must carry the re-editable artifact fields below.

## Process

### 1. Pre-Render Slideshow Re-Check
Re-score the final scene plan with `score_slideshow_risk(..., render_runtime="hyperframes")`. If `fail`, do NOT render — send back to scene_plan. This catches drift introduced during asset/edit.

### 2. Render via the Locked Runtime
- Materialize the composition (phone-framed screens, motivated Ken-Burns, hook + CTA cards), `lint`, `validate`, then `render` at the device preset resolution + target fps.
- The composition opens with the hook card and closes with the CTA card by construction.

### 3. Register the Re-Editable Artifact (P1 — MANDATORY)
The render output must be promoted to an editable artifact (`EditableArtifactStore.register`), which writes:
- `editable.json` (manifest: source HTML, sdk_version, versions, s3_uri),
- a versioned snapshot of the composition HTML (reversible edits),
- a `studio_url` an operator can open to edit the composition.

A render without these is incomplete — it breaks the agent → Studio → agent round-trip that defines this pipeline.

### 4. Verify the Output
**File checks:**
- [ ] Output MP4 exists and is a valid container.
- [ ] Duration within store window (15–30s), ±5% of target.
- [ ] Resolution matches the device preset; fps matches target.

**Re-editable checks (P1):**
- [ ] `render_report` records `editable_artifact_dir` + `studio_url`.
- [ ] `editable.json` exists next to the composition HTML.

**Legibility checks:**
- [ ] Hook reads clearly muted at sampled frames.
- [ ] Captions don't collide with phone-frame edges.
- [ ] Ken-Burns motion is smooth; no jitter.

Record findings in `render_report.verification_notes` / `warnings` and the editable artifact fields in `render_report.metadata`.

## Common Pitfalls

- Silently swapping off `hyperframes` when the runtime isn't available — escalate instead.
- Rendering but skipping `EditableArtifactStore.register`, so there's no Studio round-trip.
- Re-deriving copy/scenes in the adapter instead of passing the OM artifacts through (the adapter is thin by design).
- Accepting a render whose duration drifted outside 15–30s.
