# Idea Director — App-Preview Pipeline

## Runtime Selection (MANDATORY — lock at idea)

App previews are HTML/CSS/GSAP motion graphics, not screen captures. **Lock `render_runtime = "hyperframes"`** at this stage and record it in `decision_log` under `render_runtime_selection`. The compose stage's `video_compose` dispatches to `hyperframes_compose` based on this field; a silent swap to another runtime is a governance violation.

There is no multi-runtime choice to present here: the deliverable is a vibe-coded HyperFrames composition (phone-framed screens, Ken-Burns motion, hook + CTA cards) that renders to a *re-editable* artifact. Note this constraint to the user rather than offering Remotion/ffmpeg.

## When To Use

The deliverable is a short (15–30s), autoplay-muted-friendly App Store / Play Store preview that opens on a hook and closes on a CTA. Decide the **input mode** in the brief:

| Mode | Source material | Pick when |
|------|-----------------|-----------|
| **`screenshots`** | `screenshot_urls`, a `bundle_id` (resolves from the enriched catalog), or a `screenshot_dir` | You have real app screens — each becomes a phone-framed scene with a motivated Ken-Burns push + a benefit caption |
| **`brief`** | App description / brief only | No screens available — fall back to branded gradient teaser cards (text-led) |

**Decision question:** *"Do I have real app screens to show?"* If yes → `screenshots` (always preferred — it converts far better and de-risks the slideshow gate). If no → `brief`.

**Record the mode in `brief.metadata.input_mode`.** The asset-director reads it to choose between resolving/framing screenshots vs preparing teaser cards.

## Operating Principles

- One app, one core value proposition — do not try to show every feature.
- The hook must land **muted** in the first 5 seconds.
- Prefer real screens over teaser cards; screens are the proof.
- Optimize for store-spec compliance and legibility before style.

## Process

### 1. Identify the App + Store
- App name, category, and target store (App Store vs Play Store).
- Resolve assets if a `bundle_id` is given (the adapter reads the enriched catalog). Otherwise collect `screenshot_urls` / `screenshot_dir`.

### 2. Choose the Device Preset
Pick the preset that matches the store + orientation. Portrait autoplay is the App Store default.

| Preset | Resolution | Use |
|--------|-----------|-----|
| `iphone_6.9` | 1080×1920 | App Store portrait default |
| `iphone_6.7` / `iphone_6.5` | 886×1920 | iPhone portrait |
| `ipad_13` | 1200×1600 | iPad |
| `google_phone` | 1080×1920 | Play Store phone |
| `landscape_hd` | 1920×1080 | Landscape / web |

### 3. Set Target Duration (store window)
Stay inside **15–30s** (Apple's hard window; Play Store is similar). Reserve a hook (~3.2s) and a CTA (~4s) out of the budget; the rest is split across screen scenes. Default `target_duration = 24s`. If the input only yields enough material for < 15s, plan more screens or teaser cards — do not ship a sub-15s preview.

### 4. State the Value Proposition + Audience
The brief must answer: who is this for, what single outcome does the app deliver, and what proof (which screens) the preview will show.

### 5. Build the Brief
Schema fields carry the concise contract; richer production detail goes in `metadata`.

Recommended `metadata` keys:
- `input_mode` (`screenshots` | `brief`)
- `store` (`app_store` | `play_store`)
- `device_preset`
- `bundle_id` / `screenshot_source`
- `target_duration_seconds`
- `value_proposition`
- `audience`
- `brand` (accent color, name) — feeds the composition's gradient + CTA styling
- `notes_for_scene_planner` (which screens prove which benefit)

### 6. Quality Gate
- [ ] Store + device preset chosen; preset matches orientation.
- [ ] `target_duration_seconds` ∈ [15, 30].
- [ ] `render_runtime = "hyperframes"` locked in `decision_log`.
- [ ] Input mode decided and recorded.
- [ ] Single clear value proposition + audience stated.

## Common Pitfalls

- Choosing `brief` (teaser cards) when screens exist — text cards are slideshow-prone and convert worse.
- Planning a preview that lands outside the 15–30s window.
- Writing a feature-list brief instead of a single value proposition.
- Forgetting to lock the runtime, leaving the compose stage to guess.
