# Edit Director — App-Preview Pipeline

## When To Use

Turn the scene plan + assets into a concrete, schema-valid `edit_decisions` timeline: ordered scenes (hook → screens → CTA), per-scene durations within the store window, motivated transitions, and the locked render runtime.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]`, `state.artifacts["assets"]`, `state.artifacts["script"]` | Order, assets, copy |
| Playbook | Active style playbook | Transition + pacing defaults |

## Process

### 1. Lock the Runtime
Set `edit_decisions.render_runtime = "hyperframes"` (inherited from the idea stage). `video_compose` reads this to dispatch to `hyperframes_compose`. Do not change it.

### 2. Order the Timeline
Mandatory shape: **hook card → screen scenes (in caption order) → CTA card**. The hook always opens; the CTA always closes.

### 3. Budget the Durations (store window)
- Total must land in **[15, 30]s**.
- Reserve hook (~3.2s) + CTA (~4s); split the remainder across screen scenes (≈ 2.5–4s each).
- If the math yields < 15s, send back to scene_plan for more screens rather than padding.
- Record `target_duration` and per-scene durations in `cuts[]` / `metadata.scene_durations`.

### 4. Motivated Transitions Only
- Cross-fade between screens; a single whip is acceptable into the CTA.
- No random/decorative transitions — they add motion the scene plan didn't ask for and can re-trigger slideshow concerns.
- Keep the transition duration short (~0.4–0.5s).

### 4b. Choose the Poster-Frame Candidate
Apple defaults the poster frame to the **5-second mark** — plan the timeline so whatever is on screen at ~5s works as a static thumbnail (typically the first screen scene with its benefit caption fully visible, not mid-transition). Record `metadata.poster_frame_time_s` for publish to set deliberately.

### 5. Keep the Schema Clean
Use `cuts[]` for scene segments + durations and `transitions` for the cross-fades. Put app-preview specifics in `metadata`:
- `device_preset`, `width`, `height`, `fps`
- `scene_durations`
- `brand` (accent color)
- `compose_adapter_inputs` — the copy + ordered framed-screen paths the content-factory `compose_from_artifacts` adapter expects

### 6. Quality Gate
- [ ] `render_runtime == "hyperframes"`.
- [ ] Order is hook → screens → CTA.
- [ ] Total duration ∈ [15, 30]s.
- [ ] Every transition is motivated; none decorative.
- [ ] Poster-frame candidate at ~5s is a clean, caption-visible frame; `poster_frame_time_s` recorded.
- [ ] `metadata` carries everything the compose adapter needs (preset, fps, ordered screens, copy, brand).

## Common Pitfalls

- Dropping the hook or CTA, or letting a screen open the preview.
- A timeline that totals < 15s or > 30s.
- Cinematic transitions the format doesn't need.
- A transition landing exactly at the 5s poster-frame mark, making the default thumbnail a blur.
- Forgetting to pass the ordered framed-screen paths + copy into `metadata`, leaving the compose adapter to re-derive them.

## References

- Apple App Preview specifications (15–30s, poster frame default 5s): https://developer.apple.com/help/app-store-connect/reference/app-information/app-preview-specifications/
- App preview creation guidance (muted autoplay, first 5s): https://splitmetrics.com/blog/create-app-preview-video-app-store-ios/
