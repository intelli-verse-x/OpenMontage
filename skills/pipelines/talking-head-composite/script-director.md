# Script Director — Talking-Head Pipeline

## When To Use

Turn the brief into the presenter's **spoken narration**, broken into ordered **sections** (beats). This script is what `tts_selector` voices, what the scene-director scores for motion, and what the content-factory compose adapter renders + captions.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Topic, persona, voice, emotion, duration |
| Playbook | Active style playbook | Tone constraints |

## Operating Principles

This is **spoken word**, not on-screen copy. It will be read aloud by a synthesized voice, so:

- write the way the presenter would *speak* — contractions, short sentences, natural rhythm,
- open on a **hook sentence** that earns the next 5 seconds,
- one idea per section so each maps to a single caption + motion beat,
- close on a concrete takeaway or CTA,
- no bullet fragments, no jargon walls, no list-reading.

## Process

### 1. Write the Hook (first sentence)
- The opening line states the stakes or the promise in one breath.
- It must work spoken aloud; the captioned version of it is the first thing on screen.
- Example: "Here's the problem with almost every quiz app: you cram, you score, and a week later it's all gone."

### 2. Break the Narration into Sections
- Each section is **one idea**, ~1–3 sentences, that the presenter delivers as a beat.
- Order them as a logical arc: hook → problem → idea → how it works → proof → takeaway/CTA.
- Each section's text must be **captionable** — the edit stage derives one caption (or a tight caption pair) per section, so keep each beat self-contained.
- Vary the rhythm across sections (a punchy one after a longer one) so the delivery — and the captions — don't feel monotone. This also helps the slideshow gate downstream.

### 3. Write the Close
- End on a single concrete takeaway or a clear CTA ("Start your first round today.").
- Avoid trailing filler — the render length follows the audio, so dead words become dead air.

### 4. Build the Script Artifact
Schema fields carry the narration + sections. Put extras in `metadata`:
- `sections` — ordered list, each `{ text, information_role_hint?, emphasis? }`
- `tone` (matches the brief's emotion)
- `full_narration` (the concatenated spoken text, for TTS)
- `localization_notes` (if a non-en locale was requested)

### 5. Quality Gate
- [ ] First sentence is a real hook that works spoken + muted-captioned.
- [ ] Narration is conversational spoken-word, not bullet copy.
- [ ] Broken into ordered sections, each a single captionable idea.
- [ ] Closes on a concrete takeaway / CTA.
- [ ] Rhythm varies across sections (anti-monotone).

## Common Pitfalls

- Writing on-screen marketing copy instead of spoken sentences — it sounds robotic when voiced.
- One giant paragraph with no sections — the edit stage can't derive caption beats or motion.
- A flat open with no hook; the first 2 seconds decide retention (a hook in the first 2s retains ~19% more viewers on shorts-style feeds).
- Trailing sentences that add length without adding meaning (dead air in the render).

## References

- Hook in first 2s → +19% retention: https://www.zebracat.ai/post/youtube-shorts-statistics
- Hook structures + captions from the first word: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
