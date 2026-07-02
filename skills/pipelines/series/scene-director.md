# Scene Director — Series Pipeline

## When To Use

Turn every episode's script beats into per-episode shot plans: framing, motion, b-roll intercuts, and overlay placement. This stage carries the **anti-slideshow hard gate per episode** — episodic talking-head content is the most slideshow-prone format in the catalog.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]`, arc style bible | Beats + visual system |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow scoring per episode |
| Tool | `frame_sampler` (optional) | Reference-frame checks |

## Operating Principles

- **Talking heads never hold static.** Intercut with motivated b-roll, insert shots, or reframes; a host on camera for >8s without a visual change is a gate failure waiting to happen.
- **The style bible is law.** Framing rules, lower-third positions, and transition vocabulary come from the arc — do not invent per episode.
- **Pattern interrupts are shots, not intentions.** The re-engagement beats marked at ~25%/~65% in the script must map to a concrete visual change (location/angle/graphic segment).

## Process

### 1. Map beats → shots per episode
For each beat: `information_role`, `shot_intent`, framing (per style bible), b-roll/insert plan, overlay notes, est duration. Podcast format: plan the two-persona coverage (singles, two-shot, reaction inserts) so dialogue cuts have somewhere to go.

### 2. Place overlays
Lower-thirds, chapter markers, quiz cards (learning), and end cards go where the arc planned them; mark which are the HyperFrames finishing pass at compose. Keep all persistent text inside platform safe zones for the target aspect.

### 3. Choreograph pattern interrupts
At each marked re-engagement beat: a visible change of shot grammar (new location, graphic segment, dramatic reframe) — not just a b-roll swap.

### 4. Score every episode
Run `score_slideshow_risk` per episode. Any `fail` → rework that episode's motion intents before submitting.

### Quality Gate
- [ ] Every shot in every episode has `information_role` + `shot_intent`.
- [ ] No talking-head hold >8s without a visual change.
- [ ] Style bible applied verbatim; overlays placed per arc plan.
- [ ] Pattern interrupts are concrete shots at ~25%/~65%.
- [ ] Slideshow verdict ≥ acceptable for every episode.

## Common Pitfalls

- Planning episode 1 carefully and templating the rest — the gate scores each episode.
- B-roll as wallpaper (no information_role) — it must prove or advance the beat.
- Quiz cards placed mid-explanation instead of after the concept lands.

## References

- Pattern interrupts for gradual-decline retention curves: https://prepublish.ai/guides/youtube-retention-guide
- Re-engagement beats at 25%/65%: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
