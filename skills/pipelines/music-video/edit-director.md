# Edit Director — Music-Video Pipeline

## When To Use

Build the beat-synced timeline: extract the beat map from the final audio, place cuts and action impacts against it, and lock the render runtime. This is the stage that makes it a *music* video.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `asset_manifest` (with final audio) | Shots + beat source |
| Manifest | `pipeline_defs/music-video.yaml` `metadata.beat_sync` | Sync parameters |
| Skill | `skills/core/hyperframes.md` | Runtime decision matrix |
| Skill | `skills/meta/bespoke-composition.md` | Atelier-mode bar for hero work |

## Beat-Sync Parameters (from the manifest)

| Parameter | Value | Meaning |
|-----------|-------|---------|
| `energy_threshold` | 0.35 | Sensitive detection — music videos want a rich beat map |
| `min_interval_s` | 2.0 | Floor between cuts; choruses may approach it, verses shouldn't |
| `transition_style` | hard_cut | Default; crossfades only for section dissolves the treatment asks for |
| `visual_anticipation_ms` | 100 | **Cut ~100ms BEFORE the beat** — vision registers before audio, so an early cut *feels* on-beat |
| `mask_start_s` / `mask_end_s` | 0.5 / 1.0 | Ignore intro/outro edges when detecting |

## Runtime Routing (MANDATORY)

Lock `render_runtime` in `edit_decisions` per `skills/core/hyperframes.md`:
- **cloud adapter** (Song2MusicVideo compose seam) — the default when shots are cloud-generated clips and composition is beat-aligned assembly.
- **Remotion** — lyric-video variants and data-driven text choreography (word-timed lyric systems).
- **HyperFrames** — design-led overlay passes (title cards, stylized lyric moments).

Present both Remotion and HyperFrames options at the checkpoint per AGENT_GUIDE. **For hero deliverables, atelier mode must be explicitly considered; record the decision in `metadata.atelier_considered`.**

## Process

### 1. Extract the beat map
From the FINAL audio (assert `audio_final`). Detect beats with the manifest parameters; snap the section boundaries (chorus entries, drops) from the treatment onto detected beats.

### 2. Place the cuts
- Section boundaries first: chorus entries cut on the drop (100ms early).
- Then per-section: place each shot's **impact moment** on a beat; let the cut fall where the action demands, not on every beat.
- Cut density follows the energy curve — verses hold (≥3–4s), choruses tighten (toward the 2.0s floor).
- Vary it: an unbroken run of on-beat cuts longer than ~4 bars starts reading as wallpaper; break the pattern with a held shot or an off-beat action.

### 3. Escalate the choruses
Chorus 2 cuts faster than chorus 1; the final chorus gets the widest/strangest shots AND the fastest cadence. Verify against the treatment's escalation ladder.

### 4. Trim to the impact
Start each clip so its action's impact frame lands exactly on its assigned beat (minus 100ms). Kill dead frames before the action.

### 5. Record edit_decisions
Beat map reference, per-cut timestamps + beat indices, section map, anticipation offset, runtime lock + rationale, `atelier_considered`, and the vertical-cut section's in/out points for publish.

### Quality Gate
- [ ] Beat map from final audio; all cuts reference beat indices.
- [ ] Cuts placed 100ms before their beats.
- [ ] Cut density traces the energy curve; not every beat is cut.
- [ ] Chorus escalation audible AND visible.
- [ ] Runtime locked; atelier considered for hero work.

## Common Pitfalls

- Cutting exactly ON the beat — it reads late; anticipate by ~100ms.
- Metronome editing (every beat, whole song) — rhythm dies without contrast.
- Trimming clips from the front arbitrarily so the impact frame misses its beat.
- Re-using the verse cadence in the final chorus (flat ending).

## References

- Cut before the beat / sync actions not just cuts: https://www.reddit.com/r/premiere/comments/1nomnj0/whats_your_go_to_method_for_finding_the_rhythm/
- Beat-marker workflow: https://www.youtube.com/watch?v=yU3U6TdV5Hw
