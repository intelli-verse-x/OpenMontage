# Script Director — Shorts Pipeline

## When To Use

Turn the brief into a beat-per-shot script: hook copy, ordered shot beats with voiceover + on-screen text, and a CTA. Sound-off legibility is the primary constraint; the voiceover is reinforcement, not the carrier.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Premise, hook, archetype, duration |
| Playbook | Active style playbook | Tone + typography constraints |

## Operating Principles

- **The hook owns 0–2s.** The promise must be on screen (text + visual) by the 2-second mark; a sharp retention drop at 3s means the hook failed.
- **Captions from the very first word.** Never delay captions "for style" — the majority of feed viewing starts muted.
- **No shot outlasts its information.** Each beat carries exactly one idea; when the idea lands, cut.
- **Design the loop.** The last line/frame should hand off to the first (question ↔ answer, motion match, or hard restart that re-hooks).

## Process

### 1. Write the hook beat
- One line, ≤8 words on screen, using the structure chosen at idea (bold claim / curiosity gap / micro-story / visual shock / direct question).
- Pair it with a visual instruction ("smash cut to the broken result", "hands enter frame with X").

### 2. Write the body beats
- `standard`: ≤4 shots of 4–8s each. Each beat = VO line (≤2 sentences) + on-screen text (≤6 words) + visual.
- `teaching`: claim → demonstration → why-it-works → recap; quality bar: would a screenwriter score this ≥8.5/10 for specificity and surprise? If not, rewrite.
- `quiz_mystery`: per part — setup beats + an explicit cliffhanger line as the final beat ("Part 2 shows the clue everyone misses").
- `event_promo`/`event_recap`: follow the beat template from the brief (hook → prize → category → CTA / highlights → winner → next-event).

### 3. Write the CTA beat
Concrete and platform-appropriate: "Follow for part 2" (multi-part), "Comment your answer", "Link in bio". Never a generic "like and subscribe" line.

### 4. Design the loop seam
State in `metadata.loop_design` how the end returns to the start (e.g. final frame = first frame composition; closing question answered by the opening line on replay).

### 5. Build the script artifact
Fields: hook, ordered beats (vo / on_screen_text / visual / est_seconds), cta. Metadata: loop_design, caption_style (word-timed), per-part scripts for multi-part.

### Quality Gate
- [ ] Promise on screen by 2s, legible muted.
- [ ] Beat count and per-beat duration sum to the brief's duration ±10%.
- [ ] Every beat has one idea; zero filler lines ("so basically", "let me explain").
- [ ] CTA is a single concrete action.
- [ ] Loop seam described.

## Common Pitfalls

- Opening with context ("Hey guys, today we're…") — the number-one retention killer.
- On-screen text that paraphrases the VO instead of compressing it.
- A cliffhanger that's vague ("more soon") instead of specific ("Part 2: the clue everyone misses").

## References

- Hook in first 2s → +19% retention; 3s diagnostic: https://www.zebracat.ai/post/youtube-shorts-statistics , https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- Captions from the first word: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- ~35% drop off before the end of sub-60s videos — front-load payoff: https://animoto.com/blog/video-marketing/why-first-3-seconds-matter
- Loop design for replays: https://www.youtube.com/watch?v=gP76Sk_P6Ng
