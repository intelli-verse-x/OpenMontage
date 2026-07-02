# Edit Director — Shorts Pipeline

## When To Use

Assemble the timeline: order shots, set cut points, place captions/text timing, and lock the render runtime. The edit is where stickiness is won — cut cadence, hook timing, and the loop seam are decided here.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `asset_manifest` | What to cut |
| Skill | `skills/core/hyperframes.md` | Runtime decision matrix |
| Skill | `skills/meta/bespoke-composition.md` | Atelier-mode bar for hero work |

## Runtime Routing (MANDATORY)

Choose and lock `render_runtime` in `edit_decisions`, per the decision matrix in `skills/core/hyperframes.md`:

- **Remotion** — data-driven caption systems, React-component text effects, programmatic variations (region variants of one master).
- **HyperFrames** — design-led kinetic type, GSAP-choreographed hook cards, bespoke motion language.
- **cloud adapter** (content-factory ViralShorts compose seam) — when the shot assets are cloud-generated clips and the composition is assembly + captions.

Per AGENT_GUIDE, present both Remotion and HyperFrames options at the checkpoint; never silently substitute. **For hero deliverables, atelier mode (hand-authored composition per `skills/meta/bespoke-composition.md`) must be explicitly considered and the decision recorded.**

## Operating Principles

- **Hook first, always.** The hook card/shot occupies 0–2s; nothing precedes it (no logos, no fade-ins).
- **Cut when the information lands.** Standard cadence ~1 cut per 2–4s for talking-topic shorts, faster (1–2s) for montage energy; but never cut on a schedule — cut on information.
- **Completion is the metric.** A trimmed 38s edit that holds beats a padded 55s edit; cut anything the payoff doesn't need.
- **The loop seam is an edit decision.** Place the final cut so the last frame hands off to the first.

## Process

### 1. Assemble hook → shots → CTA
Order per script. Trim each clip to its information: start each shot at the action, not before it.

### 2. Time the captions
Word-timed from 0:00. Keep caption blocks ≤3 words for pace; sync emphasis words to cuts/beats.

### 3. Transitions
Hard cuts by default. Motivated whips/match-cuts only where the scene plan states intent. No dissolves in shorts (they read slow).

### 4. Verify duration + loop
Total ∈ [15, 60]s and matches the brief ±10%. Check first/last frame handoff.

### 5. Lock runtime + record edit_decisions
Include `render_runtime`, per-shot in/out points, caption timing map, music sync points, loop seam note, and `metadata.atelier_considered: true|false` with rationale.

### Quality Gate
- [ ] Hook occupies 0–2s with no preamble.
- [ ] Every cut is motivated; no shot outlasts its information.
- [ ] Captions word-timed from first word.
- [ ] Loop seam works (frame match or re-hook).
- [ ] `render_runtime` locked with rationale; atelier considered for hero work.

## Common Pitfalls

- A 0.5s logo sting or fade-in before the hook — instant swipe.
- Even-length shots regardless of content ("4 seconds each") — cut on information.
- Padding to 60s for "watch time"; completion rate matters more than length.

## References

- Completion rate beats length; replay weighting: https://www.digitalapplied.com/blog/short-form-video-strategy-shorts-tiktok-reels-2026
- VVSA 70–90% target band: https://medium.com/@antoinelacombled/cracking-the-youtube-shorts-algorithm-a-study-of-3-3-billion-views-4711fdf7931b
- Loop construction: https://www.youtube.com/watch?v=gP76Sk_P6Ng
