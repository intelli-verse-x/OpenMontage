# Idea Director — Talking-Head Pipeline

## Runtime Selection (MANDATORY — lock at idea)

The deliverable is a photorealistic presenter speaking with **audio-synced lip movement** and burned captions. That is produced by content-factory's **composite avatar renderer** (viseme/energy-driven mouth overlay + ffmpeg), not by an HTML/GSAP or Remotion render. **Lock `render_runtime = "composite"`** at this stage and record it in `decision_log` under `render_runtime_selection`.

There is no multi-runtime choice to present here. `video_compose` only dispatches `remotion`/`hyperframes`; the talking-head render is delegated to the content-factory `compose_from_artifacts` adapter. Note this constraint to the user rather than offering another runtime. (A GPU lip-sync backend — Wan2.2 S2V — is the higher-fidelity option when a GPU is available; the composite path is the local, no-GPU default.)

## When To Use

The deliverable is a short vertical (or chosen-aspect) explainer of one presenter speaking to camera. Decide the **inputs** in the brief:

| Input | Source | Pick when |
|-------|--------|-----------|
| **Presenter portrait** | A provided `portrait_path`, or generated front-facing head-and-shoulders portrait via `image_selector` | Always — the face is the subject |
| **Narration** | Authored in the script stage, synthesized via `tts_selector` in assets | Always |
| **Voice** | A `voice_id` (resolved/scored by `tts_selector`) | Pick a voice that matches the persona + emotion |

## Operating Principles

- One presenter, one topic — this is an explainer, not a feature tour.
- The face must read as a real person facing the camera, **mouth closed**, evenly lit (the renderer detects the mouth and overlays motion — a 3/4 or occluded mouth breaks lip-sync placement).
- Choose emotion/tone deliberately (`calm`, `confident`, `friendly`) — it feeds both voice selection and the portrait prompt.
- Optimize for legibility and a fast hook before style.

## Process

### 1. Define the Presenter + Topic
- Topic / single takeaway the explainer delivers.
- Presenter persona (e.g. "friendly product educator, 30s") — feeds the portrait prompt and voice choice.
- Target audience.

### 2. Choose the Aspect / Framing
| Aspect | Resolution | Use |
|--------|-----------|-----|
| `9:16` | 1080×1920 | Vertical autoplay default (Shorts/Reels/TikTok) |
| `1:1`  | 1080×1080 | Square feed |
| `16:9` | 1920×1080 | Landscape / web / webinar |

Front-facing, head-and-shoulders, centered — the mouth should land near the vertical center of the face for reliable lip-sync placement.

### 3. Choose Voice + Emotion
- Pick the emotion/tone; the script + voice should match it.
- A specific `voice_id` may be supplied; otherwise `tts_selector` scores and picks a voice at the assets stage. Record any explicit `voice_id` in `brief.metadata.voice_id`.

### 4. Set Target Duration
Duration is **derived from the narration**, not fixed. State an intended range (e.g. 30–60s for a topic explainer); the script director writes to it. Do not pad with dead air — the render length follows the audio.

### 5. Build the Brief
Schema fields carry the concise contract; richer production detail goes in `metadata`.

Recommended `metadata` keys:
- `aspect` (`9:16` | `1:1` | `16:9`)
- `presenter` (persona description for the portrait)
- `voice_id` (if explicitly chosen) / `emotion`
- `portrait_path` (if a presenter image is provided) or `portrait_prompt` override
- `topic`, `audience`, `target_duration_seconds`
- `brand` (accent color, name) — feeds the frame/caption styling + editable overlay
- `notes_for_script` (the single takeaway + tone)

### 6. Quality Gate
- [ ] Topic + presenter persona + audience stated.
- [ ] Aspect chosen; framing is front-facing head-and-shoulders.
- [ ] Voice + emotion chosen (or voice delegated to `tts_selector`).
- [ ] `render_runtime = "composite"` locked in `decision_log`.
- [ ] Target duration range stated (derived from narration, not padded).

## Common Pitfalls

- Specifying a 3/4 or stylized portrait whose mouth is hard to locate — lip-sync placement degrades.
- Treating duration as fixed and padding the narration to hit it.
- Trying to offer Remotion/HyperFrames runtimes — the lip-synced presenter is a composite render.
- A multi-topic brief; a talking head lands one idea well, not five.
