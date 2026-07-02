# Compose Director — Talking-Head Pipeline

## When To Use

Render the final talking-head and produce a **re-editable artifact**. This stage is the P1 swap: the composite render is wrapped in a HyperFrames composition (the raw video as a base layer + an *editable* caption/brand overlay) that round-trips through the `@hyperframes/sdk` headless engine so an agent can hand a human a Studio URL and receive caption/brand edits back (agent → Studio → agent).

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime`. It is locked to **`composite`** for this pipeline. The render is delegated to the content-factory `compose_from_artifacts` adapter, which runs the composite avatar renderer (viseme/energy-driven mouth overlay + ffmpeg) — there is no GPU/weights/service requirement. `video_compose` only dispatches `remotion`/`hyperframes` and **cannot** render composite; do not route through it and do not silently swap to another runtime. If composite rendering is unavailable, escalate per AGENT_GUIDE.md instead of substituting.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | What to render |
| Adapter | content-factory `TalkingHeadPipeline.compose_from_artifacts` | Synthesis-aware compose + composite render + editable artifact |
| Optional tools | `audio_mixer`, `subtitle_gen` | Music/voice mix; separate caption asset (rarely needed) |
| Gate | `lib/slideshow_risk.py` | Pre-render re-check |

## The Content-Factory Adapter (thin compose seam)

OpenMontage owns the creative decisions; the actual synthesis-fallback + composite render + caption burn + editable-artifact registration is delegated to the content-factory adapter so this pipeline doesn't re-implement the avatar renderer. The adapter is a **thin compose seam** — it does not re-derive copy or re-plan beats. Pass the already-decided artifacts straight through:

```python
# content-factory: pipelines/catalog/hyperframes_talking_head.py
pipeline = TalkingHeadPipeline(
    working_dir=".working_dir/talking_head",
    brand_context=edit_decisions["metadata"]["compose_adapter_inputs"].get("brand_context"),
)
report = await pipeline.compose_from_artifacts(
    title=edit_decisions["metadata"]["compose_adapter_inputs"]["title"],
    script_text=edit_decisions["metadata"]["compose_adapter_inputs"].get("script_text"),
    sections=edit_decisions["metadata"]["compose_adapter_inputs"].get("sections"),
    portrait_path=asset_manifest["metadata"]["portrait"]["path"],   # already synthesized
    audio_path=asset_manifest["metadata"]["audio"]["path"],         # already synthesized
    voice_id=edit_decisions["metadata"]["compose_adapter_inputs"].get("voice_id"),
    emotion=edit_decisions["metadata"]["compose_adapter_inputs"].get("emotion", "calm"),
    aspect=edit_decisions["metadata"]["compose_adapter_inputs"].get("aspect", "9:16"),
    brand_context=edit_decisions["metadata"]["compose_adapter_inputs"].get("brand_context"),
    render=True,
)
# report → render_report artifact (status, video_path, duration, captions_burned, …)
# report["editable"] / report["editable_artifact_dir"] / report["studio_url"]  ← P1
```

Notes on the seam:
- Pass `portrait_path` + `audio_path` from the assets stage so the adapter **reuses** the scored TTS/portrait output instead of re-synthesizing. (The adapter *can* synthesize if they're omitted — it falls back to OpenAI TTS when the ElevenLabs key is invalid — but under OM, the assets stage already routed those through the selectors.)
- The adapter runs its own slideshow gate (`renderer_family="composite-talking-head"`, `render_runtime="composite"`) and **will not render** if the gate blocks — surface that as a send-back to scene_plan.
- The adapter burns captions (script-timed, or Whisper when present) and registers the editable artifact via `EditableArtifactStore`.

## Process

### 1. Pre-Render Slideshow Re-Check
Re-score the final scene plan with `score_slideshow_risk(sections, renderer_family="composite-talking-head", render_runtime="composite")`. If `fail`, do NOT render — send back to scene_plan. This catches drift introduced during asset/edit.

### 2. Render via the Adapter (composite runtime)
Call `compose_from_artifacts(...)` with the prepared inputs. The adapter: gates → composite-renders the lip-synced presenter → burns captions → authors the editable composition → registers the re-editable artifact.

### 3. Register the Re-Editable Artifact (P1 — MANDATORY)
The adapter promotes the output to an editable artifact (`EditableArtifactStore.register`), writing:
- `editable.json` (manifest: source HTML, sdk_version, versions, s3_uri),
- a versioned snapshot of the composition HTML (raw video base layer + editable caption/brand overlay),
- a `studio_url` an operator can open to edit captions/brand.

A render without these is incomplete — it breaks the agent → Studio → agent round-trip that defines this pipeline.

### 4. Verify the Output

**File checks:**
- [ ] Output MP4 exists and is a valid container.
- [ ] Duration ≈ narration length (±5%).
- [ ] Resolution matches the aspect preset; fps matches target.

**Lip-sync checks (the bug class this port fixed):**
- [ ] Sampled frames during speech show an **open** mouth; during silence, **closed** — i.e. it tracks the audio.
- [ ] The mouth overlay sits **on the presenter's mouth** (detected via face landmarks), not on the chest/neck.

**Caption checks:**
- [ ] Captions are burned, legible, and time-aligned to the narration.

**Re-editable checks (P1):**
- [ ] `render_report` records `editable_artifact_dir` + `studio_url`.
- [ ] `editable.json` exists next to the composition HTML.

Record findings in `render_report.verification_notes` / `warnings`, and `report["captions_burned"]`, `transcript_source`, `slideshow_verdict`, and the editable artifact fields in `render_report.metadata`.

## Common Pitfalls

- Routing through `video_compose` (it can't render composite) or silently swapping runtimes — escalate instead.
- Accepting a render whose lip movement is off the mouth or not synced to the audio.
- Rendering but skipping `EditableArtifactStore.register`, so there's no Studio round-trip.
- Re-synthesizing TTS/portrait in the adapter instead of passing the scored assets through (the adapter is thin by design).
- Captions that aren't time-aligned to the narration.
