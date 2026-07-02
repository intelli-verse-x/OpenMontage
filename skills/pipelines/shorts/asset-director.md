# Asset Director — Shorts Pipeline

## When To Use

Resolve every shot in the scene plan into a concrete asset: generated/stock clips or stills, voiceover, music bed, and caption files. All generation routes through selectors scored by `lib/scoring.py` — never a hardcoded provider.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]`, `state.artifacts["script"]` | Shots + copy |
| Tools | `video_selector` (required), `image_selector`, `tts_selector`, `music_gen`, `subtitle_gen` | Asset resolution |
| Scoring | `lib/scoring.py` | Provider routing + audit trail |

## Operating Principles

- **One asset per shot, native 9:16.** Prefer generating at 1080×1920 (or 900×1600 where the provider requires) over cropping 16:9 output.
- **Muted-first mix.** The short must fully work with no audio; VO and music are additive. Gain-stage music −18 to −14 LUFS under VO.
- **Audit trail is mandatory.** Every generated asset records `selected_provider` + `provider_score`.

## Process

### 1. Resolve visuals per shot
For each shot, decide generate vs stock vs supplied footage. Prompt the generator with the shot's `information_role` + `shot_intent` + subject action (motion in the prompt, not just a static description). Verify each clip actually contains the planned motion.

### 2. Voiceover
`tts_selector` with the script's VO lines; one consistent voice; pacing brisk (shorts VO reads ~10–15% faster than long-form). Export per-beat audio so the editor can tighten gaps.

### 3. Music + SFX
`music_gen` for a bed matching the archetype energy; must loop cleanly if the video loops. Optional SFX on the hook beat (a whoosh/impact under the first cut increases perceived energy).

### 4. Captions
`subtitle_gen` word-timed from the VO. Style: word-by-word or 2–3-word chunks, high-contrast, starting at the first word. Deliver as a data file (not burned) so compose controls placement inside safe zones.

### 5. Budget check
If spend > 90% of budget with shots unresolved, downgrade optional assets (SFX, alt takes) before core visuals; alert the EP.

### Quality Gate
- [ ] Every planned shot has a resolved 9:16 asset with real motion.
- [ ] VO complete, single voice, per-beat files.
- [ ] Music loops cleanly; gain-staged under VO.
- [ ] Word-timed caption file present, starts at 0:00.
- [ ] `selected_provider` + `provider_score` on every generated asset.

## Common Pitfalls

- Accepting a generated clip whose motion doesn't match the shot_intent (re-prompt, don't settle).
- Burning captions here — placement belongs to compose where safe zones are enforced.
- Music that fights the VO because it wasn't gain-staged.

## References

- Captions from the first word: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- Loop audio + video seams for replays: https://www.youtube.com/watch?v=gP76Sk_P6Ng
