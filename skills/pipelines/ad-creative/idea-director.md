# Idea Director — Ad-Creative Pipeline

## When To Use

Turn a product/app/offer into an ad `brief`: one persona, one conversion objective, one angle, and the platform variant set. Research grounds the angle — this pipeline inherits trend analysis from its content-factory source.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Skill | `core/research.md` | Trend + competitor-creative research |

## Operating Principles

- **One persona, not an audience.** "Busy parents of toddlers" beats "families". The hook will name their pain in their words — you can't do that for three personas at once.
- **The objective is a metric.** Install, sign-up, purchase, lead. Everything (angle, proof, CTA) serves the one metric the brief names.
- **Angles are hypotheses.** The angle you choose is a testable position; name the alternates in the decision log so publish can set up the next A/B iteration.

## Process

### 1. Research
`core/research.md`: what ad creatives currently run in this category (competitor angles), what the persona complains about in their own words (reviews, forums, subreddit language), trending formats on the target platforms. Record sources in `decision_log`.

### 2. Define offer + persona + objective
Offer (the product + the deal framing, e.g. "free trial"), one persona with their pain stated in their language, one conversion objective with its CTA destination URL.

### 3. Choose the angle
| Angle | Opens with | Best when |
|-------|-----------|-----------|
| `pain-first` | the persona's frustration dramatized | the pain is felt daily and recognizable in 1s |
| `desire-first` | the after-state (what life looks like with it) | aspiration outsells relief (fitness, finance goals) |
| `social-proof` | numbers/testimonial ("2M users…") | the product is established; skepticism is the barrier |
| `demo-first` | the product doing the impressive thing | the demo IS the hook (visual tools, games, gadgets) |

Record the runner-up angle as the A/B alternate.

### 4. Declare platforms + variants
Primary 9:16 (Reels/TikTok/Shorts feeds); declare 1:1 / 16:9 only where media plans need them. Duration target within [15, 30]s.

### 5. Build the brief
Fields: offer, persona (+ pain in their words), objective + CTA destination, angle (+ alternate), platform variants, duration, tone, references.

### Quality Gate
- [ ] One persona with pain stated in their language.
- [ ] One measurable objective + CTA destination.
- [ ] Angle chosen from research; alternate recorded.
- [ ] Variants + duration declared.

## Common Pitfalls

- A "persona" that is a demographic instead of a pain.
- Choosing demo-first when the demo needs 10 seconds of context (that's an explainer, not an ad hook).
- No alternate angle recorded — the second variant is where performance ads actually get optimized.
