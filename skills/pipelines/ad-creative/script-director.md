# Script Director — Ad-Creative Pipeline

## When To Use

Write the ad's copy: a persona-pain hook, specific proof beats, and one CTA — all structured for a muted 9:16 feed where the first 2 seconds decide everything.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["idea"]["brief"]` | Offer, persona, angle, objective |

## Operating Principles

- **The hook is the persona's sentence, not yours.** Use their words from the research ("Still typing invoices by hand?") — recognition is what stops the scroll. On screen by 2s, legible muted.
- **Proof is countable or watchable.** A number ("saves 4 hours a week"), a demo moment (the feature doing the thing), or a named testimonial. Adjectives are not proof.
- **One CTA, stated twice.** Spoken/shown mid-ad once, then owning the end card. Action-led ("Start free — link below"), never brand-led ("Discover our app").

## Structure (15–30s)

```
0–2s   HOOK      persona pain/desire, on-screen text + visual dramatization
2–3s   PRODUCT   the product enters as the answer (visible by 3s)
3–12s  PROOF     2–3 beats: demo moment / number / testimonial
12–15s CTA setup urgency or offer framing ("free this week")
final  END CARD  CTA button copy + offer line, holds ≥1.5s
```
Scale the middle for longer cuts; never stretch the hook.

## Process

### 1. Write 3 hooks, pick 1
One per applicable hook structure (bold claim / curiosity gap / visual shock / direct question), each ≤8 on-screen words in the persona's language. Pick the strongest; keep the runner-up in `metadata.ab_alternates` (pairs with the alternate angle from the brief).

### 2. Write the proof beats
2–3 beats, each one VO line + on-screen text (≤6 words) + the visual evidence instruction. Order: strongest proof first.

### 3. Write the CTA
`cta_text` (≤4 words, action verb first), `offer_line` (the deal framing), destination from the brief. No secondary CTAs anywhere.

### 4. Captions
Word-timed captions from the first word — the ad must fully work muted.

### 5. Build the script artifact
Hook, ordered beats, CTA block. Metadata: `ab_alternates` (hook + angle), `caption_style`, per-platform copy trims if declared.

### Quality Gate
- [ ] Hook ≤8 words, persona-language, works muted by 2s.
- [ ] Product named/shown by 3s in the structure.
- [ ] Every proof beat countable or watchable.
- [ ] Exactly one CTA; end card copy present.
- [ ] A/B alternates recorded.

## Common Pitfalls

- Opening with the brand or product name instead of the pain (the persona doesn't care yet).
- "Revolutionary", "seamless", "powerful" — adjectives where evidence should be.
- A clever hook that doesn't connect to the proof that follows (bait-and-switch reads instantly).

## References

- Hook structures + first-word captions: https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- 2-second hook retention data: https://www.zebracat.ai/post/youtube-shorts-statistics
