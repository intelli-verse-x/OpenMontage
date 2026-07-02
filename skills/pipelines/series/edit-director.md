# Edit Director — Series Pipeline

## When To Use

Assemble each episode's timeline (intro → body → recap/teaser), enforce series-wide consistency, and lock the render runtime. Episode edits are individually good AND collectively uniform.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `asset_manifest`, arc style bible | What to cut |
| Skill | `skills/core/hyperframes.md` | Runtime decision matrix |
| Skill | `skills/meta/bespoke-composition.md` | Atelier-mode bar for hero work |

## Runtime Routing (MANDATORY)

Choose and lock `render_runtime` in `edit_decisions` per the decision matrix in `skills/core/hyperframes.md`:

- **Remotion** — the natural fit for series: one composition parameterized per episode (data-driven episodes, uniform lower-thirds/chapter markers from props).
- **HyperFrames** — design-led episodes or the planned finishing pass (chapter markers, quiz cards, end cards as GSAP overlays).
- **cloud adapter** (content-factory Learning/TV series compose seam) — when episode assets are cloud-generated clips and composition is assembly.

Per AGENT_GUIDE, present both Remotion and HyperFrames at the checkpoint; never silently substitute. **For hero deliverables (pilot episode, flagship series), atelier mode must be explicitly considered and the decision recorded in `metadata.atelier_considered`.**

## Operating Principles

- **First 30s carries the episode.** The hook beat opens cold; series branding appears after the hook, small and brief (≤2s bumper max, never before the hook).
- **Uniform episode grammar.** Same intro length, same lower-third timing, same recap/teaser shape across episodes — viewers learn the rhythm.
- **Cut on information.** Trim dialogue/narration gaps; podcast format especially benefits from tightening (remove >0.5s inter-speaker gaps unless dramatic).

## Process

### 1. Assemble per episode
Hook (cold open) → optional ≤2s bumper → body beats with b-roll/insert cuts → recap/teaser → CTA/end card. Verify the re-engagement beats land at ~25%/~65% of the final runtime, not the planned runtime.

### 2. Apply the series grammar
Timing constants from the style bible (bumper length, lower-third in/out, transition vocabulary). Record them once in `edit_decisions.metadata.series_grammar` and reference per episode.

### 3. Overlay pass plan
Mark which overlays compose renders natively vs the HyperFrames finishing pass (chapter markers at chapter starts, quiz cards after concepts, end card final 5s).

### 4. Verify durations
Each episode within ±10% of the arc's per-episode target; flag any episode >15% over for trim (retention benchmarks punish padded episodes).

### 5. Lock runtime
`render_runtime` + rationale + `atelier_considered` recorded.

### Quality Gate
- [ ] Every episode: cold-open hook, bumper ≤2s after the hook, uniform grammar.
- [ ] Re-engagement beats at ~25%/~65% of final runtime.
- [ ] Podcast gaps tightened; no dead air.
- [ ] Durations within target; runtime locked with rationale.

## Common Pitfalls

- A 5s branded intro before the hook — the first-30s drop is where series die.
- Episode 4 discovering a "better" lower-third timing — grammar changes are arc-level decisions.
- Measuring re-engagement beat placement against the planned duration instead of the cut timeline.

## References

- First-30s retention drop; >40% = weak hook: https://prepublish.ai/guides/youtube-retention-guide
- Benchmarks by length (don't pad): https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
