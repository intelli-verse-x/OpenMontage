# Idea Director — Playable Pipeline

## When To Use

First stage. Turn an app/game (and optionally its live site) into a **brief** for an interactive HTML5 playable ad: which core loop to demonstrate, which playable archetype to use, which networks to target, and where the store CTA points.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Pipeline | `pipeline_defs/playable.yaml` | `quality_gate` + stage contract |

## The One Question

**What single core-loop moment, played in under 10 seconds, makes someone want this app?** Everything else serves that. For a quiz/trivia/exam game (e.g. QuizVerse) the answer is almost always: *answer a question, feel smart, see your score, install to keep playing* — the `quiz_taste_test` archetype.

## Process

### 1. Identify the app + core loop
- App/game name, genre, and the **one** loop to demo. Resist showing the whole app — a playable proves one fun thing.

### 2. Pick the playable archetype
| Archetype | Best for | Interaction |
|-----------|----------|-------------|
| `quiz_taste_test` (default) | quiz / trivia / exam-prep / knowledge games | tap the right answer, see feedback + score |
| `flashcard_deck` | learning / language / study apps | tap to flip 3–5 cards (prompt → reveal), swipe/tap next |
| `level_sampler` | puzzle / casual | complete one mini-level |
| `tap_challenge` | reflex / arcade | beat a tiny timed challenge |

For QuizVerse-style apps, default to `quiz_taste_test`. For study/learning apps whose core loop is recall (not scoring), use `flashcard_deck` — the flip is the "aha" interaction. Flashcard decks carry a **flavor** (from content-factory's `playable_flashcard_deck`): `snackable` (surprising one-liners), `witty` (humor-forward), or `mini_lesson` (one concept taught across the deck) — record it in the brief; it drives the script's card voice.

### 3. Choose target networks + size budget
List the networks (AppLovin, ironSource, Unity, Meta, Google). Record the **strictest** size limit as the budget (Meta/Google ≈ 2 MB; AppLovin/ironSource ≈ 5 MB). The build must clear the strictest target you intend to ship to.

### 4. Capture store destinations
- `app_store_url` (iOS), `play_store_url` (Android). If the real store links aren't known yet, set a `fallback_url` (e.g. the product site) so the CTA is always live. Record all three; the build resolves iOS vs Android at runtime.

### 5. Brand source
- If a `website_url` is available, note it — the asset stage grounds the palette + icon from it. If not, the playable uses a clean unbranded fallback.

## Output — `brief` artifact

Must include:
- `app_name`, `genre`, `core_loop` (one sentence)
- `archetype` (default `quiz_taste_test`)
- `flavor` (flashcard_deck only: snackable | witty | mini_lesson)
- `num_questions` (default 3; keep it short — 2–4) or `num_cards` (flashcard: 3–5)
- `target_networks[]` + `size_budget_bytes`
- `store` `{ app_store_url, play_store_url, fallback_url }`
- `website_url` (or null)
- `decision_log` entry recording archetype + network + budget choices

## Success Criteria
- Schema-valid `brief`.
- Brief states the playable archetype, target networks, and store CTA destinations.

## Common Pitfalls
- Trying to demo the whole app instead of one core-loop moment.
- Forgetting the store CTA destination (leaves the build with a dead button).
- Targeting Meta/Google without budgeting for their 2 MB limit.
- Choosing quiz for a study app whose loop is recall — the flip, not the score, is the hook.

## References

- Size limits by network (5 MB hard cap across Google/Meta/TikTok/Unity/ironSource/AppLovin/Mintegral/Liftoff/Moloco): https://playableendcards.com/blog/playable-ad-size-limits-by-network
- Unity playable specifications (MRAID 3.0, single HTML): https://docs.unity.com/grow/acquire/creatives/playable/specifications
