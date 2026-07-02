# Design Director — Playable Pipeline

## When To Use

Third stage. Define the **states, interaction, and layout** of the playable — the equivalent of a scene plan, but for an interactive HTML5 surface rather than a video timeline. Deliverable: the `scene_plan` artifact. This stage is where the **genuine-interactivity** half of the `playable_compliance` gate is designed in.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior | `state.artifacts["script"]` | questions + end-card copy |
| Gate | `pipeline_defs/playable.yaml` `quality_gate` | intent checks: interactive, viewport, has_cta |

## The Anti-Pattern (read first)

A playable that **auto-plays an animation and shows a CTA** is not a playable — it's a video in an iframe, and networks reject it. Every state in your plan must be reached **by a user action**, and the core loop must give **immediate feedback** to that action. If a state advances purely on a timer with no tap, the design fails the gate.

## State Flow (quiz_taste_test)

```
[brand bar: icon + name + FREE pill]  (persistent)
        │
   QUIZ STATE  ──tap an answer──▶  FEEDBACK (correct=green ✓ / wrong=red ✕ + reveal)
        ▲                                   │  (~1.1s)
        └──────── next question ◀───────────┘
        │  (after last question)
        ▼
   END-CARD STATE  ── tap CTA ──▶  store (mraid.open → clickTag → window.open)
   [confetti · "You scored X/N" · headline · blurb · pulsing CTA · store badges]
```

## State Flow (flashcard_deck)

```
[brand bar: icon + name + FREE pill]  (persistent)
        │
   CARD FRONT  ──tap to flip──▶  CARD BACK (reveal + progress dots)
        ▲                              │  tap "next card"
        └──────────────────────────────┘
        │  (after last card)
        ▼
   END-CARD STATE  ── tap CTA ──▶  store (mraid.open → clickTag → window.open)
   ["N cards down — thousands to go" · headline · blurb · pulsing CTA · store badges]
```

Flip is a 3D CSS transform (~400ms, decelerate ease); the flip itself is the feedback. The first card front must state why the player should care within 3 seconds of load.

## Design Rules

- **Portrait, mobile-first.** Full-viewport; assume a phone. Declare the mobile viewport meta (gate check `viewport_meta`).
- **Big tap targets.** Answer buttons span the width, ≥56px tall, reachable one-handed. No tiny hit areas.
- **Immediate feedback.** On tap: correct turns green with a ✓; wrong turns red with a ✕ and reveals the correct option. A short feedback line ("Correct!" / "Close — see the answer").
- **Progress affordance.** Dots/segments show how many questions remain — players finish what they start.
- **One clear CTA.** The end card has exactly one primary action; make it large and gently pulsing. Store badges (App Store / Google Play) reinforce legitimacy.
- **No dead ends.** Every state has a forward path; the last question always lands on the end card.
- **Reduced-motion friendly.** Confetti/pulse are decorative, never required to reach the CTA.

## Compliance Pre-Check (intent)

Before handing off, confirm the plan can satisfy these gate checks at build time:
- `interactive` — the core loop is tap-driven (not timer-driven).
- `viewport_meta` — mobile viewport declared.
- `has_cta` — a single store CTA exists on the end card.

## Output — `scene_plan` artifact

Must include:
- `states[]` — each `{ id, role, interaction, transition_on, transition_to }`
  (e.g. `quiz` → interaction `tap_answer` → `feedback`; `feedback` → `timer_1100ms` → next `quiz`/`end`; `end` → `tap_cta` → `store`)
- `layout` — `portrait`, tap-target sizing, brand-bar spec
- `theme_slots` — accent / accent_soft / bg (filled by the asset stage)
- `compliance_intent` — `{ interactive: true, viewport: true, has_cta: true }`

## Success Criteria
- Schema-valid `scene_plan`.
- Each state names its interaction + transition; no passive auto-play, no dead ends.
- Compliance intent checks are satisfiable by the plan.

## Common Pitfalls
- A state that advances on a timer with no user tap (fails `interactive`).
- Tap targets too small or too low (thumb can't reach one-handed).
- Decorative motion gating the CTA (breaks reduced-motion + slows time-to-CTA).
- Forgetting the mobile viewport meta in the layout spec.
- An opening state that doesn't communicate the game's appeal within 3 seconds.

## References

- Unity playable specs (MRAID 3.0, CTA via mraid.open, single self-contained HTML): https://docs.unity.com/grow/acquire/creatives/playable/specifications
- IAB MRAID standard: https://www.iab.com/guidelines/mobile-rich-media-ad-interface-definitions-mraid/
- First-3-seconds rule + honest core-loop teaching: https://www.admapix.com/blog/app-going-global/mobile-game-marketing-strategy
- Size limits by network: https://playableendcards.com/blog/playable-ad-size-limits-by-network
