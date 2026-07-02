# Idea Director — Music-Video Pipeline

## When To Use

Turn a song (or a request for one) into a music-video `brief`: the song source, one coherent visual concept, recurring characters if any, and platform targets.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Skill | `core/research.md` | Genre/visual-trend research |
| Playbook | `cinematic` or `flat-motion-graphics` | Style envelope |

## Operating Principles

- **One world, not a mood board.** The concept must be statable in one sentence ("a neon-lit night drive that gets more surreal each chorus"). If it needs "and also…", it's two concepts.
- **The song dictates everything.** Genre, tempo, and structure constrain the visual energy — listen (or spec the generated track) before ideating visuals.
- **Continuity is declared, not discovered.** If a character/subject recurs, name them now so assets can enforce canonical appearance.

## Process

### 1. Resolve the song source
- `supplied`: ingest the audio; note genre, BPM feel, structure (verse/chorus map), runtime.
- `generated`: spec the track for `music_gen` — genre, mood, tempo, structure, runtime, and (optionally) lyric themes. The generated track must be approved before the edit stage.

### 2. Research the visual space
`core/research.md`: current music-video visual trends for this genre; reference videos. Record in `decision_log`.

### 3. State the visual concept
One sentence world + palette + one recurring motif that can escalate (an object, gesture, or location that transforms across sections).

### 4. Declare recurring characters
If the video features a performer/character: name, look description or reference image, and appearances. This flips `preserve_character_consistency` downstream.

### 5. Set platform targets
Primary aspect (16:9 hero on YouTube is the default) + declared variants (9:16 chorus cut for shorts is the usual second target).

### 6. Build the brief
Fields: song_source (+ audio path or generation spec), genre/mood/structure, visual concept, motif, recurring_characters, aspect_targets, duration (track length), references.

### Quality Gate
- [ ] Concept fits in one sentence and names a motif that can escalate.
- [ ] Song structure known (or specced) section by section.
- [ ] Characters declared with reference material where continuity matters.
- [ ] Aspect targets explicit.

## Common Pitfalls

- Ideating visuals before hearing/spec'ing the track — energy mismatch is unfixable later.
- A concept that's a genre ("cyberpunk") instead of a world with a motif.
- Forgetting the vertical chorus cut, the highest-leverage distribution asset.
