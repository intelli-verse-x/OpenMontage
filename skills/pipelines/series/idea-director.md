# Idea Director — Series Pipeline

## When To Use

Turn a topic or premise into a series `brief`: format, episode count, per-episode duration, recurring hosts/characters, and the arc theme. The brief is the contract every later stage inherits.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/brief.schema.json` | Artifact validation |
| Skill | `core/research.md` | Topic/audience research |
| Playbook | `clean-professional` or `flat-motion-graphics` | Style envelope |

## Operating Principles

- **A series is a promise repeated.** The premise must state what every episode reliably delivers ("each episode demystifies one ML concept in 5 minutes").
- **Episode count is earned.** Only as many episodes as there are distinct objectives; 6 strong episodes beat 12 padded ones.
- **Personas before scripts.** Hosts/characters (or podcast host+guest pairs) are defined here so the voice never drifts.

## Process

### 1. Research
Use `core/research.md`: audience, existing series in the niche, what episode lengths perform for this content class (retention benchmarks: <5min episodes hold 65–75%, 5–10min 50–60%, 10–15min 40–50%). Record sources in `decision_log`.

### 2. Choose the format
- `learning` — curriculum series; declare the pedagogy ratio (e.g. recap/assessment every 4th episode) and per-episode learning objective style.
- `drama` — narrative series; declare the season arc shape and cliffhanger policy.
- `recap` — recurring-segment series; declare the segment template.
- `podcast` — dialogue series; declare host persona, guest persona (or rotating guests), and the dialogue dynamic (interviewer/expert, debate, co-hosts).

### 3. Size the series
Episode count + per-episode duration, justified by the objectives list and the retention benchmark for that length. State target platform(s).

### 4. Define recurring elements
Hosts/characters with names, voice character, and visual treatment; recurring segments; the CTA pattern (subscribe vs next-episode tease).

### 5. Declare locales (optional)
If the series will ship in multiple languages, list target locales now — publish will hand off to the `localization-dub` pipeline.

### 6. Build the brief
Fields: premise, format, episode_count, per_episode_duration, audience, personas, arc theme, CTA/learning objective, locales, platform, references.

### Quality Gate
- [ ] Premise states the repeatable per-episode promise.
- [ ] Format + personas fully declared (podcast: both sides of the dialogue).
- [ ] Episode count justified by distinct objectives.
- [ ] Duration matched to a retention-benchmark-informed target.

## Common Pitfalls

- A season-long topic with no per-episode promise ("a series about history").
- Podcast format without a defined dynamic — two agreeing voices is radio silence.
- Choosing 15-minute episodes for content that benchmarks show holds best at 6.

## References

- Retention benchmarks by video length: https://humbleandbrag.com/blog/youtube-audience-retention-benchmarks
