# Scene Director — Shorts Pipeline

## When To Use

Turn the script's beats into a shot-by-shot `scene_plan` for a 9:16 frame: framing, motion, on-screen text placement, and timing. This stage carries the **anti-slideshow hard gate**.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]` | Beats to visualize |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow scoring |
| Tool | `frame_sampler` (optional) | Reference-frame checks |

## Operating Principles

- **Every shot must move or change.** Static holds are what the slideshow gate exists to kill; camera push, subject action, text animation, or environment change — something earns each second.
- **Safe zones are layout law.** On 1080×1920: keep text/faces/logos out of the top ~150–200px (username/sound), right ~120px (engagement rail), bottom ~250–300px (caption bar + CTA). Design in the center band.
- **Vary the shot grammar.** Alternate shot sizes and compositions; a repeated template reads as a slideshow even with motion.

## Process

### 1. Map beats → shots
One shot per beat (standard: ≤4 shots, 4–8s each). For each shot record:
- `information_role` — what this shot proves/advances.
- `shot_intent` — why this framing/motion (push-in for emphasis, whip for energy, match-cut for the loop seam).
- Framing, subject action, text block + position (center band), est duration.

### 2. Place on-screen text
- Word-timed captions start at 0:00 with the first VO word.
- Hook text: large, high-contrast, center or upper-center band.
- Never place persistent text in the bottom 300px or right 120px.

### 3. Choreograph the loop seam
Design the final shot's last frame to hand off to shot 1's first frame (matching composition, motion vector, or color field).

### 4. Score the plan
Run `score_slideshow_risk(scenes, renderer_family, render_runtime)`. Verdict `fail` → rework motion intents before submitting. Verdict `revise` → strengthen the weakest shots.

### Quality Gate
- [ ] Every shot has `information_role` + `shot_intent`.
- [ ] Shot sizes/compositions vary; no repeated template.
- [ ] All text inside safe zones; captions start at first word.
- [ ] Durations sum to target ±10%; no shot >8s without cause.
- [ ] Slideshow verdict ≥ acceptable.

## Common Pitfalls

- "Motion" that is only a slow Ken-Burns on every shot — the gate scores intent, not just movement.
- Hook text placed in the top 200px where the platform username covers it.
- Designing at 16:9 and cropping — plan natively vertical.

## References

- TikTok safe zones (top 150–200px, right 120px, bottom 250–300px): https://zeely.ai/blog/tiktok-safe-zones/
- Cross-platform safe zones: https://kreatli.com/guides/safe-zone-guide
- Motion principles (timing/spacing, anticipation, follow-through): https://blog.vmgstudios.com/10-principles-motion-design
