# Script Director — App-Preview Pipeline

## When To Use

Turn the brief into the preview's copy: a muted-legible **hook**, **one benefit caption per screen**, and a **CTA** (headline + supporting line). This is the script artifact the scene-director and the content-factory compose adapter consume.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | App, value prop, audience, screen count |
| Playbook | Active style playbook | Tone + typography constraints |

## Operating Principles

App Store previews autoplay **muted**. Every word must earn its place on screen:

- the hook must communicate the core value in 3–6 words, silently,
- one benefit line per screen, max ~6 words, no jargon,
- no emojis, no hashtags, no exclamation spam,
- the CTA must name the action, not describe the app.

## Process

### 1. Write the Hook (muted-first)
- 3–6 words, the single strongest reason to care.
- Must read clearly with no sound in the first ~5 seconds.
- If the user supplied a `hook_text`, use it verbatim.
- Examples: "Learn anything, 5 minutes a day." / "Your money, finally organized." / "Win every quiz night."

### 2. Write One Caption Per Screen
- Exactly `screen_count` captions (from the brief / scene count).
- Each names a concrete benefit tied to what that screen shows, ≤ 6 words.
- Vary the angle across captions (speed, simplicity, progress, social, value) so screens don't feel repetitive — this also helps the slideshow gate downstream.
- Bad: "Home screen". Good: "See your progress at a glance".

### 3. Write the CTA
- `cta_headline`: ≤ 4 words, action-led (e.g. "Get {app}", "Start free today").
- `cta_sub`: one supporting line, ≤ 6 words (e.g. "Download free — no signup").

### 4. Build the Script Artifact
Schema fields carry hook / captions / cta. Put extras in `metadata`:
- `tone`
- `caption_angles` (the benefit angle each caption takes)
- `localization_notes` (if a non-en locale was requested)

### 5. Quality Gate
- [ ] Hook is 3–6 words and reads muted.
- [ ] Exactly one caption per planned screen.
- [ ] No jargon, emojis, or hashtags.
- [ ] CTA headline (≤4 words) + supporting line present.
- [ ] Caption angles vary (anti-repetition).

## Common Pitfalls

- A hook that only makes sense with voiceover — autoplay is silent.
- Captions that label the UI ("Settings page") instead of selling a benefit.
- Identical caption shape on every screen, which reinforces the slideshow feel.
- A vague CTA ("Try our app") instead of a concrete action.
