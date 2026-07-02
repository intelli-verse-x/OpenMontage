# Script Director — Music-Video Pipeline

## When To Use

Write the **treatment**: a visual movement per song section that turns the brief's concept into a section-by-section plan the scene director can shoot. The treatment is the music video's script — there is no dialogue; structure and escalation are the writing.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Concept, motif, song structure |

## Operating Principles

- **Mirror the music's architecture.** Verses breathe, choruses peak, the bridge subverts, the outro resolves. The visual energy curve must trace the musical one.
- **Choruses repeat with escalation.** Same visual identity each chorus, bigger each time (chorus 1 establishes, chorus 2 intensifies, final chorus transforms).
- **The motif is the through-line.** It appears in every section, evolving — this is what makes the video one piece instead of vignettes.

## Process

### 1. Map the sections
From the brief's structure: intro / verse 1 / chorus 1 / verse 2 / chorus 2 / bridge / final chorus / outro (adapt to the actual track). Note each section's start/end time and energy level (1–5).

### 2. Write one visual movement per section
Each movement: setting, subject action, motif state, energy level, and the **transition idea** into the next section (the cut on the drop into chorus 1 is the video's biggest moment — write it explicitly).

### 3. Design the escalation ladder
For each chorus repeat, state what grows: scale (wider/more), speed (faster cuts planned), or strangeness (the world transforms). The final chorus must pay off the motif.

### 4. Opening 2 seconds
The intro movement must establish the visual world instantly — the first frames are the hook for feed-surfaced clips.

### 5. Build the script artifact
Ordered movements with `{section, time_range, energy, setting, action, motif_state, transition_out}`. Metadata: escalation ladder, lyric-video flag (if captions requested), vertical-cut section (which section becomes the 9:16 short — almost always the final chorus).

### Quality Gate
- [ ] Every song section has a movement; times sum to track length.
- [ ] Energy curve traces the music (verses < choruses; bridge distinct).
- [ ] Chorus escalation explicit; motif evolves and pays off.
- [ ] Drop transitions written as concrete moments.

## Common Pitfalls

- Uniform energy across sections — if everything peaks, nothing does.
- Choruses that look unrelated to each other (breaks the repeat-recognition payoff).
- Ignoring the bridge, which is the natural place for the video's surprise.

## References

- Sync visual moments to musical structure: https://www.reddit.com/r/premiere/comments/1nomnj0/whats_your_go_to_method_for_finding_the_rhythm/
