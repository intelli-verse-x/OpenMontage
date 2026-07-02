# Asset Director — Ad-Creative Pipeline

## When To Use

Resolve every shot: pain-dramatization footage, faithful product shots, proof visuals, VO, music, and captions. All generation routes through selectors scored by `lib/scoring.py`.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `scene_plan`, `script`, `brief` | Shots + copy + product refs |
| Tools | `video_selector` (required), `image_selector`, `tts_selector`, `music_gen`, `subtitle_gen` | Resolution |
| Scoring | `lib/scoring.py` | Provider routing + audit trail |

## Operating Principles

- **Product shots are faithful or they're liability.** The product/app as it actually looks and behaves — real screenshots/screen recordings preferred; generated product imagery must not invent features or results (ad-policy rejection + trust damage). Lifestyle/context footage may be generated freely.
- **Muted-first mix.** Captions from the first word; VO reinforces; music energizes but never carries information.
- **Native 9:16 assets.** Generate vertical; respect each shot's crop_center for variant reframes.

## Process

### 1. Product/proof assets
Real captures first (screen recordings for app demos at the interaction zoom the scene plan specifies; product photography if supplied). Numbers/testimonials: verify against the brief's research before styling them.

### 2. Dramatization footage
`video_selector` (scored) for hook/lifestyle shots. Prompts carry the action ("hands frantically sorting receipts, kitchen table, overhead") — the pain in motion.

### 3. VO
`tts_selector`: energetic, conversational read; slightly faster than explainer pace. One voice.

### 4. Music + SFX
`music_gen`: high-energy bed matching the angle's tone; if the edit will be beat-synced, the track needs clear percussive beats (the ad preset detects at energy_threshold 0.5). Hook-moment SFX accent optional.

### 5. Captions
`subtitle_gen` word-timed from the VO, starting at 0:00, delivered as data for compose (placement is compose's job).

### 6. Budget
$1.00 default is tight: real captures are free, spend generation budget on the hook shot first (it carries the ad), lifestyle b-roll second.

### Quality Gate
- [ ] Product/demo assets faithful; no invented features/results.
- [ ] Every shot resolved at 9:16 with crop_center respected.
- [ ] VO single voice; music has detectable beats if beat-sync planned.
- [ ] Word-timed captions from 0:00.
- [ ] `selected_provider` + `provider_score` on every generated asset; spend ≤ budget.

## Common Pitfalls

- Generating the app UI instead of capturing it (uncanny UI reads as scam).
- A music bed with no percussive definition, breaking the beat-synced edit downstream.
- Spending the budget on lifestyle b-roll and starving the hook shot.
