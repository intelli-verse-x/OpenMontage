# Idea Director — Long-Form Pipeline

## When To Use

Turn a topic into a long-form `brief`: content type, one-sentence thesis, target duration/chapters, and the audience whose retention expectations calibrate everything downstream.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Skill | `core/research.md` | Topic research (mandatory for documentary/deep-dive claims) |
| Manifest | `pipeline_defs/long-form.yaml` `metadata.content_types` | Type presets |

## Operating Principles

- **The thesis is a question worth 30 minutes.** If it can be answered in 60 seconds, it's a short. State it as one sentence the whole video answers ("Why did the fastest-growing city in history empty out in a decade?").
- **Length is a cost the content must pay for.** Choose the content type whose preset duration the material genuinely fills; retention benchmarks drop with length (10–15min holds 40–50%, 15+min 35–45%).
- **Research before structure.** Documentary/deep-dive claims need sources at idea time — the chapter plan is built on what the research actually supports.

## Process

### 1. Research
`core/research.md`: the topic's strongest surprising facts, the open question, existing coverage (what's been done, what angle is unclaimed). Record sources in `decision_log` — these become the script's citations.

### 2. State the thesis
One sentence, framed as a question or a claim with stakes. Test: does every planned chapter serve it?

### 3. Choose the content type
Match to the material: `documentary` (narrative journalism), `educational` (teach a skill/domain), `explainer` (demystify one system), `interview` (conversation-led), `deep_dive` (expert-level analysis). Inherit the preset duration/chapters/pacing; override only with justification.

### 4. Identify the audience + retention expectation
Who watches 30 minutes of this? Note the length-matched retention benchmark in the brief so downstream stages calibrate (an interview at 25–35% on 60 minutes is strong; an explainer at 35% on 15 minutes is weak).

### 5. Build the brief
Fields: thesis, content_type, target_minutes, chapter_count, pacing, audience, key research findings + sources, platform, narrator voice preference (professional_male / professional_female / warm_friendly / authoritative).

### Quality Gate
- [ ] Thesis is one sentence with stakes.
- [ ] Content type preset matched to material; duration justified.
- [ ] Research findings + sources recorded.
- [ ] Audience + length-matched retention expectation stated.

## Common Pitfalls

- A topic ("the history of X") instead of a thesis (a question with tension).
- Choosing deep_dive length for explainer material — padding kills gradual-decline retention.
- Skipping research and letting the chapter plan invent structure the facts won't support.

## References

- Length-matched retention benchmarks: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
