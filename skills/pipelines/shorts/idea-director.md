# Idea Director — Shorts Pipeline

## When To Use

Turn a topic, trend, or request into a shorts `brief`: one sharp premise with a hook, a payoff, and a CTA, sized for a 15–60s vertical video. You also lock the **archetype** and, for multi-part formats, the part structure.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Skill | `core/research.md` | Trend/topic research before ideation |
| Playbook | `flat-motion-graphics` or `clean-professional` | Style envelope |

## Operating Principles

- **The premise IS the hook.** If the idea can't be stated as a scroll-stopping first line, it isn't a shorts idea yet.
- **Completion over length.** A 45s short at 70% completion beats a 15s short at 40% completion — pick the duration the payoff needs, not the shortest possible.
- **One promise per short.** Multi-point ideas become multi-part series, not crowded singles.

## Process

### 1. Research the angle
Use `core/research.md`: what is currently working on the target platform for this topic; what's the audience's open question. Record sources in `decision_log`.

### 2. Choose the archetype
- `standard` — single viral short (default).
- `quiz_mystery` — 3-part series: Part 1 poses the mystery, Part 2 drops clues, Part 3 reveals. Each part must end on an explicit open loop. Declare `parts: 3` and per-part cliffhangers in the brief.
- `teaching` — ~60s lesson short: one teachable, surprising claim with a demonstration.
- `event_promo` / `event_recap` — templated beat structures (hook → prize/stakes → category → CTA; highlights → winner → next-event CTA).

### 3. Draft 3 hook options, pick 1
Use the five proven hook structures — bold claim, curiosity gap, micro-story opening, visual shock, direct question — and write one hook line per structure that fits, then choose the strongest. The hook must be visual-first (works muted).

### 4. Set duration + platform
Duration ∈ [15, 60]s; justify it by the payoff. Platform (shorts/reels/tiktok) drives safe zones, fps, and metadata downstream.

### 5. Region variants (optional)
If the request targets multiple regions (e.g. India + USA), declare variants: peak post times, hashtag sets, caption style, and any localized references. These flow to publish only — one master edit, N metadata variants.

### 6. Build the brief
`brief` fields: premise, hook line, payoff, CTA intent, archetype, parts (+ per-part cliffhangers), platform, duration, audience, region_variants, references.

### Quality Gate
- [ ] Hook line works as the literal first frame text, muted.
- [ ] Payoff is concrete (what the viewer gets by staying).
- [ ] Duration justified by payoff, within 15–60s.
- [ ] Archetype + parts declared; cliffhangers per part for multi-part.

## Common Pitfalls

- Ideas that are topics, not premises ("about productivity" vs "you're taking breaks at the wrong time").
- Cramming three points into one short instead of declaring a series.
- Choosing 15s reflexively when the payoff needs 40s to land.

## References

- Five hook structures; captions from the first word: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- Completion rate beats length: https://www.digitalapplied.com/blog/short-form-video-strategy-shorts-tiktok-reels-2026
- Hook in first 2s → +19% retention: https://www.zebracat.ai/post/youtube-shorts-statistics
