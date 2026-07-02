# Edit Director — Ad-Creative Pipeline

## When To Use

Assemble the ad timeline: hook → product → proof → CTA within [15, 30]s, apply the beat-synced ad preset when music-driven, and lock the render runtime.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `asset_manifest` | Shots + audio |
| Manifest | `pipeline_defs/ad-creative.yaml` `metadata.beat_sync_preset` | Ad sync parameters |
| Skill | `skills/core/hyperframes.md` | Runtime decision matrix |
| Skill | `skills/meta/bespoke-composition.md` | Atelier-mode bar for hero work |

## Runtime Routing (MANDATORY)

Lock `render_runtime` in `edit_decisions` per `skills/core/hyperframes.md`:
- **Remotion** — the natural fit for ad variants: one composition, props-driven angle/hook/aspect variants (A/B iteration without re-editing).
- **HyperFrames** — design-led end cards and kinetic-text hooks (GSAP choreography).
- **cloud adapter** (IdeaToAd compose seam) — assembly of cloud-generated footage.

Present both Remotion and HyperFrames at the checkpoint per AGENT_GUIDE. **For hero deliverables (flagship campaign creative), atelier mode must be explicitly considered; record in `metadata.atelier_considered`.**

## Operating Principles

- **The hook owns 0–2s, the product owns second 3.** Nothing before the hook; no logo stings.
- **Beat-synced when music-driven.** Ad preset: `energy_threshold 0.5` (major beats only), `min_interval 1.5s` (faster floor than music video), hard cuts, **cut ~100ms before the beat**. Proof-beat impacts land on beats; the CTA entrance hits a beat.
- **The end card is a hold, not a flash.** ≥1.5s static-stable so the CTA registers as a tappable action.
- **Trim to proof.** Each proof shot ends the frame after its evidence lands.

## Process

### 1. Assemble
Hook (0–2s) → product entry (by 3s) → proof beats (strongest first) → CTA setup → end card. Verify against the script structure.

### 2. Beat pass (music-driven cuts)
Extract beats from the final music at the ad preset; snap proof impacts and the CTA entrance to beats (100ms early); don't force the hook cut to a beat if it costs hook time.

### 3. Caption timing
Word-timed from 0:00; emphasis words synced to cuts.

### 4. Duration + variant map
Total ∈ [15, 30]s. Record per-shot crop_center reframe instructions for each declared aspect variant in `metadata.variant_reframes`.

### 5. Lock runtime
`render_runtime` + rationale + `atelier_considered` recorded.

### Quality Gate
- [ ] Hook 0–2s, product by 3s, end card ≥1.5s.
- [ ] Beat preset applied where music-driven; impacts on beats, cut 100ms early.
- [ ] Captions from first word; duration in window.
- [ ] Variant reframe map recorded; runtime locked with rationale.

## Common Pitfalls

- A brand sting before the hook (instant scroll).
- Cutting the end card short to fit the window — cut a proof beat instead.
- Beat-syncing the hook at the cost of its 2-second deadline.

## References

- Cut-before-beat anticipation practice: https://www.reddit.com/r/premiere/comments/1nomnj0/whats_your_go_to_method_for_finding_the_rhythm/
- Completion/replay weighting: https://www.digitalapplied.com/blog/short-form-video-strategy-shorts-tiktok-reels-2026
