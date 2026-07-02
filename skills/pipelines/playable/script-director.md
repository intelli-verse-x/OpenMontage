# Script Director — Playable Pipeline

## When To Use

Second stage. Write the **interaction content**: the quiz questions (or flashcards) a player taps through and the end-card copy that drives the install. The deliverable is the `script` artifact.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior | `state.artifacts["idea"]["brief"]` | app, genre, archetype, num_questions |
| Scoring | `lib/scoring.py` | Route the question-writing LLM (no hardcoded provider) |
| Tool | `text_director` (optional) | LLM authoring; falls back to a deterministic set |

## Provider Routing (when using an LLM)

Question writing is the only LLM call in this pipeline. If you use one, **route it through `lib/scoring.py`** like any other generation and record `selected_provider` + `provider_score` in the artifact. If no LLM provider is configured, use the deterministic fallback question bank — a run must never fail for lack of an LLM. (The content-factory adapter implements exactly this: LLM → deterministic exam-prep/trivia fallback.)

## Writing Great Playable Questions

The questions ARE the gameplay. Bad questions kill conversion. Rules:

- **Win in seconds.** A first-time player should answer the first question correctly and feel smart. Lead easy, then nudge to medium.
- **Short stems, short options.** 4 options, each a few words. No "all of the above".
- **On-genre.** For QuizVerse: SAT/ACT math, vocabulary, AP science, geography, history, pop trivia. Mix domains so it feels like the real app's breadth.
- **Exactly one correct answer**, unambiguous. Avoid trick questions in a 3-question taste-test.
- **Fair distractors.** Plausible but clearly wrong on reflection — that "oh, of course" beat is the dopamine.

### Example (deterministic fallback flavor)
```
1. SAT Math: If 3x + 6 = 21, what is x?      [3, 5, 7, 9]  → 5
2. Vocabulary: 'Ephemeral' most nearly means [Lasting, Fleeting, Massive, Hidden] → Fleeting
3. AP Biology: the 'powerhouse of the cell'  [Nucleus, Ribosome, Mitochondria, Golgi] → Mitochondria
```

## Writing Great Flashcards (flashcard_deck archetype)

Cards are `{ front_prompt, back_reveal, tag }`, 3–5 per deck. The flip is the payoff — the back must be worth the tap:

- **Front = open loop.** A question, a surprising claim, or an incomplete phrase ("The word 'quiz' was invented as a…").
- **Back = payoff in one breath.** ≤2 short lines; the reveal should be surprising, funny, or genuinely useful per the brief's `flavor`:
  - `snackable` — surprising one-liners; each card standalone.
  - `witty` — humor-forward reveals; keep the joke on the back, not the front.
  - `mini_lesson` — the cards build one concept in sequence; the last card completes it.
- **First card wins in 3 seconds.** The first front must make the player care immediately — it's the playable's hook.

## End-Card Copy

The end card converts the dopamine into an install. Write:
- `cta_headline` — short, confident, app-anchored (e.g. "Master QuizVerse"). ≤4 words ideal.
- `end_blurb` — one line of value; if a site description exists, ground it in the real product (trimmed to a clean sentence boundary, no dangling punctuation).
- `cta_button` — the action label ("Play QuizVerse Free").

## Output — `script` artifact

Must include:
- `questions[]` — each `{ prompt, options[4], correct_index, tag }` — OR `cards[]` — each `{ front_prompt, back_reveal, tag }` (flashcard_deck)
- `cta_headline`, `end_blurb`, `cta_button`
- `questions_source` — `"llm"` or `"fallback"`
- If LLM-authored: `selected_provider` + `provider_score`

## Success Criteria
- Schema-valid `script`.
- N questions (4 options + one correct each) + end-card copy present.
- If LLM-authored, scoring audit trail recorded.

## Common Pitfalls
- First question too hard — the player bounces before the "I'm smart" beat.
- Ambiguous correct answers or two defensible options.
- End-card blurb truncated mid-word/parenthesis when grounding from a site (trim to a clean boundary).
- Hardcoding the LLM provider instead of routing via scoring.
- Flashcard fronts that give away the reveal — the open loop is the interaction's fuel.

## References

- First 3s must answer "why should this player care"; teach the core loop honestly in 5–10s: https://www.admapix.com/blog/app-going-global/mobile-game-marketing-strategy
