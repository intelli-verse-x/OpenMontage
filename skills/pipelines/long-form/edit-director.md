# Edit Director — Long-Form Pipeline

## When To Use

Assemble the chaptered timeline, protect the retention architecture (cold open, interrupts, cliffs), and lock the render runtime. At this length the edit is retention engineering.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `asset_manifest` | Shots + narration |
| Skill | `skills/core/hyperframes.md` | Runtime decision matrix |
| Skill | `skills/meta/bespoke-composition.md` | Atelier-mode bar for hero work |

## Runtime Routing (MANDATORY)

Lock `render_runtime` in `edit_decisions` per `skills/core/hyperframes.md`:
- **cloud adapter** (LongFormVideo compose seam) — default for narration-driven assembly of stock/generated footage at this volume.
- **Remotion** — data-driven segments (charts, timelines, document reveals) and programmatic chapter cards.
- **HyperFrames** — the overlay finishing pass: chapter title cards, lower-thirds, citation cards, end card.

Present both Remotion and HyperFrames at the checkpoint per AGENT_GUIDE. **For hero deliverables (flagship documentary), atelier mode must be explicitly considered; record in `metadata.atelier_considered`.**

## Operating Principles

- **The cold open is untouchable.** Nothing precedes the hook; any branding after it, ≤3s. If the assembled open runs past 60s, cut it down — do not let it grow.
- **Verify beats against the FINAL runtime.** The 25%/65% interrupts were planned against estimates; after assembly, recompute their positions and nudge chapter internals so they land within ±5% of the marks.
- **No segment sags >90s.** At documentary pacing, 90 seconds without a visual grammar change or narrative turn is the sag threshold — insert a cutaway, tighten narration gaps, or split the beat.
- **Cut cadence by pacing class.** `dynamic` explainers ride 3–6s shots; `measured` documentaries hold 6–12s; interviews cut on answer boundaries with reaction inserts.

## Process

### 1. Assemble per chapter
Conform each chapter to its narration file; place evidential b-roll at claim timestamps (the shot proves what's being said *while* it's said, not seconds later).

### 2. Protect the architecture
Cold open first, cliffs preserved at chapter ends, interrupts repositioned against final runtime. Record final chapter boundary timestamps in `metadata.chapter_marks` (publish derives YouTube chapters from these).

### 3. Sag pass
Scrub the full timeline for >90s unchanged stretches; fix each. Trim narration breaths/gaps >0.7s except deliberate dramatic pauses.

### 4. Duration check
Total within ±10% of target. Over → cut whole beats (never speed up narration); under → do NOT pad; report to EP (shorter that holds beats longer that sags).

### 5. Lock runtime
`render_runtime` + rationale + `atelier_considered` + overlay-pass plan recorded.

### Quality Gate
- [ ] Cold open intact; branding ≤3s after the hook.
- [ ] Interrupts at 25%/65% ±5% of final runtime; chapter marks recorded.
- [ ] No >90s sag; b-roll synced to claims.
- [ ] Duration ±10% of target; runtime locked with rationale.

## Common Pitfalls

- Letting a "short intro sequence" creep in front of the hook during assembly.
- B-roll drifting seconds behind the claims it proves.
- Leaving the interrupts where the plan estimated them after the cut changed all timings.
- Padding to hit the target duration — total watch time rewards holding, not lasting.

## References

- First-30s discipline; pattern interrupts: https://prepublish.ai/guides/youtube-retention-guide
- Length benchmarks; watch time as the signal: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
