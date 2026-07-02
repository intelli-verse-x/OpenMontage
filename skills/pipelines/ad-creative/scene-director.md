# Scene Director — Ad-Creative Pipeline

## When To Use

Turn the ad script into a shot plan: pain dramatization, product entry, proof visuals, and end card — composed for 9:16 first with reframe intent for other variants. Carries the **anti-slideshow hard gate**.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]` | Beats + copy |
| Gate | `lib/slideshow_risk.py` | Anti-slideshow scoring |

## Operating Principles

- **The hook shot dramatizes, never illustrates.** Show the pain happening (the frustrated action, the mess, the wasted time) — not a person looking sad next to on-screen text.
- **Product by 3 seconds.** The product's first appearance is a planned shot with its own intent (the "enter as the answer" moment), not a logo watermark.
- **Design 9:16 native, reframe-aware.** Compose the primary vertically; mark each shot's safe-crop center so 1:1/16:9 variants reframe (subject re-centered) instead of letterbox.
- **Safe zones are law.** Text/CTA out of the top ~200px, bottom ~300px, right ~120px on 1080×1920.

## Process

### 1. Map beats → shots
Hook (1 shot, dramatized action), product entry (1 shot), proof beats (1 shot each — the demo moment framed tight on the evidence), CTA setup, end card. Each shot: `information_role`, `shot_intent`, framing, action, text block + position, est duration, **crop_center** for variant reframes.

### 2. Proof shots are macro-true
Demo shots show the real interface/product behavior at legible scale (UI shots: zoom to the interaction, not full-screen app). Numbers get a dedicated text treatment shot or overlay.

### 3. End card
Product + CTA button copy + offer line; static-stable (it must hold ≥1.5s and read as a tap target); brand colors.

### 4. Score the plan
`score_slideshow_risk`; `fail` → rework motion/dramatization before submitting.

### Quality Gate
- [ ] Hook shot dramatizes the pain as action.
- [ ] Product entry shot within the first 3s of the timeline.
- [ ] Every shot has `information_role` + `shot_intent` + crop_center.
- [ ] All text inside safe zones; end card holds ≥1.5s.
- [ ] Slideshow verdict ≥ acceptable.

## Common Pitfalls

- Hook shots that are stock-photo sadness instead of the pain in motion.
- Proof shots so wide the evidence is illegible on a phone.
- Forgetting crop_center, forcing letterboxed variants at compose.

## References

- Safe zones (1080×1920 bands): https://zeely.ai/blog/tiktok-safe-zones/
- Motion principles for text/product moves: https://blog.vmgstudios.com/10-principles-motion-design
