# Script Director — Series Pipeline

## When To Use

Write every episode's script from the arc: per-episode hook, body beats, recap/teaser, and CTA/learning checkpoint. For `podcast` format, write the dialogue for both personas.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["arc"]["scene_plan"]` | Episode objectives + beats + continuity hooks |
| Playbook | Active style playbook | Tone constraints |

## Operating Principles

- **Every episode earns its own first 30 seconds.** Open on the episode's key insight or dramatic question — never a series intro or channel branding. The steepest retention drop happens here; >40% drop in the first 30s means the hook failed.
- **Continuity is written, not implied.** Recaps quote what actually happened; teasers name what's actually next.
- **Dialogue has friction (podcast).** Host and guest must want slightly different things from the exchange (curiosity vs precision, skepticism vs enthusiasm) — write the dynamic, not alternating monologues.

## Process

### 1. Per-episode hook (first 30s)
Key insight or question first, in the episode's own terms. A returning viewer should still feel forward motion; a new viewer should not feel lost.

### 2. Body beats
Follow the arc outline. Each beat: VO/dialogue + on-screen support + visual note. Insert the planned re-engagement beats at ~25% and ~65% (question to viewer, segment change, visual shift).

### 3. Recap + teaser
- Recap (≤2 lines): callback to the previous episode's payoff.
- Teaser (1 line): concrete promise for the next episode ("Next: the failure mode nobody tests for").

### 4. CTA / learning checkpoint
- `learning`: end on a checkpoint question the viewer can answer if the episode worked; note where quiz-card overlays land.
- `drama`: cliffhanger per the arc's policy.
- All formats: one CTA, next-episode-oriented.

### 5. Build the script artifact
Ordered beats for every episode. Metadata: per-episode hooks list, continuity map (episode → recap/teaser text), dialogue personas (podcast), checkpoint questions (learning).

### Quality Gate
- [ ] Every episode opens on its own hook; zero series-intro openings.
- [ ] Recaps/teasers reference real adjacent content.
- [ ] Re-engagement beats present at ~25%/~65% per episode.
- [ ] Podcast dialogue has a stated dynamic, not alternating lectures.
- [ ] Sound-off legibility: key claims also appear as on-screen text.

## Common Pitfalls

- "Welcome back to the series where…" — the classic first-30s killer.
- Teasers that promise vaguely ("more great stuff next time").
- Learning episodes that end without a checkpoint — retention across episodes depends on tested progress.

## References

- First-30s drop; lead with key insight (+15–20pp retention past 30s): https://prepublish.ai/guides/youtube-retention-guide
- Re-engagement beats at 25%/65% marks: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
