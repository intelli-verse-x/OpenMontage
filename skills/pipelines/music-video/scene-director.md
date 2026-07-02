# Scene Director — Music-Video Pipeline

## When To Use

Break the treatment's movements into shots: framing, subject action, motion, and beat-landing plan. This stage carries the **anti-slideshow hard gate** and sets up the beat-sync edit by planning which actions land on beats.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]` | Movements + energy + times |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow scoring |

## Operating Principles

- **Plan actions, not just images.** The edit syncs *actions* to beats — a door slam, a head turn, a light flare. Every shot needs a describable action moment the editor can place on a beat.
- **Cut density follows energy.** Verses: fewer, longer shots (≥ the 2.0s min interval). Choruses: more, shorter shots. Plan shot counts per section accordingly.
- **The world stays coherent.** Palette, lighting logic, and the motif from the treatment appear in every shot's description.

## Process

### 1. Shots per section
From each movement's energy: low energy → 2–4 shots; peak chorus → 6–10 shots. For each shot: `information_role` (what it adds to the world/story), `shot_intent` (why this framing/motion), subject action + its **impact moment** (the frame that should land on a beat), framing, est duration.

### 2. Plan beat landings
Mark which shots carry an on-beat impact and roughly where (shot start, mid-action, or shot end). Chorus entries get the biggest impact shot. Not every shot needs one — contrast is rhythm.

### 3. Recurring-character coverage
For declared characters: specify their appearance per shot referencing the canonical description; vary framing (not the character) across appearances.

### 4. Vertical-cut awareness
For the section flagged as the 9:16 cut: compose those shots center-weighted so a vertical crop keeps the subject and any text inside safe zones.

### 5. Score the plan
Run `score_slideshow_risk`. `fail` → rework motion/action intent before submitting.

### Quality Gate
- [ ] Every shot has `information_role` + `shot_intent` + an action with an impact moment.
- [ ] Shot counts per section follow the energy curve.
- [ ] Beat-landing plan marked; chorus entries have peak shots.
- [ ] Vertical-cut shots are center-weighted.
- [ ] Slideshow verdict ≥ acceptable.

## Common Pitfalls

- Shots described as pictures ("neon alley") with no action — nothing to sync to a beat.
- Peak-energy shot grammar in verses, leaving the chorus nowhere to go.
- Character appearance re-described differently per shot (invites generation drift).

## References

- Actions on beats, cut density variation: https://www.reddit.com/r/premiere/comments/1nomnj0/whats_your_go_to_method_for_finding_the_rhythm/
- Motion principles (timing, anticipation, follow-through): https://blog.vmgstudios.com/10-principles-motion-design
